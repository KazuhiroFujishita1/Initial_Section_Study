import pandas as pd
import numpy as np
import math


#分担モーメント、到達モーメントの計算
def calc_moment(FEM_sum,member_no_each_node,myu,member_no_x,member_i_x,member_j_x):
    D1 = [];
    C1 = [];
    C1_sum = np.zeros(int((len(node_no))))
    for i in range(len(member_no_x)):
        temp_i = 0;temp_j = 0
        for j in range(len(node_no)):#i端の算定
            if member_i_x[i] == node_no[j]:
                for k in range(len(member_no_each_node[j])):
                    if member_no_x[i] == member_no_each_node[j][k]:
                        temp_i=float(myu[j][k])
            if member_j_x[i] == node_no[j]:#j端の算定
                for k in range(len(member_no_each_node[j])):
                    if member_no_x[i] == member_no_each_node[j][k]:
                        temp_j=float(myu[j][k])
        D1.append([-FEM_sum[member_i_x[i]-1] * temp_i,-FEM_sum[member_j_x[i]-1]  * temp_j])
        C1.append([-FEM_sum[member_j_x[i]-1] * temp_j/2, -FEM_sum[member_i_x[i]-1] * temp_i/2])
        C1_sum[member_i_x[i]-1]+=-FEM_sum[member_j_x[i]-1] * temp_j/2
        C1_sum[member_j_x[i]-1]+=-FEM_sum[member_i_x[i]-1] * temp_i/2

    return D1,C1,C1_sum


#固定モーメント法による長期荷重の算定(鹿島様受領Excel（固定モーメント法）の通り）
# #各節点に接続する梁の固定端モーメントの算定
#それぞれの節点に接続する柱梁番号をリストとして整理、モーメント分担率の算定
def fixed_moment_method(beam_no_x,beam_i_x,beam_j_x,beam_stiff_x,column_stiff,member_i_x,
                        member_j_x,member_load_i_x,member_load_j_x,member_no_x,beam_category_x):
    beam_no_each_node=[];column_no_each_node=[];member_no_each_node=[]
    beam_no_each_node2=[];member_no_each_node2=[]
    node_member_stiff=[];
    for i in node_no:
        temp = [];member_stiff_temp=[];temp4=[]
        for j in range(len(beam_no_x)):
            if i == beam_i_x[j] or i == beam_j_x[j] :
                if beam_category_x[j] != "BB":
                    temp.append(beam_no_x[j])
                    member_stiff_temp.append(beam_stiff_x[j])
                temp4.append(beam_no_x[j])
        beam_no_each_node.append(temp)
        beam_no_each_node2.append(temp4)#D値法計算用のリスト（基礎梁含む）
        temp2 = [];temp3=[]
        for j in range(len(column_no)):
            if i == column_i[j] or i == column_j[j] :
                temp3.append(column_no[j])
                temp2.append(column_no[j]+len(beam_no))
                member_stiff_temp.append(column_stiff[j])
        column_no_each_node.append(temp3)
        member_no_each_node.append(temp+temp2)#全部材を通し番号で整理
        member_no_each_node2.append(temp4+temp2)#全部材を通し番号で整理（基礎梁含む）
        node_member_stiff.append(member_stiff_temp)

#各節点ごとに部材ごとのモーメント分担率の算定
    myu=[];FEM_sum=np.zeros(int((len(node_no))))
    for i in range(len(node_no)):
        myu_temp=[]

    #モーメント分担率の算定
        if len(node_member_stiff[i]) > 1:
            for j in range(len(node_member_stiff[i])):
                myu_temp.append(node_member_stiff[i][j]/sum(node_member_stiff[i]))
        elif len(node_member_stiff[i]) == 1:
            myu_temp.append(1)
        myu.append(myu_temp)

#各節点の梁の固定端モーメントの算定（1回目）
    FEM1 = []
    for i in range(len(member_no_x)):
        FEM_sum[member_i_x[i]-1]+=-member_load_i_x[i]
        FEM_sum[member_j_x[i]-1]+=member_load_j_x[i]
        FEM1.append([-member_load_i_x[i],member_load_j_x[i]])

