from model_selection     import STATIC_SEED, model_evaluation
from sklearn.naive_bayes import MultinomialNB


feature_extraction    = { 'tagged_trait'               : True
                        , 'standardized_label_classes' : 5
                        , 'decorrelate'                : 0.6
                        }
search_grid_options   = { 'alpha'     : [10**(i - 4) for i in range(0,9)]
                        , 'fit_prior' : [False, True]
                        }
hyperparameter_values = { 'alpha': 0.01
                        , 'fit_prior': False
                        }

model_evaluation("Multinomial Naïve Bayes", MultinomialNB(), dataset_params=feature_extraction, param_grid=search_grid_options, best_hyperparameters=hyperparameter_values)
