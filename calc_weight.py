from member_class import *
import math
import yaml

#層重量、地震荷重の算定
def calc_layer_weight(beams,columns,layers,maximum_height):
    #df1 = pd.read_excel("input_model.xlsx", sheet_name="Story_shear", header=0)
    df1 = pd.read_csv("./make_sample_model/input_layers.csv", header=0)

    #地震荷重算定用パラメータに関するyamlファイルの読み込み
    file_path = "calc_condition.yaml"

    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    manual_T=0
    if data:
        St_type = data.get('StructuralType')
        manual_T = data.get('Manual_T')
        C0 = data.get('Baseshear')
        Tc = data.get('Tc')
        Z = data.get('Z')
    else:
        print("calclation condition can not be read.")

    #層重量の算定(とりあえず鹿島様のPPT p.3の通りに実装した）
    #内部計算した部材自重の扱いについては鹿島様要相談
    temp = 0
    temp1 = 0;temp2 = 0
    temp_seismic = 0
    for i in range(len(layers)):
        if i == 0:
            layers[i].weight_floor = layers[i].omega1 * layers[i].floor_area
            layers[i].weight_wall = layers[i].omega2 * layers[i].height/2.0 * layers[i].outerwall_length#最上階
            layers[i].weight = layers[i].weight_floor+ layers[i].weight_wall#最上階
            layers[i].weight_seismic = layers[i].omega1_seismic * layers[i].floor_area + layers[i].omega2_seismic * layers[
                i].height / 2.0 * layers[i].outerwall_length  # 最上階
        else:
            layers[i].weight_floor = layers[i].omega1 * layers[i].floor_area
            layers[i].weight_wall = layers[i].omega2 * (layers[i].height+layers[i-1].height)/2.0 * layers[i].outerwall_length
            layers[i].weight = layers[i].weight_floor + layers[i].weight_wall
            layers[i].weight_seismic = layers[i].omega1_seismic * layers[i].floor_area + layers[i].omega2_seismic * \
                               (layers[i].height+layers[i-1].height)/2.0 * layers[i].outerwall_length

        temp += layers[i].weight #上から層重量を足す
        temp1 += layers[i].weight_floor #上から層重量を足す
        temp2 += layers[i].weight_wall #上から層重量を足す
        temp_seismic += layers[i].weight_seismic
        layers[i].cum_weight = temp
        layers[i].cum_weight_floor = temp1
        layers[i].cum_weight_wall = temp2
        layers[i].cum_weight_seismic = temp_seismic

    #1次固有周期の算定
    if St_type == 'Steel':
        T = 0.03*maximum_height
    elif St_type == 'RC':
        T = 0.02*maximum_height

    if manual_T != 0:
        T = manual_T

    #振動特性係数Rtの算定
    if T < Tc:
        Rt = 1
    elif Tc <= T and T<2*Tc:
        Rt = 1-0.2*(T/Tc-1)**2
    elif 2*Tc <= T:
        Rt =1.6*Tc/T

    #地震荷重の算定
    for i in range(len(layers)):
        layers[i].alpha_i = layers[i].cum_weight_seismic / layers[len(layers)-1].cum_weight_seismic
        layers[i].Ai = 1+ (1/math.sqrt(layers[i].alpha_i)-layers[i].alpha_i)*2*T/(1+3*T)
        layers[i].Ci = Z * Rt * layers[i].Ai * C0
        layers[i].Qi = layers[i].Ci * layers[i].cum_weight_seismic

    #各層柱の長期軸力の仮定
    # 外部計算した各柱の負担面積の比率に基づいて、各層の層重量を分担
    for column in columns:
        column.N_Lx = layers[len(layers)-column.story].cum_weight_floor \
                      * column.load_area / layers[len(layers)-column.story].floor_area \
        + layers[len(layers)-column.story].cum_weight_wall \
        * column.wall_load_length / layers[len(layers)-column.story].outerwall_length
        column.N_Ly = layers[len(layers)-column.story].cum_weight_floor * column.load_area \
                      / layers[len(layers)-column.story].floor_area \
        + layers[len(layers)-column.story].cum_weight_wall \
        * column.wall_load_length / layers[len(layers)-column.story].outerwall_length