#各部材ごとに梁の分担モーメント、到達モーメントの算定（1回目）
    D1,C1,C1_sum = calc_moment(FEM_sum,member_no_each_node,myu,member_no_x,member_i_x,member_j_x)

#各部材ごとに梁の分担モーメントの算定（2回目）
    D2,C2,C2_sum = calc_moment(C1_sum,member_no_each_node,myu,member_no_x,member_i_x,member_j_x)

#各部材ごとにモーメントの和、部材長の算定
    moment_member=[];member_length=[]
    for i in range(len(member_no_x)):
        member_length.append(np.sqrt((node_x[member_i_x[i]-1]-node_x[member_j_x[i]-1])**2#各部材の部材長算定
                                     +(node_y[member_i_x[i]-1]-node_y[member_j_x[i]-1])**2
                                     +(node_z[member_i_x[i]-1]-node_z[member_j_x[i]-1])**2))
        moment_member.append(np.array(FEM1[i])+np.array(D1[i])+np.array(C1[i])+np.array(D2[i]))#固定モーメント法の解

#柱のせん断力の算定
    shear_force_column= []
    for i in column_no:
        temp = moment_member[i+len(beam_no_x)-1]
        shear_force_column.append([abs(temp[0]+temp[1])/member_length[i+len(beam_no_x)-1],
                                   abs(temp[0]+temp[1])/member_length[i+len(beam_no_x)-1]])
#梁のせん断力の算定
    shear_force_beam = [];Q0=[]

    for i in range(len(beam_no_x)):
        temp = moment_member[i]
        Q0.append(6*member_load_i_x[i]/member_length[i])#分布荷重を想定した単純梁を仮定
        shear_force_beam.append([Q0[i]-(temp[0]+temp[1])/member_length[i],
                                 Q0[i]+(temp[0]+temp[1])/member_length[i]])

    shear_member = shear_force_beam + shear_force_column

    return moment_member, shear_member, member_no_each_node2


#各柱の反曲点高比の算定
def calc_shear_slope(column_story,kk_temp,alpha1,alpha2,alpha3):

#探索用パラメータの算定
    if kk_temp < 0.95:#探索用の剛比算定
        kk_temp = round(kk_temp,1)
    elif kk_temp >= 0.95 and kk_temp < 5:
        kk_temp = int(round(kk_temp,0))
    elif kk_temp >= 5:
        kk_temp = 5

    if alpha1 < 0.4:#探索用のα1算定
        alpha1 = 0.4
    elif alpha1 <= 0.9 and alpha1 >= 0.4:
        alpha1 = round(alpha1,1)
    elif alpha1 > 0.9:
        alpha1 = 0.9

    if alpha2 < 0.4:#探索用のα2算定
        alpha2 = 0.4
    elif alpha2 <= 2 and alpha2 >= 0.4:
        alpha2 = round(math.ceil(alpha2 / 0.2) * 0.2,1)
    elif alpha2 > 2:
        alpha2 = 2.0

    if alpha3 < 0.4:  # 探索用のα3算定
        alpha3 = 0.4
    elif alpha3 <= 2 and alpha3 >= 0.4:
        alpha3 = round(math.ceil(alpha3 / 0.2) * 0.2,1)
    elif alpha3 > 2:
        alpha3 = 2.0

#y0の算定
    if len(story_height) < 12:#12F以下の場合
        target_row = y0_calc[(y0_calc['story1'] == len(story_height)) & (y0_calc['story2'] == column_story)]
        y0 = list(target_row[str(kk_temp)])[0]
    else:#12F以上の場合（未検証）
        if len(story_height) - column_story+1 <= 8:
            target_row = y0_calc[(y0_calc['story1'] == 12) & (y0_calc['story2'] == len(story_height) - column_story+1)]
        elif column_story <= 4:
            target_row = y0_calc[(y0_calc['story1'] == 12) & (y0_calc['story2'] == column_story)]
        else:
            target_row = y0_calc[(y0_calc['story1'] == 12) & (y0_calc['story2'] == "")]

