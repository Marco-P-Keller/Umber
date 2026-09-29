import XCTest
@testable import Umber

final class MixRendererTests: XCTestCase {
    private let sr: Float = 48_000

    private func make(levels: [Sound: Float], master: Float = 1, seed: UInt64 = 3) -> (MixRenderer, ParameterMailbox) {
        let mailbox = ParameterMailbox()
        let renderer = MixRenderer(sampleRate: sr, mailbox: mailbox, seed: seed)
        mailbox.publish(levels: Sound.all.map { levels[$0] ?? 0 }, master: master, rampSeconds: 0)
        return (renderer, mailbox)
    }

    private func pull(_ renderer: MixRenderer, seconds: Float, block: Int = 512) -> (left: [Float], right: [Float]) {
        let total = Int(seconds * sr)
        var left = [Float](repeating: 0, count: total)
        var right = [Float](repeating: 0, count: total)
        var done = 0
        while done < total {
            let n = min(block, total - done)
            left.withUnsafeMutableBufferPointer { l in
                right.withUnsafeMutableBufferPointer { r in
                    renderer.render(frames: n, left: l.baseAddress! + done, right: r.baseAddress! + done)
                }
            }
            done += n
        }
        return (left, right)
    }

    func testNothingOnIsSilence() {
        let (renderer, _) = make(levels: [:])
        let out = pull(renderer, seconds: 1)
        XCTAssertEqual(out.left.max(), 0)
        XCTAssertEqual(out.right.min(), 0)
    }

    func testEverythingAtFullNeverClipsAndNeverBreaks() {
        let (renderer, _) = make(levels: Dictionary(uniqueKeysWithValues: Sound.all.map { ($0, Float(1)) }))
        let out = pull(renderer, seconds: 6)
        for channel in [out.left, out.right] {
            XCTAssertFalse(channel.contains { !$0.isFinite })
            XCTAssertLessThanOrEqual(channel.map(abs).max() ?? 0, 1.0, "the soft clip must never exceed full scale")
        }
    }

    func testTheMixIsStereo() {
        let (renderer, _) = make(levels: [.rain: 0.8, .brown: 0.5])
        let out = pull(renderer, seconds: 4)
        XCTAssertLessThan(abs(correlation(out.left, out.right)), 0.25)
    }

    func testTheSoftClipIsTransparentBelowItsKnee() {
        for x in stride(from: Float(-0.72), through: 0.72, by: 0.06) {
            XCTAssertEqual(MixRenderer.softClip(x), x, accuracy: 1e-6)
        }
        XCTAssertLessThanOrEqual(MixRenderer.softClip(50), 1)
        XCTAssertGreaterThan(MixRenderer.softClip(0.9), MixRenderer.softClip(0.8))
    }

    func testFadingOutIsSmoothAndEndsInSilence() {
        let (renderer, mailbox) = make(levels: [.brown: 1])
        let before = pull(renderer, seconds: 1).left
        mailbox.publish(levels: Sound.all.map { $0 == .brown ? 1 : 0 }, master: 0, rampSeconds: 0.5)
        let during = pull(renderer, seconds: 0.5).left
        let after = pull(renderer, seconds: 0.3).left

        func maxStep(_ x: [Float]) -> Float { zip(x.dropFirst(), x).map { abs($0 - $1) }.max() ?? 0 }
        XCTAssertLessThan(maxStep(during), maxStep(before) * 1.5 + 0.001, "a fade must not click")
        XCTAssertLessThan(rms(Array(during.suffix(2400))), rms(Array(during.prefix(2400))) * 0.2)
        XCTAssertLessThan(after.map(abs).max() ?? 0, 0.0002)
    }

    func testFadingInStartsFromSilence() {
        let mailbox = ParameterMailbox()
        let renderer = MixRenderer(sampleRate: sr, mailbox: mailbox, seed: 5)
        mailbox.publish(levels: Sound.all.map { $0 == .pink ? 0.8 : 0 }, master: 1, rampSeconds: 1)
        let out = pull(renderer, seconds: 1.5).left
        XCTAssertLessThan(out.prefix(200).map(abs).max() ?? 1, 0.01, "the first milliseconds must be near silence")
        XCTAssertGreaterThan(rms(Array(out.suffix(4800))), rms(Array(out.prefix(4800))) * 5)
    }

    func testChangingALevelDoesNotCutAFadeShort() {
        let (renderer, mailbox) = make(levels: [.brown: 1])
        _ = pull(renderer, seconds: 0.5)
        let levels = Sound.all.map { $0 == .brown ? Float(1) : 0 }
        mailbox.publish(levels: levels, master: 0, rampSeconds: 2)
        _ = pull(renderer, seconds: 0.2)
        mailbox.publish(levels: Sound.all.map { $0 == .brown ? Float(0.6) : 0 }, master: 0, rampSeconds: 0)
        let out = pull(renderer, seconds: 0.2).left
        XCTAssertGreaterThan(rms(out), 0.0005, "the fade should still be under way, not snapped to silence")
    }

    func testRenderingInOddBlockSizesMatchesEvenOnes() {
        let a = make(levels: [.rain: 0.7, .wind: 0.4], seed: 11).0
        let b = make(levels: [.rain: 0.7, .wind: 0.4], seed: 11).0
        let x = pull(a, seconds: 1, block: 512).left
        let y = pull(b, seconds: 1, block: 173).left
        XCTAssertEqual(x, y)
    }
}
