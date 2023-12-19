import math
import pandas as pd
import numpy as np
import itertools
from member_class import *
from set_initial_section import *

#大梁断面を長期・短期応力評価結果に基づいて更新
def update_beam_section(nodes,beams,beam_select_mode,EE):
    #準備計算
    #梁リストの読み込み
    beam_list = pd.read_csv("beam_list.csv", header=0)

    #選定モードに準じた梁リストのみ読み込む
    selected_beam_list = beam_list[beam_list['category'].str.contains(beam_select_mode,case=False, na=False)]
    sorted_Zp_beam_list = selected_beam_list.sort_values(by='Zp', ascending=True)#応力による断面更新に用いるリスト
    #sorted_A_beam_list = selected_beam_list.sort_values(by='A', ascending=True)

    #応力による断面選定
    #梁応力の算定
    for i in beams:
        if i.category != "BB":#基礎梁以外の断面を更新
            sigma_b_L = (i.ML*1000000)/(i.Z*1000**3-i.t1*(i.H-i.t2*2)**2/6)#曲げ応力の算定時にウェブの断面係数は非考慮
            sigma_b_s = (i.Ms*1000000)/(i.Z*1000**3-i.t1*(i.H-i.t2*2)**2/6)#曲げ応力の算定時にウェブの断面係数は非考慮
            tau_L = i.QL*1000/((i.H-i.t2*2)*i.t1)
            tau_s = i.Qs*1000/((i.H-i.t2*2)*i.t1)
    #曲げ、せん断耐力の算定
            f_b = i.F*1.1#取り合えずfb低減は考慮しない
            f_s = i.F*1.1/math.sqrt(3)

    #検定比0.9を満たすために必要な梁の断面係数、ウェブ断面積の算定
            i.required_web_area = max(i.QL*1000/(0.9*f_s/1.5),i.Qs*1000/(0.9*f_s))
            i.required_Z = max(i.ML*1000000/(0.9*f_b/1.5),i.Ms*1000000/(0.9*f_b))

    #必要な梁の断面係数、ウェブ断面積以上の部材をリストより選定
            filtered_list = sorted_Zp_beam_list[(sorted_Zp_beam_list['Zp'] > i.required_Z/1000000000) &
            (sorted_Zp_beam_list['H']*sorted_Zp_beam_list['t1'] > i.required_web_area/1000000)]
    #さらに梁せいの制限で絞り込み（スパンの1/20以上）
            filtered_list2 = filtered_list[(filtered_list['H']/1000 > i.length*1/20)]

            i.selected_section_no = float(list(filtered_list2['No'])[0])
            i.I = float(list(filtered_list2['Ix'])[0])  # 断面諸元の更新
            i.H = float(list(filtered_list2['H'])[0])
            i.B = float(list(filtered_list2['B'])[0])
            i.t1 = float(list(filtered_list2['t1'])[0])
            i.t2 = float(list(filtered_list2['t2'])[0])
            i.Z = float(list(filtered_list2['Z'])[0])
            i.Zp = float(list(filtered_list2['Zp'])[0])
            i.F = float(list(filtered_list2['F'])[0])

            # 大梁のたわみ算定に基づく断面更新(ダミーの基礎梁は除く）
            temp_no=0
            while True:
                if i.direction == "X":
                    i.M_Lx0 = i.M0 - np.average([i.M_Lx[0], i.M_Lx[1]])
                    i.delta_x = (5 * i.M_Lx0 / (48 * EE * i.I) * i.length ** 2
                                - sum(i.M_Lx) / (16 * EE * i.I) * i.length ** 2)  # 梁中央のたわみ（未検証）
                # 大梁たわみが1/300以下であるか確認
                    if abs(i.delta_x / i.length) >= 1 / 300:
                    #NGの場合梁リストから一段上げて再確認
                        temp_no += 1
                        i.I = float(list(filtered_list2['Ix'])[temp_no])  # 断面諸元の更新
                        i.H = float(list(filtered_list2['H'])[temp_no])
                        i.B = float(list(filtered_list2['B'])[temp_no])
                        i.t1 = float(list(filtered_list2['t1'])[temp_no])
                        i.t2 = float(list(filtered_list2['t2'])[temp_no])
                        i.Z = float(list(filtered_list2['Z'])[temp_no])
                        i.Zp = float(list(filtered_list2['Zp'])[temp_no])
                        i.F = float(list(filtered_list2['F'])[temp_no])
                        print("Beam deflection is NG")
                    else:
                        break
                else:
                    i.M_Ly0 = i.M0 - np.average([i.M_Ly[0], i.M_Ly[1]])
                    i.delta_y = (5 * i.M_Ly0 / (48 * EE * i.I) * i.length ** 2
                                - sum(i.M_Ly) / (16 * EE * i.I) * i.length ** 2)  # 梁中央のたわみ（未検証）
                # 大梁たわみが1/300以下であるか確認
                    if abs(i.delta_y / i.length) >= 1 / 300:
                    # NGの場合梁リストから一段上げて再確認
                        temp_no += 1
                        i.I = float(list(filtered_list2['Ix'])[temp_no])  # 断面諸元の更新
                        i.H = float(list(filtered_list2['H'])[temp_no])
                        i.B = float(list(filtered_list2['B'])[temp_no])
                        i.t1 = float(list(filtered_list2['t1'])[temp_no])
                        i.t2 = float(list(filtered_list2['t2'])[temp_no])
                        i.Z = float(list(filtered_list2['Z'])[temp_no])
                        i.Zp = float(list(filtered_list2['Zp'])[temp_no])
                        i.F = float(list(filtered_list2['F'])[temp_no])
                        print("Beam deflection is NG")
                    else:
                        break

            #i.judge_b_L = sigma_b_L/(f_b/1.5)
            #i.judge_b_s = sigma_b_s/f_b
            #i.judge_s_L = tau_L/(f_s/1.5)
            #i.judge_s_s = tau_s/f_s

    #曲げせん断検定比が0.9以上の場合、選定部材を1ランク上げる
            #if i.judge_b_L >= 0.9 or i.judge_b_s >= 0.9 or i.judge_s_L >= 0.9 or i.judge_s_s >= 0.9:
            #    temp = i.selected_section_no + 1

            #    while True:
            #        if temp <= max(beam_list['No']):  # 1ランク上げたときに梁リストの上限を超えない場合
            #            if int(temp) in sorted_A_beam_list['No'].values:  # 対象の梁部材がリストに存在するとき
            #                target_row1 = sorted_A_beam_list[sorted_A_beam_list['No'] == temp]
            #                target_row2 = sorted_Zp_beam_list[sorted_A_beam_list['No'] == temp]

            #                if i.judge_b_L >= 0.9 or i.judge_b_s >= 0.9:#曲げが厳しい場合、選定リストの断面係数を確認
            #                    if float(target_row2['Z'])/i.Z * float(target_row2['F'])/i.F > max(i.judge_b_L,i.judge_b_s)/0.9:#検定比を満たせる程度Zがあげられた場合断面更新(F値の違いの影響も考慮）
            #                        i.I = float(target_row2['Ix'])  # 断面諸元の更新
            #                        i.H = float(target_row2['H'])
            #                        i.B = float(target_row2['B'])
            #                        i.t1 = float(target_row2['t1'])
            #                        i.t2 = float(target_row2['t2'])
            #                        i.Z = float(target_row2['Z'])
            #                        i.Zp = float(target_row2['Zp'])
            #                        i.F = float(target_row2['F'])
            #                        break
            #                if i.judge_s_L >= 0.9 or i.judge_s_s >= 0.9:#せん断が厳しい場合、選定リストのウェブ断面積を確認
            #                    if float(target_row1['H'])*float(target_row1['t1'])/i.H*i.t1 * float(target_row1['F'])/i.F > max(i.judge_s_L,i.judge_s_s)/0.9:#検定比を満たせる程度ウェブ断面積があげられた場合断面更新(F値の違いの影響も考慮）
            #                        i.I = float(target_row1['Ix'])  # 断面諸元の更新
            #                        i.H = float(target_row1['H'])
            #                        i.B = float(target_row1['B'])
            #                        i.t1 = float(target_row1['t1'])
            #                        i.t2 = float(target_row1['t2'])
            #                        i.Z = float(target_row1['Z'])
            #                        i.Zp = float(target_row1['Zp'])
            #                        i.F = float(target_row1['F'])
            #                        break
            #                if (i.judge_b_L >= 0.9 or i.judge_b_s >= 0.9) and (i.judge_s_L >= 0.9 or i.judge_s_s >= 0.9):
                        #曲げとせん断がともに厳しい場合、選定リストのウェブ断面積を確認
            #                    if (float(target_row2['Z'])/i.Z *float(target_row2['F'])/i.F > max(i.judge_b_L,i.judge_b_s)/0.9) and \
            #                    (float(target_row2['H'])*float(target_row2['t1'])/i.H*i.t1 * float(target_row2['F'])/i.F >
            #                     max(i.judge_s_L,i.judge_s_s)/0.9):#検定比を満たせる程度断面係数、ウェブ断面積があげられた場合断面更新
            #                        i.I = float(target_row2['Ix'])  # 断面諸元の更新
            #                        i.H = float(target_row2['H'])
            #                        i.B = float(target_row2['B'])
            #                        i.t1 = float(target_row2['t1'])
            #                        i.t2 = float(target_row2['t2'])
            #                        i.Z = float(target_row2['Z'])
            #                        i.Zp = float(target_row2['Zp'])
            #                        i.F = float(target_row2['F'])
            #                        break
            #        else:# 1ランク上げたときに梁リストの上限を超える場合
            #            print("requirement value is over upper limit of beam_list.")
            #            i.I = "Error"  # 断面諸元の更新
            #            i.H = "Error"
            #            i.B = "Error"
            #            i.t1 = "Error"
            #            i.t2 = "Error"
            #            i.Z = "Error"
            #            i.Zp = "Error"
            #            i.F = "Error"
            #            break
            #        temp += 1

    #応力に基づく梁断面更新後の梁断面の再グルーピング
    temp_list=[[beams[i].no,beams[i].H,beams[i].B,beams[i].story]
          for i in range(len(beams))]
    table_columns = ["No","H","B","story"]
    group_data = make_group(temp_list,table_columns,str("story"),str("H"))#グルーピング
    beam_groups = [member_class.Beam_Group(*data) for data in group_data]  # インスタンスの定義

    #各梁グループが隣接する梁を調べる
    for i in beam_groups:
        temp3=[]
        for j in i.ID:#そのグループに属する梁の隣接する梁の洗い出し
            temp3.extend(nodes[beams[j-1].i-1].beam_no_each_node2_x+
                                 nodes[beams[j-1].i-1].beam_no_each_node2_y+
                                 nodes[beams[j-1].j-1].beam_no_each_node2_x+
                                 nodes[beams[j-1].j-1].beam_no_each_node2_y)
            temp3.remove(j)#自分自身を除く
            temp3.remove(j)
        i.neighbor_beam = list(set(temp3))

    #各梁グループが隣接する梁のグループを調べる
        temp4= [] ;temp5 = []
        for j in i.neighbor_beam:
            for k in beam_groups:
                if j in k.ID:
                    temp4.append(k.group_name)
                    temp5.append(k.no)
        temp4 = set(temp4)
        temp5 = set(temp5)
        i.neighbor_group = temp4
        i.neighbor_group_no = temp5

    #各梁グループについて、隣接する梁のグル―プのせいとの関係性を調べる（大きい差の調整）
    for i in beam_groups:
        test_H = beams[i.ID[0]-1].H#グループに属する梁のせい
        for j in i.neighbor_group_no:
            neighbor_H = beams[beam_groups[j-1].ID[0]-1].H#隣接する梁グループに属する梁のせい
            # 梁高さの差が100mm～200mmの場合、大きい方の梁成を上げる
            if (abs(float(test_H) - float(neighbor_H)) > 100) \
                    and (abs(float(test_H) - float(neighbor_H)) <= 200):
                # 算定梁せいに適合する梁の選定
                if test_H >= neighbor_H:#元のグループの梁せいの方が大きい場合、そちらを上げる
                    temp = beams[i.ID[0]-1].selected_section_no + 1

                    while True:
                        if temp <= max(beam_list['No']):  # 1ランク上げたときに梁リストの上限を超えない場合
                            if int(temp) in selected_beam_list['No'].values:  # 対象の梁部材がリストに存在するとき
                                # 選んだ梁成の差が200以上ある場合、断面更新
                                if list(selected_beam_list[selected_beam_list['No'] == int(temp)]['H'])[0] - neighbor_H > 200:
                                    target_row = selected_beam_list[selected_beam_list['No'] == temp]
                                    for k in i.ID:
                                        beams[k - 1].selected_section_no = float(target_row['No'])
                                        beams[k - 1].I = float(target_row['Ix'])
                                        beams[k - 1].H = float(target_row['H'])
                                        beams[k - 1].B = float(target_row['B'])
                                        beams[k - 1].t1 = float(target_row['t1'])
                                        beams[k - 1].t2 = float(target_row['t2'])
                                        beams[k - 1].Z = float(target_row['Z'])
                                        beams[k - 1].Zp = float(target_row['Zp'])
                                        beams[k - 1].F = float(target_row['F'])
                        else:  # 1ランク上げたときに梁リストの上限を超える場合
                            print("requirement value is over upper limit of beam_list.")
                            for k in i.ID:
                                beams[k - 1].I = "Error"
                                beams[k - 1].H = "Error"
                                beams[k - 1].B = "Error"
                                beams[k - 1].t1 = "Error"
                                beams[k - 1].t2 = "Error"
                                beams[k - 1].Z = "Error"
                                beams[k - 1].Zp = "Error"
                                beams[k - 1].F = "Error"
                        temp += 1
                else:
                    temp = beams[beam_groups[j-1].ID[0]-1].selected_section_no + 1
                    while True:
                        if temp <= max(beam_list['No']):  # 1ランク上げたときに梁リストの上限を超えない場合
                            if int(temp) in selected_beam_list['No'].values:#対象の梁部材がリストに存在するとき
                        # 選んだ梁成の差が200以上ある場合、断面更新
                                if list(selected_beam_list[selected_beam_list['No'] == temp]['H'])[0] - test_H > 200:
                                    target_row = selected_beam_list[selected_beam_list['No'] == temp]
                                    for k in beam_groups[j-1].ID:
                                        beams[k-1].selected_section_no = float(target_row['No'])
                                        beams[k-1].I =float(target_row['Ix'])
                                        beams[k-1].H =float(target_row['H'])
                                        beams[k - 1].B = float(target_row['B'])
                                        beams[k-1].t1 = float(target_row['t1'])
                                        beams[k-1].t2 = float(target_row['t2'])
                                        beams[k-1].Z = float(target_row['Z'])
                                        beams[k-1].Zp = float(target_row['Zp'])
                                        beams[k-1].F = float(target_row['F'])
                                    break
                        else:  # 1ランク上げたときに梁リストの上限を超える場合
                            print("requirement value is over upper limit of beam_list.")
                            for k in beam_groups[j-1].ID:
                                beams[k - 1].I = "Error"
                                beams[k - 1].H = "Error"
                                beams[k - 1].B = "Error"
                                beams[k - 1].t1 = "Error"
                                beams[k - 1].t2 = "Error"
                                beams[k - 1].Z = "Error"
                                beams[k - 1].Zp = "Error"
                                beams[k - 1].F = "Error"
                            frag =1
                            break
                        temp += 1

    #梁断面の再グルーピング
    temp_list=[[beams[i].no,beams[i].H,beams[i].B,beams[i].story]
          for i in range(len(beams))]
    table_columns = ["No","H","B","story"]
    group_data = make_group(temp_list,table_columns,str("story"),str("H"))#グルーピング
    beam_groups = [member_class.Beam_Group(*data) for data in group_data]  # インスタンスの定義

    #各梁グループが隣接する梁を調べる
    for i in beam_groups:
        temp3=[]
        for j in i.ID:#そのグループに属する梁の隣接する梁の洗い出し
            temp3.extend(nodes[beams[j-1].i-1].beam_no_each_node2_x+
                                 nodes[beams[j-1].i-1].beam_no_each_node2_y+
                                 nodes[beams[j-1].j-1].beam_no_each_node2_x+
                                 nodes[beams[j-1].j-1].beam_no_each_node2_y)
            temp3.remove(j)#自分自身を除く
            temp3.remove(j)
        i.neighbor_beam = list(set(temp3))

    #各梁グループが隣接する梁のグループを調べる
        temp4= [] ;temp5 = []
        for j in i.neighbor_beam:
            for k in beam_groups:
                if j in k.ID:
                    temp4.append(k.group_name)
                    temp5.append(k.no)
        temp4 = set(temp4)
        temp5 = set(temp5)
        i.neighbor_group = temp4
        i.neighbor_group_no = temp5

    #各梁グループについて、隣接する梁のグループのせいとの関係性を調べる（小さい差の調整）
    for i in beam_groups:
        test_H = beams[i.ID[0]-1].H#グループに属する梁のせい
        for j in i.neighbor_group_no:
            neighbor_H = beams[beam_groups[j-1].ID[0]-1].H#隣接する梁グループに属する梁のせい
            # 梁高さの差が100mm以内の場合なら小さい方の梁せいを合わせにいく
            if abs(float(test_H) - float(neighbor_H)) > 5 \
                    and abs(float(test_H) - float(neighbor_H)) <= 100:
            # 算定梁せいに適合する梁の選定
                if float(test_H) >= float(neighbor_H):
                    filtered_beam_list = sorted_Zp_beam_list[(sorted_Zp_beam_list['H'] == test_H) & (sorted_Zp_beam_list['Zp'] >= beams[i.ID[0]-1].Zp) ]
                    for k in beam_groups[j-1].ID:
                        beams[k-1].I = float(list(filtered_beam_list['Ix'])[0])
                        beams[k - 1].selected_section_no = float(list(filtered_beam_list['No'])[0])
                        beams[k - 1].H = float(list(filtered_beam_list['H'])[0])
                        beams[k - 1].B = float(list(filtered_beam_list['B'])[0])
                        beams[k - 1].t1 = float(list(filtered_beam_list['t1'])[0])
                        beams[k - 1].t2 = float(list(filtered_beam_list['t2'])[0])
                        beams[k - 1].Z = float(list(filtered_beam_list['Z'])[0])
                        beams[k - 1].Zp = float(list(filtered_beam_list['Zp'])[0])
                        beams[k - 1].F = float(list(filtered_beam_list['F'])[0])

                else:
                    filtered_beam_list = sorted_Zp_beam_list[(sorted_Zp_beam_list['H'] == neighbor_H) & (sorted_Zp_beam_list['Zp'] >= beams[beam_groups[j-1].ID[0]-1].Zp) ]
                    for k in i.ID:
                        beams[k - 1].I = float(list(filtered_beam_list['Ix'])[0])
                        beams[k - 1].selected_section_no = float(list(filtered_beam_list['No'])[0])
                        beams[k - 1].H = float(list(filtered_beam_list['H'])[0])
                        beams[k - 1].B = float(list(filtered_beam_list['B'])[0])
                        beams[k - 1].t1 = float(list(filtered_beam_list['t1'])[0])
                        beams[k - 1].t2 = float(list(filtered_beam_list['t2'])[0])
                        beams[k - 1].Z = float(list(filtered_beam_list['Z'])[0])
                        beams[k - 1].Zp = float(list(filtered_beam_list['Zp'])[0])
                        beams[k - 1].F = float(list(filtered_beam_list['F'])[0])

    #梁断面の再グルーピング
    temp_list=[[beams[i].no,beams[i].H,beams[i].B,beams[i].story]
          for i in range(len(beams))]
    table_columns = ["No","H","B","story"]
    group_data = make_group(temp_list,table_columns,str("story"),str("H"))#グルーピング
    beam_groups = [member_class.Beam_Group(*data) for data in group_data]  # インスタンスの定義

    #梁断面の更新に伴う剛度の更新
    for i in beams:
        if i.category != "BB":#基礎梁以外の断面を更新
            i.K = i.I/i.length*1000000*i.pai#床スラブの剛性増大率考慮

