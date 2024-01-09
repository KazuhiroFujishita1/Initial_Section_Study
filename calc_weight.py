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

    if data:
        St_type = data.get('StructuralType')
        C0 = data.get('Baseshear')
        Rt = data.get('Rt')
        Z = data.get('Z')
    else:
        print("calclation condition can not be read.")

    #層重量の算定(とりあえず鹿島様のPPT p.3の通りに実装した）
    #内部計算した部材自重の扱いについては鹿島様要相談
    temp = 0
    for i in range(len(layers)):
        if i == 0:
            layers[i].weight = layers[i].omega1_seismic * layers[i].floor_area + layers[i].omega2_seismic * layers[i].height/2.0 * layers[i].outerwall_length#最上階
        else:
            layers[i].weight = layers[i].omega1_seismic * layers[i].floor_area + layers[i].omega2_seismic * \
                               (layers[i].height+layers[i-1].height)/2.0 * layers[i].outerwall_length
        temp += layers[i].weight #上から層重量を足す
        layers[i].cum_weight = temp

    #1次固有周期の算定
    if St_type == 'Steel':
        T = 0.03*maximum_height
    elif St_type == 'RC':
        T = 0.02*maximum_height

    #地震荷重の算定
    for i in range(len(layers)):
        layers[i].alpha_i = layers[i].cum_weight / layers[len(layers)-1].cum_weight
        layers[i].Ai = 1+ (1/math.sqrt(layers[i].alpha_i)-layers[i].alpha_i)*2*T/(1+3*T)
        layers[i].Ci = Z * Rt * layers[i].Ai * C0
        layers[i].Qi = layers[i].Ci * layers[i].cum_weight

    #各層柱の長期軸力の仮定
    # 外部計算した各柱の負担面積の比率に基づいて、各層の層重量を分担
    for column in columns:
        column.N_Lx = layers[len(layers)-column.story].cum_weight * column.load_area / layers[len(layers)-column.story].floor_area
        column.N_Ly = layers[len(layers)-column.story].cum_weight * column.load_area / layers[len(layers)-column.story].floor_area

