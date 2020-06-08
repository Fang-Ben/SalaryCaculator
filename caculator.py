from docs.conf import box_price, accessories_internal, thickness, flat_plat, box_ratio, canopy_ratio, series_name
import os
from datetime import datetime


file_path, file_name = os.getcwd(), datetime.now().strftime("%d%m%y")


# 所有价格预处理和计算单元.
def getdata():
    code_data, rr_nj_data = get_code(), rr_nj()
    length_data, price_thick, price_fp = get_length()
    base_code = code_data[0] + length_data
    init_divider, init_door, = code_data[2], code_data[1]
    price_rr, rr_name, price_nj, nj_name = rr_nj_data[0], rr_nj_data[1], rr_nj_data[2], rr_nj_data[3]
    price_divi = (int(input("请输入隔板数量:")) + init_divider) * accessories_internal["divider"]
    tube_u = (int(input("请输入U槽/方管/圆管数量:"))) * accessories_internal["U"]
    price_mesh = (int(input("请输入铝网数量"))) * accessories_internal["mesh"]
    price_draw = (int(input("请输入内抽数量"))) * accessories_internal["door"]
    price_fic_draw = (int(input("FIC抽数量"))) * accessories_internal["fic_draw"]
    price_door = (int(input("请输入新增门数的数量")) + init_door) * accessories_internal["door"]
    price_weld_rr = (int(input("请输入焊接标准顶架数量"))) * accessories_internal["weld_rr"]
    price_3_point = (int(input("请输入3点(中控)锁数量"))) * accessories_internal["3_point"]
    price_base = (int(input("请输入base数量"))) * accessories_internal["base"]
    # print(box_price[base_code], price_divi, tube_u, price_mesh, price_door, price_rr, price_weld_rr, price_3_point,
    #       price_base, price_draw, price_fic_draw, price_thick, price_fp)
    return box_price[base_code], price_thick, price_fp, price_divi, tube_u, price_mesh, price_door, price_base, \
        price_draw, price_fic_draw, price_rr, rr_name, nj_name, price_nj, price_weld_rr, price_3_point


# 厚度和平铝计算
def thick_fp_data():
    price_thick, price_fp = 0, 0
    thick_data = input("是2.5毫米厚吗?y/n")
    fp_data = input("是平铝吗?y/n")
    if thick_data == "y":
        price_thick = get_length()[1]
    elif fp_data == "y":
        price_fp = get_length()[2]
    return price_thick, price_fp


def additional():
    additional_data, additional_price = [], []
    while True:
        input_str = input("还有其他附加件和价格没有列出吗?y/n")
        if input_str == "y":
            additional_data.append(input("请输入还有那些附加件?")), additional_price.append(int(input("请输入附加件价格")))
        else:
            break
    return additional_data, additional_price


