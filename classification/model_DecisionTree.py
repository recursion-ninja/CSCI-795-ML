from model_selection import STATIC_SEED, model_evaluation
from sklearn.tree    import DecisionTreeClassifier


feature_extraction    = { 'tagged_trait'               : True
                        , 'standardized_label_classes' : 5
                        , 'decorrelate' : 0.6
                        }
search_grid_options   = { 'criterion'    : ['gini', 'entropy']
                        , 'splitter'     : ['best', 'random']
                        , 'max_features' : ['auto', 'sqrt', 'log2']
                        , 'random_state' : [STATIC_SEED]
                        }

hyperparameter_values = { 'criterion'    : 'gini'
                        , 'splitter'     : 'best'
                        , 'max_features' : 'log2'
                        , 'random_state' : STATIC_SEED
                        }

model_evaluation("Decision Tree", DecisionTreeClassifier(), dataset_params=feature_extraction, param_grid=search_grid_options, best_hyperparameters=hyperparameter_values)
