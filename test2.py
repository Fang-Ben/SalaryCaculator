from SalaryCaculator.test1 import v1_decoder, v2_decoder, v3_decoder
import pandas as pd
import numpy as np
from datetime import datetime

sheet_data = pd.read_excel('./sheet.xlsx')
sheet_data.fillna(0, inplace=True)
ls = ["Base", "2.5mm", "FP", "隔板", "U/管材", "mesh内",  "draw", "FIC_draw", "3point", "strut", "door", "ADD_1", "总计1",
      "rubber", "weld_rr", "mesh_out", "ADD_2", "总计2",  "Price_RR", "ADD_3", "自拿"]
order_num_lst,  data_res = [], []
for i in range(sheet_data.shape[0]):
    # transfer the data from sheet_data to V1_data
    v1_data = list(range(13))
    v1_data[0] = sheet_data.loc[i][2]
    v1_data[1] = sheet_data.loc[i][1]
    v1_data[2:12] = sheet_data.loc[i][3:13]
    v1_data[12] = sheet_data.loc[i]["附加价格"]
    # transfer the data from sheet_data to V2_data
    v2_data = list(range(4))
    v2_data[0:3] = sheet_data.loc[i]["胶皮":"铝网外"]
    v2_data[3] = sheet_data.loc[i][19]
    # transfer the data from sheet_data to V3_data
    v3_data = np.zeros(4, dtype=float)
    v3_data[0:3] = sheet_data.loc[i]["普通顶架":"顶架长度"]
    v3_data[3] = sheet_data.loc[i][24]
    # add order to order_lst
    order_num_lst.append(sheet_data.loc[i][0])
    # merge three of the data which decoded from decoder
    v1 = v1_decoder(v1_data)
    v2 = v2_decoder(v2_data)
    v3 = v3_decoder(v3_data, v1_data)
    data_res.append(np.hstack((v1, v2, v3)))

df = pd.DataFrame(data=data_res, index=order_num_lst, columns=ls)
df['total'] = df.apply(lambda x: x['总计1'] + x['总计2'], axis=1)
df = df[['Base', '2.5mm', 'FP', '隔板', 'U/管材', 'mesh内', 'draw', 'FIC_draw', '3point', 'strut', 'door', 'ADD_1', 'rubber', 'weld_rr', 'mesh_out', 'ADD_2',
         'Price_RR', 'ADD_3', '总计1', '总计2', 'total', '自拿']]
tmp = sum(df['total']) * 0.7 + sum(df['自拿'])
df.to_excel('方言啸{}.xlsx'.format(datetime.now().strftime("%d%m%y")))
print("税前收入:${}".format(tmp))






