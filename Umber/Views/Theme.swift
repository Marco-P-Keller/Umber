import SwiftUI

enum Theme {
    static let background = Color("LaunchBackground")
    static let card = Color.white.opacity(0.07)
    static let cardStroke = Color.white.opacity(0.09)
}

enum Links {
    static let privacy = URL(string: "https://marco-p-keller.github.io/Umber/privacy.html")!
    static let support = URL(string: "https://marco-p-keller.github.io/Umber/support.html")!
}

/// The floating player and the sheet chrome share one surface: Liquid Glass where the system has it,
/// a material everywhere else.
struct SurfaceBackground: ViewModifier {
    let cornerRadius: CGFloat

    func body(content: Content) -> some View {
        let shape = RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
        if #available(iOS 26.0, *) {
            content.glassEffect(.regular, in: shape)
        } else {
            content
                .background(.regularMaterial, in: shape)
                .overlay(shape.strokeBorder(Color.white.opacity(0.08)))
        }
    }
}

extension View {
    func surface(cornerRadius: CGFloat = 32) -> some View {
        modifier(SurfaceBackground(cornerRadius: cornerRadius))
    }
}

/// A soft wash of the dominant sound's colour behind everything, so the room takes on the mix.
struct AmbientBackground: View {
    @Environment(Player.self) private var player

    var body: some View {
        ZStack {
            Theme.background
            RadialGradient(colors: [(player.mix.dominant?.tint ?? .clear).opacity(0.26), .clear],
                           center: .top, startRadius: 0, endRadius: 520)
                .blendMode(.plusLighter)
                .animation(.easeInOut(duration: 1.2), value: player.mix.dominant)
        }
        .ignoresSafeArea()
    }
}
