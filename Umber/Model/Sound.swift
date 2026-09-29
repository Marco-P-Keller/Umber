import AppIntents
import SwiftUI

/// Everything Umber can play. Every one of these is computed sample by sample while you listen;
/// there are no recordings and therefore no loop point.
enum Sound: String, CaseIterable, Identifiable, Codable, Hashable {
    case brown, pink, white, green, fan, rain, ocean, wind, womb

    var id: String { rawValue }

    static let all = Sound.allCases

    var index: Int { Sound.all.firstIndex(of: self) ?? 0 }

    var title: LocalizedStringResource {
        switch self {
        case .brown: "sound.brown"
        case .pink: "sound.pink"
        case .white: "sound.white"
        case .green: "sound.green"
        case .fan: "sound.fan"
        case .rain: "sound.rain"
        case .ocean: "sound.ocean"
        case .wind: "sound.wind"
        case .womb: "sound.womb"
        }
    }

    /// The colour the sound wears in the interface.
    var tint: Color {
        switch self {
        case .brown: Color(red: 0.80, green: 0.55, blue: 0.35)
        case .pink: Color(red: 0.96, green: 0.55, blue: 0.70)
        case .white: Color(red: 0.90, green: 0.90, blue: 0.94)
        case .green: Color(red: 0.48, green: 0.83, blue: 0.53)
        case .fan: Color(red: 0.50, green: 0.72, blue: 0.92)
        case .rain: Color(red: 0.42, green: 0.61, blue: 0.95)
        case .ocean: Color(red: 0.24, green: 0.72, blue: 0.79)
        case .wind: Color(red: 0.72, green: 0.77, blue: 0.85)
        case .womb: Color(red: 0.94, green: 0.54, blue: 0.48)
        }
    }

    /// The three colours of noise and their sibling are drawn as spectrum bars; the rest use a symbol.
    var symbol: String? {
        switch self {
        case .brown, .pink, .white, .green: nil
        case .fan: "fan"
        case .rain: "cloud.rain"
        case .ocean: "water.waves"
        case .wind: "wind"
        case .womb: "heart.fill"
        }
    }

    /// Relative bar heights of the little spectrum drawn for the coloured noises: how much energy
    /// there is at each of seven frequencies, low to high.
    var spectrum: [Double] {
        switch self {
        case .white: [0.62, 0.50, 0.66, 0.54, 0.64, 0.48, 0.60]
        case .pink: [1.0, 0.84, 0.70, 0.57, 0.45, 0.34, 0.24]
        case .brown: [1.0, 0.70, 0.46, 0.28, 0.17, 0.10, 0.06]
        case .green: [0.14, 0.36, 0.72, 1.0, 0.72, 0.36, 0.14]
        default: []
        }
    }

    /// Target loudness at full level, in dBFS RMS. White noise is the quietest number because it is
    /// the harshest to the ear at any given energy; brown is the loudest because the ear barely hears
    /// the bottom octaves.
    var targetDecibels: Float {
        switch self {
        case .white: -27
        case .pink: -23
        case .brown: -19
        case .green: -25
        case .fan: -24
        case .rain: -24
        case .ocean: -23
        case .wind: -25
        case .womb: -24
        }
    }

    func makeKernel(channel: Int, sampleRate: Float, seed: UInt64) -> NoiseKernel {
        let s = seed &+ UInt64(index) &* 7919 &+ UInt64(channel) &* 104_729
        switch self {
        case .brown: return BrownKernel(sampleRate: sampleRate, seed: s)
        case .pink: return PinkKernel(sampleRate: sampleRate, seed: s)
        case .white: return WhiteKernel(sampleRate: sampleRate, seed: s)
        case .green: return GreenKernel(sampleRate: sampleRate, seed: s)
        case .fan: return FanKernel(sampleRate: sampleRate, seed: s)
        case .rain: return RainKernel(sampleRate: sampleRate, seed: s)
        case .ocean: return OceanKernel(sampleRate: sampleRate, seed: s)
        case .wind: return WindKernel(sampleRate: sampleRate, seed: s)
        case .womb: return WombKernel(sampleRate: sampleRate, seed: s, beatSeed: seed &+ 31_337)
        }
    }
}

extension Sound: AppEnum {
    static let typeDisplayRepresentation = TypeDisplayRepresentation(name: "intent.sound")

    static let caseDisplayRepresentations: [Sound: DisplayRepresentation] = [
        .brown: DisplayRepresentation(title: "sound.brown"),
        .pink: DisplayRepresentation(title: "sound.pink"),
        .white: DisplayRepresentation(title: "sound.white"),
        .green: DisplayRepresentation(title: "sound.green"),
        .fan: DisplayRepresentation(title: "sound.fan"),
        .rain: DisplayRepresentation(title: "sound.rain"),
        .ocean: DisplayRepresentation(title: "sound.ocean"),
        .wind: DisplayRepresentation(title: "sound.wind"),
        .womb: DisplayRepresentation(title: "sound.womb"),
    ]
}
