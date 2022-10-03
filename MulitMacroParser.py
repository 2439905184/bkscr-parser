# 基于正则表达式的多行宏函数的词法分析器
import re
import ColorPrint
# 检查是否有注释
def checkHasComment(code:str,verbose:bool)->bool:
    bufferString = ""
    for char in code: # 这里的code是一行代码
        bufferString += char
    if "//" in bufferString:
        if verbose:
            ColorPrint.print_verbose("检测到有注释",code)
        return True
    else:
        if verbose:
            ColorPrint.print_verbose("没有检测到注释",code)
        return False

# 检查当前行首尾是否有空格
def checkHasSpace(code:str,verbose: bool) -> bool:
    if code[0] == " " and code[len(code)-1] == " ":
        if verbose:
            ColorPrint.print_verbose("当前行首尾有空格",code)
        return True
    else:
        if verbose:
            ColorPrint.print_verbose("当前行首尾没有空格",code)
        return False

# 检查当前行的宏之间是否有空格 [macro] [macro]
def checkHasSpace_Between_Macro(code,verbose: bool):
    regex = r"(?<=\])\s+(?=\[)"
    check_result = re.match(regex,code)
    if check_result != None:
        ColorPrint.print_verbose("宏之间有空格",code)
        return True
    else:
        ColorPrint.print_verbose("宏之间没有空格",code)
        return False

# 检查当前行的宏的数组参数值是否包含空格
def checkIsOpenArray(code,verbose: bool) -> bool:
    regex = r"(?<=\=\[)(?<=\[)\s+|\s+(?=,)|(?<=,)\s+|\s+(?=\])"
    if re.match(regex,code) != None:
        return True
    else:
        return False

# 去除首尾注释字符串 \s\s//\s\s
# example //这是注释[macro]
def deleteComment(code,verbose: bool) -> str:
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

# 去除两宏之间的多余空格
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

allMacros = []
# 每次返回解析后的一行的数组分词
def parse(code:str,scanLine:int,verbose:bool)->list:
    '''
    用于分词的关键函数 
    verbose:是否输出详细信息
    '''
    # 预处理
    if verbose:
        ColorPrint.print_verbose("传入的原始字符串",code)
    if checkHasComment(code,verbose):
        code = deleteComment(code,verbose)
        #ColorPrint.print_verbose("删除注释后的字符串",code)
    if checkHasSpace(code,verbose):
        code = delete_space_at_head_or_tail(code,verbose)
    if checkHasSpace_Between_Macro(code,verbose):
        code = delete_space_between_Macro(code,verbose)
    if checkIsOpenArray(code,verbose):
        code = preProcessArray(code,verbose)
    #macros = getMacro(code,scanLine,verbose)
    #allMacros.append(macros)
    # print("找到的所有结果",allMacros,len(allMacros))
    if verbose:
        ColorPrint.print_compile("预处理完毕的字符串",code)
        # print(,"->",code)
    # 备份
    #regex = r"(?P<macroName>\[\w+\s)(?#匹配宏名称)|(\w+(?=\=))(?#匹配参数名称)|((?<=\=)\d+)(?#匹配int参数)|((?<=\=)\[\d+,\d+\])(?#匹配长度为2的int数组)|((?<=\=)\[\d+,\d+,\d+,\d+])(?#匹配长度为4的int数组)|(\"[a-zA-Z\._0-9\s]+\")(?#匹配使用双引号的string参数)|(\'[a-zA-Z\._0-9\s]+\')(?#匹配使用单引号的string参数)|((?<=\=)\w+)(?#匹配变量型参数)"
    #regex = r"(?P<macroName>\[\w+\s)(?#匹配宏名称)|(?P<paramName>\w+(?=\=))(?#匹配参数名称)|(?P<intValue>(?<=\=)\d+)(?#匹配int参数)|(?P<intArrayValue2>(?<=\=)\[\d+,\d+\])(?#匹配长度为2的int数组)|(?P<intArrayValue4>(?<=\=)\[\d+,\d+,\d+,\d+])(?#匹配长度为4的int数组)|(?P<stringValue1>\"[a-zA-Z\._0-9\s]+\")(?#匹配使用双引号的string参数)|(?P<stringValue2>\'[a-zA-Z\._0-9\s]+\')(?#匹配使用单引号的string参数)|(?P<var>(?<=\=)\w+)(?#匹配变量型参数)|(?P<closeMacro>\[\w+\])(?#紧凑结构的宏)"
    #regex = r"(?P<macroName>\[\w+\s)|(?# =前面的paramName)(?P<macroParamName>\S+(?=\=))|(?# =后面的数字)(?P<intValue>(?<=\=)\d+)|(?# int[2])(?P<arrayLength2>(?<=\=)\[.,.\])|(?#int[4])((?<=\=))\[.,.,.,.\]|(?# =后面的变量参数)(?P<varValue>(?<=\=)\w+)|(?#双引号字符串)((?<=\=)\".+\")|(?#单引号字符串)((?<=\=)\'.+\')|(?P<closeMacro>\[\w+\])(?#取形如'[bg]'的字符串)|(=)"
    regex = r"(?P<macroName>\[\w+\s)|(?P<paramName>\S+(?=\=))|(?P<intValue>(?<=\=)\d+)|(?P<intArray2>(?<=\=)\[\d+,\d+\])|(?P<intArray4>(?=\=)\[\d+,\d+,\d+,\d+\])|(?P<varArray2>(?<=\=)\[\S+,\S+\])|(?P<varArray4>(?<=\=)\[\S+,\S+,\S+,\S+\])|(?P<varValue>(?<=\=)\w+)|(?P<stringValue1>((?<=\=)\".+\"))|(?P<stringValue2>(?<=\=)\'.+\')|(?P<closeMacro>\[\w+\])(?#取形如'[bg]'的字符串)|(=)"
    # 备注：如果顺序是乱的，还需要在进行一个自我构造空函数用于处理顺序问题
    # 顺序应该为 <macroName> <paramName> <paramValue> <paramName> <paramValue>
    # 其中：<intValue> <stringValue1> <stringValue2> <intArrayValue2> <intArrayValue4> <var> 与顺序无关，只需要一个参数对应一个值
    matches = re.finditer(regex, code)
    result = []
    for matchNum, match in enumerate(matches, start=1):
        group = match.groupdict()
        group_value = match.group()
        if group.get("macroName") != None:
            oldMacro = group["macroName"]
            newMacro = oldMacro.replace("[","@").strip(" ")
            result.append(newMacro)
        elif group.get("closeMacro") != None:
            oldMacro:str = group["closeMacro"].strip("\[|\]")
            newMacroList = ["@"]
            newMacroList.append(oldMacro)
            newMacro:str = "".join(newMacroList)
            result.append(newMacro)
        else:
            result.append(group_value)
    # finalResult:str = "".join(result)
    # print("分词结果","->",result)
    return result