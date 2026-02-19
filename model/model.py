"""
Oscar Best Live Action Short Film Prediction Model
====================================================
A novel statistical/ML approach for predicting short film winners
using features unavailable in existing models (Zauzmer etc.)

Features:
- Festival prestige trajectory
- Platform/distributor tier
- Subject gravity
- BAFTA correlation
- Betting market signal
- Director career features
- Language/country patterns
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneGroupOut, cross_val_predict
from sklearn.metrics import accuracy_score, brier_score_loss
from sklearn.calibration import CalibratedClassifierCV
import warnings
warnings.filterwarnings('ignore')

# ──────────────────────────────────────────────────────────────
# 1. LOAD DATA
# ──────────────────────────────────────────────────────────────
exec(open('/home/claude/oscar_shorts_data.py').read())

df_train = df[df['won'].notna()].copy()
df_2026  = df[df['year'] == 2026].copy()

print("=" * 60)
print("OSCAR BEST LIVE ACTION SHORT FILM PREDICTION MODEL")
print("=" * 60)
print(f"Training data: {len(df_train)} nominees across {df_train['year'].nunique()} years")
print()

# ──────────────────────────────────────────────────────────────
# 2. FEATURE ENGINEERING
# ──────────────────────────────────────────────────────────────

FEATURES = [
    'language_english',
    'runtime_min',
    'director_prior_oscar_nom',
    'festival_prestige_score',
    'platform_tier',
    'subject_gravity',
    'bafta_win',
    'bafta_nom',
    'betting_favorite',
    'ireland_uk',
    'runtime_bucket',
    'platform_x_festival',   # interaction
    'bafta_x_english',       # interaction
]

def add_features(df):
    df = df.copy()
    # Runtime bucket: 1-15min = sweet_spot_short (1), 16-25 = sweet_spot_medium (2), 26+ = long (0)
    df['runtime_bucket'] = df['runtime_min'].apply(
        lambda r: 2 if 16 <= r <= 25 else (1 if r <= 15 else 0)
    )
    # Interaction: high platform tier + high festival = strong signal
    df['platform_x_festival'] = df['platform_tier'] * df['festival_prestige_score']
    # BAFTA win/nom AND english language
    df['bafta_x_english'] = df['bafta_nom'] * df['language_english']
    return df

df_train = add_features(df_train)
df_2026  = add_features(df_2026)

X = df_train[FEATURES].values
y = df_train['won'].values.astype(int)
groups = df_train['year'].values

X_pred = df_2026[FEATURES].values

# ──────────────────────────────────────────────────────────────
# 3. MODEL: Leave-One-Year-Out Cross-Validation
# ──────────────────────────────────────────────────────────────
# This is the right validation strategy: train on all years except
# one, predict that year. Simulates real-world forecasting.

logo = LeaveOneGroupOut()

# Logistic Regression (main model - interpretable)
lr = LogisticRegression(C=0.5, max_iter=1000, random_state=42)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Cross-val predictions
cv_proba_lr = cross_val_predict(lr, X_scaled, y, cv=logo, groups=groups, method='predict_proba')[:,1]

# Random Forest (ensemble model)
rf = RandomForestClassifier(n_estimators=200, max_depth=3, random_state=42, min_samples_leaf=3)
cv_proba_rf = cross_val_predict(rf, X, y, cv=logo, groups=groups, method='predict_proba')[:,1]

# Convert raw probabilities to normalized per-year probabilities (sum to 1)
def normalize_probs_by_year(df_in, raw_probs):
    probs = raw_probs.copy()
    for year in df_in['year'].unique():
        mask = df_in['year'].values == year
        year_sum = probs[mask].sum()
        if year_sum > 0:
            probs[mask] = probs[mask] / year_sum
    return probs

proba_lr_norm = normalize_probs_by_year(df_train, cv_proba_lr)
proba_rf_norm = normalize_probs_by_year(df_train, cv_proba_rf)

# ──────────────────────────────────────────────────────────────
# 4. EVALUATE HISTORICAL PERFORMANCE
# ──────────────────────────────────────────────────────────────

def evaluate_model(df_in, probs, model_name):
    df_eval = df_in.copy()
    df_eval['prob'] = probs
    
    # For each year, did the model pick the winner?
    correct = 0
    total_years = 0
    brier_scores = []
    
    for year, grp in df_eval.groupby('year'):
        predicted_winner = grp.loc[grp['prob'].idxmax(), 'film']
        actual_winner = grp.loc[grp['won'] == 1, 'film'].values[0] if grp['won'].sum() > 0 else None
        if actual_winner:
            correct += (predicted_winner == actual_winner)
            total_years += 1
            # Brier score for this year
            for _, row in grp.iterrows():
                brier_scores.append((row['won'] - row['prob'])**2)
    
    accuracy = correct / total_years
    brier = np.mean(brier_scores)
    print(f"\n{model_name}")
    print(f"  Pick accuracy (LOYO CV):  {correct}/{total_years} = {accuracy:.1%}")
    print(f"  Brier score (lower=better): {brier:.4f}  (baseline random: ~0.16)")
    return accuracy

acc_lr = evaluate_model(df_train, proba_lr_norm, "Logistic Regression (L2)")
acc_rf = evaluate_model(df_train, proba_rf_norm, "Random Forest")

# Ensemble
proba_ens_norm = (proba_lr_norm + proba_rf_norm) / 2
proba_ens_norm = normalize_probs_by_year(df_train, proba_ens_norm)
acc_ens = evaluate_model(df_train, proba_ens_norm, "Ensemble (LR + RF)")

# ──────────────────────────────────────────────────────────────
# 5. FEATURE IMPORTANCE
# ──────────────────────────────────────────────────────────────

lr.fit(X_scaled, y)
rf.fit(X, y)

print("\n" + "=" * 60)
print("FEATURE IMPORTANCE")
print("=" * 60)

print("\nLogistic Regression Coefficients:")
coefs = sorted(zip(FEATURES, lr.coef_[0]), key=lambda x: abs(x[1]), reverse=True)
for feat, coef in coefs:
    direction = "↑ increases" if coef > 0 else "↓ decreases"
    print(f"  {feat:30s} {coef:+.3f}  {direction} win probability")

print("\nRandom Forest Feature Importances:")
importances = sorted(zip(FEATURES, rf.feature_importances_), key=lambda x: x[1], reverse=True)
for feat, imp in importances:
    bar = "█" * int(imp * 50)
    print(f"  {feat:30s} {imp:.3f}  {bar}")

# ──────────────────────────────────────────────────────────────
# 6. PREDICT 2026
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("2026 PREDICTIONS (98th Academy Awards)")
print("=" * 60)

X_pred_scaled = scaler.transform(X_pred)

pred_lr   = lr.predict_proba(X_pred_scaled)[:,1]
pred_rf   = rf.predict_proba(X_pred)[:,1]
pred_ens  = (pred_lr + pred_rf) / 2

# Normalize
def norm(probs):
    return probs / probs.sum()

pred_lr_n  = norm(pred_lr)
pred_rf_n  = norm(pred_rf)
pred_ens_n = norm(pred_ens)

results_2026 = df_2026[['film', 'country', 'language_english', 'festival_prestige_score',
                          'platform_tier', 'subject_gravity', 'bafta_nom', 'betting_favorite', 'ireland_uk']].copy()
results_2026['prob_lr']  = pred_lr_n
results_2026['prob_rf']  = pred_rf_n
results_2026['prob_ens'] = pred_ens_n
results_2026 = results_2026.sort_values('prob_ens', ascending=False).reset_index(drop=True)
results_2026['rank'] = results_2026.index + 1

print()
for _, row in results_2026.iterrows():
    bar = "█" * int(row['prob_ens'] * 40)
    flag = "🏆 PREDICTED WINNER" if row['rank'] == 1 else ""
    print(f"  {row['rank']}. {row['film']}")
    print(f"     Model prob: {row['prob_ens']:.1%}  [{bar}]  {flag}")
    print(f"     LR: {row['prob_lr']:.1%}  |  RF: {row['prob_rf']:.1%}")
    print()

# ──────────────────────────────────────────────────────────────
# 7. HISTORICAL PATTERN ANALYSIS (the novel stuff)
# ──────────────────────────────────────────────────────────────

print("=" * 60)
print("HISTORICAL PATTERN ANALYSIS")
print("=" * 60)

winners = df_train[df_train['won'] == 1]
losers  = df_train[df_train['won'] == 0]

print(f"\nAmong {len(winners)} historical winners:")
print(f"  English language:      {winners['language_english'].mean():.0%}")
print(f"  Ireland/UK production: {winners['ireland_uk'].mean():.0%}")
print(f"  Avg festival score:    {winners['festival_prestige_score'].mean():.2f}")
print(f"  Avg platform tier:     {winners['platform_tier'].mean():.2f}")
print(f"  Heavy subject matter:  {(winners['subject_gravity'] == 2).mean():.0%}")
print(f"  BAFTA nominated:       {winners['bafta_nom'].mean():.0%}")
print(f"  BAFTA won:             {winners['bafta_win'].mean():.0%}")
print(f"  Was betting favorite:  {winners['betting_favorite'].mean():.0%}")
print(f"  Avg runtime:           {winners['runtime_min'].mean():.1f} min")

print(f"\nAmong {len(losers)} historical nominees (non-winners):")
print(f"  English language:      {losers['language_english'].mean():.0%}")
print(f"  Ireland/UK production: {losers['ireland_uk'].mean():.0%}")
print(f"  Avg festival score:    {losers['festival_prestige_score'].mean():.2f}")
print(f"  Avg platform tier:     {losers['platform_tier'].mean():.2f}")
print(f"  Heavy subject matter:  {(losers['subject_gravity'] == 2).mean():.0%}")
print(f"  BAFTA nominated:       {losers['bafta_nom'].mean():.0%}")
print(f"  BAFTA won:             {losers['bafta_win'].mean():.0%}")
print(f"  Was betting favorite:  {losers['betting_favorite'].mean():.0%}")
print(f"  Avg runtime:           {losers['runtime_min'].mean():.1f} min")

print(f"\nKey differentiators (winner rate among feature=1 vs baseline 20%):")
for feat in ['language_english', 'ireland_uk', 'bafta_win', 'bafta_nom', 'betting_favorite', 'director_prior_oscar_nom']:
    has = df_train[df_train[feat] == 1]
    if len(has) > 0:
        rate = has['won'].mean()
        n = len(has)
        print(f"  {feat:35s}: {rate:.0%} win rate (n={n})")

# Country analysis
print("\nWin rates by country/region:")
df_train['region'] = df_train.apply(lambda r: 
    'UK/Ireland' if r['ireland_uk'] == 1 
    else ('USA' if r['country'] == 'USA' 
    else ('France' if 'France' in str(r['country']) 
    else 'Other')), axis=1)
for region, grp in df_train.groupby('region'):
    rate = grp['won'].mean()
    n = len(grp)
    nominees = n // 5  # approx years nominated  
    print(f"  {region:15s}: {rate:.0%} win rate ({grp['won'].sum():.0f} wins / {n} nominations)")
