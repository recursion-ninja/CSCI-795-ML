from model_selection    import STATIC_SEED, model_evaluation
from numpy              import linspace
from sklearn.multiclass import OneVsRestClassifier

import xgboost as xgb

feature_extraction    = { 'tagged_trait'               : True
                        , 'standardized_label_classes' : 5
                        , 'decorrelate'                : 0.6
                        }
search_grid_options   = { 'n_estimators'      : [50, 100, 150, 200]
                        , 'learning_rate'     : [0.01, 0.1, 0.2, 0.3]
                        , 'max_depth'         : range(3, 10)
#                        , 'colsample_bytree'  : [ i/10.0 for i in range(1, 3) ]
#                        , 'gamma'             : [ i/10.0 for i in range(3) ]
                        , 'objective'         : ['multi:softprob']
                        , 'use_label_encoder' : [False]
                        , 'num_class'         : [3]
                        }

hyperparameter_values = None

model_evaluation("XG Boost", xgb.XGBClassifier(objective="multi:softprob", random_state=42), dataset_params=feature_extraction, param_grid=search_grid_options, best_hyperparameters=hyperparameter_values)
