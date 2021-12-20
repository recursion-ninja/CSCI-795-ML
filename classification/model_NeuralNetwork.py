import numpy              as np

from classifier_specification        import STATIC_SEED, model_evaluation
from sklearn.neural_network import MLPClassifier


#########################################
###   Model Specific Definitions:
#########################################


classifier  = MLPClassifier()

designation = 'Multi-layer Perceptron'

beta_candidates_vals  = ( [ 10**(-1 * i) for i in range(1,4)] +
                          list(np.linspace(0.2, 0.8, num=7))  +
                          [(((10**i) - 1) / (10**i)) for i in range(1,4)]
                        )
feature_extraction    = { 'tagged_trait'               : True
                        , 'standardized_label_classes' : 5
                        , 'decorrelate' : 0.6
                        }
hyperparameter_values = { 'solver'             : 'adam'
                        , 'activation'         : 'logistic'
                        , 'learning_rate'      : 'constant'
                        , 'learning_rate_init' : 0.001
                        , 'alpha'              : 0.1
                        , 'beta_1'             : 0.8
                        , 'beta_2'             : 0.99
                        , 'early_stopping'     : False
                        , 'random_state'       : STATIC_SEED
                        }
search_grid_options   = { 'activation'         : ['logistic']
                        , 'solver'             : ['adam']
                        , 'learning_rate'      : ['constant', 'invscaling', 'adaptive']
                        , 'learning_rate_init' : [10**(i - 5) for i in range(0,10)]
                        , 'alpha'              : [0.1]
                        , 'beta_1'             : beta_candidates_vals
                        , 'beta_2'             : beta_candidates_vals
                        , 'early_stopping'     : [False]
                        , 'random_state'       : [STATIC_SEED]
                        }


#########################################
###   Generic Definitions:
#########################################


def best_classifier():
    return (classifier.set_params(hyperparameter_values))


evaluation_parameters = { 'classifier_label'     : designation
                        , 'classifier'           : classifier
                        , 'dataset_params'       : feature_extraction
                        , 'hyperspace_params'    : search_grid_options
                        , 'best_hyperparameters' : hyperparameter_values
                        }


model_evaluation(**evaluation_parameters)
