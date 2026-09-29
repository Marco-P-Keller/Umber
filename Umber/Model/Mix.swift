import SwiftUI

/// Which sounds are on, and how loud each one is (0...1).
struct Mix: Equatable, Codable {
    static let defaultLevel: Float = 0.7

    private(set) var levels: [String: Float] = [:]

    init(_ pairs: [(Sound, Float)] = []) {
        for (sound, level) in pairs { set(sound, level) }
    }

    func level(_ sound: Sound) -> Float { levels[sound.rawValue] ?? 0 }

    mutating func set(_ sound: Sound, _ level: Float) {
        let clamped = min(max(level, 0), 1)
        if clamped <= 0 { levels[sound.rawValue] = nil } else { levels[sound.rawValue] = clamped }
    }

    var isEmpty: Bool { levels.isEmpty }
    var active: [Sound] { Sound.all.filter { level($0) > 0 } }
    var levelArray: [Float] { Sound.all.map { level($0) } }
    var dominant: Sound? { active.max { level($0) < level($1) } }
}

struct Preset: Identifiable {
    let id: String
    let title: LocalizedStringResource
    let symbol: String
    let mix: Mix

    static let focus = Preset(id: "focus", title: "preset.focus", symbol: "brain.head.profile",
                              mix: Mix([(.brown, 0.8)]))
    static let sleep = Preset(id: "sleep", title: "preset.sleep", symbol: "moon.stars.fill",
                              mix: Mix([(.brown, 0.55), (.pink, 0.22), (.wind, 0.15)]))
    static let storm = Preset(id: "storm", title: "preset.storm", symbol: "cloud.bolt.rain.fill",
                              mix: Mix([(.rain, 0.75), (.wind, 0.4), (.brown, 0.35)]))
    static let shore = Preset(id: "shore", title: "preset.shore", symbol: "water.waves",
                              mix: Mix([(.ocean, 0.8), (.wind, 0.2)]))
    static let baby = Preset(id: "baby", title: "preset.baby", symbol: "teddybear.fill",
                             mix: Mix([(.womb, 0.8), (.pink, 0.2)]))

    static let all = [focus, sleep, storm, shore, baby]
}
