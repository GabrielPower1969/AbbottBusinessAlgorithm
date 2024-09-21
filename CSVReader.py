import pandas as pd
from abbott_common import HOLDING_FEE, DELIVERY_CHARGE
import warnings
from MyLogger import logger

class CSVReader:
    '''

    '''
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    def get_row_by_index(self, index):
        if -len(self.df) <= -1-index < len(self.df):
            return self.df.iloc[index].to_dict()
        else:
            raise IndexError("Index out of range.", index)

    def get_value(self, index, column_name):
        if column_name not in self.df.columns:
            raise KeyError(f"Column '{column_name}' not found.")
        if -len(self.df) <= -1-index < len(self.df):
            return self.df.iloc[index][column_name]
        else:
            raise IndexError("Index out of range is ", index)

    def get_last_row(self):
        return self.df.iloc[-1].to_dict()

    def get_specific_dict_row(self, number):
        return self.df.iloc[number].to_dict()


if __name__ == "__main__":
    file_path = 'D:\\workspace\\rx.txt'
    reader = CSVReader(file_path)