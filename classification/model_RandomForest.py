from classifier_specification import STATIC_SEED, model_evaluation
from featureset_specification import default_feature_specification
from sklearn.ensemble         import RandomForestClassifier


#########################################
###   Model Specific Definitions:
#########################################


classifier  = RandomForestClassifier()

designation = 'Random Forest'


search_grid_options   = { 'n_estimators' : [ 10*i for i in range(1,16)]
                        , 'criterion'    : ['gini', 'entropy']
                        , 'max_features' : ['auto', 'sqrt', 'log2']
                        , 'bootstrap'    : [False, True]
                        , 'oob_score'    : [False, True]
                        , 'class_weight' : [None, 'balanced', 'balanced_subsample']
                        , 'random_state' : [STATIC_SEED]
                        }
hyperparameter_values = { 'n_estimators' : 150
                        , 'criterion'    : 'entropy'
                        , 'max_features' : 'auto'
                        , 'bootstrap'    : True
                        , 'oob_score'    : False
                        , 'class_weight' : 'balanced'
                        , 'random_state' : STATIC_SEED
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
