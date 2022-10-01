# 基于正则表达式的多行宏函数的词法分析器
import re
def parse(code:str)->list:
    #匹配字母 下划线 数字 或者字符串里面的内容
    regex = r"([a-z_0-9]+)|(\"(.*)\")"

    #test_str = '[sprite index=0 file="a.png" rect=[0,0,0,0] ]'
    pre = re.sub(r"//[^\n]*"," ",code)
    #print("预处理",pre)
    matches = re.finditer(regex, pre)
    result = []
    for matchNum, match in enumerate(matches, start=1):
        m = match.group().strip('"')
        result.append(m)
    return result