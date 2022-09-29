lines = ["*main","@sprite index=0 file='a.png' "]
tokens = []
def addToken(type):
    tokens.append(type)

for line in lines:
    临时标记 = ""
    临时变量 = ""
    for char in line:
        if char == "*":
            addToken("标签")
            临时标记 = "标签"
        if char == "@":
            addToken("单行宏")
            临时标记 = "单行宏"

    if 临时标记 == "标签":
        for char in line:
            if char == " ":
                pass
            else:
                临时变量 += char
        addToken(临时变量)
    # 处理单行宏
    elif 临时标记 == "单行宏":
        预处理 = []
        space_times  = 0 # 空格出现的次数
        for index,char in enumerate(line):
            if char == " ":
                space_times += 1
                if space_times == 1:
                    预处理.append(临时变量)
                    临时变量 = ""
                if space_times == 2:
                    预处理.append(临时变量)
                    临时变量 = ""
                if space_times == 3:
                    预处理.append(临时变量)
                    临时变量 = ""
            else:
                临时变量 += char
                    #print(index)
        # 进行二次处理
        新处理 = []
        for element in 预处理:
            if "=" in element:
                分词 = element.split("=")
                新处理.append(分词[0])
                新处理.append("=")
                新处理.append(分词[1])
            else:
                新处理.append(预处理[0])
        print("预处理",预处理)
        print("新处理",新处理)
        for element in 新处理:
            addToken(element)
print("分词结果",tokens)
file = open("out.txt","w",encoding="utf-8")
for element in tokens:
    file.write(element + "\n")
file.close()