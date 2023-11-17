import pandas as pd
import math

#初期仮定断面の設定
#Excelで入力した全柱梁部材に対して初期仮定断面を算定する
def set_initial_section(beams, columns, maximum_height):

    #選定候補部材リストの読み込み
    column_list = pd.read_csv("column_list.csv",header = 0)
    beam_list = pd.read_csv("beam_list.csv",header = 0)

    #初期柱せいの算定(適用高さ上限45m）
    column_KX =[];column_KY =[]
    for i in columns:
        temp = math.ceil(((maximum_height+20) *10)/50)*50#鹿島様略算式
        if temp >600:
            column_W = 600
        elif temp <= 600 and temp >= 300:
            column_W = temp
        elif temp < 300:
            column_W = 300
        #算定柱せいに適合する柱の断面二次モーメントの出力
        target_row = column_list[column_list['H'] == column_W]
        i.Ix = float(target_row['Ix'])
        i.Iy = float(target_row['Iy'])
        #柱の剛度の算定(単位cm3）
        column_KX.append(i.Ix/i.length*1000000)
        column_KY.append(i.Iy/i.length*1000000)
        #部材自重の算定
        i.unit_weight = float(target_row["unit_m"]*9.80665/1000)
        i.weight = i.unit_weight * i.length #部材自重

    # 柱の剛比算定（柱の剛度の最大値を標準剛度とみなし1とする）
    maximum_KX = max(column_KX)
    maximum_KY = max(column_KY)
    temp = 0
    for i in columns:
        i.stiff_ratio_x = column_KX[temp]/maximum_KX
        i.stiff_ratio_y = column_KY[temp] / maximum_KY
        temp += 1

    #初期梁せいの算定
    beam_K = []
    temp2=0
    for i in beams:
        temp = math.ceil((i.length*1000/18)/100)*100#鹿島様略算式
        if temp < 500:
            beam_H = 500
        elif temp > 900:
            beam_H = 900
        else:
            beam_H = temp

        #算定梁せいに適合する梁の断面二次モーメントの出力
        target_row = beam_list[beam_list['H'] == beam_H]
        i.I = float(target_row['Ix'])
        #梁の剛度の算定(単位cm3）
        beam_K.append(i.I/i.length*1000000)
        # 部材自重の算定
        i.unit_weight = float(target_row["unit_m"]*9.80665/1000)
        i.weight = i.unit_weight * i.length  # 部材自重

        i.stiff_ratio = beam_K[temp2]/maximum_KX
        temp2 += 1