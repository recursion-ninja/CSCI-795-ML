{-# LANGUAGE DeriveAnyClass             #-}
{-# LANGUAGE DeriveGeneric              #-}
{-# LANGUAGE DerivingStrategies         #-}
{-# LANGUAGE GeneralizedNewtypeDeriving #-}
{-# LANGUAGE OverloadedStrings          #-}
{-# LANGUAGE RecordWildCards            #-}

module Item
  ( Item()
  ) where

import Control.Applicative
import Data.Aeson          hiding ((.=))
import Data.Aeson.KeyMap   (lookup)
import Data.Aeson.Types    (Parser)
import Data.Csv            (DefaultOrdered(..), Field, ToField(..), ToNamedRecord(..), namedRecord, (.=))
import Data.Foldable       (fold)
import Data.List           (intersperse)
import Data.Maybe
import Data.String
import Data.Text           hiding (intersperse)
import GHC.Generics
import Prelude             hiding (break, lookup, null)
import Text.Read


newtype Bonus = Bonus Int
    deriving newtype (Eq, Num, Show)
    deriving stock   (Generic)


instance FromJSON Bonus where

    parseJSON = withText "Bonus" $ \txt ->
        let errMsg = fail $ "Cound not parse Bonus: '" <> unpack txt <> "'"
        in  maybe errMsg pure $ uncons txt >>= parseBonus
      where
        parseBonus (sign, val) = do
            f <- case sign of
                  '+' -> Just id
                  '-' -> Just negate
                  _   -> Nothing
            v <- readMaybe $ unpack val :: Maybe Word
            pure . Bonus . f $ fromEnum v


instance ToField Bonus where

    toField (Bonus n) = fromString $ show n


newtype Dice = Dice (Word, Word)
    deriving stock (Eq, Generic, Show)


instance FromJSON Dice where

    parseJSON = withText "Dice" $ \txt ->
        let (pref,suff) = break (=='d') txt
            tryReadWord = readMaybe . unpack
            errorReport = fail $ "Cound not parse Dice: " <> unpack txt
            returnMaybe = maybe errorReport pure
        in  case uncons suff of
              Nothing    -> returnMaybe $ (\v -> Dice (v,0)) <$> tryReadWord pref
              Just (_,v) -> returnMaybe . fmap Dice . liftA2 (,) (tryReadWord pref) $ tryReadWord v


instance ToField Dice where

    toField (Dice (n,0)) = fromString $ fold [show n]
    toField (Dice (n,f)) = fromString $ fold [show n, "D", show f]


newtype Range = Range (Word, Word)
    deriving stock (Eq, Generic, Show)


instance FromJSON Range where

    parseJSON = withText "Range" $ \txt ->
        let (pref,suff) = break (=='/') txt
            tryReadWord = readMaybe . unpack
            maybeRange  = uncons suff >>= fmap Range . liftA2 (,) (tryReadWord pref) . tryReadWord . snd
            errorReport = fail "Cound not parse Range"
        in  maybe errorReport pure maybeRange


instance ToField Range where

    toField (Range (s,l)) = fromString $ fold [show s, "/", show l]


data  Item
    = Observation
    { name                :: String
    , rarity              :: String
    , attunementRequired  :: Bool
    , cursed              :: Bool
    , sentient            :: Bool
    , weight              :: Double
    , baseItem            :: Maybe String
    , itemType            :: Maybe String

    , conditionImmunities :: [String]
    , damageImmunities    :: [String]
    , damageResistances   :: [String]

    , firearm             :: Bool
    , range               :: Maybe Range
    , weapon              :: Bool
    , weaponBonus         :: Bonus
    , weaponCategory      :: Maybe String
    , weaponProperty      :: [String]
    , damage1             :: Dice
    , damage1Type         :: Maybe String
    , damage2             :: Dice
    , grantsProficiency   :: Bool

    , armor               :: Bool
    , armorClassBonus     :: Bonus
    , armorClassFixed     :: Maybe Word
    , requiredStrength    :: Word
    , stealth             :: Bool

    , poison              :: Bool
    , tattoo              :: Bool
    , savingThrowBonus    :: Bonus
    , spellAttackBonus    :: Bonus
    , spellSaveDCBonus    :: Bonus
    , charges             :: Word
    , recharge            :: Maybe String
    , attachedSpells      :: [String]
    }
    deriving stock    (Eq, Generic, Show)
    deriving anyclass (DefaultOrdered)


instance FromJSON Item where

    parseJSON = withObject "Item" $ \obj -> do
        name                <- obj .:? "name"              .!= "UNNAMED????"
        weight              <- obj .:? "weight"            .!= 0
        baseItem            <- obj .:? "baseItem"
        itemType            <- obj .:? "type"
        rarity              <- obj .:? "rarity"            .!= "none"
        attunementRequired  <- "reqAttune" `existsWithin` obj

        resistances         <- obj .:? "resist"            .!= []
        conditionImmunities <- obj .:? "conditionImmune"   .!= []
        damageImmunities    <- obj .:? "immune"            .!= []

        firearm             <- obj .:? "firearm"           .!= False
        range               <- obj .:? "range"
        weapon              <- obj .:? "weapon"            .!= False
        weaponBonus         <- obj .:? "bonusWeapon"       .!= 0
        weaponCategory      <- obj .:? "weaponCategory"
        weaponProperty      <- obj .:? "property"          .!= []
        damage1             <- obj .:? "dmg1"              .!= Dice (0,0)
        damage1Type         <- obj .:? "dmgType"
        damage2             <- obj .:? "dmg1"              .!= Dice (0,0)
        grantsProficiency   <- obj .:? "grantsProficiency" .!= False
        spellAttackBonus    <- obj .:? "bonusSpellAttack"  .!= 0
        spellSaveDCBonus    <- obj .:? "bonusSpellSaveDc"  .!= 0
        charges             <- obj .:? "charges"           .!= 0
        recharge            <- obj .:? "recharge"
        cursed              <- obj .:? "curse"             .!= False

        armor               <- obj .:? "armor"             .!= False
        armorClassBonus     <- obj .:? "bonusAc"           .!= 0
        armorClassFixed     <- obj .:? "ac"
        requiredStrength    <- ((>>= readMaybe) <$> (obj .:? "strength")) .!= 0
        stealth             <- obj .:? "stealth"           .!= False

        poison              <- obj .:? "poison"            .!= False
        tattoo              <- obj .:? "tattoo"            .!= False
        sentient            <- obj .:? "sentient"          .!= False
        savingThrowBonus    <- obj .:? "bonusSavingThrow"  .!= 0
        attachedSpells      <- obj .:? "attachedSpells"    .!= []

        pure Observation
            { name                = name
            , rarity              = rarity
            , attunementRequired  = attunementRequired
            , cursed              = cursed
            , sentient            = sentient
            , weight              = weight
            , baseItem            = baseItem
            , itemType            = itemType

            , conditionImmunities = conditionImmunities
            , damageImmunities    = damageImmunities
            , damageResistances   = resistances

            , firearm             = firearm
            , range               = range
            , weapon              = weapon
            , weaponBonus         = weaponBonus
            , weaponCategory      = weaponCategory
            , weaponProperty      = weaponProperty
            , damage1             = damage1
            , damage1Type         = damage1Type
            , damage2             = damage2
            , grantsProficiency   = grantsProficiency

            , armor               = armor
            , armorClassBonus     = armorClassBonus
            , armorClassFixed     = armorClassFixed
            , requiredStrength    = requiredStrength
            , stealth             = stealth

            , poison              = poison
            , tattoo              = tattoo
            , savingThrowBonus    = savingThrowBonus
            , spellAttackBonus    = spellAttackBonus
            , spellSaveDCBonus    = spellSaveDCBonus
            , charges             = charges
            , recharge            = recharge
            , attachedSpells      = attachedSpells
            }


instance ToNamedRecord Item where

    toNamedRecord Observation{..} = namedRecord
        [ "name"                .= name
        , "rarity"              .= rarity
        , "attunementRequired"  .= boolToField attunementRequired
        , "cursed"              .= boolToField cursed
        , "sentient"            .= boolToField sentient
        , "weight"              .= weight
        , "baseItem"            .= baseItem
        , "itemType"            .= itemType

        , "conditionImmunities" .= collectionToField conditionImmunities
        , "damageImmunities"    .= collectionToField damageImmunities
        , "damageResistances"   .= collectionToField damageResistances

        , "firearm"             .= boolToField firearm
        , "range"               .= range
        , "weapon"              .= boolToField weapon
        , "weaponBonus"         .= weaponBonus
        , "weaponCategory"      .= weaponCategory
        , "weaponProperty"      .= collectionToField weaponProperty
        , "damage1"             .= damage1
        , "damage1Type"         .= damage1Type
        , "damage2"             .= damage2
        , "grantsProficiency"   .= boolToField grantsProficiency

        , "armor"               .= boolToField armor
        , "armorClassBonus"     .= armorClassBonus
        , "armorClassFixed"     .= armorClassFixed
        , "requiredStrength"    .= requiredStrength
        , "stealth"             .= boolToField stealth

        , "tattoo"              .= boolToField tattoo
        , "poison"              .= boolToField poison
        , "savingThrowBonus"    .= savingThrowBonus
        , "spellAttackBonus"    .= spellAttackBonus
        , "spellSaveDCBonus"    .= spellSaveDCBonus
        , "charges"             .= charges
        , "recharge"            .= recharge
        , "attachedSpells"      .= collectionToField attachedSpells
        ]


collectionToField :: [String] -> Field
collectionToField = fromString . fold . intersperse ","


boolToField :: Bool -> Field
boolToField = fromString . show . fromEnum


existsWithin :: Key -> Object -> Parser Bool
existsWithin key = pure . isJust . lookup key
