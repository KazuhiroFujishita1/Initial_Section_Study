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
        C1.append([-FEM_sum[beams[i-1].j - 1] * temp_j/2.0, -FEM_sum[beams[i-1].i - 1] * temp_i/2.0])
        C1_sum[beams[i-1].i-1]+=-FEM_sum[beams[i-1].j-1] * temp_j/2.0
        C1_sum[beams[i-1].j-1]+=-FEM_sum[beams[i-1].i-1] * temp_i/2.0

    for column in columns:
        temp_i = 0;
        temp_j = 0
        for j in range(len(nodes)):  # i端の算定
            if column.i == nodes[j].no:
                for k in range(len(member_no_each_node[j])):
                    if column.no + len(beams) == member_no_each_node[j][k]:
                        temp_i = float(myu[j][k])

            if column.j == nodes[j].no:
                for k in range(len(member_no_each_node[j])):
                    if column.no  +len(beams) == member_no_each_node[j][k]:
                        temp_j = float(myu[j][k])

        D1.append([-FEM_sum[column.i - 1] * temp_i, -FEM_sum[column.j - 1] * temp_j])
        C1.append([-FEM_sum[column.j - 1] * temp_j / 2.0, -FEM_sum[column.i - 1] * temp_i / 2.0])
        C1_sum[column.i - 1] += -FEM_sum[column.j - 1] * temp_j / 2.0
        C1_sum[column.j - 1] += -FEM_sum[column.i - 1] * temp_i / 2.0

    return D1,C1,C1_sum

#部材の接合状況を把握
def detect_connection(nodes,beams,columns):

    for node in nodes:
        #X方向の梁
        temp_x = [];temp4_x=[]
        count_x=0
        for beam in beams:
            if beam.direction == "X": #X方向の場合
                count_x+=1
                if node.no == beam.i or node.no == beam.j :
                    if beam.category == "BB":#基礎梁の場合
                        temp4_x.append(beam.no)
                    else:
                        temp_x.append(beam.no)
                        temp4_x.append(beam.no)
        node.beam_no_each_node_x = temp_x
        node.beam_no_each_node2_x = temp4_x#D値法計算用のリスト（基礎梁含む）

        temp2_x = [];temp3_x = []
        for column in columns:
            if node.no == column.i or node.no == column.j :
                temp3_x.append(column.no)
                temp2_x.append(column.no + len(beams))

        #Y方向の梁
        temp_y = [];temp4_y = []
        count_y=0
        for beam in beams:
            if beam.direction == "Y":  # Y方向の場合
                count_y+=1
                if node.no == beam.i or node.no == beam.j:
                    if beam.category == "BB":#基礎梁の場合
                        temp4_y.append(beam.no)
                    else:
                        temp_y.append(beam.no)
                        temp4_y.append(beam.no)

        node.beam_no_each_node_y = temp_y
        node.beam_no_each_node2_y = temp4_y  # D値法計算用のリスト（基礎梁含む）

        temp2_y = [];temp3_y = []
        for column in columns:
            if node.no == column.i or node.no == column.j :
                temp3_y.append(column.no)
                temp2_y.append(column.no + len(beams))

        node.column_no_each_node_x = temp3_x
        node.column_no_each_node_y = temp3_y
        node.member_no_each_node_x = temp_x+temp2_x#全部材を通し番号で整理
        node.member_no_each_node_y = temp_y+temp2_y#全部材を通し番号で整理
        node.member_no_each_node2_x = temp4_x+temp2_x#全部材を通し番号で整理（基礎梁含む）
        node.member_no_each_node2_y = temp4_y+temp2_y#全部材を通し番号で整理（基礎梁含む）

#固定モーメント法による長期荷重の算定(鹿島様受領Excel（固定モーメント法）の通り）
# #各節点に接続する梁の固定端モーメントの算定
#それぞれの節点に接続する柱梁番号をリストとして整理、モーメント分担率の算定
def fixed_moment_method(nodes,beams,columns,EE):

