from calc_stress import *
from member_class import *
from set_initial_section import *
from calc_weight import *
from update_section import *
from output_section_data import *

## メイン関数 ##
if __name__ == "__main__":

#計算における定数の設定
    EE= 205000000 #鋼材のヤング係数
    beam_select_mode = "cost" #梁リストの選定モード(cost or design)

#データの読み込み
    nodes, beams, columns, layers, maximum_height = read_model()

#層重量の算定
    calc_layer_weight(beams,columns,layers,maximum_height)

#部材の接合状況を把握
    detect_connection(nodes,beams,columns)

#初期仮定断面の設定
    beam_groups,column_groups = set_initial_section(nodes,beams, columns,maximum_height,beam_select_mode)

    for i in column_groups:
        print(i.group_name,i.ID)
#固定モーメント法
    fixed_moment_method(nodes,beams,columns,EE)

#D値法
    D_method(nodes,layers,beams,columns,EE)

#柱梁の長期・短期荷重まとめ
    load_calc(beams,columns)

#大梁断面の更新
    update_beam_section(nodes,beams,beam_select_mode)

#柱断面の更新
    update_column_section(nodes, beams, columns, layers, EE)

#選定断面の出力
    output_section_data(columns,beams,beam_select_mode)