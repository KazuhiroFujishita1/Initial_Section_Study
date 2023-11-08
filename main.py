from calc_stress import *
from member_class import *
from set_initial_section import *

## メイン関数 ##
if __name__ == "__main__":

#計算における定数の設定
    EE= 205000000 #鋼材のヤング係数

#初期仮定断面の設定
    beam = Beam()  # 初期インスタンスの呼び出し
    column = Column()
    member = Member()
    layer = Layer()
    column_Ix, beam_Ix = set_initial_section(beam,column,layer)

#固定モーメント法
    #X方向
    beam.call_x_dir()#X方向の諸元を呼び出し
    column.call_x_info()
    member.call_x_dir()

    moment_x_long, shear_x_long, member_no_each_node_x = fixed_moment_method(beam.no_all,beam,column,member,EE)

    # Y方向
    beam.call_y_dir()#Y方向の諸元を呼び出し
    column.call_y_info()
    member.call_y_dir()
    moment_y_long, shear_y_long, member_no_each_node_y = fixed_moment_method(beam.no_all,beam,column,member,EE)
    print(moment_y_long)

#D値法
    #X方向
    beam.call_x_dir()#X方向の諸元を呼び出し
    column.call_x_info()
    member.call_x_dir()
    layer.call_x_dir()
    moment_x_short, shear_x_short, axial_x_short = D_method(member_no_each_node_x,layer,beam,column,member)
    print(moment_x_short)

    #Y方向
    beam.call_y_dir()#Y方向の諸元を呼び出し
    column.call_y_info()
    member.call_y_dir()
    layer.call_y_dir()
    moment_y_short, shear_y_short, axial_y_short = D_method(member_no_each_node_y,layer,beam,column,member)