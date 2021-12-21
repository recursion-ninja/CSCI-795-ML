'''
Mass testing file that grabs ML models and runs all their predictions for each given value.
Used to compare results to see how different predictions are.
Compares all predicted values for all classifiers, for visual reference.
'''
#Import the main dataset processing stuff
import dataset_transforms as datum
import model_selection as modsel
#Import the models
import model_KNN as KNN
import model_SVM as SVM
import model_LogisticRegression as LRG
import model_NaiveBayes as NB
import model_DecisionTree as DT
import model_RandomForest as RF
import model_NeuralNetwork as NN
import model_XGBoost as XGB

#Tester
def bulk_test_entries():
    #Load PD frames, clean up data, then go through each entry and use it for prediction
    #Predict for each model then print out the results in blocks
    
    #First load the data
    mon_data = datum.retrieve_monster_dataset(tagged_trait = True)
    #Isolate the ELO column specifically.
    #ELO is on the last column.
    X, Y = modsel.seperate_data(mon_data)
    
    #Get the optimal classifiers
    KNN_classifier = KNN.best_classifier()
    SVM_classifier = SVM.best_classifier()
    LRG_classifier = LRG.best_classifier()
    NB_classifier = NB.best_classifier()
    DT_classifier = DT.best_classifier()
    RF_classifier = RF.best_classifier()
    NN_classifier = NN.best_classifier()
    XGB_classifier = KGB.best_classifier()
    
    #Now we do mass testing
    for i in Y:
        print(KNN_classifier.predict(i))
        print(SVM_classifier.predict(i))
        print(LRG_classifier.predict(i))
        print(NB_classifier.predict(i))
        print(DT_classifier.predict(i))
        print(RF_classifier.predict(i))
        print(NN_classifier.predict(i))
        print(XGB_classifier.predict(i))

#test_data = datum.retrieve_monster_dataset(tagged_trait = True)
#print(test_data)
bulk_test_entries()