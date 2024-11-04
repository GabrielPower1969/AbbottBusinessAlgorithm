# test_main.py
import unittest
from unittest.mock import patch, mock_open
import json
from main import main

class TestMain(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    @patch("os.path.isfile", return_value=True)
    @patch("os.makedirs")
    def test_main_receive_json(self, mock_makedirs, mock_isfile, mock_print, mock_open):
        # 模拟正确的 JSON 参数
        json_args = r'{"inputFilePath": "D:\\workspace\\rx.txt", "outputFilePath": "D:\\workspace\\output.docx", "is_ATL": true, "is_urgent": false, "overwrite_addr": "addr"}'
        args = json.loads(json_args)
        main(args)

        # 验证 main 函数接收到的参数并写入日志文件
        mock_open.assert_called_with("input_log2222.txt", "w")
        mock_open().write.assert_any_call("input_file: D:\\workspace\\rx.txt\n")
        mock_open().write.assert_any_call("output_file: D:\\workspace\\output.docx\n")
        mock_open().write.assert_any_call("is_atl: True\n")
        mock_open().write.assert_any_call("is_urgent: False\n")
        mock_open().write.assert_any_call("overwrite_addr: addr\n")

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_main_json_decode_error(self, mock_print, mock_open):
        # 模拟 JSON 解码错误
        json_args = r'{"inputFilePath": "D:\\workspace\\rx.txt", "outputFilePath": "D:\\workspace\\output.docx", "is_ATL": true, "is_urgent": false, "overwrite_addr": "addr"'

        with self.assertRaises(SystemExit):
            try:
                args = json.loads(json_args)
                main(args)
            except json.JSONDecodeError as e:
                with open("input_log11111.txt", "a") as f:
                    f.write(f"JSONDecodeError: {e}\n")
                    f.write(f"args: {json_args}\n")
                raise SystemExit

        # 验证错误信息写入日志
        mock_open.assert_called_with("input_log11111.txt", "a")
        mock_open().write.assert_any_call("JSONDecodeError: Expecting ',' delimiter: line 1 column 108 (char 107)\n")
        mock_open().write.assert_any_call(f"args: {json_args}\n")

if __name__ == "__main__":
        # 模拟正确的 JSON 参数
        json_args = '{"inputFilePath": "D:\\\\workspace\\\\rx.txt", "outputFilePath": "D:\\\\workspace\\\\output_test.docx", "is_ATL": false, "is_urgent": false, "overwrite_addr": "addr_test_demo", "note": "note_test_demo"}'
        args = json.loads(json_args)
        main(args)