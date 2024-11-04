import pandas as pd
from abbott_common import FINAL_RX_DATA_PATH, PHARMACODE_ORDERTEMPLATE_DICT, HOLDING_FEE, DELIVERY_CHARGE
from MyLogger import logger
from CSVReader import CSVReader


# 1) Information processing purpose ONE: Import and process Special Food order entry data
def read_dataset(filename):
    """Read all available rows of data from a file
    :param filename: The path to the file to be read, typically saved by business software Toniq as 'rx.txt' in 'data' folder
    :return: A list of rows from the file
    """
    infile = open(filename, 'r')
    rows = infile.read().splitlines()
    infile.close()
    
    return rows


def handle_special_conditions(rows):
    """Remove invalid rows which are administration entries, i.e., not order data, and adjust rows for empty entries as required by 
    adding space between empty quotation marks for each row to contain the same amount of data items
    The invalid entries have the reference Pharmacode "99999399", which is a processing fee, while "10000080" is a delivery charge.
    :param rows: The list of all data rows to process
    :return: A list of modified rows with invalid rows removed and empty entries adjusted
    """

    modified_rows = []
    
    for row in rows:
        modified_row = row.replace(",,", ",\"\",") # add space between commas for later spliting
        if str(HOLDING_FEE) in modified_row or str(DELIVERY_CHARGE) in modified_row:
            pass
        else:
            modified_rows.append(modified_row)
    
    return modified_rows

def check_data(modified_rows):
    """Use Pandas to check data shape and description and display outcome message 
    :param modified_rows: The list of modified data rows
    """
    df = pd.DataFrame(modified_rows)
    row_num = df.shape[0]
    unique_rows = df[0].nunique()
    if row_num == unique_rows:
        print("There are no duplicate data, good to go")
    else:
        print("Error: check for duplicate data")


def export_clean_rx_data(modified_row):
    """Save modified rows into a new data file, 'data/final_rx.txt' for further processing 
    :param modified_rows: The list of modified data rows
    """

    outfile = open(FINAL_RX_DATA_PATH, 'w')
    for row in modified_row:
        outfile.write(f"{row}\n")
    outfile.close()

def data_processing(input_file):
    """main function to import data, process data, check for duplicates and then save the clean data to 'data/final_rx.txt'"""
    rows = read_dataset(input_file)
    modified_rows = handle_special_conditions(rows)
    check_data(modified_rows)
    export_clean_rx_data(modified_rows)
    csv_reader = CSVReader(input_file)
    return get_last_avaliable_rows_list(csv_reader)

def get_last_avaliable_rows_list(csv_reader_obj):
    list = []
    patient_name = ""
    for i in range(len(csv_reader_obj.df)):
        row_dict = csv_reader_obj.get_row_by_index(-1-i)
        if row_dict['Pharmacode'] == HOLDING_FEE or row_dict['Pharmacode'] == DELIVERY_CHARGE or row_dict['Pharmacode'] not in PHARMACODE_ORDERTEMPLATE_DICT.keys():
            continue
        else:
            list.append(row_dict)
            patient_name = row_dict['Patient Name']
            Pharmacode = row_dict['Pharmacode']
            try:
                template_name = PHARMACODE_ORDERTEMPLATE_DICT[Pharmacode][0]
            except KeyError:
                logger.warning(f"first get Pharmacode '{Pharmacode}' not found in PHARMACODE_ORDERTEMPLATE_DICT.")
                return []

            while True:
                i += 1
                next_row_index = -1-i
                if -len(csv_reader_obj.df) <= next_row_index < len(csv_reader_obj.df):
                    next_row_Pharmacode = csv_reader_obj.get_value(next_row_index, 'Pharmacode')
                    try:
                        next_row_template_name = PHARMACODE_ORDERTEMPLATE_DICT[next_row_Pharmacode][0]
                    except KeyError:
                        logger.warning(f"Pharmacode '{next_row_Pharmacode}' not found in PHARMACODE_ORDERTEMPLATE_DICT.")
                    if csv_reader_obj.get_value(next_row_index, 'Patient Name') == patient_name and next_row_template_name == template_name:
                        list.append(csv_reader_obj.get_row_by_index(next_row_index))
                        continue
                    else:
                        return list
                else:
                    return list


# For testing purpose only, please run the main function() from 'abbott_app.py'
if __name__ == "__main__":
    """When main is called, the data processing function of this file will be used"""
    last_list = (data_processing("D:\\workspace\\rx.txt"))
    for row in last_list:
        print(row)














