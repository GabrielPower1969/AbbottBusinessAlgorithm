import os
import sys
from common import FINAL_RX_DATA_PATH
from data_processor import DataProcessor
from word_writer import WordWriter
from data_importing_and_processing import data_processing
from MyLogger import logger

def main(input_file, output_file):
    # 确保输入文件存在
    if not os.path.isfile(input_file):
        print(f"Error: The input file '{input_file}' does not exist.")
        sys.exit(1)

    # check output path, if not exit, then create it
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    # 处理数据
    last_avaliable_rows_list = data_processing(input_file)

    # 创建 DataProcessor 实例
    processor = DataProcessor(FINAL_RX_DATA_PATH)

    # 获取最新数据行
    latest_data = processor.get_latest_row()

    # 获取订单模板数据
    # template_data_dict = processor.get_order_template_data(latest_data) # old  should delete

    template_data_dict = processor.get_order_template_data2(last_avaliable_rows_list)
    print(f"processor.get_order_template_data2(last_avaliable_rows_list) is {template_data_dict}")
    logger.info(f"template_data_dict is {template_data_dict}")

    # 获取模板文件路径
    output_template_file = processor.get_order_template(latest_data)
    logger.info(f"获取的txt模板是 is {output_template_file}")

    # 创建 WordWriter 实例并写入Word文档
    # writer = WordWriter(output_template_file, template_data_dict) #old
    writer = WordWriter(output_template_file, template_data_dict)

    writer.write_to_word(output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <inputFilePath> <outputFilePath>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)