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

## Decisions that follow

- The **name** carries "Brown Noise" in the local language: cheap to rank for, and it is what the app does best.
- The **subtitle** carries "White Noise", "Pink", fan and rain, the terms a person actually types.
- The **keyword field** holds the rest (baby, focus, study, ADHD, tinnitus, ocean, wind, timer, nap) without repeating words from name or subtitle.
- No price word ("free") in any indexed field; it wastes characters and does not help ranking.
- Head terms in the US are not targeted directly. They come later, by association, once the app has ratings.
- Category Health & Fitness (secondary Lifestyle): less crowded with noise apps than Music and closer to the intent of sleep and focus.
- The name "Umber" had no conflicting app in the US, Swiss or German store at the time of measurement.