#各節点ごとに部材ごとのモーメント分担率の算定
    myu_x=[];FEM_sum_x=np.zeros(int((len(nodes))))
    myu_y=[];FEM_sum_y=np.zeros(int((len(nodes))))
    for node in nodes:
        myu_temp=[]

    #モーメント分担率の算定
        if len(node.node_member_stiff2_x) > 1:
            for j in node.node_member_stiff2_x:
                myu_temp.append(j/sum(node.node_member_stiff2_x))
        elif len(node.node_member_stiff2_x) == 1:
            myu_temp.append(1)
        myu_x.append(myu_temp)

        myu_temp=[]
        # モーメント分担率の算定
        if len(node.node_member_stiff2_y) > 1:
            for j in node.node_member_stiff2_y:
                myu_temp.append(j / sum(node.node_member_stiff2_y))
        elif len(node.node_member_stiff2_y) == 1:
            myu_temp.append(1)
        myu_y.append(myu_temp)

#各節点の梁の固定端モーメントの算定（1回目）
    FEM1_x = [];FEM1_y = [];beam_no_x=[];beam_no_y=[]
    for beam in beams:
        if beam.direction == "X":
            beam_no_x.append(beam.no)
            FEM_sum_x[beam.i-1]+=-beam.Ci
        else:
            beam_no_y.append(beam.no)
            FEM_sum_y[beam.i-1]+=-beam.Ci
        if beam.direction == "X":
            FEM_sum_x[beam.j-1]+= beam.Cj
        else:
            FEM_sum_y[beam.j-1]+= beam.Cj

        if beam.direction == "X":
            FEM1_x.append([-beam.Ci,beam.Cj])
        else:
            FEM1_y.append([-beam.Ci,beam.Cj])

#各部材ごとに梁の分担モーメント、到達モーメントの算定（1回目）

    member_no_each_node2_x=[];member_no_each_node2_y=[]
    for node in nodes:
        member_no_each_node2_x.append(node.member_no_each_node2_x)
    for node in nodes:
        member_no_each_node2_y.append(node.member_no_each_node2_y)

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

    for column in columns:
        column.M_Lx = np.array(D1_x[temp])+np.array(C1_x[temp])+np.array(D2_x[temp])+np.array(C2_x[temp])#固定モーメント法の解
        temp +=1

    temp = 0
    for i in beam_no_y:
        beams[i-1].M_Ly = np.array(FEM1_y[temp])+np.array(D1_y[temp])+np.array(C1_y[temp])+np.array(D2_y[temp])+np.array(C2_y[temp])#固定モーメント法の解
        temp += 1

    for column in columns:
        column.M_Ly = np.array(D1_y[temp])+np.array(C1_y[temp])+np.array(D2_y[temp])+np.array(C2_y[temp])#固定モーメント法の解
        temp += 1