#y1の算定
    target_row = y1_calc[y1_calc['alpha1'] == alpha1]
    y1 = list(target_row[str(kk_temp)])[0]

#y2の算定
    target_row = y2_calc[y2_calc['alpha2'] == alpha2]
    y2 = list(target_row[str(kk_temp)])[0]

#y3の算定
    target_row = y2_calc[y2_calc['alpha3'] == alpha3]
    y3 = list(target_row[str(kk_temp)])[0]

#反曲点高比の算定
    yy = y0 + y1 + y2 + y3

    return yy


#D値法による地震時荷重の算定
def D_method(member_no_each_node_x,story_shear_x,beam_no_x,beam_i_x,beam_j_x,beam_stiff_x):
    kk=[];a=[];D=[];D_sum=np.zeros(int((len(story_shear_x))))
    alpha1 = [];alpha2=[]; alpha3=[]; yy=[]
    for i in column_no:
        temp = member_no_each_node_x[column_i[i-1]-1]#i端部材no
        temp2 = member_no_each_node_x[column_j[i-1]-1]#j端部材no

        temp_stiff=[];temp_stiff_i=[];temp_stiff_j=[]
        flag = 0
        if (boundary[member_i[i - len(beam_no) - 1] - 1] == "pin" or
                boundary[member_j[i + len(beam_no) - 1] - 1] == "pin"):
            flag = 1  # 柱のi,j側節点にピン支点が含まれる場合
        elif (boundary[member_i[i - len(beam_no) - 1] - 1] == "fix" or
                boundary[member_j[i + len(beam_no) - 1] - 1] == "fix"):
            flag = 2  # 柱のi,j側節点に固定支点が含まれる場合

        for j in temp:
            if j <= len(beam_no):
                temp_stiff.append(member_stiff[j-1])
                temp_stiff_i.append(member_stiff[j-1])
        for j in temp2:
            if j <= len(beam_no):
                temp_stiff.append(member_stiff[j-1])
                temp_stiff_j.append(member_stiff[j-1])

        if flag == 1:
            kk_temp = sum(temp_stiff) / (member_stiff[i + len(beam_no) - 1])
            kk.append(kk_temp)
            a.append((0.5*kk_temp)/(1+2*kk_temp))
            D.append(member_stiff[i + len(beam_no) - 1]*(0.5*kk_temp)/(1+2*kk_temp))#柱脚ピンの場合
            alpha1.append(0) #最下層ではα1=0
        elif flag ==2:
            kk_temp = sum(temp_stiff) / (member_stiff[i + len(beam_no) - 1])
            kk.append(kk_temp)
            a.append((0.5+kk_temp)/(2+kk_temp))#柱脚固定の場合
            D.append(member_stiff[i + len(beam_no) - 1] * (0.5+kk_temp)/(2+kk_temp))
            alpha1.append(0) #最下層ではα1=0
        else:
            kk_temp = sum(temp_stiff)/(2*member_stiff[i+len(beam_no)-1])
            kk.append(kk_temp)
            a.append(kk_temp/(2+kk_temp))#一般階の場合
            D.append(member_stiff[i + len(beam_no) - 1] * kk_temp/(2+kk_temp))

        #alpha1の算定
            if node_z[column_i[i-1]-1] > node_z[column_j[i-1]-1]:#i端側がj端側よりも高い場合
                if sum(temp_stiff_i) <= sum(temp_stiff_j):#上梁の剛比が大きい場合
                    alpha1.append(sum(temp_stiff_i)/sum(temp_stiff_j))
                else:#下梁の剛比が大きい場合
                    alpha1.append(-sum(temp_stiff_j)/sum(temp_stiff_i))
            else:#i端側がj端側よりも低い場合
                if sum(temp_stiff_i) > sum(temp_stiff_j):#上梁の剛比が大きい場合
                    alpha1.append(sum(temp_stiff_j)/sum(temp_stiff_i))
                else:#下梁の剛比が大きい場合
                    alpha1.append(-sum(temp_stiff_i)/sum(temp_stiff_j))
        #alpha2の算定
        if max(column_story)-column_story[i-1] == max(column_story)-1:
            alpha2.append(0)#最上層の時はalpha2=0
        else:#
            alpha2.append(story_height[max(column_story)-column_story[i-1]]/story_height[max(column_story)-column_story[i-1]+1])
        #alpha3の算定
        if max(column_story)-column_story[i-1] == 0:
            alpha3.append(0)#最下層の時はalpha3=0
        else:#
            alpha3.append(story_height[max(column_story)-column_story[i-1]]/story_height[max(column_story)-column_story[i-1]-1])

        #各層のD値の和の算定
        D_sum[column_story[i-1]-1] += D[i-1]

    #各柱の反曲点高比の算定
        yy_temp = calc_shear_slope(column_story[i-1],kk_temp,alpha1[i-1],alpha2[i-1],alpha3[i-1])
        yy.append(yy_temp)

    #柱のせん断力、曲げモーメントを算定
    shear_column =[];moment_column=[]
    tt = 0
    for i in column_no:
        shear_column.append(D[i-1]/D_sum[column_story[i-1]-1]*story_shear_x[max(column_story)-column_story[i-1]])
        if node_z[column_i[i - 1] - 1] > node_z[column_j[i - 1] - 1]:  # i端側がj端側よりも高い場合
            moment_column.append([shear_column[tt] * story_height[max(column_story) - column_story[i - 1]] * (1-yy[i - 1]),
                                  shear_column[tt]*story_height[max(column_story)-column_story[i-1]]*yy[i-1]])
        else:
            moment_column.append([shear_column[tt] * story_height[max(column_story) - column_story[i - 1]] * yy[i - 1],
                                  shear_column[tt]*story_height[max(column_story)-column_story[i-1]]*(1-yy[i-1])])
        tt += 1

    #梁の曲げモーメントの算定
    node_moment = [];stiff_c=[]
    for i in node_no:#各節点においてとりつく上下柱の曲げモーメントを集計
        temp =0
        for j in range(len(column_no)):
            if i == column_i[j-1]:
                temp += moment_column[j-1][0]
            if i == column_j[j - 1]:
                temp += moment_column[j-1][1]
        node_moment.append(temp)

        # 各節点にとりつく梁の剛性和の算定
        temp=0
        for j in range(len(beam_no_x)):
            if beam_i_x[j-1] == i or beam_j_x[j-1] == i:
                temp += beam_stiff_x[j-1]
        stiff_c.append(temp)

    #各梁の剛比に応じ柱の曲げモーメントを分配
    moment_beam=[];shear_beam=[]
    for i in range(len(beam_no_x)):
        temp_i = 0;temp_j = 0
        for j in range(len(node_no)):#i端の算定
            if beam_i_x[i] == node_no[j]:
                for k in range(len(member_no_each_node_x[j])):
                    if beam_no_x[i] == member_no_each_node_x[j][k]:
                        temp_i=float(beam_stiff_x[i]/stiff_c[j]*node_moment[j])
            if beam_j_x[i] == node_no[j]:#j端の算定
                for k in range(len(member_no_each_node_x[j])):
                    if beam_no_x[i] == member_no_each_node_x[j][k]:
                        temp_j=float(beam_stiff_x[i]/stiff_c[j]*node_moment[j])
        moment_beam.append([temp_i,temp_j])
        shear_beam.append((moment_beam[i][0]+moment_beam[i][1])/np.sqrt((node_x[beam_i_x[i]-1]-node_x[beam_j_x[i]-1])**2#各部材のせん断力算定
                                     +(node_y[beam_i_x[i]-1]-node_y[beam_j_x[i]-1])**2
                                     +(node_z[beam_i_x[i]-1]-node_z[beam_j_x[i]-1])**2))

    moment_member = moment_beam + moment_column
    shear_member = shear_beam + shear_column

    #各柱の軸力算定（inputファイルにおいて柱リストは上の層のものから順に記載すること）
    temp_axial_column = [];axial_column=[]
    for i in column_no:
        #各柱にとりつく梁のせん断力から想定される軸力を算定
        if node_z[column_i[i - 1] - 1] > node_z[column_j[i - 1] - 1]:  # i端側がj端側よりも高い場合
            temp = member_no_each_node_x[column_i[i-1]-1]#i端部材no
        else:
            temp = member_no_each_node_x[column_j[i-1]-1]#j端部材no

        temp2 = []#接続梁の部材番号のみを抽出
        for j in temp:
            if j <= len(beam_no):
                temp2.append(j)
        #梁のせん断力の差分が軸力となる
        if len(temp2) == 1:
            temp_axial_column.append(shear_member[beam_no_x.index(temp2[0])])
        elif len(temp2) == 2:
            temp_axial_column.append(abs(shear_member[beam_no_x.index(temp2[0])]-shear_member[beam_no_x.index(temp2[1])]))

    for i in column_no:
        #上に接続する柱の軸力を足す
        if node_z[column_i[i - 1] - 1] > node_z[column_j[i - 1] - 1]:  # i端側がj端側よりも高い場合
            temp = member_no_each_node_x[column_i[i-1]-1]#i端部材no
        else:
            temp = member_no_each_node_x[column_j[i-1]-1]#j端部材no
        temp2 = []#接続柱の部材番号のみを抽出

        frag =0
        for j in temp:
            if j > len(beam_no) and int(j) != int(i+len(beam_no)):#自分以外の柱がある場合その柱の軸力を足す
                axial_column.append(temp_axial_column[i-1]+temp_axial_column[j-len(beam_no)-1])
                temp_axial_column[i-1]=temp_axial_column[i-1]+temp_axial_column[j-len(beam_no)-1]#temp自身も更新
                frag = 1
        if frag == 0:
            axial_column.append(temp_axial_column[i-1])

    axial_member = [0]*len(beam_no_x) + axial_column #柱の軸力は0

    return moment_member,shear_member,axial_member


