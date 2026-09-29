import SwiftUI

struct TimerSheet: View {
    @Environment(Player.self) private var player
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            List {
                if player.timer.isActive {
                    Section {
                        HStack {
                            Text("timer.stopsIn")
                            Spacer()
                            if let end = player.timer.endsAt {
                                Text(timerInterval: Date.now...max(end, Date.now.addingTimeInterval(1)), countsDown: true)
                                    .monospacedDigit().foregroundStyle(Color.accentColor)
                            } else if let paused = player.timer.pausedRemaining {
                                Text(Duration.seconds(paused).formatted(.time(pattern: .minuteSecond)))
                                    .monospacedDigit().foregroundStyle(.secondary)
                            }
                        }
                        Button("timer.cancel", role: .destructive) {
                            player.cancelTimer()
                            dismiss()
                        }
                    }
                }
                Section {
                    ForEach(SleepTimer.options, id: \.self) { length in
                        Button {
                            player.startTimer(length)
                            dismiss()
                        } label: {
                            HStack {
                                Text(Duration.seconds(length).formatted(.units(allowed: [.hours, .minutes], width: .wide)))
                                    .foregroundStyle(.primary)
                                Spacer()
                                if player.timer.duration == length {
                                    Image(systemName: "checkmark").foregroundStyle(Color.accentColor)
                                }
                            }
                        }
                    }
                } footer: {
                    Text("timer.footer")
                }
            }
            .scrollContentBackground(.hidden)
            .background(Theme.background)
            .navigationTitle("timer.title")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) { Button("common.done") { dismiss() } }
            }
        }
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
    }
}
