from main import *
from member_class import *
import math

#分担モーメント、到達モーメントの計算
def calc_moment(FEM_sum,member_no_each_node,myu,node,member):
    D1 = [];
    C1 = [];
    C1_sum = np.zeros(int((len(node.no))))

    for i in range(len(member.no)):
        temp_i = 0;temp_j = 0
        for j in range(len(node.no)):#i端の算定
            if member.i[i] == node.no[j]:
                for k in range(len(member_no_each_node[j])):
                    if member.no[i] == member_no_each_node[j][k]:
                        temp_i=float(myu[j][k])
            if member.j[i] == node.no[j]:#j端の算定
                for k in range(len(member_no_each_node[j])):
                    if member.no[i] == member_no_each_node[j][k]:
                        temp_j=float(myu[j][k])
        D1.append([-FEM_sum[member.i[i]-1] * temp_i,-FEM_sum[member.j[i]-1]  * temp_j])
        C1.append([-FEM_sum[member.j[i]-1] * temp_j/2, -FEM_sum[member.i[i]-1] * temp_i/2])
        C1_sum[member.i[i]-1]+=-FEM_sum[member.j[i]-1] * temp_j/2
        C1_sum[member.j[i]-1]+=-FEM_sum[member.i[i]-1] * temp_i/2

    return D1,C1,C1_sum


#固定モーメント法による長期荷重の算定(鹿島様受領Excel（固定モーメント法）の通り）
# #各節点に接続する梁の固定端モーメントの算定
#それぞれの節点に接続する柱梁番号をリストとして整理、モーメント分担率の算定
def fixed_moment_method(beam_no,beam,column,member,EE):
    beam_no_each_node=[];column_no_each_node=[];member_no_each_node=[]
    beam_no_each_node2=[];member_no_each_node2=[]
    node_member_stiff=[];

    node = Node()

    for i in node.no:
        temp = [];member_stiff_temp=[];temp4=[]
        for j in range(len(beam.no)):
            if i == beam.i[j] or i == beam.j[j] :
                if beam.category[j] != "BB":
                    temp.append(beam.no[j])
                    member_stiff_temp.append(beam.stiff_ratio[j])
                temp4.append(beam.no[j])
        beam_no_each_node.append(temp)
        beam_no_each_node2.append(temp4)#D値法計算用のリスト（基礎梁含む）
        temp2 = [];temp3=[]
        for j in range(len(column.no)):
            if i == column.i[j] or i == column.j[j] :
                temp3.append(column.no[j])
                temp2.append(column.no[j]+len(beam_no))
                member_stiff_temp.append(column.stiff_ratio[j])
        column_no_each_node.append(temp3)
        member_no_each_node.append(temp+temp2)#全部材を通し番号で整理
        member_no_each_node2.append(temp4+temp2)#全部材を通し番号で整理（基礎梁含む）
        node_member_stiff.append(member_stiff_temp)

#各節点ごとに部材ごとのモーメント分担率の算定
    myu=[];FEM_sum=np.zeros(int((len(node.no))))
    for i in range(len(node.no)):
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
    for i in range(len(member.no)):
        FEM_sum[member.i[i]-1]+=-member.Ci[i]
        FEM_sum[member.j[i]-1]+=member.Cj[i]
        FEM1.append([-member.Ci[i],member.Cj[i]])

#各部材ごとに梁の分担モーメント、到達モーメントの算定（1回目）
    D1,C1,C1_sum = calc_moment(FEM_sum,member_no_each_node,myu,node,member)

#各部材ごとに梁の分担モーメントの算定（2回目）
    D2,C2,C2_sum = calc_moment(C1_sum,member_no_each_node,myu,node,member)


#各部材ごとにモーメントの和、部材長の算定
    moment_member=[]
    for i in range(len(member.no)):
        moment_member.append(np.array(FEM1[i])+np.array(D1[i])+np.array(C1[i])+np.array(D2[i]))#固定モーメント法の解

#各部材ごとに大梁のたわみ算定
    center_moment=[];beam_disp = []
    for i in range(len(beam.no)):
        center_moment.append(-beam.dist_load[i]*member.length[i]**2/8
                             -np.average([abs(moment_member[i][0]),abs(moment_member[i][1])]))#固定端モーメントを考慮した梁中央の曲げモーメントM0
        beam_disp.append(5*center_moment[i]/(48*EE*beam.I[i])*member.length[i]**2
                     -sum(moment_member[i])/(16*EE*beam.I[i])*member.length[i]**2)#梁中央のたわみ（未検証）

#柱のせん断力の算定
    shear_force_column= []
    for i in column.no:
        temp = moment_member[i+len(beam.no)-1]
        shear_force_column.append([abs(temp[0]+temp[1])/member.length[i+len(beam.no)-1],
                                   abs(temp[0]+temp[1])/member.length[i+len(beam.no)-1]])