## メイン関数 ##
if __name__ == "__main__":
    df1 = pd.read_excel("input_model.xlsx", sheet_name="Node", header=0)
    df2 = pd.read_excel("input_model.xlsx", sheet_name="Beam", header=0)
    df3 = pd.read_excel("input_model.xlsx", sheet_name="Column", header=0)
    df4 = pd.read_excel("input_model.xlsx", sheet_name="Story_shear", header=0)

# 節点座標、柱、梁リストに関してDataFrameから辞書を生成
    data_dict1 = df1.to_dict(orient='records')
    data_dict2 = df2.to_dict(orient='records')
    data_dict3 = df3.to_dict(orient='records')

# 反曲点高比計算用データを読み込み
    y0_calc = pd.read_csv("y0_table.csv", header=0)
    y1_calc = pd.read_csv("y1_table.csv", header=0)
    y2_calc = pd.read_csv("y2_table.csv", header=0)

# 節点の情報を収集
    node_no = list(df1['No'])
    node_x = list(df1['x'])
    node_y = list(df1['y'])
    node_z = list(df1['z'])
    boundary = list(df1['boundary'])

# 梁の情報を収集
    member_no = [];#部材の通し番号もつくる
    beam_no = list(df2['No.'])
    beam_i = list(df2['i_point'])
    beam_j = list(df2['j_point'])
    beam_stiff = list(df2['stiffness_ratio'])
    beam_load_i = list(df2['C_i'])
    beam_load_j = list(df2['C_j'])
    beam_category = list(df2['category'])

