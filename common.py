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


# 模板文件路径
ORDERFORM_TEMPLATE_SRC = os.path.join(BASE_DIR, 'orderform_template_src')

# 日志配置
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')


# 确保必要的目录存在
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
