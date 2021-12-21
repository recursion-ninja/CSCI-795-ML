# Hunter College CSCI-795 Project

# Introduction to Machine Learning

### Authors:

 - Alex Washburn (@recursion-ninja)

 - "John"  (@johnl11235)

---


## Abstract

In this project, we explore an under-developed aspect of Dungeons and Dragons 5th Edition (D&D), the monster "Challenge Rating" system.
The Challenge Rating (CR) is a measure of a monster's lethality against a party of *four* characters, each that a character level equal to the monster's CR.
Unfortunately, the supplied CR values that have been published are more often than not poor estimates of monster lethality.
In this project, we attempt to produce an substitute ranking of monster lethality, ordering them into tiers of either `[1, 5]`, `[1, 10]`, or `[1, 20]`.
We hypothesize that the application of machine learning will produce a better intdicator of monster lethality than the supplied CR score.


## The D&D Monster Data

We take the stat-block of each monster from the [`5e.tools`][5e-mirror] database and match the monster with the [Elo Ranking][elo-wiki] from [`dndcombat.com`][compendium].
Elo Ranks scores on [`dndcombat.com`][compendium] are continually updated.
The Elo observations were taken on `2021-12-08`.

The raw data used for this project has been stored within the repository for reference:

  - [`data/5e.tools/*`     ][repo-5e-tools  ]
  - [`data/dndcombat.com/*`][repo-dnd-combat]

Both the data from [`5e.tools`][5e-mirror] and [`dndcombat.com`][compendium] were retrieved in [JSON format][json].
The data was parsed and curated using a custom tool written by the authors.
The tool is named `curate-json` and is written in [Haskell][haskell].
In order to build the `curate-json` tool, the [Haskell][haskell] compiler [GHC][ghc-dl] and build tool [`cabal`][cabal-dl] are required.

The source code for the `curate-json` tool has been stored within the repository for reference:

  - [`curation/*`][repo-curation]

Additionally, there is a [`curate-dataset.sh`][repo-script] script in the root of the repository which, assuming both [GHC][ghc-dl] and [`cabal`][cabal-dl] are installed, will replicate the data curation used for this project.
The `curate-dataset.sh` script will place the curated dataset in the `data` directory.

The curated data used for this project has been stored within the repository for reference:

  - [`data/dnd-5e-monsters.csv`][repo-dataset]

[5e-mirror ]: https://5etools-mirror-1.github.io/
[elo-wiki  ]: https://en.wikipedia.org/wiki/Elo_rating_system
[compendium]: https://www.dndcombat.com/dndcombat/Welcome.do?page=Compendium
[json      ]: https://en.wikipedia.org/wiki/JSON
[haskell   ]: https://www.haskell.org/
[ghc-dl    ]: https://www.haskell.org/ghc/download.html
[cabal-dl  ]: https://www.haskell.org/cabal/download.html

[repo-5e-tools  ]: https://github.com/recursion-ninja/CSCI-795-ML/tree/main/data/5e.tools
[repo-dnd-combat]: https://github.com/recursion-ninja/CSCI-795-ML/tree/main/data/dndcombat.com
[repo-curation  ]: https://github.com/recursion-ninja/CSCI-795-ML/tree/main/curation
[repo-script    ]: https://github.com/recursion-ninja/CSCI-795-ML/blob/main/curate-dataset.sh
[repo-dataset   ]: https://github.com/recursion-ninja/CSCI-795-ML/blob/main/data/dnd-5e-monsters.csv


## Feature Extraction & Selection

The curated [`dnd-5e-monsters.csv`][repo-dataset] dataset has `1386` rows and `72` columns, constituting the project's initial observations and measurements, respectively.
There are two leading textual columns, labeled `'Name'` and `'Type'` indexed `[0, 1]`.
The subsequent `20` columns indexed `[2, 21]` are "continuous," integral-valued measurements of common D&D attributes.
The final `'Elo Rank'` column indexed `71` is the label for supervised machine learning models.
The next three trailing columns, labeled `Damage Tags`, `Spellcasting Tags` and `Trait Tags` indexed `[66, 70]`
The remaining columns indexed `[22, 67]` are binary indicators for various monster attributes.
A column summary of the initial data set is presented below.

