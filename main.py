"""
def 多行宏解析单元():
    labels = []
    current_line_type = ""
    file = open("test/main.bkscr","r",encoding="utf-8")
    for line in file.readlines():
        print(line)
        for char in line:
            if char == "*":
                current_line_type = "label"
                break
            if char == "[" or char == "]":
                current_line_type = "mulit_macro"
                break
        if current_line_type == "label":
            current_label = line
            labels.append(current_label)
        if current_line_type == "mulit_macro":

    
多行宏解析单元() """

import scanner

def run(source):
    bkscrScanner = scanner.Scanner(source)
    tokens = bkscrScanner.scanTokens()
    #print(bkscrScanner)
    print(tokens)
    #for token in tokens:
        # print(token)
def runFile():
    file = open("test/main.bkscr","r",encoding="utf-8")
    content = file.read()
    #print(content)
    run(content)
    file.close()
runFile()