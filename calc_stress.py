from main import *
from member_class import *
import math

#分担モーメント、到達モーメントの計算
def calc_moment(FEM_sum,member_no_each_node,myu,nodes,beams,columns,beam_no):
    D1 = [];
    C1 = [];
    C1_sum = np.zeros(len(nodes))

    for i in beam_no:
        temp_i = 0;temp_j=0
        for j in range(len(nodes)):#i端の算定
            if beams[i-1].i == nodes[j].no:
                for k in range(len(member_no_each_node[j])):
                    if beams[i-1].no == member_no_each_node[j][k]:
                        temp_i=float(myu[j][k])
            if beams[i-1].j == nodes[j].no:
                for k in range(len(member_no_each_node[j])):
                    if beams[i-1].no == member_no_each_node[j][k]:
                        temp_j = float(myu[j][k])

        D1.append([-FEM_sum[beams[i-1].i-1]*temp_i, -FEM_sum[beams[i-1].j-1]*temp_j])
        C1.append([-FEM_sum[beams[i-1].j - 1] * temp_j/2, -FEM_sum[beams[i-1].i - 1] * temp_i/2])
        C1_sum[beams[i-1].i-1]+=-FEM_sum[beams[i-1].j-1] * temp_j/2
        C1_sum[beams[i-1].j-1]+=-FEM_sum[beams[i-1].i-1] * temp_i/2

    for i in columns:
        temp_i = 0;
        temp_j = 0
        for j in range(len(nodes)):  # i端の算定
            if i.i == nodes[j].no:
                for k in range(len(member_no_each_node[j])):
                    if i.no + len(beams) == member_no_each_node[j][k]:
                        temp_i = float(myu[j][k])

            if i.j == nodes[j].no:
                for k in range(len(member_no_each_node[j])):
                    if i.no  +len(beams) == member_no_each_node[j][k]:
                        temp_j = float(myu[j][k])

        D1.append([-FEM_sum[i.i - 1] * temp_i, -FEM_sum[i.j - 1] * temp_j])
        C1.append([-FEM_sum[i.j - 1] * temp_j / 2, -FEM_sum[i.i - 1] * temp_i / 2])
        C1_sum[i.i - 1] += -FEM_sum[i.j - 1] * temp_j / 2
        C1_sum[i.j - 1] += -FEM_sum[i.i - 1] * temp_i / 2

    return D1,C1,C1_sum

#部材の接合状況を把握
def detect_connection(nodes,beams,columns):

    for i in nodes:
        #X方向の梁
        temp_x = [];temp4_x=[]
        count_x=0
        for j in beams:
            if j.direction == "X": #X方向の場合
                count_x+=1
                if i.no == j.i or i.no == j.j :
                    if j.category == "BB":#基礎梁の場合
                        temp4_x.append(j.no)
                    else:
                        temp_x.append(j.no)
                        temp4_x.append(j.no)
        i.beam_no_each_node_x = temp_x
        i.beam_no_each_node2_x = temp4_x#D値法計算用のリスト（基礎梁含む）

        temp2_x = [];temp3_x = []
        for j in columns:
            if i.no == j.i or i.no == j.j :
                temp3_x.append(j.no)
                temp2_x.append(j.no + len(beams))

        #Y方向の梁
        temp_y = [];temp4_y = []
        count_y=0
        for j in beams:
            if j.direction == "Y":  # Y方向の場合
                count_y+=1
                if i.no == j.i or i.no == j.j:
                    if j.category == "BB":#基礎梁の場合
                        temp4_y.append(j.no)
                    else:
                        temp_y.append(j.no)
                        temp4_y.append(j.no)

        i.beam_no_each_node_y = temp_y
        i.beam_no_each_node2_y = temp4_y  # D値法計算用のリスト（基礎梁含む）

        temp2_y = [];temp3_y = []
        for j in columns:
            if i.no == j.i or i.no == j.j :
                temp3_y.append(j.no)
                temp2_y.append(j.no + len(beams))

        i.column_no_each_node_x = temp3_x
        i.column_no_each_node_y = temp3_y
        i.member_no_each_node_x = temp_x+temp2_x#全部材を通し番号で整理
        i.member_no_each_node_y = temp_y+temp2_y#全部材を通し番号で整理
        i.member_no_each_node2_x = temp4_x+temp2_x#全部材を通し番号で整理（基礎梁含む）
        i.member_no_each_node2_y = temp4_y+temp2_y#全部材を通し番号で整理（基礎梁含む）

