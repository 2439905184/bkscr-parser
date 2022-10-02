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

# 在分析完成之后，替换[sprite -> @sprite 
# example: [sprite pos=[0,2]] 最简格式，所以sprite命令和第一个参数之间有且至少有一个空格
# codeArray是已经处理完成的数组
# example: ['sprite', 'pos', '[0,2]']
# 使用正则可能难以处理，这里使用逐字符扫描器土法炮制
# [sprite index=0 pos=[0,2]]
# 先处理原始字符串里的[sprite ，这里把 '[' 和 ' ' 之间的字符视为字符串
# 获得宏名称
def getMacro(code,line,verbose)->list:
    bufferMacro = []
    #bufferCloseMacro = []
    regex = r"(?P<openMacro>\[\w+\s)(?#取形如:'[bg '的字符串)|(?P<closeMacro>\[\w+\])(?#取形如'[bg]'的字符串)"
    matches = re.finditer(regex,code)
    for matchNum, match in enumerate(matches):
        group = match.groupdict()
        if group.get("openMacro") != None:
            if verbose:
                print(">>>找到带有空格的宏，开始编译...")
            oldValue = group["openMacro"]
            newValue = oldValue.replace("[","@")
            if verbose:
                print("行:",line,">>>",oldValue,"-> ",newValue)
            bufferMacro.append(newValue)
        elif group.get("closeMacro") != None:
            if verbose:
                print(">>>找到紧凑的宏，开始编译...")
            oldValue = group["closeMacro"]
            newValue = oldValue.replace("[","@")
            if verbose:
                print("行:",line,">>>",oldValue,"-> ",newValue)
            bufferMacro.append(newValue)
        # print("行:",line,"找到的组","-> ",group)
    if verbose:
        # print("结果",line,"-> ",bufferMacro)
        pass
    return bufferMacro

def replaceMacro(codeArray:list):
    # 匹配 ' ' 前面的宏名称 或者 ']' 前面的宏名
    # example1 [sprite index=1] 中匹配到sprite字符串
    # example2 [endif] 中匹配到 endif字符串
    macro_regex = r"\w+(?=\s)|\w+(?=\])"
    regex = r"\[\w+\s"
    subst = "@sprite "

    cc = re.sub(regex, subst, code)

    

# 用于分词的关键函数 verbose:是否输出详细信息
allMacros = []
def parse(code:str,scanLine:int,verbose:bool)->list:
    if checkHasComment(code):
        code = deleteComment(code)
    code = preProcessArray(code)
    macros = getMacro(code,scanLine,verbose)
    allMacros.append(macros)
    # print("找到的所有结果",allMacros,len(allMacros))
    # 备份
    #regex = r"(?P<macroName>\[\w+\s)(?#匹配宏名称)|(\w+(?=\=))(?#匹配参数名称)|((?<=\=)\d+)(?#匹配int参数)|((?<=\=)\[\d+,\d+\])(?#匹配长度为2的int数组)|((?<=\=)\[\d+,\d+,\d+,\d+])(?#匹配长度为4的int数组)|(\"[a-zA-Z\._0-9\s]+\")(?#匹配使用双引号的string参数)|(\'[a-zA-Z\._0-9\s]+\')(?#匹配使用单引号的string参数)|((?<=\=)\w+)(?#匹配变量型参数)"
    regex = r"(?P<macroName>\[\w+\s)(?#匹配宏名称)|(?P<paramName>\w+(?=\=))(?#匹配参数名称)|(?P<intValue>(?<=\=)\d+)(?#匹配int参数)|(?P<intArrayValue2>(?<=\=)\[\d+,\d+\])(?#匹配长度为2的int数组)|(?P<intArrayValue4>(?<=\=)\[\d+,\d+,\d+,\d+])(?#匹配长度为4的int数组)|(?P<stringValue1>\"[a-zA-Z\._0-9\s]+\")(?#匹配使用双引号的string参数)|(?P<stringValue2>\'[a-zA-Z\._0-9\s]+\')(?#匹配使用单引号的string参数)|(?P<var>(?<=\=)\w+)(?#匹配变量型参数)"
    
    # 备注：如果顺序是乱的，还需要在进行一个自我构造空函数用于处理顺序问题
    # 顺序应该为 <macroName> <paramName> <paramValue> <paramName> <paramValue>
    # 其中：<intValue> <stringValue1> <stringValue2> <intArrayValue2> <intArrayValue4> <var> 与顺序无关，只需要一个参数对应一个值
    matches = re.finditer(regex, code)
    result = []
    for matchNum, match in enumerate(matches, start=1):
        group = match.groupdict()#.strip('"')
        if group.get("macroName") != None:
            oldMacro = group["macroName"]
            newMacro = oldMacro.replace("[","@")
            result.append(newMacro)
        elif group.get("paramName") != None:
            result.append(group["paramName"])
        elif group.get("intValue") != None:
            result.append(group["intValue"])
        elif group.get("stringValue1") != None:
            result.append(group["stringValue1"])
        elif group.get("stringValue2") != None:
            result.append(group["stringValue2"])
        elif group.get("intArrayValue2") != None:
            result.append(group["intArrayValue2"])
        elif group.get("intArrayValue4") != None:
            result.append(group["intArrayValue4"])
        elif group.get("var") != None:
            result.append(group["var"])
        # print(m)
        #result.append(m)
    print("结果",result)
    #replaceMacro(result)
    return result