'''
Mass testing file that grabs ML models and runs all their predictions for each given value.
Used to compare results to see how different predictions are.
Compares all predicted values for all classifiers, for visual reference.
'''
#Import the main dataset processing stuff
import classifier_specification as modsel
import featureset_specification as datum
#Import the models
import model_KNN                as KNN
import model_SVM                as SVM
import model_LogisticRegression as LRG
import model_NaiveBayes         as NB
import model_DecisionTree       as DT
import model_RandomForest       as RF
import model_NeuralNetwork      as NN
import model_XGBoost            as XGB

#Tester
def bulk_test_entries():
    #Load PD frames, clean up data, then go through each entry and use it for prediction
    #Predict for each model then print out the results in blocks
    
    #First load the data
    mon_data = datum.retrieve_monster_dataset(tagged_trait = True)
    
    #Get the optimal classifiers
    KNN_classifier = KNN.best_classifier()
    SVM_classifier = SVM.best_classifier()
    LRG_classifier = LRG.best_classifier()
    NB_classifier  = NB.best_classifier()
    DT_classifier  = DT.best_classifier()
    RF_classifier  = RF.best_classifier()
    NN_classifier  = NN.best_classifier()
    XGB_classifier = XGB.best_classifier()
    
    #Isolate the ELO column specifically.
    #ELO is on the last column.
    X, Y = modsel.seperate_data(mon_data)
    #Train data split for training
    X_full, X_train, X_valid, X_test, Y_full, Y_train, Y_valid, Y_test = modsel.train_valid_test(X, Y, 0.2, 0.2)
    #Train up the different classifiers using optimized results.
    KNN_trained = KNN_classifier.fit(X_full, Y_full)
    SVM_trained = SVM_classifier.fit(X_full, Y_full)
    LRG_trained = LRG_classifier.fit(X_full, Y_full)
    NB_trained = NB_classifier.fit(X_full, Y_full)
    DT_trained = DT_classifier.fit(X_full, Y_full)
    RF_trained = RF_classifier.fit(X_full, Y_full)
    NN_trained = NN_classifier.fit(X_full, Y_full)
    XGB_trained = XGB_classifier.fit(X_full, Y_full)
    
    #Now check it's comparator.
    
    #Now we do mass testing
    for i in range(1, len(Y)):
        print("K Nearest Nbr Predicted Value: ", KNN_trained.predict(X[i]), "\n")
        print("SVM           Predicted Value: ", SVM_trained.predict(X[i]), "\n")
        print("Log Regess    Predicted Value: ", LRG_trained.predict(X[i]), "\n")
        print("Naive Bayes   Predicted Value: ",  NB_trained.predict(X[i]), "\n")
        print("D Tree        Predicted Value: ",  DT_trained.predict(X[i]), "\n")
        print("R Forest      Predicted Value: ",  RF_trained.predict(X[i]), "\n")
        print("Neural Net    Predicted Value: ",  NN_trained.predict(X[i]), "\n")
        print("XGBoost       Predicted Value: ", XGB_trained.predict(X[i]), "\n")
        print("                 Actual Value: ", Y[i], "\n\n")
#test_data = datum.retrieve_monster_dataset(tagged_trait = True)
#print(test_data)
bulk_test_entries()
