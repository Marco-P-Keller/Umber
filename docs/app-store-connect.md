# Getting Umber into the App Store, in order

1. **Register the bundle ID** `com.connexa.umber` (Developer portal > Identifiers). No capabilities needed.
2. **Create the app** in App Store Connect with the values in `store/app-information.md`.
3. **Upload the build**: `Tools/ship.sh` archives, exports with `-allowProvisioningUpdates` and uploads with the account signed into Xcode. No API key needed. Wait for "Ready to Submit" processing (5-15 min).
4. **Add localizations.** In the version page use the language menu > add all 39, and paste per locale from `store/<locale>/`. Faster: the paste order is name, subtitle, promotional text, description, keywords.
5. **Upload screenshots** per locale from `store/screenshots/<locale>/`: the iPhone 6.9" set (5 files) and the iPad 13" set (5 files). Apple scales them down to the other sizes.
6. **App Privacy**: "Data Not Collected". Age rating: all "None" (4+). Category Health & Fitness, secondary Lifestyle.
7. **Review notes** from `store/review-notes.txt`, select the build, **Submit for Review**.
8. Choose "Manually release" for the first version only if you want to line up the launch (see the growth plan in `docs/aso.md`).
