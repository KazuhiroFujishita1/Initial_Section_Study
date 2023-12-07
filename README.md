# Initial_Section_Study

以下、ファイルの構成に関する簡単な説明を記載します。    

## プログラムの構成  
main.py：メインプログラム  
member_class.py：部材変数を整理したクラス  
set_initial_section.py：初期仮定断面を設定するプログラム  
calc_stress.py：固定モーメント法、D値法により部材応力を算定するプログラム  
calc_weight.py：重量、地震荷重などの算定関連  
update_section.py:応力算定結果などに基づく断面更新プログラム  

## インプットファイル
input_model.xlsx：対象モデルの諸元に関する入力ファイル  
input_load_condition.yaml：地震荷重算定などのパラメータ入力ファイル  
＜内部計算用＞  
column_list.csv、beam_list.csv：柱梁部材リストを暫定的に作成(梁リストについてはコスパ、デザインのものを全て入れた）   
y0_table.csv、y1_table.csv、y2_table.csv：反曲点高比の算定用シート  

## アウトプットファイル
output_section_cost.csv : 梁リストの選定基準をコストとした場合に選定される柱梁断面リスト  
output_section_design.csv：梁リストの選定基準をデザインとした場合に選定される断面リスト  

