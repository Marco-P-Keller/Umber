#!/bin/bash
# Archive Umber and upload it to App Store Connect with the Apple ID signed into Xcode.
# No API key needed: -allowProvisioningUpdates fetches the distribution profile.
# Usage: Tools/ship.sh [build-number]
set -euo pipefail
cd "$(dirname "$0")/.."

if [ "${1:-}" != "" ]; then
  sed -i '' "s/CURRENT_PROJECT_VERSION: \".*\"/CURRENT_PROJECT_VERSION: \"$1\"/" project.yml
fi

python3 Tools/make-strings.py
xcodegen generate
rm -rf build/Umber.xcarchive build/export
xcodebuild -project Umber.xcodeproj -scheme Umber -configuration Release \
  -destination 'generic/platform=iOS' -archivePath build/Umber.xcarchive \
  -allowProvisioningUpdates archive
xcodebuild -exportArchive -archivePath build/Umber.xcarchive -exportPath build/export \
  -exportOptionsPlist ExportOptions-upload.plist -allowProvisioningUpdates
echo "Uploaded. Wait for processing in App Store Connect > TestFlight, then attach the build to version 1.0."
