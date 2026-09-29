import Foundation
import MediaPlayer
import Observation
import UIKit

@MainActor
@Observable
final class Player {
    static let shared = Player.makeShared()

    /// A session counts towards the review prompt once it has run this long.
    static let qualifyingSession: TimeInterval = 10 * 60
    static let sessionsBeforeReview = 3

    private(set) var mix: Mix
    private(set) var isPlaying = false
    private(set) var timer = SleepTimer()
    private(set) var mixWithOthers: Bool
    private(set) var reviewPending = false
    var startFailed = false

    @ObservationIgnored private let host: AudioHost
    @ObservationIgnored private let defaults: UserDefaults
    @ObservationIgnored private let publishesNowPlaying: Bool
    @ObservationIgnored private var master: Float = 0
    @ObservationIgnored private var timerTask: Task<Void, Never>?
    @ObservationIgnored private var playStartedAt: Date?
    @ObservationIgnored private var resumeAfterInterruption = false

    init(host: AudioHost, defaults: UserDefaults, publishesNowPlaying: Bool) {
        self.host = host
        self.defaults = defaults
        self.publishesNowPlaying = publishesNowPlaying
        if let data = defaults.data(forKey: Keys.mix), let stored = try? JSONDecoder().decode(Mix.self, from: data) {
            mix = stored
        } else {
            mix = Mix()
        }
        mixWithOthers = defaults.bool(forKey: Keys.mixWithOthers)
        host.mixWithOthers = mixWithOthers
        host.onEvent = { [weak self] event in self?.handle(event) }
        if publishesNowPlaying { configureRemoteCommands() }
    }

    private static func makeShared() -> Player {
        let options = LaunchOptions.current
        guard options.silent else {
            return Player(host: SystemAudioHost(), defaults: .standard, publishesNowPlaying: true)
        }
        let suite = "com.connexa.umber.silent"
        UserDefaults().removePersistentDomain(forName: suite)
        let player = Player(host: SilentHost(), defaults: UserDefaults(suiteName: suite) ?? .standard,
                            publishesNowPlaying: false)
        player.apply(scene: options.scene)
        return player
    }

    // MARK: Playback

    func play() {
        if mix.isEmpty { mix = Preset.focus.mix }
        do {
            host.mixWithOthers = mixWithOthers
            try host.start()
        } catch {
            startFailed = true
            return
        }
        isPlaying = true
        playStartedAt = .now
        master = 1
        host.update(levels: mix.levelArray, master: 1, ramp: 1.5)
        timer.resume()
        scheduleTimer()
        save()
        refreshNowPlaying()
    }

    func pause() {
        guard isPlaying else { return }
        isPlaying = false
        master = 0
        finishSession()
        timer.pause()
        timerTask?.cancel()
        host.stop(fade: 0.5)
        refreshNowPlaying()
    }

    func togglePlayback() {
        if isPlaying { pause() } else { play() }
    }

    // MARK: Mix

    /// Tapping a tile turns the sound on at a comfortable level, or off again.
    func toggle(_ sound: Sound) {
        if mix.level(sound) > 0 {
            setLevel(sound, 0)
        } else {
            mix.set(sound, Mix.defaultLevel)
            if isPlaying { publish() } else { play() }
            save()
            refreshNowPlaying()
        }
    }

    func setLevel(_ sound: Sound, _ level: Float) {
        mix.set(sound, level)
        if mix.isEmpty {
            pause()
        } else {
            publish()
        }
        save()
        refreshNowPlaying()
    }

    func apply(_ preset: Preset) {
        mix = preset.mix
        if isPlaying { publish() } else { play() }
        save()
        refreshNowPlaying()
    }

    /// For Shortcuts and Siri: exactly this one sound.
    func playOnly(_ sound: Sound, level: Float = 0.8) {
        mix = Mix([(sound, level)])
        if isPlaying { publish() } else { play() }
        save()
        refreshNowPlaying()
    }

    func setMixWithOthers(_ value: Bool) {
        mixWithOthers = value
        host.mixWithOthers = value
        defaults.set(value, forKey: Keys.mixWithOthers)
    }

    private func publish() {
        host.update(levels: mix.levelArray, master: master, ramp: 0)
    }

    // MARK: Sleep timer

    func startTimer(_ length: TimeInterval) {
        timer.start(length)
        if isPlaying {
            if master == 0 { master = 1; host.update(levels: mix.levelArray, master: 1, ramp: 1) }
            scheduleTimer()
        } else {
            play()
        }
    }

    func cancelTimer() {
        timerTask?.cancel()
        timer.cancel()
        if isPlaying, master == 0 {
            master = 1
            host.update(levels: mix.levelArray, master: 1, ramp: 1)
        }
    }

    private func scheduleTimer() {
        timerTask?.cancel()
        guard isPlaying, let end = timer.endsAt else { return }
        timerTask = Task { [weak self] in
            let untilFade = end.timeIntervalSinceNow - SleepTimer.fadeDuration
            if untilFade > 0 { try? await Task.sleep(for: .seconds(untilFade)) }
            guard !Task.isCancelled, let self else { return }
            let left = max(end.timeIntervalSinceNow, 0.5)
            self.master = 0
            self.host.update(levels: self.mix.levelArray, master: 0, ramp: left)
            try? await Task.sleep(for: .seconds(left))
            guard !Task.isCancelled else { return }
            self.timer.cancel()
            self.pause()
        }
    }

