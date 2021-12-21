from classifier_specification import STATIC_SEED, model_evaluation
from featureset_specification import default_feature_specification

import xgboost as xgb


#########################################
###   Model Specific Definitions:
#########################################


class_count = 5

classifier  = xgb.XGBClassifier()

designation = 'X Gradient Boosting'

hyperparameter_values = { 'objective'         : 'multi:softprob'
                        , 'eval_metric'       : 'mlogloss'
                        , 'num_class'         : class_count
                        , 'n_estimators'      : 50
                        , 'use_label_encoder' : False
                        , 'colsample_bytree'  : 0.2
                        , 'gamma'             : 0.2
                        , 'learning_rate'     : 0.2
                        , 'max_depth'         : 3
                        , 'random_state'      : STATIC_SEED
                        }
search_grid_options   = { 'objective'         : [ 'multi:softprob' ]
                        , 'eval_metric'       : [ 'mlogloss' ]
                        , 'num_class'         : [ class_count ]
                        , 'n_estimators'      : [   50 ] # , 100, 150, 200 ]
                        , 'use_label_encoder' : [ False ]
                        , 'colsample_bytree'  : [ 0.2 ] # [ i/10.0 for i in range(1, 10) ]
                        , 'gamma'             : [ i/10.0 for i in range(6) ]
                        , 'learning_rate'     : [ 0.2 ] # [ 0.1, 0.2, 0.3 ] # [ 0.01, 0.1, 0.2, 0.3 ]
                        , 'max_depth'         : range(3, 4) # range(3, 10)
                        , 'random_state'      : [STATIC_SEED]
                        }


#########################################
###   Generic Definitions:
#########################################


def best_classifier(tiers=5):
    return (classifier.set_params(**hyperparameter_values))


evaluation_parameters = { 'classifier_label'     : designation
                        , 'classifier'           : classifier
                        , 'dataset_params'       : default_feature_specification
                        , 'hyperspace_params'    : search_grid_options
                        , 'best_hyperparameters' : hyperparameter_values
                        }


model_evaluation(**evaluation_parameters)
