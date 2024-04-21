

import unittest

from calc_stress import *
from member_class import *
from set_initial_section import *
from calc_weight import *
from update_section import *
from output_section_data import *
import yaml

class CalculationTests(unittest.TestCase):
    TO_CALC_WEIGHT = 0
    TO_DETECT_CONNECTION = 1
    TO_INITIAL_SECTION = 2
    TO_FIXED_MOMENT_METHOD = 3
    TO_D_METHOD = 4
    TO_D_UPDATE_SECTION = 5

    def setup(self):
        self.nodes = []
        self.beams = []
        self.columns = []
        self.layers = []
        self.column_groups = []
        self.beam_groups = []
        self.maximum_height = 0.0

    def prepare(self, step):

        self.nodes = [
            Node(1, 0.0, 0.0, 0.0, '','1F','X1','Y1'),
            Node(2, 6.0, 0.0, 0.0, '','1F','X2','Y1'),
            Node(3, 0.0, 0.0, 3.0, '','2F','X1','Y1'),
            Node(4, 6.0, 0.0, 3.0, '','2F','X2','Y1'),
            Node(5, 0.0, 6.0, 0.0, '','1F','X1','Y2'),
            Node(6, 6.0, 6.0, 0.0, '','1F','X2','Y2'),
            Node(7, 0.0, 6.0, 3.0, '','2F','X1','Y1'),
            Node(8, 6.0, 6.0, 3.0, '','2F','X2','Y2'),
        ]
        (phi, phi2) = (1.2, 1.3)
        beam_length = 6.0
        beam_load_i = 10.0
        beam_load_j = 10.0
        dist_load = beam_load_i*12.0/beam_length**2
        category = ''
        M0 = beam_load_i * 0.8
        Q0 = 5.0
        self.beams = [
            Beam(1, 3, 4, beam_length, dist_load, beam_load_i, beam_load_j, category, 'Y', phi, phi2, M0, Q0, 2, 'fix', 'fix'),
            Beam(2, 7, 8, beam_length, dist_load, beam_load_i, beam_load_j, category, 'Y', phi, phi2, M0, Q0, 2, 'fix', 'fix'),
            Beam(3, 3, 7, beam_length, dist_load, beam_load_i, beam_load_j, category, 'X', phi, phi2, M0, Q0, 2, 'fix', 'fix'),
            Beam(4, 4, 8, beam_length, dist_load, beam_load_i, beam_load_j, category, 'X', phi, phi2, M0, Q0, 2, 'fix', 'fix')
        ]
        load_area = 9
        column_length = 3.0
        wall_load_length = 6.0
        self.columns = [
            Column(1, 1, 3, 1, column_length,load_area, wall_load_length),
            Column(2, 2, 4, 1, column_length,load_area, wall_load_length),
            Column(3, 5, 7, 1, column_length,load_area, wall_load_length),
            Column(4, 6, 8, 1, column_length,load_area, wall_load_length)
        ]

        floor_area = 36
        outer_wall_length = 24.0
        self.layers = [
            Layer(1, 3.0, 7.65, 1.0, 7.3, 1.0, floor_area, outer_wall_length)
        ] 

        if step < self.TO_DETECT_CONNECTION:
            return

        detect_connection(self.nodes, self.beams, self.columns)

        maximum_height = 3.0
        calc_layer_weight(self.nodes,self.beams, self.columns, self.layers, maximum_height)

        if step < self.TO_INITIAL_SECTION: 
            return

        beam_select_mode = "cost"
        self.beam_groups,self.column_groups = set_initial_section(self.nodes, self.beams, self.columns, maximum_height, beam_select_mode)

        if step < self.TO_FIXED_MOMENT_METHOD:
            return

        EE= 205000000 #鋼材のヤング係数
        fixed_moment_method(self.nodes, self.beams, self.columns, EE)

        if step < self.TO_D_METHOD: 
            return
        D_method(self.nodes, self.layers, self.beams, self.columns, EE)

        if step < self.TO_D_UPDATE_SECTION: 
            return
        #柱梁の長期・短期荷重まとめ
        load_calc(self.beams, self.columns)
        
        fLag=0
        #大梁断面の更新
        beam_groups = update_beam_section(self.nodes, self.beams, beam_select_mode,EE,self.column_groups,self.beam_groups,fLag)
        #柱断面の更新
        column_groups = update_column_section(self.nodes, self.beams, self.columns, self.layers, EE, self.column_groups,
                                              self.beam_groups,beam_select_mode, fLag)

        return
    
    def test_before_detect_connection(self):
        self.prepare(self.TO_CALC_WEIGHT)

        y_beams = filter(lambda b: b.direction == "Y", self.beams)#X、Y方向の梁はそれぞれ2本ずつになるはず
        x_beams = filter(lambda b: b.direction == "X", self.beams)
        self.assertEqual(2, len(list(y_beams)))
        self.assertEqual(2, len(list(x_beams)))

    def test_detect_connection(self):
        self.prepare(self.TO_DETECT_CONNECTION)

        for node in self.nodes:
            print(node.__dict__)
        for beam in self.beams:
            print(beam.__dict__)
        for column in self.columns:
            print(column.__dict__)

        # 接続梁数が想定通りか
        self.assertEqual(0, len(self.nodes[0].beam_no_each_node_x))
        self.assertEqual(0, len(self.nodes[0].beam_no_each_node_y))
        self.assertEqual(1, len(self.nodes[2].beam_no_each_node_x))
        self.assertEqual(1, len(self.nodes[2].beam_no_each_node_y))

        # 接続柱数が想定通りか
        self.assertEqual(1, len(self.nodes[0].column_no_each_node_x))
        self.assertEqual(1, len(self.nodes[0].column_no_each_node_y))
        self.assertEqual(1, len(self.nodes[2].column_no_each_node_x))
        self.assertEqual(1, len(self.nodes[2].column_no_each_node_y))

        # 接続柱梁数が想定通りか
        self.assertEqual(1, len(self.nodes[0].member_no_each_node_x))
        self.assertEqual(1, len(self.nodes[0].member_no_each_node_y))
        self.assertEqual(2, len(self.nodes[2].member_no_each_node_x))
        self.assertEqual(2, len(self.nodes[2].member_no_each_node_y))

        outer_wall_length = 24.0
        floor_area = 36
        # 層重量の算定が妥当か
        self.assertEqual(7.65*floor_area+1*3/2*outer_wall_length, self.layers[0].weight)
        self.assertEqual(7.3*floor_area+1*3/2*outer_wall_length, self.layers[0].weight_seismic)

        # 柱軸力の算定が妥当か
        self.assertEqual(self.layers[0].weight/4, self.columns[0].N_Lx)
        self.assertEqual(self.layers[0].weight/4, self.columns[0].N_Ly)

    def test_set_initial_section(self):
        self.prepare(self.TO_INITIAL_SECTION)

        #初期梁せいが正しく算定されているか
        self.assertEqual(400,self.beams[0].H)
        #初期柱せいが正しく算定されているか
        self.assertEqual(300, self.columns[0].H)
        #内梁、外梁判定が機能しているか
        self.assertEqual('OB', self.beams[0].beam_place)

        #柱梁の初期グルーピング数が適切か
        beam_group_no = 0; column_group_no = 0
        for i in self.beam_groups:
            beam_group_no += 1
        for i in self.column_groups:
            column_group_no += 1
        self.assertEqual(2, beam_group_no)
        self.assertEqual(1, column_group_no)

    def test_fixed_moment(self):
        self.prepare(self.TO_FIXED_MOMENT_METHOD)
        # モーメント
        column1 = self.columns[0]
        beam1   = self.beams[0]
        beam2   = self.beams[2]
        # 節点周りのモーメントが釣り合うか？
        self.assertAlmostEqual(0.0, column1.M_Ly[1] + beam1.M_Ly[0], places=2)

        # 撓みの計算が適切か？
        EE= 205000000 #鋼材のヤング係数
        self.assertAlmostEqual(beam1.delta_y,5 * beam1.M0 / (48.0 * EE * beam1.I * beam1.calc_phai) * beam1.length ** 2
                                       -(abs(beam1.M_Ly[0])+abs(beam1.M_Ly[1]))/(16.0*EE*beam1.I* beam1.calc_phai)*beam1.length**2)#Y方向梁
        self.assertAlmostEqual(beam2.delta_x,5 * beam2.M0 / (48.0 * EE * beam2.I * beam2.calc_phai) * beam2.length ** 2
                                       -(abs(beam2.M_Lx[0])+abs(beam2.M_Lx[1]))/(16.0*EE*beam2.I* beam1.calc_phai)*beam2.length**2)#X方向梁

    def test_D_method(self):
        self.prepare(self.TO_D_METHOD)
        column1 = self.columns[0];column2 = self.columns[1]
        column3 = self.columns[2];column4 = self.columns[3]
        # 層の地震力と得られる柱の層せん断力の和が等しくなるか
        self.assertAlmostEqual(self.layers[0].shear_force_x,column1.Q_Sx+column2.Q_Sx+column3.Q_Sx+column4.Q_Sx)
        self.assertAlmostEqual(self.layers[0].shear_force_y,column1.Q_Sy+column2.Q_Sy+column3.Q_Sy+column4.Q_Sy)

    def test_update_beam_section(self):
        self.prepare(self.TO_D_UPDATE_SECTION)
        #梁断面更新後のグルーピング数が前後で同じか？
        beam_group_no = 0
        for i in self.beam_groups:
            beam_group_no += 1
        self.assertEqual(2,beam_group_no)
        #選定断面に基づく梁応力検定比が0.9以下となるか？
        kN_to_N = 1000.0  # kN→Nへ
        m_to_mm = 1000.0  # m→mmへ
        EE = 205000000  # 鋼材のヤング係数
        for beam in self.beams:
            self.assertLess(beam.QL*kN_to_N/#せん断長期
                        ((beam.H-beam.t2*2-beam.r*2)*beam.B)
                        /(beam.F/math.sqrt(3)/1.5),0.9)
            self.assertLess(beam.ML*kN_to_N*m_to_mm/#曲げ長期
                        (beam.t1*(beam.H-beam.t2*2)**2/6)
                        /(beam.F/1.5),0.9)
            self.assertLess(beam.Qs*kN_to_N/#せん断短期
                        ((beam.H-beam.t2*2-beam.r*2)*beam.B)
                        /(beam.F/math.sqrt(3)),0.9)
            self.assertLess(beam.Ms*kN_to_N*m_to_mm/#曲げ短期
                        (beam.t1*(beam.H-beam.t2*2)**2/6)
                        /(beam.F),0.9)

        #選定断面に基づく梁たわみが1/300rad以下となるか？
        self.assertLess(5 * self.beams[0].M0 / (48.0 * EE * self.beams[0].I * self.beams[0].calc_phai) * self.beams[0].length ** 2
                                - (abs(self.beams[0].M_Ly[0])+abs(self.beams[0].M_Ly[1])) /
                            (16.0 * EE * self.beams[0].I * self.beams[0].calc_phai) * self.beams[0].length ** 2,
                        1/300*self.beams[0].length)

    def test_update_column_section(self):
        self.prepare(self.TO_D_UPDATE_SECTION)

        #選定断面に基づく柱諸元が層間変形角1/200radを満たすために必要な層の必要剛性を満たしているか？
        for column in self.columns:
            self.assertGreater(column.Ix,self.layers[0].I_limit1_x)
            self.assertGreater(column.Iy,self.layers[0].I_limit1_y)

        kN_to_N = 1000.0  # kN→Nへ
        m_to_mm = 1000.0  # m→mmへ
        #柱梁耐力比1以上を満たしているか
        tarbeam_Mp=0
        # for tar_beam in self.nodes[self.columns[0].j-1].beam_no_each_node_x:
        #     print(self.beams[tar_beam-1].Mp)
        #     tarbeam_Mp += self.beams[tar_beam-1].Mp#最上階、最下階の節点については、柱梁耐力比を考慮していない

        axial_ratio_x = (self.columns[0].axial_column_x_Mp * kN_to_N /
                         (self.columns[0].A * m_to_mm ** 2 * self.columns[0].F))
        if axial_ratio_x <= 0.5:#軸力比を考慮した全塑性曲げモーメントの低下率の算定
            reduction_ratio_x = 1-4*axial_ratio_x**2/3.0
        else:
            reduction_ratio_x = 4*(1-axial_ratio_x)/3.0
        self.assertGreater(self.columns[0].Mpx*reduction_ratio_x,tarbeam_Mp)#柱梁耐力比が1以上ならOK

if __name__ == '__main__':
    unittest.main()