#各部材ごとに大梁のたわみ算定(ダミーの基礎梁は除く）
    temp=0
    for i in beam_no_x:
        if beams[i-1].category != "BB":
            beams[i-1].M_Lx0 = beams[i-1].M0\
                          -np.average([beams[i-1].M_Lx[0],beams[i-1].M_Lx[1]])#固定端モーメントを考慮した梁中央の曲げモーメントM0
            beams[i-1].delta_x = (5*beams[i-1].M_Lx0/(48.0*EE*beams[i-1].I)*beams[i-1].length**2
                              -sum(beams[i-1].M_Lx)/(16.0*EE*beams[i-1].I)*beams[i-1].length**2)#梁中央のたわみ（未検証）
            temp += 1
        else:#基礎梁の場合、とりあえず0に
            beams[i - 1].M_Lx0 = 0
            beams[i - 1].delta_x = 0

    temp=0
    for i in beam_no_y:
        if beams[i-1].category != "BB":
            beams[i-1].M_Ly0 = beams[i-1].M0\
                          -np.average([beams[i-1].M_Ly[0],beams[i-1].M_Ly[1]])#固定端モーメントを考慮した梁中央の曲げモーメントM0
            beams[i-1].delta_y = (5*beams[i-1].M_Ly0/(48.0*EE*beams[i-1].I)*beams[i-1].length**2
                            -sum(beams[i-1].M_Ly)/(16.0*EE*beams[i-1].I)*beams[i-1].length**2)#梁中央のたわみ（未検証）
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
    for column in columns:
        temp2 = column.M_Lx
        column.Q_Lx = [(abs(temp2[0])+abs(temp2[1]))/column.length,
                               (abs(temp2[0])+abs(temp2[1]))/column.length]
        temp += 1
    temp = 0
    for column in columns:
        temp2 = column.M_Ly
        column.Q_Ly = [(abs(temp2[0])+abs(temp2[1]))/column.length,
                               (abs(temp2[0])+abs(temp2[1]))/column.length]
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

    for column in columns:
        if direction == "X":
            temp = nodes[column.i - 1].beam_no_each_node2_x  # i端部材no
            temp2 = nodes[column.j - 1].beam_no_each_node2_x  # j端部材no
        else:
            temp = nodes[column.i - 1].beam_no_each_node2_y  # i端部材no
            temp2 = nodes[column.j - 1].beam_no_each_node2_y  # j端部材no

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
            kk_temp = sum(temp_stiff) / (column.stiff_ratio_x)
            kk.append(kk_temp)
            a.append((0.5*kk_temp)/(1+2*kk_temp))
            D.append(column.stiff_ratio_x*(0.5*kk_temp)/(1+2*kk_temp))#柱脚ピンの場合
            alpha1.append(0) #最下層ではα1=0
        elif flag ==2:
            kk_temp = sum(temp_stiff) / (column.stiff_ratio_x)
            kk.append(kk_temp)
            a.append((0.5+kk_temp)/(2+kk_temp))#柱脚固定の場合
            D.append(column.stiff_ratio_x * (0.5+kk_temp)/(2+kk_temp))
            alpha1.append(0) #最下層ではα1=0
        elif flag == 3:
            kk_temp = sum(temp_stiff)/(2*column.stiff_ratio_x)
            kk.append(kk_temp)
            a.append(kk_temp/(2+kk_temp))#一般階の場合
            D.append(column.stiff_ratio_x * kk_temp/(2+kk_temp))

        #alpha1の算定
            if nodes[column.i-1].z > nodes[column.j-1].z:#i端側がj端側よりも高い場合
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
        if column.story == layers[0].story:
            alpha2.append(0)#最上層の時はalpha2=0
        else:#
            alpha2.append(layers[column.story-layers[0].story].height/layers[column.story-layers[0].story+1].height)
        #alpha3の算定
        if column.story == layers[len(layers)-1].story:
            alpha3.append(0)#最下層の時はalpha3=0
        else:#
            alpha3.append(layers[column.story-layers[0].story+1].height/layers[column.story-layers[0].story].height)

        #各層のD値の和の算定
        D_sum[column.story-1] += D[column.no-1]

    #各柱の反曲点高比の算定
        maximum_story = layers[0].story
        yy_temp = calc_shear_slope(column.story,kk_temp,alpha1[column.no-1],alpha2[column.no-1],alpha3[column.no-1],maximum_story)
        yy.append(yy_temp)

    return D,D_sum,yy

