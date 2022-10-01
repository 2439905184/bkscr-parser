def parse(code:str)->list:
    code = "@addto index=1280 p2=6\n"
    current = 0
    end = len(code) - 1
    tokens = []

    def peekNext():
        nonlocal current
        current += 1
        return code[current]

    action = "scanParamName" #scanParamValue
    #print("启动为",action)
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
                #print("切换为",action)

        if char == "=" and action == "scanParamValue":
            vc = ""
            while peekNext() != " " and current != end:
                #print(code[current])
                vc += code[current]
            #print(vc)
            tokens.append(vc)
            if code[current] == "\n":
                break
            if code[current] == " " and current == end:
                break
            if code[current] == " ":
                action = "scanParamName"
                #print("切换为",action)
    #print(tokens)
    return tokens