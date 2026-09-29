import SwiftUI

/// Seven bars that draw how much energy a colour of noise has at each frequency. While the sound is
/// playing they breathe a little.
struct SpectrumGlyph: View {
    let bars: [Double]
    let tint: Color
    let animated: Bool

    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        TimelineView(.animation(minimumInterval: 1.0 / 20, paused: !animated || reduceMotion)) { context in
            let t = context.date.timeIntervalSinceReferenceDate
            HStack(alignment: .bottom, spacing: 3) {
                ForEach(bars.indices, id: \.self) { i in
                    let wobble = animated && !reduceMotion ? 0.09 * sin(t * 2.2 + Double(i) * 0.9) : 0
                    Capsule()
                        .fill(tint)
                        .frame(width: 4, height: max(4, 26 * min(1, bars[i] + wobble)))
                }
            }
            .frame(height: 26, alignment: .bottom)
            .environment(\.layoutDirection, .leftToRight)
        }
        .accessibilityHidden(true)
    }
}