#固定モーメント法による長期荷重の算定(鹿島様受領Excel（固定モーメント法）の通り）
# #各節点に接続する梁の固定端モーメントの算定
#それぞれの節点に接続する柱梁番号をリストとして整理、モーメント分担率の算定
def fixed_moment_method(nodes,beams,columns,EE):

#各節点ごとに部材ごとのモーメント分担率の算定
    myu_x=[];FEM_sum_x=np.zeros(int((len(nodes))))
    myu_y=[];FEM_sum_y=np.zeros(int((len(nodes))))
    for i in nodes:
        myu_temp=[]

    #モーメント分担率の算定
        if len(i.node_member_stiff2_x) > 1:
            for j in i.node_member_stiff2_x:
                myu_temp.append(j/sum(i.node_member_stiff2_x))
        elif len(i.node_member_stiff2_x) == 1:
            myu_temp.append(1)
        myu_x.append(myu_temp)

        myu_temp=[]
        # モーメント分担率の算定
        if len(i.node_member_stiff2_y) > 1:
            for j in i.node_member_stiff2_y:
                myu_temp.append(j / sum(i.node_member_stiff2_y))
        elif len(i.node_member_stiff2_y) == 1:
            myu_temp.append(1)
        myu_y.append(myu_temp)

#各節点の梁の固定端モーメントの算定（1回目）
    FEM1_x = [];FEM1_y = [];beam_no_x=[];beam_no_y=[]
    for i in beams:
        if i.direction == "X":
            beam_no_x.append(i.no)
            FEM_sum_x[i.i-1]+=-i.Ci
        else:
            beam_no_y.append(i.no)
            FEM_sum_y[i.i-1]+=-i.Ci
        if i.direction == "X":
            FEM_sum_x[i.j-1]+=i.Cj
        else:
            FEM_sum_y[i.j-1]+=i.Cj

        if i.direction == "X":
            FEM1_x.append([-i.Ci,i.Cj])
        else:
            FEM1_y.append([-i.Ci,i.Cj])

#各部材ごとに梁の分担モーメント、到達モーメントの算定（1回目）

    member_no_each_node2_x=[];member_no_each_node2_y=[]
    for i in nodes:
        member_no_each_node2_x.append(i.member_no_each_node2_x)
    for i in nodes:
        member_no_each_node2_y.append(i.member_no_each_node2_y)

    D1_x,C1_x,C1_sum_x = calc_moment(FEM_sum_x,member_no_each_node2_x,myu_x,nodes,beams,columns,beam_no_x)
    D1_y,C1_y,C1_sum_y = calc_moment(FEM_sum_y,member_no_each_node2_y,myu_y,nodes,beams,columns,beam_no_y)


#各部材ごとに梁の分担モーメントの算定（2回目）
    D2_x,C2_x,C2_sum_x = calc_moment(C1_sum_x,member_no_each_node2_x,myu_x,nodes,beams,columns,beam_no_x)
    D2_y,C2_y,C2_sum_y = calc_moment(C1_sum_y,member_no_each_node2_y,myu_y,nodes,beams,columns,beam_no_y)

#各部材ごとにモーメントの和、部材長の算定(C2まで計算する）
    temp = 0
    for i in beam_no_x:
        beams[i-1].M_Lx = np.array(FEM1_x[temp])+np.array(D1_x[temp])+np.array(C1_x[temp])+np.array(D2_x[temp])+np.array(C2_x[temp])#固定モーメント法の解
        temp +=1

    for i in columns:
        i.M_Lx = np.array(D1_x[temp])+np.array(C1_x[temp])+np.array(D2_x[temp])+np.array(C2_x[temp])#固定モーメント法の解
        temp +=1

    temp = 0
    for i in beam_no_y:
        beams[i-1].M_Ly = np.array(FEM1_y[temp])+np.array(D1_y[temp])+np.array(C1_y[temp])+np.array(D2_y[temp])+np.array(C2_y[temp])#固定モーメント法の解
        temp += 1

    for i in columns:
        i.M_Ly = np.array(D1_y[temp])+np.array(C1_y[temp])+np.array(D2_y[temp])+np.array(C2_y[temp])#固定モーメント法の解
        temp += 1

