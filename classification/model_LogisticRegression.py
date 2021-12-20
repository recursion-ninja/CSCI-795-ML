from model_selection      import STATIC_SEED, model_evaluation
from numpy                import linspace
from sklearn.linear_model import LogisticRegression


feature_extraction    = { 'tagged_trait'               : True
                        , 'standardized_label_classes' : 5
                        , 'decorrelate'                : 0.6
                        }
search_grid_options   = { 'penalty'     : ['elasticnet','l1','l2']
                        , 'solver'      : ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']
                        , 'C'           : [20**(-1*i) for i in range(1,6)]
                        , 'tol'         : [10**(-1*i) for i in range(1,6)]
                        , 'max_iter'    : [10**( 1+i) for i in range(1,4)]
                        , 'random_state': [STATIC_SEED]
                        , 'l1_ratio'    : linspace(0, 1, num=13)
                        }

hyperparameter_values = { 'penalty'     : 'l2'
                        , 'solver'      : 'lbfgs'
                        , 'C'           : 0.05
                        , 'tol'         : 0.1
                        , 'max_iter'    : 10000
                        , 'random_state': STATIC_SEED
                        }

model_evaluation("Logistic Regression", LogisticRegression(), dataset_params=feature_extraction, param_grid=search_grid_options, best_hyperparameters=hyperparameter_values)
