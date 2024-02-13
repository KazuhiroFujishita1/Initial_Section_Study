
from calc_stress import *
from member_class import *
from set_initial_section import *
from calc_weight import *
from update_section import *
from output_section_data import *
import yaml

def start():
    EE= 205000000 #鋼材のヤング係数
# 計算条件に関するyamlファイルの読み込み
    file_path = "calc_condition.yaml"
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    if data:
        beam_select_mode = data.get('CalcCondition')
    else:
        print("calclation condition can not be read.")

#データの読み込み
    nodes, beams, columns, layers, maximum_height = read_model()

#層重量の算定
    calc_layer_weight(beams,columns,layers,maximum_height)

#部材の接合状況を把握
    detect_connection(nodes,beams,columns)

#初期仮定断面の設定
    beam_groups,column_groups = \
        set_initial_section(nodes,beams, columns, maximum_height,beam_select_mode)

#固定モーメント法
    fixed_moment_method(nodes,beams,columns,EE)

#D値法
    D_method(nodes,layers,beams,columns,EE)

#柱梁の長期・短期荷重まとめ
    load_calc(beams,columns)

#大梁断面の更新
    update_beam_section(nodes,beams,beam_select_mode,EE)

#柱断面の更新
    update_column_section(nodes, beams, columns, layers, EE)

#選定断面の出力
    output_section_data(columns,beams,beam_select_mode)

#全データの出力
    output_whole_data(columns,beams,nodes,layers)

    return nodes, beams, columns, layers, maximum_height