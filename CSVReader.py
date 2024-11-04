import pandas as pd

class CSVReader:
    """
    A class to read and process CSV files using pandas.

    Attributes:
    ----------
    df : pandas.DataFrame
        The dataframe containing the CSV data.

    Methods:
    -------
    get_row_by_index(index):
        Returns a row as a dictionary by its index.
    get_value(index, column_name):
        Returns a specific value from a given row and column.
    get_last_row():
        Returns the last row of the dataframe as a dictionary.
    get_specific_dict_row(number):
        Returns a specific row as a dictionary by its index.
    """

    def __init__(self, file_path):
        """
        Initializes the CSVReader with the path to the CSV file.

        Parameters:
        ----------
        file_path : str
            The path to the CSV file.
        """
        self.df = pd.read_csv(file_path, encoding='latin1')

    def get_row_by_index(self, index):
        """
        Returns a row as a dictionary by its index.

        Parameters:
        ----------
        index : int
            The index of the row to retrieve.

        Returns:
        -------
        dict
            The row data as a dictionary.

        Raises:
        ------
        IndexError
            If the index is out of range.
        """
        if -len(self.df) <= -1-index < len(self.df):
            return self.df.iloc[index].to_dict()
        else:
            raise IndexError("Index out of range.", index)

    def get_value(self, index, column_name):
        """
        Returns a specific value from a given row and column.

        Parameters:
        ----------
        index : int
            The index of the row.
        column_name : str
            The name of the column.

        Returns:
        -------
        object
            The value at the specified row and column.

        Raises:
        ------
        KeyError
            If the column name is not found.
        IndexError
            If the index is out of range.
        """
        if column_name not in self.df.columns:
            raise KeyError(f"Column '{column_name}' not found.")
        if -len(self.df) <= -1-index < len(self.df):
            return self.df.iloc[index][column_name]
        else:
            raise IndexError("Index out of range is ", index)

    def get_last_row(self):
        """
        Returns the last row of the dataframe as a dictionary.

        Returns:
        -------
        dict
            The last row data as a dictionary.
        """
        return self.df.iloc[-1].to_dict()

    def get_specific_dict_row(self, number):
        """
        Returns a specific row as a dictionary by its index.

        Parameters:
        ----------
        number : int
            The index of the row to retrieve.

        Returns:
        -------
        dict
            The row data as a dictionary.
        """
        return self.df.iloc[number].to_dict()


if __name__ == "__main__":
    file_path = 'D:\\workspace\\rx.txt'
    reader = CSVReader(file_path)