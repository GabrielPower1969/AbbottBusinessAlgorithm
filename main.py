import os
import sys
import json
from abbott_common import FINAL_RX_DATA_PATH
from data_processor import DataProcessor
from word_writer import WordWriter
from data_importing_and_processing import data_processing
from MyLogger import logger

def load_config(args):
    return {
        "INPUT_FILE": args["inputFilePath"],
        "OUTPUT_FILE": args["outputFilePath"],
        "IS_ATL": args["is_ATL"],
        "IS_URGENT": args["is_urgent"],
        "OVERWRITE_ADDR": args["overwrite_addr"]
    }

def validate_input_file(input_file):
    if not os.path.isfile(input_file):
        logger.error(f"Error: The input file '{input_file}' does not exist.")
        sys.exit(1)

def ensure_output_path_exists(output_file):
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def main(args):
    config = load_config(args)
    logger.info(f"***************** start main *****************\n input_file is {config['INPUT_FILE']}\n output_file is {config['OUTPUT_FILE']}\n is_atl is {config['IS_ATL']}\n is_urgent is {config['IS_URGENT']}\n overwrite_addr is {config['OVERWRITE_ADDR']}")

    validate_input_file(config["INPUT_FILE"])
    ensure_output_path_exists(config['OUTPUT_FILE'])

    last_avaliable_rows_list = data_processing(config["INPUT_FILE"])
    print(f"last_avaliable_rows_list is {last_avaliable_rows_list}")
    processor = DataProcessor()
    template_data_dict = processor.get_order_template_data(last_avaliable_rows_list, config)

    logger.info(f"template_data_dict is {template_data_dict}")
    output_template_file = processor.get_order_template()
    logger.info(f"The obtained txt template is {output_template_file}")

    writer = WordWriter(output_template_file, template_data_dict)
    writer.write_to_word(config['OUTPUT_FILE'])
    logger.info(f"***************** end main *****************")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <jsonArgs>")
        sys.exit(1)

    with open("input_log0000.txt", "w") as f:
        f.write(f"args: {sys.argv[0]}\n")

    json_args = sys.argv[1]
    try:
        args = json.loads(json_args)
        main(args)
    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError: {e}")
        with open("input_log11111.txt", "a") as f:
            f.write(f"JSONDecodeError: {e}\n")
            f.write(f"args: {json_args}\n")
        sys.exit(1)