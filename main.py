import os
import sys
import Encoder
import SingleMacroParser as sp
import MulitMacroParser as mp
import ColorPrint

# 都是string类型
params = ""
param_input_dir = None 
param_verbose = None
# 用于扫描器的独立参数
verbose_enabled = False

def getParams() -> list:
    params = []
    args = sys.argv
    params = args[1:len(args)]
    print(params)
    return params

# 查错
try:
    params = getParams()
    # print(params)
except IndexError:
    print("数组越界或者数组参数过少!")
else:
    if len(params) == 1:
        param_input_dir = params[0]
    if len(params) == 2:
        param_input_dir = params[0]
        param_verbose = params[1]

if param_verbose == "verbose":
    verbose_enabled = True

filein = "bkscr/多行.bkscr"
fileout = "compile_out/out.txt" # 备份 fileout = filein.replace(".bkscr",".txt")

ColorPrint.print_verbose_once()
ColorPrint.print_compile_once()
ColorPrint.print_verbose_hint("输入文件夹 -> " + param_input_dir)
ColorPrint.print_verbose_hint("输出文件 -> " + fileout)

if param_input_dir != None:
    if Encoder.encodeProject(param_input_dir,verbose_enabled):
        srcfile = open(filein,"r",encoding="utf-8")
        lines = srcfile.readlines()
        # print("所有行")
        # #print(lines)
        srcfile.close()
        out = open(fileout,"w",encoding="utf-8")
        # result = [] 以后可能要用到的变量 先暂时备份
        # 逐行扫描
        for index,line in enumerate(lines):
            currentScanLine = index + 1
            # 每一行的结果 如果遇到注释行，则会丢弃那一行
            buffer_array = []
            # if line[0] == "@":
            #     buffer_line = "\n".join(sp.parse(line))
            #     #print("缓冲区",buffer_line)
            #     result.append(buffer_line)
            if line[0] == "[":
                lineToken:list = mp.parse(code=line, scanLine=currentScanLine, verbose=verbose_enabled)
                for element in lineToken:
                    #print(currentScanLine, buffer_array)
                    out.write(element + "\n")
                #result.append(buffer_array)
        out.close()