import re

# 在模块级别定义全局基础属性类型
global_list = ["String", "Boolean", "Integer", "Double", "Date"]


# 属性名得到字段名
def camel_to_snake(name):
    # 使用正则表达式将驼峰式命名转换为下划线风格
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()

def private_fields_java(fields, field_types):
    result = ''
    i = 0
    for field in fields:
        result += f"\n    private {field_types[i]} {field};\n"
        i += 1
    return result

def private_fields_form(fields,field_types):
    result = ''
    i = 0
    for field in fields:
        content = ''
        if field_types[i] in global_list:
            content += f"\n    private String {field};\n"
        else:
            content += f"\n    private String {field}Id;\n"
            content += f"\n    private String {field}Name;\n"
            if 'List' in field_types[i]:
                content = content.replace('Id', 'Ids').replace('Name', 'Names')
        i += 1
        result += content
    return result

def public_fields_getset_java(fields,field_types,chinese_means):
    result = ''
    i = 0
    for field in fields:
        result += f'\n    /**\n    * {chinese_means[i]}\n    */\n    '
        result += f"public {field_types[i]} get{field[0].upper()}{field[1:]}() {{\n" \
              f"        return this.{field};\n" \
                  f"    }}\n"
        result += f'\n    /**\n    * {chinese_means[i]}\n    */\n    '
        result += f"public void set{field[0].upper()}{field[1:]}({field_types[i]} {field}) {{\n" \
                         f"        this.{field} = {field};\n" \
                         f"    }}\n"
        i +=1
    return result

def public_fields_getset_form(fields,field_types,chinese_means):
    result = ''
    i = 0
    for field in fields:
        content = ''
        if field_types[i] in global_list:
            if field_types[i] == 'Double':
                content += f'\n    /**\n    * {chinese_means[i]}\n    */\n    '
                content += f"public String get{field[0].upper()}{field[1:]}() {{\n" \
                          f"        if(StringUtil.isNull(this.{field})){{\n" \
                          f"            return this.{field};\n" \
                          f"        }}\n" \
                          f"        return new DecimalFormat(\"0.0#\").format(Double.valueOf(this.{field}));\n" \
                          f"    }}\n"
            else:
                content += f'\n    /**\n    * {chinese_means[i]}\n    */\n    '
                content += f"public String get{field[0].upper()}{field[1:]}() {{\n" \
                          f"        return this.{field};\n" \
                          f"    }}\n"
            content += f'\n    /**\n    * {chinese_means[i]}\n    */\n    '
            content += f"public void set{field[0].upper()}{field[1:]}(String {field}) {{\n" \
                      f"        this.{field} = {field};\n" \
                      f"    }}\n"
        else:
            content += f'\n    /**\n    * {chinese_means[i]}\n    */\n    '
            content += f"public String get{field[0].upper()}{field[1:]}Id() {{\n" \
                      f"        return this.{field}Id;\n" \
                      f"    }}\n"
            content += f'\n    /**\n    * {chinese_means[i]}\n    */\n    '
            content += f"public void set{field[0].upper()}{field[1:]}Id(String {field}Id){{\n" \
                      f"        this.{field}Id = {field}Id;\n" \
                      f"    }}\n"
            content += f'\n    /**\n    * {chinese_means[i]}\n    */\n    '
            content += f"public String get{field[0].upper()}{field[1:]}Name() {{\n" \
                      f"        return this.{field}Name;\n" \
                      f"    }}\n"
            content += f'\n    /**\n    * {chinese_means[i]}\n    */\n    '
            content += f"public void set{field[0].upper()}{field[1:]}Name(String {field}Name){{\n" \
                      f"        this.{field}Name = {field}Name;\n" \
                      f"    }}\n"
            if 'List' in field_types[i]:
                content = content.replace('Id', 'Ids').replace('Name', 'Names')
        i += 1
        result += content
    return result

