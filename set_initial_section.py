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

    #単位変換用係数
    m_to_mm = 1000.0#m→mmへ
    kN_to_N = 1000.0#kN→Nへ

    #選定候補部材リストの読み込み
    column_list = pd.read_csv("column_list.csv",header = 0)
    beam_list = pd.read_csv("beam_list.csv",header = 0)

    #選定モードに準じた梁リストのみ読み込む
    selected_beam_list = beam_list[beam_list['category'].str.contains(beam_select_mode,case=False, na=False)]

    #柱部材リストの断面積によるソート
    sorted_A_column_list = column_list.sort_values(by='A', ascending=True)

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
        target_row = sorted_A_column_list[sorted_A_column_list['H'] >= column_W]

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
        column.Zp = float(list(target_row['Zp'])[0])
        column.F = float(list(target_row['F'])[0])

    #長期軸力に関する軸力比のクライテリアから考えうる必要な柱断面積の算定
    column_area = map(lambda i: [sorted_A_column_list['A'][i]], range(len(sorted_A_column_list)))
    column_KX =[];column_KY =[]
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
            column.Zp = float(list(filtered_data['Zp'])[0])
            column.F = float(list(filtered_data['F'])[0])

        #柱の剛度の算定(単位cm3）
        column_KX.append(column.Ix/column.length*1000000.0)
        column_KY.append(column.Iy/column.length*1000000.0)

    #初期柱断面のグルーピング
    temp_list = map(lambda i:[columns[i].no,columns[i].H,columns[i].t,columns[i].story],range(len(columns)))
    table_columns = ["No", "H", "t", "story"]
    group_data = make_group(temp_list,table_columns,str("story"),str("H"))#グルーピング
    column_groups = [member_class.Column_Group(*data) for data in group_data]  # グループのインスタンス定義

    # 柱の剛比算定（柱の剛度の最大値を標準剛度とみなし1とする）
    maximum_KX = max(column_KX)
    maximum_KY = max(column_KY)
    temp = 0
    for column in columns:
        column.stiff_ratio_x = column_KX[temp]/maximum_KX
        column.stiff_ratio_y = column_KY[temp] / maximum_KY
        temp += 1

    #経験式に基づく初期梁せいの算定
    temp2=0
    #等価な基礎梁の断面二次モーメント
    II = 3240000000#800×900の基礎梁断面
    for beam in beams:
        if beam.category != "BB":#基礎梁以外で適用
            temp = beam.length*m_to_mm/18.0#鹿島様略算式

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
            beam.selected_section_no = float(list(sorted_target_rows['No'])[0])
            beam.I = float(list(sorted_target_rows['Ix'])[0])
            beam.H = float(list(sorted_target_rows['H'])[0])
            beam.B = float(list(sorted_target_rows['B'])[0])
            beam.t1 = float(list(sorted_target_rows['t1'])[0])
            beam.t2 = float(list(sorted_target_rows['t2'])[0])
            beam.Z = float(list(sorted_target_rows['Z'])[0])
            beam.Zp = float(list(sorted_target_rows['Zp'])[0])
            beam.F = float(list(sorted_target_rows['F'])[0])

        #梁の剛度の算定(単位cm3）
            # 梁せいに応じた床スラブによる梁の剛性増大率の考慮
            if beam.H <= 600:
                beam.K = beam.I/beam.length*1000000*beam.pai2#床スラブの剛性増大率考慮
            else:
                beam.K = beam.I/beam.length*1000000*beam.pai#床スラブの剛性増大率考慮

        # 部材自重の算定
            beam.unit_weight = float(list(sorted_target_rows['unit_m'])[0]*9.80665/m_to_mm)
            beam.weight = beam.unit_weight * beam.length  # 部材自重

            beam.stiff_ratio = beam.K/maximum_KX
            temp2 += 1

        #基礎梁の場合、選択した柱のせいより決まる剛度を設定
        else:#とりあえずi端側の柱を参照
            beam.K = columns[nodes[beam.i-1].column_no_each_node_x[0]-1].base_K
            #beam.stiff_ratio = columns[nodes[beam.i-1].column_no_each_node_x[0]-1].base_K/100.0
            beam.eq_beam_stiff_ratio_i = 1.0/(1.0/columns[nodes[beam.i-1].column_no_each_node_x[0]-1].base_K+1.0/(II/(beam.length*m_to_mm)))/100000.0
            beam.eq_beam_stiff_ratio_j = 1.0/(1.0/columns[nodes[beam.j-1].column_no_each_node_x[0]-1].base_K+1.0/(II/(beam.length*m_to_mm)))/100000.0
            beam.selected_section_no = ""
            beam.I =  0
            beam.H =  0
            beam.B =  0
            beam.t1 =  0
            beam.t2 =  0
            beam.Z = 0
            beam.Zp = 0
            beam.F = 0

    #初期梁断面のグルーピング
    temp_list = map(lambda i: [beams[i].no, beams[i].H, beams[i].B, beams[i].story], range(len(beams)))
    table_columns = ["No","H","B","story"]
    group_data = make_group(temp_list,table_columns,str("story"),str("H"))#グルーピング
    beam_groups = [member_class.Beam_Group(*data) for data in group_data]  # インスタンスの定義

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
                        member_stiff_temp2_x.append(1000000000)# 固定モーメント法の時は基礎梁剛性は無限大
                    elif beam.boundary_i == "pin" and beam.boundary_j == "fix":
                        # i端の境界条件がピン、j端の境界条件が固定の場合
                        if node.no == beam.i:
                            member_stiff_temp2_x.append(0)
                            member_stiff_temp_x.append(0)
                        elif node.no == beam.j:
                            member_stiff_temp2_x.append(beam.stiff_ratio*0.5)
                            member_stiff_temp_x.append(beam.stiff_ratio*0.5)
                    elif beam.boundary_i == "fix" and beam.boundary_j == "pin":
                        # i端の境界条件が固定、j端の境界条件がピンの場合
                        if node.no == beam.i:
                            member_stiff_temp2_x.append(beam.stiff_ratio*0.5)
                            member_stiff_temp_x.append(beam.stiff_ratio * 0.5)
                        elif node.no == beam.j:
                            member_stiff_temp2_x.append(0)
                            member_stiff_temp_x.append(0)
                    elif beam.boundary_i == "pin" and beam.boundary_j == "pin":
                            # i端の境界条件がピン、j端の境界条件がピンの場合
                        if node.no == beam.i:
                            member_stiff_temp2_x.append(0)
                            member_stiff_temp_x.append(0)
                        elif node.no == beam.j:
                            member_stiff_temp2_x.append(0)
                            member_stiff_temp_x.append(0)
                    else:
                        member_stiff_temp2_x.append(beam.stiff_ratio)
                        member_stiff_temp_x.append(beam.stiff_ratio)

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
                        member_stiff_temp2_y.append(1000000000)# 固定モーメント法の時は基礎梁剛性は無限大
                    elif beam.boundary_i == "pin" and beam.boundary_j == "fix":
                        # i端の境界条件がピン、j端の境界条件が固定の場合
                        if node.no == beam.i:
                            member_stiff_temp2_y.append(0)
                            member_stiff_temp_y.append(0)
                        elif node.no == beam.j:
                            member_stiff_temp2_y.append(beam.stiff_ratio*0.5)
                            member_stiff_temp_y.append(beam.stiff_ratio*0.5)
                    elif beam.boundary_i == "fix" and beam.boundary_j == "pin":
                        # i端の境界条件が固定、j端の境界条件がピンの場合
                        if node.no == beam.i:
                            member_stiff_temp2_y.append(beam.stiff_ratio*0.5)
                            member_stiff_temp_y.append(beam.stiff_ratio*0.5)
                        elif node.no == beam.j:
                            member_stiff_temp2_y.append(0)
                            member_stiff_temp_y.append(0)
                    elif beam.boundary_i == "pin" and beam.boundary_j == "pin":
                            # 両端ピンの場合
                        if node.no == beam.i:
                            member_stiff_temp2_y.append(0)
                            member_stiff_temp_y.append(0)
                        elif node.no == beam.j:
                            member_stiff_temp2_y.append(0)
                            member_stiff_temp_y.append(0)

                    else:
                        member_stiff_temp2_y.append(beam.stiff_ratio)  # 固定モーメント法の時は基礎梁剛性は無限大
                        member_stiff_temp_y.append(beam.stiff_ratio)

        for column in columns:
            if node.no == column.i or node.no == column.j :
                member_stiff_temp_y.append(column.stiff_ratio_x)
                member_stiff_temp2_y.append(column.stiff_ratio_x)

        node.node_member_stiff_x = member_stiff_temp_x
        node.node_member_stiff_y = member_stiff_temp_y
        node.node_member_stiff2_x = member_stiff_temp2_x
        node.node_member_stiff2_y = member_stiff_temp2_y

    return beam_groups,column_groups
