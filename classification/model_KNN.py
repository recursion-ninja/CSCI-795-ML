from model_selection   import STATIC_SEED, model_evaluation
from sklearn.neighbors import KNeighborsClassifier


feature_extraction    = { 'tagged_trait'               : True
                        , 'standardized_label_classes' : 5
                        , 'decorrelate'                : 0.6
                        }
search_grid_options   = { 'n_neighbors' : range(1, 23, 2) + range(23, 32) + range(33, 38, 2)
                        , 'p'           : range(1,5)
                        , 'weights'     : ['distance', 'uniform']
                        , 'algorithm'   : ['auto', 'ball_tree', 'kd_tree']
                        , 'leaf_size'   : range(1,10) + range(10, 51, 5)
                        }
hyperparameter_values = { 'algorithm'   : 'ball_tree'
                        , 'weights'     : 'distance'
                        , 'n_neighbors' : 30
                        , 'leaf_size'   : 5
                        , 'p'           : 1
                        }

model_evaluation("K Nearest Neighbors", KNeighborsClassifier(), dataset_params=feature_extraction, param_grid=search_grid_options, best_hyperparameters=hyperparameter_values)
