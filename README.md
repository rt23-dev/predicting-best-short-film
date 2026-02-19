# Predict the best short film

### The Core Problem

Short films are the hardest category to predict. They lack the institutional precursor infrastructure (guilds, major betting markets, wide critic coverage) that makes traditional mathematical models for oscar predictions work. I want to find unconventional, previously unexplored signals that could potetially help me make a lot of money.

### Features

To begin with, we need a list of features. 
1. Festival graph features (# festivals, prestige score, trajectory)
2. Director prior nomination (binary)
3. Director film school tier (categorical)
4. Country historical hit rate
5. Language (English vs. subtitled)
6. Runtime
7. Distributor/platform tier
8. Vimeo Staff Pick / New Yorker (binary)
9. Subject matter embedding similarity to past winners

The most unique thing here, in my opinion, is the festival graph. That is, what festivals has the short film gone through before reaching the Oscars? What historical paths have been successful and which ones have not?
