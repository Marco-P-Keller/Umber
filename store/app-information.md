# App Store Connect: every field that is not localized text

Paste these once. The per-locale text lives in `store/<locale>/` (run `python3 Tools/make-store.py` to regenerate and re-check the limits).

## App record (My Apps > +)

| Field | Value |
|---|---|
| Platforms | iOS (iPhone and iPad; the build is universal) |
| Name (primary language) | `Umber: Brown Noise & Sleep` (en-US) |
| Primary language | English (U.S.) |
| Bundle ID | `com.connexa.umber` (register it under Certificates, Identifiers & Profiles first if it is not in the list; enable no capabilities) |
| SKU | `umber-ios-1` |
| User access | Full access |

## App Information

| Field | Value |
|---|---|
| Subtitle | from `store/<locale>/subtitle.txt` |
| Category (primary) | Health & Fitness |
| Category (secondary) | Lifestyle |
| Content rights | Does not contain, show or access third-party content |
| Age rating | 4+ (answer "None" / "No" to every question) |
| Privacy Policy URL | https://marco-p-keller.github.io/Umber/privacy.html |

## Pricing and Availability

| Field | Value |
|---|---|
| Price | Free (tier 0) |
| Availability | All 175 countries and regions |
| Pre-orders | Off |

## Version 1.0 page (per locale, from `store/<locale>/`)

| Field | Source |
|---|---|
| Promotional Text | `promotional_text.txt` (170 chars, can be changed any time without review) |
| Description | `description.txt` |
| Keywords | `keywords.txt` (100 chars, comma separated) |
| Support URL | https://marco-p-keller.github.io/Umber/support.html |
| Marketing URL | https://marco-p-keller.github.io/Umber/ (optional) |
| Version | 1.0 |
| Copyright | `2026 Connexa GmbH` |
| Screenshots | `store/screenshots/<locale>/iphone-6.9/*.png` (1320 x 2868) and `ipad-13/*.png` (2064 x 2752) |
| App Preview | none |
| What's New | not shown for version 1.0 |

## App Review Information

| Field | Value |
|---|---|
| Sign-in required | No |
| Contact | your name, phone and email (Apple only, never shown publicly) |
| Notes | paste `store/review-notes.txt` |
| Attachment | none needed |

## App Privacy

- Data collection: **"No, we do not collect data from this app"** → shows "Data Not Collected".
- The build also carries `PrivacyInfo.xcprivacy` (no tracking, no collected types, UserDefaults reason CA92.1).

## Export compliance

`ITSAppUsesNonExemptEncryption = NO` is already set in Info.plist, so no question is asked on upload. If the form still appears: "None of the algorithms mentioned above".

## Other

- Advertising Identifier (IDFA): **No**.
- Digital Services Act trader status (EU): fill in as Connexa GmbH.
- Game Center, In-App Purchases, Subscriptions, Sign in with Apple: none.
- Accessibility Nutrition Label (optional): VoiceOver, Voice Control, Larger Text, Dark Interface, Sufficient Contrast, Reduced Motion are supported.
