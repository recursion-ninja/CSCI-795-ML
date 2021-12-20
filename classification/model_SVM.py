from model_selection import STATIC_SEED, model_evaluation
from sklearn.svm     import SVC

import numpy as np


feature_extraction    = { 'tagged_trait'               : True
                        , 'standardized_label_classes' : 5
                        , 'decorrelate'                : 0.6
                        }
search_grid_options   = { 'C'                       : [10**(-1 * i) for i in range(0,9)] + list(np.linspace(0.005, 0.001, num=31)) + [0.04625]
                        , 'kernel'                  : ['linear', 'poly', 'rbf', 'sigmoid']
                        , 'degree'                  : range(2,17)
                        , 'gamma'                   : ['scale','auto']
                        , 'shrinking'               : [ False, True ]
                        , 'probability'             : [ False, True ]
                        , 'decision_function_shape' : [ 'ovo', 'ovr' ]
                        , 'random_state'            : [ STATIC_SEED ]
                        }
hyperparameter_values = { 'C'                       : 0.04625
                        , 'kernel'                  : 'linear'
                        , 'gamma'                   : 'scale'
                        , 'shrinking'               : False
                        , 'probability'             : True
                        , 'decision_function_shape' : 'ovo'
                        , 'random_state'            : STATIC_SEED
                        }

model_evaluation("Support Vector Classifier", SVC(), dataset_params=feature_extraction, param_grid=search_grid_options, best_hyperparameters=hyperparameter_values)
