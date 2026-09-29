import Foundation
import os

/// How the main thread talks to the audio thread: a handful of numbers behind a lock that the audio
/// thread only ever *tries*. If the main thread happens to hold it, the audio thread keeps the values
/// it already has for another few milliseconds, which nobody can hear; it never waits.
final class ParameterMailbox: @unchecked Sendable {
    private let lock: UnsafeMutablePointer<os_unfair_lock>
    private let levels: UnsafeMutablePointer<Float>
    private var master: Float = 0
    private var ramp: Float = 0
    private var version: UInt32 = 0
    private let count = Sound.all.count

    init() {
        lock = .allocate(capacity: 1)
        lock.initialize(to: os_unfair_lock())
        levels = .allocate(capacity: Sound.all.count)
        levels.initialize(repeating: 0, count: Sound.all.count)
    }

    deinit {
        lock.deallocate()
        levels.deallocate()
    }

    /// Main thread. `levels` is one 0...1 value per sound, in `Sound.all` order.
    func publish(levels newLevels: [Float], master newMaster: Float, rampSeconds: Float) {
        os_unfair_lock_lock(lock)
        for i in 0..<min(count, newLevels.count) { levels[i] = newLevels[i] }
        master = newMaster
        ramp = rampSeconds
        version &+= 1
        os_unfair_lock_unlock(lock)
    }

    /// Audio thread. Returns false when there is nothing new or the lock was busy.
    func read(levels out: UnsafeMutablePointer<Float>, master outMaster: inout Float, ramp outRamp: inout Float,
              seen: inout UInt32) -> Bool {
        guard os_unfair_lock_trylock(lock) else { return false }
        defer { os_unfair_lock_unlock(lock) }
        guard version != seen else { return false }
        for i in 0..<count { out[i] = levels[i] }
        outMaster = master
        outRamp = ramp
        seen = version
        return true
    }
}

/// Mixes every active sound into a stereo buffer. Built for the audio thread: after `init` it
/// allocates nothing.
final class MixRenderer {
    private static let chunk = 256

    let sampleRate: Float
    private let mailbox: ParameterMailbox
    private let kernels: ContiguousArray<NoiseKernel>
    private let voiceCount = Sound.all.count

    private let targetLevels: UnsafeMutablePointer<Float>
    private let currentLevels: UnsafeMutablePointer<Float>
    private let trims: UnsafeMutablePointer<Float>
    private let scratchLeft: UnsafeMutablePointer<Float>
    private let scratchRight: UnsafeMutablePointer<Float>
    private let pendingLeft: UnsafeMutablePointer<Float>
    private let pendingRight: UnsafeMutablePointer<Float>
    private var pendingPosition = MixRenderer.chunk

    private let levelSmoothing: Float
    private var seenVersion: UInt32 = .max
    private var firstSync = true

    private var masterGain: Float = 0
    private var masterTarget: Float = 0
    private var masterStep: Float = 0
    private var masterFramesLeft = 0

    init(sampleRate: Float, mailbox: ParameterMailbox, seed: UInt64 = UInt64.random(in: 1...UInt64.max)) {
        self.sampleRate = sampleRate
        self.mailbox = mailbox

        var built = ContiguousArray<NoiseKernel>()
        for sound in Sound.all {
            built.append(sound.makeKernel(channel: 0, sampleRate: sampleRate, seed: seed))
            built.append(sound.makeKernel(channel: 1, sampleRate: sampleRate, seed: seed))
        }
        kernels = built

        let n = Sound.all.count
        targetLevels = .allocate(capacity: n)
        currentLevels = .allocate(capacity: n)
        trims = .allocate(capacity: n)
        targetLevels.initialize(repeating: 0, count: n)
        currentLevels.initialize(repeating: 0, count: n)
        for (i, s) in Sound.all.enumerated() { trims[i] = LoudnessTrim.gain(for: s) }
        scratchLeft = .allocate(capacity: MixRenderer.chunk)
        scratchRight = .allocate(capacity: MixRenderer.chunk)
        scratchLeft.initialize(repeating: 0, count: MixRenderer.chunk)
        scratchRight.initialize(repeating: 0, count: MixRenderer.chunk)
        pendingLeft = .allocate(capacity: MixRenderer.chunk)
        pendingRight = .allocate(capacity: MixRenderer.chunk)
        pendingLeft.initialize(repeating: 0, count: MixRenderer.chunk)
        pendingRight.initialize(repeating: 0, count: MixRenderer.chunk)

        levelSmoothing = 1 - expf(-1 / (0.05 * sampleRate))
    }

