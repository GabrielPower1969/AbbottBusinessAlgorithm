from datetime import datetime
from data_importing_and_processing import data_processing
from abbott_common import PHARMACODE_ORDERTEMPLATE_DICT
from MyLogger import logger

class DataProcessor:
    def __init__(self):
        self.target_pharmacode = 0

    def get_order_template(self):
        """
        Get the Abbott order template from the Abbott Product Dictionary.
        :return: The path to the order template file, or an empty string if not found.
        """
        try:
            product_details = PHARMACODE_ORDERTEMPLATE_DICT[self.target_pharmacode]
            return product_details[0]
        except KeyError:
            logger.error(f"Pharmacode {self.target_pharmacode} not found in PHARMACODE_ORDERTEMPLATE_DICT.")
            return ""

    def get_order_template_data(self, latest_data_list, config):
        """
        Generate order template data dictionary from the latest data list and config.
        :param latest_data_list: List of latest data rows.

        latest_data_list:
        [
            {'Rx Number': 1997792, 'Rx Date': '05/07/2024 14:28', 'Rx Day': 5, 'Rx Hour': 14, 'Rx Minute': 28, 'Patient Name': 'Boyd, P', 'Patient NHI': 'PCP1245', 'Brand Name': 'ENSURE PLUS', 'Strength': '1.5 kcal/mL banana', 'Form': 'Oral liquid', 'Pharmacode': 234885, 'Qty (x100)': 540000, 'Address1': '80 Bush Street', 'Address2': nan, 'Address3': 'Rangiora', 'Post Code': 7400.0},
            {'Rx Number': 1997791, 'Rx Date': '05/07/2024 14:27', 'Rx Day': 5, 'Rx Hour': 14, 'Rx Minute': 27, 'Patient Name': 'Boyd, P', 'Patient NHI': 'PCP1245', 'Brand Name': 'ENSURE PLUS', 'Strength': '1.5 kcal/mL for fr', 'Form': 'Oral liquid', 'Pharmacode': 234893, 'Qty (x100)': 540000, 'Address1': '80 Bush Street', 'Address2': nan, 'Address3': 'Rangiora', 'Post Code': 7400.0},
            {'Rx Number': 1997790, 'Rx Date': '05/07/2024 14:27', 'Rx Day': 5, 'Rx Hour': 14, 'Rx Minute': 27, 'Patient Name': 'Boyd, P', 'Patient NHI': 'PCP1245', 'Brand Name': 'ENSURE PLUS', 'Strength': '1.5 kcal/mL choc', 'Form': 'Oral liquid', 'Pharmacode': 234680, 'Qty (x100)': 540000, 'Address1': '80 Bush Street', 'Address2': nan, 'Address3': 'Rangiora', 'Post Code': 7400.0},
            {'Rx Number': 1997789, 'Rx Date': '05/07/2024 14:27', 'Rx Day': 5, 'Rx Hour': 14, 'Rx Minute': 27, 'Patient Name': 'Boyd, P', 'Patient NHI': 'PCP1245', 'Brand Name': 'ENSURE PLUS', 'Strength': '1.5 kcal/mL van', 'Form': 'Oral liquid', 'Pharmacode': 234672, 'Qty (x100)': 540000, 'Address1': '80 Bush Street', 'Address2': nan, 'Address3': 'Rangiora', 'Post Code': 7400.0}
        ]

        :param config: Configuration dictionary.
        :return: Order template data dictionary.
        """
        order_template_data_dict = {
            "N_d_selection": "√" if not config["IS_URGENT"] else "□",
            "U_selection": "√" if config["IS_URGENT"] else "□",
            "S_selection": "√" if not config["IS_ATL"] else "□",
            "U_A_selection": "√" if config["IS_ATL"] else "□"
        }

        if latest_data_list:
            data = latest_data_list[0]
            self.target_pharmacode = data['Pharmacode']
            order_template_data_dict.update({
                "name": data['Patient Name'],
                "address": config["OVERWRITE_ADDR"] or f"{data['Address1']} {data['Address2']} {data['Address3']} {data['Post Code']}",
                "pharmacode": data['Pharmacode'],
                "NHI": data['Patient NHI'],
                "Rx Date": data['Rx Date'].split(" ")[0],
                "Note": data['Note'] if isinstance(data['Note'], str) else ""
            })

            for i, row in enumerate(latest_data_list):
                order_template_data_dict.update({
                    f"Rx Number_{i}": row['Rx Number'],
                    f"Qty (x100)_{i}": int(row['Qty (x100)'] / 100)
                })
                try:
                    product_details = PHARMACODE_ORDERTEMPLATE_DICT[self.target_pharmacode]
                    pack_divisor, outer_divisor = product_details[1], product_details[3]
                    order_template_data_dict[str(row['Pharmacode'])] = int(row['Qty (x100)'] / (pack_divisor * outer_divisor))
                except KeyError:
                    logger.error(f"Pharmacode {self.target_pharmacode} not found in PHARMACODE_ORDERTEMPLATE_DICT.")
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