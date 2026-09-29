import SwiftUI

struct PresetRow: View {
    @Environment(Player.self) private var player

    var body: some View {
        ScrollView(.horizontal) {
            HStack(spacing: 10) {
                ForEach(Preset.all) { preset in
                    let selected = player.mix == preset.mix
                    Button { player.apply(preset) } label: {
                        Label { Text(preset.title) } icon: { Image(systemName: preset.symbol) }
                            .font(.subheadline.weight(.semibold))
                            .padding(.horizontal, 16)
                            .padding(.vertical, 11)
                            .foregroundStyle(selected ? Color.black : Color.primary)
                            .background(Capsule().fill(selected ? Color.accentColor : Theme.card))
                            .overlay(Capsule().strokeBorder(selected ? .clear : Theme.cardStroke))
                    }
                    .buttonStyle(.plain)
                    .sensoryFeedback(.selection, trigger: selected)
                    .accessibilityAddTraits(selected ? .isSelected : [])
                }
            }
            .padding(.horizontal, 20)
        }
        .scrollIndicators(.hidden)
    }
}
