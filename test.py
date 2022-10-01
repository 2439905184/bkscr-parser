code = "@sprite index=0"
start = 0
current = 1

# def readBack():
#     global current
#     current -= 1
#     return code[current-1]

# def readNext():
#     pass

# equal_index = 0
# for char in code:
#     if char == "=":
#         equal_index = current
#         print(equal_index)
#         # if readBack() != " ":
#         #     paramName = code[current:equal_index]
#         #     print(paramName)
#     if char == " ":
#         print(current)
#     current += 1

a = "@bg abc=1"
split_start = 0
split_end = 0
start = 0
current = 0
equals_index = 0
tokens = []
# 用于归位的索引
priv_index = 0
def readBack():
    global current
    current -= 1
    return a[current -1]

def readNext():
    global start
    global current
    current += 1
    return a[current -1]

def isAtStart():
    global current
    global start
    if current < start:
        return True
    else:
        return False

def isAtEnd():
    global current
    global start
    if current >= len(a):
        return True
    else: 
        return False

def peekBack():
    global current
    # if isAtStart(): 
    #     return "\0"
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
        #print(current)
        split_start = equals_index - len(a)
        split_end = current - len(a)
        revert_str = a[split_start - 1 : split_end -1 :-1]
        #print(revert_str)
        s = revert_str[::-1]
        #print(s)
        #print(s == "abc")
        tokens.append(s)
        # 索引归位
        current = priv_index
# 开始位置是实际位置-1 结束位置是实际位置
#print(a[-3:-7:-1])
print(tokens)