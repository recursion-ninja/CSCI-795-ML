{-# LANGUAGE DerivingStrategies         #-}
{-# LANGUAGE GeneralizedNewtypeDeriving #-}
{-# LANGUAGE OverloadedStrings          #-}

module Parameters
  ( parseCommandLineOptions
  , Parameters(..)
  ) where

import Data.Foldable
import Options.Applicative


data  Parameters
    = Parameters
    { filesWithRanks :: [FilePath]
    , filesWithStats :: [FilePath]
    , outputFile     :: FilePath
    }
    deriving stock (Show)


defaultOutputCSV :: FilePath
defaultOutputCSV = "dnd-5e-monsters.csv"


-- |
-- Command to parse the command line options.
parseCommandLineOptions :: IO Parameters
parseCommandLineOptions = customExecParser preferences parserInformation
  where
    preferences = prefs $ fold [showHelpOnError, showHelpOnEmpty]


-- |
-- Information regarding which command line options are valid and how they are
-- parsed and interpreted.
parserInformation :: ParserInfo Parameters
parserInformation = info commandLineOptions fullDesc
  where
    commandLineOptions =
        Parameters
          <$> inputRanksSpec
          <*> inputStatsSpec
          <*> outputFileSpec


    inputRanksSpec :: Parser [FilePath]
    inputRanksSpec = some . strOption $ fold
        [ short 'r'
        , long  "ranks"
        , help  "ranking file(s)"
        , metavar "[ FILE ]"
        ]

    inputStatsSpec :: Parser [FilePath]
    inputStatsSpec = some . strOption $ fold
        [ short 's'
        , long  "stats"
        , help  "stat-block file(s)"
        , metavar "[ FILE ]"
        ]

    outputFileSpec :: Parser FilePath
    outputFileSpec = strOption $ fold
        [ short 'o'
        , long  "output"
        , value defaultOutputCSV
        , help  $ fold ["Output file", " (default ", defaultOutputCSV, ")"]
        , metavar "FILE"
        ]
