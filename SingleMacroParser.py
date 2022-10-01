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