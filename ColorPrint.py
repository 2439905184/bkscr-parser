"""终端的字符颜色是用转义序列控制的，是文本模式下的系统显示功能，和具体的语言无关。
   转义序列是以ESC开头,即用\033来完成（ESC的ASCII码用十进制表示是27，用八进制表示就是033）。
"""
def print_verbose(*args):
    '''
    :args: 可变参数[0]是输出提示，[1]是代码行
    '''
    to = "\033[0;33;40m" + args[0] + " -> " + args[1] + "\033[0m"
    print(to)

def print_compile(*args):
    '''
    :args: 可变参数[0]是附加提示，[1]是代码行
    '''
    #to = args[0] + "\033[0;32;40m"  + " -> " + "\033[0m" + args[1]
    source_in = "\033[0;34;40m"+ args[0] + "\033[0m"
    arrow = "->"
    compile_out = "\033[0;32;40m"+ args[1] + "\033[0m"
    out = source_in + " " + arrow + " " + compile_out
    print(out)

# 仅输出一次详细输出提示，在开始所有详细输出之前调用一次
def print_verbose_once():
    print("\033[1;31;40m详细输出\033[0m")

# 仅输出一次编译开始提示，在所有编译开始之前调用一次
def print_compile_once():
    print("\033[1;31;40m开始编译\033[0m")

# 可重复使用的函数
def print_verbose_hint(arg:str):
    print("\033[1;31;40m" + arg + "\033[0m")

def test():        
    print_verbose_hint()
    for i in range(20):
        print_verbose("@init","提示")
    print_compile_once()
    for i in range(20):
        print_compile("@sprite","提示")

#test()