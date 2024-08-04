import pandas as pd
from common import FINAL_RX_DATA_PATH, PHARMACODE_ORDERTEMPLATE_DICT_PATH, HOLDING_FEE, DELIVERY_CHARGE, ORDERFORM_TEMPLATE_SRC


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
        if HOLDING_FEE in modified_row or DELIVERY_CHARGE in modified_row:
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

# 2) Information processing purpose TWO: Read Abbott brand Special Food products dictionary 
def read_template_dict():
    """Read the Abbott product dictionary from Abbott product data file, 'pharmacode_ordertemplate_dict' in the 'data' foler
    This function is called whenever information of an Abbott Special Food product is needed 
    :param PHARMACODE_ORDERTEMPLATE_DICT_PATH: The path to the file containing the product dictionary, 'data/pharmacode_ordertemplate_dict.config'
    :return: A dictionary 'PHARMACODE_ORDERTEMPLATE_DICT' mapping product codes to template details
    """

    PHARMACODE_ORDERTEMPLATE_DICT = {}
    
    infile = open(PHARMACODE_ORDERTEMPLATE_DICT_PATH)
    rows = infile.read().splitlines()
    infile.close()

    index = 1
    while index < len(rows):
        items = rows[index].split(',')
        product_code = items[0]
        # 拼接模板文件绝对路径
        template_path = f"{ORDERFORM_TEMPLATE_SRC}/{items[1]}"
        pack_divisor = int(items[2])
        product_name = items[3]
        outer_divisor = int(items[4])
        PHARMACODE_ORDERTEMPLATE_DICT[product_code] = (template_path, pack_divisor, product_name, outer_divisor)
        index += 1

    return PHARMACODE_ORDERTEMPLATE_DICT

# For testing purpose only, please run the main function() from 'abbott_app.py'
if __name__ == "__main__":
    """When main is called, the data processing function of this file will be used"""
    data_processing()














