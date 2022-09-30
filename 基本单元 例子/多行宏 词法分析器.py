a = "[sprite index=0 rect=[0,0,0,0] file='a.png']" # [addto index=0 pos=[0,2]]
start = 0 #开始位置 为0
current = 0 #当前位置 

tokens = []
# 是否遇到数组参数
array_meet = False
array_closed = False

def eatNext()->str:
    global current
    current += 1
    return a[current -1]

def getMacro():
    global current
    global start
    # 原理就是 "  " 作为字符串两端，获得这两个符号的位置，并提取子字符串
    while peek() != ' ' and not isAtEnd():
        eatNext()
    if isAtEnd():
        print("宏名不完整")
        return
    value = a[start +1 : current]
    #print(value)
    tokens.append(value)

def addToken(type):
    global start
    global current
    text = a[start,current]

def getParamName():
    global current
    global start
    while peek() != "=" and not isAtEnd():
        eatNext()
    if isAtEnd():
        print("第" + str(current) + "列处，参数不完整")
        return
    value:str = a[start : current]
    #print(value)
    tokens.append(value)

def getParamValue():
    global current
    global start
    global array_meet
    global array_closed
    array_meet = False
    array_closed = False
    # 处理rect_t 长度为4的整数型数组 范围型
    if a[current] == "[":
        # array_meet == True
        while peek() != "]" and not isAtEnd():
            eatNext()
        if isAtEnd():
            print("第" + str(current) + "列处，参数不完整")
            return
        value:str = a[start+2 : current]
        v2 = value.split(",")
        for param in v2:
            tokens.append(param)
        #print("范围型的值为",value)
    elif a[current].isdigit():
        while peek() != ' ' and not isAtEnd():
            eatNext()
        if isAtEnd():
            print("第" + str(current) + "列处，参数不完整")
            return
        value:str = a[start+1 : current]
        #print("int型的值为",value)
        tokens.append(value)
    elif a[current] == "'":
        #先前进一下，避免从' 开头检测
        pp = eatNext()
        #print("先前进后的值",pp)
        while peek() != "'" and not isAtEnd():
            eatNext()
        if isAtEnd():
            print("第" + str(current) + "列处，参数不完整")
            return
        value:str = a[start+2 : current]
        #print("string型的值为",value)
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
    if c == "[":#and current == 1:
        #tokens.append("多行宏开始")
        getMacro()
    elif c == "]":
        pass
        #tokens.append("多行宏结束")
    elif c == " ": pass
    elif c == "=":
        getParamValue()
    else:
        getParamName()

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