# 柱の情報を収集
    column_no = list(df3['No.'])
    column_i = list(df3['i_point'])
    column_j = list(df3['j_point'])
    column_stiff_x = list(df3['stiffness_ratio_x'])
    column_stiff_y = list(df3['stiffness_ratio_y'])
    column_story = list(df3['story'])

# 層に関する情報を収集
    story_height = list(df4['Story_height'])
    story_shear_x = list(df4['Shear_force_X'])
    story_shear_y = list(df4['Shear_force_Y'])

#全部材の情報を定義
    member_no = list(df2['No.']) + list(df3['No.']+len(beam_no))
    member_i = list(df2['i_point']) + list(df3['i_point'])
    member_j = list(df2['j_point']) + list(df3['j_point'])
    member_load_i = list(df2['C_i'])+list([0]*len(column_no))
    member_load_j = list(df2['C_j'])+list([0]*len(column_no))

    member_stiff = beam_stiff + column_stiff_x

# 梁の方向を分類（まずは直交座標を仮定）
    beam_no_x=[];beam_no_y=[];beam_i_x=[];beam_i_y=[]
    beam_j_x=[];beam_j_y=[];beam_stiff_x=[];beam_stiff_y=[];
    beam_load_i_x=[];beam_load_j_x=[];beam_load_i_y=[];beam_load_j_y=[]
    C_moment_x = []; C_moment_y = [];beam_category_x=[];beam_category_y=[]
    for i in range(len(beam_no)):
        coordinate_i = next(item for item in data_dict1 if item['No'] == int(beam_i[i]))
        coordinate_j = next(item for item in data_dict1 if item['No'] == int(beam_j[i]))

        x_value_i = coordinate_i['x']
        x_value_j = coordinate_j['x']
        y_value_i = coordinate_j['y']
        y_value_j = coordinate_j['y']

        if x_value_i == x_value_j:
            beam_no_y.append(beam_no[i])
            beam_i_y.append(beam_i[i])
            beam_j_y.append(beam_j[i])
            beam_stiff_y.append(beam_stiff[i])
            beam_load_i_y.append(beam_load_i[i])
            beam_load_j_y.append(beam_load_j[i])
            C_moment_y.append([-beam_load_i[i],beam_load_j[i]])
            beam_category_y.append(beam_category[i])

            member_no_y=beam_no_y +  list(df3['No.']+len(beam_no))
            member_i_y = beam_i_y + column_i
            member_j_y = beam_j_y + column_j
            member_load_i_y = beam_load_i_y +list([0]*len(column_no))
            member_load_j_y = beam_load_j_y +list([0]*len(column_no))

            member_stiff_y = beam_stiff_y + column_stiff_y

        elif y_value_i == y_value_j:
            beam_no_x.append(beam_no[i])
            beam_i_x.append(beam_i[i])
            beam_j_x.append(beam_j[i])
            beam_stiff_x.append(beam_stiff[i])
            beam_load_i_x.append(beam_load_i[i])
            beam_load_j_x.append(beam_load_j[i])
            C_moment_x.append([-beam_load_i[i],beam_load_j[i]])
            beam_category_x.append(beam_category[i])

            member_no_x = beam_no_x +  list(df3['No.']+len(beam_no))
            member_i_x = beam_i_x + column_i
            member_j_x = beam_j_x + column_j
            member_load_i_x = beam_load_i_x +list([0]*len(column_no))
            member_load_j_x = beam_load_j_x +list([0]*len(column_no))

            member_stiff_x = beam_stiff_x + column_stiff_x

#固定モーメント法
    #X方向
    moment_x_long, shear_x_long, member_no_each_node_x = fixed_moment_method(beam_no_x,beam_i_x,beam_j_x,beam_stiff_x,column_stiff_x,
                                                                   member_i_x,member_j_x,member_load_i_x,member_load_j_x,member_no_x,beam_category_x)

    #Y方向
    moment_y_long, shear_y_long, member_no_each_node_y = fixed_moment_method(beam_no_y,beam_i_y,beam_j_y,beam_stiff_y,column_stiff_y,
                                                                   member_i_y,member_j_y,member_load_i_y,member_load_j_y,member_no_y,beam_category_y)

#D値法
    #X方向
    moment_x_short, shear_x_short, axial_x_short = D_method(member_no_each_node_x,story_shear_x,beam_no_x,beam_i_x,beam_j_x,beam_stiff_x)
    #Y方向
    moment_y_short, shear_y_short, axial_y_short = D_method(member_no_each_node_y,story_shear_y,beam_no_y,beam_i_y,beam_j_y,beam_stiff_y)
