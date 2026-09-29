import Foundation

/// The gain that brings each generator's raw output to `Sound.targetDecibels` at full level.
/// Measured, not guessed: `LoudnessTests.testPrintTrims` prints these from ten seconds of each
/// kernel, and `LoudnessTests.testEverySoundLandsOnItsTarget` fails if one drifts.
enum LoudnessTrim {
    private static let table: [Sound: Float] = [
        .brown: 0.0168, .pink: 0.3616, .white: 0.0774, .green: 0.4296, .fan: 0.0968,
        .rain: 0.1953, .ocean: 0.2748, .wind: 0.3316, .womb: 0.1184,
    ]

    static func gain(for sound: Sound) -> Float {
        table[sound] ?? 1
    }
}
