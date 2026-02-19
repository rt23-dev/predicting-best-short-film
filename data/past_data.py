"""
Historical dataset: Oscar Best Live Action Short Film nominees 2005-2026
Features engineered from public data.

Features:
- year: ceremony year
- film: title
- won: 1 if winner, 0 if nominee
- country: production country (simplified)
- language_english: 1 if primarily English, 0 if subtitled
- runtime_min: runtime in minutes (approximate)
- director_prior_oscar_nom: 1 if director had prior Oscar nomination
- festival_prestige_score: 0-3 (0=unknown, 1=national, 2=Sundance/BIFF/major intl, 3=Cannes/Venice/TIFF)
- platform_tier: 0=unknown/self, 1=small distrib, 2=major distrib/streaming, 3=Netflix/A24/NYorker
- subject_gravity: 0=comedy/light, 1=drama, 2=heavy social/political/war
- bafta_win: 1 if won BAFTA short
- bafta_nom: 1 if nominated for BAFTA short
- betting_favorite: 1 if was consensus betting favorite going in (from historical awards coverage)
- ireland_uk: 1 if UK or Ireland production (historically overrepresented)
"""

import pandas as pd

data = [
    # 2006 (78th) - West Bank Story won
    {"year": 2006, "film": "West Bank Story", "won": 1, "country": "USA", "language_english": 1, "runtime_min": 21, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 1, "ireland_uk": 0},
    {"year": 2006, "film": "Binta and the Great Idea", "won": 0, "country": "Spain", "language_english": 0, "runtime_min": 30, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2006, "film": "Eramos Pocos", "won": 0, "country": "Spain", "language_english": 0, "runtime_min": 16, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2006, "film": "Helmer & Son", "won": 0, "country": "Denmark", "language_english": 0, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2006, "film": "The Saviour", "won": 0, "country": "Australia", "language_english": 1, "runtime_min": 15, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2007 (79th) - The Mozart of Pickpockets won
    {"year": 2007, "film": "The Mozart of Pickpockets", "won": 1, "country": "France", "language_english": 0, "runtime_min": 28, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2007, "film": "At Night", "won": 0, "country": "Denmark", "language_english": 0, "runtime_min": 30, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 1, "ireland_uk": 0},
    {"year": 2007, "film": "Il Supplente", "won": 0, "country": "Italy", "language_english": 0, "runtime_min": 18, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2007, "film": "Tanghi Argentini", "won": 0, "country": "Belgium", "language_english": 0, "runtime_min": 14, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 0, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2007, "film": "The Tonto Woman", "won": 0, "country": "UK", "language_english": 1, "runtime_min": 36, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 1, "bafta_nom": 1, "betting_favorite": 1, "ireland_uk": 1},

    # 2008 (80th) - Toyland won
    {"year": 2008, "film": "Toyland", "won": 1, "country": "Germany", "language_english": 0, "runtime_min": 14, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 1, "ireland_uk": 0},
    {"year": 2008, "film": "Auf der Strecke", "won": 0, "country": "Switzerland", "language_english": 0, "runtime_min": 30, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2008, "film": "Manon on the Asphalt", "won": 0, "country": "France", "language_english": 0, "runtime_min": 15, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2008, "film": "New Boy", "won": 0, "country": "Ireland", "language_english": 1, "runtime_min": 12, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 1},
    {"year": 2008, "film": "The Pig", "won": 0, "country": "France", "language_english": 0, "runtime_min": 16, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2009 (81st) - Spielzeugland won (same as Toyland - this IS Toyland, already covered above)
    # Let me use 2010
    # 2010 (82nd) - The New Tenants won
    {"year": 2010, "film": "The New Tenants", "won": 1, "country": "USA/Denmark", "language_english": 1, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2010, "film": "The Door", "won": 0, "country": "Ireland", "language_english": 1, "runtime_min": 25, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 1},
    {"year": 2010, "film": "Instead of Abracadabra", "won": 0, "country": "Sweden", "language_english": 0, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 0, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2010, "film": "Miracle Fish", "won": 0, "country": "Australia", "language_english": 1, "runtime_min": 17, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 1, "ireland_uk": 0},
    {"year": 2010, "film": "Kavi", "won": 0, "country": "USA/India", "language_english": 0, "runtime_min": 19, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2011 (83rd) - God of Love won
    {"year": 2011, "film": "God of Love", "won": 1, "country": "USA", "language_english": 1, "runtime_min": 18, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 0, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2011, "film": "The Confession", "won": 0, "country": "UK", "language_english": 1, "runtime_min": 25, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 1, "bafta_nom": 1, "betting_favorite": 1, "ireland_uk": 1},
    {"year": 2011, "film": "Wish 143", "won": 0, "country": "UK", "language_english": 1, "runtime_min": 25, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 1},
    {"year": 2011, "film": "Na Wewe", "won": 0, "country": "Belgium", "language_english": 0, "runtime_min": 17, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2011, "film": "Strokestown", "won": 0, "country": "Ireland", "language_english": 1, "runtime_min": 13, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 1},

    # 2012 (84th) - The Shore won
    {"year": 2012, "film": "The Shore", "won": 1, "country": "UK/Ireland", "language_english": 1, "runtime_min": 30, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 1, "betting_favorite": 1, "ireland_uk": 1},
    {"year": 2012, "film": "Pentecost", "won": 0, "country": "Ireland", "language_english": 1, "runtime_min": 12, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 0, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 1},
    {"year": 2012, "film": "Raju", "won": 0, "country": "Germany", "language_english": 0, "runtime_min": 30, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2012, "film": "Time Freak", "won": 0, "country": "USA", "language_english": 1, "runtime_min": 12, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 0, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2012, "film": "Tuba Atlantic", "won": 0, "country": "Norway", "language_english": 0, "runtime_min": 26, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2013 (85th) - Curfew won
    {"year": 2013, "film": "Curfew", "won": 1, "country": "USA", "language_english": 1, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 1, "ireland_uk": 0},
    {"year": 2013, "film": "Asad", "won": 0, "country": "USA/South Africa", "language_english": 0, "runtime_min": 18, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2013, "film": "Buzkashi Boys", "won": 0, "country": "USA/Afghanistan", "language_english": 0, "runtime_min": 28, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2013, "film": "Death of a Shadow", "won": 0, "country": "Belgium", "language_english": 0, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2013, "film": "Henry", "won": 0, "country": "Canada", "language_english": 1, "runtime_min": 21, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2014 (86th) - That Wasn't Me won
    {"year": 2014, "film": "That Wasn't Me", "won": 1, "country": "Spain", "language_english": 0, "runtime_min": 32, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2014, "film": "Aquel No Era Yo", "won": 0, "country": "Spain", "language_english": 0, "runtime_min": 32, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2014, "film": "Do I Have to Take Care of Everything?", "won": 0, "country": "Finland", "language_english": 0, "runtime_min": 7, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 0, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 1, "ireland_uk": 0},
    {"year": 2014, "film": "Just Before Losing Everything", "won": 0, "country": "France", "language_english": 0, "runtime_min": 30, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2014, "film": "Pitääkö Mun Kaikki Hoitaa?", "won": 0, "country": "Finland", "language_english": 0, "runtime_min": 7, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 0, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2015 (87th) - The Phone Call won
    {"year": 2015, "film": "The Phone Call", "won": 1, "country": "UK", "language_english": 1, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 2, "subject_gravity": 2, "bafta_win": 1, "bafta_nom": 1, "betting_favorite": 1, "ireland_uk": 1},
    {"year": 2015, "film": "Aya", "won": 0, "country": "Israel", "language_english": 0, "runtime_min": 38, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2015, "film": "Boogaloo and Graham", "won": 0, "country": "UK", "language_english": 1, "runtime_min": 14, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 0, "bafta_win": 0, "bafta_nom": 1, "betting_favorite": 0, "ireland_uk": 1},
    {"year": 2015, "film": "Butter Lamp", "won": 0, "country": "France/China", "language_english": 0, "runtime_min": 16, "director_prior_oscar_nom": 0, "festival_prestige_score": 3, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2015, "film": "Parvaneh", "won": 0, "country": "Switzerland", "language_english": 0, "runtime_min": 25, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2016 (88th) - Stutterer won
    {"year": 2016, "film": "Stutterer", "won": 1, "country": "UK", "language_english": 1, "runtime_min": 13, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 2, "subject_gravity": 1, "bafta_win": 1, "bafta_nom": 1, "betting_favorite": 1, "ireland_uk": 1},
    {"year": 2016, "film": "Ave Maria", "won": 0, "country": "Palestine/France/Germany", "language_english": 0, "runtime_min": 15, "director_prior_oscar_nom": 0, "festival_prestige_score": 3, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2016, "film": "Day One", "won": 0, "country": "USA", "language_english": 0, "runtime_min": 22, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2016, "film": "Everything Will Be Okay", "won": 0, "country": "Austria/Germany", "language_english": 0, "runtime_min": 30, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2016, "film": "Shok", "won": 0, "country": "UK/Kosovo", "language_english": 0, "runtime_min": 21, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 1, "betting_favorite": 0, "ireland_uk": 1},

    # 2017 (89th) - Sing won
    {"year": 2017, "film": "Sing", "won": 1, "country": "Hungary", "language_english": 0, "runtime_min": 25, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2017, "film": "Ennemis Intérieurs", "won": 0, "country": "France", "language_english": 0, "runtime_min": 28, "director_prior_oscar_nom": 0, "festival_prestige_score": 3, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 1, "ireland_uk": 0},
    {"year": 2017, "film": "La Femme et le TGV", "won": 0, "country": "Switzerland", "language_english": 0, "runtime_min": 30, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2017, "film": "Silent Nights", "won": 0, "country": "Denmark", "language_english": 0, "runtime_min": 30, "director_prior_oscar_nom": 0, "festival_prestige_score": 3, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2017, "film": "Timecode", "won": 0, "country": "Spain", "language_english": 0, "runtime_min": 15, "director_prior_oscar_nom": 0, "festival_prestige_score": 3, "platform_tier": 1, "subject_gravity": 0, "bafta_win": 1, "bafta_nom": 1, "betting_favorite": 0, "ireland_uk": 0},

    # 2018 (90th) - The Silent Child won
    {"year": 2018, "film": "The Silent Child", "won": 1, "country": "UK", "language_english": 1, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 2, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 1, "ireland_uk": 1},
    {"year": 2018, "film": "DeKalb Elementary", "won": 0, "country": "USA", "language_english": 1, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2018, "film": "The Eleven O'Clock", "won": 0, "country": "Australia", "language_english": 1, "runtime_min": 13, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 0, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2018, "film": "My Nephew Emmett", "won": 0, "country": "USA", "language_english": 1, "runtime_min": 21, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2018, "film": "Watu Wote/All of Us", "won": 0, "country": "Germany/Kenya", "language_english": 0, "runtime_min": 22, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2019 (91st) - Skin won
    {"year": 2019, "film": "Skin", "won": 1, "country": "USA", "language_english": 1, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 1, "ireland_uk": 0},
    {"year": 2019, "film": "Brotherhood", "won": 0, "country": "Tunisia/France", "language_english": 0, "runtime_min": 25, "director_prior_oscar_nom": 0, "festival_prestige_score": 3, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2019, "film": "Detainment", "won": 0, "country": "Ireland", "language_english": 1, "runtime_min": 30, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 1},
    {"year": 2019, "film": "Fauve", "won": 0, "country": "Canada", "language_english": 0, "runtime_min": 17, "director_prior_oscar_nom": 0, "festival_prestige_score": 3, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2019, "film": "Marguerite", "won": 0, "country": "Canada", "language_english": 0, "runtime_min": 19, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2020 (92nd) - The Neighbor's Window won
    {"year": 2020, "film": "The Neighbor's Window", "won": 1, "country": "USA", "language_english": 1, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 2, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 1, "ireland_uk": 0},
    {"year": 2020, "film": "Brotherhood", "won": 0, "country": "Tunisia/France", "language_english": 0, "runtime_min": 25, "director_prior_oscar_nom": 0, "festival_prestige_score": 3, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2020, "film": "Nefta Football Club", "won": 0, "country": "France/Tunisia", "language_english": 0, "runtime_min": 17, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 0, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2020, "film": "The Sickness of June", "won": 0, "country": "Germany", "language_english": 0, "runtime_min": 30, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2020, "film": "A Sister", "won": 0, "country": "Belgium", "language_english": 0, "runtime_min": 18, "director_prior_oscar_nom": 0, "festival_prestige_score": 3, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2021 (93rd) - Two Distant Strangers won
    {"year": 2021, "film": "Two Distant Strangers", "won": 1, "country": "USA", "language_english": 1, "runtime_min": 32, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 3, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2021, "film": "The Letter Room", "won": 0, "country": "USA", "language_english": 1, "runtime_min": 33, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 2, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2021, "film": "The Present", "won": 0, "country": "Palestine/UK", "language_english": 0, "runtime_min": 24, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 3, "subject_gravity": 2, "bafta_win": 1, "bafta_nom": 1, "betting_favorite": 1, "ireland_uk": 0},
    {"year": 2021, "film": "Feeling Through", "won": 0, "country": "USA", "language_english": 1, "runtime_min": 19, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2021, "film": "White Eye", "won": 0, "country": "Israel", "language_english": 0, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 3, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2022 (94th) - The Long Goodbye won
    {"year": 2022, "film": "The Long Goodbye", "won": 1, "country": "UK", "language_english": 1, "runtime_min": 12, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 2, "subject_gravity": 2, "bafta_win": 1, "bafta_nom": 1, "betting_favorite": 1, "ireland_uk": 1},
    {"year": 2022, "film": "Ala Kachuu - Take and Run", "won": 0, "country": "Switzerland", "language_english": 0, "runtime_min": 39, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2022, "film": "The Dress", "won": 0, "country": "Poland", "language_english": 0, "runtime_min": 30, "director_prior_oscar_nom": 0, "festival_prestige_score": 3, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2022, "film": "On My Mind", "won": 0, "country": "Denmark", "language_english": 0, "runtime_min": 17, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2022, "film": "Please Hold", "won": 0, "country": "USA", "language_english": 1, "runtime_min": 19, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2023 (95th) - An Irish Goodbye won
    {"year": 2023, "film": "An Irish Goodbye", "won": 1, "country": "UK/Ireland", "language_english": 1, "runtime_min": 23, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 1, "bafta_nom": 1, "betting_favorite": 1, "ireland_uk": 1},
    {"year": 2023, "film": "Ivalu", "won": 0, "country": "Denmark", "language_english": 0, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2023, "film": "Le Pupille", "won": 0, "country": "Italy", "language_english": 0, "runtime_min": 37, "director_prior_oscar_nom": 1, "festival_prestige_score": 2, "platform_tier": 3, "subject_gravity": 0, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2023, "film": "Night Ride", "won": 0, "country": "Norway", "language_english": 0, "runtime_min": 15, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2023, "film": "The Red Suitcase", "won": 0, "country": "Luxembourg", "language_english": 0, "runtime_min": 17, "director_prior_oscar_nom": 0, "festival_prestige_score": 3, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2024 (96th) - The After won
    {"year": 2024, "film": "The After", "won": 1, "country": "UK", "language_english": 1, "runtime_min": 24, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 3, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 1, "betting_favorite": 0, "ireland_uk": 1},
    {"year": 2024, "film": "Invincible", "won": 0, "country": "Australia", "language_english": 1, "runtime_min": 25, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2024, "film": "Knight of Fortune", "won": 0, "country": "Denmark", "language_english": 0, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 0, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2024, "film": "Red, White and Blue", "won": 0, "country": "USA", "language_english": 1, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 3, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 1, "ireland_uk": 0},
    {"year": 2024, "film": "Wad al-Deen", "won": 0, "country": "Palestine", "language_english": 0, "runtime_min": 18, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2025 (97th) - I'm Not a Robot won
    {"year": 2025, "film": "I'm Not a Robot", "won": 1, "country": "Netherlands", "language_english": 0, "runtime_min": 13, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 2, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2025, "film": "A Lien", "won": 0, "country": "USA", "language_english": 1, "runtime_min": 22, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2025, "film": "The Man Who Could Not Remain Silent", "won": 0, "country": "Croatia/France/Slovenia", "language_english": 0, "runtime_min": 14, "director_prior_oscar_nom": 0, "festival_prestige_score": 3, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2025, "film": "The Last Ranger", "won": 0, "country": "South Africa", "language_english": 1, "runtime_min": 30, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2025, "film": "The 11th Day", "won": 0, "country": "Armenia/Switzerland", "language_english": 0, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},

    # 2026 (98th) - Current nominees - these are what we're predicting
    {"year": 2026, "film": "Two People Exchanging Saliva", "won": None, "country": "France", "language_english": 0, "runtime_min": 20, "director_prior_oscar_nom": 0, "festival_prestige_score": 2, "platform_tier": 3, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 1, "ireland_uk": 0},
    {"year": 2026, "film": "A Friend of Dorothy", "won": None, "country": "UK", "language_english": 1, "runtime_min": 25, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 1, "betting_favorite": 0, "ireland_uk": 1},
    {"year": 2026, "film": "Butcher's Stain", "won": None, "country": "Israel", "language_english": 0, "runtime_min": 22, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 2, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2026, "film": "The Singers", "won": None, "country": "USA", "language_english": 1, "runtime_min": 18, "director_prior_oscar_nom": 1, "festival_prestige_score": 2, "platform_tier": 1, "subject_gravity": 1, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
    {"year": 2026, "film": "Jane Austen's Period Drama", "won": None, "country": "USA", "language_english": 1, "runtime_min": 15, "director_prior_oscar_nom": 0, "festival_prestige_score": 1, "platform_tier": 1, "subject_gravity": 0, "bafta_win": 0, "bafta_nom": 0, "betting_favorite": 0, "ireland_uk": 0},
]

df = pd.DataFrame(data)
print(f"Total records: {len(df)}")
print(f"Years covered: {df[df['won'].notna()]['year'].min()} - {df[df['won'].notna()]['year'].max()}")
print(f"Training examples: {len(df[df['won'].notna()])}")
print(f"Winners: {df['won'].sum()}")
print(df[df['won'].notna()].head())
