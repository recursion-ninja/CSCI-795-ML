#!/bin/bash

########################
# include the magic
########################
. recording/demo-magic.sh

# hide the evidence
clear
PROMPT_TIMEOUT=2

# Put your stuff here
pei '# Classifying Creature Combat Capability'
pei '# Dungeons and Dragons 5th Edition'
pei '#'
pei '#   * John Lee'
pei '#   * Alex Washburn'
pei '#'
wait
clear

pei '# We are in the root directory of our repository:'
pei '#'
pei '#   https://github.com/recursion-ninja/CSCI-795-ML/'
pei '#'
pei "# Now, let's take a look around."
pei 'ls'
wait
clear

pei '# We collected our creature stat-block data from the venerable 5e.tools site:'
pei '#'
pei '#   https://5e.tools'
pei '#'
pei '# And we scraped our creature Elo ranking from the DnD Combat site:'
pei '#'
pei '#   https://dndcombat.com'
pei '#'
pei '# Both sites provided us some *lovely* JSON files,'
pei '# But of course we have to curate and link these two data sets.'
wait
clear


pei "# Let's check out the curator."
pei "#"
pei 'cd curation'
pei 'ls'
pei '# You can build the curator yourself like this:'
p   'cabal build'
pei '#'
pei '# You can call the curator like this:'
p   "cabal run curate-json -r ../data/dndcombat.com/*.json' -s ../data/5e.tools/bestiary-*.json -o output.csv"
pei 'cd ../'
wait
clear


pei "# Let's checkout the data"
pei "#"
pei 'cd data'
pei 'ls'
pei '# Elo ranks archived here:'
pei 'ls dndcombat.com'
pei '# Stat-blocks archived here:'
pei 'ls 5e.tools/'
pei '# Curated data set archived here:'
pei 'ls dnd-5e-monsters.csv'
pei 'cd ../'
wait
clear


pei '# But you came here for machine learning.'
pei "# Let's checkout the classifiers!"
pei 'cd classification'
pei 'ls'
pei '# WOW! Look at all those models!'
pei "#"
pei "Shall we take a tour?"
wait
clear


pei '# No time for a whole tour!'
pei '#'
pei "# Let's just checkout the best classifier,"
pei '# Constructed using the X Gradient Boosting model'
pei '#'
pei 'python3 model_XGBoost.py'
wait
clear


pei '# Now you know how to play with our project on your own!'
wait
clear
