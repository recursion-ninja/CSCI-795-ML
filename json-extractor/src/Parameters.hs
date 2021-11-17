{-# Language DerivingStrategies #-}
{-# Language GeneralizedNewtypeDeriving #-}
{-# Language OverloadedStrings  #-}

module Parameters
  ( parseCommandLineOptions
  , Parameters(..)
  , InputFile(..)
  ) where

import Data.Aeson.Key (Key)
import Data.Foldable
import Options.Applicative


data  Parameters
    = Parameters
    { inputFiles :: [InputFile]
    , outputFile :: FilePath
    }
    deriving stock (Show)


newtype InputFile = Input { getInputFile :: (Key, FilePath) }
    deriving newtype (Read, Show)


defaultOutputCSV :: FilePath
defaultOutputCSV = "magic-items.csv"


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
          <$> inputFilesSpec
          <*> outputFileSpec


    inputFilesSpec :: Parser [InputFile]
    inputFilesSpec = option auto $ fold
        [ short 'i'
        , long  "inputs"
        , help  "input file(s)"
        , metavar "[ ( KEY, FILE ) ]"
        ]

    outputFileSpec :: Parser FilePath
    outputFileSpec = strOption $ fold
        [ short 'o'
        , long  "output"
        , value defaultOutputCSV
        , help  $ fold ["Output file", " (default ", defaultOutputCSV, ")"]
        , metavar "FILE"
        ]
