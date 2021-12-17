#!/bin/bash

tool="curate-json"
path="data"
rank="$path/dndcombat.com"
stat="$path/5e.tools"
file="$path/dnd-5e-monsters.csv"

echo "Compiling $tool tool"
cd curation
cabal build
exe=$(cabal list-bin $tool)
cd ../

echo "Curating D&D Monster data-set"
echo "  using Elo ranks from $rank"
echo "  and Stat-blocks from $stat"
echo ""
CMD="$exe -r '$rank/*.json' -s '$stat/bestiary-*.json' -o '$file'"
echo "$CMD"
$CMD
