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
column_list.csv、beam_list.csv：柱梁部材リストを暫定的に作成  
(梁リストについてはコスパ、デザインのものを全て入れた）   
y0_table.csv、y1_table.csv、y2_table.csv：反曲点高比の算定用シート  

## アウトプットファイル
output_section_cost.csv : 梁リストの選定基準をコストとした場合に選定される柱梁断面リスト  
output_section_design.csv：梁リストの選定基準をデザインとした場合に選定される断面リスト  

## プログラムの構成（作成中）
read_model()：input_model.xlsxより、架構形状のデータ読み込み  
→  
calc_layer_weight()：input_model.xlsx、input_load_condition.yamlより、架構荷重の入力  
→  
detect_connection()：読み込んだ架構形状より、各部材の接続関係をリスト化  
→  
set_initial_section()：初期仮定断面の設定  
　柱：建物の全体階高と長期の柱軸力比より決定  
  梁：各梁のスパン長より決定
→  
fixed_moment_method()：固定モーメント法による長期応力算定  
→  
D_method()：D値法による地震時応力算定  
→  
load_calc()：長期・地震時応力に基づいて、長期・短期の部材応力を算定  
→  
update_beam_section()：算定応力等に基づく梁断面の更新  
　算定応力（曲げ、せん断）による検定比に基づく部材断面の更新  
　各節点における隣接する梁のダイヤフラム段差幅の確認に基づく断面更新（要チェック）  
→  
update_column_section()：算定応力等に基づく柱断面の更新  
　calc_limit_column_size()：剛性チェック、柱梁耐力比に基づく必要最低柱断面の算定と必要に応じた更新  
　update_column_thickness()：算定長期・短期応力に基づく必要柱板厚の算定と更新  
 　


