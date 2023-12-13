import pandas as pd
import math
import numpy as np
import itertools
import member_class

#部材のグルーピング
def make_group(list,list_name,key1,key2):

    data_frame = pd.DataFrame(list, columns=list_name)
    sorted_frame = data_frame.sort_values(by=[key1, key2])

    group_data = []
    temp = 1
    for name, group in sorted_frame.groupby([key1]):
        for name2, group2 in group.groupby([key2]):
            group_data.append((temp, str(name) + 'F_' + str(name2), group2['No'].values.tolist()))
            temp += 1

    return group_data

#初期仮定断面の設定
#Excelで入力した全柱梁部材に対して初期仮定断面を算定する
def set_initial_section(nodes,beams, columns, maximum_height,beam_select_mode):

    #選定候補部材リストの読み込み
    column_list = pd.read_csv("column_list.csv",header = 0)
    beam_list = pd.read_csv("beam_list.csv",header = 0)

    #選定モードに準じた梁リストのみ読み込む
    selected_beam_list = beam_list[beam_list['category'].str.contains(beam_select_mode,case=False, na=False)]

    #経験式に基づく初期柱せいの算定(適用高さ上限45m）
    for i in columns:
        temp = math.ceil(((maximum_height+20) *10)/50)*50#鹿島様略算式
        if temp >600:
            column_W = 600
        elif temp <= 600 and temp >= 300:
            column_W = temp
        elif temp < 300:
            column_W = 300

        # 求めた必要梁成以上を満たす柱リストを選定
        target_row = column_list[column_list['H'] >= column_W]

            # 同じ梁せいのリストから最も小さいNoのものを取り出す
        sorted_target_rows = target_row.sort_values(by='No', ascending=True)

        #算定柱せいに適合する柱の断面二次モーメントの出力
        target_row = column_list[column_list['H'] == column_W]
        i.A = float(list(sorted_target_rows['A'])[0])
        i.Ix = float(list(sorted_target_rows['Ix'])[0])
        i.Iy = float(list(sorted_target_rows['Iy'])[0])
        i.selected_section_no = float(list(sorted_target_rows['No'])[0])
        #部材自重の算定
        i.unit_weight = float(list(sorted_target_rows['unit_m'])[0])*9.80665/1000
        i.weight = i.unit_weight * i.length #部材自重
        #算定柱せいによる等価な基礎梁剛度の取得
        i.base_K = float(list(sorted_target_rows['base_K'])[0])
        i.H = float(list(sorted_target_rows['H'])[0])
        i.t = float(list(sorted_target_rows['t'])[0])
        i.Zp = float(list(sorted_target_rows['Zp'])[0])
        i.F = float(list(sorted_target_rows['F'])[0])

    #長期軸力に関する軸力比のクライテリアから考えうる必要な柱断面積の算定
    column_area = [float(column_list['A'][i]) for i in range(len(column_list))]
    column_KX =[];column_KY =[]
    for i in columns:
        i.required_area = i.N_Lx*1000/(0.4*i.F)#長期軸力比を0.4とする場合の必要断面積
        #柱リストより得られた各諸元以上のキャパシティを有する柱断面の選定
        filtered_data = column_list[(column_list['A'] > i.required_area/1000000)]

        #それぞれの選定断面を比較のうえ、こちらの方がリスト番号が大きい場合更新
        if i.selected_section_no-1 < list(filtered_data['No'])[0]:
            i.selected_section_no = list(filtered_data['No'])[0]
            i.A = list(filtered_data['A'])[0]
            i.Ix = list(filtered_data['Ix'])[0]
            i.Iy = list(filtered_data['Iy'])[0]
            # 部材自重の算定
            i.unit_weight = float(list(filtered_data['unit_m'])[0] * 9.80665 / 1000)
            i.weight = i.unit_weight * i.length  # 部材自重
            i.base_K = float(list(filtered_data['base_K'])[0])
            i.H = float(list(filtered_data['H'])[0])
            i.t = float(list(filtered_data['t'])[0])
            i.Zp = float(list(filtered_data['Zp'])[0])
            i.F = float(list(filtered_data['F'])[0])

        #柱の剛度の算定(単位cm3）
        column_KX.append(i.Ix/i.length*1000000)
        column_KY.append(i.Iy/i.length*1000000)

    #初期柱断面のグルーピング
    temp_list=[[columns[i].no,columns[i].H,columns[i].t,columns[i].story]
           for i in range(len(columns))]
    table_columns = ["No", "H", "t", "story"]
    group_data = make_group(temp_list,table_columns,str("story"),str("H"))#グルーピング
    column_groups = [member_class.Column_Group(*data) for data in group_data]  # グループのインスタンス定義

    # 柱の剛比算定（柱の剛度の最大値を標準剛度とみなし1とする）
    maximum_KX = max(column_KX)
    maximum_KY = max(column_KY)
    temp = 0
    for i in columns:
        i.stiff_ratio_x = column_KX[temp]/maximum_KX
        i.stiff_ratio_y = column_KY[temp] / maximum_KY
        temp += 1

    #経験式に基づく初期梁せいの算定
    temp2=0
    for i in beams:
        if i.category != "BB":#基礎梁以外で適用
            temp = i.length*1000/18#鹿島様略算式

            if temp < 500:
                beam_H = 500
            elif temp > 900:
                beam_H = 900
            else:
                beam_H = temp
            # 求めた必要梁成以上を満たす梁リストを選定
            target_row = selected_beam_list[selected_beam_list['H'] >= beam_H]

            #同じ梁せいのリストから最も小さいNoのものを取り出す
            sorted_target_rows = target_row.sort_values(by='No', ascending=True)

        #算定梁せいに適合する梁の選定
            i.selected_section_no = float(list(sorted_target_rows['No'])[0])
            i.I = float(list(sorted_target_rows['Ix'])[0])
            i.H = float(list(sorted_target_rows['H'])[0])
            i.B = float(list(sorted_target_rows['B'])[0])
            i.t1 = float(list(sorted_target_rows['t1'])[0])
            i.t2 = float(list(sorted_target_rows['t2'])[0])
            i.Z = float(list(sorted_target_rows['Z'])[0])
            i.Zp = float(list(sorted_target_rows['Zp'])[0])
            i.F = float(list(sorted_target_rows['F'])[0])

        #梁の剛度の算定(単位cm3）
            i.K = i.I/i.length*1000000*i.pai#床スラブの剛性増大率考慮

        # 部材自重の算定
            i.unit_weight = float(list(sorted_target_rows['unit_m'])[0]*9.80665/1000)
            i.weight = i.unit_weight * i.length  # 部材自重

            i.stiff_ratio = i.K/maximum_KX
            temp2 += 1

        #基礎梁の場合、選択した柱のせいより決まる剛度を設定
        else:#とりあえずi端側の柱を参照
            i.K = columns[nodes[i.i-1].column_no_each_node_x[0]-1].base_K
            i.stiff_ratio = columns[nodes[i.i-1].column_no_each_node_x[0]-1].base_K/100
            i.selected_section_no = ""
            i.I =  0
            i.H =  0
            i.B =  0
            i.t1 =  0
            i.t2 =  0
            i.Z = 0
            i.Zp = 0
            i.F = 0

    #初期梁断面のグルーピング
    temp_list=[[beams[i].no,beams[i].H,beams[i].B,beams[i].story]
           for i in range(len(beams))]
    table_columns = ["No","H","B","story"]
    group_data = make_group(temp_list,table_columns,str("story"),str("H"))#グルーピング
    beam_groups = [member_class.Beam_Group(*data) for data in group_data]  # インスタンスの定義

    #架構の剛性配置を整理
    for i in nodes:
        #X方向の梁
        member_stiff_temp_x=[];member_stiff_temp2_x=[]
        count_x=0
        for j in beams:
            if j.direction == "X": #X方向の場合
                count_x+=1
                if i.no == j.i or i.no == j.j :
                    if j.category == "BB":#基礎梁の場合
                        member_stiff_temp2_x.append(1000000000)# 固定モーメント法の時は基礎梁剛性は無限大
                    else:
                        member_stiff_temp2_x.append(j.stiff_ratio)
                        member_stiff_temp_x.append(j.stiff_ratio)

        for j in columns:
            if i.no == j.i or i.no == j.j :
                member_stiff_temp_x.append(j.stiff_ratio_x)
                member_stiff_temp2_x.append(j.stiff_ratio_x)

        #Y方向の梁
        member_stiff_temp_y = [];member_stiff_temp2_y = []
        count_y=0
        for j in beams:
            if j.direction == "Y":  # Y方向の場合
                count_y+=1
                if i.no == j.i or i.no == j.j:
                    if j.category == "BB":#基礎梁の場合
                        member_stiff_temp2_y.append(1000000000)# 固定モーメント法の時は基礎梁剛性は無限大
                    else:

                        member_stiff_temp2_y.append(j.stiff_ratio)  # 固定モーメント法の時は基礎梁剛性は無限大
                        member_stiff_temp_y.append(j.stiff_ratio)

        for j in columns:
            if i.no == j.i or i.no == j.j :
                member_stiff_temp_y.append(j.stiff_ratio_x)
                member_stiff_temp2_y.append(j.stiff_ratio_x)

        i.node_member_stiff_x = member_stiff_temp_x
        i.node_member_stiff_y = member_stiff_temp_y
        i.node_member_stiff2_x = member_stiff_temp2_x
        i.node_member_stiff2_y = member_stiff_temp2_y

    return beam_groups,column_groups
