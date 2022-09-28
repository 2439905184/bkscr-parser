# 参考了Lox语言的实现
import tokentype
import token
class Scanner:
    source:str = ""
    tokens = []
    start = 0 # 第一个字符
    current = 0 # 当前正在处理的字符
    line = 1 # 当前扫描器执行到第几行
    def __init__(self,source:str) -> None:
        self.source = source
    def isAtEnd(self)->bool:
        return True
        #return self.current >= len(self.source)
        """if self.current >= len(self.source):
            return True
        else:
            return False"""
    # -> char
    def nextChar(self):
        self.current += 1
        return self.source[self.current]# - 1]

    def addToken(self,type):
        self.tokens.append(type)

    def scanToken(self):
        char = self.nextChar()
        print(char)
        if char == "[":
            self.addToken(tokentype.TokenType.左中括号)
        elif char == "]":
            self.addToken(tokentype.TokenType.右中括号)
        elif char == "*":
            self.addToken(tokentype.TokenType.标签)
        elif char == " ":pass
        else:
            #if char is str:
            self.addToken(type)
    # 扫描标记
    def scanTokens(self):
        # while not self.isAtEnd():
        #     print("执行扫描")
        #     start = self.current
        #     self.scanToken()
        max_index = 5
        index = 0
        while index < max_index:
            #print("执行扫描")
            self.start = self.current
            self.scanToken()
            index += 1
        self.tokens.append(tokentype.TokenType.结尾)
        return self.tokens
        # 当扫描到结尾时
        #self.tokens.add(token.Token(tokentype.结尾,"",null,line))
        #return self.tokens