    // MARK: Interruptions

    private func handle(_ event: AudioEvent) {
        switch event {
        case .interruptionBegan:
            resumeAfterInterruption = isPlaying
            pause()
        case .interruptionEnded(let shouldResume):
            if resumeAfterInterruption && shouldResume { play() }
            resumeAfterInterruption = false
        case .outputLost:
            pause()
        case .engineFailed:
            pause()
            startFailed = true
        }
    }

    // MARK: Review prompt

    private func finishSession() {
        guard let started = playStartedAt else { return }
        playStartedAt = nil
        guard Date.now.timeIntervalSince(started) >= Player.qualifyingSession else { return }
        let sessions = defaults.integer(forKey: Keys.qualifiedSessions) + 1
        defaults.set(sessions, forKey: Keys.qualifiedSessions)
        if sessions >= Player.sessionsBeforeReview, defaults.string(forKey: Keys.reviewedVersion) != Player.appVersion {
            reviewPending = true
        }
    }

    func reviewWasRequested() {
        reviewPending = false
        defaults.set(Player.appVersion, forKey: Keys.reviewedVersion)
    }

    private static var appVersion: String {
        Bundle.main.object(forInfoDictionaryKey: "CFBundleShortVersionString") as? String ?? "1"
    }

    // MARK: Persistence

    private enum Keys {
        static let mix = "mix"
        static let mixWithOthers = "mixWithOthers"
        static let qualifiedSessions = "qualifiedSessions"
        static let reviewedVersion = "reviewedVersion"
    }

    private func save() {
        if let data = try? JSONEncoder().encode(mix) { defaults.set(data, forKey: Keys.mix) }
    }

    // MARK: Lock screen

    var summary: String {
        mix.active.map { String(localized: $0.title) }.formatted(.list(type: .and, width: .narrow))
    }

    private func refreshNowPlaying() {
        guard publishesNowPlaying else { return }
        let center = MPNowPlayingInfoCenter.default()
        guard !mix.isEmpty else {
            center.nowPlayingInfo = nil
            return
        }
        center.nowPlayingInfo = [
            MPMediaItemPropertyTitle: summary,
            MPMediaItemPropertyArtist: "Umber",
            MPMediaItemPropertyArtwork: Player.artwork,
            MPNowPlayingInfoPropertyIsLiveStream: true,
            MPNowPlayingInfoPropertyPlaybackRate: isPlaying ? 1.0 : 0.0,
        ]
        center.playbackState = isPlaying ? .playing : .paused
    }

    private func configureRemoteCommands() {
        let commands = MPRemoteCommandCenter.shared()
        for command in [commands.nextTrackCommand, commands.previousTrackCommand, commands.seekForwardCommand,
                        commands.seekBackwardCommand, commands.skipForwardCommand, commands.skipBackwardCommand,
                        commands.changePlaybackPositionCommand] {
            command.isEnabled = false
        }
        commands.playCommand.addTarget { [weak self] _ in
            Task { @MainActor in self?.play() }
            return .success
        }
        commands.pauseCommand.addTarget { [weak self] _ in
            Task { @MainActor in self?.pause() }
            return .success
        }
        commands.togglePlayPauseCommand.addTarget { [weak self] _ in
            Task { @MainActor in self?.togglePlayback() }
            return .success
        }
    }

    private static let artwork: MPMediaItemArtwork = {
        let size = CGSize(width: 600, height: 600)
        let image = UIGraphicsImageRenderer(size: size).image { context in
            UIColor(red: 0.043, green: 0.035, blue: 0.031, alpha: 1).setFill()
            context.fill(CGRect(origin: .zero, size: size))
            let colors = [UIColor(red: 0.95, green: 0.70, blue: 0.42, alpha: 1).cgColor,
                          UIColor(red: 0.62, green: 0.34, blue: 0.16, alpha: 1).cgColor]
            let gradient = CGGradient(colorsSpace: CGColorSpaceCreateDeviceRGB(), colors: colors as CFArray, locations: [0, 1])!
            context.cgContext.addEllipse(in: CGRect(x: 120, y: 120, width: 360, height: 360))
            context.cgContext.clip()
            context.cgContext.drawLinearGradient(gradient, start: CGPoint(x: 200, y: 120), end: CGPoint(x: 400, y: 480), options: [])
        }
        return MPMediaItemArtwork(boundsSize: size) { _ in image }
    }()

    // MARK: Scenes for screenshots

    func apply(scene: String?) {
        switch scene {
        case "focus":
            mix = Preset.focus.mix
            play()
            startTimer(45 * 60)
        case "mix":
            mix = Mix([(.rain, 0.7), (.wind, 0.38), (.brown, 0.45), (.ocean, 0.0)])
            play()
        case "timer":
            mix = Preset.sleep.mix
            play()
            startTimer(60 * 60)
        case "sleep":
            mix = Preset.sleep.mix
            play()
            startTimer(90 * 60)
        case "settings":
            mix = Preset.focus.mix
        default:
            break
        }
    }
}
