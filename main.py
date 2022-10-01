import SingleMacroParser as sp
import MulitMacroParser as mp

# 注意 此处默认使用utf-8 with bom 编码打开，因为bkengine的脚本编码默认就是这种的，麻了，直接全部转utf-8格式
srcfile = open("test/多行.bkscr","r",encoding="utf-8")
lines = srcfile.readlines()
print("所有行")
print(lines)
srcfile.close()

result = []

file_name = "out.txt"
out = open("compile_out/" + file_name,"w",encoding="utf-8")
for line in lines:
    buffer_line = ""
    if line[0] == "@":
        buffer_line = "\n".join(sp.parse(line))
        #print("缓冲区",buffer_line)
        result.append(buffer_line)
    if line[0] == "[":
        buffer_line = "\n".join(mp.parse(line))
        #print("缓冲区",buffer_line)
        result.append(buffer_line)
print("结果",result)
for element in result:
    out.write(element + "\n")
out.close()
