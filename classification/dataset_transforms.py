import numpy             as np
import pandas            as pd
import pathlib           as p
import functools         as f

from sklearn.preprocessing import LabelBinarizer, QuantileTransformer


def retrieve_monster_dataset(compress=True, textual=False, tagged_damage=False, tagged_trait=False, standardized_label_classes=None, decorrelate=None):
    absPath = p.Path(__file__).parent.resolve()
    dataset = pd.read_csv(absPath.parent.joinpath('data','dnd-5e-monsters.csv'), sep=',')

    if tagged_damage:
        dataset = inclusionBitEncodeColumn(dataset, 'Damage Tags', 'Damage')

    if tagged_trait:
        dataset = inclusionBitEncodeColumn(dataset, 'Trait Tags', '')

    if standardized_label_classes is not None:
        dataset = standarize_data_set(dataset, class_count=standardized_label_classes)

    if decorrelate is not None:
        dataset = decorrelate_columns(dataset, threshold=decorrelate)

    if not textual:
        dataset = dropTextualColumns(dataset)

    if compress:
        dataset = compress_dataset(dataset)
        
    return dataset


def decorrelate_columns(df, threshold=0.6):
    corr_set = list()

    for rName, row in df.iloc[:, :-1].corr().iterrows():
        for cName, col in row.iteritems():
            if rName > cName and col >= 0.6:
                cL = list(filter(lambda x: cName in x, corr_set))
                cV = cL[0] if len(cL) > 0 else None
                rL = list(filter(lambda x: rName in x, corr_set))
                rV = rL[0] if len(rL) > 0 else None
                if cV is None and rV is None:
                    corr_set.append({cName, rName})
                elif cV is None and rV is not None:
                    rV.add(cName)
                elif cV is not None and rV is None:
                    cV.add(rName)
                elif cV is not None and rV is not None:
                    corr_set.remove(rV)
                    cV |= rV

    for proxies in corr_set:
        kept = proxies.pop()
        for extra in proxies:
            if extra in df.columns:
                df.drop(extra, 1, inplace=True)

    return df


# Make dataset up less than 19% of the original space!
def compress_dataset(dataset):
    # Unsigned, large-valued columns
    uWide = { 'Hit Points'
            }
    # Signed,   large-valued columns
    sWide = { 'Elo Rank'
            }
    # Textual content columns
    texty = { 'Damage Tags'
            , 'Spellcasting Tags'
            , 'Trait Tags'
            , 'Name'
            , 'Type'
            }
    
    for col in list(dataset.columns):
        # If the column contains textual data, skip it!
        if col in texty:
            continue
        
        # If the column can contain potentially large values,
        # and the values are non-negative, truncate the bits!
        if col in uWide:
            setType(dataset, col, np.uint16)
        # If the column can contain potentially large values,
        # and the values can be negative, truncate the bits!
        elif col in sWide:
            setType(dataset, col, np.int16)
        # If the column is not textual and cannot contain large values,
        # then it is a tiny column, turncate as many bits as possible@
        else:
            setType(dataset, col, np.uint8)

    return dataset


def oneHotBitEncodeColumn(df, colName, prefix=None):
    if colName not in df.columns:
        return
    spot = df.columns.get_loc(colName)
    cols = pd.get_dummies(df[colName], prefix)
    ordered = sorted(cols.columns)
    ordered.reverse()
    for name in ordered:
        df.insert(spot, name, cols[name])
    df.drop(colName, 1, inplace=True)
    return df
    

def inclusionBitEncodeColumn(df, colName, prefix=None):
    if colName not in df.columns:
        return
    values  = pd.DataFrame(df[colName].values.tolist()).stack().values
    uniques = f.reduce(lambda a,b: set(b.split(',')).union(a), values, set())
    colSpot = df.columns.get_loc(colName)
    ordered = sorted(uniques)
    ordered.reverse()
    for val in ordered:
        col = df[colName].map(lambda x: val in set(str(x).split(',')))
        pref = colName
        if prefix is not None:
            pref = prefix
        if prefix != "":
            pref += "_"
        df.insert(colSpot, pref + val, col.astype(np.uint8))
    df.drop(colName, 1, inplace=True)
    return df


## Acceptable classes are:
# 20
# 10
#  5
#  2 (binary, default)
def standarize_data_set(df, colName='Elo Rank', class_count=None):
    # Standard normalization:
    scaler = QuantileTransformer(output_distribution='normal')
    df[colName] = scaler.fit_transform(df[colName].to_numpy().reshape(-1, 1))

    if class_count == 20:
        df.loc[:,colName] *=4.5
        df.loc[:,colName] +=10
        setType(df, colName, np.uint8)
        df.drop(df.loc[df[colName] >= 20].index, inplace=True)
#        df.loc[:,colName] +=1

    elif class_count == 10:
        df.loc[:,colName] *=2.5
        df.loc[:,colName] +=5
        setType(df, colName, np.uint8)
        df.drop(df.loc[df[colName] >= 10].index, inplace=True)
#        df.loc[:,colName] +=1

    elif class_count == 5:
        df.loc[:,colName] *=1.33
        df.loc[:,colName] +=3
        setType(df, colName, np.uint8)
        df.drop(df.loc[df[colName] >= 5].index, inplace=True)
#        df.loc[:,colName] +=1
    else:
        df.loc[:,colName] *=0.5
        df.loc[:,colName] +=1
        setType(df, colName, np.uint8)
        df.drop(df.loc[df[colName] >= 2].index, inplace=True)

    return df


def dropTextualColumns(df):
    return df.select_dtypes(exclude=['object'])


def dropColumns_Names(df, names):
    for name in df.columns:
        if name in names:
            df.drop(name, 1, inplace=True)


def setType(df, colName, colType):
    df[colName] = df[colName].astype(colType)
