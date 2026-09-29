import Foundation

/// One channel of one sound. `render` runs on the audio thread: no allocation, no locks, no I/O.
protocol NoiseKernel: AnyObject {
    func render(_ out: UnsafeMutablePointer<Float>, frames: Int)
}

/// Paul Kellet's refined pink-noise filter: within about 0.05 dB of -3 dB/octave from 10 Hz to Nyquist.
struct PinkFilter {
    private var b0: Float = 0, b1: Float = 0, b2: Float = 0, b3: Float = 0, b4: Float = 0, b5: Float = 0, b6: Float = 0

    @inline(__always)
    mutating func process(_ w: Float) -> Float {
        b0 = 0.99886 * b0 + w * 0.0555179
        b1 = 0.99332 * b1 + w * 0.0750759
        b2 = 0.96900 * b2 + w * 0.1538520
        b3 = 0.86650 * b3 + w * 0.3104856
        b4 = 0.55000 * b4 + w * 0.5329522
        b5 = -0.7616 * b5 - w * 0.0168980
        let out = b0 + b1 + b2 + b3 + b4 + b5 + b6 + w * 0.5362
        b6 = w * 0.115926
        return out * 0.11
    }
}

// MARK: - The coloured noises

final class WhiteKernel: NoiseKernel {
    private var rng: FastRandom

    init(sampleRate: Float, seed: UInt64) {
        rng = FastRandom(seed: seed)
    }

    func render(_ out: UnsafeMutablePointer<Float>, frames: Int) {
        for i in 0..<frames { out[i] = rng.bipolar() }
    }
}

final class PinkKernel: NoiseKernel {
    private var rng: FastRandom
    private var filter = PinkFilter()

    init(sampleRate: Float, seed: UInt64) {
        rng = FastRandom(seed: seed)
    }

    func render(_ out: UnsafeMutablePointer<Float>, frames: Int) {
        for i in 0..<frames { out[i] = filter.process(rng.bipolar()) }
    }
}

/// A leaky integrator: -6 dB/octave above its corner, flat below it, so the rumble stops short of DC.
final class BrownKernel: NoiseKernel {
    private var rng: FastRandom
    private var y: Float = 0
    private let leak: Float

    init(sampleRate: Float, seed: UInt64) {
        rng = FastRandom(seed: seed)
        leak = 1 - 2 * Float.pi * 28 / sampleRate
    }

    func render(_ out: UnsafeMutablePointer<Float>, frames: Int) {
        for i in 0..<frames {
            y = leak * y + rng.bipolar()
            out[i] = y
        }
    }
}

/// Noise limited to the middle of the spectrum, about two octaves around 500 Hz.
final class GreenKernel: NoiseKernel {
    private var rng: FastRandom
    private var band: Biquad

    init(sampleRate: Float, seed: UInt64) {
        rng = FastRandom(seed: seed)
        band = Biquad(bandpass: 500, q: 0.6, sampleRate: sampleRate)
    }

    func render(_ out: UnsafeMutablePointer<Float>, frames: Int) {
        for i in 0..<frames { out[i] = band.process(rng.bipolar()) }
    }
}

// MARK: - The places

/// A room fan: soft broadband air plus the low motor hum and its first harmonics, drifting a little.
final class FanKernel: NoiseKernel {
    private var rng: FastRandom
    private var pink = PinkFilter()
    private var air: OnePole
    private var drift: SlowDrift
    private var wobble: Float = 0.5
    private var phase1: Float
    private var phase2: Float
    private var phase3: Float
    private let step1: Float

    init(sampleRate: Float, seed: UInt64) {
        var r = FastRandom(seed: seed)
        air = OnePole(cutoff: 2100, sampleRate: sampleRate)
        drift = SlowDrift(periodA: 7, periodB: 3.1, sampleRate: sampleRate, rng: &r)
        phase1 = r.unit() * 2 * Float.pi
        phase2 = r.unit() * 2 * Float.pi
        phase3 = r.unit() * 2 * Float.pi
        step1 = 2 * Float.pi * (104 + 12 * r.unit()) / sampleRate
        rng = r
    }

    func render(_ out: UnsafeMutablePointer<Float>, frames: Int) {
        let target = drift.advance(frames)
        let step = (target - wobble) / Float(frames)
        for i in 0..<frames {
            wobble += step
            phase1 += step1
            phase2 += step1 * 2
            phase3 += step1 * 3
            if phase1 > 2 * Float.pi { phase1 -= 2 * Float.pi }
            if phase2 > 2 * Float.pi { phase2 -= 2 * Float.pi }
            if phase3 > 2 * Float.pi { phase3 -= 2 * Float.pi }
            let hum = 0.5 * sinf(phase1) + 0.2 * sinf(phase2) + 0.07 * sinf(phase3)
            let breath = air.lowpass(pink.process(rng.bipolar()))
            out[i] = breath * 3.2 + hum * (0.8 + 0.4 * wobble)
        }
    }
}

