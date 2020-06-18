from docs.conf import box_price, accessories_internal, thickness, flat_plat, box_ratio, canopy_ratio, series_name, \
    canopy_price, special_name1, special_name2, special_name3, init_divider, init_door, canopy_name, init_strut
import os
from datetime import datetime


file_path, file_name = os.getcwd(), datetime.now().strftime("%d%m%y")


# 所有价格预处理和计算单元.
def getdata():
    code_data, rr_nj_data = get_code(), rr_nj()
    length_data, price_thick, price_fp = get_length()
    price_box, price_canopy = 0, 0
    if code_data[0] == "0":
        base_code = code_data[0]
    elif code_data[0] in series_name:
        base_code = code_data[0] + length_data
        price_box = box_price[base_code]
    else:
        base_code = code_data[0]
        price_canopy = canopy_price[base_code]
    divider_init, door_init, strut_init = code_data[2], code_data[1], code_data[3]
    price_rr, rr_name, price_nj, nj_name = rr_nj_data[0], rr_nj_data[1], rr_nj_data[2], rr_nj_data[3]
    price_divi = (int(input("请输入隔板数量:")) + divider_init) * accessories_internal["divider"]
    tube_u = (int(input("请输入U槽/方管/圆管数量:"))) * accessories_internal["U"]
    price_strut = strut_init * accessories_internal["strut"]
    price_draw = (int(input("请输入内抽数量"))) * accessories_internal["draw"]
    price_fic_draw = (int(input("FIC抽数量"))) * accessories_internal["fic_draw"]
    price_door = (int(input("请输入新增门数的数量")) + door_init) * accessories_internal["door"]
    price_weld_rr = (int(input("请输入焊接标准顶架数量"))) * accessories_internal["weld_rr"]
    price_3_point = (int(input("请输入3点(中控)锁数量"))) * accessories_internal["3_point"]
    price_rubber = (int(input("请输入胶皮数量"))) * accessories_internal["rubber"]
    num_ = int(input("本单还有几个重复?"))
    if num_ is None:
        num_ = 1
    return price_box, price_thick, price_fp, price_divi, tube_u, price_door, price_draw, price_fic_draw, \
        price_rubber, price_rr, rr_name, nj_name, price_nj, price_weld_rr, price_3_point, price_canopy, base_code, \
        price_strut, num_


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
    additional_data1, additional_data2, additional_price1, additional_price2 = [], [], [], []
    while True:
        input_str = input("1:有折板的附加件。2无折板的附加件。其他键结束")
        if input_str == "1":
            additional_data1.append(input("请输入附加件?")), additional_price1.append(int(input("请输入附加件价格")))
        elif input_str == "2":
            additional_data2.append(input("请输入附加件?")), additional_price2.append(int(input("请输入附加件价格")))
        else:
            break
    return additional_data1, additional_data2, additional_price1, additional_price2


