import re
import ColorPrint
# 仅适用于宏函数的预处理 预处理完成 写入内存
# 检查是否有注释
def 检查到_有注释(code:str,verbose:bool)->bool:
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
def 检查到_当前行的首尾有空格(code:str,verbose: bool) -> bool:
    if code[0] == " " or code[len(code)-1] == " ":
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
def 检查到_数组之间的空格(code,verbose: bool) -> bool:
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

# 去除首尾注释字符串 //注释 或者 // 注释
def deleteComment(code) -> str:
    regex = r"//.+"
    result = re.sub(regex,"",code)
    return result

# 去除当前行首尾位的多余空格字符串
# example:\s\s\s\s\s[macro param=value]\s\s\s\s\s\n -> [macro param=value]\n
def 删除_首尾的空格(code) -> str:
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
def 删除_数组之间的空格(code) -> str:
    regex = r"(?<=\[)\s+|\s+(?=,)|(?<=,)\s+|\s+(?=\])"
    result = re.sub(regex,"",code)
    return result

def 检查到_当前代码行是空的(code) -> bool:
    if code == "":
        return True
    else:
        return False

def 清理数组(code_line: str,fianl_result: list) -> list:
    for element in code_line:
        if element == None or element == "\n":
            pass
        else:
            fianl_result.append(element)
    return fianl_result

# 返回当前代码行
# todo 移除数组中的None和\n
def 处理(code_type: str, 当前代码行: str, 详细输出: bool) -> str:
    删除注释后的代码行 = ""
    删除首尾空格后的代码行 = ""
    删除数组空格后的代码行 = ""
    最终结果 = []
    # if code_type == "多行宏":
    #     pass
    # todo 移除这个参数？
    if code_type == "单行宏":
        
        if 检查到_当前代码行是空的(当前代码行):
            ColorPrint.print_verbose_hint("当前代码行是空的,跳过!")
            pass
        else:
            if 详细输出:
                ColorPrint.print_verbose("传入的原始字符串",当前代码行)

            if 检查到_有注释(当前代码行, 详细输出):
                删除注释后的代码行 = deleteComment(当前代码行)
                ColorPrint.print_verbose("删除注释后的字符串",删除注释后的代码行)
                if 检查到_当前代码行是空的(删除注释后的代码行):
                    ColorPrint.print_verbose_hint("删除注释后的字符串是空的,跳过!")
                    pass
                else:          
                    if 检查到_当前行的首尾有空格(删除注释后的代码行, 详细输出):
                        删除首尾空格后的代码行 = 删除_首尾的空格(删除注释后的代码行)
                        ColorPrint.print_verbose("删除头尾空格后的字符串",删除首尾空格后的代码行)
                    else:
                        删除首尾空格后的代码行 = 删除注释后的代码行

                    if 检查到_数组之间的空格(删除首尾空格后的代码行, 详细输出):
                        删除数组空格后的代码行 = 删除_数组之间的空格(删除首尾空格后的代码行)
                        ColorPrint.print_verbose("删除数组之间空格后的字符串",删除数组空格后的代码行)
                        if 详细输出:
                            ColorPrint.print_compile("预处理完毕的字符串",删除数组空格后的代码行)
                        最终结果 = 清理数组(删除数组空格后的代码行)
                        return 最终结果

                    else:
                        ColorPrint.print_verbose_hint("没有检测到数组之间的空格")
                        ColorPrint.print_verbose("预处理完毕的结果",删除首尾空格后的代码行)
                        if 详细输出:
                            ColorPrint.print_compile("预处理完毕的字符串",删除首尾空格后的代码行)
                        最终结果 = 清理数组(删除数组空格后的代码行)
                        return 最终结果
                        # return 删除首尾空格后的代码行
                                        
    # elif code_type == "Parser脚本":
    #     pass