#剛性チェックに基づく各層柱の必要剛性の算定
def calc_based_stiffness(nodes,layers,beams,columns,EE):

    for i in layers:
    #各層の層間変形角1/200を満たすために必要な柱のD値算定
        i.req_D_sum_x = i.shear_force_x*1000*(i.height*1000)**2/12/EE/(i.height*1000/200)/10**2
        i.req_D_sum_y = i.shear_force_y*1000*(i.height*1000)**2/12/EE/(i.height*1000/200)/10**2

    #各層柱のD値、D値の最大値の集計
    temp_x = np.zeros(len(layers))
    temp_y = np.zeros(len(layers))
    temp_max_x = np.zeros(len(layers))
    temp_max_y = np.zeros(len(layers))

    beam_stiff_x =[];beam_stiff_y=[]
    for i in columns:
        temp_x[len(layers)-i.story] += i.D_x
        temp_y[len(layers)-i.story] += i.D_y
        if temp_max_x[len(layers)-i.story] <= i.D_x:
            temp_max_x[len(layers) - i.story] = i.D_x
        if temp_max_y[len(layers) - i.story] <= i.D_y:
            temp_max_y[len(layers) - i.story] = i.D_y

        #各柱の接する梁の剛度を足す
        #i端
        temp_stiff_x = 0
        temp_stiff_y = 0
        for k in nodes[i.i-1].beam_no_each_node2_x:
            temp_stiff_x += beams[k-1].K
        beam_stiff_x.append(float(temp_stiff_x))
        #j端
        for k in nodes[i.j-1].beam_no_each_node2_x:
            temp_stiff_y += beams[k-1].K
        beam_stiff_y.append(float(temp_stiff_y))

    for i in range(len(layers)):
        layers[i].D_sum_x = temp_x[i]
        layers[i].D_sum_y = temp_y[i]
        layers[i].D_max_x = temp_max_x[i]
        layers[i].D_max_y = temp_max_y[i]

        #各層柱の必要D値算定
        layers[i].req_D_x = float(layers[i].req_D_sum_x) / float(layers[i].D_sum_x)*float(layers[i].D_max_x)
        layers[i].req_D_y = float(layers[i].req_D_sum_y) / float(layers[i].D_sum_y)*float(layers[i].D_max_y)
        #各柱の必要剛度、断面二次モーメント算定
        #とりあえず計算に用いる各梁の剛比については最大値を想定する

        layers[i].k_limit1_x = max(beam_stiff_x)/(max(beam_stiff_x)/layers[i].req_D_x-2)
        layers[i].k_limit1_y = max(beam_stiff_y)/(max(beam_stiff_y)/layers[i].req_D_y-2)

        layers[i].I_limit1_x = layers[i].k_limit1_x * 10**5 * layers[i].height*1000/(10**12)
        layers[i].I_limit1_y = layers[i].k_limit1_y * 10**5 * layers[i].height*1000/(10**12)

