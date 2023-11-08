import pandas as pd
import numpy as np

#部材長の算定
def calc_length(member_i,member_j):
    node = Node()
    length = np.sqrt((node.x[member_i-1] - node.x[member_j-1]) ** 2  # 各部材の部材長算定
            + (node.y[member_i-1] - node.y[member_j-1]) ** 2 + (node.z[member_i-1] - node.z[member_j-1])**2)
    return length

# 節点のクラス
class Node():
    def __init__(self):
        df1 = pd.read_excel("input_model.xlsx", sheet_name="Node", header=0)
        # 節点の情報を収集
        node_no = list(df1['No'])
        node_x = list(df1['x'])
        node_y = list(df1['y'])
        node_z = list(df1['z'])
        boundary = list(df1['boundary'])

        self.no = node_no
        self.x = node_x
        self.y = node_y
        self.z = node_z
        self.boundary_cond = boundary

    def call_node(self, no):
        return self.x[no], self.y[no], self.z[no]

    def call_boundary(self, no):
        return self.boundary_cond[no]

    # 梁のクラス
class Beam():
    def __init__(self):
        df2 = pd.read_excel("input_model.xlsx", sheet_name="Beam", header=0)

        # 梁の情報を収集
        member_no = [];  # 部材の通し番号もつくる
        beam_no = list(df2['No.'])
        beam_i = list(df2['i_point'])
        beam_j = list(df2['j_point'])
        beam_section_I = list(df2['I'])
        beam_stiff = list(df2['stiffness_ratio'])
        beam_distributed_load = list(df2['w'])
        beam_category = list(df2['category'])
        beam_length = []
        for i in range(len(beam_no)):  # 梁部材長の算定
            beam_length.append(calc_length(beam_i[i], beam_j[i]))

        # 分布荷重→C
        beam_load_i = [];
        beam_load_j = []
        for i in range(len(beam_no)):
            beam_load_i.append(-beam_distributed_load[i] * beam_length[i] ** 2 / 12)
            beam_load_j.append(-beam_distributed_load[i] * beam_length[i] ** 2 / 12)

            # 梁の方向を分類（まずは直交座標を仮定）
        beam_no_x = [];
        beam_no_y = [];
        beam_i_x = [];
        beam_i_y = []
        beam_j_x = [];
        beam_j_y = [];
        beam_stiff_x = [];
        beam_stiff_y = [];
        beam_load_i_x = [];
        beam_load_j_x = [];
        beam_load_i_y = [];
        beam_load_j_y = []
        C_moment_x = [];
        C_moment_y = [];
        beam_category_x = [];
        beam_category_y = []
        beam_distributed_load_x = [];
        beam_distributed_load_y = []
        beam_section_I_x = [];
        beam_section_I_y = []
        beam_length_x = [];
        beam_length_y = [];

            # 節点情報に関してDataFrameから辞書を生成
        df1 = pd.read_excel("input_model.xlsx", sheet_name="Node", header=0)
        data_dict1 = df1.to_dict(orient='records')

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
                beam_distributed_load_y.append(beam_distributed_load[i])
                C_moment_y.append([-beam_load_i[i], beam_load_j[i]])
                beam_category_y.append(beam_category[i])
                beam_section_I_y.append(beam_section_I[i])
                beam_length_y.append(beam_length[i])

            elif y_value_i == y_value_j:
                beam_no_x.append(beam_no[i])
                beam_i_x.append(beam_i[i])
                beam_j_x.append(beam_j[i])
                beam_stiff_x.append(beam_stiff[i])
                beam_load_i_x.append(beam_load_i[i])
                beam_load_j_x.append(beam_load_j[i])
                beam_distributed_load_x.append(beam_distributed_load[i])
                C_moment_x.append([-beam_load_i[i], beam_load_j[i]])
                beam_category_x.append(beam_category[i])
                beam_section_I_x.append(beam_section_I[i])
                beam_length_x.append(beam_length[i])

        self.no_all = beam_no
        self.i = beam_i
        self.j = beam_j
        self.length = beam_length
        self.I = beam_section_I
        self.stiff_ratio = beam_stiff
        self.dist_load = beam_distributed_load
        self.Ci = beam_load_i
        self.Cj = beam_load_j
        self.category = beam_category

        self.beam_no_x =beam_no_x
        self.beam_i_x = beam_i_x
        self.beam_j_x = beam_j_x
        self.beam_length_x =beam_length_x
        self.beam_section_I_x =beam_section_I_x
        self.beam_stiff_x =beam_stiff_x
        self.beam_distributed_load_x = beam_distributed_load_x
        self.beam_load_i_x = beam_load_i_x
        self.beam_load_j_x = beam_load_j_x
        self.beam_category_x = beam_category_x

        self.beam_no_y = beam_no_y
        self.beam_i_y = beam_i_y
        self.beam_j_y = beam_j_y
        self.beam_length_y = beam_length_y
        self.beam_section_I_y = beam_section_I_y
        self.beam_stiff_y = beam_stiff_y
        self.beam_distributed_load_y = beam_distributed_load_y
        self.beam_load_i_y = beam_load_i_y
        self.beam_load_j_y = beam_load_j_y
        self.beam_category_y = beam_category_y

    def call_x_dir(self):  # X方向の梁の呼び出し
        self.no = self.beam_no_x
        self.i = self.beam_i_x
        self.j = self.beam_j_x
        self.length = self.beam_length_x
        self.I = self.beam_section_I_x
        self.stiff_ratio = self.beam_stiff_x
        self.dist_load = self.beam_distributed_load_x
        self.Ci = self.beam_load_i_x
        self.Cj = self.beam_load_j_x
        self.category = self.beam_category_x

    def call_y_dir(self):  # Y方向の梁の呼び出し
        self.no = self.beam_no_y
        self.i = self.beam_i_y
        self.j = self.beam_j_y
        self.length = self.beam_length_y
        self.I = self.beam_section_I_y
        self.stiff_ratio = self.beam_stiff_y
        self.dist_load = self.beam_distributed_load_y
        self.Ci = self.beam_load_i_y
        self.Cj = self.beam_load_j_y
        self.category = self.beam_category_y

    # 柱のクラス
