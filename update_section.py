import math
import pandas as pd
import numpy as np
import itertools
import calc_stress
from member_class import *
from set_initial_section import *

# 隣接グループの梁せいチェック
def check_beam_height(nodes, beam_groups, beams):
    # 各梁グループが隣接する梁を調べる
    for beam_group in beam_groups:
        temp3 = []
        for j in beam_group.ID:  # そのグループに属する梁の隣接する梁の洗い出し
            temp3.extend(nodes[beams[j - 1].i - 1].beam_no_each_node2_x +
                         nodes[beams[j - 1].i - 1].beam_no_each_node2_y +
                         nodes[beams[j - 1].j - 1].beam_no_each_node2_x +
                         nodes[beams[j - 1].j - 1].beam_no_each_node2_y)
            temp3.remove(j)  # 自分自身を除く
            temp3.remove(j)
        beam_group.neighbor_beam = list(set(temp3))

        # 各梁グループが隣接する梁のグループを調べる
        temp4 = [];
        temp5 = []
        for j in beam_group.neighbor_beam:
            for beam_group2 in beam_groups:
                if j in beam_group2.ID:
                    temp4.append(beam_group2.group_name)
                    temp5.append(beam_group2.no)
        temp4 = set(temp4)
        temp5 = set(temp5)
        beam_group.neighbor_group = temp4
        beam_group.neighbor_group_no = temp5

    beam_height_condition = "beam height is OK"
    check1 = True
    for beam_group in beam_groups:
        test_H = beams[beam_group.ID[0] - 1].H  # グループに属する梁のせい
        for j in beam_group.neighbor_group_no:
            neighbor_H = beams[beam_groups[j - 1].ID[0] - 1].H  # 隣接する梁グループに属する梁のせい
            if abs(test_H-neighbor_H) > 5 and abs(test_H-neighbor_H) < 200:#せいに調整が必要な場合　NGを返す
                #beam_height_condition ="beam height is NG"
                check1 = False
                break
    return beam_height_condition, check1