/// Steady rain: a bed of hiss, with individual drops on top. Each drop is a short damped ringing at a
/// random pitch, so the pattern never settles into a repeat.
final class RainKernel: NoiseKernel {
    private static let dropSlots = 28

    private var rng: FastRandom
    private var pink = PinkFilter()
    private var low: OnePole
    private var high: OnePole
    private var drift: SlowDrift
    private var intensity: Float = 0.5
    private let sampleRate: Float
    private let dropChance: Float

    private let x: UnsafeMutablePointer<Float>
    private let y: UnsafeMutablePointer<Float>
    private let cosine: UnsafeMutablePointer<Float>
    private let sine: UnsafeMutablePointer<Float>
    private let decay: UnsafeMutablePointer<Float>
    private var nextSlot = 0

    init(sampleRate: Float, seed: UInt64) {
        var r = FastRandom(seed: seed)
        self.sampleRate = sampleRate
        low = OnePole(cutoff: 9000, sampleRate: sampleRate)
        high = OnePole(cutoff: 700, sampleRate: sampleRate)
        drift = SlowDrift(periodA: 23, periodB: 9, sampleRate: sampleRate, rng: &r)
        dropChance = 95 / sampleRate
        let n = RainKernel.dropSlots
        x = .allocate(capacity: n)
        y = .allocate(capacity: n)
        cosine = .allocate(capacity: n)
        sine = .allocate(capacity: n)
        decay = .allocate(capacity: n)
        x.initialize(repeating: 0, count: n)
        y.initialize(repeating: 0, count: n)
        cosine.initialize(repeating: 1, count: n)
        sine.initialize(repeating: 0, count: n)
        decay.initialize(repeating: 0, count: n)
        rng = r
    }

    deinit {
        x.deallocate(); y.deallocate(); cosine.deallocate(); sine.deallocate(); decay.deallocate()
    }

    func render(_ out: UnsafeMutablePointer<Float>, frames: Int) {
        let target = drift.advance(frames)
        let step = (target - intensity) / Float(frames)
        let n = RainKernel.dropSlots
        for i in 0..<frames {
            intensity += step
            let bed = high.highpass(low.lowpass(pink.process(rng.bipolar()))) * (0.9 + 0.5 * intensity)

            if rng.unit() < dropChance * (0.6 + 0.8 * intensity) {
                let s = nextSlot
                nextSlot = (nextSlot + 1) % n
                let pitch = 1700 * powf(4.0, rng.unit())
                let w = 2 * Float.pi * pitch / sampleRate
                cosine[s] = cosf(w)
                sine[s] = sinf(w)
                decay[s] = expf(-1 / (sampleRate * (0.0025 + 0.010 * rng.unit())))
                x[s] = 0.35 + 0.65 * rng.unit()
                y[s] = 0
            }

            var drops: Float = 0
            for s in 0..<n {
                let px = x[s], py = y[s]
                if px == 0 && py == 0 { continue }
                let r = decay[s]
                let nx = r * (cosine[s] * px - sine[s] * py)
                let ny = r * (sine[s] * px + cosine[s] * py)
                if abs(nx) + abs(ny) < 0.0003 { x[s] = 0; y[s] = 0 } else { x[s] = nx; y[s] = ny }
                drops += nx
            }
            out[i] = bed * 2.6 + drops * 0.32
        }
    }
}

/// Slow surf: filtered noise whose loudness and brightness rise and fall together, like a wave arriving.
final class OceanKernel: NoiseKernel {
    private var rng: FastRandom
    private var pink = PinkFilter()
    private var low: OnePole
    private var drift: SlowDrift
    private var swell: Float = 0.4
    private let sampleRate: Float

    init(sampleRate: Float, seed: UInt64) {
        var r = FastRandom(seed: seed)
        self.sampleRate = sampleRate
        low = OnePole(cutoff: 400, sampleRate: sampleRate)
        drift = SlowDrift(periodA: 10.5, periodB: 6.2, sampleRate: sampleRate, rng: &r)
        rng = r
    }

    func render(_ out: UnsafeMutablePointer<Float>, frames: Int) {
        let target = drift.advance(frames)
        let step = (target - swell) / Float(frames)
        for i in 0..<frames {
            swell += step
            let crest = max(swell, 0) * max(swell, 0)
            if i & 31 == 0 { low.setCutoff(180 + 2900 * crest, sampleRate: sampleRate) }
            out[i] = low.lowpass(pink.process(rng.bipolar())) * (0.16 + 0.84 * crest) * 3.4
        }
    }
}