#柱梁耐力比チェックに基づく各柱の必要剛性の算定
def member_strength_check(nodes,beams,columns):
    #梁の全塑性曲げモーメントの算定
    for i in beams:
        if i.category != "BB":#基礎梁以外の断面について算定
            i.Mp = i.F *1/1000*1000*1000* i.Zp

    #柱の全塑性モーメントの算定
    for i in columns:
        axial_ratio_x = i.NSx * 1000 / (i.A*1000**2*i.F)#長期＋短期荷重時の柱軸力比
        if axial_ratio_x <= 0.5:#軸力比を考慮した全塑性曲げモーメントの低下率の算定
            i.decrement_ratio_x = 1-4*axial_ratio_x**2/3
        else:
            i.decrement_ratio_x = 4*(1-axial_ratio_x)/3

        axial_ratio_y = i.NSy * 1000 / (i.A*1000**2*i.F)
        if axial_ratio_y <= 0.5:#軸力比を考慮した全塑性曲げモーメントの低下率の算定
            i.decrement_ratio_y = 1-4*axial_ratio_y**2/3
        else:
            i.decrement_ratio_y = 4*(1-axial_ratio_y)/3

        #低下率を考慮した柱の全塑性曲げモーメントの算定
        i.Mpx = i.decrement_ratio_x * i.F * 1/1000*1000*1000* i.Zp
        i.Mpy = i.decrement_ratio_y * i.F * 1/1000*1000*1000* i.Zp

    #各節点における柱梁耐力比の確認
    for i in nodes:
        #左右梁の全塑性モーメントの集計
        #X方向
        temp_beam_Mp_x =0
        for j in i.beam_no_each_node_x:
            temp_beam_Mp_x += beams[j-1].Mp
        #Y方向
        temp_beam_Mp_y = 0
        for j in i.beam_no_each_node_y:
            temp_beam_Mp_y += beams[j - 1].Mp

        #上下柱の全塑性モーメントの集計
        #X方向
        #temp_column_Mp_x =0
        #for j in i.column_no_each_node_x:
        #    temp_column_Mp_x += columns[j-1].Mpx
        #Y方向
        #temp_column_Mp_y = 0
        #for j in i.column_no_each_node_y:
        #    temp_column_Mp_y += columns[j - 1].Mpy

        #現断面での柱梁耐力比の確認
        #ratio_x = temp_column_Mp_x/temp_beam_Mp_x
        #ratio_y = temp_column_Mp_y / temp_beam_Mp_y

        #柱梁耐力比が1.0以下の場合、1以上にするために必要な柱の全塑性モーメントを求める
        if len(i.column_no_each_node_x) > 1:#最上層、最下層以外で検討
            i.req_Mpx = temp_beam_Mp_x / len(i.beam_no_each_node_x)
        else:
            i.req_Mpx = 0

        if len(i.column_no_each_node_y) > 1:  # 最上層、最下層以外で検討
            i.req_Mpy = temp_beam_Mp_y / len(i.beam_no_each_node_y)
        else:
            i.req_Mpy = 0

