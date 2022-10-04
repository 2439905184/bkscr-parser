# 基于正则表达式的多行宏函数的词法分析器
import re
import ColorPrint

def getTokens(code_line) -> list:
    token_result = []
    pre = []
    a:str = code_line[1:len(code_line)]
    split = a.split("=")[0] # a=1 b=2 c=3 [a,1]
    param_name = split[0]
    param_value = split[1]
    pre.append()
    token_result.append(param_name)
    token_result.append(param_value)
# 每次返回解析后的一行的数组分词
def parse(code:str,scanLine:int,verbose:bool)->list:
    '''
    code: 经过预处理的一行代码
    verbose: 是否输出详细信息
    '''
    result = re.split(r"\s+","code")
    
    return result