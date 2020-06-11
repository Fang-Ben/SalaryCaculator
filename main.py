from caculator import print_
import os
from datetime import datetime

file_path, file_name = os.getcwd(), datetime.now().strftime("%d%m%y")

# TODO: 添加容错机制避免中间环节出错不用报警而是再来一变循环,添加输入制作数量(默认是1)
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
            try:
                price_before_fit_, price_for_self_ = print_()
            except KeyError:
                print("型号不在数据库中,请核对信息")
                continue
            except ValueError:
                print("配件数字输入错误.")
                continue
            else:
                price_before_fit += price_before_fit_
                price_for_self += price_for_self_
                print("计算,累加成功!")

