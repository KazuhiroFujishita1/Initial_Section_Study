import math
import pandas as pd
import numpy as np
import itertools

#大梁断面を長期・短期応力評価結果に基づいて更新
def update_beam_section(nodes,beams,beam_select_mode):
    #梁リストの読み込み
    beam_list = pd.read_csv("beam_list.csv", header=0)

    #選定モードに準じた梁リストのみ読み込む
    selected_beam_list = beam_list[beam_list['category'].str.contains(beam_select_mode,case=False, na=False)]

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

            i.judge_b_L = sigma_b_L/(f_b/1.5)
            i.judge_b_s = sigma_b_s/f_b
            i.judge_s_L = tau_L/(f_s/1.5)
            i.judge_s_s = tau_s/f_s

    #曲げせん断検定比が0.9以上の場合、選定部材を1ランク上げる
            if i.judge_b_L >= 0.9 or i.judge_b_s >= 0.9 or i.judge_s_L >= 0.9 or i.judge_s_s >= 0.9:
                temp = i.selected_section_no + 1

                while True:
                    if temp <= max(beam_list['No']):  # 1ランク上げたときに梁リストの上限を超えない場合
                        if int(temp) in selected_beam_list['No'].values:  # 対象の梁部材がリストに存在するとき
                            target_row = selected_beam_list[selected_beam_list['No'] == temp]

                            if i.judge_b_L >= 0.9 or i.judge_b_s >= 0.9:#曲げが厳しい場合、選定リストの断面係数を確認
                                if float(target_row['Z'])/i.Z * float(target_row['F'])/i.F > max(i.judge_b_L,i.judge_b_s)/0.9:#検定比を満たせる程度Zがあげられた場合断面更新(F値の違いの影響も考慮）
                                    i.I = float(target_row['Ix'])  # 断面諸元の更新
                                    i.H = float(target_row['H'])
                                    i.B = float(target_row['B'])
                                    i.t1 = float(target_row['t1'])
                                    i.t2 = float(target_row['t2'])
                                    i.Z = float(target_row['Z'])
                                    i.Zp = float(target_row['Zp'])
                                    i.F = float(target_row['F'])
                                    break
                            if i.judge_s_L >= 0.9 or i.judge_s_s >= 0.9:#せん断が厳しい場合、選定リストのウェブ断面積を確認
                                if float(target_row['H'])*float(target_row['t1'])/i.H*i.t1 * float(target_row['F'])/i.F > max(i.judge_s_L,i.judge_s_s)/0.9:#検定比を満たせる程度ウェブ断面積があげられた場合断面更新(F値の違いの影響も考慮）
                                    i.I = float(target_row['Ix'])  # 断面諸元の更新
                                    i.H = float(target_row['H'])
                                    i.B = float(target_row['B'])
                                    i.t1 = float(target_row['t1'])
                                    i.t2 = float(target_row['t2'])
                                    i.Z = float(target_row['Z'])
                                    i.Zp = float(target_row['Zp'])
                                    i.F = float(target_row['F'])
                                    break
                            if (i.judge_b_L >= 0.9 or i.judge_b_s >= 0.9) and (i.judge_s_L >= 0.9 or i.judge_s_s >= 0.9):
                        #曲げとせん断がともに厳しい場合、選定リストのウェブ断面積を確認
                                if (float(target_row['Z'])/i.Z *float(target_row['F'])/i.F > max(i.judge_b_L,i.judge_b_s)/0.9) and \
                                (float(target_row['H'])*float(target_row['t1'])/i.H*i.t1 * float(target_row['F'])/i.F >
                                 max(i.judge_s_L,i.judge_s_s)/0.9):#検定比を満たせる程度断面係数、ウェブ断面積があげられた場合断面更新
                                    i.I = float(target_row['Ix'])  # 断面諸元の更新
                                    i.H = float(target_row['H'])
                                    i.B = float(target_row['B'])
                                    i.t1 = float(target_row['t1'])
                                    i.t2 = float(target_row['t2'])
                                    i.Z = float(target_row['Z'])
                                    i.Zp = float(target_row['Zp'])
                                    i.F = float(target_row['F'])
                                    break
                    else:# 1ランク上げたときに梁リストの上限を超える場合
                        print("requirement value is over upper limit of beam_list.")
                        i.I = "Error"  # 断面諸元の更新
                        i.H = "Error"
                        i.B = "Error"
                        i.t1 = "Error"
                        i.t2 = "Error"
                        i.Z = "Error"
                        i.Zp = "Error"
                        i.F = "Error"
                        break
                    temp += 1

        #各節点における隣接する梁のダイヤフラム段差幅の確認とそれに伴う断面修正（ここはまだ少し穴がありそう）
    for i in nodes:
        #XY方向の梁せいをともに確認する
        confirm_beam_list = i.beam_no_each_node_x + i.beam_no_each_node_y
        test_case = list(itertools.permutations(confirm_beam_list,2))#比較するケースの洗い出し
        index = 0
        frag = 0
        while index < len(test_case):
            item = test_case[index]

            if abs(float(beams[item[0]-1].H) - float(beams[item[1]-1].H)) <= 5:#梁高さの差が5mm以内ならそのまま
                index += 1
                # 梁高さの差が100mm以内の場合なら小さい方の梁せいを合わせにいく
            elif (abs(float(beams[item[0] - 1].H) - float(beams[item[1] - 1].H)) > 5) \
                    and (abs(float(beams[item[0]-1].H) - float(beams[item[1]-1].H)) <= 100):
                # 算定梁せいに適合する梁の選定
                if float(beams[item[0]-1].H) >= float(beams[item[1]-1].H):
                    beams[item[1] - 1].selected_section_no = float(beams[item[0]-1].selected_section_no)
                    beams[item[1] - 1].I = float(beams[item[0]-1].I)
                    beams[item[1] - 1].H = float(beams[item[0]-1].H)
                    beams[item[1] - 1].B = float(beams[item[0]-1].B)
                    beams[item[1] - 1].t1 = float(beams[item[0]-1].t1)
                    beams[item[1] - 1].t2 = float(beams[item[0]-1].t2)
                    beams[item[1] - 1].Z = float(beams[item[0] - 1].Z)
                    beams[item[1] - 1].Zp = float(beams[item[0] - 1].Zp)
                    beams[item[1] - 1].F = float(beams[item[0] - 1].F)
                else:
                    beams[item[0] - 1].selected_section_no = float(beams[item[1]-1].selected_section_no)
                    beams[item[0] - 1].I = float(beams[item[1]-1].I)
                    beams[item[0] - 1].H = float(beams[item[1]-1].H)
                    beams[item[0] - 1].B = float(beams[item[1]-1].B)
                    beams[item[0] - 1].t1 = float(beams[item[1]-1].t1)
                    beams[item[0] - 1].t2 = float(beams[item[1]-1].t2)
                    beams[item[0] - 1].Z = float(beams[item[1] - 1].Z)
                    beams[item[0] - 1].Zp = float(beams[item[1] - 1].Zp)
                    beams[item[0] - 1].F = float(beams[item[1] - 1].F)

                index = 0 #もう一度リスタート

            # 梁高さの差が100mm～200mmの場合、大きい方の梁成を上げる
            elif (abs(float(beams[item[0]-1].H) - float(beams[item[1]-1].H)) > 100) \
                    and (abs(float(beams[item[0]-1].H) - float(beams[item[1]-1].H)) <= 200):
                # 算定梁せいに適合する梁の選定
                if beams[item[0]-1].H >= beams[item[1]-1].H:
                    temp = beams[item[0]-1].selected_section_no + 1

                    while True:
                        if temp <= max(beam_list['No']):  # 1ランク上げたときに梁リストの上限を超えない場合
                            if int(temp) in selected_beam_list['No'].values:#対象の梁部材がリストに存在するとき
                        #選んだ梁成の差が200以上ある場合、断面更新
                                if list(selected_beam_list[selected_beam_list['No'] == int(temp)]['H'])[0] - beams[item[1]-1].H > 200:
                                    target_row = selected_beam_list[selected_beam_list['No'] == temp]
                                    beams[item[0]-1].selected_section_no = float(target_row['No'])
                                    beams[item[0]-1].I =float(target_row['Ix'])
                                    beams[item[0]-1].H =float(target_row['H'])
                                    beams[item[0] - 1].B = float(target_row['B'])
                                    beams[item[0]-1].t1 =float(target_row['t1'])
                                    beams[item[0]-1].t2 =float(target_row['t2'])
                                    beams[item[0]-1].Z =float(target_row['Z'])
                                    beams[item[0]-1].Zp =float(target_row['Zp'])
                                    beams[item[0]-1].F =float(target_row['F'])
                                    index = 0#もう一度リスタート
                                    break
                        else:  # 1ランク上げたときに梁リストの上限を超える場合
                            print("requirement value is over upper limit of beam_list.")
                            i.I = "Error"  # 断面諸元の更新
                            i.H = "Error"
                            i.B = "Error"
                            i.t1 = "Error"
                            i.t2 = "Error"
                            i.Z = "Error"
                            i.Zp = "Error"
                            i.F = "Error"
                            frag = 1 #次の比較へ
                            break

                        temp += 1

                else:
                    temp = beams[item[1]-1].selected_section_no + 1
                    while True:
                        if temp <= max(beam_list['No']):  # 1ランク上げたときに梁リストの上限を超えない場合
                            if int(temp) in selected_beam_list['No'].values:#対象の梁部材がリストに存在するとき
                        # 選んだ梁成の差が200以上ある場合、断面更新
                                if list(selected_beam_list[selected_beam_list['No'] == temp]['H'])[0] - beams[item[0] - 1].H > 200:
                                    target_row = selected_beam_list[selected_beam_list['No'] == temp]
                                    beams[item[1]-1].selected_section_no = float(target_row['No'])
                                    beams[item[1]-1].I =float(target_row['Ix'])
                                    beams[item[1]-1].H =float(target_row['H'])
                                    beams[item[1] - 1].B = float(target_row['B'])
                                    beams[item[1]-1].t1 = float(target_row['t1'])
                                    beams[item[1]-1].t2 = float(target_row['t2'])
                                    beams[item[1]-1].Z = float(target_row['Z'])
                                    beams[item[1]-1].Zp = float(target_row['Zp'])
                                    beams[item[1]-1].F = float(target_row['F'])
                                    index = 0 #断面更新したらもう一度リスタート
                                    break
                        else:  # 1ランク上げたときに梁リストの上限を超える場合
                            print("requirement value is over upper limit of beam_list.")
                            i.I = "Error"  # 断面諸元の更新
                            i.H = "Error"
                            i.B = "Error"
                            i.t1 = "Error"
                            i.t2 = "Error"
                            i.Z = "Error"
                            i.Zp = "Error"
                            i.F = "Error"
                            frag =1
                            break

                        temp += 1
                if frag == 1:
                    break #もしエラーならwhileループを抜ける

            else:
                index += 1

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
    #板厚の設定
    for i in columns:
        if i.H != "Error":#柱の最低断面が決められている場合のみ板厚の更新を実施
            i.tc1 = (0.75*(i.MLx+i.MLy)*10**6/i.H**2/(i.F/1.5)+i.NL*1000/(4*i.H)/(i.F/1.5*0.9))*1.1
            i.tc2x = (0.75*i.MSx*10**6/i.H**2/i.F+i.NL*1000/(4*i.H)/(i.F*0.9))*1.1
            i.tc2y = (0.75*i.MSy*10**6/i.H**2/i.F+i.NL*1000/(4*i.H)/(i.F*0.9))*1.1
            i.tc = max(i.tc1,i.tc2x,i.tc2y)

    #必要板厚に基づく板厚の更新
            i.t  = math.ceil(i.tc)#小数第一位で切り上げ

    #断面諸元の再計算（更新した板厚で実施）
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


