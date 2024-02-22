import pandas as pd
import math
import numpy as np
import itertools
import member_class
import calc_stress

#部材のグルーピング
def make_group(list,list_name,key1,key2,key3):

    #list = sorted(list, key=lambda x: x[1],reverse=True)#高さが高い順に並びかえ

    data_frame = pd.DataFrame(list, columns=list_name)
    sorted_frame = data_frame.sort_values(by=[key1, key2, key3])

    group_data = []
    temp = 1
    for name, group in sorted_frame.groupby([key1]):
        for name2, group2 in group.groupby([key2]):
            for name3, group3 in group2.groupby([key3]):
                group_data.append((temp, str(name) + 'F_' + str(name2) + '_' + str(name3), group2['No'].values.tolist()))
                temp += 1
    # group_data = sorted(group_data,reverse=True)#グループを降順に並び替え
    # temp=1#group_noを昇順に書き換え
    # group_data_rev = []
    # for tem in group_data:
    #     tem = (temp, tem[1], tem[2])
    #     group_data_rev.append(tem)
    #     temp+= 1
    return group_data

#初期仮定断面の設定
#Excelで入力した全柱梁部材に対して初期仮定断面を算定する
def set_initial_section(nodes,beams, columns, maximum_height,beam_select_mode):

    #単位変換用係数
    m_to_mm = 1000.0#m→mmへ
    kN_to_N = 1000.0#kN→Nへ

    #選定候補部材リストの読み込み
    column_list = pd.read_csv("column_list.csv",header = 0)
    beam_list = pd.read_csv("beam_list.csv",header = 0)
    initial_beam_list = pd.read_csv("initial_beam_list.csv",header = 0)
    initial_column_list = pd.read_csv("initial_column_list.csv",header = 0)

    #選定モードに準じた梁リストのみ読み込む
    selected_beam_list = beam_list[beam_list['category'].str.contains(beam_select_mode,case=False, na=False)]

    #柱部材リストの断面積によるソート
    sorted_A_column_list = initial_column_list.sort_values(by='A', ascending=True)

    #経験式に基づく初期柱せいの算定(適用高さ上限45m）
    for column in columns:
        temp = math.ceil(((maximum_height+20.0) *10.0)/50.0)*50#鹿島様略算式
        if temp >600:
            column_W = 600
        elif temp <= 600 and temp >= 300:
            column_W = temp
        elif temp < 300:
            column_W = 300

        # 求めた必要梁成以上を満たす柱リストを選定
        target_row = initial_column_list[initial_column_list['H'] >= column_W]

            # 同じ梁せいのリストから最も小さいNoのものを取り出す
        #sorted_target_rows = target_row.sort_values(by='No', ascending=True)

        #算定柱せいに適合する柱の断面二次モーメントの出力
        #target_row = sorted_A_column_list[sorted_A_column_list['H'] == column_W]
        column.A = float(list(target_row['A'])[0])
        column.Ix = float(list(target_row['Ix'])[0])
        column.Iy = float(list(target_row['Iy'])[0])
        column.selected_section_no = float(list(target_row['No'])[0])
        #部材自重の算定
        column.unit_weight = float(list(target_row['unit_m'])[0])*9.80665/m_to_mm
        column.weight = column.unit_weight * column.length #部材自重
        #算定柱せいによる等価な基礎梁剛度の取得
        column.base_K = float(list(target_row['base_K'])[0])
        column.H = float(list(target_row['H'])[0])
        column.t = float(list(target_row['t'])[0])
        column.r = float(list(target_row['r'])[0])
        column.Zp = float(list(target_row['Zp'])[0])
        column.F = float(list(target_row['F'])[0])

    #長期軸力に関する軸力比のクライテリアから考えうる必要な柱断面積の算定
    column_area = map(lambda i: [sorted_A_column_list['A'][i]], range(len(sorted_A_column_list)))
    for column in columns:
        column.required_area = column.N_Lx*kN_to_N/(0.4*column.F)#長期軸力比を0.4とする場合の必要断面積
        #柱リストより得られた各諸元以上のキャパシティを有する柱断面の選定
        filtered_data = sorted_A_column_list[(sorted_A_column_list['A'] > column.required_area/m_to_mm**2)]

        #それぞれの選定断面を比較のうえ、こちらの方がリスト番号が大きい場合更新
        if column.selected_section_no-1 < list(filtered_data['No'])[0]:
            column.selected_section_no = list(filtered_data['No'])[0]
            column.A = list(filtered_data['A'])[0]
            column.Ix = list(filtered_data['Ix'])[0]
            column.Iy = list(filtered_data['Iy'])[0]
            # 部材自重の算定
            column.unit_weight = float(list(filtered_data['unit_m'])[0] * 9.80665 / m_to_mm)
            column.weight = column.unit_weight * column.length  # 部材自重
            column.base_K = float(list(filtered_data['base_K'])[0])
            column.H = float(list(filtered_data['H'])[0])
            column.t = float(list(filtered_data['t'])[0])
            column.r = float(list(filtered_data['r'])[0])
            column.Zp = float(list(filtered_data['Zp'])[0])
            column.F = float(list(filtered_data['F'])[0])

        #柱の剛度の算定(単位cm3）
        column.KX = column.Ix/column.length*1000000.0
        column.KY = column.Iy/column.length*1000000.0

    #初期柱断面のグルーピング
    temp_list = map(lambda i:[columns[i].no,columns[i].H,columns[i].t,columns[i].story],range(len(columns)))
    table_columns = ["No", "H", "t", "story"]
    group_data = make_group(temp_list,table_columns,str("story"),str("H"),str("t"))#グルーピング
    column_groups = [member_class.Column_Group(*data) for data in group_data]  # グループのインスタンス定義

    #経験式に基づく初期梁せいの算定
    temp2=0
    #等価な基礎梁の断面二次モーメント
    for beam in beams:
        if beam.category != "BB":#基礎梁以外で適用
            temp = beam.length*m_to_mm/18.0#鹿島様略算式

            if temp < 350:
                beam_H = 350
            elif temp > 900:
                beam_H = 900
            else:
                beam_H = temp
            # 求めた必要梁成以上を満たす梁リストを選定
            target_row = initial_beam_list[initial_beam_list['H'] >= beam_H]

            #同じ梁せいのリストから最も小さいNoのものを取り出す
            sorted_target_rows = target_row.sort_values(by='No', ascending=True)

        #算定梁せいに適合する梁の選定
            beam.selected_section_no = float(list(sorted_target_rows['No'])[0])
            beam.I = float(list(sorted_target_rows['Ix'])[0])
            beam.H = float(list(sorted_target_rows['H'])[0])
            beam.B = float(list(sorted_target_rows['B'])[0])
            beam.t1 = float(list(sorted_target_rows['t1'])[0])
            beam.t2 = float(list(sorted_target_rows['t2'])[0])
            beam.Z = float(list(sorted_target_rows['Z'])[0])
            beam.Zp = float(list(sorted_target_rows['Zp'])[0])
            beam.F = float(list(sorted_target_rows['F'])[0])
            beam.r = float(list(sorted_target_rows['r'])[0])

        #梁の剛度の算定(単位cm3）
            # 梁せいに応じた床スラブによる梁の剛性増大率の考慮
            if beam.H <= 600:
                beam.K = beam.I/beam.length*1000000*beam.pai2#床スラブの剛性増大率考慮
                beam.calc_phai = beam.pai2
            else:
                beam.K = beam.I/beam.length*1000000*beam.pai#床スラブの剛性増大率考慮
                beam.calc_phai = beam.pai

        # 部材自重の算定
            beam.unit_weight = float(list(sorted_target_rows['unit_m'])[0]*9.80665/m_to_mm)
            beam.weight = beam.unit_weight * beam.length  # 部材自重

            temp2 += 1

        #基礎梁の場合、選択した柱のせいより決まる剛度を設定
        else:#とりあえずi端側の柱を参照
            beam.selected_section_no = ""
            beam.I =  0
            beam.H =  0
            beam.B =  0
            beam.t1 =  0
            beam.t2 =  0
            beam.Z = 0
            beam.Zp = 0
            beam.F = 0
            beam.r = 0

    #初期梁断面のグルーピング
    temp_list = map(lambda i: [beams[i].no, beams[i].H, beams[i].B, beams[i].story], range(len(beams)))
    table_columns = ["No","H","B","story"]
    group_data = make_group(temp_list,table_columns,str("story"),str("H"),str("B"))#グルーピング
    beam_groups = [member_class.Beam_Group(*data) for data in group_data]  # インスタンスの定義

    #柱梁の剛比算定
    calc_stress.calc_stiffness_ratio(columns,beams,nodes)

    #初期選定柱断面のメモリー
    for column in columns:
        column.H_initial = column.H
        column.t_initial = column.t
        column.stiff_ratio_x_initial = column.stiff_ratio_x
        column.stiff_ratio_y_initial = column.stiff_ratio_y
        column.base_K_initial = column.base_K
    #初期選定はり断面のメモリー
    for beam in beams:
        beam.B_initial = beam.B
        beam.H_initial = beam.H
        beam.t1_initial = beam.t1
        beam.t2_initial = beam.t2
        beam.r_initial = beam.r
        beam.eq_beam_stiff_ratio_i_initial = beam.eq_beam_stiff_ratio_i
        beam.eq_beam_stiff_ratio_j_initial = beam.eq_beam_stiff_ratio_j

    #架構の剛性配置を整理
    for node in nodes:
        #X方向の梁
        member_stiff_temp_x=[];member_stiff_temp2_x=[]
        count_x=0
        for beam in beams:
            if beam.direction == "X": #X方向の場合
                count_x+=1
                if node.no == beam.i or node.no == beam.j :
                    if beam.category == "BB":#基礎梁の場合
                        if node.no == beam.i:
                            member_stiff_temp2_x.append(1000000000)# 固定モーメント法の時は基礎梁剛性は無限大
                            member_stiff_temp_x.append(beam.eq_beam_stiff_ratio_i)
                        elif node.no == beam.j:
                            member_stiff_temp2_x.append(1000000000)# 固定モーメント法の時は基礎梁剛性は無限大
                            member_stiff_temp_x.append(beam.eq_beam_stiff_ratio_j)
                    else:#基礎梁以外の場合
                        if node.no == beam.i:
                            member_stiff_temp2_x.append(beam.eq_beam_stiff_ratio_i)
                            member_stiff_temp_x.append(beam.eq_beam_stiff_ratio_i)
                        elif node.no == beam.j:
                            member_stiff_temp2_x.append(beam.eq_beam_stiff_ratio_j)
                            member_stiff_temp_x.append(beam.eq_beam_stiff_ratio_j)

        for column in columns:
            if node.no == column.i or node.no == column.j :
                member_stiff_temp_x.append(column.stiff_ratio_x)
                member_stiff_temp2_x.append(column.stiff_ratio_x)

        #Y方向の梁
        member_stiff_temp_y = [];member_stiff_temp2_y = []
        count_y=0
        for beam in beams:
            if beam.direction == "Y":  # Y方向の場合
                count_y+= 1
                if node.no == beam.i or node.no == beam.j:
                    if beam.category == "BB":#基礎梁の場合
                        if node.no == beam.i:
                            member_stiff_temp2_y.append(1000000000)# 固定モーメント法の時は基礎梁剛性は無限大
                            member_stiff_temp_y.append(beam.eq_beam_stiff_ratio_i)
                        elif node.no == beam.j:
                            member_stiff_temp2_y.append(1000000000)# 固定モーメント法の時は基礎梁剛性は無限大
                            member_stiff_temp_y.append(beam.eq_beam_stiff_ratio_j)
                    else:#基礎梁以外の場合
                        if node.no == beam.i:
                            member_stiff_temp2_y.append(beam.eq_beam_stiff_ratio_i)
                            member_stiff_temp_y.append(beam.eq_beam_stiff_ratio_i)
                        elif node.no == beam.j:
                            member_stiff_temp2_y.append(beam.eq_beam_stiff_ratio_j)
                            member_stiff_temp_y.append(beam.eq_beam_stiff_ratio_j)

        for column in columns:
            if node.no == column.i or node.no == column.j :
                member_stiff_temp_y.append(column.stiff_ratio_x)
                member_stiff_temp2_y.append(column.stiff_ratio_x)

        node.node_member_stiff_x = member_stiff_temp_x
        node.node_member_stiff_y = member_stiff_temp_y
        node.node_member_stiff2_x = member_stiff_temp2_x
        node.node_member_stiff2_y = member_stiff_temp2_y

    return beam_groups,column_groups