#D値法による地震時荷重の算定
def D_method(nodes,layers,beams,columns,EE):
    #単位変換用係数
    m_to_mm = 1000.0#m→mmへ
    kN_to_N = 1000.0#kN→Nへ

    D_sum_x=np.zeros((len(layers)));D_sum_y=np.zeros((len(layers)))

    #D値の算定
    D_x,D_sum_x,yy_x = calc_D(nodes,columns,beams,layers,"X",D_sum_x)
    D_y,D_sum_y,yy_y = calc_D(nodes,columns,beams,layers,"Y",D_sum_y)

    #各層の地震荷重を内部算定している場合代入
    for layer in layers:
        if layer.Qi:
            layer.shear_force_x = layer.Qi
            layer.shear_force_y = layer.Qi
        else:
            layer.shear_force_x = layer.shear_force_x
            layer.shear_force_y = layer.shear_force_y

    #柱のせん断力、曲げモーメントを算定
    for column in columns:
        #せん断力の算定
        column.D_x = D_x[column.no-1]
        column.D_y = D_y[column.no-1]#D値の柱クラスへの代入

        column.Q_Sx = D_x[column.no-1]/D_sum_x[column.story-1]*layers[layers[0].story-column.story].shear_force_x
        column.Q_Sy = D_y[column.no-1]/D_sum_y[column.story-1]*layers[layers[0].story-column.story].shear_force_y
        #曲げモーメントの算定
        if nodes[column.i-1].z > nodes[column.j-1].z:  # i端側がj端側よりも高い場合
            column.M_Sx = [column.Q_Sx * layers[layers[0].story-column.story].height * (1-yy_x[column.no - 1]),
                                  column.Q_Sx*layers[layers[0].story-column.story].height*yy_x[column.no-1]]
            column.M_Sy = [column.Q_Sy * layers[layers[0].story - column.story].height * (1 - yy_y[column.no - 1]),
                      column.Q_Sy * layers[layers[0].story - column.story].height * yy_y[column.no - 1]]
        else:
            column.M_Sx = [column.Q_Sx * layers[layers[0].story - column.story].height * yy_x[column.no - 1],
                      column.Q_Sx * layers[layers[0].story - column.story].height * (1 - yy_x[column.no - 1])]
            column.M_Sy = [column.Q_Sy * layers[layers[0].story - column.story].height * yy_y[column.no - 1],
                      column.Q_Sy * layers[layers[0].story - column.story].height * (1 - yy_y[column.no - 1])]

    #梁のせん断力、曲げモーメントの算定
    node_moment_x = [];node_moment_y = [];stiff_c_x=[];stiff_c_y=[]
    for node in nodes:#各節点においてとりつく上下柱の曲げモーメントを集計
        temp =0;temp2=0
        for column in columns:
            if node.no == column.i:
                temp += column.M_Sx[0]
                temp2 += column.M_Sy[0]
            if node.no == column.j:
                temp += column.M_Sx[1]
                temp2 += column.M_Sy[1]
        node_moment_x.append(temp)
        node_moment_y.append(temp2)

        # 各節点にとりつく梁の剛性和の算定
        temp=0;temp2=0
        for beam in beams:
            if beam.direction == "X":
                if beam.i == node.no or beam.j == node.no:
                    temp += beam.stiff_ratio
            else:
                if beam.i == node.no or beam.j == node.no:
                    temp2 += beam.stiff_ratio
        stiff_c_x.append(temp)
        stiff_c_y.append(temp2)

    #各梁の剛比に応じ柱の曲げモーメントを分配
    for beam in beams:
        temp_i_x = 0;temp_j_x = 0
        temp_i_y = 0;temp_j_y = 0
        for node in nodes:#i端の算定
            if beam.i == node.no:
                for k in node.member_no_each_node_x:
                    if beam.no == k:
                        temp_i_x=float(beam.stiff_ratio/stiff_c_x[node.no-1]*node_moment_x[node.no-1])
                for k in node.member_no_each_node_y:
                    if beam.no == k:
                        temp_i_y=float(beam.stiff_ratio/stiff_c_y[node.no-1]*node_moment_y[node.no-1])
            if beam.j == node.no:#j端の算定
                for k in node.member_no_each_node_x:
                    if beam.no == k:
                        temp_j_x=float(beam.stiff_ratio/stiff_c_x[node.no-1]*node_moment_x[node.no-1])
                for k in node.member_no_each_node_y:
                    if beam.no == k:
                        temp_j_y=float(beam.stiff_ratio/stiff_c_y[node.no-1]*node_moment_y[node.no-1])
        beam.M_Sx = [temp_i_x,temp_j_x]
        beam.M_Sy = [temp_i_y, temp_j_y]

        beam.Q_Sx = (beam.M_Sx[0]+beam.M_Sx[1])/beam.length
        beam.Q_Sy = (beam.M_Sy[0]+beam.M_Sy[1])/beam.length

    #各柱の軸力算定（inputファイルにおいて柱リストは上の層のものから順に記載すること）
    temp_axial_column_x = []
    temp_axial_column_y = []

    for column in columns:
            #各柱にとりつく梁のせん断力から想定される軸力を算定
        if nodes[column.i-1].z > nodes[column.j-1].z:  # i端側がj端側よりも高い場合
            temp = nodes[column.i-1].beam_no_each_node_x#i端部材no
            temp2 = nodes[column.i-1].beam_no_each_node_y
        else:
            temp = nodes[column.j-1].beam_no_each_node_x
            temp2 = nodes[column.j-1].beam_no_each_node_y#j端部材no

        #梁のせん断力の差分が軸力となる
        if len(temp) == 1:
            column.temp_axial_column_x = beams[temp[0]-1].Q_Sx
        elif len(temp) == 2:
            column.temp_axial_column_x = abs(beams[temp[0]-1].Q_Sx-beams[temp[1]-1].Q_Sx)

        if len(temp2) == 1:
            column.temp_axial_column_y = beams[temp2[0]-1].Q_Sy
        elif len(temp2) == 2:
            column.temp_axial_column_y = abs(beams[temp2[0]-1].Q_Sy-beams[temp2[1]-1].Q_Sy)

        #上に接続する柱の軸力を足す
    for k in range(len(layers)):
        for column in columns:
            if column.story == len(layers)-k:
                if nodes[column.i-1].z > nodes[column.j-1].z:  # i端側がj端側よりも高い場合
                    temp = nodes[column.i-1].column_no_each_node_x#i端部材no
                    temp2 = nodes[column.i-1].column_no_each_node_y
                else:
                    temp = nodes[column.j-1].column_no_each_node_x
                    temp2 = nodes[column.j-1].column_no_each_node_y#j端部材no

                for j in temp:
                    if j != column.no:#自分以外の柱がある場合その柱の軸力を足す
                        column.N_Sx = columns[column.no-1].temp_axial_column_x+columns[j-1].temp_axial_column_x
                    else:
                        column.N_Sx = columns[column.no-1].temp_axial_column_x

                for j in temp2:
                    if j != column.no:  # 自分以外の柱がある場合その柱の軸力を足す
                        column.N_Sy = columns[column.no-1].temp_axial_column_y+ columns[j- 1].temp_axial_column_y
                    else:
                        column.N_Sy = columns[column.no-1].temp_axial_column_y

        #各層の水平変形の算定
    D_sum_x =np.zeros(len(layers))
    D_sum_y = np.zeros(len(layers))
    for layer in layers:
        for column in columns:
            if layer.story == column.story:
                D_sum_x[len(layers) -layer.story] += column.D_x        #各層柱のD値の集計
                D_sum_y[len(layers)- layer.story] += column.D_y

    temp = 0
    for layer in layers:#各層の水平変形、水平変形角の算定
        layer.horizontal_disp_x = layer.shear_force_x*kN_to_N/D_sum_x[temp]*(layer.height*m_to_mm)**2/12.0/(EE/1000.0)/(10**5)
        layer.horizontal_disp_y = layer.shear_force_y*kN_to_N/D_sum_y[temp]*(layer.height*m_to_mm)**2/12.0/(EE/1000.0)/10**5
        layer.horizontal_angle_x = 1.0/(layer.horizontal_disp_x/layer.height/m_to_mm)
        layer.horizontal_angle_y = 1.0/(layer.horizontal_disp_y/layer.height/m_to_mm)
        temp +=1

