import pandas as pd
import numpy as np

#部材長の算定
def calc_length(member_i,member_j,nodes):
    length = np.sqrt((nodes[member_i-1].x - nodes[member_j-1].x) ** 2  # 各部材の部材長算定
            + (nodes[member_i-1].y - nodes[member_j-1].y) ** 2 + (nodes[member_i-1].z - nodes[member_j-1].z)**2)
    return length

#データの読み込み
def read_model():
    # 節点の情報を収集
    df1 = pd.read_csv("./make_sample_model/output_node.csv",header=0)
    #df1 = pd.read_excel("input_model.xlsx", sheet_name="Node", header=0)
    node_data = []
    for i in range(len(df1)):
        node_data.append((df1['No'][i],df1['x'][i],df1['y'][i],df1['z'][i],df1['boundary'][i]))

    nodes = [Node(*data) for data in node_data] #節点インスタンスの作成

    #　梁の情報を収集
    df2 = pd.read_csv("./make_sample_model/output_beams.csv",header=0)
    #df2 = pd.read_excel("input_model.xlsx", sheet_name="Beam", header=0)
    beam_data = []
    for i in range(len(df2)):
        #梁長さの算定
        beam_length=calc_length(df2['i_point'][i],df2['j_point'][i],nodes)
        #梁のCMQの読み込み
        beam_load_i=df2['C'][i] #* beam_length ** 2 / 12
        beam_load_j=df2['C'][i] #* beam_length ** 2 / 12
        M0 = df2['M'][i]
        Q0 = df2['Q'][i]

        #梁の分布荷重の逆算（等分布荷重を想定）
        dist_load = beam_load_i*12/beam_length**2

        #梁の方向判定
        if round(nodes[df2['i_point'][i] - 1].x,1) == round(nodes[df2['j_point'][i] - 1].x,1):
            beam_direction="X"
        else:
            beam_direction="Y"
        beam_data.append((df2['No.'][i],df2['i_point'][i],df2['j_point'][i],beam_length,
                          dist_load,beam_load_i,beam_load_j,df2['category'][i],beam_direction,df2['phai'][i],M0,Q0,df2['story'][i]))

    beams = [Beam(*data) for data in beam_data] #梁インスタンスの作成

    #柱の情報を収集
    df3 = pd.read_csv("./make_sample_model/output_columns.csv",header=0)
    #df3 = pd.read_excel("input_model.xlsx", sheet_name="Column", header=0)
    column_data = [];
    for i in range(len(df3)):
        #柱長さの算定
        column_length=calc_length(df3['i_point'][i],df3['j_point'][i],nodes)

        column_data.append((df3['No.'][i],df3['i_point'][i],df3['j_point'][i],df3['story'][i],column_length,df3['load_area'][i]))

    columns = [Column(*data) for data in column_data]#柱インスタンスの作成

    #層の情報を収集
    df4 = pd.read_csv("./make_sample_model/output_layer.csv",header=0)
    #df4 = pd.read_excel("input_model.xlsx", sheet_name="Story_shear", header=0)
    layer_data = []; maximum_height =0
    for i in range(len(df4)):
        layer_data.append((df4['Story'][i],df4['Story_height'][i],df4['omega_1'][i],df4['omega_2'][i],df4['floor_area'][i]))
        maximum_height += df4['Story_height'][i]
    layers = [Layer(*data) for data in layer_data]#層インスタンスの作成

    return nodes, beams, columns,layers,maximum_height

# 節点のクラス
class Node():
    boundary_cond: object

    def __init__(self, node_no, node_x, node_y, node_z, boundary):
        self.no = node_no
        self.x = node_x
        self.y = node_y
        self.z = node_z
        self.boundary_cond = boundary

        self.beam_no_each_node_x = []
        self.column_no_each_node_x = []
        self.column_no_each_node_y = []
        self.member_no_each_node_x = []
        self.beam_no_each_node2_x = []
        self.member_no_each_node2_x = []
        self.beam_no_each_node_y = []
        self.beam_no_each_node2_y = []
        self.member_no_each_node_y = []
        self.member_no_each_node2_y = []
        self.node_member_stiff_x = []
        self.node_member_stiff_y = []
        self.node_member_stiff2_x = []
        self.node_member_stiff2_y = []

        self.req_Mpx = [] #柱梁耐力比1以上とするために必要な柱の全塑性モーメント
        self.req_Mpy = [] #柱梁耐力比1以上とするために必要な柱の全塑性モーメント

    # 梁のクラス
