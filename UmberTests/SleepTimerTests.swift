import XCTest
@testable import Umber

final class SleepTimerTests: XCTestCase {
    private let t0 = Date(timeIntervalSinceReferenceDate: 1_000)

    func testCountsDown() {
        var timer = SleepTimer()
        timer.start(600, now: t0)
        XCTAssertEqual(timer.remaining(now: t0.addingTimeInterval(100)), 500)
        XCTAssertEqual(timer.remaining(now: t0.addingTimeInterval(700)), 0)
        XCTAssertTrue(timer.isRunning)
    }

    func testPauseFreezesAndResumeContinues() {
        var timer = SleepTimer()
        timer.start(600, now: t0)
        timer.pause(now: t0.addingTimeInterval(200))
        XCTAssertFalse(timer.isRunning)
        XCTAssertTrue(timer.isActive)
        XCTAssertEqual(timer.remaining(now: t0.addingTimeInterval(9_000)), 400)
        timer.resume(now: t0.addingTimeInterval(1_000))
        XCTAssertEqual(timer.remaining(now: t0.addingTimeInterval(1_100)), 300)
    }

    func testCancelClearsEverything() {
        var timer = SleepTimer()
        timer.start(60, now: t0)
        timer.cancel()
        XCTAssertFalse(timer.isActive)
        XCTAssertNil(timer.remaining(now: t0))
        XCTAssertNil(timer.duration)
    }

    func testPausingAnIdleTimerDoesNothing() {
        var timer = SleepTimer()
        timer.pause(now: t0)
        timer.resume(now: t0)
        XCTAssertEqual(timer, SleepTimer())
    }

    func testTheOptionsAreAscendingAndLongerThanTheFade() {
        XCTAssertEqual(SleepTimer.options, SleepTimer.options.sorted())
        XCTAssertGreaterThan(SleepTimer.options.first ?? 0, SleepTimer.fadeDuration * 10)
    }
}
