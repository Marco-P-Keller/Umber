import SwiftUI

struct SettingsView: View {
    @Environment(Player.self) private var player
    @Environment(\.dismiss) private var dismiss

    private var version: String {
        let short = Bundle.main.object(forInfoDictionaryKey: "CFBundleShortVersionString") as? String ?? "1"
        let build = Bundle.main.object(forInfoDictionaryKey: "CFBundleVersion") as? String ?? "1"
        return "\(short) (\(build))"
    }

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    Toggle("settings.mix", isOn: Binding(get: { player.mixWithOthers }, set: { player.setMixWithOthers($0) }))
                } footer: {
                    Text("settings.mix.footer")
                }
                Section {
                    Link("settings.privacy", destination: Links.privacy)
                    Link("settings.support", destination: Links.support)
                    LabeledContent("settings.version", value: version)
                } footer: {
                    Text("settings.promise")
                }
                Section {
                    EmptyView()
                } footer: {
                    Text(verbatim: "© Connexa GmbH")
                }
            }
            .scrollContentBackground(.hidden)
            .background(Theme.background)
            .navigationTitle("settings.title")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) { Button("common.done") { dismiss() } }
            }
        }
    }
}