#各部材ごとに大梁のたわみ算定(ダミーの基礎梁は除く）
    temp=0
    for i in beam_no_x:
        if beams[i-1].category != "BB":
            beams[i-1].M_Lx0 = -beams[i-1].M0\
                          -np.average([abs(beams[i-1].M_Lx[0]),abs(beams[i-1].M_Lx[1])])#固定端モーメントを考慮した梁中央の曲げモーメントM0
            beams[i-1].delta_x = (5*beams[i-1].M_Lx0/(48*EE*beams[i-1].I)*beams[i-1].length**2
                              -sum(beams[i-1].M_Lx)/(16*EE*beams[i-1].I)*beams[i-1].length**2)#梁中央のたわみ（未検証）
            temp += 1
        else:#基礎梁の場合、とりあえず0に
            beams[i - 1].M_Lx0 = 0
            beams[i - 1].delta_x = 0

    temp=0
    for i in beam_no_y:
        if beams[i-1].category != "BB":
            beams[i-1].M_Ly0 = -beams[i-1].M0\
                          -np.average([abs(beams[i-1].M_Ly[0]),abs(beams[i-1].M_Ly[1])])#固定端モーメントを考慮した梁中央の曲げモーメントM0
            beams[i-1].delta_y = (5*beams[i-1].M_Ly0/(48*EE*beams[i-1].I)*beams[i-1].length**2
                            -sum(beams[i-1].M_Ly)/(16*EE*beams[i-1].I)*beams[i-1].length**2)#梁中央のたわみ（未検証）
            temp += 1
        else:#基礎梁の場合、とりあえず0に
            beams[i-1].M_Ly0 = 0
            beams[i-1].delta_y = 0

    # 梁のせん断力の算定
    #X方向
    temp = 0
    for i in beam_no_x:
        temp2 = beams[i-1].M_Lx
        Q0_temp = beams[i-1].Q0  # 分布荷重を想定した単純梁を仮定
        beams[i-1].Q_Lx = [Q0_temp - (temp2[0] + temp2[1]) / beams[i-1].length,
                                 Q0_temp + (temp2[0] + temp2[1]) / beams[i-1].length]
        temp += 1
    #Y方向
    temp = 0
    for i in beam_no_y:
        temp2 = beams[i-1].M_Ly
        Q0_temp = beams[i-1].Q0  # 分布荷重を想定した単純梁を仮定
        beams[i-1].Q_Ly = [Q0_temp - (temp2[0] + temp2[1]) / beams[i-1].length,
                                 Q0_temp + (temp2[0] + temp2[1]) / beams[i-1].length]
        temp += 1

    # 柱のせん断力の算定
    temp = 0
    for i in columns:
        temp2 = i.M_Lx
        i.Q_Lx = [(abs(temp2[0])+abs(temp2[1]))/i.length,
                               (abs(temp2[0])+abs(temp2[1]))/i.length]
        temp += 1
    temp = 0
    for i in columns:
        temp2 = i.M_Ly
        i.Q_Ly = [(abs(temp2[0])+abs(temp2[1]))/i.length,
                               (abs(temp2[0])+abs(temp2[1]))/i.length]
        temp += 1

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

    flag = 0
    if alpha1 < 0:#α1が負の時
        alpha1 = abs(alpha1)
        flag = 1#旗を立てる
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
    if flag == 0:#α1が正のときそのまま
        y1 = list(target_row[str(kk_temp)])[0]
    elif flag == 1:#α1が負の時y1を負にする
        y1 = -list(target_row[str(kk_temp)])[0]

#y2の算定
    target_row = y2_calc[y2_calc['alpha2'] == alpha2]
    if column_story == maximum_story:#最上層の柱ではy2=0とする
        y2 = 0
    else:
        y2 = list(target_row[str(kk_temp)])[0]

#y3の算定
    target_row = y2_calc[y2_calc['alpha3'] == alpha3]
    if column_story == 1:#最下層（1Fとする）の柱ではy3=0とする
        y3= 0
    else:
        y3 = list(target_row[str(kk_temp)])[0]

#反曲点高比の算定
    yy = y0 + y1 + y2 + y3

    return yy

