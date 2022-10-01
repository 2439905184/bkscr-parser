import SingleMacroParser as sp
import MulitMacroParser as mp

#mp.parse("")
file1 = open("test/单行.bkscr","r",encoding="utf-8-sig")
lines = file1.readlines()
#print(lines)
src = "".join(lines)
#print(src)
result = sp.parse(src)
print(result)
file1.close()