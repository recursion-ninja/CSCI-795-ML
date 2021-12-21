from classifier_specification import STATIC_SEED, model_evaluation
from featureset_specification import default_feature_specification
from numpy                    import linspace
from sklearn.svm              import SVC
from copy                     import deepcopy


#########################################
###   Model Specific Definitions:
#########################################


classifier  = SVC()

designation = 'Support Vector Classification'

hyperparameter_values = { 'C'                       : 0.04625
                        , 'kernel'                  : 'linear'
                        , 'gamma'                   : 'scale'
                        , 'shrinking'               : False
                        , 'probability'             : True
                        , 'decision_function_shape' : 'ovo'
                        , 'random_state'            : STATIC_SEED
                        }
search_grid_options   = { 'C'                       : ( [10**(-1 * i) for i in range(0,9)]
                                                      + list(linspace(0.005, 0.001, num=31))
                                                      + [0.04625]
                                                      )
                        , 'kernel'                  : ['linear', 'poly', 'rbf', 'sigmoid']
                        , 'degree'                  : range(2,17)
                        , 'gamma'                   : ['scale','auto']
                        , 'shrinking'               : [ False, True ]
                        , 'probability'             : [ False, True ]
                        , 'decision_function_shape' : [ 'ovo', 'ovr' ]
                        , 'random_state'            : [ STATIC_SEED ]
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
    return (classifier.set_params(hyperparameter_values))


def tier_parameters(tiers=5):
    return tiered_parameters[tiers] 


def main():
    model_evaluation(**evaluation_parameters)


if __name__ == "__main__":
    main()