#D値の算定
def calc_D(nodes,columns,beams,layers,direction,D_sum):
    kk=[];a=[];D=[]
    alpha1 = [];alpha2=[]; alpha3=[]; yy=[]

    for i in columns:
        if direction == "X":
            temp = nodes[i.i - 1].beam_no_each_node2_x  # i端部材no
            temp2 = nodes[i.j - 1].beam_no_each_node2_x  # j端部材no
        else:
            temp = nodes[i.i - 1].beam_no_each_node2_y  # i端部材no
            temp2 = nodes[i.j - 1].beam_no_each_node2_y  # j端部材no

        temp_stiff=[];temp_stiff_i=[];temp_stiff_j=[]
        #flag = 0
        #if (nodes[i.i-1].boundary_cond == "pin" or
        #        nodes[i.j-1].boundary_cond == "pin"):
        #    flag = 1  # 柱のi,j側節点にピン支点が含まれる場合
        #elif (nodes[i.i-1].boundary_cond == "fix" or
        #        nodes[i.j-1].boundary_cond == "fix"):
        #    flag = 2  # 柱のi,j側節点に固定支点が含まれる場合
        flag = 3 #とりあえず基礎梁があるものとし、D値法では境界条件の影響は考えない。

        for j in temp:#i端側に接続する梁部材の剛性のみを抽出
            temp_stiff.append(beams[j-1].stiff_ratio)
            temp_stiff_i.append(beams[j-1].stiff_ratio)
        for j in temp2:#j端側に接続する梁部材の剛性のみを抽出
            temp_stiff.append(beams[j-1].stiff_ratio)
            temp_stiff_j.append(beams[j-1].stiff_ratio)

        if flag == 1:
            kk_temp = sum(temp_stiff) / (i.stiff_ratio_x)
            kk.append(kk_temp)
            a.append((0.5*kk_temp)/(1+2*kk_temp))
            D.append(i.stiff_ratio_x*(0.5*kk_temp)/(1+2*kk_temp))#柱脚ピンの場合
            alpha1.append(0) #最下層ではα1=0
        elif flag ==2:
            kk_temp = sum(temp_stiff) / (i.stiff_ratio_x)
            kk.append(kk_temp)
            a.append((0.5+kk_temp)/(2+kk_temp))#柱脚固定の場合
            D.append(i.stiff_ratio_x * (0.5+kk_temp)/(2+kk_temp))
            alpha1.append(0) #最下層ではα1=0
        elif flag == 3:
            kk_temp = sum(temp_stiff)/(2*i.stiff_ratio_x)
            kk.append(kk_temp)
            a.append(kk_temp/(2+kk_temp))#一般階の場合
            D.append(i.stiff_ratio_x * kk_temp/(2+kk_temp))


        #alpha1の算定
            if nodes[i.i-1].z > nodes[i.j-1].z:#i端側がj端側よりも高い場合
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
        if i.story == layers[0].story:
            alpha2.append(0)#最上層の時はalpha2=0
        else:#
            alpha2.append(layers[i.story-layers[0].story].height/layers[i.story-layers[0].story+1].height)
        #alpha3の算定
        if i.story == layers[len(layers)-1].story:
            alpha3.append(0)#最下層の時はalpha3=0
        else:#
            alpha3.append(layers[i.story-layers[0].story+1].height/layers[i.story-layers[0].story].height)

        #各層のD値の和の算定
        D_sum[i.story-1] += D[i.no-1]

    #各柱の反曲点高比の算定
        maximum_story = layers[0].story
        yy_temp = calc_shear_slope(i.story,kk_temp,alpha1[i.no-1],alpha2[i.no-1],alpha3[i.no-1],maximum_story)
        yy.append(yy_temp)

    return D,D_sum,yy

