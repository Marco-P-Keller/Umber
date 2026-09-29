import AppIntents

struct PlaySoundIntent: AudioPlaybackIntent {
    static let title: LocalizedStringResource = "intent.play.title"

    @Parameter(title: "intent.sound", default: .brown)
    var sound: Sound

    init() {}
    init(sound: Sound) { self.sound = sound }

    @MainActor
    func perform() async throws -> some IntentResult {
        Player.shared.playOnly(sound)
        return .result()
    }
}

struct StopSoundIntent: AudioPlaybackIntent {
    static let title: LocalizedStringResource = "intent.stop.title"

    init() {}

    @MainActor
    func perform() async throws -> some IntentResult {
        Player.shared.pause()
        return .result()
    }
}

struct UmberShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: PlaySoundIntent(),
            phrases: [
                "Play \(\.$sound) in \(.applicationName)",
                "Play brown noise in \(.applicationName)",
                "Start \(.applicationName)",
            ],
            shortTitle: "intent.play.title",
            systemImageName: "play.circle.fill"
        )
        AppShortcut(
            intent: StopSoundIntent(),
            phrases: [
                "Stop \(.applicationName)",
                "Stop the sound in \(.applicationName)",
            ],
            shortTitle: "intent.stop.title",
            systemImageName: "pause.circle.fill"
        )
    }
}