### Initial Dataset

|  # | Column Label       | Data Type |
|---:|:-------------------|:----------|
|  0 | Name               | Textual   |
|  1 | Type               | Textual   |
|  2 | Size               | Integral  |
|  3 | Armor              | Integral  | 
|  4 | Hit Points         | Integral  | 
|  5 | Move Burrow        | Integral  | 
|  6 | Move Climb         | Integral  | 
|  7 | Move Fly           | Integral  | 
|  8 | Move Swim          | Integral  | 
|  9 | Move Walk          | Integral  | 
| 10 | Stat Str           | Integral  | 
| 11 | Stat Dex           | Integral  | 
| 12 | Stat Con           | Integral  | 
| 13 | Stat Int           | Integral  | 
| 14 | Stat Wis           | Integral  | 
| 15 | Stat Cha           | Integral  | 
| 16 | Save Str           | Integral  | 
| 17 | Save Dex           | Integral  | 
| 18 | Save Con           | Integral  | 
| 19 | Save Int           | Integral  | 
| 20 | Save Wis           | Integral  | 
| 21 | Save Cha           | Integral  | 
| 22 | Blind Sight        | Binary    | 
| 23 | Dark Vision        | Binary    | 
| 24 | Tremorsense        | Binary    | 
| 25 | True Sight         | Binary    | 
| 26 | Immune Acid        | Binary    | 
| 27 | Immune Bludgeoning | Binary    | 
| 28 | Immune Cold        | Binary    | 
| 29 | Immune Fire        | Binary    | 
| 30 | Immune Force       | Binary    | 
| 31 | Immune Lightning   | Binary    | 
| 32 | Immune Necrotic    | Binary    | 
| 33 | Immune Piercing    | Binary    | 
| 34 | Immune Poison      | Binary    | 
| 35 | Immune Psychic     | Binary    | 
| 36 | Immune Radiant     | Binary    | 
| 37 | Immune Slashing    | Binary    | 
| 38 | Immune Thunder     | Binary    | 
| 39 | Resist Acid        | Binary    | 
| 40 | Resist Bludgeoning | Binary    | 
| 41 | Resist Cold        | Binary    | 
| 42 | Resist Fire        | Binary    | 
| 43 | Resist Force       | Binary    | 
| 44 | Resist Lightning   | Binary    | 
| 45 | Resist Necrotic    | Binary    | 
| 46 | Resist Piercing    | Binary    | 
| 47 | Resist Poison      | Binary    | 
| 48 | Resist Psychic     | Binary    | 
| 49 | Resist Radiant     | Binary    | 
| 50 | Resist Slashing    | Binary    | 
| 51 | Resist Thunder     | Binary    | 
| 52 | Cause Blinded      | Binary    | 
| 53 | Cause Charmed      | Binary    | 
| 54 | Cause Deafened     | Binary    | 
| 55 | Cause Frightened   | Binary    | 
| 56 | Cause Grappled     | Binary    | 
| 57 | Cause Incapacitated| Binary    | 
| 58 | Cause Invisible    | Binary    | 
| 59 | Cause Paralyzed    | Binary    | 
| 60 | Cause Petrified    | Binary    | 
| 61 | Cause Poisoned     | Binary    | 
| 62 | Cause Prone        | Binary    | 
| 63 | Cause Restrained   | Binary    | 
| 64 | Cause Stunned      | Binary    | 
| 65 | Cause Unconscious  | Binary    | 
| 66 | Multiattack        | Binary    | 
| 67 | Spellcasting       | Binary    | 
| 68 | Damage Tags        | Textual   |
| 69 | Spellcasting Tags  | Textual   |
| 70 | Trait Tags         | Textual   |
| 71 | Elo Rank           | Integral  |

For our analysis, we desire the `'Elo Rank'` to be represented as an integral "tier list."
We extract the tier list feature by discretizing the the 'Elo Rank' column via following procedure:

  1. Normalize the data into normally distributed quantiles via the `QuantileTransformer`.

  2. Decide on the number of tiers: `[1, 5]`, `[1, 10]`, or `[1, 20]`.

  3. Scale the data to fit the tier range.

  4. Remove outliers.

  5. Round values to nearest integer value.

