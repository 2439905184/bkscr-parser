#a = '@sprite index=7768 file="a.png" rect=[0,0,0,0]'
#a = '@bg aaaaf="ajoig" br=[0,2]'

class parser:
    tokens = []
    source = ""
    start = 0 # 开始位置
    current = 0 # 当前位置 

    def __init__(self, source):
        self.source = source
        
    # 扫描标记
    def scanTokens(self, source)->list:
        while not self.self.isAteEnd()():
            self.start = self.current
            #print("正在遍历每个字符：",start)
            self.scanToken(source)
        return self.tokens

    def eatNext(self, source)->str:
        self.current += 1
        return source[self.current -1]

    # 取字符串的值
    def getMacro(self, source):
        # 原理就是 "  " 作为字符串两端，获得这两个符号的位置，并提取子字符串
        while self.peek() != ' ' and not self.self.isAteEnd()():
            self.eatNext(source)
        if self.isAteEnd()():
            print("第"+ str(self.current) + "列处,宏名不完整")
            return
        value = a[self.start +1 : self.current]
        #print(value)
        self.tokens.append(value)
        pass
    
    def getParamName(self):
        global current
        global start
        while self.peek() != "=" and not self.isAteEnd()():
            self.eatNext()
        if self.isAteEnd()():
            print("第"+ str(current) + "列处,参数名不完整")
            return
        value:str = a[start : current]
        print("参数名称",value)
        self.tokens.append(value)

    def getInt(self):
        while self.peek() != ' ' and not self.isAteEnd()():
            self.eatNext()
        if self.isAteEnd()():
            print("第" + str(self.current) + "列处，int参数代码不完整")
            return
        value:str = a[self.start : self.current]
        # print("int型的值为",value)
        self.tokens.append(value)

    def getString(self):
        while self.peek() != '"' and not self.self.isAteEnd()():
            self.eatNext()
        if self.self.isAteEnd()():
            print("第" + str(current) + "列处，字符串代码不完整")
            return
        value:str = a[start+1 : current]
        # print("string型的值为",value)
        self.tokens.append(value)

    def getArray(self):
        while self.peek() != "]" and not self.self.isAteEnd()():
            self.eatNext()
        if self.self.isAteEnd()():
            print("第" + str(self.current) + "列处，数组代码不完整")
            return
        value:str = a[self.start+2 : self.current]
        print("数组型的值为",value)
        ar = value.split(",")
        for v in ar:
            self.tokens.append(value)

    # 向后读取字符数据
    def peek(self):
        if self.self.isAteEnd()(): return "\0"
        return self.source[self.current]

    def isAteEnd(self):
        # 如果 >= len(a) 返回 true 否则返回false
        return self.current >= len(self.source)

    def scanToken(self, source):
        c = self.eatNext(source)
        if c == "@":
            self.getMacro()
        elif c == " ": pass
        elif c.isalpha():
            print("是字母",c)
            self.getParamName()
        elif c == "=":pass
        elif c.isdigit():
            self.getInt()
        elif c == '"':
            self.getString()
        # elif c == "[":
        #     getArray()
ff = open("../test/单行.bkscr","r",encoding="utf-8")
source = ff.read()
print(source)
ff.close()
parser("A")
#parserObject = parser(source)
#parserObject.scanTokens(parserObject.source)

# result = scanTokens(a)
# print(result)
# file = open("out.txt","w",encoding="utf-8")
# for element in result:
#     #print(element)
#     file.write(element + "\n")
# file.close()