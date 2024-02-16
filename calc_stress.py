from main import *
from member_class import *
import math

#分担モーメント、到達モーメントの計算
def calc_moment(FEM_sum,member_no_each_node,myu,nodes,beams,columns,beam_no):
    D1 = [];
    C1 = [];
    C1_sum = np.zeros(len(nodes))

    for i in beam_no:#梁について
        temp_i = 0;temp_j=0
        for k in range(len(member_no_each_node[beams[i-1].i])):#i端側の算定
            if beams[i - 1].no == member_no_each_node[beams[i-1].i][k]:
                temp_i = float(myu[beams[i-1].i-1][k])
        for k in range(len(member_no_each_node[beams[i-1].j])):#j端側の算定
            if beams[i - 1].no == member_no_each_node[beams[i-1].j][k]:
                temp_j = float(myu[beams[i-1].j-1][k])

        D1.append([-FEM_sum[beams[i-1].i-1]*temp_i, -FEM_sum[beams[i-1].j-1]*temp_j])
        C1.append([-FEM_sum[beams[i-1].j - 1] * temp_j/2.0, -FEM_sum[beams[i-1].i - 1] * temp_i/2.0])
        C1_sum[beams[i-1].i-1]+=-FEM_sum[beams[i-1].j-1] * temp_j/2.0
        C1_sum[beams[i-1].j-1]+=-FEM_sum[beams[i-1].i-1] * temp_i/2.0

    for column in columns:#柱について
        temp_i = 0;
        temp_j = 0
        for k in range(len(member_no_each_node[column.i])):#i端側の算定
            if column.no + len(beams) == member_no_each_node[column.i][k]:
                temp_i = float(myu[column.i-1][k])
        for k in range(len(member_no_each_node[column.j])):#j端側の算定
            if column.no + len(beams) == member_no_each_node[column.j][k]:
                temp_j = float(myu[column.j-1][k])

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

#更新後断面における剛比算定
def calc_stiffness_ratio(columns,beams,nodes):
    #柱断面の最大剛度を探索
    max_K = 0
    for column in columns:
        if column.KX >= max_K:
            max_K = column.KX
    #柱の最大剛度を基準に各部材の剛比を算定
    for column in columns:
        column.stiff_ratio_x = column.KX/max_K
        column.stiff_ratio_y = column.KY/max_K
    for beam in beams:
        if beam.category != "BB":  # 基礎梁以外
            beam.stiff_ratio = beam.K/max_K
    
    #梁種別、梁端条件に応じた等価剛比の格納
    calc_eq_beam_stiffness(beams,columns,nodes)

#梁部材について基礎梁か否か、また梁端境界条件に応じた等価剛比を格納
def calc_eq_beam_stiffness(beams,columns,nodes):
    #単位変換用係数
    m_to_mm = 1000.0#m→mmへ
    II = 10000#800×900の基礎梁断面→無限大の基礎梁断面
    for beam in beams:
        if beam.category != "BB":  # 基礎梁以外
            if beam.boundary_i == "pin" and beam.boundary_j == "fix":  # i端がピン接合の場合
                beam.eq_beam_stiff_ratio_i = 0
                beam.eq_beam_stiff_ratio_j = beam.stiff_ratio * 0.5
            elif beam.boundary_i == "fix" and beam.boundary_j == "pin":  # j端がピン接合の場合
                beam.eq_beam_stiff_ratio_i = beam.stiff_ratio * 0.5
                beam.eq_beam_stiff_ratio_j = 0
            elif beam.boundary_i == "pin" and beam.boundary_j == "pin":  # 両端がピン接合の場合
                beam.eq_beam_stiff_ratio_i = 0
                beam.eq_beam_stiff_ratio_j = 0
            else:
                beam.eq_beam_stiff_ratio_i = beam.stiff_ratio
                beam.eq_beam_stiff_ratio_j = beam.stiff_ratio  # 両端に同じ等価剛比を代入

        else:  # 基礎梁の場合
            beam.K = columns[nodes[beam.i-1].column_no_each_node_x[0]-1].base_K
            beam.eq_beam_stiff_ratio_i = 1.0/(1.0/columns[nodes[beam.i-1].column_no_each_node_x[0]-1].base_K+1.0/(II/(beam.length*m_to_mm)))/100000.0
            beam.eq_beam_stiff_ratio_j = 1.0/(1.0/columns[nodes[beam.j-1].column_no_each_node_x[0]-1].base_K+1.0/(II/(beam.length*m_to_mm)))/100000.0