    deinit {
        targetLevels.deallocate(); currentLevels.deallocate(); trims.deallocate()
        scratchLeft.deallocate(); scratchRight.deallocate()
        pendingLeft.deallocate(); pendingRight.deallocate()
    }

    /// Whatever size of buffer the hardware asks for, the sound is always synthesised in blocks of
    /// exactly `chunk` frames and handed out from there, so it never depends on the route or the
    /// device's buffer size.
    func render(frames: Int, left: UnsafeMutablePointer<Float>, right: UnsafeMutablePointer<Float>) {
        var offset = 0
        while offset < frames {
            if pendingPosition == MixRenderer.chunk {
                renderChunk(pendingLeft, pendingRight)
                pendingPosition = 0
            }
            let n = min(MixRenderer.chunk - pendingPosition, frames - offset)
            memcpy(left + offset, pendingLeft + pendingPosition, n * MemoryLayout<Float>.size)
            memcpy(right + offset, pendingRight + pendingPosition, n * MemoryLayout<Float>.size)
            pendingPosition += n
            offset += n
        }
    }

    private func syncParameters() {
        var master: Float = 0
        var ramp: Float = 0
        guard mailbox.read(levels: targetLevels, master: &master, ramp: &ramp, seen: &seenVersion) else { return }
        if firstSync {
            firstSync = false
            for i in 0..<voiceCount { currentLevels[i] = targetLevels[i] }
        }
        // A level change re-publishes the same master; only a *new* master starts a new ramp, so a
        // fade already under way is not cut short.
        guard master != masterTarget else { return }
        masterTarget = master
        let frames = Int(ramp * sampleRate)
        if frames <= 0 {
            masterGain = master
            masterFramesLeft = 0
        } else {
            masterStep = (master - masterGain) / Float(frames)
            masterFramesLeft = frames
        }
    }

    private func renderChunk(_ left: UnsafeMutablePointer<Float>, _ right: UnsafeMutablePointer<Float>) {
        let n = MixRenderer.chunk
        syncParameters()
        memset(left, 0, n * MemoryLayout<Float>.size)
        memset(right, 0, n * MemoryLayout<Float>.size)

        let smoothing = levelSmoothing
        for s in 0..<voiceCount {
            let target = targetLevels[s]
            var current = currentLevels[s]
            if target == 0 && current < 0.00001 {
                currentLevels[s] = 0
                continue
            }
            kernels[s * 2].render(scratchLeft, frames: n)
            kernels[s * 2 + 1].render(scratchRight, frames: n)
            let trim = trims[s]
            for i in 0..<n {
                current += smoothing * (target - current)
                let g = current * current * trim
                left[i] += scratchLeft[i] * g
                right[i] += scratchRight[i] * g
            }
            currentLevels[s] = current
        }

        for i in 0..<n {
            if masterFramesLeft > 0 {
                masterGain += masterStep
                masterFramesLeft -= 1
                if masterFramesLeft == 0 { masterGain = masterTarget }
            }
            let g = masterGain * masterGain
            left[i] = MixRenderer.softClip(left[i] * g)
            right[i] = MixRenderer.softClip(right[i] * g)
        }
    }

    /// Linear up to 0.72, then a smooth shoulder that never reaches 1. A stack of loud layers bends
    /// instead of clipping.
    @inline(__always)
    static func softClip(_ x: Float) -> Float {
        let a = abs(x)
        if a <= 0.72 { return x }
        let y = 0.72 + 0.28 * tanhf((a - 0.72) * (1 / 0.28))
        return x < 0 ? -y : y
    }
}