#梁のせん断力の算定
    shear_force_beam = [];Q0=[]

    for i in range(len(beam.no)):
        temp = moment_member[i]
        Q0.append(6*member.Ci[i]/member.length[i])#分布荷重を想定した単純梁を仮定
        shear_force_beam.append([Q0[i]-(temp[0]+temp[1])/member.length[i],
                                 Q0[i]+(temp[0]+temp[1])/member.length[i]])

    shear_member = shear_force_beam + shear_force_column

    return moment_member, shear_member, member_no_each_node2


#各柱の反曲点高比の算定
def calc_shear_slope(column_story,kk_temp,alpha1,alpha2,alpha3,maximum_story):

# 反曲点高比計算用データを読み込み
    y0_calc = pd.read_csv("y0_table.csv", header=0)
    y1_calc = pd.read_csv("y1_table.csv", header=0)
    y2_calc = pd.read_csv("y2_table.csv", header=0)

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
    if maximum_story < 12:#12F以下の場合
        target_row = y0_calc[(y0_calc['story1'] == maximum_story) & (y0_calc['story2'] == column_story)]
        y0 = list(target_row[str(kk_temp)])[0]
    else:#12F以上の場合（未検証）
        if maximum_story - column_story+1 <= 8:
            target_row = y0_calc[(y0_calc['story1'] == 12) & (y0_calc['story2'] == maximum_story - column_story+1)]
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
def D_method(member_no_each_node_x,layer,beam,column,member):
    kk=[];a=[];D=[];D_sum=np.zeros(int((len(layer.shear_force))))
    alpha1 = [];alpha2=[]; alpha3=[]; yy=[]

    node = Node()

    for i in column.no:
        temp = member_no_each_node_x[column.i[i-1]-1]#i端部材no
        temp2 = member_no_each_node_x[column.j[i-1]-1]#j端部材no

        boundary_i = node.call_boundary(member.i_all[i - len(beam.no_all) - 1] - 1)
        boundary_j = node.call_boundary(member.j_all[i - len(beam.no_all) - 1] - 1)

        temp_stiff=[];temp_stiff_i=[];temp_stiff_j=[]
        flag = 0
        if (boundary_i == "pin" or
                boundary_j == "pin"):
            flag = 1  # 柱のi,j側節点にピン支点が含まれる場合
        elif (boundary_i == "fix" or
                boundary_j == "fix"):
            flag = 2  # 柱のi,j側節点に固定支点が含まれる場合

        for j in temp:
            if j <= len(beam.no_all):
                temp_stiff.append(member.stiff_ratio[j-1])
                temp_stiff_i.append(member.stiff_ratio[j-1])
        for j in temp2:
            if j <= len(beam.no_all):
                temp_stiff.append(member.stiff_ratio[j-1])
                temp_stiff_j.append(member.stiff_ratio[j-1])

        if flag == 1:
            kk_temp = sum(temp_stiff) / (member.stiff_ratio[i + len(beam.no_all) - 1])
            kk.append(kk_temp)
            a.append((0.5*kk_temp)/(1+2*kk_temp))
            D.append(member.stiff_ratio[i + len(beam.no_all) - 1]*(0.5*kk_temp)/(1+2*kk_temp))#柱脚ピンの場合
            alpha1.append(0) #最下層ではα1=0
        elif flag ==2:
            kk_temp = sum(temp_stiff) / (member.stiff_ratio[i + len(beam.no_all) - 1])
            kk.append(kk_temp)
            a.append((0.5+kk_temp)/(2+kk_temp))#柱脚固定の場合
            D.append(member.stiff_ratio[i + len(beam.no_all) - 1] * (0.5+kk_temp)/(2+kk_temp))
            alpha1.append(0) #最下層ではα1=0
        else:
            kk_temp = sum(temp_stiff)/(2*member.stiff_ratio[i+len(beam.no_all)-1])
            kk.append(kk_temp)
            a.append(kk_temp/(2+kk_temp))#一般階の場合
            D.append(member.stiff_ratio[i + len(beam.no_all) - 1] * kk_temp/(2+kk_temp))

        #alpha1の算定
            if node.z[column.i[i-1]-1] > node.z[column.j[i-1]-1]:#i端側がj端側よりも高い場合
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
        if max(column.story)-column.story[i-1] == max(column.story)-1:
            alpha2.append(0)#最上層の時はalpha2=0
        else:#
            alpha2.append(layer.height[max(column.story)-column.story[i-1]]/layer.height[max(column.story)-column.story[i-1]+1])
        #alpha3の算定
        if max(column.story)-column.story[i-1] == 0:
            alpha3.append(0)#最下層の時はalpha3=0
        else:#
            alpha3.append(layer.height[max(column.story)-column.story[i-1]]/layer.height[max(column.story)-column.story[i-1]-1])

        #各層のD値の和の算定
        D_sum[column.story[i-1]-1] += D[i-1]

    #各柱の反曲点高比の算定
        maximum_story = len(layer.height)
        yy_temp = calc_shear_slope(column.story[i-1],kk_temp,alpha1[i-1],alpha2[i-1],alpha3[i-1],maximum_story)
        yy.append(yy_temp)

    #柱のせん断力、曲げモーメントを算定
    shear_column =[];moment_column=[]
    tt = 0
    for i in column.no:
        shear_column.append(D[i-1]/D_sum[column.story[i-1]-1]*layer.shear_force[max(column.story)-column.story[i-1]])
        if node.z[column.i[i - 1] - 1] > node.z[column.j[i - 1] - 1]:  # i端側がj端側よりも高い場合
            moment_column.append([shear_column[tt] * layer.height[max(column.story) - column.story[i - 1]] * (1-yy[i - 1]),
                                  shear_column[tt]*layer.height[max(column.story)-column.story[i-1]]*yy[i-1]])
        else:
            moment_column.append([shear_column[tt] * layer.height[max(column.story) - column.story[i - 1]] * yy[i - 1],
                                  shear_column[tt]*layer.height[max(column.story)-column.story[i-1]]*(1-yy[i-1])])
        tt += 1

    #梁の曲げモーメントの算定
    node_moment = [];stiff_c=[]
    for i in node.no:#各節点においてとりつく上下柱の曲げモーメントを集計
        temp =0
        for j in range(len(column.no)):
            if i == column.i[j-1]:
                temp += moment_column[j-1][0]
            if i == column.j[j - 1]:
                temp += moment_column[j-1][1]
        node_moment.append(temp)

        # 各節点にとりつく梁の剛性和の算定
        temp=0
        for j in range(len(beam.no)):
            if beam.i[j-1] == i or beam.j[j-1] == i:
                temp += beam.stiff_ratio[j-1]
        stiff_c.append(temp)

    #各梁の剛比に応じ柱の曲げモーメントを分配
    moment_beam=[];shear_beam=[]
    for i in range(len(beam.no)):
        temp_i = 0;temp_j = 0
        for j in range(len(node.no)):#i端の算定
            if beam.i[i] == node.no[j]:
                for k in range(len(member_no_each_node_x[j])):
                    if beam.no[i] == member_no_each_node_x[j][k]:
                        temp_i=float(beam.stiff_ratio[i]/stiff_c[j]*node_moment[j])
            if beam.j[i] == node.no[j]:#j端の算定
                for k in range(len(member_no_each_node_x[j])):
                    if beam.no[i] == member_no_each_node_x[j][k]:
                        temp_j=float(beam.stiff_ratio[i]/stiff_c[j]*node_moment[j])
        moment_beam.append([temp_i,temp_j])

        shear_beam.append((moment_beam[i][0]+moment_beam[i][1])/beam.length[i])

    moment_member = moment_beam + moment_column
    shear_member = shear_beam + shear_column

    #各柱の軸力算定（inputファイルにおいて柱リストは上の層のものから順に記載すること）
    temp_axial_column = [];axial_column=[]
    for i in column.no:
        column_x1,column_y1,column_z1 = node.call_node(column.i[i-1]-1)
        column_x2,column_y2,column_z2 = node.call_node(column.j[i-1]-1)
        #各柱にとりつく梁のせん断力から想定される軸力を算定
        if column_z1 > column_z2:  # i端側がj端側よりも高い場合
            temp = member_no_each_node_x[column.i[i-1]-1]#i端部材no
        else:
            temp = member_no_each_node_x[column.j[i-1]-1]#j端部材no

        temp2 = []#接続梁の部材番号のみを抽出
        for j in temp:
            if j <= len(beam.no_all):
                temp2.append(j)
        #梁のせん断力の差分が軸力となる
        if len(temp2) == 1:
            temp_axial_column.append(shear_member[beam.no.index(temp2[0])])
        elif len(temp2) == 2:
            temp_axial_column.append(abs(shear_member[beam.no.index(temp2[0])]-shear_member[beam.no.index(temp2[1])]))

    for i in column.no:
        column_x1,column_y1,column_z1 = node.call_node(column.i[i-1]-1)
        column_x2,column_y2,column_z2 = node.call_node(column.j[i-1]-1)
        #上に接続する柱の軸力を足す
        if column_z1 > column_z2:  # i端側がj端側よりも高い場合
            temp = member_no_each_node_x[column.i[i-1]-1]#i端部材no
        else:
            temp = member_no_each_node_x[column.j[i-1]-1]#j端部材no
        temp2 = []#接続柱の部材番号のみを抽出

        frag =0
        for j in temp:
            if j > len(beam.no_all) and int(j) != int(i+len(beam.no_all)):#自分以外の柱がある場合その柱の軸力を足す
                axial_column.append(temp_axial_column[i-1]+temp_axial_column[j-len(beam.no_all)-1])
                temp_axial_column[i-1]=temp_axial_column[i-1]+temp_axial_column[j-len(beam.no_all)-1]#temp自身も更新
                frag = 1
        if frag == 0:
            axial_column.append(temp_axial_column[i-1])

    axial_member = [0]*len(beam.no) + axial_column #柱の軸力は0

    return moment_member,shear_member,axial_member