/// Wind: a resonant band of noise whose centre wanders and whose gusts come and go.
final class WindKernel: NoiseKernel {
    private var rng: FastRandom
    private var pink = PinkFilter()
    private var band: StateVariableBandpass
    private var floor: OnePole
    private var pitchDrift: SlowDrift
    private var gustDrift: SlowDrift
    private var pitch: Float = 0.5
    private var gust: Float = 0.5
    private let sampleRate: Float

    init(sampleRate: Float, seed: UInt64) {
        var r = FastRandom(seed: seed)
        self.sampleRate = sampleRate
        band = StateVariableBandpass(q: 2.4)
        floor = OnePole(cutoff: 220, sampleRate: sampleRate)
        pitchDrift = SlowDrift(periodA: 6, periodB: 13.7, sampleRate: sampleRate, rng: &r)
        gustDrift = SlowDrift(periodA: 8.5, periodB: 4.3, sampleRate: sampleRate, rng: &r)
        rng = r
    }

    func render(_ out: UnsafeMutablePointer<Float>, frames: Int) {
        let pitchTarget = pitchDrift.advance(frames)
        let gustTarget = gustDrift.advance(frames)
        let pitchStep = (pitchTarget - pitch) / Float(frames)
        let gustStep = (gustTarget - gust) / Float(frames)
        for i in 0..<frames {
            pitch += pitchStep
            gust += gustStep
            let strength = max(gust, 0) * max(gust, 0)
            if i & 15 == 0 { band.setCutoff(260 + 750 * pitch + 350 * strength, sampleRate: sampleRate) }
            let w = rng.bipolar()
            let whistle = band.process(w) * (0.18 + 0.82 * strength)
            let body = floor.lowpass(pink.process(w)) * (0.5 + 0.9 * strength)
            out[i] = whistle * 0.55 + body * 1.5
        }
    }
}

/// The sound of a womb: low rumble, a soft swish, and a heartbeat at about 130 beats a minute.
/// Both channels are seeded with the same `beatSeed`, so the heart is in the middle and the rumble is wide.
final class WombKernel: NoiseKernel {
    private var noise: FastRandom
    private var beats: FastRandom
    private var pink = PinkFilter()
    private var rumble: OnePole
    private var rumbleFloor: OnePole
    private var brown: Float = 0
    private let brownLeak: Float
    private var swish: Biquad
    private var swishFollow: Float = 0
    private let sampleRate: Float
    private var t: Float = 0
    private var period: Float
    private var phaseLub: Float = 0
    private var phaseDub: Float = 0

    init(sampleRate: Float, seed: UInt64, beatSeed: UInt64) {
        self.sampleRate = sampleRate
        noise = FastRandom(seed: seed)
        beats = FastRandom(seed: beatSeed)
        rumble = OnePole(cutoff: 340, sampleRate: sampleRate)
        rumbleFloor = OnePole(cutoff: 32, sampleRate: sampleRate)
        brownLeak = 1 - 2 * Float.pi * 20 / sampleRate
        swish = Biquad(bandpass: 620, q: 0.7, sampleRate: sampleRate)
        period = 0.44 + 0.04 * beats.unit()
    }

    @inline(__always)
    private func thump(_ u: Float) -> Float {
        u < 0 ? 0 : (1 - expf(-u / 0.005)) * expf(-u / 0.05)
    }

    func render(_ out: UnsafeMutablePointer<Float>, frames: Int) {
        let dt = 1 / sampleRate
        let lubStep = 2 * Float.pi * 52 * dt
        let dubStep = 2 * Float.pi * 43 * dt
        for i in 0..<frames {
            t += dt
            if t >= period {
                t -= period
                period = 0.43 + 0.05 * beats.unit()
            }
            phaseLub += lubStep
            phaseDub += dubStep
            if phaseLub > 2 * Float.pi { phaseLub -= 2 * Float.pi }
            if phaseDub > 2 * Float.pi { phaseDub -= 2 * Float.pi }

            let lub = thump(t)
            let dub = thump(t - 0.17)
            let heart = sinf(phaseLub) * lub + 0.65 * sinf(phaseDub) * dub

            let w = noise.bipolar()
            brown = brownLeak * brown + w
            let body = rumbleFloor.highpass(rumble.lowpass(brown)) * 0.06
            swishFollow += 0.0008 * ((lub + dub) - swishFollow)
            let air = swish.process(pink.process(w)) * (0.25 + 1.4 * swishFollow)
            out[i] = body + air * 1.5 + heart * 2.6
        }
    }
}
