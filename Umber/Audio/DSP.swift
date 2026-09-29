import Foundation

/// A fast generator with a period of 2^64 - 1: at 48 kHz that is longer than the age of the universe,
/// which is what "never loops" means here. Not for cryptography.
struct FastRandom {
    private var state: UInt64

    init(seed: UInt64) {
        var z = seed &+ 0x9E37_79B9_7F4A_7C15
        z = (z ^ (z >> 30)) &* 0xBF58_476D_1CE4_E5B9
        z = (z ^ (z >> 27)) &* 0x94D0_49BB_1331_11EB
        state = (z ^ (z >> 31)) | 1
    }

    @inline(__always)
    mutating func nextBits() -> UInt32 {
        state ^= state >> 12
        state ^= state << 25
        state ^= state >> 27
        return UInt32(truncatingIfNeeded: (state &* 0x2545_F491_4F6C_DD1D) >> 32)
    }

    /// Uniform in [-1, 1).
    @inline(__always)
    mutating func bipolar() -> Float {
        Float(Int32(bitPattern: nextBits())) * (1.0 / 2_147_483_648.0)
    }

    /// Uniform in [0, 1).
    @inline(__always)
    mutating func unit() -> Float {
        Float(nextBits() >> 8) * (1.0 / 16_777_216.0)
    }
}

struct OnePole {
    private var a: Float
    private var z: Float = 0

    init(cutoff: Float, sampleRate: Float) {
        a = OnePole.coefficient(cutoff: cutoff, sampleRate: sampleRate)
    }

    static func coefficient(cutoff: Float, sampleRate: Float) -> Float {
        1 - expf(-2 * Float.pi * min(cutoff, sampleRate * 0.45) / sampleRate)
    }

    mutating func setCutoff(_ cutoff: Float, sampleRate: Float) {
        a = OnePole.coefficient(cutoff: cutoff, sampleRate: sampleRate)
    }

    @inline(__always)
    mutating func lowpass(_ x: Float) -> Float {
        z += a * (x - z)
        return z
    }

    @inline(__always)
    mutating func highpass(_ x: Float) -> Float {
        z += a * (x - z)
        return x - z
    }
}

/// Band-pass with constant 0 dB peak gain (RBJ cookbook), transposed direct form II.
struct Biquad {
    private var b0: Float
    private var b2: Float
    private var a1: Float
    private var a2: Float
    private var z1: Float = 0
    private var z2: Float = 0

    init(bandpass frequency: Float, q: Float, sampleRate: Float) {
        let w0 = 2 * Float.pi * min(frequency, sampleRate * 0.45) / sampleRate
        let alpha = sinf(w0) / (2 * q)
        let a0 = 1 + alpha
        b0 = alpha / a0
        b2 = -alpha / a0
        a1 = -2 * cosf(w0) / a0
        a2 = (1 - alpha) / a0
    }

    @inline(__always)
    mutating func process(_ x: Float) -> Float {
        let y = b0 * x + z1
        z1 = -a1 * y + z2
        z2 = b2 * x - a2 * y
        return y
    }
}

/// Chamberlin state-variable filter, band-pass output. Stable for cutoffs below fs/6, which every use here is.
struct StateVariableBandpass {
    private var low: Float = 0
    private var band: Float = 0
    private var f: Float = 0.1
    private var damping: Float

    init(q: Float) {
        damping = 1 / q
    }

    mutating func setCutoff(_ cutoff: Float, sampleRate: Float) {
        f = 2 * sinf(Float.pi * min(cutoff, sampleRate / 6.5) / sampleRate)
    }

    @inline(__always)
    mutating func process(_ x: Float) -> Float {
        low += f * band
        let high = x - low - damping * band
        band += f * high
        return band
    }
}

/// A slow, never-repeating wobble in 0...1: two sines of unrelated periods whose phases and
/// periods are picked at random, so no two listeners (or two channels) hear the same swell.
struct SlowDrift {
    private var phaseA: Float
    private var phaseB: Float
    private let stepA: Float
    private let stepB: Float

    init(periodA: Float, periodB: Float, sampleRate: Float, rng: inout FastRandom) {
        phaseA = rng.unit() * 2 * Float.pi
        phaseB = rng.unit() * 2 * Float.pi
        stepA = 2 * Float.pi / (periodA * (0.85 + 0.3 * rng.unit()) * sampleRate)
        stepB = 2 * Float.pi / (periodB * (0.85 + 0.3 * rng.unit()) * sampleRate)
    }

    /// Advance by `frames` samples and return the value at the end.
    @inline(__always)
    mutating func advance(_ frames: Int) -> Float {
        phaseA += stepA * Float(frames)
        phaseB += stepB * Float(frames)
        if phaseA > 2 * Float.pi { phaseA -= 2 * Float.pi }
        if phaseB > 2 * Float.pi { phaseB -= 2 * Float.pi }
        return 0.5 + 0.34 * sinf(phaseA) + 0.16 * sinf(phaseB)
    }
}