#固定モーメント法に関する関数
#モーメント分担率の算定
def distribute_moment(node_moment):
    myu_temp = []
    if len(node_moment) > 1:
        for j in node_moment:
            myu_temp.append(j / sum(node_moment))
    elif len(node_moment) == 1:
        myu_temp.append(1)

    return myu_temp
    
#モーメントの和の算定
def moment_sum(FEM,D1,C1,D2,temp):
    if len(FEM) != 0:
        sigma_moment = np.array(FEM[temp])+np.array(D1[temp])+np.array(C1[temp])+np.array(D2[temp])#+np.array(C2[temp])
    else:
        sigma_moment = np.array(D1[temp])+np.array(C1[temp])+np.array(D2[temp])#+np.array(C2[temp])
    return sigma_moment

#梁たわみ算定（とりあえず両端固定の境界条件で考えている）
def calc_beam_deflection(beam_no,beams,EE,dir):
    beam_M=[];delta=[]
    temp=0
    for i in beam_no:
        if beams[i-1].category != "BB":
            if dir == "X":
                beam_M.append(beams[i-1].M0\
                          -np.average([abs(beams[i-1].M_Lx[0]),abs(beams[i-1].M_Lx[1])]))#固定端モーメントを考慮した梁中央の曲げモーメントM0
                delta.append(5 * beams[i-1].M0 / (48.0 * EE * beams[i - 1].I * beams[i-1].calc_phai) * beams[i - 1].length ** 2
                                       -(abs(beams[i-1].M_Lx[0])+abs(beams[i-1].M_Lx[1]))/(16.0*EE*beams[i-1].I)*beams[i-1].length**2)#梁中央のたわみ（未検証

            elif dir == "Y":
                beam_M.append(beams[i-1].M0\
                          -np.average([abs(beams[i-1].M_Ly[0]),abs(beams[i-1].M_Ly[1])]))#固定端モーメントを考慮した梁中央の曲げモーメントM0
                delta.append(5 * beams[i-1].M0 / (48.0 * EE * beams[i - 1].I* beams[i-1].calc_phai) * beams[i - 1].length ** 2
                                       -(abs(beams[i-1].M_Ly[0])+abs(beams[i-1].M_Ly[1]))/(16.0*EE*beams[i-1].I)*beams[i-1].length**2)#梁中央のたわみ（未検証
            else:#XY方向以外の場合例外エラー
                "Error:calc of beam deflection."

        else:#基礎梁の場合、とりあえず0に
            beam_M.append(0)
            delta.append(0)
        temp +=1
    return beam_M, delta
    
#はりのせんだん力算定
def calc_beam_shear(temp2,Q0_temp,length):
     # 分布荷重を想定した単純梁を仮定
    beam_shear = [Q0_temp - (temp2[0] + temp2[1]) / length,
                                 Q0_temp + (temp2[0] + temp2[1]) / length]
    return beam_shear
    
#柱のせんだん力算定
def calc_column_shear(temp2,length):
    column_shear = [(temp2[0]+temp2[1])/length,(temp2[0]+temp2[1])/length]
    return column_shear

#固定モーメント法による長期荷重の算定(鹿島様受領Excel（固定モーメント法）の通り）
# #各節点に接続する梁の固定端モーメントの算定
#それぞれの節点に接続する柱梁番号をリストとして整理、モーメント分担率の算定
def fixed_moment_method(nodes,beams,columns,EE):

