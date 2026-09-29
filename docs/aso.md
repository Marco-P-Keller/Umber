# ASO and growth plan for Umber

Goal: as many organic downloads as possible, at least 100 per day. Read this honestly: nobody can promise a number. What can be controlled is that the listing matches the words people search, converts the people who look, and gets better every two weeks with real numbers.

## What is already built in

- **34 app languages, 39 store locales.** Most competitors ship in English only. Every locale has its own name, subtitle, keywords, promotional text, description and screenshots (`store/`). Each additional storefront is an additional search index.
- **Uncontested names.** See `market.md`: the local words for "brown noise" have 0 to 40 competitors in most of Europe and Asia.
- **Screenshots that state the promise.** Caption 1 is "Brown noise that never loops" (the real differentiator: sounds are generated, not recorded), caption 5 "No ads. No accounts. Offline.", the thing reviews of competitors complain about.
- **Ratings prompt** only after three sessions of ten minutes or more, once. Good moment, no nagging.
- **Siri and Shortcuts** ("Play brown noise in Umber") for retention and for App Store search suggestions.
- **Size and speed**: the app is small, starts instantly, needs no network.

## Keyword field notes

- Apple indexes name, subtitle and keywords as one pool and combines words across fields into phrases. A word written twice wastes space. `Tools/make-store.py` fails if a word repeats.
- Es-MX, en-CA, en-AU and en-GB carry different extra English keywords on purpose. The US storefront is commonly reported to also index the es-MX keyword field; this is common ASO practice and not measured here, so treat it as a cheap bet, not a fact.

## The first 30 days

| When | Do | Measure |
|---|---|---|
| Launch day | Release in all 175 storefronts. Put the link in your own channels. | Impressions and product page views in App Analytics |
| Week 1 | Ask friends and family for an honest rating (the in-app prompt handles the rest). A rating average above 4.5 lifts conversion. | Rating count, conversion (downloads / product page views) |
| Week 2 | Read Search Terms in App Analytics. Replace keywords that produce zero impressions in each large locale. | Impressions per keyword |
| Week 3 | Change the promotional text (no review needed) to test wording; try a new first screenshot caption through a Product Page Optimization test. | Conversion of the test |
| Week 4 | Move the best-converting locale's wording to similar languages. | Downloads per locale |

Rule: change at most two things per fortnight, so the cause of a change is known.

## Custom product pages (free, up to 70)

Create one per intent and use it as a link in posts and communities:

1. **Baby** (screenshot 4 first): link in parenting forums.
2. **ADHD and focus** (screenshot 1 first): communities for brown noise and study.
3. **Sleep timer** (screenshot 3 first): sleep and insomnia communities.

## Where the first users come from

- Search: the locales where competition is empty (DE, FR, IT, ES, RU, TR, JP) should deliver the first steady trickle.
- Communities that already talk about brown noise (ADHD, study and parenting communities). Do not post promotion without adding something: share the fact that this brown noise never loops and how the timer works.
- A short screen-recorded demo with the actual sound: brown noise is a sound product, so show the sound.

## When to worry

- Impressions high, downloads low: the first screenshot or the name is wrong. Test the caption.
- Impressions low: the keywords miss. Check Search Terms, replace them.
- Downloads fine, ratings low: read the reviews and fix that first.
