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
        if verbose:
            ColorPrint.print_verbose("宏之间有空格",code)
        return True
    else:
        if verbose:
            ColorPrint.print_verbose("宏之间没有空格",code)
        return False

# 检查当前行的宏的数组参数值是否包含空格
def checkIsOpenArray(code,verbose: bool) -> bool:
    regex = r"(?<=\=\[)(?<=\[)\s+|\s+(?=,)|(?<=,)\s+|\s+(?=\])"
    matches = re.finditer(regex,code)
    for matchNum, match in enumerate(matches):
        if match != None:
            if verbose:
                ColorPrint.print_verbose("数组值之间包含空格",code)
            return True
        else:
            if verbose:
                ColorPrint.print_verbose("数组值之间不包含空格",code)
            return False
    #return False

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

# 去除两宏之间的多余空格
# 意思是查找 ]之后的多个空格并且找到[之前的多个空格 查找结果为 ]\s\s\s[ 里面的所有\s符号（不包括 '][' 符号)
def delete_space_between_Macro(code) -> str:
    regex = r"(?<=\])\s+(?=\[)"
    result = re.sub(regex,"",code)
    return result

# 将数组参数里面的空格化为1 解释：# 匹配[后面的所有空格 或者,前面的所有空格 或者，后面的所有空格 或者]前面的所有空格并替换为""
# example:[macro param=[\s\s\s800\s\s\s,\s\s\s600\s\s\s]] -> [macro param=[800,600]]
def delete_space_between_Array(code) -> str:
    regex = r"(?<=\[)\s+|\s+(?=,)|(?<=,)\s+|\s+(?=\])"
    result = re.sub(regex,"",code)
    return result

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
        code = deleteComment(code)
        ColorPrint.print_verbose("删除注释后的字符串",code)
    if checkHasSpace(code,verbose):
        code = delete_space_at_head_or_tail(code)
        ColorPrint.print_verbose("删除头尾空格后的字符串",code)
    if checkHasSpace_Between_Macro(code,verbose):
        code = delete_space_between_Macro(code)
        ColorPrint.print_verbose("删除宏之间空格后的字符串",code)
    if checkIsOpenArray(code,verbose):
        code = delete_space_between_Array(code)
        ColorPrint.print_verbose("删除数组之间空格后的字符串",code)
    if verbose:
        ColorPrint.print_compile("预处理完毕的字符串",code)
    regex = r"(?P<macroName>\[\w+\s)|(?P<paramName>\S+(?=\=))|(?P<intValue>(?<=\=)\d+)|(?P<intArray2>(?<=\=)\[\d+,\d+\])|(?P<intArray4>(?=\=)\[\d+,\d+,\d+,\d+\])|(?P<varArray2>(?<=\=)\[\S+,\S+\])|(?P<varArray4>(?<=\=)\[\S+,\S+,\S+,\S+\])|(?P<varValue>(?<=\=)\w+)|(?P<stringValue1>((?<=\=)\".+\"))|(?P<stringValue2>(?<=\=)\'.+\')|(?P<closeMacro>\[\w+\])(?#取形如'[bg]'的字符串)|(=)"
    matches = re.finditer(regex, code)
    result = []
    for matchNum, match in enumerate(matches, start=1):
        group = match.groupdict()
        group_value = match.group()
        if group.get("macroName") != None:
            oldMacro = group["macroName"]
            newMacro = oldMacro.replace("[","@").strip(" ")
            result.append(newMacro)
        elif group.get("varArray2") != None:
            oldArray = group["varArray2"] # 把[x,y]] -> [x,y]
            ColorPrint.print_verbose("识别到变量数组",oldArray)
            newArray = oldArray[0:len(oldArray)-1]
            ColorPrint.print_verbose_hint("预处理变量数组并开始编译")
            ColorPrint.print_compile(oldArray,newArray)
            result.append(newArray)
        elif group.get("closeMacro") != None:
            oldMacro:str = group["closeMacro"].strip("\[|\]")
            newMacroList = ["@"]
            newMacroList.append(oldMacro)
            newMacro:str = "".join(newMacroList)
            result.append(newMacro)
        else:
            result.append(group_value)
    if verbose:
        ColorPrint.print_compile("编译结果",str(result))
    return result