import SwiftUI

@main
struct UmberApp: App {
    @State private var player = Player.shared

    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(player)
                .preferredColorScheme(.dark)
        }
    }
}
