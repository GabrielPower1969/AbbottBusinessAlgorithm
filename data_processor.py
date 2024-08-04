from datetime import datetime
from data_importing_and_processing import data_processing, read_template_dict

# Define file path
PHARMACODE_ORDERTEMPLATE_DICT = read_template_dict()

class DataProcessor:
    def __init__(self, filepath):
        self.filepath = filepath

    def get_latest_row(self):
        """
        Get the last row of data from the file.
        :return: The latest row of data as a string.
        """
        with open(self.filepath, 'r') as infile:
            rows = infile.read().splitlines()

        latest_row = None
        for row in rows[1:]:
            if row.strip() != "":
                latest_row = row
        return latest_row

    def get_order_template(self, latest_data):
        """
        Check if the latest row is an Abbott order and get the Abbott order template from the Abbott Product Dictionary.
        :param latest_data: The latest order data as a string.
        :return: The path to the order template file, or an empty string if not found.
        """
        data = latest_data.split(",")
        target_pharmacode = data[11]

        try:
            product_details = PHARMACODE_ORDERTEMPLATE_DICT[target_pharmacode]
            template_file = product_details[0]
            return template_file
        except KeyError:
            return ""

    def get_order_template_data(self, latest_data):
        """
        Manipulate data items in the latest data row to correct data entry order and to create a patient detail dictionary
        for filling in the Abbott order form.
        :param latest_data: The latest order data as a string.
        :return: A dictionary with keys 'name', 'address', 'pharmacode', and 'outer quantity'.
        """
        order_template_data_dict = {}
        data = latest_data.replace("\"", "").strip().split(",")
        name = f"{data[6]}, {data[5]}"
        address = f"{data[-4]} {data[-3]} {data[-2]} {data[-1]}"
        order_template_data_dict["name"] = name
        order_template_data_dict["address"] = address
        target_pharmacode = data[11]
        order_template_data_dict["pharmacode"] = target_pharmacode

        outer_value = int(data[12])
        try:
            product_details = PHARMACODE_ORDERTEMPLATE_DICT[target_pharmacode]
            pack_divisor, outer_divisor = product_details[1], product_details[3]
            outer_num_float = outer_value / (pack_divisor * outer_divisor)
            outer_num = int(outer_num_float)
            order_template_data_dict["outer quantity"] = outer_num
            return order_template_data_dict
        except KeyError:
            print(f"Pharmacode {target_pharmacode} not found in PHARMACODE_ORDERTEMPLATE_DICT.")
            return {}

def add_timestamp_to_filename(filename):
    """
    Add a timestamp to the filename.
    :param filename: The base filename.
    :return: The filename with a timestamp appended.
    """
    timestamp = datetime.now().strftime('%Y_%m_%d_T%H_%M_%S')
    return f"{filename}_{timestamp}"