import XCTest
@testable import Umber

final class LoudnessTests: XCTestCase {
    private let sr: Float = 48_000

    /// Raw kernel level in dBFS, both ears, ten seconds.
    private func rawDecibels(_ sound: Sound) -> Float {
        let l = render(sound.makeKernel(channel: 0, sampleRate: sr, seed: 77), seconds: 10, sampleRate: sr)
        let r = render(sound.makeKernel(channel: 1, sampleRate: sr, seed: 77), seconds: 10, sampleRate: sr)
        return decibels(amplitude: sqrtf((rms(l) * rms(l) + rms(r) * rms(r)) / 2))
    }

    /// Prints the table to paste into LoudnessTrim.swift.
    func testPrintTrims() {
        var lines = [String]()
        for sound in Sound.all {
            let trim = powf(10, (sound.targetDecibels - rawDecibels(sound)) / 20)
            lines.append(".\(sound.rawValue): \(String(format: "%.4f", trim))")
        }
        print("TRIMS " + lines.joined(separator: ", "))
    }

    func testEverySoundLandsOnItsTarget() {
        for sound in Sound.all {
            let level = rawDecibels(sound) + 20 * log10f(LoudnessTrim.gain(for: sound))
            XCTAssertEqual(level, sound.targetDecibels, accuracy: 0.6, "\(sound) is off its loudness target")
        }
    }

    func testNoSoundIsLouderThanBrownNoise() {
        let brown = Sound.brown.targetDecibels
        XCTAssertTrue(Sound.all.allSatisfy { $0.targetDecibels <= brown })
    }
}