#ダイヤフラムの形状制約に基づく梁せいの調整
def revise_beam_height(nodes,beam_groups,beams,selected_beam_list):

    # 各梁グループが隣接する梁を調べる
    for beam_group in beam_groups:
        temp3 = []
        for j in beam_group.ID:  # そのグループに属する梁の隣接する梁の洗い出し
            temp3.extend(nodes[beams[j - 1].i - 1].beam_no_each_node2_x +
                         nodes[beams[j - 1].i - 1].beam_no_each_node2_y +
                         nodes[beams[j - 1].j - 1].beam_no_each_node2_x +
                         nodes[beams[j - 1].j - 1].beam_no_each_node2_y)
            temp3.remove(j)  # 自分自身を除く
            temp3.remove(j)
        beam_group.neighbor_beam = list(set(temp3))

        # 各梁グループが隣接する梁のグループを調べる
        temp4 = [];
        temp5 = []
        for j in beam_group.neighbor_beam:
            for beam_group2 in beam_groups:
                if j in beam_group2.ID:
                    temp4.append(beam_group2.group_name)
                    temp5.append(beam_group2.no)
        temp4 = set(temp4)
        temp5 = set(temp5)
        beam_group.neighbor_group = temp4
        beam_group.neighbor_group_no = temp5

    #比較する順序を設定（梁高さが大きいものから順に比較）
    for group in beam_groups:
        group.neighbor_group = sorted(group.neighbor_group, reverse=True)#各節点で大きいものから比較するため隣接梁のリストは降順に並べる）
        print(group.group_name,group.neighbor_group)

    # 各梁グループについて、隣接する梁のグループのせいとの関係性を調べる（小さい差の調整）
    group_no =0
    while group_no < len(beam_groups):
        test_H = beams[beam_groups[group_no].ID[0] - 1].H  # グループに属する梁のせい
        for j in beam_groups[group_no].neighbor_group_no:
            neighbor_H = beams[beam_groups[j - 1].ID[0] - 1].H  # 隣接する梁グループに属する梁のせい
            # 梁高さの差が150mm以内の場合なら小さい方の梁せいを合わせにいく(588と600の隣接はOK）(2/7 revised)
            if abs(float(test_H) - float(neighbor_H)) > 5 \
                    and abs(float(test_H) - float(neighbor_H)) <= 150:
                # 算定梁せいに適合する梁の選定
                if float(test_H) >= float(neighbor_H):
                    filtered_beam_list = selected_beam_list[
                        (selected_beam_list['H'] == test_H) & (selected_beam_list['Zp'] >= beams[beam_groups[group_no].ID[0] - 1].Zp)]
                    for k in beam_groups[j - 1].ID:
                        beams[k - 1].I = float(list(filtered_beam_list['Ix'])[0])
                        beams[k - 1].selected_section_no = float(list(filtered_beam_list['No'])[0])
                        beams[k - 1].H = float(list(filtered_beam_list['H'])[0])
                        beams[k - 1].B = float(list(filtered_beam_list['B'])[0])
                        beams[k - 1].t1 = float(list(filtered_beam_list['t1'])[0])
                        beams[k - 1].t2 = float(list(filtered_beam_list['t2'])[0])
                        beams[k - 1].Z = float(list(filtered_beam_list['Z'])[0])
                        beams[k - 1].Zp = float(list(filtered_beam_list['Zp'])[0])
                        beams[k - 1].r = float(list(filtered_beam_list['r'])[0])
                        #beams[k - 1].F = float(list(filtered_beam_list['F'])[0])ここで変更した場合材質はオリジナルのまま（2/7 revised）
                    break  # 2重ループから抜ける
                else:
                    filtered_beam_list = selected_beam_list[(selected_beam_list['H'] == neighbor_H) & (
                                selected_beam_list['Zp'] >= beams[beam_groups[j - 1].ID[0] - 1].Zp)]
                    for k in beam_groups[group_no].ID:
                        beams[k - 1].I = float(list(filtered_beam_list['Ix'])[0])
                        beams[k - 1].selected_section_no = float(list(filtered_beam_list['No'])[0])
                        beams[k - 1].H = float(list(filtered_beam_list['H'])[0])
                        beams[k - 1].B = float(list(filtered_beam_list['B'])[0])
                        beams[k - 1].t1 = float(list(filtered_beam_list['t1'])[0])
                        beams[k - 1].t2 = float(list(filtered_beam_list['t2'])[0])
                        beams[k - 1].Z = float(list(filtered_beam_list['Z'])[0])
                        beams[k - 1].Zp = float(list(filtered_beam_list['Zp'])[0])
                        beams[k - 1].r = float(list(filtered_beam_list['r'])[0])
                        #beams[k - 1].F = float(list(filtered_beam_list['F'])[0])ここで変更した場合材質はオリジナルのまま（2/7 revised）
                    break  # 2重ループから抜ける
        group_no += 1#梁成を更新しない場合次のグループをチェック

    # 梁断面の再グルーピング
    temp_list = [[beams[i].no, beams[i].H, beams[i].B, beams[i].story]
                 for i in range(len(beams))]
    table_columns = ["No", "H", "B", "story"]
    group_data = make_group(temp_list, table_columns, str("story"), str("H"))  # グルーピング
    beam_groups = [member_class.Beam_Group(*data) for data in group_data]  # インスタンスの定義

    # # 各梁グループが隣接する梁を調べる
    # for beam_group in beam_groups:
    #     temp3 = []
    #     for j in beam_group.ID:  # そのグループに属する梁の隣接する梁の洗い出し
    #         temp3.extend(nodes[beams[j - 1].i - 1].beam_no_each_node2_x +
    #                      nodes[beams[j - 1].i - 1].beam_no_each_node2_y +
    #                      nodes[beams[j - 1].j - 1].beam_no_each_node2_x +
    #                      nodes[beams[j - 1].j - 1].beam_no_each_node2_y)
    #         temp3.remove(j)  # 自分自身を除く
    #         temp3.remove(j)
    #     beam_group.neighbor_beam = list(set(temp3))
    #
    #     # 各梁グループが隣接する梁のグループを調べる
    #     temp4 = [];
    #     temp5 = []
    #     for j in beam_group.neighbor_beam:
    #         for k in beam_groups:
    #             if j in k.ID:
    #                 temp4.append(k.group_name)
    #                 temp5.append(k.no)
    #     temp4 = set(temp4)
    #     temp5 = set(temp5)
    #     beam_group.neighbor_group = temp4
    #     beam_group.neighbor_group_no = temp5
    #
    # # 各梁グループについて、隣接する梁のグル―プのせいとの関係性を調べる（大きい差の調整）
    # for beam_group in beam_groups:
    #     test_H = beams[beam_group.ID[0] - 1].H  # グループに属する梁のせい
    #     for j in beam_group.neighbor_group_no:
    #         neighbor_H = beams[beam_groups[j - 1].ID[0] - 1].H  # 隣接する梁グループに属する梁のせい
    #         # 梁高さの差が100mm～200mmの場合、大きい方の梁成を上げる
    #         if (abs(float(test_H) - float(neighbor_H)) > 100) \
    #                 and (abs(float(test_H) - float(neighbor_H)) <= 200):
    #             # 算定梁せいに適合する梁の選定
    #             if test_H >= neighbor_H:  # 元のグループの梁せいの方が大きい場合、そちらを上げる
    #                 temp = beams[beam_group.ID[0] - 1].selected_section_no + 1
    #
    #                 while True:
    #                     if temp <= max(selected_beam_list['No']):  # 1ランク上げたときに梁リストの上限を超えない場合
    #                         if int(temp) in selected_beam_list['No'].values:  # 対象の梁部材がリストに存在するとき
    #                             # 選んだ梁成の差が200以上ある場合、断面更新
    #                             if list(selected_beam_list[selected_beam_list['No'] == int(temp)]['H'])[
    #                                 0] - neighbor_H > 200:
    #                                 target_row = selected_beam_list[selected_beam_list['No'] == temp]
    #                                 for k in beam_group.ID:
    #                                     beams[k - 1].selected_section_no = float(target_row['No'])
    #                                     beams[k - 1].I = float(target_row['Ix'])
    #                                     beams[k - 1].H = float(target_row['H'])
    #                                     beams[k - 1].B = float(target_row['B'])
    #                                     beams[k - 1].t1 = float(target_row['t1'])
    #                                     beams[k - 1].t2 = float(target_row['t2'])
    #                                     beams[k - 1].Z = float(target_row['Z'])
    #                                     beams[k - 1].Zp = float(target_row['Zp'])
    #                                     beams[k - 1].F = float(target_row['F'])
    #                     else:  # 1ランク上げたときに梁リストの上限を超える場合
    #                         print("requirement value is over upper limit of beam_list.")
    #                         for k in beam_group.ID:
    #                             beams[k - 1].I = "Error"
    #                             beams[k - 1].H = "Error"
    #                             beams[k - 1].B = "Error"
    #                             beams[k - 1].t1 = "Error"
    #                             beams[k - 1].t2 = "Error"
    #                             beams[k - 1].Z = "Error"
    #                             beams[k - 1].Zp = "Error"
    #                             beams[k - 1].F = "Error"
    #                     temp += 1
    #             else:
    #                 temp = beams[beam_groups[j - 1].ID[0] - 1].selected_section_no + 1
    #                 while True:
    #                     if temp <= max(selected_beam_list['No']):  # 1ランク上げたときに梁リストの上限を超えない場合
    #                         if int(temp) in selected_beam_list['No'].values:  # 対象の梁部材がリストに存在するとき
    #                             # 選んだ梁成の差が200以上ある場合、断面更新
    #                             if list(selected_beam_list[selected_beam_list['No'] == temp]['H'])[0] - test_H > 200:
    #                                 target_row = selected_beam_list[selected_beam_list['No'] == temp]
    #                                 for k in beam_groups[j - 1].ID:
    #                                     beams[k - 1].selected_section_no = float(target_row['No'])
    #                                     beams[k - 1].I = float(target_row['Ix'])
    #                                     beams[k - 1].H = float(target_row['H'])
    #                                     beams[k - 1].B = float(target_row['B'])
    #                                     beams[k - 1].t1 = float(target_row['t1'])
    #                                     beams[k - 1].t2 = float(target_row['t2'])
    #                                     beams[k - 1].Z = float(target_row['Z'])
    #                                     beams[k - 1].Zp = float(target_row['Zp'])
    #                                     beams[k - 1].F = float(target_row['F'])
    #                                 break
    #                     else:  # 1ランク上げたときに梁リストの上限を超える場合
    #                         print("requirement value is over upper limit of beam_list.")
    #                         for k in beam_groups[j - 1].ID:
    #                             beams[k - 1].I = "Error"
    #                             beams[k - 1].H = "Error"
    #                             beams[k - 1].B = "Error"
    #                             beams[k - 1].t1 = "Error"
    #                             beams[k - 1].t2 = "Error"
    #                             beams[k - 1].Z = "Error"
    #                             beams[k - 1].Zp = "Error"
    #                             beams[k - 1].F = "Error"
    #                         frag = 1
    #                         break
    #                     temp += 1

