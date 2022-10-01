def parse(code:str)->list:
    #code = "@addto index=1280 "
    #=1
    current = 0
    end = len(code) - 1
    tokens = []

    def peekNext():
        nonlocal current
        current += 1
        return code[current]

    action = "scanParamName" #scanParamValue
    #print("启动为",action)
    # 适用于没有换行符的解析 末尾字母参数
    tail = ""
    for index,char in enumerate(code):
        if char == "@":
            while peekNext() != " " and index != end:
                pass
            vc = code[index:current]
            tokens.append(vc)

        if char == " " and action == "scanParamName":
            sp_start = index + 1
            while peekNext() != "=" and index != end:
                #print(code[current])
                pass
            if code[current] == "=":
                action = "scanParamValue"
                vc = code[sp_start:current]
                tokens.append(vc)
                #print(vc)
                print("切换为",action)

        if char == "=" and action == "scanParamValue":
            while peekNext() != " " and current != end:
                print(code[current])
                tail += code[current]
            if code[current] == " " and current != end:
                action = "scanParamName"
                print("切换为",action)
            elif code[current] == " " and current == end:
                print("参数的末尾是空格 且代码已结束")
                break
        # 适用于没有换行符的解析 末尾字母参数
        if index == end and char != "\n":
            tail += code[end]
            tt = list(tail)
            del tt[0]
            rs = "".join(tt)
            print("换回来",rs)
            print("添加尾巴",rs)
            tokens.append(rs)
            break
        if char == "\n":
            break
    #print(tokens)
    return tokens