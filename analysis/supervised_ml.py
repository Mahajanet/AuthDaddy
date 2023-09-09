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
    def __init__(self, screen, deg, model="dt"):
        super().__init__(screen)
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
        for i in range(nchars):
            self.df[f"time{i}"] = self.df[f'end{i}'] - self.df[f'start{i}']
            self.df.drop(columns=[f"start{i}", f"end{i}"], inplace=True)
        
        new_rows = []
        # Random imputation
        for index, row in self.df.iterrows():
            track = {}
            for i in range(nchars):
                track[f'time{i}'] = row[f"time{i}"] + random.uniform(-1*math.log(deg+1), math.log(deg+1))
                track[f'error{i}'] = row[f"error{i}"] + random.uniform(-2,2)
            track['user'] = 1
            new_rows.append(track)
        
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
        elif model.equals("log"):
            classifier = LogisticRegression(max_iter=1000)
        return (classifier.fit(self.X_train,self.y_train))
    
    def metrics(self):
        mae = self.model.score(self.X_test, self.y_test)
        return mae
    
    def make_prediction(self, file):
        attempt = ml(file)
        nchars = attempt.df.shape[1]/3
        for i in range(nchars):
            attempt.df[f"time{i}"] = attempt.df[f'end{i}'] - attempt.df[f'start{i}']
            attempt.df.drop(columns=[f"start{i}", f"end{i}"], inplace=True)
            attempt.df[f"error{i}"] = attempt.df[f"error{i}"].astype(int)

        predictions = self.model.predict(attempt.df)
        return (int(sum(predictions))<3)
    
if __name__ == "__main__":
    mlm = supervised_ml("data.txt", 2)
    print(mlm.make_prediction("data.txt"))