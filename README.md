# Umber

Brown noise, pink noise, white noise and six more calming sounds, generated live on iPhone and iPad. Nothing loops, nothing repeats. No ads, no accounts, no network.

Native SwiftUI, iOS 17+, 34 languages, published by Connexa GmbH.

## How the sound is made

Every sound is a small DSP kernel (`Umber/Audio`) run inside an `AVAudioSourceNode`, synthesized in fixed 256-frame chunks so it does not depend on the hardware buffer size. There are no audio files. The tests (`UmberTests/KernelTests.swift`) measure the spectrum of each generator: brown falls 6 dB per octave, pink 3, white is flat; each sound's loudness is trimmed to a measured target.

## Build

```
brew install xcodegen
xcodegen generate
open Umber.xcodeproj
```

Tests: `xcodebuild -project Umber.xcodeproj -scheme Umber -destination 'platform=iOS Simulator,name=iPhone 17 Pro Max' test CODE_SIGNING_ALLOWED=NO`

Launch arguments for screenshots: `-UmberScene focus|mix|timer|sleep|settings|library` and `-UmberSilent`.

## Shipping

`Tools/ship.sh [build-number]` archives, exports and uploads with the Apple ID signed into Xcode. The full App Store Connect walkthrough is in `docs/app-store-connect.md`, the listing text in `store/`, the ASO reasoning in `docs/aso.md` and `docs/market.md`.

## Layout

| Path | What |
|---|---|
| `Umber/` | app: `Audio`, `Model`, `Views`, `Intents`, `Resources` |
| `UmberTests/` | DSP measurements, player, timer, localization |
| `Tools/` | strings, icon, screenshots, store text generators |
| `store/` | App Store Connect content |
| `site/` | privacy and support pages (GitHub Pages) |
