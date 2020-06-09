from caculator import print_
import os
from datetime import datetime

file_path, file_name = os.getcwd(), datetime.now().strftime("%d%m%y")

# TODO: print_里面有两个返回值每次调用print_()函数记得作sum.
# TODO: 写一个循环,直到输入特殊终止符比如END,终止print_()函数,两个sum的返回值也写入到同一个文件.
if __name__ == "__main__":
    print("程序开始")
    price_before_fit, price_for_self = 0, 0
    while True:
        input_keyb = input("确定结束吗?END结束,任意键继续")
        if input_keyb == "END":
            with open(file_name, mode='a') as f:
                print("总计:${}\t个人自拿${}\t本人到帐${}".format(round(price_before_fit, 3), round(price_for_self, 3),
                                                        round(price_before_fit*0.7+price_for_self, 3)), end="\n", file=f)
                print("程序结束")
            break
        else:
            price_before_fit_, price_for_self_ = print_()
            price_before_fit += price_before_fit_
            price_for_self += price_for_self_
            print("计算,累加成功!")

