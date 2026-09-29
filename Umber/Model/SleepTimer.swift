import Foundation

/// A countdown that can be paused. Pure value type: the player decides when "now" is.
struct SleepTimer: Equatable {
    /// The last stretch of the timer is spent fading out, so the sound leaves the way a lullaby does.
    static let fadeDuration: TimeInterval = 20
    static let options: [TimeInterval] = [15, 30, 45, 60, 90, 120, 180, 480].map { $0 * 60 }

    private(set) var duration: TimeInterval?
    private(set) var endsAt: Date?
    private(set) var pausedRemaining: TimeInterval?

    var isActive: Bool { endsAt != nil || pausedRemaining != nil }
    var isRunning: Bool { endsAt != nil }

    mutating func start(_ length: TimeInterval, now: Date = .now) {
        duration = length
        endsAt = now.addingTimeInterval(length)
        pausedRemaining = nil
    }

    mutating func pause(now: Date = .now) {
        guard let endsAt else { return }
        pausedRemaining = max(0, endsAt.timeIntervalSince(now))
        self.endsAt = nil
    }

    mutating func resume(now: Date = .now) {
        guard let pausedRemaining else { return }
        endsAt = now.addingTimeInterval(pausedRemaining)
        self.pausedRemaining = nil
    }

    mutating func cancel() {
        duration = nil
        endsAt = nil
        pausedRemaining = nil
    }

    func remaining(now: Date = .now) -> TimeInterval? {
        if let endsAt { return max(0, endsAt.timeIntervalSince(now)) }
        return pausedRemaining
    }
}
