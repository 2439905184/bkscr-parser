# 在进入编译之前，先检查文件编码格式，如果不是utf-8，则转换为utf-8编码格式并覆盖源文件
import os
from chardet import detect
import ColorPrint

def encodeProject(dir:str) -> bool:
    ColorPrint.print_verbose_hint("开始转换工程的编码格式")
    L = []
    for root, dirs, files in os.walk(dir):
        #获得所有bkscr文件
        for file in files:
            if os.path.splitext(file)[1] == ".bkscr" or os.path.splitext(file)[1] == ".bkpsr":
                L.append(os.path.join(root, file))
    if len(L) > 0:
        for path in L:
            # print(path)
            #修改编码格式
            with open(path, 'rb+') as fp:
                old_content = fp.read()
                encoding = detect(old_content)['encoding']
                ColorPrint.print_verbose_hint("检测到编码 -> " + encoding)
                if encoding == "UTF-8-SIG":
                    content = old_content.decode(encoding).encode('utf8')
                    fp.seek(0)
                    fp.write(content)
                    ColorPrint.print_compile(old_content.decode("utf-8-sig"),content.decode("utf-8"))
                elif encoding == "utf-8" or encoding == "ascii": pass
                else:
                    ColorPrint.print_verbose_hint("暂时不支持转换的编码格式,或者你需要手动修改转换器代码并添加新的编码格式转换支持")
                    return False
    return True