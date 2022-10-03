from enum import Enum
class TokenType(Enum):
    # 单字符标记
    左中括号 = 1
    右中括号 = 2
    标签 = 3
    
    # 单字符或者双字符标记
    赋值 = 4 # =
    等于 = 5 # ==
    
    结尾 = -1
    #注释 = 1