import XCTest
@testable import Umber

@MainActor
final class PlayerTests: XCTestCase {
    private var host: SilentHost!
    private var suite: String!
    private var defaults: UserDefaults!

    override func setUp() {
        host = SilentHost()
        suite = "umber.tests.\(UUID().uuidString)"
        defaults = UserDefaults(suiteName: suite)
    }

    override func tearDown() {
        defaults.removePersistentDomain(forName: suite)
    }

    private func makePlayer() -> Player {
        Player(host: host, defaults: defaults, publishesNowPlaying: false)
    }

    func testTappingASoundStartsItAtAComfortableLevel() {
        let player = makePlayer()
        player.toggle(.rain)
        XCTAssertTrue(player.isPlaying)
        XCTAssertEqual(player.mix.level(.rain), Mix.defaultLevel)
        XCTAssertEqual(host.master, 1)
        XCTAssertEqual(host.levels[Sound.rain.index], Mix.defaultLevel)
    }

    func testTappingAgainTurnsItOffAndTheLastOneStopsPlayback() {
        let player = makePlayer()
        player.toggle(.rain)
        player.toggle(.wind)
        player.toggle(.rain)
        XCTAssertTrue(player.isPlaying)
        XCTAssertEqual(player.mix.active, [.wind])
        player.toggle(.wind)
        XCTAssertFalse(player.isPlaying)
        XCTAssertTrue(player.mix.isEmpty)
    }

    func testPlayWithNothingChosenFallsBackToFocus() {
        let player = makePlayer()
        player.play()
        XCTAssertEqual(player.mix, Preset.focus.mix)
    }

    func testPresetsReplaceTheMixAndStartPlayback() {
        let player = makePlayer()
        player.toggle(.fan)
        player.apply(.storm)
        XCTAssertEqual(player.mix, Preset.storm.mix)
        XCTAssertEqual(player.mix.level(.fan), 0)
        XCTAssertTrue(player.isPlaying)
    }

    func testMovingASliderNeverStartsPlaybackByItself() {
        let player = makePlayer()
        player.toggle(.brown)
        player.pause()
        player.setLevel(.brown, 0.3)
        XCTAssertFalse(player.isPlaying)
        XCTAssertEqual(player.mix.level(.brown), 0.3, accuracy: 0.0001)
    }

    func testTheMixSurvivesARelaunchButPlaybackDoesNot() {
        let first = makePlayer()
        first.apply(.shore)
        let second = makePlayer()
        XCTAssertEqual(second.mix, Preset.shore.mix)
        XCTAssertFalse(second.isPlaying)
    }

    func testMixWithOthersIsRememberedAndReachesTheHost() {
        let player = makePlayer()
        player.setMixWithOthers(true)
        XCTAssertTrue(host.mixWithOthers)
        XCTAssertTrue(makePlayer().mixWithOthers)
    }

    func testAnInterruptionPausesAndResumesOnlyWhenTheSystemSaysSo() {
        let player = makePlayer()
        player.toggle(.brown)
        host.onEvent?(.interruptionBegan)
        XCTAssertFalse(player.isPlaying)
        host.onEvent?(.interruptionEnded(shouldResume: true))
        XCTAssertTrue(player.isPlaying)

        host.onEvent?(.interruptionBegan)
        host.onEvent?(.interruptionEnded(shouldResume: false))
        XCTAssertFalse(player.isPlaying)
    }

    func testAnInterruptionDoesNotStartAnythingThatWasNotPlaying() {
        let player = makePlayer()
        player.toggle(.brown)
        player.pause()
        host.onEvent?(.interruptionBegan)
        host.onEvent?(.interruptionEnded(shouldResume: true))
        XCTAssertFalse(player.isPlaying)
    }

    func testUnpluggingHeadphonesPauses() {
        let player = makePlayer()
        player.toggle(.brown)
        host.onEvent?(.outputLost)
        XCTAssertFalse(player.isPlaying)
    }

    func testAnEngineThatWillNotStartIsReportedNotHidden() {
        host.failToStart = true
        let player = makePlayer()
        player.toggle(.brown)
        XCTAssertFalse(player.isPlaying)
        XCTAssertTrue(player.startFailed)
    }

    func testTheSleepTimerFadesAndStops() async throws {
        let player = makePlayer()
        player.toggle(.brown)
        player.startTimer(0.3)
        XCTAssertTrue(player.timer.isRunning)
        try await Task.sleep(for: .seconds(1.4))
        XCTAssertFalse(player.isPlaying)
        XCTAssertFalse(player.timer.isActive)
        XCTAssertFalse(host.isRunning)
    }

    func testPausingHoldsTheTimerAndPlayingResumesIt() {
        let player = makePlayer()
        player.toggle(.brown)
        player.startTimer(3_600)
        player.pause()
        XCTAssertNotNil(player.timer.pausedRemaining)
        XCTAssertNil(player.timer.endsAt)
        player.play()
        XCTAssertNotNil(player.timer.endsAt)
    }

    func testCancellingTheTimerLeavesTheSoundPlaying() {
        let player = makePlayer()
        player.toggle(.brown)
        player.startTimer(3_600)
        player.cancelTimer()
        XCTAssertTrue(player.isPlaying)
        XCTAssertFalse(player.timer.isActive)
    }

    func testStartingATimerWhilePausedStartsTheSound() {
        let player = makePlayer()
        player.startTimer(1_800)
        XCTAssertTrue(player.isPlaying)
        XCTAssertTrue(player.timer.isRunning)
    }

    func testEveryPresetIsInRangeAndUsesRealSounds() {
        for preset in Preset.all {
            XCTAssertFalse(preset.mix.isEmpty)
            for sound in preset.mix.active {
                XCTAssertTrue((0.05...1).contains(preset.mix.level(sound)), "\(preset.id)/\(sound)")
            }
        }
        XCTAssertEqual(Set(Preset.all.map(\.id)).count, Preset.all.count)
    }

    func testLaunchOptionsParse() {
        let o = LaunchOptions(arguments: ["Umber", "-UmberScene", "timer", "-UmberSilent"])
        XCTAssertEqual(o.scene, "timer")
        XCTAssertTrue(o.silent)
        XCTAssertTrue(o.opensTimer)
        XCTAssertNil(LaunchOptions(arguments: ["Umber", "-UmberScene"]).scene)
    }
}
