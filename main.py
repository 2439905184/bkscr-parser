import SingleMacroParser as sp
import MulitMacroParser as mp

#mp.parse("")
# 注意 此处默认使用utf-8 with bom 编码打开，因为bkengine的脚本编码默认就是这种的，麻了，直接全部转utf-8格式
file1 = open("test/单行.bkscr","r",encoding="utf-8")
lines = file1.readlines()
print("所有行")
print(lines)


result = []
for line in lines:
    if line[0] == "@":
        result = sp.parse(line)
        break
    # if line[0] == "[":
    #     pass
#src = "".join(lines)
# print(src)
# result = sp.parse(src)
print("结果")
print(result)
file_name = "out.txt"
out = open("compile_out/" + file_name,"w",encoding="utf-8")
for element in result:
    out.write(element + "\n")
out.close()
file1.close()