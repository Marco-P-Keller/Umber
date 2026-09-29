# store/

Everything that goes into App Store Connect.

- `app-information.md`: every non-localized field (category, age rating, privacy, URLs, pricing).
- `review-notes.txt`: paste into App Review Information.
- `PASTE.md`: name, subtitle, keywords and promotional text for all 39 locales.
- `<locale>/`: one folder per App Store Connect locale with `name.txt`, `subtitle.txt`, `keywords.txt`, `promotional_text.txt`, `description.txt`.
- `screenshots/<locale>/iphone-6.9/` and `ipad-13/`: 5 PNGs each (not in git; rebuild with `Tools/capture-screens.py` then `Tools/make-shots.py`).

The text is generated from `Tools/listing_data.py` by `Tools/make-store.py`, which also checks every length limit and repeated keywords. Edit the data file, never the generated `.txt` files.
