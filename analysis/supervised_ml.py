#!/usr/bin/env python3

import pandas as pd
from ml import ml
import math
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split



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
    
    def supervised_ml(self, deg=1):
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
        X_train, X_test, y_train, y_test = train_test_split(
            X,y,test_size=0.2,random_state=42
        )
        
        classifier = DecisionTreeClassifier(max_depth=10, random_state=42)
        return (classifier.fit(X,y))
    
if __name__ == "__main__":
    mlm = supervised_ml("data.txt", 2)
    print(mlm.model)