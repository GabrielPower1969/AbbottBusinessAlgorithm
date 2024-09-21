分两步：
第一步：直接打包，看看依赖是什么
$ pyinstaller main.spec

************* main.spec begin ****************
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data', 'data'),
        ('orderform_template_src', 'orderform_template_src')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
************* main.spec end ****************

第二步：用命令行，打包“第一步”所有生成了/_internal，把它放到main.py的同级目录下；这里是所有需要的依赖，
打包所有依赖
pyinstaller --onefile --add-data "D:\\workspace\\Abbott\\SpecialFood_0727\\_internal;main/_internal" --add-data "D:\\workspace\\Abbott\\SpecialFood_0727\\orderform_template_src;orderform_template_src" --add-data "D:\\workspace\\Abbott\\SpecialFood_0727\\data;data" main.py


************** 修改 txt模板 配置语法或者添加字段 begin **************
def parse_style(self, style_string):
def apply_style(self, run, style_info):
************** 修改模板配置语法或者添加字段 end **************

************** 提取row data 并新增字段 begin **************
get_order_template_data（）方法中添加字段
************** 提取row data 并新增字段 end **************

************** 测试模板 Begin **************
python .\main.py 'D:\workspace\rx.txt' 'D:\workspace\080413_docx.docx'; Start-Process "winword.exe" -ArgumentList "D:\workspace\080413_docx.docx"
************** 测试模板 end **************



