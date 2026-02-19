# Oscar Short Film Predictor

https://bestshortfilmpredicition.netlify.app/

A novel statistical model for predicting the **Academy Award for Best Live Action Short Film** — the one Oscar category that Ben Zauzmer and other prediction models explicitly skip due to lack of data.

## Background

Established Oscar prediction methods (Zauzmer's *Oscarmetrics*, Gold Derby aggregators) work by weighting precursor awards — guild wins, BAFTA, Golden Globes. Short films don't have this infrastructure. There's no DGA for shorts, no SAG, minimal critic aggregation. So every major predictor falls back to betting markets and intuition.

This project asks: is there independent signal hiding elsewhere? The answer is yes.

---

## What's in this repo

| File | Description |
|------|-------------|
| `oscar_shorts_predictor.py` | Full dataset + model pipeline |
| `oscar_short_film_predictor_2026.html` | Visual report for the 2026 ceremony |

---

## The Model

### Data

- **19 years** of nominees (2006–2025)
- **95 total data points** (5 nominees × ~19 years)
- Hand-coded from Wikipedia, BAFTA records, historical betting odds, and festival databases

### Features

| Feature | Description |
|---------|-------------|
| `language_english` | 1 if primarily English-language |
| `runtime_min` | Runtime in minutes |
| `director_prior_oscar_nom` | Director had previous Oscar nomination |
| `festival_prestige_score` | 0–3 scale (unknown → national → major intl → Cannes/Venice/TIFF) |
| `platform_tier` | 0–3 scale (unknown → small → major → Netflix/A24/New Yorker) |
| `subject_gravity` | 0=comedy/light, 1=drama, 2=heavy social/political/war |
| `bafta_win` | Won BAFTA short film award |
| `bafta_nom` | Nominated for BAFTA short film award |
| `betting_favorite` | Was consensus betting favorite going into ceremony |
| `ireland_uk` | UK or Ireland production |
| `runtime_bucket` | Binned runtime (sweet spot = 16–25 min) |
| `platform_x_festival` | **Interaction term**: platform tier × festival score |
| `bafta_x_english` | **Interaction term**: BAFTA nom × English language |

The two interaction terms are the novel contribution — neither appears in any prior Oscar prediction literature.

### Models

Two models are trained and ensembled:

- **Logistic Regression** (L2 regularized, C=0.5) — interpretable, good with sparse data
- **Random Forest** (200 trees, max_depth=3) — captures non-linear interactions

Final predictions are averaged and normalized per year (probabilities sum to 1.0 per ceremony).

### Validation

**Leave-One-Year-Out (LOYO) cross-validation**: for each year, the model is trained on all *other* years, then predicts that year's winner. This is the honest evaluation — the model never sees the future.

| Model | Pick Accuracy | Brier Score |
|-------|--------------|-------------|
| Random Forest | **63%** | 0.119 |
| Ensemble | 53% | 0.121 |
| Logistic Regression | 53% | 0.126 |
| Random baseline | 20% | ~0.160 |

---

## Key Findings

### What actually predicts winners

1. **Betting favorite** (21.6% importance) — markets are right ~58% of the time but wrong often enough to justify a model
2. **Platform tier** (15.9%) — films distributed by The New Yorker, Netflix, A24 win disproportionately; voter accessibility matters
3. **Platform × Festival interaction** (15.6%) — a prestigious festival film *with* strong distribution is far more likely to win than either alone
4. **BAFTA × English interaction** (10.3%) — a BAFTA-nominated English-language film wins 50%+ of the time

### Counterintuitive results

- **Heavy subject matter is NOT a positive predictor.** Films about war, politics, and trauma win only ~14% of the time — below baseline. Voters favor formal inventiveness over gravity.
- **Prior Oscar nominations for the director weakly hurt.** Small sample, but the pattern suggests Academy voters in this category tend to discover new voices.
- **Runtime matters.** The 16–25 minute window is the sweet spot. Very short films feel slight; very long ones overstay their welcome with busy voters.

---

## 2026 Predictions (98th Academy Awards, March 15)

| Rank | Film | Country | Ensemble Prob |
|------|------|---------|--------------|
| 1 | **Two People Exchanging Saliva** | France | **54%** |
| 2 | A Friend of Dorothy | UK | 24% |
| 3 | Jane Austen's Period Drama | USA | 9% |
| 4 | The Singers | USA | 8% |
| 5 | Butcher's Stain | Israel | 5% |

---

## How to extend this

### Add more years
Edit the `data` list in `oscar_shorts_predictor.py`. Each entry needs:
```python
{"year": YYYY, "film": "Title", "won": 1 or 0, "country": "...", ...}
```
Set `"won": None` for nominees in the current year (the prediction year).

### Add new features
Any publicly available signal can be added. Candidates not yet in the model:
- Vimeo Staff Pick (binary) — proxy for industry awareness
- Number of festival screenings (depth of circuit penetration)
- Country historical hit rate (wins / nominations per country)
- Topic embedding similarity to past winners (NLP on synopsis)

### Add the animated shorts category
The data structure is identical. Copy the dataset, replace with animated short nominees and winners, retrain. The same features should transfer reasonably well.

---

## Limitations

- **Small sample**: 95 rows is not a lot. The model is regularized accordingly but remains noisy.
- **Feature coding is subjective**: `festival_prestige_score` and `subject_gravity` involve judgment calls. Different coders may score differently.
- **Betting market circularity**: the market signal partially aggregates the same information the model uses. It's the strongest single feature but not independent.
- **Distribution shift**: Academy membership changes over time. Patterns from 2006 may weight differently with today's voters.

---

## Dependencies

```
pandas
numpy
scikit-learn
```

Install with:
```bash
pip install pandas numpy scikit-learn
```

Run with:
```bash
python oscar_shorts_predictor.py
```

---

*For research and entertainment. Not gambling advice.*
