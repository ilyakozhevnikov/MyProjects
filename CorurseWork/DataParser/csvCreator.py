import pandas as pd
import numpy as np


class CSVMaker:
    def __init__(self, categories, data, output):
        self.categories = categories
        self.data = data
        self.output = output
        self.result = {}

    def __fill_flat_data__(self, flat_id):
        flat_dict = {}
        for cat in self.categories:
            flat_dict[cat] = np.nan
        flat_dict["id"] = flat_id
        for datapoint in self.data[flat_id]:
            flat_dict[datapoint[0]] = datapoint[1]

        return flat_dict

    def __fill_dict__(self):
        for cat in self.categories:
            self.result[cat] = []
        for flat_id in self.data.keys():
            flat_data = self.__fill_flat_data__(flat_id)
            for cat in self.result.keys():
                self.result[cat].append(flat_data[cat])

    def get_csv(self):
        self.__fill_dict__()
        df = pd.DataFrame(data=self.result)
        df.to_csv(self.output)
