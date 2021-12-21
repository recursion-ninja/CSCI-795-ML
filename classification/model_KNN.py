from classifier_specification import STATIC_SEED, model_evaluation
from featureset_specification import default_feature_specification
from sklearn.neighbors        import KNeighborsClassifier
from copy                     import deepcopy


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
