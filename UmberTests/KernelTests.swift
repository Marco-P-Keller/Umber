import XCTest
@testable import Umber

/// The generators, measured. A pink noise that is not -3 dB/octave is not pink noise, whatever the
/// button says.
final class KernelTests: XCTestCase {
    private let sr: Float = 48_000
    private let seed: UInt64 = 20_260_929
    private let octaves: [Float] = [250, 500, 1000, 2000, 4000]

    private func spectrum(of sound: Sound, seconds: Float = 12) -> [Float] {
        Spectrum.psd(render(sound.makeKernel(channel: 0, sampleRate: sr, seed: seed), seconds: seconds, sampleRate: sr))
    }

    func testWhiteNoiseIsFlat() {
        let slope = Spectrum.slope(spectrum(of: .white), sampleRate: sr, centres: octaves)
        XCTAssertEqual(slope, 0, accuracy: 0.5)
    }

    func testPinkNoiseFallsThreeDecibelsPerOctave() {
        let slope = Spectrum.slope(spectrum(of: .pink), sampleRate: sr, centres: octaves)
        XCTAssertEqual(slope, -3, accuracy: 0.6)
    }

    func testBrownNoiseFallsSixDecibelsPerOctave() {
        let slope = Spectrum.slope(spectrum(of: .brown), sampleRate: sr, centres: octaves)
        XCTAssertEqual(slope, -6, accuracy: 0.7)
    }

    func testBrownNoiseKeepsItsRumbleBelowTheCorner() {
        let psd = spectrum(of: .brown)
        let rumble = Spectrum.decibels(Spectrum.meanPower(psd, sampleRate: sr, from: 40, to: 80))
        let hiss = Spectrum.decibels(Spectrum.meanPower(psd, sampleRate: sr, from: 4000, to: 8000))
        XCTAssertGreaterThan(rumble - hiss, 30)
    }

    func testGreenNoiseLivesInTheMiddle() {
        let psd = spectrum(of: .green)
        let middle = Spectrum.decibels(Spectrum.meanPower(psd, sampleRate: sr, from: 350, to: 700))
        let low = Spectrum.decibels(Spectrum.meanPower(psd, sampleRate: sr, from: 30, to: 60))
        let high = Spectrum.decibels(Spectrum.meanPower(psd, sampleRate: sr, from: 6000, to: 10000))
        XCTAssertGreaterThan(middle - low, 15)
        XCTAssertGreaterThan(middle - high, 17)
    }

    func testFanHasAHumUnderItsBreath() {
        let psd = spectrum(of: .fan)
        let hum = Spectrum.decibels(Spectrum.meanPower(psd, sampleRate: sr, from: 95, to: 125))
        let breath = Spectrum.decibels(Spectrum.meanPower(psd, sampleRate: sr, from: 400, to: 600))
        XCTAssertGreaterThan(hum, breath, "the motor should be audible under the air")
    }

    func testEverySoundIsFiniteBoundedAndCentred() {
        for sound in Sound.all {
            let x = render(sound.makeKernel(channel: 0, sampleRate: sr, seed: seed), seconds: 8, sampleRate: sr)
            XCTAssertFalse(x.contains { !$0.isFinite }, "\(sound) produced a NaN or infinity")
            let level = rms(x)
            XCTAssertGreaterThan(level, 0.001, "\(sound) is silent")
            XCTAssertLessThan((x.map(abs).max() ?? 0) / level, 14, "\(sound) has runaway peaks")
            let mean = x.reduce(0, +) / Float(x.count)
            XCTAssertLessThan(abs(mean) / level, 0.25, "\(sound) has a DC offset")
        }
    }

    func testTheTwoEarsHearDifferentNoise() {
        for sound in Sound.all where sound != .womb {
            let l = render(sound.makeKernel(channel: 0, sampleRate: sr, seed: seed), seconds: 6, sampleRate: sr)
            let r = render(sound.makeKernel(channel: 1, sampleRate: sr, seed: seed), seconds: 6, sampleRate: sr)
            XCTAssertLessThan(abs(correlation(l, r)), 0.2, "\(sound) is close to mono")
        }
    }

