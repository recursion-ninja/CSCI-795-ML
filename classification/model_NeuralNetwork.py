import numpy              as np

from model_selection        import STATIC_SEED, model_evaluation
from sklearn.neural_network import MLPClassifier


beta_candidates_vals  = ( [ 10**(-1 * i) for i in range(1,4)] +
                          list(np.linspace(0.2, 0.8, num=7))  +
                          [(((10**i) - 1) / (10**i)) for i in range(1,4)]
                        )
feature_extraction    = { 'tagged_trait'               : True
                        , 'standardized_label_classes' : 5
                        , 'decorrelate' : 0.6
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

model_evaluation("Multi-layer Perceptron", MLPClassifier(), dataset_params=feature_extraction, param_grid=search_grid_options, best_hyperparameters=hyperparameter_values)
