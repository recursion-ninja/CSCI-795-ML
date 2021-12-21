from classifier_specification import STATIC_SEED, model_evaluation
from featureset_specification import default_feature_specification
from sklearn.tree             import DecisionTreeClassifier
from copy                     import deepcopy


#########################################
###   Model Specific Definitions:
#########################################

classifier  = DecisionTreeClassifier()

designation = 'Decision Tree'

hyperparameter_values = { 'criterion'    : 'gini'
                        , 'splitter'     : 'best'
                        , 'max_features' : 'log2'
                        , 'random_state' : STATIC_SEED
                        }
search_grid_options   = { 'criterion'    : ['gini', 'entropy']
                        , 'splitter'     : ['best', 'random']
                        , 'max_features' : ['auto', 'sqrt', 'log2']
                        , 'random_state' : [STATIC_SEED]
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

