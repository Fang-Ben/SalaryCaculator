from .docs.conf import box_price, accessories_internal, thickness, flat_plat, box_ratio, canopy_ratio, series_name, \
    canopy_price, special_name1, special_name2, special_name3, init_divider, init_door, canopy_name, init_strut
import numpy as np


"""
暂时定义为三个向量V1，v2，v3分别为
V1：里面所有的数据都是要乘折板系数的
V2：是不需要乘折板系数但是需要乘装箱系数的
V3：是自拿不需要分出去的
"""


def len_object(v1_data):
    """"
    input data_len return [length, price_thi, price_fp]
    then use another function to pick data from the list
    """
    lst = []
    if v1_data[0] <= 1200:
        length = str(1200)
    elif 1200 < v1_data[0] <= 1500:
        length = str(1500)
    elif 1500 < v1_data[0] <= 1800:
        length = str(1800)
    elif 1800 < v1_data[0] <= 2000:
        length = str(2000)
    else:
        length = str(2001)
    lst.append(length)
    lst.append(thickness[length])
    lst.append(flat_plat[length])
    return lst


def init_data(v1_data):
    door_init, divider_init, strut_init, code, lst = 0, 0, 0, v1_data[2], []
    if v1_data[1][0] == 0:
        if v1_data[1][1] in init_door:
            door_init = 1
        if v1_data[1][1] in init_divider:
            divider_init = -1
        if v1_data[1][1] in init_strut:
            strut_init = -2
        if v1_data[1][1] in special_name1:
            code = "fil"
        if v1_data[1][1] in special_name2:
            code = "rec"
        if v1_data[1][1] in special_name3:
            code = "sts"
    lst.append(door_init), lst.append(divider_init), lst.append(strut_init), lst.append(code)
    return lst


def v3_decoder(v3_data, v1_data):
    """"
    v3_data = [x, x]
    index_0 = Norm RR
    index_1 = heavy duty RR
    index_2 = len of RR
    index_3 = ADD
    return [x, x] index_0 = price, index_1 = name
    """
    lst = np.zeros(3, dtype=float)
    if v3_data[0] == 1:
        price_rr = 40.0
    elif v3_data[1] == 1:
        if v3_data[2] <= 1999:
            price_rr = 50.0
        elif 2000 <= v3_data[2] <= 3000:
            price_rr = 60.0
        else:
            price_rr = 70.0
    else:
        price_rr = 0.0
    if v1_data[1] == "sb":
        lst[2] += 380.0
    lst[0] = price_rr
    lst[1] = v3_data[3]
    lst[2] = lst[2] + lst[0] + lst[1]
    return lst


def v2_decoder(v2_data):
    """
    v2_data = [x, x, x, x, x]
    index_0 = num of rubber
    index_1 = flag of weld the RR 0 = False, 1 = True
    index_2 = num of mesh of outside
    index_3 = additional price(total)
    return total price
    """
    lst = np.zeros(5, dtype=float)
    lst[0] = v2_data[0]*accessories_internal["rubber"]
    lst[1] = v2_data[1]*accessories_internal["weld_rr"]
    lst[2] = v2_data[2]*accessories_internal["mesh"]
    lst[3] = v2_data[3]
    lst[4] = sum(lst[0:4])
    return lst


def v1_decoder(v1_data):
    """
    v1_data is list
    index_0: len_data
    index_1: [name]
    index_2: flag of 2.5mm---> 0:False 1: True
    index_3: flag of FP  ----> same above
    index_4: num of norm Divider
    index_5: num of U/tube/any price in $2
    index_6: num of mesh which inside
    index_7: num of Norm Draw
    index_8: num of FIC Draw
    index_9: num of lock in 3_point or center lock
    index_10: num of strut
    index_11: num of add_door
    index_12: addition list [total price, "name"]
    """
    # index_0 not need return so np.zeros only 11 element in the list
    lst = np.zeros(13, dtype=float)
    # TODO replace special name !!caution the
    if v1_data[1] in series_name:
        code = v1_data[1]
        if v1_data[1] in special_name1:
            code = "fil"
        elif v1_data[1] in special_name2:
            code = "rec"
        elif v1_data[1] in special_name3:
            code = "sts"
        lst[0] = box_price[code+str(len_object(v1_data)[0])]
    elif v1_data[1] in canopy_name:
        lst[0] = canopy_price[v1_data[1]]
    elif v1_data[1] == "sb":
        lst[0] = 0
    if v1_data[2] == 1:
        lst[1] = len_object(v1_data)[1]
    if v1_data[3] == 1:
        lst[2] = len_object(v1_data)[2]
    lst[3] = (v1_data[4]+init_data(v1_data)[1])*accessories_internal["divider"]
    lst[4] = v1_data[5]*accessories_internal["U"]
    lst[5] = v1_data[6]*accessories_internal["mesh"]
    lst[6] = v1_data[7]*accessories_internal["draw"]
    lst[7] = v1_data[8]*accessories_internal["fic_draw"]
    lst[8] = v1_data[9]*accessories_internal["3_point"]
    lst[9] = (v1_data[10]+init_data(v1_data)[2])*accessories_internal["strut"]
    lst[10] = (v1_data[11]+init_data(v1_data)[0])*accessories_internal["door"]
    lst[11] = v1_data[12]
    if v1_data[1] in series_name:
        lst[12] = sum(lst[0:12]) * box_ratio
    elif v1_data[1] == "sb":
        lst[12] = sum(lst[3:12]) * canopy_ratio
    elif v1_data[1] in canopy_name:
        lst[12] = sum(lst[0:12]) * canopy_ratio
    return lst