#大梁断面を長期・短期応力評価結果に基づいて更新
def update_beam_section(nodes,beams,beam_select_mode,EE):

    #単位変換用係数
    m_to_mm = 1000.0#m→mmへ
    kN_to_N = 1000.0#kN→Nへ
    #準備計算
    #梁リストの読み込み
    beam_list = pd.read_csv("beam_list.csv", header=0)

    #選定モードに準じた梁リストのみ読み込む
    selected_beam_list = beam_list[beam_list['category'].str.contains(beam_select_mode,case=False, na=False)]
    sorted_H_beam_list = selected_beam_list.sort_values(by='H', ascending=True)#梁せいでソートしたリスト（とりあえず使わない）
    sorted_Z_beam_list = selected_beam_list.sort_values(by='Z', ascending=True)#断面係数でソートしたリスト（とりあえず使わない）
    #sorted_A_beam_list = selected_beam_list.sort_values(by='A', ascending=True)

    #応力による断面選定後のdeltaの設定
    for beam in beams:
        beam.rev_delta_x = beam.delta_x
        beam.rev_delta_y = beam.delta_y

    #応力による断面選定
    #梁応力の算定
    for beam in beams:
        if beam.category != "BB":#基礎梁以外の断面を更新
            beam.sigma_b_L = (beam.ML*kN_to_N*m_to_mm)/(beam.Z*m_to_mm**3-beam.t1*(beam.H-beam.t2*2)**2/6.0)#曲げ応力の算定時にウェブの断面係数は非考慮
            beam.sigma_b_s = (beam.Ms*kN_to_N*m_to_mm)/(beam.Z*m_to_mm**3-beam.t1*(beam.H-beam.t2*2)**2/6.0)#曲げ応力の算定時にウェブの断面係数は非考慮
            beam.tau_L = beam.QL*kN_to_N/((beam.H-beam.t2*2-beam.r*2)*beam.t1)
            beam.tau_s = beam.Qs*kN_to_N/((beam.H-beam.t2*2-beam.r*2)*beam.t1)
    #曲げ、せん断耐力の算定
            f_b = beam.F#取り合えずfb低減は考慮しない
            f_s = beam.F/math.sqrt(3)

    #検定比0.9を満たすために必要な梁の断面係数、ウェブ断面積の算定
            beam.required_web_area = max(beam.QL*kN_to_N/(0.9*f_s/1.5),beam.Qs*kN_to_N/(0.9*f_s))
            beam.required_Z = max(beam.ML*kN_to_N*m_to_mm/(0.9*f_b/1.5),beam.Ms*kN_to_N*m_to_mm/(0.9*f_b))

    #必要な梁の断面係数、ウェブ断面積以上の部材をリストより選定
            filtered_list = selected_beam_list[((selected_beam_list['Z']*m_to_mm**3-selected_beam_list['t1']*(selected_beam_list['H']-selected_beam_list['t2']*2)**2/6) \
                                                * selected_beam_list['F']/beam.F > beam.required_Z) &
            ((selected_beam_list['H']-selected_beam_list['t2']*2-selected_beam_list['r']*2)*selected_beam_list['t1'] * selected_beam_list['F']/beam.F \
              > beam.required_web_area)]

    #さらに梁せいの制限で絞り込み（スパンの1/20以上）
            filtered_list2 = filtered_list#filtered_list[(filtered_list['H']/(m_to_mm) > beam.length*1.0/20.0)]
            print(filtered_list2)

            beam.selected_section_no = float(list(filtered_list2['No'])[0])
            beam.I = float(list(filtered_list2['Ix'])[0])  # 断面諸元の更新
            beam.H = float(list(filtered_list2['H'])[0])
            beam.B = float(list(filtered_list2['B'])[0])
            beam.t1 = float(list(filtered_list2['t1'])[0])
            beam.t2 = float(list(filtered_list2['t2'])[0])
            beam.Z = float(list(filtered_list2['Z'])[0])
            beam.Zp = float(list(filtered_list2['Zp'])[0])
            beam.F = float(list(filtered_list2['F'])[0])
            beam.r = float(list(filtered_list2['r'])[0])

    #応力に基づく大梁の選定断面のメモリー
            beam.B_phase1 = beam.B
            beam.H_phase1 = beam.H
            beam.t1_phase1 = beam.t1
            beam.t2_phase1 = beam.t2
            beam.r_phase1 = beam.r

            # 大梁のたわみ算定に基づく断面更新(ダミーの基礎梁は除く）
            temp_no=0
            while True:
                if beam.direction == "X":
                    temp_M_Lx0 = beam.M0 - np.average([abs(beam.M_Lx[0]), abs(beam.M_Lx[1])])
                    temp_delta_x = (5 * beam.M0 / (48.0 * EE * beam.I) * beam.length ** 2
                                - (abs(beam.M_Lx[0])+abs(beam.M_Lx[1])) / (16.0 * EE * beam.I) * beam.length ** 2)  # 梁中央のたわみ（未検証）

                # 大梁たわみが1/300以上または20mm以上の場合大梁断面を更新
                    if abs(temp_delta_x / beam.length) >= 1.0 / 300.0: #or temp_delta_x > 0.02: (2/7 revised)
                    #NGの場合梁リストから一段上げて再確認
                        temp_no += 1
                        beam.I = float(list(filtered_list2['Ix'])[temp_no])  # 断面諸元の更新
                        beam.H = float(list(filtered_list2['H'])[temp_no])
                        beam.B = float(list(filtered_list2['B'])[temp_no])
                        beam.t1 = float(list(filtered_list2['t1'])[temp_no])
                        beam.t2 = float(list(filtered_list2['t2'])[temp_no])
                        beam.Z = float(list(filtered_list2['Z'])[temp_no])
                        beam.Zp = float(list(filtered_list2['Zp'])[temp_no])
                        beam.F = float(list(filtered_list2['F'])[temp_no])
                        beam.r = float(list(filtered_list2['r'])[temp_no])
                        print("Beam deflection is NG")
                    else:
                        print("Beam deflection is OK")
                        break
                else:
                    temp_M_Ly0 = beam.M0 - np.average([abs(beam.M_Ly[0]), abs(beam.M_Ly[1])])
                    temp_delta_y = (5 * beam.M0 / (48.0 * EE * beam.I) * beam.length ** 2
                                - (abs(beam.M_Ly[0])+abs(beam.M_Ly[1])) / (16.0 * EE * beam.I) * beam.length ** 2)  # 梁中央のたわみ（未検証）
                # 大梁たわみが1/300以下であるか確認
                    if abs(temp_delta_y / beam.length) >= 1.0 / 300.0: #or temp_delta_y >= 0.02: (2/7 revised)
                    # NGの場合梁リストから一段上げて再確認
                        temp_no += 1
                        beam.I = float(list(filtered_list2['Ix'])[temp_no])  # 断面諸元の更新
                        beam.H = float(list(filtered_list2['H'])[temp_no])
                        beam.B = float(list(filtered_list2['B'])[temp_no])
                        beam.t1 = float(list(filtered_list2['t1'])[temp_no])
                        beam.t2 = float(list(filtered_list2['t2'])[temp_no])
                        beam.Z = float(list(filtered_list2['Z'])[temp_no])
                        beam.Zp = float(list(filtered_list2['Zp'])[temp_no])
                        beam.F = float(list(filtered_list2['F'])[temp_no])
                        beam.r = float(list(filtered_list2['r'])[temp_no])
                        print("Beam deflection is NG")
                    else:
                        print("Beam deflection is OK")
                        break
            #更新後断面のdeltaを格納
            if beam.direction == "X":
                beam.rev_delta_x = temp_delta_x
            elif beam.direction == "Y":
                beam.rev_delta_y = temp_delta_y

            # 長期たわみ考慮に基づく大梁の選定断面のメモリー
            beam.B_phase2 = beam.B
            beam.H_phase2 = beam.H
            beam.t1_phase2 = beam.t1
            beam.t2_phase2 = beam.t2
            beam.r_phase2 = beam.r

            # i.judge_b_L = sigma_b_L/(f_b/1.5)
            # i.judge_b_s = sigma_b_s/f_b
            # i.judge_s_L = tau_L/(f_s/1.5)
            # i.judge_s_s = tau_s/f_s

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

    #梁せいの調整アルゴリズムの実行
    while True:
    #隣接グループの梁せいチェック
        beam_height_condition, check1 = check_beam_height(nodes,beam_groups,beams)
    #以下チェック結果がNGの場合、OKになるまで実施
        print(beam_height_condition)
    #ダイヤフラムの形状制約に基づく梁せいの調整
        if check1 is False:
            revise_beam_height(nodes,beam_groups,beams,selected_beam_list)
        else:#OKの場合アルゴリズムのループを抜ける
            break

    # ダイヤフラム調整後の大梁の選定断面のメモリー
    for beam in beams:
        beam.B_phase3 = beam.B
        beam.H_phase3 = beam.H
        beam.t1_phase3 = beam.t1
        beam.t2_phase3 = beam.t2
        beam.r_phase3 = beam.r

    #梁断面の更新に伴う剛度の更新
    for beam in beams:
        if beam.category != "BB":#基礎梁以外の断面を更新
            # 梁せいに応じた床スラブによる梁の剛性増大率の考慮
            if beam.H <= 600:
                beam.K = beam.I/beam.length*m_to_mm**2*beam.pai2#床スラブの剛性増大率考慮
            else:
                beam.K = beam.I/beam.length*m_to_mm**2*beam.pai#床スラブの剛性増大率考慮

