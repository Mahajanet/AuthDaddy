#!/usr/bin/env python3

import pandas as pd
from ml import ml
import simulated
import math
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
#from sklearn.metrics import mean_absolute_error


class supervised_ml(ml):
    def __init__(self, screen, deg, model="dt", import_df=False):
        if not import_df:
            super().__init__(screen)
        else:
            self.df = screen
        self.impute_df(deg)
        self.model = self.supervised_ml(model=model)
        
    def impute_df(self, deg):
        """

        Parameters
        ----------
        deg : int, the deg difference of the random imputation.

        Returns
        -------
        n/a
        
        Modifies
        -------
        df : new df which is the original dataframe with 
        difference of datetime values,
        True user matches and
        False user matches using random data.

        """
        nchars = self.df.shape[1]/3
        for i in range(int(nchars)):
            self.df[f"time{i}"] = self.df[f'end{i}'] - self.df[f'start{i}']
            self.df.drop(columns=[f"start{i}", f"end{i}"], inplace=True)
        
        new_rows = []
        # Random imputation
        for index, row in self.df.iterrows():
            track = {}
            for i in range(int(nchars)):
                track[f'time{i}'] = row[f"time{i}"] + random.uniform(-1*math.log(deg+1), math.log(deg+1))
                track[f'error{i}'] = row[f"error{i}"] + random.uniform(-2,2)
            track['label'] = 1
            new_rows.append(track)
        
        self.df = self.df.append(new_rows, ignore_index=True)
        self.df.fillna(0,inplace=True)
        self.df["label"] = self.df["label"].astype(int)
    
    def supervised_ml(self, deg=1, model="dt"):
        """

        Parameters
        ----------
        deg : int, optional
            the deg difference of the random imputation. The default is 1.

        Returns
        -------
        supervised machine learning model.

        """
        
        # create X and y vectors
        target = "label"
        X = self.df.drop(columns=[target], inplace=False)
        y = self.df[target]
        
        # create train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X,y,test_size=0.2,random_state=42
        )
        
        if model=="dt":
            classifier = DecisionTreeClassifier(max_depth=10, random_state=42)
        elif model=="log":
            classifier = LogisticRegression(max_iter=1000)
        return (classifier.fit(self.X_train,self.y_train))
    
    def metrics(self):
        mae = self.model.score(self.X_test, self.y_test)
        return mae
    
    def opt_decision_tree
    
    def make_prediction(self, file, import_df=False):
        if not import_df:
            attempt = ml(file).df
        else:
            attempt = file
        nchars = attempt.shape[1]/3
        for i in range(int(nchars)):
            attempt[f"time{i}"] = attempt[f'end{i}'] - attempt[f'start{i}']
            attempt.drop(columns=[f"start{i}", f"end{i}"], inplace=True)
            attempt[f"error{i}"] = attempt[f"error{i}"].astype(int)

        predictions = self.model.predict(attempt)
        return predictions
    
if __name__ == "__main__":
    data, test = simulated.simulate_data(10,30,3,10)
    test['label'].replace({'Person': 0, 'Hacker': 1}, inplace=True)
    mlm = supervised_ml(data, 2, import_df=True, model="dt")
    #print(mlm.make_prediction("data.txt"))
    pred = mlm.make_prediction(test.drop(columns='label'),import_df=True)
    test = test['label'].tolist()

    cor = 0
    inc = 0
    for i in range(len(test)):
        if test[i] == pred[i]:
            cor += 1
        else:
            inc += 1
    print(cor)
    print(inc)