#必要最低柱断面の算定
def calc_limit_column_size(nodes,layers,columns,beams,EE):

    #柱リストの読み込み
    column_list = pd.read_csv("column_list.csv", header=0)

    # 剛性チェックに基づく各層柱の必要剛性の算定
    calc_based_stiffness(nodes, layers, beams, columns, EE)

    # 柱梁耐力比チェックに基づく各柱の必要剛性の算定
    member_strength_check(nodes, beams, columns)

    #各柱について剛性チェックに基づく断面二次モーメント、
    #柱梁耐力比チェックに基づく柱の全塑性耐力を満たす最低柱断面の算定
    for i in columns:
        #剛性チェックに基づく断面二次モーメントのクライテリアの呼び出し
        minimum_Ix = layers[len(layers)-i.story].I_limit1_x
        minimum_Iy = layers[len(layers)-i.story].I_limit1_y
        #柱梁耐力比チェックに基づく全塑性モーメントのクライテリアの呼び出し
        minimum_Mpx = max(float(nodes[i.i-1].req_Mpx),float(nodes[i.j-1].req_Mpx)) / i.decrement_ratio_x
        minimum_Mpy = max(float(nodes[i.i-1].req_Mpy),float(nodes[i.j-1].req_Mpy)) / i.decrement_ratio_y

        #柱リストより得られた各諸元以上のキャパシティを有する柱断面の選定
        filtered_data = column_list[(column_list['Mpx'] > minimum_Mpx) & (column_list['Mpy'] > minimum_Mpy)
                                    & (column_list['Ix'] > minimum_Ix) & (column_list['Iy'] > minimum_Iy)]
        if len(filtered_data) >= 1:#選定リストから選べる場合
            i.minimum_selected_section_no = list(filtered_data['No'])[0]

    #得られた最低柱断面諸元に更新
            target_row = column_list[column_list['No'] == i.minimum_selected_section_no]
            i.t = float(target_row['t'])
            i.A = float(target_row['A'])
            i.Ix = float(target_row['Ix'])
            i.Iy = float(target_row['Iy'])
            i.selected_section_no = float(target_row['No'])
        #部材自重の算定
            i.unit_weight = float(target_row["unit_m"]*9.80665/1000)
            i.weight = i.unit_weight * i.length #部材自重
        #算定柱せいによる等価な基礎梁剛度の取得
            i.base_K = float(target_row['base_K'])
            i.H = float(target_row['H'])
            i.Zp = float(target_row['Zp'])
            i.F = float(target_row['F'])
        #選定リストの上限値を超えている場合
        else:
            print("requirement value is over upper limit of column_list.")
            i.t = "Error"
            i.A = "Error"
            i.Ix = "Error"
            i.Iy = "Error"
            i.selected_section_no = "Error"
            # 部材自重の算定
            i.unit_weight = "Error"
            i.weight = "Error"  # 部材自重
        # 算定柱せいによる等価な基礎梁剛度の取得
            i.base_K = "Error"
            i.H = "Error"
            i.Zp = "Error"
            i.F = "Error"

