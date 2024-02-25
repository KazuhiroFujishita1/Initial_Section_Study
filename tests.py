

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
        self.maximum_height = 0.0

    def prepare(self, step):

        self.nodes = [
            Node(1, 0.0, 0.0, 0.0, ''),
            Node(2, 6.0, 0.0, 0.0, ''),
            Node(3, 0.0, 0.0, 3.0, ''),
            Node(4, 6.0, 0.0, 3.0, ''),
            Node(5, 0.0, 6.0, 0.0, ''),
            Node(6, 6.0, 6.0, 0.0, ''),
            Node(7, 0.0, 6.0, 3.0, ''),
            Node(8, 6.0, 6.0, 3.0, ''),
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
            Beam(1, 3, 4, beam_length, dist_load, beam_load_i, beam_load_j, category, 'Y', phi, phi2, M0, Q0, 1, 'fix', 'fix'),
            Beam(2, 7, 8, beam_length, dist_load, beam_load_i, beam_load_j, category, 'Y', phi, phi2, M0, Q0, 2, 'fix', 'fix'),
            Beam(3, 3, 7, beam_length, dist_load, beam_load_i, beam_load_j, category, 'X', phi, phi2, M0, Q0, 1, 'fix', 'fix'),
            Beam(4, 4, 8, beam_length, dist_load, beam_load_i, beam_load_j, category, 'X', phi, phi2, M0, Q0, 2, 'fix', 'fix')
        ] 
        column_length = 3.0
        load_area = 20.0
        self.columns = [
            Column(1, 1, 3, 1, column_length, load_area),
            Column(2, 2, 4, 1, column_length, load_area),
            Column(3, 5, 7, 1, column_length, load_area),
            Column(4, 6, 8, 1, column_length, load_area)
        ]

        floor_area = 36.0
        outer_wall_length = 24.0
        self.layers = [
            Layer(1, 3.0, 7.65, 1.0, 7.3, 1.0, floor_area, outer_wall_length)
        ] 

        maximum_height = 3.0

        calc_layer_weight(self.beams, self.columns, self.layers, maximum_height)
        
        if step < self.TO_DETECT_CONNECTION: 
            return

        detect_connection(self.nodes, self.beams, self.columns)

        if step < self.TO_INITIAL_SECTION: 
            return

        beam_select_mode = "design"
        set_initial_section(self.nodes, self.beams, self.columns, maximum_height, beam_select_mode)

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
        
        #大梁断面の更新
        update_beam_section(self.nodes, self.beams, self.beam_select_mode, EE)
        
        #柱断面の更新
        update_column_section(self.nodes, self.beams, self.columns, self.layers, EE)


        return
    
    def test_before_detect_connection(self):
        self.prepare(self.TO_CALC_WEIGHT)

        y_beams = filter(lambda b: b.direction == "Y", self.beams)
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

    def test_initial_section(self):
        self.prepare(self.TO_INITIAL_SECTION)
        self.assertTrue(False)

    def test_fixed_moment(self):
        self.prepare(self.TO_FIXED_MOMENT_METHOD)

        # モーメント
        column1 = self.columns[0]
        beam1   = self.beams[0]

        # 節点周りのモーメントが釣り合うか？
        self.assertAlmostEqual(0.0, column1.M_Ly[1] + beam1.M_Ly[0], places=2)

        # 撓みの計算が適切か？

        # TODO




    def test_D_method(self):
        self.prepare(self.TO_D_METHOD)
        self.assertTrue(False)

    #def test_update_beam_section(self):
    #    self.prepare(self.TO_D_UPDATE_SECTION)
    #    self.assertTrue(False)

    #def test_update_column_section(self):
    #    self.prepare(self.TO_D_UPDATE_SECTION)
    #    self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()