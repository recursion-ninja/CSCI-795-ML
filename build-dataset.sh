#!/bin/bash

# This script creates a FSA describing the input grammar *.g4

if [ ! "$#" -lt 4 ]; then
  echo "Usage: ./assemble-dataset.sh"
  exit 1
fi

rank="data/dndcombat.com/"
stat="data/5e.tools/"
file="dnd-5e-monsters.csv"

echo "Compiling JSON parser/matcher"
cd assemble-dataset-from-json
cabal build
exe=$(cabal list-bin assemble-dataset-from-json)
cd ../

echo "Assembling D&D Monster data-set"
echo "  using Elo ranks from $rank"
echo "  and Stat-blocks from $stat"
echo ""
CMD="$exe -r [\"$rank/*.json\"] -s [\"$stat/bestiary-*.json\"] -o $file"
$CMD
