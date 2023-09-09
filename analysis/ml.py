#!/usr/bin/env python3
import json
import pandas as pd

class ml:

    def __init__(self, screen):
        # initialize matrices for start, end, error
        self.start = []
        self.end = []
        self.error = []

        # fill matrices for start, end, error
        self.parseJSON(screen)
        self.df = pd.DataFrame(
            {"start": self.start, "end": self.end, "error": self.error})

    def parseJSON(self, screen):
        """

        Parameters
        ----------
        screen : JSON file with rows including key value, 
        start time of pressing the key, 
        end time of pressing the key.

        Returns
        -------
        n/a.

        Modifies
        -------
        start, end, error fields

        """
        with open(screen, "r") as json_file:
            data = json.load(json_file)

        b = 0
        for row in data:
            if row['key'] == 'b':
                b += 1
                self.error[b*-1] += 1
            else:
                if b == 0:
                    self.start.append(row['start'])
                    self.end.append(row['end'])
                else:
                    self.start[b*-1] = row['start']
                    self.start[b*-2] = row['end']