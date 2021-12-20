from model_selection      import STATIC_SEED, model_evaluation
from numpy                import linspace
from sklearn.linear_model import LogisticRegression


feature_extraction    = { 'tagged_trait'               : True
                        , 'standardized_label_classes' : 5
                        , 'decorrelate'                : 0.6
                        }
search_grid_options   = { 'C'           : [10**(i - 4) for i in range(0,9)]
                        , 'kernel'      : ['linear', 'poly', 'rbf', 'sigmoid']
                        , 'degree'      : range(2,16)
                        , 'gamma'       : ['scale', 'auto']
                        , 'shrinking'   : [False, True]
                        , 'probability' : [False, True]
                        , 'decision_function_shape' : ['ovo', 'ovr']
                        , 'random_state' : [STATIC_SEED]
                        }
hyperparameter_values = None

model_evaluation("Support Vector Classifier", SVC(), dataset_params=feature_extraction, param_grid=search_grid_options, best_hyperparameters=hyperparameter_values)
