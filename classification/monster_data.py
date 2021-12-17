import numpy   as np
import pathlib as p
import pandas  as pd


def retreive_monster_dataset():
    absPath = p.Path(__file__).parent.resolve()
    dataset = pd.read_csv(absPath.parent.joinpath('data','dnd-5e-monsters.csv'), sep=',')
    return compress_dataset(dataset)
    

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


def setType(df, colName, colType):
    df[colName] = df[colName].astype(colType)