#各節点ごとに部材ごとのモーメント分担率の算定
    myu_x =[];myu_y=[]
    FEM_sum_x=np.zeros(int((len(nodes))))
    FEM_sum_y=np.zeros(int((len(nodes))))
    temp=0
    for node in nodes:
    #モーメント分担率の算定
        myu_x.append(distribute_moment(node.node_member_stiff2_x))
        myu_y.append(distribute_moment(node.node_member_stiff2_y))
        temp+=1

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
    member_no_each_node2_x_dict = {node.no: node.member_no_each_node2_x for node in nodes}
    member_no_each_node2_y_dict = {node.no: node.member_no_each_node2_y for node in nodes}

    D1_x,C1_x,C1_sum_x = calc_moment(FEM_sum_x,member_no_each_node2_x_dict,myu_x,nodes,beams,columns,beam_no_x)
    D1_y,C1_y,C1_sum_y = calc_moment(FEM_sum_y,member_no_each_node2_y_dict,myu_y,nodes,beams,columns,beam_no_y)

#各部材ごとに梁の分担モーメントの算定（2回目）
    D2_x,C2_x,C2_sum_x = calc_moment(C1_sum_x,member_no_each_node2_x_dict,myu_x,nodes,beams,columns,beam_no_x)
    D2_y,C2_y,C2_sum_y = calc_moment(C1_sum_y,member_no_each_node2_y_dict,myu_y,nodes,beams,columns,beam_no_y)

#各部材ごとにモーメントの和の算定(D2まで計算する(受領Excelに整合させる））
    temp = 0
    for i in beam_no_x:
        beams[i-1].M_Lx = moment_sum(FEM1_x,D1_x,C1_x,D2_x,temp)#固定モーメント法の解
        temp +=1
    for column in columns:
        column.M_Lx = moment_sum("",D1_x,C1_x,D2_x,temp)#固定モーメント法の解
        temp +=1

    temp = 0
    for i in beam_no_y:
        beams[i-1].M_Ly = moment_sum(FEM1_y,D1_y,C1_y,D2_y,temp)#固定モーメント法の解
        temp += 1
    for column in columns:
        column.M_Ly = moment_sum("",D1_y,C1_y,D2_y,temp)#固定モーメント法の解
        temp += 1

#最下部の柱端のみC2を変える処理
    for column in columns:
        for node in nodes:  # 最下部（z=0)となる柱端のみC2を変える処理
            if node.no == column.i:
                if node.z == 0:
                    column.M_Lx[0] = column.M_Lx[1] / 2
                    column.M_Ly[0] = column.M_Ly[1] / 2
            if node.no == column.j:
                if node.z == 0:
                    column.M_Lx[1] = column.M_Lx[0] / 2
                    column.M_Ly[1] = column.M_Ly[0] / 2

#各部材ごとに大梁のたわみ算定(ダミーの基礎梁は除く）
    beam_M_x, delta_x = calc_beam_deflection(beam_no_x,beams,EE,"X")
    temp = 0
    for i in beam_no_x:
        beams[i-1].M_Lx0 = beam_M_x[temp]
        beams[i-1].delta_x = delta_x[temp]
        temp += 1

    beam_M_y, delta_y = calc_beam_deflection(beam_no_y,beams,EE,"Y")
    temp = 0
    for i in beam_no_y:
        beams[i-1].M_Ly0 = beam_M_y[temp]
        beams[i-1].delta_y = delta_y[temp]
        temp += 1
    #print(beam_M_y)

    # 梁のせん断力の算定
    #X方向
    temp = 0
    for i in beam_no_x:
        beams[i-1].Q_Lx = calc_beam_shear(beams[i-1].M_Lx,beams[i-1].Q0,beams[i-1].length)
        temp += 1
    #Y方向
    temp = 0
    for i in beam_no_y:
        beams[i-1].Q_Ly = calc_beam_shear(beams[i-1].M_Ly,beams[i-1].Q0,beams[i-1].length)
        temp += 1

    # 柱のせん断力の算定
    for column in columns:
        column.Q_Lx = calc_column_shear(column.M_Lx,column.length)
        column.Q_Ly = calc_column_shear(column.M_Ly,column.length)

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

    return y0,y1,y2,y3,yy

