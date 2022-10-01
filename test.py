def 获得参数名1():
    a = "@bg abc=1"
    split_start = 0
    split_end = 0
    start = 0
    current = 0
    equals_index = 0
    tokens = []
    # 用于归位的索引
    priv_index = 0

    def isAtStart():
        if current < start:
            return True
        else:
            return False

    def isAtEnd():
        nonlocal current
        if current >= len(a):
            return True
        else: 
            return False

    def readBack():
        nonlocal current
        current -= 1
        return a[current -1]

    def readNext():
        nonlocal current
        current += 1
        return a[current -1]

    def peekBack():
        nonlocal current
        return a[current-1]

    while not isAtEnd(): 
        c = readNext()
        #print(c)
        if c == "=":
            equals_index = current -1
            priv_index = current
            while peekBack() != " " and not isAtStart():
                readBack()
            if isAtStart():
                print("越界")
                break
            split_start = equals_index - len(a)
            split_end = current - len(a)
            revert_str = a[split_start - 1 : split_end -1 :-1]
            s = revert_str[::-1]
            tokens.append(s)
            # 索引归位
            current = priv_index
    # 开始位置是实际位置-1 结束位置是实际位置

    print(tokens)

def 分析标记():
    code = "@addto index=16568 pos=[0,0] //这是注释comment"
    split_start = 0
    split_end = 0
    start = 0
    current = 0
    equals_index = 0
    tokens = []
    # 用于归位的索引
    priv_index = 0

    def readBack():
        nonlocal current
        current -= 1
        return code[current -1]

    def readNext():
        nonlocal current
        current += 1
        return code[current -1]

    def isAtStart():
        nonlocal start
        nonlocal current
        if current < start:
            return True
        else:
            return False

    def isAtEnd():
        nonlocal start
        nonlocal current
        if current >= len(code):
            return True
        else: 
            return False

    def peekBack():
        nonlocal current
        return code[current-1]

    def peekNext():
        nonlocal current
        current += 1
        return code[current]

    def getMacro():
        # 原理就是 "  " 作为字符串两端，获得这两个符号的位置，并提取子字符串
        while peekNext() != ' ' and not isAtEnd():
            readNext()
        if isAtEnd():
            print("第"+ str(current) + "列处,宏名不完整")
            return
        value = code[start +1 : current]
        #print(value)
        tokens.append(value)

    def getArray():
        while peekNext() != "]" and not isAtEnd():
            readNext()
        if isAtEnd():
            print("第" + str(current) + "列处，数组代码不完整")
            return
        value:str = code[start : current]
        print("数组型的值为",value)
        ar = value.split(",")
        for v in ar:
            tokens.append(v)

    def getParamName()->str:
        split_start = equals_index - len(code)
        split_end = current - len(code)
        revert_str = code[split_start - 1 : split_end -1 :-1]
        s = revert_str[::-1]
        return s

    def getParamValue()->str:
        split_start = equals_index
        value = code[split_start+1 : current]
        return value
        
    while not isAtEnd(): 
        c = readNext()
        #print(c)
        if c == "@":
            getMacro()

        elif c == "=":
            equals_index = current -1
            priv_index = current
            # 取参数名字 回溯法
            while peekBack() != " " and not isAtStart():
                readBack()
            if isAtStart():
                print("越界,at: ",current)
                break
            tokens.append(getParamName())
            # 索引归位
            current = priv_index
            # 取参数值
            while peekNext() != " " and not isAtEnd():
                readNext()
            if isAtEnd():
                print("扫描器出错,在宏代码: " + current + "列处")
                break
            tokens.append(getParamValue())

        elif c == "/":
            if readNext() == "/":
                pass
            else:
                print("注释代码编写错误,列: ",current)
                break
    print(tokens)
#获得参数名1()
分析标记()