class Beam():
    def __init__(self,beam_no,beam_i,beam_j,beam_length,
                 dist_load,beam_load_i,beam_load_j,beam_category,beam_direction,beam_phai,M0,Q0,story):
        self.no = beam_no
        self.i = beam_i
        self.j = beam_j
        self.length = beam_length
        self.I = []#beam_section_I
        self.K = [] #剛度
        self.pai = beam_phai #床スラブの剛性増大率
        self.stiff_ratio = []#beam_stiff#剛比
        self.dist_load = dist_load #梁の分布荷重
        self.Ci = beam_load_i#i端の固定端モーメント
        self.Cj = beam_load_j#j端の固定端モーメント
        self.category = beam_category#基礎梁か否か
        self.direction = beam_direction#梁方向
        self.story = story

        self.M0 = M0#MQ荷重※とりあえずM0は単純梁の曲げモーメントとして内部計算に使用
        self.Q0 = Q0

        self.unit_weight = 0#部材自重　kg/m
        self.weight = 0

        self.Z = []#断面係数
        self.Zp = []

        self.B = []#H型鋼の形状
        self.H = []
        self.t1 = []
        self.t2 = []

        self.init_group = []#初期断面のグルーピング

        self.Mp = []#選択された部材の全塑性モーメント

        self.M_Lx =[]#算定応力
        self.M_Lx0 =[]
        self.M_Ly =[]
        self.M_Ly0 =[]
        self.M_Sx =[]
        self.M_Sy =[]

        self.Q_Lx = []
        self.Q_Ly = []
        self.Q_Sx = []
        self.Q_Sy = []

        self.N_Lx = []
        self.N_Ly = []
        self.N_Sx = []
        self.N_Sy = []

        self.ML = []
        self.QL = []
        self.Ms = []
        self.Qs = []

        self.sigma_b_L = []
        self.tau_L = []
        self.sigma_b_s = []
        self.tau_s = []

        self.judge_b_L = []
        self.judge_b_s = []
        self.judge_s_L = []
        self.judge_s_s = []

        self.delta_x = []
        self.delta_y = []

        self.selected_section_no = []
        self.required_web_area = []
        self.required_Z = []

        self.F = []#FF

    # 柱のクラス
class Column():
    def __init__(self,column_no,column_i,column_j,column_story,column_length,load_area):
        self.no = column_no
        self.i = column_i
        self.j = column_j
        self.story = column_story
        self.length = column_length
        self.A = []
        self.Ix = []#Ix
        self.Iy = []#Iy
        self.Z = []
        self.Zp = []
        self.H = []
        self.t = []
        self.stiff_ratio_x = []#stiff_ratio_x#剛比
        self.stiff_ratio_y = []#stiff_ratio_y
        self.F = []#FF
        self.base_K = [] #柱せいより決まる等価な基礎梁剛度
        self.load_area = load_area #柱の負担面積

        self.init_group = []#初期断面のグルーピング

        self.Mpx = []#全塑性曲げモーメント
        self.Mpy = []#全塑性曲げモーメント

        self.unit_weight = 0#部材自重
        self.weight = 0

        self.D_x = []#算定D値
        self.D_y = []

        self.M_Lx =[]#算定応力
        self.M_Ly =[]
        self.M_Sx =[]
        self.M_Sy =[]

        self.Q_Lx = []
        self.Q_Ly = []
        self.Q_Sx = []
        self.Q_Sy = []

        self.N_Lx = []
        self.N_Ly = []
        self.N_Sx = []
        self.N_Sy = []

        self.MLx = []
        self.MLy = []
        self.QLx = []
        self.QLy = []
        self.NL = []
        self.MSx = []
        self.MSy = []
        self.QSx = []
        self.QSy = []
        self.NSx = []
        self.NSy = []

        self.required_area = []
        self.selected_section_no = []
        self.decrement_ratio_x = []
        self.decrement_ratio_y = []

        self.minimum_selected_section_no = []
        self.tc1 = []
        self.tc2x = []
        self.tc2y = []
        self.tc = []

        self.temp_axial_column_x = []
        self.temp_axial_column_y = []

    # 層のクラス
class Layer():
    def __init__(self,story,height,omega_1,omega_2,floor_area):
        self.story = story
        self.height = height
        self.shear_force_x = []#shear_force_x
        self.shear_force_y = []#shear_force_y
        self.omega1 = omega_1
        self.omega2 = omega_2
        self.floor_area = floor_area

        self.weight = []
        self.cum_weight = []
        self.alpha_i = []
        self.Ai = []
        self.Ci = []
        self.Qi = []

        self.horizontal_disp_x = []#層間変形
        self.horizontal_disp_y = []
        self.horizontal_angle_x = []#層間変形角
        self.horizontal_angle_y = []

        self.column_num = [] #柱本数

        self.req_D_sum_x = [] #変形から決まる各層の必要D
        self.req_D_sum_y = [] #変形から決まる各層の必要D
        self.req_D_x = [] #変形から決まる各柱の必要D値
        self.req_D_y = [] #変形から決まる各柱の必要D値

        self.D_sum_x = [] #各層のD
        self.D_sum_y = [] #各層のD

        self.D_max_x = []#各層のD値の最大値
        self.D_max_y = []#各層のD値の最大値

        self.k_limit1_x = []#剛性バランスにより決まる各層の柱剛性のクライテリア
        self.k_limit1_y = []#剛性バランスにより決まる各層の柱剛性のクライテリア

        self.I_limit1_x = []#剛性バランスにより決まる各層の柱断面二次モーメントのクライテリア
        self.I_limit1_y = []#剛性バランスにより決まる各層の柱断面二次モーメントのクライテリア

class Column_Group():#柱グループ
    def __init__(self,group_no,group_name,group_ID):
        self.no = group_no
        self.group_name = group_name
        self.ID = group_ID

class Beam_Group():#梁グループ
    def __init__(self,group_no,group_name,group_ID):
        self.no = group_no
        self.group_name = group_name
        self.ID = group_ID
        self.neighbor_beam = []
        self.neighbor_group = []
        self.neighbor_group_no = []