# 0 price_box, price_thick, price_fp, price_divi, tube_u, price_door, price_draw, price_fic_draw, \
# 8  price_rubber, price_rr, rr_name, nj_name, price_nj, price_weld_rr, price_3_point, price_canopy, base_code,
# 17 price_strut, num_
# additional_data是一个二维元组([additional_data1], [additional_data2], [additional_price1], [additional_price2]
def print_():
    order_num = input("请输入订单号:")
    data, additional_data, price_after_fold = getdata(), additional(), 0
    if data[0] != 0:
        price_after_fold = (sum(data[0:7])+data[14]+data[17]+sum(additional_data[2][:])) * box_ratio
    elif data[0] ==0 and data[16] == "0":
        price_after_fold = (sum(data[0:7]) + data[14] + data[17]+sum(additional_data[2][:])) * box_ratio
    elif data[0] == 0:
        price_after_fold = (data[17]+data[15]+data[14]+sum(data[1:7])) * canopy_ratio
    price_before_fit = (price_after_fold + data[8] + data[12] + data[13] + sum(additional_data[3][:]))*(1+data[18])
    with open(file_name,  mode='a') as f:
        if data[0] != 0:
            print("{}\t${}=({} ${}".format(order_num, round(price_before_fit, 3), data[16], data[0]),
                  end="", file=f)
        else:
            print("{}\t${}=({} ${}".format(order_num, round(price_before_fit, 3), data[16], data[15]),
                  end="", file=f)
        if data[1] != 0:
            print("+2.5${}".format(data[1]), end="", file=f)
        if data[2] != 0:
            print("+fp${}".format(data[2]), end="", file=f)
        if data[3] != 0:
            print("+隔${}".format(data[3]), end="", file=f)
        if data[4] != 0:
            print("+(U/圆/方)${}".format(data[4]), end="", file=f)
        if data[5] != 0:
            print("+门${}".format(data[5]), end="", file=f)
        if data[6] != 0:
            print("+内抽${}".format(data[6]), end="", file=f)
        if data[7] != 0:
            print("+FIC${}".format(data[7]), end="", file=f)
        if data[17] != 0:
            print("+撑杆${}".format(data[18]), end="", file=f)
        if data[14] != 0:
            print("+三点${}".format(data[14]), end="", file=f)
        if len(additional_data[0]) != 0:
            for i, j in zip(additional_data[0], additional_data[2]):
                print("+", i, "$", j, end=" ", file=f)
        if data[0] != 0:
            print(")X0.775", end="", file=f)
        elif data[0] == 0 and data[16] == "0":
            print(")X0.775", end="", file=f)
        else:
            print(")X0.925", end="", file=f)
        if data[8] != 0:
            print("+胶皮${}".format(data[8]), end="", file=f)
        if data[13] != 0:
            print("+焊顶架${}".format(data[13]), end="", file=f)
        price_for_self = data[9] + data[12]
        if data[9] != 0:
            print("\tPLUS!!!!!定制{}${},焊工自切自拿".format(data[10], data[9]), end="", file=f)
        if data[12] != 0:
            print("\tPLUS!!!!!{}价格${},焊工自切自拿".format(data[11], data[12]), end="", file=f)
        if len(additional_data[1]) != 0:
            print("\t附加件有:", end="", file=f)
            for i, j in zip(additional_data[1], additional_data[3]):
                print(i, ":", "$", j, end=" ", file=f)
        if data[18] >= 0:
            print("\t共有{}份".format(1+data[18]), end="", file=f)
        print("\n", file=f)
        f.close()
    return price_before_fit, price_for_self


# 通过输入长度自动生成标准box_price中的格式
# 判断输入为DBL,FID,DBU自动按照双门计算.
# 判断输入为"FID" or "DBU" or "TSO"时 隔板初始化-1
# 判断输入为"UTTI" or "UTTE" or "TB"时 撑杆初始化-2
def get_code():
    while True:
        series_code = input("*******请输入型号:")
        if series_code in series_name:
            break
        elif series_code == "0":
            break
        elif series_code in canopy_name:
            break
        else:
            print("!!!!!!!输入的型号不在列表中,请核实后再次输入!")
    door_init, divider_init, code, strut_init = 0, 0, series_code, 0
    if series_code in init_door:
        door_init = 1
    if series_code in init_divider:
        divider_init = -1
    if series_code in init_strut:
        strut_init = -2
    if series_code in special_name1:
        code = "fil"
    elif series_code in special_name2:
        code = "rec"
    elif series_code in special_name3:
        code = "sts"
    else:
        code = series_code
    return code, door_init, divider_init, strut_init


# 根据输入的长度格式化为系统规定的长度显示.并且自动计算出材料种类和厚度价格的变化
def get_length():
    length_input = input("请输入长度")
    if int(length_input) <= 1200:
        length = str(1200)
    elif 1200 < int(length_input) <= 1500:
        length = str(1500)
    elif 1500 < int(length_input) <= 1800:
        length = str(1800)
    elif 1800 < int(length_input) <= 2000:
        length = str(2000)
    else:
        length = str(2001)
    price_thick, price_fp = 0, 0
    thick_data = input("是2.5毫米厚吗?y/n")
    fp_data = input("是平铝吗?y/n")
    if thick_data == "y":
        price_thick = thickness[length]
    if fp_data == "y":
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

