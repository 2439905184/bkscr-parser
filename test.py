import 预处理
# 测试单行宏预处理
def test_single():
    filein = "bkscr/单行.bkscr"
    srcfile = open(filein,"r",encoding="utf-8")
    lines = srcfile.readlines()
    srcfile.close()
    预处理结果 = [] # string []
    for line in lines:
        预处理结果.append(预处理.处理("单行宏",line,True))
    return 预处理结果

a = test_single()
print("结果")
print(a)