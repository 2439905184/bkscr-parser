#a = '@sprite     index=7768   file="a.png"   rect=[0,0,0,0]'
#a = '@bg aaaaf="ajoig" br=[0,2]'

class parser:
    tokens = []
    source = ""
    start = 0 # 开始位置
    current = 0 # 当前位置 

    def __init__(self, source):
        self.source = source

    # 用于回溯
    def eatBack(self)->str:
        self.current -= 1
        return self.source[self.current + 1]

    def getMacro(self):
        # 原理就是 "  " 作为字符串两端，获得这两个符号的位置，并提取子字符串
        while self.peek() != ' ' and not self.isAtEnd():
            self.eatNext()
        if self.isAtEnd():
            print("第"+ str(self.current) + "列处,宏名不完整")
            return
        value = self.source[self.start +1 : self.current]
        #print(value)
        self.tokens.append(value)

    def scanToken(self, source):
        c = self.eatNext()
        #print(c)
        if c == "@":
            self.getMacro()
        elif c == " ": pass
        elif c == "=":
            self.getParamName()
        # elif c.isalpha() :
        #     print("是字母",c)
        #     self.getParamName()
        
        # elif c.isdigit():
        #     self.getInt()
        # elif c == '"':
        #     self.getString()
        # elif c == "[":
        #     getArray()

    # 扫描标记
    def scanTokens(self)->list:
        while not self.isAtEnd():
            self.start = self.current
            #print("正在遍历每个字符：",start)
            self.scanToken(self.source)
        return self.tokens

    def eatNext(self)->str:
        self.current += 1
        return self.source[self.current -1]

    def getParamName(self):
        while self.peek() != " ":# and not self.isAtEnd():
            self.eatNext()
        # if self.isAtEnd():
        #     print("第"+ str(self.current) + "列处,参数名不完整")
        #     return
        value:str = self.source[self.start : self.current]
        print("参数名称",value)
        self.tokens.append(value)

    def getInt(self):
        while self.peek() != ' ' and not self.isAtEnd():
            self.eatNext()
        if self.isAtEnd()():
            print("第" + str(self.current) + "列处，int参数代码不完整")
            return
        value:str = a[self.start : self.current]
        # print("int型的值为",value)
        self.tokens.append(value)

    def getString(self):
        while self.peek() != '"' and not self.isAtEnd():
            self.eatNext()
        if self.isAtEnd():
            print("第" + str(current) + "列处，字符串代码不完整")
            return
        value:str = a[start+1 : current]
        # print("string型的值为",value)
        self.tokens.append(value)

    def getArray(self):
        while self.peek() != "]" and not self.isAtEnd():
            self.eatNext()
        if self.isAtEnd():
            print("第" + str(self.current) + "列处，数组代码不完整")
            return
        value:str = a[self.start+2 : self.current]
        print("数组型的值为",value)
        ar = value.split(",")
        for v in ar:
            self.tokens.append(value)

    # 向后读取字符数据
    def peek(self):
        if self.isAtEnd(): return "\0"
        return self.source[self.current]

    def isAtEnd(self):
        # 如果 >= len(a) 返回 true 否则返回false
        return self.current >= len(self.source)


ff = open("../test/单行.bkscr","r",encoding="utf-8")
s = ff.read()
print(s)
ff.close()
parserObject = parser(s)
result = parserObject.scanTokens()
print(result)

""" 备份
# 基于逐字符分析的单行宏词法分析器
import re
def parse(code:str)->list:
    #code = "@addto index=1280 "
    current = 0  
    end = len(code) - 1 #实际用来判断结尾的变量
    tokens = []

    def peekNext():
        nonlocal current
        current += 1
        return code[current]

    action = "scanParamName" #scanParamValue
    
    # 适用于没有换行符的解析 末尾字母参数
    tail = ""
    print("去除注释前",len(code),code)
    if "//" in code:
        # 处理注释 并补充空格
        code = re.sub(r"\s+//.*|//.*"," ",code)
        print("去除注释后",len(code),code)
        pt = list(code)
        code = "".join(pt)
        # 如果有注释的时候就去除注释，添加末尾空格，并重新计算末尾index
        end = len(code)-1
        if code[end] == " ":
            print("预处理结果",list(code))
        else: print("预处理出错了！")
    #不是空格 加上空格 便于程序识别
    elif code[len(code)-1] != " ":
        #print("code末尾不是空格",list(code))
        code += " "
        end = len(code) -1
        if code[end] == " ":
            print("预处理结果",list(code))
        else: print("预处理出错了！")
        
    print("启动为",action)
    for index,char in enumerate(code):
        if char == "@":
            while peekNext() != " " and index != end:
                pass
            vc = code[index:current]
            tokens.append(vc)

        if char == " " and action == "scanParamName":
            sp_start = index + 1
            while peekNext() != "=" and current != end:
                #print(code[current])
                pass
            if code[current] == "=":
                action = "scanParamValue"
                vc = code[sp_start:current]
                tokens.append(vc)
                print(vc)
                print("切换为",action)

        if char == "=" and action == "scanParamValue":
            while peekNext() != " " and current != end:
                pass
            vc = code[index+1:current]
            tokens.append(vc)
            if code[current] == " ":
                action = "scanParamName"
                print(vc)
                print("切换为",action)
                if current == end:
                    break

    #print(tokens)
    return tokens
"""