import os
import sys
import Encoder
import SingleMacroParser as sp
import MulitMacroParser as mp
import ColorPrint
import 预处理
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

# filein = "bkscr/多行.bkscr"
# filein =  os.path.split(param_input_dir)[1] # 多好.bkscr
# fileout = "",filein.replace(".bkscr",".txt")
# fileout = "compile_out/out.txt" # 备份 fileout = filein.replace(".bkscr",".txt")

ColorPrint.print_verbose_once()
ColorPrint.print_compile_once()
ColorPrint.print_verbose_hint("输入文件夹 -> " + param_input_dir)
# ColorPrint.print_verbose_hint("输出文件 -> " + fileout)

def getAllBkscr(p_dir) -> list:
    L = []
    for root, dirs, files in os.walk(p_dir):
        #获得所有bkscr文件
        for file in files:
            if os.path.splitext(file)[1] == ".bkscr":
                if file != "macro.bkscr":
                    L.append(os.path.join(root, file))
    return L

# 先预处理一变所有文件的所有行的开头和结尾的空格 因为这个空格是非必要的,而且三种格式可能都存在首尾空格,所以去除空格并不会影响游戏代码
def preCompile(eachFile: str) -> list:
    result = [] # string []
    # 针对每个文件，读取每个文件的所有行
    each_lines:str = eachFile.readlines()
    for lines in each_lines:
        result.append(预处理.处理("单行宏",lines,verbose_enabled))
        ColorPrint.print_compile("预处理结果",str(result))

    return result
# 过程 getAllBkscr -> preCompile -> compile
def compileProject(p_dir,p_verbose):
    all_FilePaths:list = getAllBkscr(p_dir)

    for each_FilePath in all_FilePaths:
        with open(each_FilePath,"r",encoding="utf-8") as eachFile:
            # filein =  os.path.split(param_input_dir)[1] # 多好.bkscr
            # fileout filein.replace(".bkscr",".txt")
            p = os.path.split(each_FilePath)
            output_name = "compile_out/" + p[1].replace(".bkscr",".txt")
            FileOut = open(output_name,"w",encoding="utf-8")
            # 这里的预处理结果是当前的一行
            每一行的预处理结果:list = preCompile(eachFile)
            # ColorPrint.print_compile("预处理结果",str(预处理结果))
            for index,line in enumerate(每一行的预处理结果):
                currentScanLine = index + 1
                if line[0] == "@":
                    lineToken:list = sp.parse(line,currentScanLine,verbose_enabled)
                    #print("缓冲区",buffer_line)
                    for element in lineToken:
                        # print(currentScanLine, buffer_array)
                        
                        FileOut.write(element + "\n")
                    # result.append(buffer_line)
                if line[0] == "[":
                    lineToken:list = mp.parse(line,currentScanLine,verbose_enabled)
                    for element in lineToken:
            #             #print(currentScanLine, buffer_array)
                        FileOut.write(element + "\n")
            #         #result.append(buffer_array)

if param_input_dir != None:
    if Encoder.encodeProject(param_input_dir,verbose_enabled):
        compileProject(param_input_dir,verbose_enabled)
        # srcfile = open(filein,"r",encoding="utf-8")
        # lines = srcfile.readlines()
        # srcfile.close()
        # # print("所有行")
        # # #print(lines)
        
        # out = open(fileout,"w",encoding="utf-8")
        
        # 预处理结果 = [] # string []
        # for line in lines:
        #     预处理结果.append(预处理.处理("单行宏",line,verbose_enabled))
        # ColorPrint.print_compile("预处理结果",str(预处理结果))

        # # 逐行扫描
        # for index,line in enumerate(lines):
        #     currentScanLine = index + 1
        # #     # 每一行的结果 如果遇到注释行，则会丢弃那一行
        # #     buffer_array = []
        #     if line[0] == "@":
        #         lineToken:list = sp.parse(line,currentScanLine,verbose_enabled)
        #         #print("缓冲区",buffer_line)
        #         for element in lineToken:
        #             # print(currentScanLine, buffer_array)
                
        #             out.write(element + "\n")
        #         # result.append(buffer_line)
        #     if line[0] == "[":
        #         lineToken:list = mp.parse(code=line, scanLine=currentScanLine, verbose=verbose_enabled)
        #         for element in lineToken:
        # #             #print(currentScanLine, buffer_array)
        #             out.write(element + "\n")
        # #         #result.append(buffer_array)
        # out.close()