#剛性チェックに基づく各層柱の必要剛性の算定
def calc_based_stiffness(nodes,layers,beams,columns,EE):

    #単位変換用係数
    m_to_mm = 1000.0#m→mmへ
    kN_to_N = 1000.0#kN→Nへ

    for layer in layers:
    #各層の層間変形角1/200を満たすために必要な柱のD値算定
        layer.req_D_sum_x = layer.shear_force_x*kN_to_N*(layer.height*m_to_mm)**2/12.0/EE/(layer.height*m_to_mm/200.0)/10**2
        layer.req_D_sum_y = layer.shear_force_y*kN_to_N*(layer.height*m_to_mm)**2/12.0/EE/(layer.height*m_to_mm/200.0)/10**2

    #各層柱のD値、D値の最大値の集計
    temp_x = np.zeros(len(layers))
    temp_y = np.zeros(len(layers))
    temp_max_x = np.zeros(len(layers))
    temp_max_y = np.zeros(len(layers))

    beam_stiff_x =[];beam_stiff_y=[]
    for column in columns:
        temp_x[len(layers)-column.story] += column.D_x
        temp_y[len(layers)-column.story] += column.D_y
        if temp_max_x[len(layers)-column.story] <= column.D_x:
            temp_max_x[len(layers) - column.story] = column.D_x
        if temp_max_y[len(layers) - column.story] <= column.D_y:
            temp_max_y[len(layers) - column.story] = column.D_y

        #各柱の接する梁の剛度を足す
        #i端
        temp_stiff_x = 0
        temp_stiff_y = 0
        for k in nodes[column.i-1].beam_no_each_node2_x:
            temp_stiff_x += beams[k-1].K
        beam_stiff_x.append(float(temp_stiff_x))
        #j端
        for k in nodes[column.j-1].beam_no_each_node2_x:
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

        layers[i].I_limit1_x = layers[i].k_limit1_x * 10**5 * layers[i].height*m_to_mm/(10**12)
        layers[i].I_limit1_y = layers[i].k_limit1_y * 10**5 * layers[i].height*m_to_mm/(10**12)