#柱梁の長期・短期荷重の算定
def load_calc(beams,columns):
    #大梁の荷重算定
    for beam in beams:
        if beam.direction == "X":
            beam.ML = max(abs(beam.M_Lx[0]),abs(beam.M_Lx[1]),abs(beam.M_Lx0))
            beam.QL = abs(beam.Q_Lx[0])
            #中央及び端部の最大値として算定
            beam.Ms = max(abs(beam.M_Lx0),abs(beam.M_Sx[0])+abs(beam.M_Lx[0]),abs(beam.M_Sx[1])+abs(beam.M_Lx[1]))
            beam.Qs = max(abs(beam.Q_Lx[0]),abs(beam.Q_Lx[1]))+beam.Q_Sx
        else:
            beam.ML = max(abs(beam.M_Ly[0]),abs(beam.M_Ly[1]),abs(beam.M_Ly0))
            beam.QL = abs(beam.Q_Ly[0])
            #中央及び端部の最大値として算定
            beam.Ms = max(abs(beam.M_Ly0),abs(beam.M_Sy[0])+abs(beam.M_Ly[0]),abs(beam.M_Sy[1])+abs(beam.M_Ly[1]))
            beam.Qs = max(abs(beam.Q_Ly[0]),abs(beam.Q_Ly[1]))+beam.Q_Sy

    #柱の荷重算定
    for column in columns:
        column.MLx = max(abs(column.M_Lx[0]),abs(column.M_Lx[1]))
        column.MLy = max(abs(column.M_Ly[0]),abs(column.M_Ly[1]))
        column.QLx = column.Q_Lx[0]
        column.QLy = column.Q_Ly[0]
        column.NL = column.N_Lx
        column.MSx = column.MLx + max(abs(column.M_Sx[0]),abs(column.M_Sx[1]))
        column.QSx = column.QLx + column.Q_Sx
        column.NSx = column.NL + abs(column.N_Sx)
        column.NSy = column.NL + abs(column.N_Sy)
        column.MSy = column.MLy + max(abs(column.M_Sy[0]),abs(column.M_Sy[1]))
        column.QSy = column.QLy + column.Q_Sy

