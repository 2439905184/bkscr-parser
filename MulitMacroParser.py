# 基于正则表达式的多行宏函数的词法分析器
import re
# 检查是否有注释
def checkHasComment(code:str)->bool:
    bufferString = ""
    for char in code:
        bufferString += char
    if bufferString == "//":
        return True
    else:
        return False

# 检查当前行首尾是否有空格
def checkHasSpace(code:str) -> bool:
    if code[0] == " " and code[len(code)-1] == " ":
        return True
    else:
        return False
# 检查当前行的宏直接是否有空格
def checkHasSpace_Between_Macro(code):
    regex = r"(?<=\])\s+(?=\[)"
    check_result = re.match(regex,code)
    if check_result != None:
        return True
    else:
        return False

# 检查当前行的宏的数组参数值是否包含空格
def checkIsOpenArray(code) -> bool:
    regex = r"(?<=\=\[)(?<=\[)\s+|\s+(?=,)|(?<=,)\s+|\s+(?=\])"
    if re.match(regex,code) != None:
        return True
    else:
        return False

# 去除首尾注释字符串 \s\s//\s\s
# example //这是注释[macro]
def deleteComment(code) -> str:
    #匹配模式：多个空格//后面的所有字符内容 除了\n换行符
    regex = r"\s+//[^\n]*"
    result = re.sub(regex,"",code)
    return result

# 去除当前行首尾位的多余空格字符串
# example:\s\s\s\s\s[macro param=value]\s\s\s\s\s\n -> [macro param=value]\n
def delete_space_at_head_or_tail(code) -> str:
    regex = r"^\s+|\s+$"
    result = re.sub(regex,"",code)
    return result

# 去除两宏直接的多余空格
# 意思是查找 ]之后的多个空格并且找到[之前的多个空格 查找结果为 ]\s\s\s[ 里面的所有\s符号（不包括 '][' 符号)
def delete_space_between_Macro(code) -> str:
    regex = r"(?<=\])\s+(?=\[)"
    result = re.sub(regex,"",code)
    return result

# 将数组参数里面的空格化为1 解释：# 匹配[后面的所有空格 或者,前面的所有空格 或者，后面的所有空格 或者]前面的所有空格并替换为""
# example:[macro param=[\s\s\s800\s\s\s,\s\s\s600\s\s\s]] -> [macro param=[800,600]]
def preProcessArray(code) -> str:
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
# todo
def replaceMacro(codeArray:list):
    # 匹配 ' ' 前面的宏名称 或者 ']' 前面的宏名
    # example1 [sprite index=1] 中匹配到sprite字符串
    # example2 [endif] 中匹配到 endif字符串
    macro_regex = r"\w+(?=\s)|\w+(?=\])"
    regex = r"\[\w+\s"
    subst = "@sprite "
    #cc = re.sub(regex, subst, code)

# 用于分词的关键函数 verbose:是否输出详细信息
allMacros = []
# 每次返回解析后的一行的数组分词
def parse(code:str,scanLine:int,verbose:bool)->list:
    # 预处理
    if checkHasComment(code):
        code = deleteComment(code)
    if checkHasSpace(code):
        code = delete_space_at_head_or_tail(code)
    if checkHasSpace_Between_Macro(code):
        code = delete_space_between_Macro(code)
    if checkIsOpenArray(code):
        code = preProcessArray(code)
    #macros = getMacro(code,scanLine,verbose)
    #allMacros.append(macros)
    # print("找到的所有结果",allMacros,len(allMacros))
   
    # 备份
    #regex = r"(?P<macroName>\[\w+\s)(?#匹配宏名称)|(\w+(?=\=))(?#匹配参数名称)|((?<=\=)\d+)(?#匹配int参数)|((?<=\=)\[\d+,\d+\])(?#匹配长度为2的int数组)|((?<=\=)\[\d+,\d+,\d+,\d+])(?#匹配长度为4的int数组)|(\"[a-zA-Z\._0-9\s]+\")(?#匹配使用双引号的string参数)|(\'[a-zA-Z\._0-9\s]+\')(?#匹配使用单引号的string参数)|((?<=\=)\w+)(?#匹配变量型参数)"
    #regex = r"(?P<macroName>\[\w+\s)(?#匹配宏名称)|(?P<paramName>\w+(?=\=))(?#匹配参数名称)|(?P<intValue>(?<=\=)\d+)(?#匹配int参数)|(?P<intArrayValue2>(?<=\=)\[\d+,\d+\])(?#匹配长度为2的int数组)|(?P<intArrayValue4>(?<=\=)\[\d+,\d+,\d+,\d+])(?#匹配长度为4的int数组)|(?P<stringValue1>\"[a-zA-Z\._0-9\s]+\")(?#匹配使用双引号的string参数)|(?P<stringValue2>\'[a-zA-Z\._0-9\s]+\')(?#匹配使用单引号的string参数)|(?P<var>(?<=\=)\w+)(?#匹配变量型参数)|(?P<closeMacro>\[\w+\])(?#紧凑结构的宏)"
    regex = r"(?# [macro )(?P<macroName>\[\w+\s)|(?# =前面的paramName)(?P<macroParamName>\S+(?=\=))|(?# =后面的数字)(?P<intValue>(?<=\=)\d+)|(?# int[2])(?P<arrayLength2>(?<=\=)\[.,.\])|(?#int[4])((?<=\=))\[.,.,.,.\]|(?# =后面的变量参数)(?P<varValue>(?<=\=)\w+)|(?#双引号字符串)((?<=\=)\".+\")|(?#单引号字符串)((?<=\=)\'.+\')|(?P<closeMacro>\[\w+\])(?#取形如'[bg]'的字符串)|(=)"
    # 备注：如果顺序是乱的，还需要在进行一个自我构造空函数用于处理顺序问题
    # 顺序应该为 <macroName> <paramName> <paramValue> <paramName> <paramValue>
    # 其中：<intValue> <stringValue1> <stringValue2> <intArrayValue2> <intArrayValue4> <var> 与顺序无关，只需要一个参数对应一个值
    matches = re.finditer(regex, code)
    result = []
    for matchNum, match in enumerate(matches, start=1):
        group = match.groupdict()#.strip('"')
        group_value = match.group()
        if group.get("macroName") != None:
            oldMacro = group["macroName"]
            newMacro = oldMacro.replace("[","@")
            result.append(newMacro)
        elif group.get("closeMacro") != None:
            oldMacro:str = group["closeMacro"].strip("\[|\]")
            newMacroList = ["@"]
            newMacroList.append(oldMacro)
            newMacro:str = "".join(newMacroList)
            result.append(newMacro)
        else:
            result.append(group_value)
        # elif group.get("paramName") != None:
        #     result.append(group["paramName"])
        # elif group.get("intValue") != None:
        #     result.append(group["intValue"])
        # elif group.get("stringValue1") != None:
        #     result.append(group["stringValue1"])
        # elif group.get("stringValue2") != None:
        #     result.append(group["stringValue2"])
        # elif group.get("intArrayValue2") != None:
        #     result.append(group["intArrayValue2"])
        # elif group.get("intArrayValue4") != None:
        #     result.append(group["intArrayValue4"])
        # elif group.get("var") != None:
        #     result.append(group["var"])
        
        # print(m)
        #result.append(m)
    # finalResult:str = "".join(result)
    print("分词结果",result)
    return result