#D値法による地震時荷重の算定
def D_method(nodes,layers,beams,columns,EE):
    D_sum_x=np.zeros((len(layers)));D_sum_y=np.zeros((len(layers)))

    #D値の算定
    D_x,D_sum_x,yy_x = calc_D(nodes,columns,beams,layers,"X",D_sum_x)
    D_y,D_sum_y,yy_y = calc_D(nodes,columns,beams,layers,"Y",D_sum_y)

    #各層の地震荷重を内部算定している場合代入
    for i in layers:
        if i.Qi:
            i.shear_force_x = i.Qi
            i.shear_force_y = i.Qi
        else:
            i.shear_force_x = i.shear_force_x
            i.shear_force_y = i.shear_force_y

    #柱のせん断力、曲げモーメントを算定
    for i in columns:
        #せん断力の算定
        i.D_x = D_x[i.no-1]
        i.D_y = D_y[i.no-1]#D値の柱クラスへの代入

        i.Q_Sx = D_x[i.no-1]/D_sum_x[i.story-1]*layers[layers[0].story-i.story].shear_force_x
        i.Q_Sy = D_y[i.no-1]/D_sum_y[i.story-1]*layers[layers[0].story-i.story].shear_force_y
        #曲げモーメントの算定
        if nodes[i.i-1].z > nodes[i.j-1].z:  # i端側がj端側よりも高い場合
            i.M_Sx = [i.Q_Sx * layers[layers[0].story-i.story].height * (1-yy_x[i.no - 1]),
                                  i.Q_Sx*layers[layers[0].story-i.story].height*yy_x[i.no-1]]
            i.M_Sy = [i.Q_Sy * layers[layers[0].story - i.story].height * (1 - yy_y[i.no - 1]),
                      i.Q_Sy * layers[layers[0].story - i.story].height * yy_y[i.no - 1]]
        else:
            i.M_Sx = [i.Q_Sx * layers[layers[0].story - i.story].height * yy_x[i.no - 1],
                      i.Q_Sx * layers[layers[0].story - i.story].height * (1 - yy_x[i.no - 1])]
            i.M_Sy = [i.Q_Sy * layers[layers[0].story - i.story].height * yy_y[i.no - 1],
                      i.Q_Sy * layers[layers[0].story - i.story].height * (1 - yy_y[i.no - 1])]

    #梁のせん断力、曲げモーメントの算定
    node_moment_x = [];node_moment_y = [];stiff_c_x=[];stiff_c_y=[]
    for i in nodes:#各節点においてとりつく上下柱の曲げモーメントを集計
        temp =0;temp2=0
        for j in columns:
            if i.no == j.i:
                temp += j.M_Sx[0]
                temp2 += j.M_Sy[0]
            if i.no == j.j:
                temp += j.M_Sx[1]
                temp2 += j.M_Sy[1]
        node_moment_x.append(temp)
        node_moment_y.append(temp2)

        # 各節点にとりつく梁の剛性和の算定
        temp=0;temp2=0
        for j in beams:
            if j.direction == "X":
                if j.i == i.no or j.j == i.no:
                    temp += j.stiff_ratio
            else:
                if j.i == i.no or j.j == i.no:
                    temp2 += j.stiff_ratio
        stiff_c_x.append(temp)
        stiff_c_y.append(temp2)

    #各梁の剛比に応じ柱の曲げモーメントを分配
    for i in beams:
        temp_i_x = 0;temp_j_x = 0
        temp_i_y = 0;temp_j_y = 0
        for j in nodes:#i端の算定
            if i.i == j.no:
                for k in j.member_no_each_node_x:
                    if i.no == k:
                        temp_i_x=float(i.stiff_ratio/stiff_c_x[j.no-1]*node_moment_x[j.no-1])
                for k in j.member_no_each_node_y:
                    if i.no == k:
                        temp_i_y=float(i.stiff_ratio/stiff_c_y[j.no-1]*node_moment_y[j.no-1])
            if i.j == j.no:#j端の算定
                for k in j.member_no_each_node_x:
                    if i.no == k:
                        temp_j_x=float(i.stiff_ratio/stiff_c_x[j.no-1]*node_moment_x[j.no-1])
                for k in j.member_no_each_node_y:
                    if i.no == k:
                        temp_j_y=float(i.stiff_ratio/stiff_c_y[j.no-1]*node_moment_y[j.no-1])
        i.M_Sx = [temp_i_x,temp_j_x]
        i.M_Sy = [temp_i_y, temp_j_y]

        i.Q_Sx = (i.M_Sx[0]+i.M_Sx[1])/i.length
        i.Q_Sy = (i.M_Sy[0]+i.M_Sy[1])/i.length

    #各柱の軸力算定（inputファイルにおいて柱リストは上の層のものから順に記載すること）
    temp_axial_column_x = []
    temp_axial_column_y = []

    for i in columns:
            #各柱にとりつく梁のせん断力から想定される軸力を算定
        if nodes[i.i-1].z > nodes[i.j-1].z:  # i端側がj端側よりも高い場合
            temp = nodes[i.i-1].beam_no_each_node_x#i端部材no
            temp2 = nodes[i.i-1].beam_no_each_node_y
        else:
            temp = nodes[i.j-1].beam_no_each_node_x
            temp2 = nodes[i.j-1].beam_no_each_node_y#j端部材no

        #梁のせん断力の差分が軸力となる
        if len(temp) == 1:
            i.temp_axial_column_x = beams[temp[0]-1].Q_Sx
        elif len(temp) == 2:
            i.temp_axial_column_x = abs(beams[temp[0]-1].Q_Sx-beams[temp[1]-1].Q_Sx)

        if len(temp2) == 1:
            i.temp_axial_column_y = beams[temp2[0]-1].Q_Sy
        elif len(temp2) == 2:
            i.temp_axial_column_y = abs(beams[temp2[0]-1].Q_Sy-beams[temp2[1]-1].Q_Sy)

        #上に接続する柱の軸力を足す
    for k in range(len(layers)):
        for i in columns:
            if i.story == len(layers)-k:
                if nodes[i.i-1].z > nodes[i.j-1].z:  # i端側がj端側よりも高い場合
                    temp = nodes[i.i-1].column_no_each_node_x#i端部材no
                    temp2 = nodes[i.i-1].column_no_each_node_y
                else:
                    temp = nodes[i.j-1].column_no_each_node_x
                    temp2 = nodes[i.j-1].column_no_each_node_y#j端部材no

                for j in temp:
                    if j != i.no:#自分以外の柱がある場合その柱の軸力を足す
                        i.N_Sx = columns[i.no-1].temp_axial_column_x+columns[j-1].temp_axial_column_x
                    else:
                        i.N_Sx = columns[i.no-1].temp_axial_column_x

                for j in temp2:
                    if j != i.no:  # 自分以外の柱がある場合その柱の軸力を足す
                        i.N_Sy = columns[i.no-1].temp_axial_column_y+ columns[j- 1].temp_axial_column_y
                    else:
                        i.N_Sy = columns[i.no-1].temp_axial_column_y

        #各層の水平変形の算定
    D_sum_x =np.zeros(len(layers))
    D_sum_y = np.zeros(len(layers))
    for i in layers:
        for j in columns:
            if i.story == j.story:
                D_sum_x[len(layers) -i.story] += j.D_x        #各層柱のD値の集計
                D_sum_y[len(layers)- i.story] += j.D_y

    temp = 0
    for i in layers:#各層の水平変形、水平変形角の算定
        i.horizontal_disp_x = i.shear_force_x*1000/D_sum_x[temp]*(i.height*1000)**2/12/(EE/1000)/(10**5)
        i.horizontal_disp_y = i.shear_force_y*1000/D_sum_y[temp]*(i.height*1000)**2/12/(EE/1000)/10**5
        i.horizontal_angle_x = 1/(i.horizontal_disp_x/i.height/1000)
        i.horizontal_angle_y = 1/(i.horizontal_disp_y/i.height/1000)
        temp +=1

