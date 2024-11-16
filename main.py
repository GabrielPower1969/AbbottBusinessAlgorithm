import os
import sys
import json
from data_processor import DataProcessor
from word_writer import WordWriter
from data_importing_and_processing import data_processing
from MyLogger import logger
from docx import Document

def load_config(args):
    return {
        "INPUT_FILE": args["inputFilePath"],
        "OUTPUT_FILE": args["outputFilePath"],
        "IS_ATL": args["is_ATL"],
        "IS_URGENT": args["is_urgent"],
        "OVERWRITE_ADDR": args["overwrite_addr"],
        "NOTE": args["note"]
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
    logger.info(f"***************** start main *****************\n input_file is {config['INPUT_FILE']}\n output_file is {config['OUTPUT_FILE']}\n is_atl is {config['IS_ATL']}\n is_urgent is {config['IS_URGENT']}\n overwrite_addr is {config['OVERWRITE_ADDR']}\n note is {config['NOTE']}\n")

    validate_input_file(config["INPUT_FILE"])
    ensure_output_path_exists(config['OUTPUT_FILE'])

    templates_data_list = data_processing(config["INPUT_FILE"])
    logger.info(f"last_avaliable_rows_list is \n{templates_data_list}\n")
    logger.info(f"\nlen(last_avaliable_rows_list) is {len(templates_data_list)}\n")

    # Keep track of all generated files
    generated_files = []

    # Process each template and generate Word documents
    for i in range(len(templates_data_list)):
        avaliable_rows_list = templates_data_list[i]
        processor = DataProcessor()
        template_data_dict = processor.get_order_template_data(avaliable_rows_list, config)

        logger.info(f"template_data_dict is {template_data_dict}")
        output_template_file = processor.get_order_template()
        logger.info(f"The obtained txt template is {output_template_file}")

        writer = WordWriter(output_template_file, template_data_dict)

        # Generate output filename
        # Get the file prefix (path + file name has no format)
        file_prefix = os.path.splitext(config['OUTPUT_FILE'])[0]
        print("File Prefix:", file_prefix)
        # Get file suffix (file format)
        file_extension = os.path.splitext(config['OUTPUT_FILE'])[1]
        print("File Extension:", file_extension)

        output_file = config['OUTPUT_FILE'] if i == 0 else f"{file_prefix}_{i}{file_extension}"
        logger.info(f"writer.write_to_word {output_file}")
        writer.write_to_word(output_file)
        generated_files.append(output_file)
        logger.info(f"Generated document {output_file}")

    # Merge all documents if more than one template was processed
    if len(generated_files) > 1:
        logger.info("Merging multiple documents into single file...")
        writer.merge_word_documents(generated_files, config['OUTPUT_FILE'])
        logger.info(f"Successfully merged all documents into {config['OUTPUT_FILE']}")

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