import SwiftUI

struct SoundTile: View {
    let sound: Sound

    @Environment(Player.self) private var player
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @Environment(\.horizontalSizeClass) private var sizeClass

    private var level: Float { player.mix.level(sound) }
    private var isOn: Bool { level > 0 }
    private var isSounding: Bool { isOn && player.isPlaying }

    var body: some View {
        ZStack(alignment: .bottom) {
            Button { player.toggle(sound) } label: { face }
                .buttonStyle(TileStyle(tint: sound.tint, isOn: isOn))
                .sensoryFeedback(.selection, trigger: isOn)
                .accessibilityLabel(Text(sound.title))
                .accessibilityValue(isOn ? Text(Double(level).formatted(.percent.precision(.fractionLength(0)))) : Text("a11y.off"))
                .accessibilityAdjustableAction { direction in
                    let step: Float = direction == .increment ? 0.1 : -0.1
                    if isOn { player.setLevel(sound, max(0.05, level + step)) } else if direction == .increment { player.toggle(sound) }
                }

            if isOn {
                Slider(value: Binding(get: { Double(level) }, set: { player.setLevel(sound, Float($0)) }), in: 0.05...1)
                    .tint(sound.tint)
                    .padding(.horizontal, 14)
                    .padding(.bottom, 12)
                    .accessibilityHidden(true)
                    .transition(.opacity)
            }
        }
        .animation(reduceMotion ? nil : .smooth(duration: 0.25), value: isOn)
    }

    private var face: some View {
        VStack(alignment: .leading, spacing: 0) {
            glyph
            Spacer(minLength: 8)
            Text(sound.title)
                .font(.headline)
                .foregroundStyle(.primary)
                .lineLimit(1)
                .minimumScaleFactor(0.8)
            Color.clear.frame(height: 30)
        }
        .padding(14)
        .frame(maxWidth: .infinity, minHeight: sizeClass == .regular ? 180 : 128, alignment: .topLeading)
    }

    @ViewBuilder private var glyph: some View {
        if let symbol = sound.symbol {
            Image(systemName: symbol)
                .font(.system(size: 22, weight: .medium))
                .foregroundStyle(isOn ? sound.tint : Color.secondary)
                .symbolEffect(.pulse, isActive: isSounding && !reduceMotion)
                .frame(height: 26, alignment: .bottom)
                .accessibilityHidden(true)
        } else {
            SpectrumGlyph(bars: sound.spectrum, tint: isOn ? sound.tint : Color.secondary, animated: isSounding)
        }
    }
}

struct TileStyle: ButtonStyle {
    let tint: Color
    let isOn: Bool

    func makeBody(configuration: Configuration) -> some View {
        let shape = RoundedRectangle(cornerRadius: 24, style: .continuous)
        configuration.label
            .background(shape.fill(isOn ? tint.opacity(0.16) : Theme.card))
            .overlay(shape.strokeBorder(isOn ? tint.opacity(0.55) : Theme.cardStroke, lineWidth: isOn ? 1.5 : 1))
            .contentShape(shape)
            .scaleEffect(configuration.isPressed ? 0.97 : 1)
            .animation(.snappy(duration: 0.18), value: configuration.isPressed)
    }
}
