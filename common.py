# common.py

import sys
import os


# 获取项目根目录 -- 适用于 pyinstaller 打包后的项目
def get_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)

    print(f"Base path: {base_path}")
    return base_path

# # 获取项目根目录 -- 适用于 pyinstaller 打包后的项目
# def get_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except AttributeError:
#         base_path = os.path.abspath(".")
#
#     return os.path.normpath(os.path.join(base_path, relative_path))

BASE_DIR = get_path(".")

# # 获取项目根目录
# if getattr(sys, 'frozen', False):
#     BASE_DIR = os.path.dirname(sys.executable)
# else:
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据文件路径
FINAL_RX_DATA_PATH = os.path.join(BASE_DIR, 'data', 'final_rx.txt')
PHARMACODE_ORDERTEMPLATE_DICT_PATH = os.path.join(BASE_DIR, 'data', 'pharmacode_ordertemplate_dict.config')

# 模板文件路径
ORDERFORM_TEMPLATE_SRC = os.path.join(BASE_DIR, 'orderform_template_src')

# 日志配置
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')

# 其他全局常量和配置
PHARMACODE_ORDERTEMPLATE_DICT = {
    # 示例数据
    '12345': ['template1.docx', 10, 'Product A', 5],
    '67890': ['template2.docx', 20, 'Product B', 10],
}

# Global fee product code that are to be excluded from data rows in data handling process
HOLDING_FEE = "99999399"
DELIVERY_CHARGE = "10000080"

# 确保必要的目录存在
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)