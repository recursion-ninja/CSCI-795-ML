# CSCI-795-ML

### The course project for CSCI-795: Introduction to Machine Learning

### Authors

 - Alex Washburn (@recursion-ninja)

 - "John"  @johnl11235

---


## Abstract

In this project, we explore an under-developed aspect of Dungeons and Dragons 5th Edition (D&D), the monster "Challenge Rating" system.
The Challenge Rating (CR) is a measure of a monster's lethality against a party of *four* characters, each that a character level equal to the monster's CR.
Unfortunately, the supplied CR values that have been published are more often than not poor estimates of monster lethality.
In this project, we attempt to produce an substitute ranking of monster lethality, ordering them into teirs of either `[1, 5]`, `[1, 10]`, or `[1, 20]`.
We hypothesize that the application of machine learning will produce a better intdicator of monster lethality than the supplied CR score.


## The D&D Monster Data

We take the stat-block of each monster from the [`5e.tools`][5e-mirror] database and match the monster with the [Elo Ranking][elo-wiki] from [`dndcombat.com`][compendium].
Elo Ranks scores on [`dndcombat.com`][compendium] are continually updated.
The Elo observations were taken on `2021-12-08`.

The raw data used for this project has been stored within the repository for reference:

  - [`data/5e.tools/*`     ][repo-5e-tools  ]
  - [`data/dndcombat.com/*`][repo-dnd-combat]

Both the data from [`5e.tools`][5e-mirror] and [`dndcombat.com`][compendium] were retreived in [JSON format][json].
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


## Feature Selection and Extraction

The curated [`dnd-5e-monsters.csv`][repo-dataset] dataset has `1386` rows and `67` columns, constituting the project's initial observations and measurements, respectively.
There are two leading textual columns, labeled `'Name'` and `'Type'` indexed `[0, 1]`,, which are dropped for analysis as they do not influence combat efficacy and are not convertable to a meanininful numeric representation.
The subsequent `20` columns indexed `[2, 21]` are "continuous," integral-valued measurments of common D&D attributes.
The final `'Elo Rank'` column indexed `[66, 66]` is the label for supervised machine learning models.
The next three trailing coumns, labeled `Damage Tags`, `Spellcasting Tags` and `Trait Tags` indexed `[63, 65]`
The remaining columns indexed `[22, 62]` are binary indicators for various monster atributes.
A column summary of the initial data set is presented below:

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


