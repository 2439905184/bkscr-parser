# 基于正则表达式的多行宏函数的词法分析器
import re
# 检查是否有注释
def checkHasComment(code)->bool:
    bufferString = ""
    for char in code:
        bufferString += char
    if bufferString == "//":
        return True
    else:
        return False

# 返回去除掉注释字符串的干净代码
def deleteComment(code)->str:
    #匹配模式：多个空格//后面的所有字符内容 除了\n换行符
    regex = r"\s+//[^\n]*"
    result = re.sub(regex,"",code)
    return result

# 预处理数组里面的空格
def preProcessArray(code)->str:
    # 匹配[后面的所有空格 或者,前面的所有空格 或者，后面的所有空格 或者]前面的所有空格并替换为""
    regex = r"(?<=\[)\s+|\s+(?=,)|(?<=,)\s+|\s+(?=\])"
    result = re.sub(regex,"",code)
    return result

# 用于分词的关键函数
def parse(code:str)->list:
    if checkHasComment(code):
        code = deleteComment(code)
    code = preProcessArray(code)
    regex = r"((?<=\[)\w+)(?#匹配宏名称)|(\w+(?=\=))(?#匹配参数名称)|((?<=\=)\d+)(?#匹配int参数)|((?<=\=)\[\d+,\d+\])(?#匹配长度为2的int数组)|((?<=\=)\[\d+,\d+,\d+,\d+])(?#匹配长度为4的int数组)|(\"[a-zA-Z\._0-9\s]+\")(?#匹配使用双引号的string参数)|(\'[a-zA-Z\._0-9\s]+\')(?#匹配使用单引号的string参数)|((?<=\=)\w+)(?#匹配变量型参数)"
    
    matches = re.finditer(regex, code)
    result = []
    for matchNum, match in enumerate(matches, start=1):
        m = match.group()#.strip('"')
        result.append(m)
    #print("结果",result)
    return result