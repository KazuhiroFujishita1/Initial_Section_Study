import pandas as pd
import math

#初期仮定断面の設定
#Excelで入力した全柱梁部材に対して初期仮定断面を算定する
def set_initial_section(beam,column,layer):

    #選定候補部材リストの読み込み
    column_list = pd.read_csv("column_list.csv",header = 0)
    beam_list = pd.read_csv("beam_list.csv",header = 0)

    #初期柱せいの算定(適用高さ上限45m）
    column_W = [];column_Ix = []
    maximum_height = sum(layer.height)#建物高さ
    for i in range(len(column.no)):
        temp = math.ceil(((maximum_height+20) *10)/50)*50#鹿島様略算式
        if temp >600:
            column_W.append(600)
        elif temp <= 600 and temp >= 300:
            column_W.append(temp)
        elif temp < 300:
            column_W.append(300)
        #算定柱せいに適合する柱の断面二次モーメントの出力
        target_row = column_list[column_list['H'] == column_W[i]]
        column_Ix.append(float(target_row['Ix']))

    #初期梁せいの算定
    beam_H = [];beam_Ix = []
    for i in range(len(beam.no_all)):
        temp = math.ceil((beam.length[i]*1000/18)/100)*100#鹿島様略算式
        if temp < 500:
            beam_H.append(500)
        elif temp > 900:
            beam_H.append(900)
        else:
            beam_H.append(temp)

        #算定梁せいに適合する梁の断面二次モーメントの出力
        target_row = beam_list[beam_list['H'] == beam_H[i]]
        beam_Ix.append(float(target_row['Ix']))

    return column_Ix,beam_Ix