> **Note:** The removal of outliers will shink the dataset as follows:

| Tier List | Observations |
|----------:|:------------:|
| `[1,  5]` |    `1200`    |
| `[1, 10]` |    `1316`    |
| `[1, 20]` |    `1348`    |

The final feature extraction involves the last three columns, labeled `Damage Tags`, `Spellcasting Tags` and `Trait Tags` indexed `[63, 65]`.
Each can be expanded to extract an additional features, totaling `63` features combined.
This feature extraction nearly doubles the fully expanded dataset size, now totaling to `135` features.

### Fully Extracted Dataset

|  #  | Column Label             | Data Type |
|----:|:-------------------------|:----------|
|   0 | Name                     | Textual   |
|   1 | Type                     | Textual   |
|   2 | Size                     | Integral  |
|   3 | Armor                    | Integral  |
|   4 | Hit Points               | Integral  |
|   5 | Move Burrow              | Integral  |
|   6 | Move Climb               | Integral  |
|   7 | Move Fly                 | Integral  |
|   8 | Move Swim                | Integral  |
|   9 | Move Walk                | Integral  |
|  10 | Stat Str                 | Integral  |
|  11 | Stat Dex                 | Integral  |
|  12 | Stat Con                 | Integral  |
|  13 | Stat Int                 | Integral  |
|  14 | Stat Wis                 | Integral  |
|  15 | Stat Cha                 | Integral  |
|  16 | Save Str                 | Integral  |
|  17 | Save Dex                 | Integral  |
|  18 | Save Con                 | Integral  |
|  19 | Save Int                 | Integral  |
|  20 | Save Wis                 | Integral  |
|  21 | Save Cha                 | Integral  |
|  22 | Blind Sight              | Binary    |
|  23 | Dark Vision              | Binary    |
|  24 | Tremorsense              | Binary    |
|  25 | True Sight               | Binary    |
|  26 | Immune Acid              | Binary    |
|  27 | Immune Bludgeoning       | Binary    |
|  28 | Immune Cold              | Binary    |
|  29 | Immune Fire              | Binary    |
|  30 | Immune Force             | Binary    |
|  31 | Immune Lightning         | Binary    |
|  32 | Immune Necrotic          | Binary    |
|  33 | Immune Piercing          | Binary    |
|  34 | Immune Poison            | Binary    |
|  35 | Immune Psychic           | Binary    |
|  36 | Immune Radiant           | Binary    |
|  37 | Immune Slashing          | Binary    |
|  38 | Immune Thunder           | Binary    |
|  39 | Resist Acid              | Binary    |
|  40 | Resist Bludgeoning       | Binary    |
|  41 | Resist Cold              | Binary    |
|  42 | Resist Fire              | Binary    |
|  43 | Resist Force             | Binary    |
|  44 | Resist Lightning         | Binary    |
|  45 | Resist Necrotic          | Binary    |
|  46 | Resist Piercing          | Binary    |
|  47 | Resist Poison            | Binary    |
|  48 | Resist Psychic           | Binary    |
|  49 | Resist Radiant           | Binary    |
|  50 | Resist Slashing          | Binary    |
|  51 | Resist Thunder           | Binary    |
|  52 | Cause Blinded            | Binary    |
|  53 | Cause Charmed            | Binary    |
|  54 | Cause Deafened           | Binary    |
|  55 | Cause Frightened         | Binary    |
|  56 | Cause Grappled           | Binary    |
|  57 | Cause Incapacitated      | Binary    |
|  58 | Cause Invisible          | Binary    |
|  59 | Cause Paralyzed          | Binary    |
|  60 | Cause Petrified          | Binary    |
|  61 | Cause Poisoned           | Binary    |
|  62 | Cause Prone              | Binary    |
|  63 | Cause Restrained         | Binary    |
|  64 | Cause Stunned            | Binary    |
|  65 | Cause Unconscious        | Binary    |
|  66 | Multiattack              | Binary    |
|  67 | Spellcasting             | Binary    |
|  68 | Damage_A                 | Binary    |
|  69 | Damage_B                 | Binary    |
|  70 | Damage_C                 | Binary    |
|  71 | Damage_F                 | Binary    |
|  72 | Damage_I                 | Binary    |
|  73 | Damage_L                 | Binary    |
|  74 | Damage_N                 | Binary    |
|  75 | Damage_O                 | Binary    |
|  76 | Damage_P                 | Binary    |
|  77 | Damage_R                 | Binary    |
|  78 | Damage_S                 | Binary    |
|  79 | Damage_T                 | Binary    |
|  80 | Damage_Y                 | Binary    |
|  81 | Spellcasting_CA          | Binary    |
|  82 | Spellcasting_CB          | Binary    |
|  83 | Spellcasting_CC          | Binary    |
|  84 | Spellcasting_CD          | Binary    |
|  85 | Spellcasting_CL          | Binary    |
|  86 | Spellcasting_CP          | Binary    |
|  87 | Spellcasting_CR          | Binary    |
|  88 | Spellcasting_CS          | Binary    |
|  89 | Spellcasting_CW          | Binary    |
|  90 | Spellcasting_F           | Binary    |
|  91 | Spellcasting_I           | Binary    |
|  92 | Spellcasting_P           | Binary    |
|  93 | Spellcasting_S           | Binary    |
|  94 | Aggressive               | Binary    |
|  95 | Ambusher                 | Binary    |
|  96 | Amorphous                | Binary    |
|  97 | Amphibious               | Binary    |
|  98 | Antimagic Susceptibility | Binary    |
|  99 | Brute                    | Binary    |
| 100 | Charge                   | Binary    |
| 101 | Damage Absorption        | Binary    |
| 102 | Death Burst              | Binary    |
| 103 | Devil's Sight            | Binary    |
| 104 | False Appearance         | Binary    |
| 105 | Fey Ancestry             | Binary    |
| 106 | Flyby                    | Binary    |
| 107 | Hold Breath              | Binary    |
| 108 | Illumination             | Binary    |
| 109 | Immutable Form           | Binary    |
| 110 | Incorporeal Movement     | Binary    |
| 111 | Keen Senses              | Binary    |
| 112 | Legendary Resistances    | Binary    |
| 113 | Light Sensitivity        | Binary    |
| 114 | Magic Resistance         | Binary    |
| 115 | Magic Weapons            | Binary    |
| 116 | Pack Tactics             | Binary    |
| 117 | Pounce                   | Binary    |
| 118 | Rampage                  | Binary    |
| 119 | Reckless                 | Binary    |
| 120 | Regeneration             | Binary    |
| 121 | Rejuvenation             | Binary    |
| 122 | Shapechanger             | Binary    |
| 123 | Siege Monster            | Binary    |
| 124 | Sneak Attack             | Binary    |
| 125 | Spell Immunity           | Binary    |
| 126 | Spider Climb             | Binary    |
| 127 | Sunlight Sensitivity     | Binary    |
| 128 | Turn Immunity            | Binary    |
| 129 | Turn Resistance          | Binary    |
| 130 | Undead Fortitude         | Binary    |
| 131 | Water Breathing          | Binary    |
| 132 | Web Sense                | Binary    |
| 133 | Web Walker               | Binary    |
| 134 | Elo Rank                 | Integral  |

