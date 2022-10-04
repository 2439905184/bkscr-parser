# 基于正则表达式的多行宏函数的词法分析器
import re
import ColorPrint
# bkengine单行宏匹配
# @\w+(?# 宏名称)|[a-z_A-Z]+(?=\=)(?# =前面的参数名)|(?<=\=)\w+(?# =后面的变量或者数字)|(?<=\=)\'.+\'|(?<=\=)\".+\"(?# =后面的字符串)|(?<=\=)\[\S+\](?# =后面的数组)
def getTokens(code_line) -> list:
    token_result = []
    regex = r"@\w+(?# 宏名称)|[a-z_A-Z]+(?=\=)(?# =前面的参数名)|(?<=\=)\w+(?# =后面的变量或者数字)|(?<=\=)\'.+\'|(?<=\=)\".+\"(?# =后面的字符串)|(?<=\=)\[\S+\](?# =后面的数组)"
    matches = re.finditer(regex,code_line)
    for matchNum, match in enumerate(matches):
        group = match.group()
        token_result.append(group)
    return token_result
# 每次返回解析后的一行的数组分词
def parse(code_line:str,scanLine:int,verbose:bool)->list:
    '''
    code: 经过预处理的一行代码
    verbose: 是否输出详细信息
    '''
    result = getTokens(code_line)
    if verbose:
        ColorPrint.print_compile("单行宏编译完毕的结果",str(result))
    return result