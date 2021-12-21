from classifier_specification import STATIC_SEED, model_evaluation
from featureset_specification import default_feature_specification
from sklearn.ensemble         import RandomForestClassifier
from copy                     import deepcopy


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


evaluation_parameters = { 'classifier_label'     : designation
                        , 'classifier'           : classifier
                        , 'dataset_params'       : default_feature_specification
                        , 'hyperspace_params'    : search_grid_options
                        , 'best_hyperparameters' : hyperparameter_values
                        }
t_05 = deepcopy(evaluation_parameters)
t_10 = deepcopy(evaluation_parameters)
t_10['dataset_params']['standardized_label_classes'] = 10
t_20 = deepcopy(evaluation_parameters)
t_20['dataset_params']['standardized_label_classes'] = 20
tiered_parameters     = {  5: t_05
                        , 10: t_10
                        , 20: t_20
                        }


def best_classifier(tiers=5):
    return classifier.set_params(**hyperparameter_values)


def tier_parameters(tiers=5):
    return tiered_parameters[tiers] 


def main():
    model_evaluation(**evaluation_parameters)
#    clf = best_classifier()
#    print("Features :", clf.n_features_in_)
#    print("Inputs   :", clf.feature_names_in_)
#    print("Outputs  :", clf.n_outputs_)
#    print("Important:", clf.feature_importances_)


if __name__ == "__main__":
    main()
