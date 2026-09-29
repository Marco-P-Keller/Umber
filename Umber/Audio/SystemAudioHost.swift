import AVFoundation
import Foundation

@MainActor
final class SystemAudioHost: AudioHost {
    var onEvent: (@MainActor (AudioEvent) -> Void)?
    var mixWithOthers = false {
        didSet {
            if engine.isRunning { try? configureSession() }
        }
    }

    private let engine = AVAudioEngine()
    private let mailbox = ParameterMailbox()
    private var node: AVAudioSourceNode?
    private var builtRate: Double = 0
    private var lastLevels = [Float](repeating: 0, count: Sound.all.count)
    private var wantsRunning = false
    private var generation = 0
    private var observers: [NSObjectProtocol] = []

    init() {
        let center = NotificationCenter.default
        let session = AVAudioSession.sharedInstance()
        observers = [
            center.addObserver(forName: AVAudioSession.interruptionNotification, object: session, queue: .main) { [weak self] note in
                let kind = (note.userInfo?[AVAudioSessionInterruptionTypeKey] as? UInt).flatMap(AVAudioSession.InterruptionType.init)
                let options = (note.userInfo?[AVAudioSessionInterruptionOptionKey] as? UInt).map(AVAudioSession.InterruptionOptions.init)
                MainActor.assumeIsolated { self?.interruption(kind, options) }
            },
            center.addObserver(forName: AVAudioSession.routeChangeNotification, object: session, queue: .main) { [weak self] note in
                let reason = (note.userInfo?[AVAudioSessionRouteChangeReasonKey] as? UInt).flatMap(AVAudioSession.RouteChangeReason.init)
                MainActor.assumeIsolated { self?.routeChanged(reason) }
            },
            center.addObserver(forName: .AVAudioEngineConfigurationChange, object: engine, queue: .main) { [weak self] _ in
                MainActor.assumeIsolated { self?.configurationChanged() }
            },
            center.addObserver(forName: AVAudioSession.mediaServicesWereResetNotification, object: session, queue: .main) { [weak self] _ in
                MainActor.assumeIsolated { self?.mediaServicesReset() }
            },
        ]
    }

    deinit {
        observers.forEach(NotificationCenter.default.removeObserver)
    }

    func start() throws {
        generation += 1
        try configureSession()
        try buildGraphIfNeeded()
        if !engine.isRunning { try engine.start() }
        wantsRunning = true
    }

    func update(levels: [Float], master: Float, ramp: TimeInterval) {
        lastLevels = levels
        mailbox.publish(levels: levels, master: master, rampSeconds: Float(ramp))
    }

    func stop(fade: TimeInterval) {
        wantsRunning = false
        generation += 1
        let mine = generation
        mailbox.publish(levels: lastLevels, master: 0, rampSeconds: Float(fade))
        Task { [weak self] in
            try? await Task.sleep(for: .seconds(fade + 0.2))
            guard let self, self.generation == mine else { return }
            self.engine.stop()
        }
    }

    // MARK: Graph

    private func configureSession() throws {
        let session = AVAudioSession.sharedInstance()
        try session.setCategory(.playback, mode: .default, options: mixWithOthers ? [.mixWithOthers] : [])
        try session.setActive(true)
    }

    private func buildGraphIfNeeded() throws {
        let reported = AVAudioSession.sharedInstance().sampleRate
        let rate = reported > 0 ? reported : 48_000
        if node != nil, builtRate == rate { return }

        if let node {
            engine.stop()
            engine.detach(node)
        }
        let renderer = MixRenderer(sampleRate: Float(rate), mailbox: mailbox)
        guard let format = AVAudioFormat(standardFormatWithSampleRate: rate, channels: 2) else {
            throw CocoaError(.featureUnsupported)
        }
        let source = AVAudioSourceNode(format: format) { _, _, frames, bufferList in
            let buffers = UnsafeMutableAudioBufferListPointer(bufferList)
            guard buffers.count >= 2,
                  let left = buffers[0].mData?.assumingMemoryBound(to: Float.self),
                  let right = buffers[1].mData?.assumingMemoryBound(to: Float.self) else { return noErr }
            renderer.render(frames: Int(frames), left: left, right: right)
            return noErr
        }
        engine.attach(source)
        engine.connect(source, to: engine.mainMixerNode, format: format)
        node = source
        builtRate = rate
    }

    // MARK: Notifications

    private func interruption(_ kind: AVAudioSession.InterruptionType?, _ options: AVAudioSession.InterruptionOptions?) {
        switch kind {
        case .began:
            onEvent?(.interruptionBegan)
        case .ended:
            onEvent?(.interruptionEnded(shouldResume: options?.contains(.shouldResume) ?? false))
        default:
            break
        }
    }

    private func routeChanged(_ reason: AVAudioSession.RouteChangeReason?) {
        if reason == .oldDeviceUnavailable { onEvent?(.outputLost) }
    }

    private func configurationChanged() {
        guard wantsRunning else { return }
        do {
            try buildGraphIfNeeded()
            if !engine.isRunning { try engine.start() }
        } catch {
            onEvent?(.engineFailed)
        }
    }

    private func mediaServicesReset() {
        node = nil
        builtRate = 0
        guard wantsRunning else { return }
        do {
            try configureSession()
            try buildGraphIfNeeded()
            try engine.start()
            mailbox.publish(levels: lastLevels, master: 1, rampSeconds: 0.5)
        } catch {
            onEvent?(.engineFailed)
        }
    }
}