def public_fields_null_form(fields,field_types):
    result = ''
    i = 0
    for field in fields:
        if field_types[i] in global_list:
            result += f'        {field} = null;\n'
        else:
            result += f'        {field}Id = null;\n' \
                      f'        {field}Name = null;\n'
            if 'List' in field_types[i]:
                result = result.replace('Id', 'Ids').replace('Name', 'Names')
        i +=1
    return result

def public_fields_obj_java(fields,field_types):
    result = ''
    i = 0
    for field in fields:
        content = ''
        if field_types[i] not in global_list:
            if 'List' in field_types[i]:
                content += f'            toFormPropertyMap.put("{field}", new ModelConvertor_ModelListToString("{field}Ids:{field}Names", "fdId:fdName"));\n'
            else:
                content += f'            toFormPropertyMap.put("{field}.fdId", "{field}Id");\n' \
                                 f'            toFormPropertyMap.put("{field}.fdName", "{field}Name");\n'
        elif 'Date' == field_types[i]:
            content += f'            toFormPropertyMap.put("{field}", new ModelConvertor_Common("{field}").setDateTimeType(DateUtil.TYPE_DATE));\n'
        i +=1
        result += content
    return result

def public_fields_obj_form(fields,field_types):
    result = ''
    i = 0
    for field in fields:
        if field_types[i] in global_list:
            if 'Date' == field_types[i]:
                result += f'            toModelPropertyMap.put("{field}", new FormConvertor_Common("{field}").setDateTimeType(DateUtil.TYPE_DATE));\n'
        else:
            result += f'            toModelPropertyMap.put("{field}Id", new FormConvertor_IDToModel("{field}", {field_types[i]}.class));\n'
        if 'List' in field_types[i]:
            result = result.replace('Id', 'Ids').replace('Name', 'Names').replace('IDToModel','IDsToModelList').replace('List<', '').replace('>', '')
        i += 1
    return result

def get_java_content(fields, field_types,chinese_means):
    result = private_fields_java(fields,field_types)+public_fields_getset_java(fields,field_types,chinese_means)+public_fields_obj_java(fields,field_types)
    return result

def get_form_content(fields,field_types,chinese_means):
    result = private_fields_form(fields,field_types)+public_fields_getset_form(fields,field_types,chinese_means)+public_fields_null_form(fields,field_types)+public_fields_obj_form(fields,field_types)
    return result


def generate_class_name(input_str):
    # 如果输入字符串为空或不包含字母，则直接返回输入字符串
    if not input_str or not any(c.isalpha() for c in input_str):
        return input_str

    # 查找<>之间的内容
    match = re.search(r'<(.*?)>', input_str)
    if match:
        between_angle_brackets = match.group(1).strip()
    else:
        between_angle_brackets = input_str

    # 规范类名，首字母小写改大写
    between_angle_brackets = between_angle_brackets[0].upper() + between_angle_brackets[1:]

    # 拆解类
    firtPart = re.findall(r'[A-Za-z][a-z]*', between_angle_brackets)[0].lower()
    secondPart = re.findall(r'[A-Za-z][a-z]*', between_angle_brackets)[1].lower()

    # 特殊情况
    if secondPart == "org":
        secondPart = "organization"

    # 构建最终字符串
    result = f"com.landray.kmss.{firtPart}.{secondPart}.model.{between_angle_brackets}"
    return result


# hbm文件
def getHbmXml(field_name, length, filedType, modelName):
    if 'List' in filedType:
        tableName = camel_to_snake(modelName) + '_' + match_last_uppercase(
            re.search(r'<(.*?)>', filedType).group(1).strip()) + match_last_uppercase(field_name)
        xml_element = '        <bag\n'
        xml_element += f'            name="{field_name}"\n'
        xml_element += f'            table="' + tableName + f'"'
        xml_element += '''
            lazy="true">
            <key
                column="fd_source_id"/>
            <many-to-many
    '''
        xml_element += '                class="' + generate_class_name(filedType) + '"'
        xml_element += '''
                column="fd_target_id"/>
        </bag>\n'''
        return xml_element
    column_name = camel_to_snake(field_name)
    # 生成不同类型的元素
    if filedType not in global_list:
        column_name += "_id"
        xml_element = f'        <many-to-one\n'  # "\"表示多行字符串，可要可不要的，但是这里不能加，不能后面接else
    else:
        xml_element = f'        <property\n'

    xml_element += f'            name="{field_name}"\n' \
                   f'            column="{column_name}"\n' \
                   f'            update="true"\n' \
                   f'            insert="true"'
    if length != -1:
        xml_element += f'\n            length="{length}"'
    xml_element += '/>'
    return xml_element + "\n"


