import Foundation

enum AudioEvent {
    case interruptionBegan
    case interruptionEnded(shouldResume: Bool)
    case outputLost
    case engineFailed
}

/// The seam between the player and the hardware. The real one drives AVAudioEngine; the silent one
/// lets tests and the screenshot tooling run the whole app without a sound card.
@MainActor
protocol AudioHost: AnyObject {
    var onEvent: (@MainActor (AudioEvent) -> Void)? { get set }
    var mixWithOthers: Bool { get set }

    func start() throws
    func update(levels: [Float], master: Float, ramp: TimeInterval)
    func stop(fade: TimeInterval)
}

@MainActor
final class SilentHost: AudioHost {
    var onEvent: (@MainActor (AudioEvent) -> Void)?
    var mixWithOthers = false

    private(set) var isRunning = false
    private(set) var levels: [Float] = []
    private(set) var master: Float = 0
    private(set) var startCount = 0
    var failToStart = false

    func start() throws {
        if failToStart { throw CocoaError(.featureUnsupported) }
        isRunning = true
        startCount += 1
    }

    func update(levels: [Float], master: Float, ramp: TimeInterval) {
        self.levels = levels
        self.master = master
    }

    func stop(fade: TimeInterval) {
        master = 0
        isRunning = false
    }
}
