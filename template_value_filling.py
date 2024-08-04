"""
Gabriel Chen
"""

from datetime import datetime
from data_importing_and_processing import data_processing, read_template_dict
from common import FINAL_RX_DATA_PATH

# Generate Abbott product dictionary 
PHARMACODE_ORDERTEMPLATE_DICT = read_template_dict()

def get_latest_row(filename):
    """
    Get the last row of data from file
    :param filename: The path to the file to be read, typically 'data/final_rx.txt'
    :return: The latest row of data as a string.
    """
    infile = open(filename, 'r')
    rows = infile.read().splitlines()
    infile.close()
   
    latest_row = None
    
    for row in rows[1:]:
        if row.strip() != "":  
            if row != rows[-2]:
                latest_row = row 

    return latest_row


def get_order_template(latest_data):
    """Check if latest row is an Abbott order and get the Abbott order template from Abbott Product Dictionary
    :param latest_data(str): The latest order data
    :return: The path to the order template file, or an empty string if not found
    """

    data = latest_data.split(",")
    target_pharmacode = data[11]

    try:
        product_details = PHARMACODE_ORDERTEMPLATE_DICT[target_pharmacode] 
        template_file = product_details[0]
        return template_file
        
    except KeyError:
        return ""



def get_orderTemplate_data(latest_data):
    """Manipulate data items in latest data row to correct data entry order and to create a patient detail dictionary for 
    filling in the Abbott order form with 2 steps:
    1. Spliting one name data item into two data items, last name and first name. Then invert the order then store in 
        patient detail dictionary 'order_template_data_dict'
    2. Removing empty entries in address strings and concatenate them into one address value in dictionary
    Dictionary structure breakdown: {"name": {First_name, last_name}", "address":"{address1} {address2} {address3} {postcode}"}
    :param latest_data: The latest order data as a string
    :return: A dictionary with keys 'name' and 'address'
    """

    order_template_data_dict = {}

    data = latest_data.replace("\"","").strip().split(",")

    name = f"{data[6]}, {data[5]}"
    address = f"{data[-4]} {data[-3]} {data[-2]} {data[-1]}"
    order_template_data_dict["name"] = name
    order_template_data_dict["address"] = address
    target_pharmacode = data[11]
    order_template_data_dict["pharmacode"] = target_pharmacode
    # to do - get more data from a row - Gabriel
    # rx_number
    # rx_date
    # patient_name
    # patient_nhi
    # qty_x100

    outer_value = int(data[12])
    print("outer_value", outer_value)
    outer_num = None

    try:
        # for pharmacode_str, product_details in PHARMACODE_ORDERTEMPLATE_DICT.items():
        product_details = PHARMACODE_ORDERTEMPLATE_DICT[target_pharmacode] 
        pack_divisor, outer_divisor = product_details[1], product_details[3]
        print("pack_divisor, outer_divisor", pack_divisor, outer_divisor)
        outer_num_float = outer_value/(pack_divisor*outer_divisor)
        outer_num = int(outer_num_float)
        print("outer_num", outer_num)
        order_template_data_dict["outer quantity"] = outer_num
        return order_template_data_dict
        
    except KeyError:
        print(f"Pharmacode {target_pharmacode} not found in PHARMACODE_ORDERTEMPLATE_DICT.")
        return ""




def write_orderTemplate_data(output_template_file, data_dict):
    """Fill in the matching Abbott order template with data from patient details dictionary and store the written file in 
    'printed_orders' folder if data row is an Abbott order. The written file will be saved with time stamp as filename for 
    future reference as required. 
    If the order is not an Abbott product, a reminder message will be printed and programme ends. 
    :param output_template_file: The path to the Abbott order template file in 'orderform_template_src' folder
    :param data_dict: Patient detail dictionary 'order_template_data_dict' that contains'name' and 'address'
    """

    # Check if output_template_file is empty
    if output_template_file == "":
        print("No Abbott product template is available for this order")      
        return
    
    print("Written order template data:")         
    print(output_template_file)                      
    print(data_dict)


    # Read template file and modify content            
    infile = open(output_template_file, 'r')
    lines = infile.read().splitlines()
    infile.close()
    
    # Create a new output file for writing
    written_order_form = "order.txt"  
    outfile = open(written_order_form, 'w')

    for line in lines:
        line = line.strip()
        replacement_string = "__" + str(data_dict['outer quantity']) + "__"
        if line.startswith('Name:'): 
            outfile.write(f"{line} {data_dict['name']}\n")
        elif line.startswith('Address:'):
            outfile.write(f"{line} {data_dict['address']}\n")
        elif line.endswith(data_dict['pharmacode']):
            line = line.replace("_______", replacement_string)
            outfile.write(f"{line}\n")
        else:
            outfile.write(f"{line}\n")  
    
    print(written_order_form)
    outfile.close()

    
    # Read and print the content of the output template file
    with open(written_order_form, 'r') as file:
        print(file.read())


    # Store written_order_form in 'printed_orders' folder 
    new_filename = add_timestamp_to_filename('./printed_orders/rx')+'.txt'
    with open(new_filename, 'w') as new_file:
        with open(written_order_form, 'r') as file:
            for line in file:
                new_file.write(line)


def add_timestamp_to_filename(filename):
    """Add a timestamp to the filename 
    :param filename: The base filename
    :return: The filename with a timestamp appended
    """
    timestamp = datetime.now().strftime('%Y_%m_%d_T%H_%M_%S')
    return f"{filename}_{timestamp}" 

# For testing purpose only, please run the main function() from 'abbott_app.py'
if __name__ == "__main__":
    """This main function performs the first purpose of Abbott Order Management Application, which is to check if the latest 
    Special Food order is an Abbott order. If it is, fill in template value and save the written template file in separate folder 
    'printed_orders' with timestamp filename
    """
    data_processing()
    latest_data = get_latest_row(FINAL_RX_DATA_PATH)
    template_data_dict = get_orderTemplate_data(latest_data) 
    output_template_file = get_order_template(latest_data)
    write_orderTemplate_data(output_template_file, template_data_dict)