#柱梁耐力比チェックに基づく各柱の必要剛性の算定
def member_strength_check(nodes,beams,columns,layers):
    #単位変換用係数
    m_to_mm = 1000.0#m→mmへ
    kN_to_N = 1000.0#kN→Nへ

    #梁の全塑性曲げモーメントの算定
    for beam in beams:
        if beam.category != "BB":#基礎梁以外の断面について算定
            beam.Mp = beam.F *1.0/1000.0*1000*1000* beam.Zp

    #柱の全塑性モーメント算定時には梁両端ヒンジ時の軸力を考慮
    #各柱の軸力算定（梁両端ヒンジ時）
    for column in columns:
            #各柱にとりつく梁のせん断力から想定される軸力を算定
        if nodes[column.i-1].z > nodes[column.j-1].z:  # 上はりの剪断力を参照
            #i端側がj端側よりも高い場合
            temp = nodes[column.i-1].beam_no_each_node_x#i端部材no
            temp2 = nodes[column.i-1].beam_no_each_node_y
        else:
            temp = nodes[column.j-1].beam_no_each_node_x
            temp2 = nodes[column.j-1].beam_no_each_node_y#j端部材no

        #柱の上側に取りつく梁の両端ヒンジ時のせん断力の差分がはりの剪断力による軸力となる
        if len(temp) == 1:
            Mp_beam = beams[temp[0]-1].Zp*10**9*beams[temp[0]-1].F/(10**6)
            column.temp_axial_column_x_Mp = Mp_beam*2/beams[temp[0]-1].length
        elif len(temp) == 2:
            Mp_beam1 = beams[temp[0]-1].Zp*10**9*beams[temp[0]-1].F/(10**6)
            Mp_beam2 = beams[temp[1]-1].Zp*10**9*beams[temp[1]-1].F/(10**6)
            column.temp_axial_column_x_Mp = abs(Mp_beam1*2/beams[temp[0]-1].length
                                                -Mp_beam2*2/beams[temp[1]-1].length)

        if len(temp2) == 1:
            Mp_beam = beams[temp2[0]-1].Zp*10**9*beams[temp2[0]-1].F/(10**6)
            column.temp_axial_column_y_Mp = Mp_beam*2/beams[temp2[0]-1].length
        elif len(temp2) == 2:
            Mp_beam1 = beams[temp2[0]-1].Zp*10**9*beams[temp2[0]-1].F/(10**6)
            Mp_beam2 = beams[temp2[1]-1].Zp*10**9*beams[temp2[1]-1].F/(10**6)
            column.temp_axial_column_y_Mp = abs(Mp_beam1*2/beams[temp2[0]-1].length
                                                -Mp_beam2*2/beams[temp2[1]-1].length)

        #上の層の柱の軸力から順に足す
    D_sum_x =np.zeros(len(layers))
    D_sum_y = np.zeros(len(layers))
    for layer in layers:
        for column in columns:
            if column.story == layer.story:
                if nodes[column.i-1].z > nodes[column.j-1].z:  # i端側がj端側よりも高い場合
                    temp = nodes[column.i-1].column_no_each_node_x#i端部材no
                    temp2 = nodes[column.i-1].column_no_each_node_y
                else:
                    temp = nodes[column.j-1].column_no_each_node_x
                    temp2 = nodes[column.j-1].column_no_each_node_y#j端部材no

                for j in temp:
                    if j != column.no:#自分以外の柱がある場合その柱の軸力を足す
                        column.axial_column_x_Mp = column.temp_axial_column_x_Mp+columns[j-1].temp_axial_column_x_Mp
                        column.temp_axial_column_x_Mp += columns[j-1].temp_axial_column_x_Mp #該当する柱の仮の軸力も更新する
                    else:
                        column.axial_column_x_Mp = column.temp_axial_column_x_Mp

                for j in temp2:
                    if j != column.no:  # 自分以外の柱がある場合その柱の軸力を足す
                        column.axial_column_y_Mp = column.temp_axial_column_y_Mp+ columns[j- 1].temp_axial_column_y_Mp
                        column.temp_axial_column_y_Mp += columns[j-1].temp_axial_column_y_Mp #該当する柱の仮の軸力も更新する
                    else:
                        column.axial_column_y_Mp = column.temp_axial_column_y_Mp

    #柱の全塑性モーメントの算定
    for column in columns:
        axial_ratio_x = column.axial_column_x_Mp * kN_to_N / (column.A*m_to_mm**2*column.F)#長期＋短期荷重時の柱軸力比
        if axial_ratio_x <= 0.5:#軸力比を考慮した全塑性曲げモーメントの低下率の算定
            column.decrement_ratio_x = 1-4*axial_ratio_x**2/3.0
        else:
            column.decrement_ratio_x = 4*(1-axial_ratio_x)/3.0

        axial_ratio_y = column.axial_column_y_Mp * kN_to_N / (column.A*m_to_mm**2*column.F)
        if axial_ratio_y <= 0.5:#軸力比を考慮した全塑性曲げモーメントの低下率の算定
            column.decrement_ratio_y = 1-4*axial_ratio_y**2/3.0
        else:
            column.decrement_ratio_y = 4*(1-axial_ratio_y)/3.0

        #低下率を考慮した柱の全塑性曲げモーメントの算定
        column.Mpx = column.decrement_ratio_x * column.F * 1.0/1000.0*1000*1000* column.Zp
        column.Mpy = column.decrement_ratio_y * column.F * 1.0/1000.0*1000*1000* column.Zp

    #各節点における柱梁耐力比の確認
    for node in nodes:
        #左右梁の全塑性モーメントの集計
        #X方向
        temp_beam_Mp_x =0
        for j in node.beam_no_each_node_x:
            #該当部分がピン接合の時は、該当梁のMpはカウントしない
            if (beams[j-1].boundary_i != "pin" and beams[j-1].i != node.no) or \
                (beams[j-1].boundary_j != "pin" and beams[j-1].j != node.no):
                temp_beam_Mp_x += beams[j-1].Mp
        #Y方向
        temp_beam_Mp_y = 0
        for j in node.beam_no_each_node_y:
            #該当部分がピン接合の時は、該当梁のMpはカウントしない
            if (beams[j-1].boundary_i != "pin" and beams[j-1].i != node.no) or \
                (beams[j-1].boundary_j != "pin" and beams[j-1].j != node.no):
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

        #柱梁耐力比が1.5以下の場合、1.5以上にするために必要な柱の全塑性モーメントを求める
        if len(node.column_no_each_node_x) > 1:#最上層、最下層以外で検討
            node.req_Mpx = temp_beam_Mp_x / len(node.beam_no_each_node_x)*1.5
        else:
            node.req_Mpx = 0

        if len(node.column_no_each_node_y) > 1:  # 最上層、最下層以外で検討
            node.req_Mpy = temp_beam_Mp_y / len(node.beam_no_each_node_y)*1.5
        else:
            node.req_Mpy = 0