class Column():
    def __init__(self):
        df3 = pd.read_excel("input_model.xlsx", sheet_name="Column", header=0)

        # 柱の情報を収集
        column_no = list(df3['No.'])
        column_i = list(df3['i_point'])
        column_j = list(df3['j_point'])
        column_story = list(df3['story'])
        column_length = []
        for i in range(len(column_no)):  # 柱部材長の算定
            column_length.append(calc_length(column_i[i], column_j[i]))

        self.no = column_no
        self.i = column_i
        self.j = column_j
        self.story = column_story
        self.length = column_length
        self.column_section_Ix = list(df3['Ix'])
        self.column_stiff_x = list(df3['stiffness_ratio_x'])
        self.column_section_Iy = list(df3['Iy'])
        self.column_stiff_y = list(df3['stiffness_ratio_y'])

    def call_x_info(self):  # X方向諸元の呼び出し
        self.I = self.column_section_Ix
        self.stiff_ratio = self.column_stiff_x

    def call_y_info(self):  # Y方向諸元の呼び出し
        self.I = self.column_section_Iy
        self.stiff_ratio = self.column_stiff_y

    # 部材のクラス
class Member():
    def __init__(self):
        df2 = pd.read_excel("input_model.xlsx", sheet_name="Beam", header=0)
        df3 = pd.read_excel("input_model.xlsx", sheet_name="Column", header=0)
        beam_no = list(df2['No.'])
        beam_i = list(df2['i_point'])
        beam_j = list(df2['j_point'])
        beam= Beam()
        column = Column()
        column.call_x_info()#とりあえず部材のクラスを埋めるときは、x方向を参照
        # 全部材の情報を定義
        member_no = list(df2['No.']) + list(df3['No.'] + len(beam.no_all))
        member_i = list(df2['i_point']) + list(df3['i_point'])
        member_j = list(df2['j_point']) + list(df3['j_point'])
        member_load_i = list(beam.Ci) + list([0] * len(column.no))
        member_load_j = list(beam.Cj) + list([0] * len(column.no))
        member_length = list(beam.length) + list(column.length)

        member_stiff = beam.stiff_ratio + column.stiff_ratio

        # 節点情報に関してDataFrameから辞書を生成
        df1 = pd.read_excel("input_model.xlsx", sheet_name="Node", header=0)
        data_dict1 = df1.to_dict(orient='records')

        for i in range(len(beam_no)):
            coordinate_i = next(item for item in data_dict1 if item['No'] == int(beam_i[i]))
            coordinate_j = next(item for item in data_dict1 if item['No'] == int(beam_j[i]))

            x_value_i = coordinate_i['x']
            x_value_j = coordinate_j['x']
            y_value_i = coordinate_j['y']
            y_value_j = coordinate_j['y']

            if x_value_i == x_value_j:
                beam.call_y_dir()
                member_no_y = beam.no + list(df3['No.'] + len(beam_no))
                member_i_y = beam.i + column.i
                member_j_y = beam.j + column.j
                member_load_i_y = beam.Ci + list([0] * len(column.no))
                member_load_j_y = beam.Cj + list([0] * len(column.no))

            elif y_value_i == y_value_j:
                beam.call_x_dir()
                member_no_x = beam.no + list(df3['No.'] + len(beam_no))
                member_i_x = beam.i + column.i
                member_j_x = beam.j + column.j
                member_load_i_x = beam.Ci + list([0] * len(column.no))
                member_load_j_x = beam.Cj + list([0] * len(column.no))

        beam.call_x_dir()
        member_length_x = list(beam.length) + list(column.length)
        beam.call_y_dir()
        member_length_y = list(beam.length) + list(column.length)

        self.no = member_no
        self.i = member_i
        self.j = member_j
        self.i_all = member_i
        self.j_all = member_j
        self.length = member_length
        self.stiff_ratio = member_stiff
        self.Ci = member_load_i
        self.Cj = member_load_j

        self.member_no_x = member_no_x
        self.member_i_x = member_i_x
        self.member_j_x = member_j_x
        self.member_length_x = member_length_x
        self.member_load_i_x = member_load_i_x
        self.member_load_j_x = member_load_j_x

        self.member_no_y = member_no_y
        self.member_i_y = member_i_y
        self.member_j_y = member_j_y
        self.member_length_y = member_length_y
        self.member_load_i_y = member_load_i_y
        self.member_load_j_y = member_load_j_y

    def call_x_dir(self):  # X方向の梁の呼び出し
        self.no = self.member_no_x
        self.i = self.member_i_x
        self.j = self.member_j_x
        self.length = self.member_length_x
        self.Ci = self.member_load_i_x
        self.Cj = self.member_load_j_x

    def call_y_dir(self):  # Y方向の梁の呼び出し
        self.no = self.member_no_y
        self.i = self.member_i_y
        self.j = self.member_j_y
        self.length = self.member_length_y
        self.Ci = self.member_load_i_y
        self.Cj = self.member_load_j_y

    # 層のクラス
class Layer():
    def __init__(self):
        df4 = pd.read_excel("input_model.xlsx", sheet_name="Story_shear", header=0)
        self.height = list(df4['Story_height'])

    def call_x_dir(self):  # X方向
        df4 = pd.read_excel("input_model.xlsx", sheet_name="Story_shear", header=0)
        self.shear_force = list(df4['Shear_force_X'])

    def call_y_dir(self):  # Y方向
        df4 = pd.read_excel("input_model.xlsx", sheet_name="Story_shear", header=0)
        self.shear_force = list(df4['Shear_force_Y'])