from classifier_specification     import STATIC_SEED, model_evaluation
from sklearn.naive_bayes import MultinomialNB


#########################################
###   Model Specific Definitions:
#########################################


classifier  = MultinomialNB()

designation = 'Multinomial Naïve Bayes'

feature_extraction    = { 'tagged_trait'               : True
                        , 'standardized_label_classes' : 5
                        , 'decorrelate'                : 0.6
                        }
hyperparameter_values = { 'alpha': 0.01
                        , 'fit_prior': False
                        }
search_grid_options   = { 'alpha'     : [10**(i - 4) for i in range(0,9)]
                        , 'fit_prior' : [False, True]
                        }


#########################################
###   Generic Definitions:
#########################################


def best_classifier():
    return (classifier.set_params(hyperparameter_values))


evaluation_parameters = { 'classifier_label'     : designation
                        , 'classifier'           : classifier
                        , 'dataset_params'       : feature_extraction
                        , 'hyperspace_params'    : search_grid_options
                        , 'best_hyperparameters' : hyperparameter_values
                        }


model_evaluation(**evaluation_parameters)