> After extracting all possible features we perform feature selection.


First, the textual columns, labeled `'Name'` and `'Type'` indexed `[0, 1]` are dropped from our analysis.
These columns do not influence combat efficacy and are not convertible to a meanininful numeric representation.
Their absence makes the machine learning process much smoother.

Second, we drop all features extracted from the 'Damage Tag' and 'Spell Tag' columns.
These extracted features had essentially no bearing on our first explored model (Multinomial Naive Bayes), and hence we decided to omit them from all future models for efficiency reasons.

For the final component of our feature selection process, we perform a "decorrelation" pass through the feature set.
If any pair of features have a correlation coefficient of `0.6` or higher, we drop one of the columns and use the other as a proxy.
Consequently, we dropped the following features:

|      Proxy        |   Dropped Feature    |
|:------------------|:---------------------|
| Hit Points        | Size                 |
| Hit Points        | Stat Str             |
| Hit Points        | Stat Con             |
| Stat Cha          | Stat Int             |
| Resist Fire       | Resist Cold          |
| Resist Fire       | Resist Lightning     |
| Resist Acid       | Resist Thunder       |
| Resist Acid       | Incorporeal Movement |
| Damage Absorption | Immutable Form       |
| Spell Immunity    | Immune Force         |
| Web Sense         | Web Walker           |

