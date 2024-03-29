#通过匹配行插入
def find_matching_line(file_path, target, upordown):
    # 假设replace_single_slash_with_double函数已经定义，用于替换路径中的单斜杠为双斜杠
    file_path = replace_single_slash_with_double(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            line_number = 0
            for line in file:
                line_number += 1
                # 移除line和target中的所有空格，然后进行比较
                if target.replace(" ", "") == line.strip().replace(" ", ""):
                    return line_number + upordown  # 找到第一个匹配行就结束
        print("未找到匹配的行。")
        return None  # 添加返回语句以明确表示没有找到匹配行
    except FileNotFoundError:
        print("文件路径不存在。")
        return None  # 添加返回语句以明确表示文件未找到

def replace_stars(lst):
    result = []
    for i in lst:
        i = i.replace('\n','')  # 删除换行符
        i = i.replace('\t','%zwf%')  # 替换制表符为四个空格
        result.append(i)  # 将处理后的字符串添加到结果列表中
    return result
def find_unique_blank_lines(file_path):
    file_path = replace_single_slash_with_double(file_path)
    unique_blank_lines = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip() == '':
                    unique_blank_lines.add(line)
        if not unique_blank_lines:
            print("未找到任何空白行。")
        return replace_stars(list(unique_blank_lines))
    except FileNotFoundError:
        print("文件路径不存在。")
# 生成排除像
def generate_code(lst):
     # 如果lst是None或者长度为0，则将其定义为['']  
    lst = lst if lst is not None and len(lst) > 0 else [''] 
    code = ""
    if len(lst) == 1:
        code += 'if not "%%b"=="{}" (\n\techo %%b\n) else (\n\techo.{}\n)'.format(lst[0], lst[0])
    else:
        code += 'if not "%%b"=="{}" (\n'.format(lst[0])
        for item in lst[1:]:
            code += '\tif "%%b"=="{}" (\n\t\techo.{}\n\t) else (\n'.format(item, item)
        code += '\t\techo %%b\n'
        code += '\t)\n' * (len(lst)-1)
        code += '\t) else (\n\t\techo.{}\n)'.format(lst[0])
    return code

# 文件地址规范
def replace_single_slash_with_double(file_path):
    # 检查文件路径中是否包含单斜杠
    if '/' in file_path:
        # 使用 replace 方法替换单斜杠为双斜杠
        file_path = file_path.replace('/', '\\\\')
    return file_path

def bat_blank_rep_api(file_string):
    return (generate_code(find_unique_blank_lines(file_string)))