#必要最低柱断面の算定
def calc_limit_column_size(nodes,layers,columns,beams,EE):
    #単位変換用係数
    m_to_mm = 1000.0#m→mmへ
    kN_to_N = 1000.0#kN→Nへ

    #柱リストの読み込み
    column_list = pd.read_csv("column_list.csv", header=0)

    # 剛性チェックに基づく各層柱の必要剛性の算定
    calc_based_stiffness(nodes, layers, beams, columns, EE)

    # 柱梁耐力比チェックに基づく各柱の必要剛性の算定
    member_strength_check(nodes, beams, columns, layers)

    #各柱について剛性チェックに基づく断面二次モーメント、
    #柱梁耐力比チェックに基づく柱の全塑性耐力を満たす最低柱断面の算定
    for column in columns:
        #剛性チェックに基づく断面二次モーメントのクライテリアの呼び出し
        minimum_Ix = layers[len(layers)-column.story].I_limit1_x
        minimum_Iy = layers[len(layers)-column.story].I_limit1_y
        #柱梁耐力比チェックに基づく全塑性モーメントのクライテリアの呼び出し
        minimum_Mpx = max(float(nodes[column.i-1].req_Mpx),float(nodes[column.j-1].req_Mpx)) / column.decrement_ratio_x
        minimum_Mpy = max(float(nodes[column.i-1].req_Mpy),float(nodes[column.j-1].req_Mpy)) / column.decrement_ratio_y

        #柱リストより得られた各諸元以上のキャパシティを有する柱断面の選定
        filtered_data = column_list[(column_list['Mpx'] > minimum_Mpx) & (column_list['Mpy'] > minimum_Mpy)
                                    & (column_list['Ix'] > minimum_Ix) & (column_list['Iy'] > minimum_Iy)]
        if len(filtered_data) >= 1:#選定リストから選べる場合
            column.minimum_selected_section_no = list(filtered_data['No'])[0]

    #得られた最低柱断面諸元に更新
            target_row = column_list[column_list['No'] == column.minimum_selected_section_no]
            column.t = float(target_row['t'])
            column.A = float(target_row['A'])
            column.Ix = float(target_row['Ix'])
            column.Iy = float(target_row['Iy'])
            column.selected_section_no = float(target_row['No'])
        #部材自重の算定
            column.unit_weight = float(target_row["unit_m"]*9.80665/m_to_mm)
            column.weight = column.unit_weight * column.length #部材自重
        #算定柱せいによる等価な基礎梁剛度の取得
            column.base_K = float(target_row['base_K'])
            column.H = float(target_row['H'])
            column.Zp = float(target_row['Zp'])
            column.F = float(target_row['F'])
        #選定リストの上限値を超えている場合
        else:
            print("requirement value is over upper limit of column_list.")
            column.t = "Error"
            column.A = "Error"
            column.Ix = "Error"
            column.Iy = "Error"
            column.selected_section_no = "Error"
            # 部材自重の算定
            column.unit_weight = "Error"
            column.weight = "Error"  # 部材自重
        # 算定柱せいによる等価な基礎梁剛度の取得
            column.base_K = "Error"
            column.H = "Error"
            column.Zp = "Error"
            column.F = "Error"

        #柱の剛度の算定(単位cm3）
        column.KX = column.Ix/column.length*1000000.0
        column.KY = column.Iy/column.length*1000000.0