> After feature extraction *and* feature selection, our dataset was comprised of `96` features.

### Final Dataset

|  #  | Column Label             | Data Type |
|----:|:-------------------------|:----------|
|   0 | Armor                    | Integral  |
|   1 | Hit Points               | Integral  |
|   2 | Move Burrow              | Integral  |
|   3 | Move Climb               | Integral  |
|   4 | Move Fly                 | Integral  |
|   5 | Move Swim                | Integral  |
|   6 | Move Walk                | Integral  |
|   7 | Stat Dex                 | Integral  |
|   8 | Stat Wis                 | Integral  |
|   9 | Stat Cha                 | Integral  |
|  10 | Save Str                 | Integral  |
|  11 | Save Dex                 | Integral  |
|  12 | Save Con                 | Integral  |
|  13 | Save Int                 | Integral  |
|  14 | Save Wis                 | Integral  |
|  15 | Save Cha                 | Integral  |
|  16 | Blind Sight              | Binary    |
|  17 | Dark Vision              | Binary    |
|  18 | Tremorsense              | Binary    |
|  19 | True Sight               | Binary    |
|  20 | Immune Acid              | Binary    |
|  21 | Immune Bludgeoning       | Binary    |
|  22 | Immune Cold              | Binary    |
|  23 | Immune Fire              | Binary    |
|  24 | Immune Lightning         | Binary    |
|  25 | Immune Necrotic          | Binary    |
|  26 | Immune Piercing          | Binary    |
|  27 | Immune Poison            | Binary    |
|  28 | Immune Psychic           | Binary    |
|  29 | Immune Radiant           | Binary    |
|  30 | Immune Slashing          | Binary    |
|  31 | Immune Thunder           | Binary    |
|  32 | Resist Bludgeoning       | Binary    |
|  33 | Resist Cold              | Binary    |
|  34 | Resist Force             | Binary    |
|  35 | Resist Necrotic          | Binary    |
|  36 | Resist Piercing          | Binary    |
|  37 | Resist Poison            | Binary    |
|  38 | Resist Psychic           | Binary    |
|  39 | Resist Radiant           | Binary    |
|  40 | Resist Slashing          | Binary    |
|  41 | Cause Blinded            | Binary    |
|  42 | Cause Charmed            | Binary    |
|  43 | Cause Deafened           | Binary    |
|  44 | Cause Frightened         | Binary    |
|  45 | Cause Grappled           | Binary    |
|  46 | Cause Incapacitated      | Binary    |
|  47 | Cause Invisible          | Binary    |
|  48 | Cause Paralyzed          | Binary    |
|  49 | Cause Petrified          | Binary    |
|  50 | Cause Poisoned           | Binary    |
|  51 | Cause Prone              | Binary    |
|  52 | Cause Restrained         | Binary    |
|  53 | Cause Stunned            | Binary    |
|  54 | Cause Unconscious        | Binary    |
|  55 | Multiattack              | Binary    |
|  56 | Spellcasting             | Binary    |
|  57 | Aggressive               | Binary    |
|  58 | Ambusher                 | Binary    |
|  59 | Amorphous                | Binary    |
|  60 | Amphibious               | Binary    |
|  61 | Antimagic Susceptibility | Binary    |
|  62 | Brute                    | Binary    |
|  63 | Charge                   | Binary    |
|  64 | Death Burst              | Binary    |
|  65 | Devil's Sight            | Binary    |
|  66 | False Appearance         | Binary    |
|  67 | Fey Ancestry             | Binary    |
|  68 | Flyby                    | Binary    |
|  69 | Hold Breath              | Binary    |
|  70 | Illumination             | Binary    |
|  71 | Immutable Form           | Binary    |
|  72 | Incorporeal Movement     | Binary    |
|  73 | Keen Senses              | Binary    |
|  74 | Legendary Resistances    | Binary    |
|  75 | Light Sensitivity        | Binary    |
|  76 | Magic Resistance         | Binary    |
|  77 | Magic Weapons            | Binary    |
|  78 | Pack Tactics             | Binary    |
|  79 | Pounce                   | Binary    |
|  80 | Rampage                  | Binary    |
|  81 | Reckless                 | Binary    |
|  82 | Regeneration             | Binary    |
|  83 | Rejuvenation             | Binary    |
|  84 | Shapechanger             | Binary    |
|  85 | Siege Monster            | Binary    |
|  86 | Sneak Attack             | Binary    |
|  87 | Spell Immunity           | Binary    |
|  88 | Spider Climb             | Binary    |
|  89 | Sunlight Sensitivity     | Binary    |
|  90 | Turn Immunity            | Binary    |
|  91 | Turn Resistance          | Binary    |
|  92 | Undead Fortitude         | Binary    |
|  93 | Water Breathing          | Binary    |
|  94 | Web Walker               | Binary    |
|  95 | Elo Rank                 | Integral  |