# box_price[base_code], price_thick, price_fp, price_divi, tube_u, price_mesh, price_door, price_base, price_draw,
# price_fic_draw,
# 10.price_rr, rr_name, nj_name, price_nj, price_weld_rr, price_3_point
# additional_data是一个二维元组([additional_data],[additional_price])
# TODO: 写入到文件
def print_():
    order_num = input("请输入订单号:")
    data = getdata()
    additional_data = additional()
    price_after_fold = sum(data[0:9]) * box_ratio
    price_before_fit = price_after_fold + sum(additional_data[1][:])
    with open(file_name,  mode='a') as f:
        print("订单号{}折板后价格是${}=(系列价格${}".format(order_num, price_before_fit, data[0]), end="", file=f)
        if data[1] != 0:
            print("+2.5mm价格${}".format(data[1]), end="", file=f)
        if data[2] != 0:
            print("+平铝价格${}".format(data[2]), end="", file=f)
        if data[3] != 0:
            print("+搁板价格${}".format(data[3]), end="", file=f)
        if data[4] != 0:
            print("+(U槽/圆管/方管)总价${}".format(data[4]), end="", file=f)
        if data[5] != 0:
            print("+铝网价格${}".format(data[5]), end="", file=f)
        if data[6] != 0:
            print("+新增门价格${}".format(data[6]), end="", file=f)
        if data[7] != 0:
            print("+Base价格${}".format(data[7]), end="", file=f)
        if data[8] != 0:
            print("+内抽价格${}".format(data[8]), end="", file=f)
        if data[9] != 0:
            print("+FIC抽价格${}".format(data[9]), end="", file=f)
        print(")X0.775", end="", file=f)
        if data[14] != 0:
            print("+焊接顶架价格${}".format(data[14]), end="", file=f)
        elif data[15] != 0:
            print("+三点锁价格${}".format(data[15]), end="", file=f)
        price_for_self = data[10] + data[13]
        if data[10] != 0:
            print("\tPLUS!!!!!定制{}${},焊工自切自拿".format(data[11], data[10]), file=f)
        elif data[13] != 0:
            print("\tPLUS!!!!!{}价格${},焊工自切自拿".format(data[12], data[13]), file=f)
        elif len(additional_data[0]) != 0:
            print("\t附加件有:", end="", file=f)
            for i, j in zip(additional_data[0], additional_data[1]):
                print(i, ":", "$", j, end=" ", file=f)
        print("\n", file=f)
        f.close()
    return price_before_fit, price_for_self


# 通过输入长度自动生成标准box_price中的格式
# 判断输入为DBL,FID,DBU自动按照双门计算.
# 判断输入为"FID" or "DBU" or "TSO"时 门的初始化+1
# 判断输入为"UTTI" or "UTTE" or "TB"时 撑杆初始化-2
def get_code():
    while True:
        series_code = input("清输入型号")
        if series_code in series_name:
            break
        else:
            print("输入的型号不在列表中,请核实后再次输入!")
    init_door, init_divider, code = 0, 0, ""
    if series_code == "DBL" or "FID" or "DBU":
        init_door = 1
    if series_code == "FID" or "DBU" or "TSO":
        init_divider = -1
    if series_code == "FID" or "FIS":
        code = "FIL"
    if series_code == "DBL":
        code = "REC"
    if series_code == "DBU":
        code = "STS"
    return code, init_door, init_divider


# 根据输入的长度格式化为系统规定的长度显示.并且自动计算出材料种类和厚度价格的变化
def get_length():
    length = input("请输入长度")
    if int(length) <= 1200:
        length = str(1200)
    elif 1200 < int(length) <= 1500:
        length = str(1500)
    elif 1500 < int(length) <= 1800:
        length = str(1800)
    elif 1800 < int(length) <= 2000:
        length = str(2000)
    else:
        length = str(2001)
    price_thick, price_fp = 0, 0
    thick_data = input("是2.5毫米厚吗?y/n")
    fp_data = input("是平铝吗?y/n")
    if thick_data == "y":
        price_thick = thickness[length]
    elif fp_data == "y":
        price_fp = flat_plat[length]
    return length, price_thick, price_fp


# 顶架和牛角的计算函数
def rr_nj():
    tmp1 = input("是否自制顶架?y/n")
    price_nj, nj_name = 0, None
    price_rr, rr_name = 0, None
    if tmp1 == "y":
        tmp2 = int(input("1:Heavy duty 2:普通顶架? 1/2"))
        if tmp2 == 1:
            length = int(input("输入顶架长度?"))
            if length <= 1999:
                price_rr = 50
            elif 2000 <= length <= 3000:
                price_rr = 60
            else:
                price_rr = 70
            rr_name = "Heavy duty顶架"
        else:
            price_rr, rr_name = 40, "普通顶架"
    else:
        tmp3 = input("是否有牛角?/y/n")
        if tmp3 == "y":
            num = int(input("请输入牛角个数"))
            price_nj, nj_name = 5 * num, "牛角"
    return price_rr, rr_name, price_nj, nj_name

