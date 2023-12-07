from member_class import *
import math
import yaml

#層重量、地震荷重の算定
def calc_layer_weight(beams,columns,layers,maximum_height):
    df1 = pd.read_excel("input_model.xlsx", sheet_name="Story_shear", header=0)

    #地震荷重算定用パラメータに関するyamlファイルの読み込み
    file_path = "input_load_condition.yaml"

    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    if data:
        St_type = data.get('StructuralType')
        C0 = data.get('Baseshear')
        Rt = data.get('Rt')
        Z = data.get('Z')
    else:
        print("load_condition can not be read.")

    #層重量の算定(とりあえず鹿島様のPPT p.3の通りに実装した）
    #内部計算した部材自重の扱いについては鹿島様要相談
    temp = 0
    for i in range(len(layers)):
        if i == 0:
            layers[i].weight = layers[i].omega1 * layers[i].floor_area + layers[i].omega2 * layers[i].height/2#最上階
        else:
            layers[i].weight = layers[i].omega1 * layers[i].floor_area + layers[i].omega2 * (layers[i].height+layers[i-1].height)/2
        temp += layers[i].weight #上から層重量を足す
        layers[i].cum_weight = temp

    #1次固有周期の算定
    if St_type == 'Steel':
        T = 0.03*maximum_height
    elif St_type == 'Concrete':
        T = 0.02*maximum_height

    #地震荷重の算定
    for i in range(len(layers)):
        layers[i].alpha_i = layers[i].cum_weight / layers[len(layers)-1].cum_weight
        layers[i].Ai = 1+ (1/math.sqrt(layers[i].alpha_i)-layers[i].alpha_i)*2*T/(1+3*T)
        layers[i].Ci = Z * Rt * layers[i].Ai * C0
        layers[i].Qi = layers[i].Ci * layers[i].cum_weight

    #各層の柱本数のカウント
    for i in range(len(layers)):
        count = 0
        for j in columns:
            if j.story == layers[i].story:
                count += 1
        layers[i].column_num = count

    #各層柱の長期軸力の仮定
    # （とりあえず層重量／柱本数で算定、鹿島様PPTの内容は各柱の負担面積を算定の上、軸力を算定している）
    for i in columns:
        i.N_Lx = layers[len(layers)-i.story].cum_weight/layers[len(layers)-i.story].column_num
        i.N_Ly = layers[len(layers)-i.story].cum_weight/layers[len(layers)-i.story].column_num

