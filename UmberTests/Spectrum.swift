import Accelerate
import Foundation
@testable import Umber

/// Measurement helpers for the tests: what a generator actually puts out, not what it is called.
enum Spectrum {
    /// Welch power spectral density: Hann-windowed segments, 50% overlap, averaged. One value per FFT bin
    /// from 0 to Nyquist (exclusive).
    static func psd(_ x: [Float], segment n: Int = 4096) -> [Float] {
        let log2n = vDSP_Length(log2(Double(n)))
        guard let setup = vDSP_create_fftsetup(log2n, FFTRadix(kFFTRadix2)) else { return [] }
        defer { vDSP_destroy_fftsetup(setup) }

        var window = [Float](repeating: 0, count: n)
        vDSP_hann_window(&window, vDSP_Length(n), Int32(vDSP_HANN_NORM))

        let half = n / 2
        var power = [Float](repeating: 0, count: half)
        var segments = 0
        var start = 0
        var real = [Float](repeating: 0, count: half)
        var imag = [Float](repeating: 0, count: half)

        while start + n <= x.count {
            var windowed = [Float](repeating: 0, count: n)
            vDSP_vmul(Array(x[start..<start + n]), 1, window, 1, &windowed, 1, vDSP_Length(n))
            real.withUnsafeMutableBufferPointer { rp in
                imag.withUnsafeMutableBufferPointer { ip in
                    var split = DSPSplitComplex(realp: rp.baseAddress!, imagp: ip.baseAddress!)
                    windowed.withUnsafeBufferPointer { wp in
                        wp.baseAddress!.withMemoryRebound(to: DSPComplex.self, capacity: half) {
                            vDSP_ctoz($0, 2, &split, 1, vDSP_Length(half))
                        }
                    }
                    vDSP_fft_zrip(setup, &split, 1, log2n, FFTDirection(FFT_FORWARD))
                    for k in 1..<half {
                        power[k] += rp[k] * rp[k] + ip[k] * ip[k]
                    }
                }
            }
            segments += 1
            start += n / 2
        }
        guard segments > 0 else { return power }
        return power.map { $0 / Float(segments) }
    }

    /// Mean power per bin between two frequencies.
    static func meanPower(_ psd: [Float], sampleRate: Float, from low: Float, to high: Float) -> Float {
        let binWidth = sampleRate / Float(psd.count * 2)
        let lo = max(1, Int(low / binWidth))
        let hi = min(psd.count - 1, Int(high / binWidth))
        guard hi > lo else { return 0 }
        return psd[lo...hi].reduce(0, +) / Float(hi - lo + 1)
    }

    static func decibels(_ power: Float) -> Float {
        10 * log10f(max(power, 1e-30))
    }

    /// Least-squares slope of the spectral density, in dB per octave, over octave bands centred on the
    /// given frequencies.
    static func slope(_ psd: [Float], sampleRate: Float, centres: [Float]) -> Float {
        let ys = centres.map { c in decibels(meanPower(psd, sampleRate: sampleRate, from: c / 1.4142, to: c * 1.4142)) }
        let xs = centres.map { log2f($0) }
        let mx = xs.reduce(0, +) / Float(xs.count)
        let my = ys.reduce(0, +) / Float(ys.count)
        var num: Float = 0, den: Float = 0
        for i in 0..<xs.count {
            num += (xs[i] - mx) * (ys[i] - my)
            den += (xs[i] - mx) * (xs[i] - mx)
        }
        return num / den
    }
}

func rms(_ x: [Float]) -> Float {
    var r: Float = 0
    vDSP_rmsqv(x, 1, &r, vDSP_Length(x.count))
    return r
}

func decibels(amplitude: Float) -> Float {
    20 * log10f(max(amplitude, 1e-12))
}

func correlation(_ a: [Float], _ b: [Float]) -> Float {
    let n = vDSP_Length(min(a.count, b.count))
    var dot: Float = 0
    vDSP_dotpr(a, 1, b, 1, &dot, n)
    var ea: Float = 0, eb: Float = 0
    vDSP_dotpr(a, 1, a, 1, &ea, n)
    vDSP_dotpr(b, 1, b, 1, &eb, n)
    return dot / max(sqrtf(ea * eb), 1e-12)
}

/// Runs a kernel for `seconds` and returns what it produced.
func render(_ kernel: NoiseKernel, seconds: Float, sampleRate: Float = 48_000, block: Int = 480) -> [Float] {
    let total = Int(seconds * sampleRate)
    var out = [Float](repeating: 0, count: total)
    out.withUnsafeMutableBufferPointer { buffer in
        var done = 0
        while done < total {
            let n = min(block, total - done)
            kernel.render(buffer.baseAddress! + done, frames: n)
            done += n
        }
    }
    return out
}
