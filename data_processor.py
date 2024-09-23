from datetime import datetime
from data_importing_and_processing import data_processing
from abbott_common import PHARMACODE_ORDERTEMPLATE_DICT
from MyLogger import logger


class DataProcessor:
    def __init__(self, ):
        self.target_pharmacode = 0

    def get_order_template(self):
        """
        Check if the latest row is an Abbott order and get the Abbott order template from the Abbott Product Dictionary.
        :param latest_data: The latest order data as a string.
        :return: The path to the order template file, or an empty string if not found.
        """
        print("target_pharmacode: ", self.target_pharmacode)

        try:
            product_details = PHARMACODE_ORDERTEMPLATE_DICT[self.target_pharmacode]
            template_file = product_details[0]
            return template_file
        except KeyError:
            print(f"Pharmacode {self.target_pharmacode} not found in PHARMACODE_ORDERTEMPLATE_DICT.")
            raise KeyError(f"Pharmacode {self.target_pharmacode} not found in PHARMACODE_ORDERTEMPLATE_DICT.")
            return ""

    def get_order_template_data(self, latest_data_list, config):
        '''
        input:[
            {'Rx Number': 1997792, 'Rx Date': '05/07/2024 14:28', 'Rx Day': 5, 'Rx Hour': 14, 'Rx Minute': 28, 'Patient Name': 'Boyd, P', 'Patient NHI': 'PCP1245', 'Brand Name': 'ENSURE PLUS', 'Strength': '1.5 kcal/mL banana', 'Form': 'Oral liquid', 'Pharmacode': 234885, 'Qty (x100)': 540000, 'Address1': '80 Bush Street', 'Address2': nan, 'Address3': 'Rangiora', 'Post Code': 7400.0},
            {'Rx Number': 1997791, 'Rx Date': '05/07/2024 14:27', 'Rx Day': 5, 'Rx Hour': 14, 'Rx Minute': 27, 'Patient Name': 'Boyd, P', 'Patient NHI': 'PCP1245', 'Brand Name': 'ENSURE PLUS', 'Strength': '1.5 kcal/mL for fr', 'Form': 'Oral liquid', 'Pharmacode': 234893, 'Qty (x100)': 540000, 'Address1': '80 Bush Street', 'Address2': nan, 'Address3': 'Rangiora', 'Post Code': 7400.0},
            {'Rx Number': 1997790, 'Rx Date': '05/07/2024 14:27', 'Rx Day': 5, 'Rx Hour': 14, 'Rx Minute': 27, 'Patient Name': 'Boyd, P', 'Patient NHI': 'PCP1245', 'Brand Name': 'ENSURE PLUS', 'Strength': '1.5 kcal/mL choc', 'Form': 'Oral liquid', 'Pharmacode': 234680, 'Qty (x100)': 540000, 'Address1': '80 Bush Street', 'Address2': nan, 'Address3': 'Rangiora', 'Post Code': 7400.0},
            {'Rx Number': 1997789, 'Rx Date': '05/07/2024 14:27', 'Rx Day': 5, 'Rx Hour': 14, 'Rx Minute': 27, 'Patient Name': 'Boyd, P', 'Patient NHI': 'PCP1245', 'Brand Name': 'ENSURE PLUS', 'Strength': '1.5 kcal/mL van', 'Form': 'Oral liquid', 'Pharmacode': 234672, 'Qty (x100)': 540000, 'Address1': '80 Bush Street', 'Address2': nan, 'Address3': 'Rangiora', 'Post Code': 7400.0}
        ]
        '''
        order_template_data_dict = {}
        #□Normal delivery / □Urgent
        order_template_data_dict["N_d_selection"] = "□"
        order_template_data_dict["U_selection"] = "□"
        if config["IS_URGENT"]:
            order_template_data_dict["U_selection"] = "√"
        else:
            order_template_data_dict["N_d_selection"] = "√"

            #□Standard / □Urgent_ATL
        order_template_data_dict["S_selection"] = "□"
        order_template_data_dict["U_A_selection"] = "□"
        if config["IS_ATL"]:
            order_template_data_dict["U_A_selection"] = "√"
        else:
            order_template_data_dict["S_selection"] = "√"

        # Multi-lines status
        if len(latest_data_list) > 0:
            # template general information
            data = latest_data_list[0]
            target_pharmacode = data['Pharmacode']
            self.target_pharmacode = target_pharmacode
            order_template_data_dict["name"] = f"{data['Patient Name']}"
            if config["OVERWRITE_ADDR"] != "":
                order_template_data_dict["address"] = config["OVERWRITE_ADDR"]
            else:
                order_template_data_dict["address"] = f"{data['Address1']} {data['Address2']} {data['Address3']} {data['Post Code']}"

            order_template_data_dict["pharmacode"] = target_pharmacode
            order_template_data_dict["NHI"] = data['Patient NHI']
            order_template_data_dict["Rx Date"] = data['Rx Date'].split(" ")[0]

            # template customised information
            for i in range(len(latest_data_list)):
                row = latest_data_list[i]
                order_template_data_dict[f"Rx Number_{i}"] = row['Rx Number']
                order_template_data_dict[f"Qty (x100)_{i}"] = int(row['Qty (x100)']/100)
                #if row['Note'] str? yes, str else do nothing
                if isinstance(row['Note'], str):
                    order_template_data_dict["Note"] = row['Note']
                print(f"Note: {row['Note']}")
                try:
                    product_details = PHARMACODE_ORDERTEMPLATE_DICT[target_pharmacode]
                    pack_divisor, outer_divisor = product_details[1], product_details[3]
                    order_template_data_dict[str(row['Pharmacode'])] = int(row['Qty (x100)'] / (pack_divisor * outer_divisor)) # 540000 / (14 * 28)
                except KeyError:
                    print(f"Pharmacode {target_pharmacode} not found in PHARMACODE_ORDERTEMPLATE_DICT.")
                    return {}
        return order_template_data_dict

def add_timestamp_to_filename(filename):
    """
    Add a timestamp to the filename.
    :param filename: The base filename.
    :return: The filename with a timestamp appended.
    """
    timestamp = datetime.now().strftime('%Y_%m_%d_T%H_%M_%S')
    return f"{filename}_{timestamp}"