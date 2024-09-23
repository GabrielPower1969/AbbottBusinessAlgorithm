import os
from common import BASE_DIR

# 数据文件路径
PHARMACODE_ORDERTEMPLATE_DICT_PATH = os.path.join(BASE_DIR, 'data', 'pharmacode_ordertemplate_dict.config')

# 模板文件路径
ORDERFORM_TEMPLATE_SRC = os.path.join(BASE_DIR, 'orderform_template_src')

# 日志配置
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')
FINAL_RX_DATA_PATH = os.path.join(BASE_DIR, 'data', 'final_rx.txt')

# 示例数据
PHARMACODE_ORDERTEMPLATE_DICT = {
    '12345': ['template1.docx', 10, 'Product A', 5],
    '67890': ['template2.docx', 20, 'Product B', 10],
}

# Global fee product code that are to be excluded from data rows in data handling process
HOLDING_FEE = 99999399
DELIVERY_CHARGE = 10000080

def read_template_dict():
    """Read the Abbott product dictionary from Abbott product data file, 'pharmacode_ordertemplate_dict' in the 'data' foler
    This function is called whenever information of an Abbott Special Food product is needed
    :param PHARMACODE_ORDERTEMPLATE_DICT_PATH: The path to the file containing the product dictionary, 'data/pharmacode_ordertemplate_dict.config'
    :return: A dictionary 'PHARMACODE_ORDERTEMPLATE_DICT' mapping product codes to template details
    """
    template_dict = {}

    with open(PHARMACODE_ORDERTEMPLATE_DICT_PATH) as infile:
        rows = infile.read().splitlines()

    for row in rows[1:]:
        items = row.split(',')
        product_code = int(items[0])
        template_path = os.path.join(ORDERFORM_TEMPLATE_SRC, items[1])
        pack_divisor = int(items[2])
        product_name = items[3]
        outer_divisor = int(items[4])
        template_dict[product_code] = (template_path, pack_divisor, product_name, outer_divisor)

    return template_dict

PHARMACODE_ORDERTEMPLATE_DICT = read_template_dict()