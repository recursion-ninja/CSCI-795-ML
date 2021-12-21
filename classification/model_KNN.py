from classifier_specification import STATIC_SEED, model_evaluation
from featureset_specification import default_feature_specification
from sklearn.neighbors        import KNeighborsClassifier


#########################################
###   Model Specific Definitions:
#########################################

classifier  = KNeighborsClassifier()

designation = 'K Nearest Neighbors'

hyperparameter_values = { 'algorithm'   : 'ball_tree'
                        , 'weights'     : 'distance'
                        , 'n_neighbors' : 30
                        , 'leaf_size'   : 5
                        , 'p'           : 1
                        }
search_grid_options   = { 'n_neighbors' : list(range(1, 23, 2)) + list(range(23, 32)) + list(range(33, 38, 2))
                        , 'p'           : range(1,5)
                        , 'weights'     : ['distance', 'uniform']
                        , 'algorithm'   : ['auto', 'ball_tree', 'kd_tree']
                        , 'leaf_size'   : list(range(1,10)) + list(range(10, 51, 5))
                        }


#########################################
###   Generic Definitions:
#########################################


def best_classifier(tiers=5):
    return (classifier.set_params(**hyperparameter_values))


evaluation_parameters = { 'classifier_label'     : designation
                        , 'classifier'           : classifier
                        , 'dataset_params'       : default_feature_specification
                        , 'hyperspace_params'    : search_grid_options
                        , 'best_hyperparameters' : hyperparameter_values
                        }


model_evaluation(**evaluation_parameters)
