import re
import os
import NLP


# 字符串生成对应echo
def generate_echo_statements(input_string):
    lines = input_string.split('\n')  # 将输入字符串按行分割成列表
    echo_statements = []  # 用于存储生成的echo语句

    for line in lines:
        if line.strip() == "":
            echo_statement = '            echo.'
        else:
            echo_statement = '            echo ' + line
        echo_statements.append(echo_statement)

    # 将生成的echo语句列表合并为一个字符串，并用换行符分隔
    result = '\n'.join(echo_statements)
    if result.strip() == "echo.":
        return ""
    return result


def getContent(str):
    # 检查字符串末尾是否包含换行符
    if str.endswith('\n'):
        # 去掉末尾的换行符
        str = str.rstrip('\n')
    text = generate_echo_statements(str).replace('(', '^(').replace(')', '^)').replace('"', '^"').replace('<',
                                                                                                          "^<").replace(
        '>', '^>')
    return text


def create_bat_file(hbmxml, json, properties, addr, modelName, java_private, java_getset, java_obj, form_private,
                    form_getset, form_null, form_obj):
    # 创建一个空字典
    my_dict = {}
    content_dict = {"hbm": hbmxml, 'json': json, 'properties': properties}
    serch_dict = {"hbm": '            length="36"/>', 'json': '        },',
                  'properties': '#table ' + NLP.camel_to_snake(modelName)}
    # 遍历键并为每个键放入值
    keys = ['hbm', 'json', 'properties']  # 你的键列表
    for key in keys:
        file_addr = get_file_addr(addr, modelName, key)
        serchLine = serch_dict[key]
        content = getContent(content_dict[key])
        my_dict[key] = [file_addr, serchLine, content]
    # 构建批处理脚本内容，使用获取的参数
    batch_script = f'''@echo off
chcp 65001 >nul 2>&1

setlocal disabledelayedexpansion'''
    for key, values in my_dict.items():
        batch_script += f'''
set "{key}File={values[0]}"
set "{key}SearchLine={values[1]}"
set "{key}TempFile=%temp%\{key}TempFile.txt"
set "{key}Inserted="

(for /f "tokens=1,* delims=:" %%a in ('findstr /n "^" "%{key}File%"')do (
    if not "%%b"=="" (
        echo %%b
    ) else (
        echo.
    ) 
    if "%%b"=="%{key}SearchLine%" (
        if not defined {key}Inserted (
{values[2]}
            set "{key}Inserted=true"
        )
    )
)) > %{key}TempFile%

copy /y %{key}TempFile% %{key}File% >nul
del %{key}TempFile%

if not "%{key}Inserted%"=="true" (
    echo {key}文件插入失败。未找到目标行！请手动插入
)'''
    java_addr = get_file_addr(addr, modelName, 'java')
    form_addr = get_file_addr(addr, modelName, 'form')
    batch_script += get_java_and_form_bat(java_addr, java_private, java_getset, java_obj, form_addr, form_private,
                                          form_getset, form_null, form_obj)
    batch_script += '\npause'
    return batch_script


def get_file_addr(base_path, model_name, file_type):
    # 使用正则表达式将参数中的前两个驼峰单词提取出来，并转换为小写字母
    words = re.findall(r'[A-Za-z][a-z]*', model_name)[:2]
    words_path = os.path.join(*words).lower()

    if file_type == 'json':
        base_path = base_path.replace('src', '')
        file_path = os.path.join(base_path, 'WebContent', 'WEB-INF', 'KmssConfig', words_path, 'data-dict',
                                 f'{model_name}.json')
    elif file_type == 'java':
        file_path = os.path.join(base_path, 'com', 'landray', 'kmss', words_path, 'model', f'{model_name}.java')
    elif file_type == 'form':
        file_path = os.path.join(base_path, 'com', 'landray', 'kmss', words_path, 'forms', f'{model_name}Form.java')
    elif file_type == 'hbm':
        file_path = os.path.join(base_path, 'com', 'landray', 'kmss', words_path, 'model', f'{model_name}.hbm.xml')
    elif file_type == 'properties':
        file_path = os.path.join(base_path, 'com', 'landray', 'kmss', words_path, 'ApplicationResources.properties')
    else:
        raise ValueError("Invalid file type")
    file_path = file_path.replace('/', '\\')
    return file_path


