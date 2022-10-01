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

# file = open("out.txt","w",encoding="utf-8")
# for element in result:
#     #print(element)
#     file.write(element + "\n")
# file.close()