#柱梁の長期・短期荷重の算定
def load_calc(beams,columns):
    #大梁の荷重算定
    for i in beams:
        if i.direction == "X":
            i.ML = max(abs(i.M_Lx[0]),abs(i.M_Lx[1]),abs(i.M_Lx0))
            i.QL = abs(i.Q_Lx[0])
            #中央及び端部の最大値として算定
            i.Ms = max(abs(i.M_Lx0),abs(i.M_Sx[0])+abs(i.M_Lx[0]),abs(i.M_Sx[1])+abs(i.M_Lx[1]))
            i.Qs = max(abs(i.Q_Lx[0]),abs(i.Q_Lx[1]))+i.Q_Sx
        else:
            i.ML = max(abs(i.M_Ly[0]),abs(i.M_Ly[1]),abs(i.M_Ly0))
            i.QL = abs(i.Q_Ly[0])
            #中央及び端部の最大値として算定
            i.Ms = max(abs(i.M_Ly0),abs(i.M_Sy[0])+abs(i.M_Ly[0]),abs(i.M_Sy[1])+abs(i.M_Ly[1]))
            i.Qs = max(abs(i.Q_Ly[0]),abs(i.Q_Ly[1]))+i.Q_Sy

    #柱の荷重算定
    for i in columns:
        i.MLx = max(abs(i.M_Lx[0]),abs(i.M_Lx[1]))
        i.MLy = max(abs(i.M_Ly[0]),abs(i.M_Ly[1]))
        i.QLx = i.Q_Lx[0]
        i.QLy = i.Q_Ly[0]
        i.NL = i.N_Lx
        i.MSx = i.MLx + max(abs(i.M_Sx[0]),abs(i.M_Sx[1]))
        i.QSx = i.QLx + i.Q_Sx
        i.NSx = i.NL + abs(i.N_Sx)
        i.NSy = i.NL + abs(i.N_Sy)
        i.MSy = i.MLy + max(abs(i.M_Sy[0]),abs(i.M_Sy[1]))
        i.QSy = i.QLy + i.Q_Sy

