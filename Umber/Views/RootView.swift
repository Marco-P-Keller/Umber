import StoreKit
import SwiftUI

struct RootView: View {
    @Environment(Player.self) private var player
    @Environment(\.scenePhase) private var scenePhase
    @Environment(\.requestReview) private var requestReview
    @Environment(\.horizontalSizeClass) private var sizeClass

    @State private var showTimer = LaunchOptions.current.opensTimer
    @State private var showSettings = LaunchOptions.current.opensSettings

    private var columns: [GridItem] {
        Array(repeating: GridItem(.flexible(), spacing: 12), count: sizeClass == .regular ? 3 : 2)
    }

    var body: some View {
        @Bindable var player = player
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 22) {
                    header
                    PresetRow()
                    LazyVGrid(columns: columns, spacing: 12) {
                        ForEach(Sound.all) { SoundTile(sound: $0) }
                    }
                    .padding(.horizontal, 20)
                }
                .padding(.top, 4)
                .padding(.bottom, 24)
                .frame(maxWidth: 900)
                .frame(maxWidth: .infinity)
            }
            .scrollIndicators(.hidden)
            .background(AmbientBackground())
            .toolbar(.hidden, for: .navigationBar)
            .safeAreaInset(edge: .bottom) { PlayerDock(showTimer: $showTimer) }
        }
        .sheet(isPresented: $showTimer) { TimerSheet() }
        .sheet(isPresented: $showSettings) { SettingsView() }
        .alert("error.title", isPresented: $player.startFailed) {
        } message: {
            Text("error.message")
        }
        .task(id: player.reviewPending && scenePhase == .active) {
            guard player.reviewPending, scenePhase == .active else { return }
            try? await Task.sleep(for: .seconds(1.5))
            guard !Task.isCancelled else { return }
            player.reviewWasRequested()
            requestReview()
        }
    }

    private var header: some View {
        HStack {
            Text(verbatim: "Umber")
                .font(.largeTitle.bold())
                .accessibilityAddTraits(.isHeader)
            Spacer()
            Button { showSettings = true } label: {
                Label("settings.title", systemImage: "gearshape")
                    .labelStyle(.iconOnly)
                    .font(.body.weight(.medium))
                    .frame(width: 44, height: 44)
                    .background(.white.opacity(0.08), in: Circle())
            }
            .buttonStyle(.plain)
        }
        .padding(.horizontal, 20)
    }
}
