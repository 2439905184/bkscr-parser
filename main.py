import os
import sys
import SingleMacroParser as sp
import MulitMacroParser as mp
import ColorPrint
arg = sys.argv[1]
print("输入文件",arg)
filein = os.path.split(arg)[1]
if len(sys.argv) == 3:
    argv_verbose = sys.argv[2]
else:
    argv_verbose = None
# 注意 此处默认使用utf-8 with bom 编码打开，因为bkengine的脚本编码默认就是这种的，麻了，直接全部转utf-8格式
srcfile = open(arg,"r",encoding="utf-8")
lines = srcfile.readlines()
#print("所有行")
#print(lines)
srcfile.close()

result = []

fileout = filein.replace(".bkscr",".txt")
print("输出文件",fileout)
# file_name = arg
out = open("compile_out/" + fileout,"w+",encoding="utf-8")
currentScanLine = 0

if argv_verbose == "verbose":
    verbose_mode = True
else:
    verbose_mode = False
if verbose_mode:
    ColorPrint.print_verbose_once()
    ColorPrint.print_compile_once()
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
        lineToken:list = mp.parse(code=line, scanLine=currentScanLine, verbose=verbose_mode)
        for element in lineToken:
            #print(currentScanLine, buffer_array)
            out.write(element + "\n")
        #result.append(buffer_array)
out.close()
