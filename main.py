from calc_stress import *
from member_class import *
from set_initial_section import *
from calc_weight import *

## メイン関数 ##
if __name__ == "__main__":

#計算における定数の設定
    EE= 205000000 #鋼材のヤング係数

#データの読み込み
    nodes, beams, columns, layers, maximum_height = read_model()

#初期仮定断面の設定
    set_initial_section(beams, columns,maximum_height)

#層重量の算定
    calc_layer_weight(beams,columns,layers,maximum_height)

#部材の接合状況を把握
    detect_connection(nodes,beams,columns)

#固定モーメント法
    fixed_moment_method(nodes,beams,columns,EE)

#D値法
    #X方向
    D_method(nodes,layers,beams,columns,EE)

    for i in columns:
        print(i.M_Sx,i.M_Sy)
