import SwiftUI

struct PlayerDock: View {
    @Binding var showTimer: Bool
    @Environment(Player.self) private var player

    var body: some View {
        HStack(spacing: 14) {
            Button { player.togglePlayback() } label: {
                Image(systemName: player.isPlaying ? "pause.fill" : "play.fill")
                    .font(.system(size: 24, weight: .semibold))
                    .contentTransition(.symbolEffect(.replace))
                    .foregroundStyle(.black)
                    .frame(width: 58, height: 58)
                    .background(Circle().fill(Color.accentColor))
            }
            .buttonStyle(.plain)
            .sensoryFeedback(.impact(weight: .light), trigger: player.isPlaying)
            .accessibilityLabel(Text(player.isPlaying ? "dock.pause" : "dock.play"))

            VStack(alignment: .leading, spacing: 2) {
                if player.mix.isEmpty {
                    Text("dock.idle").font(.subheadline.weight(.semibold))
                    Text("dock.idle.hint").font(.caption).foregroundStyle(.secondary)
                } else {
                    Text(player.summary).font(.subheadline.weight(.semibold)).lineLimit(1)
                    Text(player.isPlaying ? "dock.live" : "dock.paused").font(.caption).foregroundStyle(.secondary).lineLimit(1)
                }
            }
            Spacer(minLength: 0)

            Button { showTimer = true } label: { timerLabel }
                .buttonStyle(.plain)
                .accessibilityLabel(Text("timer.title"))
        }
        .padding(8)
        .padding(.trailing, 6)
        .surface()
        .padding(.horizontal, 16)
        .padding(.bottom, 8)
        .frame(maxWidth: 640)
        .frame(maxWidth: .infinity)
    }

    @ViewBuilder private var timerLabel: some View {
        if let end = player.timer.endsAt {
            HStack(spacing: 6) {
                Image(systemName: "timer")
                Text(timerInterval: Date.now...max(end, Date.now.addingTimeInterval(1)), countsDown: true)
                    .monospacedDigit()
            }
            .font(.subheadline.weight(.semibold))
            .padding(.horizontal, 14)
            .frame(height: 44)
            .background(Capsule().fill(Color.accentColor.opacity(0.18)))
            .foregroundStyle(Color.accentColor)
        } else if let paused = player.timer.pausedRemaining {
            HStack(spacing: 6) {
                Image(systemName: "timer")
                Text(Duration.seconds(paused).formatted(.time(pattern: .minuteSecond))).monospacedDigit()
            }
            .font(.subheadline.weight(.semibold))
            .padding(.horizontal, 14)
            .frame(height: 44)
            .background(Capsule().fill(Color.white.opacity(0.1)))
            .foregroundStyle(.secondary)
        } else {
            Image(systemName: "timer")
                .font(.system(size: 19, weight: .medium))
                .frame(width: 44, height: 44)
                .background(Circle().fill(Color.white.opacity(0.1)))
                .foregroundStyle(.primary)
        }
    }
}