    func testSameSeedSameSoundDifferentSeedDifferentSound() {
        for sound in Sound.all {
            let a = render(sound.makeKernel(channel: 0, sampleRate: sr, seed: 5), seconds: 1, sampleRate: sr)
            let b = render(sound.makeKernel(channel: 0, sampleRate: sr, seed: 5), seconds: 1, sampleRate: sr)
            let c = render(sound.makeKernel(channel: 0, sampleRate: sr, seed: 6), seconds: 1, sampleRate: sr)
            XCTAssertEqual(a, b, "\(sound) is not deterministic")
            XCTAssertNotEqual(a, c, "\(sound) ignores its seed")
        }
    }

    func testTheOceanBreathes() {
        let x = render(Sound.ocean.makeKernel(channel: 0, sampleRate: sr, seed: seed), seconds: 40, sampleRate: sr)
        let window = Int(sr)  // one second
        let levels = stride(from: 0, to: x.count - window, by: window).map { rms(Array(x[$0..<$0 + window])) }
        XCTAssertGreaterThan((levels.max() ?? 0) / max(levels.min() ?? 1, 1e-6), 1.8, "the surf never rises and falls")
    }

    func testTheWindGusts() {
        let x = render(Sound.wind.makeKernel(channel: 0, sampleRate: sr, seed: seed), seconds: 40, sampleRate: sr)
        let window = Int(sr)
        let levels = stride(from: 0, to: x.count - window, by: window).map { rms(Array(x[$0..<$0 + window])) }
        XCTAssertGreaterThan((levels.max() ?? 0) / max(levels.min() ?? 1, 1e-6), 1.5, "the wind never changes")
    }

    func testTheHeartBeatsAtAboutOneThirtyAMinute() {
        let x = render(Sound.womb.makeKernel(channel: 0, sampleRate: sr, seed: seed), seconds: 30, sampleRate: sr)
        // The heart lives below 90 Hz. Take the envelope of that band at 200 Hz and find the lag at
        // which it best repeats.
        var low = OnePole(cutoff: 90, sampleRate: sr)
        var smooth: Float = 0
        var envelope = [Float]()
        for (i, v) in x.enumerated() {
            smooth += 0.004 * (abs(low.lowpass(v)) - smooth)
            if i % 240 == 0 { envelope.append(smooth) }
        }
        let mean = envelope.reduce(0, +) / Float(envelope.count)
        let e = envelope.map { $0 - mean }
        func autocorrelation(_ lag: Int) -> Float {
            var sum: Float = 0
            for i in 0..<(e.count - lag) { sum += e[i] * e[i + lag] }
            return sum
        }
        let lags = Array(60...140)  // 0.3 s ... 0.7 s at 200 Hz
        let best = lags.max { autocorrelation($0) < autocorrelation($1) }!
        let perMinute = 60 / (Float(best) / 200)
        XCTAssertEqual(perMinute, 130, accuracy: 12, "the heart repeats every \(Float(best) / 200) s")
    }

    func testRainHasDropsOnTopOfItsHiss() {
        let x = render(Sound.rain.makeKernel(channel: 0, sampleRate: sr, seed: seed), seconds: 10, sampleRate: sr)
        let white = render(Sound.white.makeKernel(channel: 0, sampleRate: sr, seed: seed), seconds: 10, sampleRate: sr)
        func kurtosis(_ v: [Float]) -> Float {
            let m = v.reduce(0, +) / Float(v.count)
            let d = v.map { $0 - m }
            let s2 = d.map { $0 * $0 }.reduce(0, +) / Float(d.count)
            let s4 = d.map { $0 * $0 * $0 * $0 }.reduce(0, +) / Float(d.count)
            return s4 / (s2 * s2)
        }
        XCTAssertGreaterThan(kurtosis(x), kurtosis(white) + 0.3, "rain should be more impulsive than plain noise")
    }
}