#応力に基づく柱断面の必要板厚の算定
def calc_column_thickness(columns):

    #柱リストの読み込み
    column_list = pd.read_csv("column_list.csv", header=0)

    #板厚の設定
    for i in columns:
        if i.H != "Error":#柱の最低断面が決められている場合のみ板厚の更新を実施
            i.tc1 = (0.75*(i.MLx+i.MLy)*10**6/i.H**2/(i.F/1.5)+i.NL*1000/(4*i.H)/(i.F/1.5*0.9))*1.1
            i.tc2x = (0.75*i.MSx*10**6/i.H**2/i.F+i.NL*1000/(4*i.H)/(i.F*0.9))*1.1
            i.tc2y = (0.75*i.MSy*10**6/i.H**2/i.F+i.NL*1000/(4*i.H)/(i.F*0.9))*1.1
            i.tc = max(i.tc1,i.tc2x,i.tc2y)

    #柱リストより得られた板厚以上のキャパシティを有する柱断面の選定
            filtered_data = column_list[(column_list['t'] > i.tc) & (column_list['H'] == i.H)]
            if len(filtered_data) != 0:#柱リストの中に必要板厚以上のものがある場合リストから選定
                i.minimum_selected_section_no = list(filtered_data['No'])[0]

                # 得られた最低柱断面諸元に更新
                target_row = column_list[column_list['No'] == i.minimum_selected_section_no]

                i.A = float(target_row['A'])
                i.t = float(target_row['t'])
                i.Ix = float(target_row['Ix'])
                i.Iy = float(target_row['Iy'])
                i.selected_section_no = float(target_row['No'])
                # 部材自重の算定
                i.unit_weight = float(target_row["unit_m"] * 9.80665 / 1000)
                i.weight = i.unit_weight * i.length  # 部材自重
                # 算定柱せいによる等価な基礎梁剛度の取得
                i.base_K = float(target_row['base_K'])
                i.H = float(target_row['H'])
                i.Zp = float(target_row['Zp'])
                i.F = float(target_row['F'])

            else:#柱リストの中に必要板厚以上のものがない場合
             #必要板厚に基づく板厚の更新
                i.t  = math.ceil(i.tc)#小数第一位で切り上げ
            #
            # #断面諸元の再計算（更新した板厚で実施）
                i.A = ((i.H)**2 - (i.H-i.t*2)**2)/1000000
                i.Ix = (((i.H)**4-(i.H-i.t*2)**4)/12)/10**12
                i.Iy = ((i.H)**4-(i.H-i.t*2)**4)/12/10**12
                i.Z = ((i.H)**4-(i.H-i.t*2)**4)/(6*i.H)/10**9

#柱断面を長期・短期応力評価結果に基づいて更新
def update_column_section(nodes,beams,columns,layers,EE):
    #剛性チェック、柱梁耐力比に基づく必要最低柱断面の算定
    calc_limit_column_size(nodes,layers,columns,beams,EE)
    #応力に基づく柱断面の必要板厚の算定
    calc_column_thickness(columns)


