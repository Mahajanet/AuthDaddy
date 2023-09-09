#!/usr/bin/env python3

import json
import pandas as pd
from ml import ml
import math
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
#from sklearn.metrics import mean_absolute_error


class supervised_ml(ml):
    def __init__(self, screen, deg):
        super().__init__(screen)
        self.impute_df(deg)
        self.model = self.supervised_ml()
        
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
        self.df["time"] = self.df['end'] - self.df['start']
        self.df.drop(columns=["start", "end"], inplace=True)
        
        new_rows = []
        
        # Random imputation
        for index, row in self.df.iterrows():
            new_time = row["time"] + random.uniform(-1*math.log(deg+1), math.log(deg+1))
            new_error = row["error"] + random.uniform(-2,2)
            new_rows.append({'time':new_time, 'error':new_error, 'user':1})
        
        self.df = self.df.append(new_rows, ignore_index=True)
        self.df.fillna(0,inplace=True)
        self.df["user"] = self.df["user"].astype(int)
    
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
        target = "user"
        X = self.df.drop(columns=[target], inplace=False)
        y = self.df[target]
        
        # create train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X,y,test_size=0.2,random_state=42
        )
        
        if model.equals("dt"):
            classifier = DecisionTreeClassifier(max_depth=10, random_state=42)
        elif model.equals()
        return (classifier.fit(self.X_train,self.y_train))
    
    def metrics(self):
        mae = self.model.score(self.X_test, self.y_test)
        return mae
    
    def make_prediction(self, file):
        attempt = ml(file)
        attempt.df["time"] = attempt.df['end'] - attempt.df['start']
        attempt.df.drop(columns=["start", "end"], inplace=True)
        attempt.df["error"] = attempt.df["error"].astype(int)

        predictions = self.model.predict(attempt.df)
        return (int(sum(predictions))<3)
    
if __name__ == "__main__":
    mlm = supervised_ml("data.txt", 2)
    print(mlm.make_prediction("data.txt"))