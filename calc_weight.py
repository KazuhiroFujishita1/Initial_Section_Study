from member_class import *
import math

#層重量、地震荷重の算定
def calc_layer_weight(beams,columns,layers,maximum_height):
    df1 = pd.read_excel("input_model.xlsx", sheet_name="Story_shear", header=0)

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
    T = 0.03*maximum_height
    #ベースシア係数の仮定
    C0 = 0.2
    #振動特性係数Rtの算定
    Rt = 1 #軟弱地盤の影響は考慮しない
    #地域係数Zの算定
    Z = 1 #地域係数による影響は考慮しない

    #地震荷重の算定
    for i in range(len(layers)):
        layers[i].alpha_i = layers[i].cum_weight / layers[len(layers)-1].cum_weight
        layers[i].Ai = 1+ (1/math.sqrt(layers[i].alpha_i)-layers[i].alpha_i)*2*T/(1+3*T)
        layers[i].Ci = Z * Rt * layers[i].Ai * C0
        layers[i].Qi = layers[i].Ci * layers[i].cum_weight


