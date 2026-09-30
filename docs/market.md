# Market measurements (iTunes Search API, September 2026)

Method: for each storefront and search term, the top 10 results and their rating counts. Rating count is a proxy for how hard a term is to win. "Median" is the median of the ten.

## United States

| Term | Median ratings of top 10 | Comment |
|---|---|---|
| white noise | 169,685 | out of reach for a new app |
| sound machine | 169,685 | same |
| sleep sounds | 62,786 | same |
| fan sound | 30,030 | hard |
| baby white noise | 2,531 | reachable later |
| brown noise | 3,178 | four of the top ten under 1,000 ratings: **reachable** |
| pink noise | 1,554 | four of the top ten under 1,000: **reachable** |
| noise generator | 866 | five of the top ten under 1,000: **reachable** |

## Outside the US

The localized "brown noise" is almost empty. Number of results that carry the term in the store listing (fewer is better):

| Storefront | Term | Competing results |
|---|---|---|
| Germany | braunes Rauschen | 39 |
| France | bruit brun | 0 |
| Italy | rumore marrone | 0 |
| Spain | ruido marrón | 5 |
| Russia | коричневый шум | 1 |
| Turkey | kahverengi gürültü | 2 |
| Japan | ブラウンノイズ | 13 |
| Korea | 브라운 노이즈 | 38 |
| Brazil | ruído marrom | 465 |
| UK / Australia / Canada | brown noise | 85 / 21 / 120 |

"White noise" localized is mid-sized in the big markets (DE 602, FR 632, ES 349, IT 413, JP 694, KR 3,227, CN 2,304, TW 798, RU 979, BR 1,642) and small in NL, PL, SE, TR, SA, ID, TH, VN, UA, CZ, GR, IL, IN.

## Search volume (Apple search suggestions, 30 September 2026)

Method: type the term one letter at a time into the App Store suggestion service of each storefront; "letters" is how many it takes before the term is suggested. Fewer letters means more people search it. Combined with the rating counts of the top 10 this gives volume against difficulty.

| Storefront | Term | Letters | Median ratings of top 10 | Verdict |
|---|---|---|---|---|
| US | brown noise | 4 | 2,027 | name |
| US | womb sounds | 4 | 1,209 | subtitle (was keyword) |
| US | tinnitus relief | 4 (first suggestion) | 612 | keywords: tinnitus, relief |
| US | insomnia | 4 | 1,545 | keywords |
| US | red noise (= brown noise) | 5 | 2,460, no app has it in the title | keywords |
| US | pink noise | 6 | 2,210 | subtitle |
| US | noise generator | 7 (first suggestion) | 866 | keywords |
| US | green noise / wind sounds | 7 | 1,092 / 83 | keywords |
| US | colic | 5 | 33 | keywords |
| US | white noise / sleep sounds / noise machine | 2-3 | 90,000-200,000 | only by association |
| US | nap / calm / adhd / relax | - | Snapchat, Calm, planners | dropped |
| UK | fan noise | 5 (first) | 166 | fan in subtitle |
| UK | womb sounds / brown noise / green noise | 4 / 4 / 7 | 55 / 94 / 63 | covered |
| Germany | white noise (English) | 3 | 1,255 | covered through en-GB |
| Germany | brown noise (English) / braunes Rauschen | 4 / 6 | 21 / 31 | en-GB name / de name |
| Germany | einschlafgeräusche, meeresrauschen, beruhigung | 4 | beruhigung 24 | de keywords |
| Spain | acúfenos (tinnitus) | 3 (first) | 8 | es keywords |
| France | sons pour dormir | 4 (first) | 356 | "sons" added |
| Japan | 胎内音, 扇風機, 雨音, 睡眠導入, 入眠 | 1 | 扇風機 9 | subtitle and keywords |
| Korea | 브라운노이즈 (no space) | 3 | 38 | name written without the space |
| Korea | 이명 (tinnitus), 불면증, 선풍기 | 1-2 | 3 / 1,951 / 33 | keywords and subtitle |
| Brazil | sons para dormir | 4 (first) | 2,511 | "sons" added |

## Which locales a storefront searches

Apple's table (App Store Connect Help > Reference > App Store localizations) decides where each keyword counts:

- **en-GB is searched in every storefront except the US, Canada and Japan.** It carries the full English set and is as important as en-US.
- The US searches en-US plus es-MX, fr-FR, pt-BR, ko, ru, vi, ar-SA and both Chinese locales. Japan searches ja plus en-US. Canada searches en-CA plus fr-CA. Australia and New Zealand search en-AU plus en-GB.
- A word that the co-searched English locale already holds is wasted, so the local keyword fields no longer repeat tinnitus, timer, baby, wind, ocean or focus, es-MX carries no English, and en-AU carries only words en-GB lacks. `Tools/make-store.py` fails on any such duplicate (accents ignored, as Apple does).

## Decisions that follow

- The **name** carries "Brown Noise" in the local language: cheap to rank for, and it is what the app does best.
- The **subtitle** carries "White & Pink Noise", fan and womb: the most searched terms that a new app can still win or that feed long-tail phrases.
- The **keyword field** holds the rest (tinnitus, relief, insomnia, red, green, generator, colic, rain, wind, ocean) without repeating words from name or subtitle.
- Words that describe something the app does not do (lullaby, shush, heartbeat, other apps' names) stay out even where they are popular: they bring people who leave, and guideline 2.3.7 forbids them.
- No price word ("free") in any indexed field; it wastes characters and does not help ranking.
- Head terms in the US are not targeted directly. They come later, by association, once the app has ratings.
- Category Health & Fitness (secondary Lifestyle): less crowded with noise apps than Music and closer to the intent of sleep and focus.
- The name "Umber" had no conflicting app in the US, Swiss or German store at the time of measurement.
