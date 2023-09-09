#!/usr/bin/env python3

from ml.py import ml
import math
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

class supervised_ml(ml):
    
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
        supervised_df = self.impute_df(deg)
        
        # create X and y vectors
        target = "user"
        X = supervised_df.drop(columns=[target])
        y = supervised_df[target]
        
        # create train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X,y,test_size=0.2,random_state=42
        )
        
        classifier = DecisionTreeClassifier(max_depth=10, random_state=42)
        classifier.fit(X,y)
        
    def impute_df(self, deg):
        """

        Parameters
        ----------
        deg : int, the deg difference of the random imputation.

        Returns
        -------
        new df which is the original dataframe with 
        difference of datetime values,
        True user matches and
        False user matches using random data.

        """
        supervised_df = self.df
        supervised_df["time"] = supervised_df['end'] - supervised_df['start']
        supervised_df.drop(columns=["start", "end"], inplace=True)
        
        new_rows = []
        
        # Random imputation
        for index, row in supervised_df.iterrows():
            new_time = row["time"] + random.uniform(-1*math.log(deg+1), math.log(deg+1))
            new_error = row["error"] + random.uniform(-2,2)
            new_rows.append({'time':new_time, 'error':new_error, 'user':1})
        
        supervised_df.append(new_rows, ignore_index=True)
        
        return (
            supervised_df.fillna(0,inplace=True).astype(int)
        )