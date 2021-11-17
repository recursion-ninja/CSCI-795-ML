{-# LANGUAGE LambdaCase #-}

module Main
  ( main
  ) where

import Item
import Parameters
import Control.Monad ((<=<))
import Data.Aeson (Object, Value(..), eitherDecode')
import Data.Aeson.Key (Key, toString)
import Data.Aeson.Types (parseEither, parseJSON)
import qualified Data.Aeson.KeyMap    as KM
import           Data.ByteString.Lazy (ByteString)
import qualified Data.ByteString.Lazy as BS
import Data.Csv   (encodeDefaultOrderedByName)
import Data.Foldable (fold, toList)


main :: IO ()
main = do
    params <- parseCommandLineOptions
    byteStreams <- traverse (traverse BS.readFile . getInputFile) $ inputFiles params :: IO [(Key, ByteString)]
    case traverse (extractItems <=< traverse eitherDecode') byteStreams :: Either String [[Item]] of
      Left errMsg -> fail errMsg
      Right    [] -> putStrLn "The were no magic items!"
      Right items ->
        let csvStream = encodeDefaultOrderedByName $ fold items
        in  BS.writeFile (outputFile params) csvStream


extractItems :: (Key, Object) -> Either String [Item]
extractItems (key, val) =
    target >>= \case
      Array arr    -> parseItems arr
      obj@Object{} -> pure <$> parseItem obj
      wrongValue   -> Left $ "Expected to parse a target of an Array or Object\nRecieved: " <> show wrongValue
  where
    target
      -- Allow "" to be a key representing no indexing!
      | null (toString key) = Right $ Object val
      | otherwise =
        let maybeItems = KM.lookup key val
        in  case maybeItems of
              Nothing -> Left $ "No index of " <> show key
              Just v  -> Right v


parseItems :: Foldable f => f Value -> Either String [Item]
parseItems = traverse parseItem . toList


parseItem :: Value -> Either String Item
parseItem = parseEither parseJSON