# 得到pro文件地址
def getProKey(mainModel):
    # 使用正则表达式将参数中的前两个驼峰单词提取出来，并转换为小写字母
    words = re.findall(r'[A-Za-z][a-z]*', mainModel)[:2]
    # 使用连字符 "-" 连接单词，并返回格式化后的字符串
    return '-'.join(words).lower()


# 生成json文件
def getJson(fild, length, filedType, modelName):
    json_element = f'        "{fild}"  :   {{\n'
    messageKey = f'            "messageKey": "' + getProKey(
        modelName) + f':{modelName[0].lower() + modelName[1:]}.{fild}",\n'
    if 'List' in filedType:
        tableName = camel_to_snake(modelName) + '_' + match_last_uppercase(
            re.search(r'<(.*?)>', filedType).group(1).strip()) + match_last_uppercase(fild)
        json_element += f'            "propertyType": "list",\n'
        json_element += messageKey
        json_element += f'            "type": "' + generate_class_name(filedType) + f'",\n'
        json_element += f'            "table" : "' + tableName + '",'
        json_element += '''
            "elementColumn" : "fd_target_id",
            "column" : "fd_source_id",
            "notNull" : "false",
            "readOnly" : "false",
            "validate" : "true",
            "canDisplay" : "true",
            "canRelation" : "true",
            "canSearch" : "true"'''
        if 'Sys' in filedType:
            json_element += f',\n            "dialogJS" : "Dialog_Address(!{{mulSelect}}, \'!{{idField}}\',\'!{{nameField}}\', \';\',ORG_TYPE_ALL);"'
        json_element += '\n        },\n'
        return json_element
    column_name = camel_to_snake(fild)
    if filedType in global_list:
        json_element += f'            "propertyType": "simple",\n'
    else:
        json_element += f'            "propertyType": "model",\n'
    json_element += messageKey
    if filedType in global_list:
        json_element += f'            "type": "{filedType}",\n'
    else:
        json_element += f'            "type": "' + generate_class_name(filedType) + f'",\n'
        column_name += "_id"
    json_element += f'            "column": "{column_name}",\n' \
                    f'            "notNull": "false",\n' \
                    f'            "readOnly": "false",\n' \
                    f'            "validate": "true",\n' \
                    f'            "canDisplay": "true",\n' \
                    f'            "canRelation": "true",\n' \
                    f'            "canSearch" : "true"'
    if length != -1:
        json_element += f',\n            "length": "{length}"'
    json_element += '\n        },'
    return json_element + "\n"


def getPropertiesMessage(modelName, field, chineseMean):
    # 首字母大写改小写
    modelName = modelName[0].lower() + modelName[1:]
    return modelName + '.' + field + '=' + chineseMean + "\n"

def getPropertiesUnicode(modelName, field, chineseMean):
    unicode_escape_string = chineseMean.encode('unicode_escape').decode('utf-8')
    # 首字母大写改小写
    modelName = modelName[0].lower() + modelName[1:]
    return modelName + '.' + field + '=' + unicode_escape_string + "\n"


def match_last_uppercase(input_str):
    # 找到字符串中最后一个大写字母的索引
    last_uppercase_index = None
    for i in range(len(input_str) - 1, -1, -1):
        if input_str[i].isupper():
            last_uppercase_index = i
            break

    # 如果找到了最后一个大写字母
    if last_uppercase_index is not None:
        # 提取最后一个大写字母开始的三个字符，并转换为小写形式
        result = input_str[last_uppercase_index:last_uppercase_index + 3].lower()
        return result
    else:
        return None
