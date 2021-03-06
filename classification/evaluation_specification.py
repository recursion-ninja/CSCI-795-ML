'''
Mass testing file that grabs ML models and runs all their predictions for each given value.
Used to compare results to see how different predictions are.
Compares all predicted values for all classifiers, for visual reference.
'''
#Import the main dataset processing stuff
from classifier_specification import model_evaluation
from featureset_specification import TIERS_SET
from copy                     import deepclone
#Import the models
import model_DecisionTree       as  DT
import model_KNN                as KNN
import model_LogisticRegression as LRG
import model_NaiveBayes         as  NB
import model_NeuralNetwork      as ANN
import model_RandomForest       as  RF
import model_SVM                as SVM
import model_XGBoost            as XGB


def generate_all_evaluation_tables():
    
    for tier_size in TIERS_SET:
        print("\n")
        param_list =    [  DT.tier_parameters(tier_size)
                        , KNN.tier_parameters(tier_size)
                        , LRG.tier_parameters(tier_size)
                        ,  NB.tier_parameters(tier_size)
                        , ANN.tier_parameters(tier_size)
                        ,  RF.tier_parameters(tier_size)
                        , SVM.tier_parameters(tier_size)
                        , XGB.tier_parameters(tier_size)
                        ]
        print( "Tier size:\t{}\n\n".format(tier_size) )
        generate_evaluation_table(param_list)

    print("\n")


def generate_evaluation_table(param_list):
    label_index  = 'classifier_label'
    eval_results = []
    for params in param_list:
        params['verbose'] = False
        eval_results.append( ( params, model_evaluation(**params) ) )

    keys_wlog  = eval_results[0][1].keys()
    num_column = len(keys_wlog)
    
    max_column = len(max(keys_wlog , key=lambda keyval: len(keyval)))
    max_label  = len(max(param_list, key=lambda params: len(params[label_index]))[label_index])
    border_str =    (   '|:' + '-' * max_label  + '-'
                    + (('|:' + '-' * max_column + ':') * num_column)
                    +   '|'
                    )
    format_str =    (   '| {:<' + str(max_label)  + '} '
                    + (('| {:^' + str(max_column) + '} ') * num_column)
                    +   '|'
                    )
    
    headers      = deepclone(keys_wlog)
    headers['1'] = ''
    header_str   = format_str.format(headers.values())

    print(header_str)
    print(border_str)
    for params, result in eval_results:
        result[label_index] = params[label_index]
        for key in keys_wlog:
            result[key] = getDecimal(result, key)
        outputs = result.values()
        print( format_str.format(**outputs) )


def getDecimal(d, k):
    double_str = '{:<06}'
    d[k] = double_str.format(d[k])
    return d[k]
    

def main():
    generate_all_evaluation_tables()


if __name__ == "__main__":
    main()
