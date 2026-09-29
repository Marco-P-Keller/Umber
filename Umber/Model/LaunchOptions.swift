import Foundation

/// Launch arguments used by the screenshot and test tooling: `-UmberScene <name>` puts the app in a
/// composed state, `-UmberSilent` swaps the audio engine for one that makes no sound.
struct LaunchOptions {
    static let current = LaunchOptions(arguments: ProcessInfo.processInfo.arguments)

    let scene: String?
    let silent: Bool

    init(arguments: [String]) {
        silent = arguments.contains("-UmberSilent")
        if let i = arguments.firstIndex(of: "-UmberScene"), arguments.indices.contains(i + 1) {
            scene = arguments[i + 1]
        } else {
            scene = nil
        }
    }

    var opensTimer: Bool { scene == "timer" }
    var opensSettings: Bool { scene == "settings" }
}