## Datset partitioning

We take the prepared dataset and train multiple machine learning classifiers.
We use 80% of the randomly permuted data as the training set and the remaining 20% as the test set.
This partition data was stratified by the `'Elo Rank'` column to ensure that each tier is represented.
Furthermore, we partition the training set again, using 80% as a learning set and the remaining 20% as the validation set.
Model selection was performed on the training set; comprised of the "learning" and validation subsets.

> The dataset was paritioned according to the following distribution, stratified by `'Elo Rank'`:

|   Set    | Ratio |
|:--------:|------:|
| Test     |  20%  |
| Train    |  80%  |
| Learn    |  64%  |
| Validate |  16%  |


## Model Specification

  1.  **Decision Tree**
      Decision trees make extremely fast classifiers once constructed, but can be increadibly time consuming to build.
      We decided to try our luck with this model and see if an effective classifier could be built within a reasonable timeframe.

  2.  **K Nearest Neighbors**
      A very simple model with a theoretical bound on it's maximum inaccuracy.
      Because of our familiartiy with this model from the extensive discussion in class and it's prominent presence in our first homework, we chose this as our initial classifier to get our bearing and some quick benchmarking numbers.

  3.  **Logistic Regression**
      We read that the a logistic regression can be an effective and efficient model for multi-class output, which our tier list is.
      This model was included because we suspected that the features had some linear, but not polynomial, relationship(s).
      The logistic regression ought to capture and train well if linear relationships exists between the features and the tier list labels.

  4.  **Multinomial Naive Bayes**
      Independent features are am important factor for the efficacy of Naive Bayes models.
      Because we decorrelated our dataset, we felt that the remaining correlations beneath the `0.6` threshold was small enough to not interfere with the model's performancce.
      Naive Bayes models are supposed to train well on small number of observations.
      Our dataset is just above the `1000` observation threshold, so we had high hopes that this model would train well.
      This was our second model used to get quick benchmarking numbers.

  5.  **Multi-layer Perceptron**
      We wanted to experiment with the concept of artificial neural nets.
      The inclusion of this model allowed us to to get some experience with an instance of the buzzword-worthy model.
      Given the great flexibility of ANNs, we expected very good performance from this model.

  6.  **Random Forest**
      Given the unknown nature and limited domain knowledge that we could use to direct the machine learning process, the use of at least one ensamble learning technique seemed to be a prudent choice.
      We selected the random forest model for it's ease of use and support of multi-output classes.

  7.  **Support Vector Machines**
      The authors have a really solid theoretical understanding of how SVMs work so their inclusion was a natural choice.
      Because we have multi-class output, a support vector classifier using the "One-versus-One" multiclass strategy strategy was used.

  8.  **X-Gradiant Boost**
      With the guidance of our professor Anita Raja, we were directed to experiment with `XGBoost` as a possibly effective ensamble learning technique which might out perform the random forest.
      This is the model we had the least knowledge of, but it served as a great learning opportunity, both from a technical and theoretic perspective.


## Model Selection