a = "@sprite index=0 file='a.png' "
start = 0 #开始位置 为0
current = 0 #当前位置 

tokens = []
def eatNext()->str:
    global current
    current += 1
    return a[current -1]
# 取字符串的值
def getMacro():
    global current
    global start
    # 原理就是 "  " 作为字符串两端，获得这两个符号的位置，并提取子字符串
    while peek() != ' ' and not isAtEnd():
        current += 1
    value = a[start +1 : current]
    #print(value)
    tokens.append(value)
    pass

def getParamName():
    global current
    global start
    while peek() != "=" and not isAtEnd():
        eatNext()
    if isAtEnd():
        print("参数名不完整")
        return
    value:str = a[start : current]
    #print(value)
    tokens.append(value)

def getParamValue():
    global current
    global start
    while peek() != " " and not isAtEnd():
        eatNext()
    if isAtEnd():
        print("参数名不完整")
        return
    value:str = a[start+1 : current]
    #print(value)
    tokens.append(value)
# 向后读取字符数据
def peek():
    if isAtEnd(): return "\0"
    return a[current]

def isAtEnd():
    # 如果 >= len(a) 返回 true 否则返回false
    return current >= len(a)

def scanToken():
    c = eatNext()
    if c == "@":
        tokens.append("单行宏")
        getMacro()
    elif c == " ": pass
    elif c == "=":
        getParamValue()
    else:
        getParamName()
        pass
# 扫描标记
def scanTokens():
    global start
    global current
    #print("start:")
    while not isAtEnd():
        start = current
        #print("正在遍历每个字符：",start)
        scanToken()
    return tokens
result = scanTokens()
print(result)