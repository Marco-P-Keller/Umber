import XCTest
@testable import Umber

/// Every visible string exists in every language the app declares, and no key leaks through raw.
final class LocalizationTests: XCTestCase {
    private let keys = [
        "sound.brown", "sound.pink", "sound.white", "sound.green", "sound.fan", "sound.rain", "sound.ocean",
        "sound.wind", "sound.womb", "preset.focus", "preset.sleep", "preset.storm", "preset.shore", "preset.baby",
        "dock.idle", "dock.idle.hint", "dock.live", "dock.paused", "dock.play", "dock.pause", "timer.title",
        "timer.stopsIn", "timer.cancel", "timer.footer", "common.done", "settings.title", "settings.mix",
        "settings.mix.footer", "settings.privacy", "settings.support", "settings.version", "settings.promise",
        "error.title", "error.message", "a11y.off", "intent.sound", "intent.play.title", "intent.stop.title",
    ]

    private var app: Bundle { Bundle(for: Player.self) }

    func testEveryDeclaredLanguageHasEveryString() {
        let languages = app.localizations.filter { $0 != "Base" }
        XCTAssertGreaterThanOrEqual(languages.count, 34)
        for language in languages {
            guard let path = app.path(forResource: language, ofType: "lproj"), let bundle = Bundle(path: path) else {
                XCTFail("no \(language).lproj"); continue
            }
            for key in keys {
                let value = bundle.localizedString(forKey: key, value: "⚠︎missing", table: nil)
                XCTAssertNotEqual(value, "⚠︎missing", "\(language) lacks \(key)")
                XCTAssertNotEqual(value, key, "\(language) shows the raw key \(key)")
            }
        }
    }

    func testTheSourceCodeOnlyUsesKeysTheCatalogKnows() throws {
        let root = URL(fileURLWithPath: #filePath).deletingLastPathComponent().deletingLastPathComponent()
        let enumerator = FileManager.default.enumerator(at: root.appendingPathComponent("Umber"), includingPropertiesForKeys: nil)!
        let pattern = try NSRegularExpression(pattern: "\"((?:sound|preset|dock|timer|settings|error|a11y|intent|common)\\.[A-Za-z.]+)\"")
        var used = Set<String>()
        for case let url as URL in enumerator where url.pathExtension == "swift" {
            let text = try String(contentsOf: url, encoding: .utf8)
            for m in pattern.matches(in: text, range: NSRange(text.startIndex..., in: text)) {
                used.insert(String(text[Range(m.range(at: 1), in: text)!]))
            }
        }
        XCTAssertFalse(used.isEmpty)
        XCTAssertEqual(used.subtracting(keys), [], "used in code but not localized")
    }
}