#応力に基づく柱断面の必要板厚の算定
def calc_column_thickness(columns):

    #単位変換用係数
    m_to_mm = 1000.0#m→mmへ
    kN_to_N = 1000.0#kN→Nへ

    #柱リストの読み込み
    column_list = pd.read_csv("column_list.csv", header=0)

    #板厚の設定
    for column in columns:
        if column.H != "Error":#柱の最低断面が決められている場合のみ板厚の更新を実施
            column.tc1 = (0.75*(column.MLx+column.MLy)*m_to_mm*kN_to_N/column.H**2/(column.F/1.5)+column.NL*kN_to_N/(4*column.H)/(column.F/1.5*0.9))*1.1
            column.tc2x = (0.75*column.MSx*m_to_mm*kN_to_N/column.H**2/column.F+column.NL*kN_to_N/(4*column.H)/(column.F*0.9))*1.1
            column.tc2y = (0.75*column.MSy*m_to_mm*kN_to_N/column.H**2/column.F+column.NL*kN_to_N/(4*column.H)/(column.F*0.9))*1.1
            column.tc = max(column.tc1,column.tc2x,column.tc2y)

    #柱リストより得られた板厚以上のキャパシティを有する柱断面の選定
            filtered_data = column_list[(column_list['t'] > column.tc) & (column_list['H'] == column.H)]
            if len(filtered_data) != 0:#柱リストの中に必要板厚以上のものがある場合リストから選定
                column.minimum_selected_section_no = list(filtered_data['No'])[0]

                # 得られた最低柱断面諸元に更新
                target_row = column_list[column_list['No'] == column.minimum_selected_section_no]

                column.A = float(target_row['A'])
                column.t = float(target_row['t'])
                column.Ix = float(target_row['Ix'])
                column.Iy = float(target_row['Iy'])
                column.selected_section_no = float(target_row['No'])
                # 部材自重の算定
                column.unit_weight = float(target_row["unit_m"] * 9.80665 /m_to_mm)
                column.weight = column.unit_weight * column.length  # 部材自重
                # 算定柱せいによる等価な基礎梁剛度の取得
                column.base_K = float(target_row['base_K'])
                column.H = float(target_row['H'])
                column.Zp = float(target_row['Zp'])
                column.F = float(target_row['F'])

            else:#柱リストの中に必要板厚以上のものがない場合（ビルドエッジを使うことをとりあえず想定）
             #必要板厚に基づく板厚の更新
                column.t  = math.ceil(column.tc)#小数第一位で切り上げ
            #
            # #断面諸元の再計算（更新した板厚で実施）
                column.A = ((column.H)**2 - (column.H-column.t*2)**2)/m_to_mm**2
                column.Ix = (((column.H)**4-(column.H-column.t*2)**4)/12.0)/m_to_mm**4
                column.Iy = ((column.H)**4-(column.H-column.t*2)**4)/12.0/m_to_mm**4
                column.Z = ((column.H)**4-(column.H-column.t*2)**4)/(6*column.H)/m_to_mm**3

        #柱の剛度の算定(単位cm3）
            column.KX = column.Ix/column.length*1000000.0
            column.KY = column.Iy/column.length*1000000.0

#柱断面を長期・短期応力評価結果に基づいて更新
def update_column_section(nodes,beams,columns,layers,EE):
    #剛性チェック、柱梁耐力比に基づく必要最低柱断面の算定
    calc_limit_column_size(nodes,layers,columns,beams,EE)
    #応力に基づく柱断面の必要板厚の算定
    calc_column_thickness(columns)
    #更新後断面における剛比算定
    calc_stress.calc_stiffness_ratio(columns,beams,nodes)