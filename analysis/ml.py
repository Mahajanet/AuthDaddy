#!/usr/bin/env python3
import json
import pandas as pd


class ml:
    def __init__(self, screen):
        print(screen)
        # initialize dict for df
        self.trials = {}

        # fill matrices for start, end, error
        self.parseJSON(screen)
        #self.df = pd.DataFrame(
        #    {"start": self.start, "end": self.end, "error": self.error})
        self.df = pd.DataFrame(self.trials)

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

        for i in range(len(data)):
            entry = data[i]
            self.trials[f"start{i}"] = []
            self.trials[f"end{i}"] = []
            self.trials[f"error{i}"] = []
            b = 0
            for row in entry:
                if row['key'] == 'b':
                    b += 1
                    self.trials[f"error{i}"][b*-1] += 1
                else:
                    if b == 0:
                        self.trials[f"start{i}"].append(row['timepressed'])
                        self.trials[f"end{i}"].append(row['timereleased'])
                        self.trials[f"error{i}"].append(0)
                    else:
                        self.trials[f"start{i}"][b*-1] = row['timepressed']
                        self.trials[f"end{i}"][b*-1] = row['timereleased']
                        b -= 1


if __name__ == "__main__":
    mlm = ml("data.txt")
    print(mlm.df)