#D値の算定
def calc_D(nodes,columns,beams,layers,direction,D_sum):
    kk=[];a=[];D=[]
    alpha1 = [];alpha2=[]; alpha3=[]; yy=[]
    tttt = 0
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
        flag = 3 #とりあえず基礎梁があるものとし、架構基部の境界があるときのD値法の式は考えない。

        for j in temp:#i端側に接続する梁部材の剛性のみを抽出
            if beams[j-1].i == nodes[column.i - 1].no:
                temp_stiff.append(beams[j-1].eq_beam_stiff_ratio_i)
                temp_stiff_i.append(beams[j-1].eq_beam_stiff_ratio_i)
            else:
                temp_stiff.append(beams[j-1].eq_beam_stiff_ratio_j)
                temp_stiff_i.append(beams[j-1].eq_beam_stiff_ratio_j)

        for j in temp2:#j端側に接続する梁部材の剛性のみを抽出
            if beams[j-1].i == nodes[column.i - 1].no:
                temp_stiff.append(beams[j-1].eq_beam_stiff_ratio_i)
                temp_stiff_j.append(beams[j-1].eq_beam_stiff_ratio_i)
            else:
                temp_stiff.append(beams[j-1].eq_beam_stiff_ratio_j)
                temp_stiff_j.append(beams[j-1].eq_beam_stiff_ratio_j)

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
        y0_temp, y1_temp, y2_temp, y3_temp, yy_temp = calc_shear_slope(column.story,kk_temp,alpha1[column.no-1],alpha2[column.no-1],alpha3[column.no-1],maximum_story)
        yy.append(yy_temp)

    #D値法の諸元出力
        if direction =="X":
            column.y0_x = y0_temp
            column.y1_x = y1_temp
            column.y2_x = y2_temp
            column.y3_x = y3_temp
        elif direction == "Y":
            column.y0_y = y0_temp
            column.y1_y = y1_temp
            column.y2_y = y2_temp
            column.y3_y = y3_temp
        else:
            "Error: No direction on the calc y."

        column.kk = kk[tttt]
        column.a = a[tttt]

        tttt += 1

    return D,D_sum,yy

#D値法における柱剪断力算定
def calc_D_column_shear(D,D_sum,layer_shear):
    column_shear = D/D_sum*layer_shear
    return column_shear

