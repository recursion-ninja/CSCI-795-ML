from model_selection   import STATIC_SEED, model_evaluation
from sklearn.neighbors import KNeighborsClassifier

import numpy as np


feature_extraction    = { 'tagged_trait'               : True
                        , 'standardized_label_classes' : 5
                        , 'decorrelate'                : 0.6
                        }
search_grid_options   = { 'n_neighbors' : np.arange(1, 37, 2)
                        , 'p'           : [1, 2, 5, 10, 20, 30, 50, 100]
                        , 'weights'     : ["uniform", "distance"]
                        }
hyperparameter_values = None

model_evaluation("K Nearest Neighbors", KNeighborsClassifier(), dataset_params=feature_extraction, param_grid=search_grid_options, best_hyperparameters=hyperparameter_values)
