import tokentype
class Token:
    type:tokentype.TokenType
    词素:str
    字面量 = 0
    line:int
    def __init__(self,type) -> None:
        self.type = type
        self.词素 = ""
        self.字面量 = ""
        self.line = "line"
    