#D値法における柱曲げモーメントの算定
def calc_D_column_moment(h_i,h_j,column_shear,height,ho):
    if h_i > h_j:  # i端側がj端側よりも高い場合
        column_moment = [column_shear * height * (1-ho),column_shear * height*ho]
    else:
        column_moment = [column_shear * height*ho,column_shear * height * (1-ho)]
    return column_moment        

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

        column.Q_Sx = calc_D_column_shear(D_x[column.no-1],D_sum_x[column.story-1],
                                        layers[layers[0].story-column.story].shear_force_x)
        column.Q_Sy = calc_D_column_shear(D_y[column.no-1],D_sum_y[column.story-1],
                                        layers[layers[0].story-column.story].shear_force_y)
        #曲げモーメントの算定
        column.M_Sx = calc_D_column_moment(nodes[column.i-1].z,nodes[column.j-1].z,
                                               column.Q_Sx,layers[layers[0].story-column.story].height,yy_x[column.no - 1])
        column.M_Sy = calc_D_column_moment(nodes[column.i-1].z,nodes[column.j-1].z,
                                               column.Q_Sy,layers[layers[0].story-column.story].height,yy_y[column.no - 1])            

    #梁のせん断力、曲げモーメントの算定
    node_moment_x = [];node_moment_y = [];stiff_c_x=[];stiff_c_y=[]
    for node in nodes:#各節点においてとりつく上下柱の曲げモーメントを集計
        temp =0;temp2=0
        for attached_column in node.column_no_each_node_x:
            if node.no == columns[attached_column-1].i:#i端のモーメント参照
                temp += columns[attached_column-1].M_Sx[0]
            else:#j端のモーメント参照
                temp += columns[attached_column-1].M_Sx[1]    
        for attached_column in node.column_no_each_node_y:
            if node.no == columns[attached_column-1].i:#i端のモーメント参照
                temp2 += columns[attached_column-1].M_Sy[0]
            else:#j端のモーメント参照
                temp2 += columns[attached_column-1].M_Sy[1]                
        node_moment_x.append(temp)
        node_moment_y.append(temp2)

        # 各節点にとりつく梁の剛性和の算定
        temp=0;temp2=0
        for attached_beam in node.beam_no_each_node2_x:
            if node.no == beams[attached_beam-1].i:#i端のモーメント参照
                temp += beams[attached_beam-1].eq_beam_stiff_ratio_i
            else:#j端のモーメント参照
                temp += beams[attached_beam-1].eq_beam_stiff_ratio_j 
        for attached_beam in node.beam_no_each_node2_y:
            if node.no == beams[attached_beam-1].j:#i端のモーメント参照
                temp2 += beams[attached_beam-1].eq_beam_stiff_ratio_i
            else:#j端のモーメント参照
                temp2 += beams[attached_beam-1].eq_beam_stiff_ratio_j 

        stiff_c_x.append(temp)
        stiff_c_y.append(temp2)

    #各梁の剛比に応じ柱の曲げモーメントを分配
    for beam in beams:
        temp_i_x=0;temp_j_x=0
        temp_i_y=0;temp_j_y=0
        if beam.direction == "X":
            if stiff_c_x[beam.i-1] != 0:
                temp_i_x = float(beam.eq_beam_stiff_ratio_i/stiff_c_x[beam.i-1]*node_moment_x[beam.i-1])
            else:#i端にとりつく梁の剛性和が0の場合
                temp_i_x = 0
            if stiff_c_x[beam.j-1] != 0:
                temp_j_x = float(beam.eq_beam_stiff_ratio_j/stiff_c_x[beam.j-1]*node_moment_x[beam.j-1])
            else:#j端にとりつく梁の剛性和が0の場合
                temp_j_x = 0

        else:
            if stiff_c_y[beam.i-1] != 0:
                temp_i_y = float(beam.eq_beam_stiff_ratio_i/stiff_c_y[beam.i-1]*node_moment_y[beam.i-1])
            else:#i端にとりつく梁の剛性和が0の場合
                temp_i_y = 0
            if stiff_c_y[beam.j-1] != 0:
                temp_j_y = float(beam.eq_beam_stiff_ratio_j/stiff_c_y[beam.j-1]*node_moment_y[beam.j-1])
            else:#j端にとりつく梁の剛性和が0の場合
                temp_j_y = 0

        beam.M_Sx = [temp_i_x,temp_j_x]
        beam.M_Sy = [temp_i_y, temp_j_y]

        beam.Q_Sx = (beam.M_Sx[0]+beam.M_Sx[1])/beam.length
        beam.Q_Sy = (beam.M_Sy[0]+beam.M_Sy[1])/beam.length

    #各柱の軸力算定
    for column in columns:
            #各柱にとりつく梁のせん断力から想定される軸力を算定
        if nodes[column.i-1].z > nodes[column.j-1].z:  # 上はりの剪断力を参照
            #i端側がj端側よりも高い場合
            temp = nodes[column.i-1].beam_no_each_node_x#i端部材no
            temp2 = nodes[column.i-1].beam_no_each_node_y
        else:
            temp = nodes[column.j-1].beam_no_each_node_x
            temp2 = nodes[column.j-1].beam_no_each_node_y#j端部材no

        #柱の上側に取りつく梁のせん断力の差分がはりの剪断力による軸力となる
        if len(temp) == 1:
            column.temp_axial_column_x = beams[temp[0]-1].Q_Sx
        elif len(temp) == 2:
            column.temp_axial_column_x = beams[temp[0]-1].Q_Sx-beams[temp[1]-1].Q_Sx

        if len(temp2) == 1:
            column.temp_axial_column_y = beams[temp2[0]-1].Q_Sy
        elif len(temp2) == 2:
            column.temp_axial_column_y = beams[temp2[0]-1].Q_Sy-beams[temp2[1]-1].Q_Sy

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
                        column.N_Sx = column.temp_axial_column_x+columns[j-1].temp_axial_column_x
                        column.temp_axial_column_x = column.N_Sx #該当する柱の仮の軸力も更新する
                    else:
                        column.N_Sx = column.temp_axial_column_x

                for j in temp2:
                    if j != column.no:  # 自分以外の柱がある場合その柱の軸力を足す
                        column.N_Sy = column.temp_axial_column_y+ columns[j- 1].temp_axial_column_y
                        column.temp_axial_column_y = column.N_Sy #該当する柱の仮の軸力も更新する
                    else:
                        column.N_Sy = column.temp_axial_column_y

                D_sum_x[len(layers) -layer.story] += column.D_x        #各層柱のD値の集計
                D_sum_y[len(layers)- layer.story] += column.D_y

        #各層の水平変形の算定
    
    temp = 0
    for layer in layers:#各層の水平変形、水平変形角の算定
        layer.D_sum_x = D_sum_x[temp]
        layer.D_sum_y = D_sum_y[temp]
        layer.horizontal_disp_x = layer.shear_force_x*kN_to_N/layer.D_sum_x*(layer.height*m_to_mm)**2/12.0/(EE/1000.0)/(10**5)
        layer.horizontal_disp_y = layer.shear_force_y*kN_to_N/layer.D_sum_y*(layer.height*m_to_mm)**2/12.0/(EE/1000.0)/10**5
        layer.horizontal_angle_x = 1.0/(layer.horizontal_disp_x/layer.height/m_to_mm)
        layer.horizontal_angle_y = 1.0/(layer.horizontal_disp_y/layer.height/m_to_mm)
        temp += 1

