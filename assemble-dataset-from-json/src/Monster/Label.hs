{-# LANGUAGE Strict #-}

module Monster.Label
  ( Label(..)
  ) where

import Data.Coerce
import Data.Char


newtype Label = Label String


instance Eq Label where

    (==) lhs rhs =
        let f = filter isAlpha . fmap toLower . coerce
        in  f lhs == f rhs


instance Ord Label where

    compare lhs@(Label x) rhs@(Label y)
      | lhs == rhs = EQ
      | otherwise  = x `compare` y