def get_java_and_form_bat(java_addr, java_private, java_getset, java_obj, form_addr, form_private, form_getset,
                          form_null, form_obj):
    return f'''
set "javaFile={java_addr}"
set "javaSearchLine1=    private static ModelToFormPropertyMap toFormPropertyMap;"
set "javaSearchLine2=    }}"
set "javaSearchLine3=            toFormPropertyMap = new ModelToFormPropertyMap();"
set "javaTempFile=%temp%\javaTempFile.txt"
set "javaInserted1="
set "javaInserted2="
set "javaInserted3="

(for /f "tokens=1,* delims=:" %%a in ('findstr /n "^" "%javaFile%"')do (
	if "%%b"=="    " (
		echo.    
	)else if "%%b"=="	" (
		echo.	
	)else if "%%b"=="   " (
		echo.   
	)else if "%%b"=="" (
		echo.
	)else (
		echo %%b
	)
    if "%%b"=="%javaSearchLine1%" (
        if not defined javaInserted1 (
{java_private}
            set "javaInserted1=true"
        )
    )else if "%%b"=="%javaSearchLine2%" (
        if not defined javaInserted2 (  
{java_getset}
            set "javaInserted2=true"
        )
    )else if "%%b"=="%javaSearchLine3%" (
        if not defined javaInserted3 (    
{java_obj}
            set "javaInserted3=true"
        )
    )
)) > %javaTempFile%

copy /y %javaTempFile% %javaFile% >nul
del %javaTempFile%

if not "%javaInserted1%"=="true" (
    echo java文件 private部分插入失败。未找到目标行！请手动插入!
)
if not "%javaInserted2%"=="true" (
    echo java文件 getset方法插入失败。未找到目标行！请手动插入!
)
if not "%javaInserted3%"=="true" (
    echo java文件 toFormPropertyMap部分插入失败。未找到目标行！请手动插入!
)

set "formFile={form_addr}"
set "formSearchLine1=    private static FormToModelPropertyMap toModelPropertyMap;"
set "formSearchLine2=    }}"
set "formSearchLine3=    public void reset(ActionMapping mapping, HttpServletRequest request) {{"
set "formSearchLine4=            toModelPropertyMap = new FormToModelPropertyMap();"
set "formTempFile=%temp%\\formTempFile.txt"
set "formInserted1="
set "formInserted2="
set "formInserted3="
set "formInserted4="

(for /f "tokens=1,* delims=:" %%a in ('findstr /n "^" "%formFile%"')do (
	if "%%b"=="    " (
		echo.    
	)else if "%%b"=="	" (
		echo.	
	)else if "%%b"=="   " (
		echo.   
	)else if "%%b"=="" (
		echo.
	)else (
		echo %%b
	)
    if "%%b"=="%formSearchLine1%" (
        if not defined formInserted1 (  
{form_private}
            set "formInserted1=true"
        )
    )else if "%%b"=="%formSearchLine2%" (
        if not defined formInserted2 ( 
{form_getset}
            set "formInserted2=true"
        )
    )else if "%%b"=="%formSearchLine3%" (
        if not defined formInserted3 (   
{form_null}
            set "formInserted3=true"
        )
    )else if "%%b"=="%formSearchLine4%" (
        if not defined formInserted4 (   
{form_obj}
            set "formInserted4=true"
        )
    )
)) > %formTempFile%

copy /y %formTempFile% %formFile% >nul
del %formTempFile%

if not "%formInserted1%"=="true" (
    echo form文件 private 部分插入失败。未找到目标行！请手动插入
)
if not "%formInserted2%"=="true" (
    echo form文件 getset 部分插入失败。未找到目标行！请手动插入
)
if not "%formInserted3%"=="true" (
    echo form文件 =null部分插入失败。未找到目标行！请手动插入
)
if not "%formInserted4%"=="true" (
    echo form文件 toModelPropertyMap部分插入失败。未找到目标行！请手动插入
)
echo 没闪退,没提示插入失败的话，那就是插入成功了！
'''
