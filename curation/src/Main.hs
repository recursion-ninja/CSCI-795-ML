{-# LANGUAGE LambdaCase        #-}
{-# LANGUAGE OverloadedStrings #-}

module Main
  ( main
  ) where

import           Control.Monad        ((<=<))
import           Data.Aeson           (FromJSON, Object, Value(..), eitherDecode')
import           Data.Aeson.Key       (Key)
import qualified Data.Aeson.KeyMap    as KM
import           Data.Aeson.Types     (parseEither, parseJSON)
import           Data.ByteString.Lazy (ByteString)
import qualified Data.ByteString.Lazy as BS
import           Data.Csv             (DefaultOrdered, ToNamedRecord, encodeDefaultOrderedByName)
import           Data.Either
import           Data.Foldable        (fold, toList)
import qualified Data.Map.Strict      as Map
import           Data.Maybe           (isJust)
import           GHC.Exts             (IsList(fromList))
import           Monster.Elo
import           Monster.StatBlock
import           Parameters
import           System.FilePath.Glob


main :: IO ()
main = do
    params <- parseCommandLineOptions
    ranks  <- readAndDecodeFiles extractRankings   $ filesWithRanks params :: IO [EloReference]
    stats  <- readAndDecodeFiles extractStatBlocks $ filesWithStats params :: IO [StatBlock]

    let (unmatched, matched) = matchRankToStat ranks stats

    writeOutCSV (outputFile params) matched

    putStr $ unlines
      [ unwords [ "Data Summary:",       "matched"                 , "+",       "unmatched"                                , "=",       "total"                ]
      , unwords [ "Elo Rankings:", padBy "matched" $ length matched, "+", padBy "unmatched" $ length ranks - length matched, "=", padBy "total" $ length ranks ]
      , unwords [ "D&D Monsters:", padBy "matched" $ length matched, "+", padBy "unmatched" $ length              unmatched, "=", padBy "total" $ length stats ]
      , unwords [ "CSV Location:", show $ outputFile params ]
      ]


padBy :: Show a => String -> a -> String
padBy long str =
    let width = length long
        shown = show str
    in  replicate (width - length shown) ' ' <> shown


readAndDecodeFiles :: (Object -> Either String [a]) -> [FilePath] -> IO [a]
readAndDecodeFiles extractor paths = do
    let globPatterns = compile <$> paths
    matchedPaths <- fold <$> globDir globPatterns "."
    byteStreams  <- traverse BS.readFile matchedPaths :: IO [ByteString]
    let  results = traverse (extractor <=< eitherDecode') byteStreams
    case results of
      Left errMsg -> fail errMsg
      Right    [] -> fail "The were no extracted values!"
      Right value -> pure $ fold value


extractRankings :: Object -> Either String [EloReference]
extractRankings   = extractFromKey extractionKeyForRanks


extractStatBlocks :: Object -> Either String [StatBlock]
extractStatBlocks = extractFromKey extractionKeyForStats


extractFromKey :: FromJSON a => Key -> Object -> Either String [a]
extractFromKey key root =
    let missingKey = Left $ "No index of " <> show key
        parseOne  = parseEither parseJSON
        parseMany = traverse parseOne . filter (not . isModifierEntry) . toList
        arrayMay =
          \case
            Array arr -> Just arr
            _         -> Nothing
    in  maybe missingKey parseMany $ KM.lookup key root >>= arrayMay


writeOutCSV :: (DefaultOrdered a, ToNamedRecord a) => FilePath -> [a] -> IO ()
writeOutCSV path = BS.writeFile path . encodeDefaultOrderedByName


matchRankToStat :: (Foldable f, Foldable g) => f EloReference -> g StatBlock -> ( [StatBlock], [StatBlock] )
matchRankToStat ranks = partitionEithers . fmap f . toList
  where
    mapping = fromList $ toRankingPair <$> toList ranks

    f stat =
        case getMonsterName stat `Map.lookup` mapping of
          Just elo -> Right $ setEloRank elo stat
          Nothing  -> Left stat


isModifierEntry :: Value -> Bool
isModifierEntry (Object km) = isJust $ KM.lookup "_copy" km
isModifierEntry _           = False