#柱梁の長期・短期荷重の算定
def load_calc(beams,columns):
    #大梁の荷重算定
    for beam in beams:
        if beam.direction == "X":
            beam.ML = max(abs(beam.M_Lx[0]),abs(beam.M_Lx[1]),abs(beam.M_Lx0))
            beam.QL = max(abs(beam.Q_Lx[0]),abs(beam.Q_Lx[1]))
            #中央及び端部の最大値として算定
            beam.Ms = max(abs(beam.M_Lx0),abs(beam.M_Sx[0])+abs(beam.M_Lx[0]),abs(beam.M_Sx[1])+abs(beam.M_Lx[1]))
            beam.Qs = max(abs(beam.Q_Lx[0]),abs(beam.Q_Lx[1]))+beam.Q_Sx
        else:
            beam.ML = max(abs(beam.M_Ly[0]),abs(beam.M_Ly[1]),abs(beam.M_Ly0))
            beam.QL = max(abs(beam.Q_Ly[0]),abs(beam.Q_Ly[1]))
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
        column.QSx = abs(column.QLx) + column.Q_Sx
        column.NSx = column.NL + abs(column.N_Sx)
        column.NSy = column.NL + abs(column.N_Sy)
        column.MSy = column.MLy + max(abs(column.M_Sy[0]),abs(column.M_Sy[1]))
        column.QSy = abs(column.QLy) + column.Q_Sy

