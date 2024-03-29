# -*- coding: utf-8 -*-
from flask import Flask, request,send_file, render_template,jsonify,redirect, url_for
import NLP
import bat_file
app = Flask(__name__)
import re
import getService
# 设置允许的文件扩展名
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

# 检查文件扩展名是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# 自定义安全文件名函数，保留中文字符
def custom_secure_filename(filename):
    # 保留中文字符和数字、字母、下划线
    filename = re.sub(r'[^\w\u4e00-\u9fa5.]', '_', filename)
    return filename
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        hbmxml = ''
        properties = ''
        json = ''
        fileds = []
        filedTypes = []
        chineseMeans = []
        # 获取前端传递的两个字符串参数
        index = 0  # 初始索引
        while True:
            field_key = 'field' + str(index)  # 构建字段名称，例如 'field0', 'field1', ...
            filedType_key = 'filedType' + str(index)
            chineseMean_key = 'chineseMean' + str(index)
            if field_key not in data:
                break  # 如果字段不存在或为空，停止循环

            field = data[field_key].strip()
            filedType = data[filedType_key].strip()  # 假设类型字段名称是 'filedType0', 'filedType1', ...
            modelName = data['modelName'].strip()
            chineseMean = data[chineseMean_key].strip()  # 假设中文字段名称是 'chineseMean0', 'chineseMean1', ...

            length = -1
            if filedType in NLP.global_list and filedType != 'Date' :
                length_key = 'length' + str(index)  # 假设长度字段名称是 'length0', 'length1', ...
                if length_key in data and data[length_key] != '':
                    length = data[length_key].strip()
            fileds.append(field)
            filedTypes.append(filedType)
            chineseMeans.append(chineseMean)
            # 执行你的操作，使用 field, filedType, modelName, chineseMean, length
            hbmxml += NLP.getHbmXml(field, length, filedType,modelName).replace('<', '&lt;').replace('\n', '<br>').replace(' ','&nbsp;')
            properties += NLP.getPropertiesMessage(modelName, field, chineseMean).replace('<', '&lt;').replace('\n','<br>').replace(' ', '&nbsp;')
            json += NLP.getJson(field, length, filedType, modelName).replace('<', '&lt;').replace('\n', '<br>').replace(' ', '&nbsp;')
            index += 1  # 增加索引，处理下一个字段
        javaContent = NLP.get_java_content(fileds, filedTypes, chineseMeans).replace('<', '&lt;').replace('\n','<br>').replace(' ', '&nbsp;')
        formContent = NLP.get_form_content(fileds, filedTypes, chineseMeans).replace('<', '&lt;').replace('\n','<br>').replace(' ', '&nbsp;')
        return jsonify({
            "getMethod": javaContent.rstrip('<br>'),
            "hbmxml": hbmxml.rstrip('>').rstrip('<br'),
            "formMethod": formContent.rstrip('<br>'),
            "properties": properties.rstrip('<br>'),
            "json": json.rstrip('<br>'),
            "message": "Success"
        })  # 返回 JSON 响应
    return render_template('index.html', getMethod=None,hbmxml=None,formMethod=None,properties=None,json=None)

@app.route('/bat', methods=['GET', 'POST'])
def down_bat():
    if request.method == 'POST':
        data = request.get_json()
        hbmxml = ''
        properties = ''
        json = ''
        fileds = []
        filedTypes = []
        chineseMeans = []
        # 获取前端传递的两个字符串参数
        index = 0  # 初始索引
        modelName = data['modelName'].strip()
        while True:
            field_key = 'field' + str(index)  # 构建字段名称，例如 'field0', 'field1', ...
            filedType_key = 'filedType' + str(index)
            chineseMean_key = 'chineseMean' + str(index)
            if field_key not in data:
                break  # 如果字段不存在或为空，停止循环
            field = data[field_key].strip()
            filedType = data[filedType_key].strip()  # 假设类型字段名称是 'filedType0', 'filedType1', ...
            chineseMean = data[chineseMean_key].strip()  # 假设中文字段名称是 'chineseMean0', 'chineseMean1', ...
            length = -1
            if filedType in NLP.global_list and filedType != 'Date' :
                length_key = 'length' + str(index)  # 假设长度字段名称是 'length0', 'length1', ...
                if length_key in data and data[length_key] != '':
                    length = data[length_key].strip()
            # 执行你的操作，使用 field, filedType, modelName, chineseMean, length
            fileds.append(field)
            filedTypes.append(filedType)
            chineseMeans.append(chineseMean)
            hbmxml += NLP.getHbmXml(field, length, filedType,modelName)
            properties += NLP.getPropertiesMessage(modelName, field, chineseMean)
            json += NLP.getJson(field, length, filedType, modelName)
            index += 1  # 增加索引，处理下一个字段

        addr = data['addr'].strip()
        # 将批处理脚本内容写入内存中的文件对象
        java_private =bat_file.getContent(NLP.private_fields_java(fileds,filedTypes))
        form_private =bat_file.getContent(NLP.private_fields_form(fileds,filedTypes))
        java_getset =bat_file.getContent(NLP.public_fields_getset_java(fileds,filedTypes,chineseMeans))
        form_getset =bat_file.getContent(NLP.public_fields_getset_form(fileds,filedTypes,chineseMeans))
        java_obj =bat_file.getContent(NLP.public_fields_obj_java(fileds,filedTypes))
        form_obj =bat_file.getContent(NLP.public_fields_obj_form(fileds,filedTypes))
        form_null =bat_file.getContent(NLP.public_fields_null_form(fileds,filedTypes))
        json_bat_script = bat_file.create_bat_file(hbmxml,json,properties,addr,modelName,java_private,java_getset,java_obj,form_private,form_getset,form_null,form_obj)

        # 将BAT文件保存（名为script.bat）
        with open('script.bat', 'w', encoding='utf-8', newline='\r\n') as file:
            file.write(json_bat_script)


        # 返回BAT文件给前端
        return send_file('script.bat', as_attachment=True)

@app.route('/getService', methods=['GET', 'POST'])
def getServiceCode():
    if request.method == 'POST':
        data = request.get_json()
        name = data['serviceName']
        serviceCode = ''
        if isinstance(name, str) and len(name) > 5:
            serviceCode = getService.get_service_method(name)
            serviceCodeEasy = getService.get_service_method_easy(name)

        return jsonify({
            "serviceCode": serviceCode.replace('<', '&lt;').replace('\n', '<br>').replace(' ', '&nbsp;'),
            "serviceCodeEasy": serviceCodeEasy.replace('<', '&lt;').replace('\n', '<br>').replace(' ', '&nbsp;')
        })
    return render_template('get_service.html', get_service=None)    

if __name__ == '__main__':
    app.run()
