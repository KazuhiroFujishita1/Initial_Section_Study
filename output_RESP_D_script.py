import csv
import json
import yaml
import pandas as pd

def output_RESP_D_script(columns,beams,beam_select_mode,nodes,layers,column_groups,beam_groups,frames):
    #設定yamlファイルの読み込み
    with open("generate_JSON_condition.yaml", 'r') as yml_file:
        input_data = yaml.safe_load(yml_file)

    # csvファイル名
    output_file_column_csv = input_data['Output_file_column_name']
    output_file_girder_csv = input_data['Output_file_girder_name']

#RESP-D向けの部材グルーピング出力
    #層方向の関係にある梁部材抽出
    data_for_sort=[]
    for beam in beams:
        data_for_sort.append([beam.no,beam.story,beam.group_name,nodes[beam.i-1].x,nodes[beam.i-1].y,
                              nodes[beam.j-1].x,nodes[beam.j-1].y])
    sort_beam = pd.DataFrame(data_for_sort)
    sorted_beam = sort_beam.sort_values(by=[3,4,5])
    mark=[]
    count=1
    for i in range(len(sorted_beam)):
        if i == len(sorted_beam)-1:
            mark.append("G" + str(count))
        if i != 0:
            if sorted_beam.iloc[i-1][3] == sorted_beam.iloc[i][3] and sorted_beam.iloc[i-1][4] == sorted_beam.iloc[i][4] \
                    and sorted_beam.iloc[i-1][5] == sorted_beam.iloc[i][5]:
                mark.append("G"+str(count))
            else:
                mark.append("G"+str(count))
                count+= 1
    sorted_beam["mark"]=mark #層方向に並ぶ部材に同じマークを付ける
    #マークごとに符号確認
    test_mark = sorted(set(mark), key=lambda x: int(x[1:]))
    i=0
    while i < len(test_mark):
        j=0
        test1 = sorted_beam[sorted_beam["mark"] == test_mark[i]]
        while j < len(test_mark):
            test2 = sorted_beam[sorted_beam["mark"] == test_mark[j]]
            if test_mark[i] != test_mark[j]:#自分自身以外と比較
                if all(x == y for x, y in zip(list(test1[2]), list(test2[2]))) and len(test1) == len(test2):#比較対象のグループ項目がすべて同じ場合書き換える
                    sorted_beam.loc[sorted_beam["mark"] == test_mark[j], "mark"] = test_mark[i]
                    sorted_beam.loc[sorted_beam["mark"] == test_mark[i], "mark"] = test_mark[i]
                    count += 1
            j+=1
        i+= 1

    #層方向の関係にある柱部材抽出
    data_for_sort=[]
    for column in columns:
        data_for_sort.append([column.no,column.story,column.group_name,nodes[column.i-1].x,nodes[column.i-1].y])
    sort_column = pd.DataFrame(data_for_sort)
    sorted_column = sort_column.sort_values(by=[3,4])
    mark=[]
    count=1
    for i in range(len(sorted_column)):
        if i == len(sorted_column)-1:
            mark.append("C" + str(count))
        if i != 0:
            if sorted_column.iloc[i-1][3] == sorted_column.iloc[i][3] and sorted_column.iloc[i-1][4] == sorted_column.iloc[i][4]:
                mark.append("C"+str(count))
            else:
                mark.append("C"+str(count))
                count+= 1
    sorted_column["mark"]=mark #層方向に並ぶ部材に同じマークを付ける
    #マークごとに符号確認
    test_mark = sorted(set(mark), key=lambda x: int(x[1:]))
    i=0
    while i < len(test_mark):
        j=0
        test1 = sorted_column[sorted_column["mark"] == test_mark[i]]
        while j < len(test_mark):
            test2 = sorted_column[sorted_column["mark"] == test_mark[j]]
            if test_mark[i] != test_mark[j]:#自分自身以外と比較
                if all(x == y for x, y in zip(list(test1[2]), list(test2[2]))) and len(test1) == len(test2):#比較対象のグループ項目がすべて同じ場合書き換える
                    sorted_column.loc[sorted_column["mark"] == test_mark[j], "mark"] = test_mark[i]
                    sorted_column.loc[sorted_column["mark"] == test_mark[i], "mark"] = test_mark[i]
                    count += 1
            j+=1
        i+= 1

    #使っている柱梁グループ名の抽出
    rec_column_mark=[]
    rec_beam_mark=[]
    for i in sorted_column["mark"]:
        rec_column_mark.append(i)
    rec_column_mark = set(rec_column_mark)
    for i in sorted_beam["mark"]:
        rec_beam_mark.append(i)
    rec_beam_mark = set(rec_beam_mark)

    for column_flag in rec_column_mark:
        temp = sorted_column[sorted_column["mark"] == column_flag]
        column_no = list(temp[0])
        column_mark = list(temp['mark'])
        column_story = list(temp[1])
        for i in range(len(column_mark)):
            columns[column_no[i]-1].group_name_for_RESP = column_mark[i]#整理したグループ名を柱クラスに登録
    for beam_flag in rec_beam_mark:
        temp = sorted_beam[sorted_beam["mark"] == beam_flag]
        beam_no = list(temp[0])
        beam_mark = list(temp['mark'])
        beam_story = list(temp[1])
        for i in range(len(beam_mark)):
            beams[beam_no[i]-1].group_name_for_RESP = beam_mark[i]#整理したグループ名を梁クラスに登録

    # csvファイルにデータを書き込む
    #柱グループ諸元の出力
    group_output_column = pd.DataFrame()
    for column in columns:
        if column.F == 295:
            if column.H <= 550:  # 柱せい550mm以下はBCR
                temp_text = "BCR295"  # F値が235ならSS400
            elif column.H > 550:  # 柱せい550mmを超える場合BCP
                temp_text = "BCP295"
            else:
                temp_text = "Error"
        elif column.F == 325:
            temp_text = "BCP325"  # F値が325ならBCP325
        else:
            temp_text = "Error"

        new_row_data={
            "//Floor" : str(column.story) + str("F"),
            "Mark" : column.group_name_for_RESP,
            "Shape" : "Box",
            "H" : column.H,
            "B" : column.H,
            "tw" : column.t,
            "tf" : column.t,
            "r" : column.r,
            "MAT" : temp_text
        }

        group_output_column = group_output_column.append(new_row_data, ignore_index=True)

    group_output_column = group_output_column.drop_duplicates()#重複データを削除
    group_output_column = group_output_column.sort_values(by=["Mark","//Floor"])  # データをソート
    group_output_column.to_csv(output_file_column_csv+".csv", index=False)#柱断面リストをcsv出力

    # #梁グループ諸元の出力
    # #対象架構の最上層の検出
    max_story_name = str(len(layers)+1) +"F"

    group_output_beam = pd.DataFrame()
    for beam in beams:
        if beam.F == 235:
            temp_text = "SS400"  # F値が235ならSS400
        elif beam.F == 325:
            temp_text = "SM490"  # F値が325ならSM490
        else:
            temp_text = "Error"

        if str(beam.story) + str("F") != max_story_name:
            story_name = str(beam.story) + str("F")
        else:
            story_name = "RF"

        new_row_data = {
            "//Floor": story_name,
            "Mark": beam.group_name_for_RESP,
            "Shape": "H",
            "H": beam.H,
            "B": beam.B,
            "tw": beam.t1,
            "tf": beam.t2,
            "r": beam.r,
            "MAT": temp_text
        }

        group_output_beam = group_output_beam.append(new_row_data, ignore_index=True)

    group_output_beam = group_output_beam.drop_duplicates()  # 重複データを削除
    group_output_beam = group_output_beam.sort_values(by=["Mark", "//Floor"])  # データをソート
    group_output_beam = group_output_beam[group_output_beam["MAT"] != "Error"]  #"MAT"がErrorとなっているデータを除外（基礎梁）
    group_output_beam.to_csv(output_file_girder_csv + ".csv", index=False)  # 梁断面リストをcsv出力

    #jsonファイル出力

    # #節点のインプットデータに構面情報が定義されていない場合直交座標系を仮定して、各節点へ構面を割り当て(一旦キャンセル）
    # #各構面に関するデータ整理
    # #X方向構面
    # #重複座標を削除
    # X_axis=[];Y_axis=[];Z_axis=[]
    # X_axis_name=[];Y_axis_name=[];Z_axis_name=[]
    # for node in nodes:
    #     X_axis.append(round(node.x,3))
    #     Y_axis.append(round(node.y,3))
    #     Z_axis.append(round(node.z,3))
    # X_axis = set(X_axis)
    # Y_axis = set(Y_axis)
    # Z_axis = set(Z_axis)
    # X_axis = sorted(X_axis,reverse=True)
    # Y_axis = sorted(Y_axis,reverse=True)
    # Z_axis = sorted(Z_axis,reverse=True)
    # X_axis_diff=[];Y_axis_diff=[];Z_axis_diff=[]
    #
    # #構面間座標の算定
    # if len(X_axis) > 2:
    #     for no in range(len(X_axis)-1):
    #         X_axis_diff.append(X_axis[no]-X_axis[no+1])
    #         X_axis_name.append("X"+str(len(X_axis)-no))
    #     X_axis_diff.append(0)
    #     X_axis_name.append("X1")
    # elif len(X_axis)<=2:
    #     for no in range(len(X_axis)):
    #         X_axis_diff.append(X_axis[no])
    #         X_axis_name.append("X"+str(len(X_axis)-no))
    # if len(Y_axis) > 2:
    #     for no in range(len(Y_axis)-1):
    #         Y_axis_diff.append(Y_axis[no] - Y_axis[no+1])
    #         Y_axis_name.append("Y"+str(len(Y_axis)-no))
    #     Y_axis_diff.append(0)
    #     Y_axis_name.append("Y1")
    # elif len(Y_axis) <= 2:
    #     for no in range(len(Y_axis)):
    #         Y_axis_diff.append(Y_axis[no])
    #         Y_axis_name.append("Y"+str(len(X_axis)-no))
    # if len(Z_axis) > 2:
    #     for no in range(len(Z_axis)-1):
    #         Z_axis_diff.append(Z_axis[no] - Z_axis[no+1])
    #         if str(len(Z_axis)-no)+"F" != max_story_name:
    #             Z_axis_name.append(str(len(Z_axis)-no)+"F")
    #         elif str(len(Z_axis)-no)+"F" == max_story_name:
    #             Z_axis_name.append("RF")
    #     Z_axis_diff.append(0)
    #     Z_axis_name.append("1F")
    # elif len(Z_axis) <= 2:
    #     for no in range(len(Z_axis)):
    #         Z_axis_diff.append(Z_axis[no])
    #         Z_axis_name.append("Z" + str(len(Z_axis) - no))
    #
     #jsonファイルの書き出し
    dict = {"Model":{}}#jsonのベースディクショナリ
    #
    # #構面情報の代入
    # X_frame = [];Y_frame = [];Z_frame = []
    # for axis_x_no in range(len(X_axis_name)):
    #     x_axis_info = {}
    #     x_axis_info["Name"] = X_axis_name[len(X_axis_name)-axis_x_no-1]
    #     x_axis_info["RelativePosition"] = round(X_axis_diff[len(X_axis_name)-axis_x_no-1],3)
    #     X_frame.append(x_axis_info)
    # for axis_y_no in range(len(Y_axis_name)):
    #     y_axis_info = {}
    #     y_axis_info["Name"] = Y_axis_name[len(Y_axis_name)-axis_y_no-1]
    #     y_axis_info["RelativePosition"] = round(Y_axis_diff[len(Y_axis_name)-axis_y_no-1],3)
    #     Y_frame.append(y_axis_info)
    # for axis_z_no in range(len(Z_axis_name)):
    #     z_axis_info = {}
    #     z_axis_info["Name"] = Z_axis_name[len(Z_axis_name)-axis_z_no-1]
    #     z_axis_info["RelativeHeight"] = round(Z_axis_diff[len(Z_axis_name)-axis_z_no-1],3)
    #     Z_frame.append(z_axis_info)
    # dict["Model"]["Yframes"] = X_frame
    # dict["Model"]["Xframes"] = Y_frame
    # dict["Model"]["Stories"] = Z_frame

    #構面情報の代入
    X_frame=[];Y_frame=[];Z_frame=[]
    for frame in frames:
        if frame.category == "X":#Y方向構面の場合
            y_axis_info = {}
            y_axis_info["Name"] = frame.frame_name
            y_axis_info["RelativePosition"] = frame.re_pos_x
            Y_frame.append(y_axis_info)
        elif frame.category == "Y": #X方向構面の場合
            x_axis_info = {}
            x_axis_info["Name"] = frame.frame_name
            x_axis_info["RelativePosition"] = frame.re_pos_y
            X_frame.append(x_axis_info)
        elif frame.category == "Z": #Z方向構面の場合
            z_axis_info = {}
            z_axis_info["Name"] = frame.frame_name
            z_axis_info["RelativePosition"] = frame.re_pos_z
            Z_frame.append(z_axis_info)
    dict["Model"]["Yframes"] = X_frame
    dict["Model"]["Xframes"] = Y_frame
    dict["Model"]["Stories"] = Z_frame
    #
    # X_frame_dict = {};Y_frame_dict = {};Z_frame_dict = {}
    # for temp in range(len(X_axis)):
    #     X_frame_dict[X_axis[temp]] = X_axis_name[temp]
    # for temp in range(len(Y_axis)):
    #     Y_frame_dict[Y_axis[temp]] = Y_axis_name[temp]
    # for temp in range(len(Z_axis)):
    #     Z_frame_dict[Z_axis[temp]] = Z_axis_name[temp]

    #節点情報のリスト化・代入
    # node_info = []
    # for node in nodes:
    #     temp = {}
    #     temp["Id"] = int(node.no)
    #     temp["Floor"] = str(Z_frame_dict[node.z])
    #     temp["AxisX"] = str(X_frame_dict[node.x])
    #     temp["AxisY"] = str(Y_frame_dict[node.y])
    #     temp["X"] = node.x
    #     temp["Y"] = node.y
    #     temp["Z"] = node.z
    #     node_info.append(temp)
    node_info = []
    for node in nodes:
        temp = {}
        temp["Id"] = int(node.no)
        temp["Floor"] = node.floor
        temp["AxisX"] = node.axisX
        temp["AxisY"] = node.axisY
        temp["X"] = node.x
        temp["Y"] = node.y
        temp["Z"] = node.z
        node_info.append(temp)

    dict["Model"]["MemberArrangement"] = {}
    dict["Model"]["MemberArrangement"]["Nodes"] = node_info

    #柱情報のリスト化・代入
    column_info = []
    for column in columns:
        temp = {}
        temp["BottomNodeId"] = int(column.i)
        temp["TopNodeId"] = int(column.j)
        temp["Mark"] = column.group_name_for_RESP
        column_info.append(temp)

    dict["Model"]["MemberArrangement"]["Columns"] = column_info

    # 梁情報のリスト化・代入
    beam_info = []
    for beam in beams:
        if beam.category != "BB":#基礎梁以外をモデルデータとして出力
            temp = {}
            temp["StartNodeId"] = int(beam.i)
            temp["EndNodeId"] = int(beam.j)
            temp["Mark"] = beam.group_name_for_RESP
            beam_info.append(temp)

    dict["Model"]["MemberArrangement"]["Girders"] = beam_info

    #モデル各種構造諸元の代入
    dict["Model"]["StructureType"] = "S"
    dict["Model"]["SteelStructureCondition"] = {"ColumnBaseType":"Fix"}
    dict["Model"]["MarkRules"] = []#一旦markrulesの代入は保留（よくわからない）

    #外壁荷重リストの出力
    wall_load_mark = []; wall_load_weight= []
    for i in range(len(input_data['Load']['OuterwallLoadList'])):
        wall_load_mark.append(input_data['Load']['OuterwallLoadList'][i]['Mark'])
        wall_load_weight.append(input_data['Load']['OuterwallLoadList'][i]['Weight'])
    wall_load_data = pd.DataFrame({'//Mark': wall_load_mark, 'Weight(N/m2)': wall_load_weight})
    wall_load_data.to_csv("outer-wall-load.csv", index=False)

    #荷重情報の入力
    dict["Load"]={}
    dict["Load"]["OuterwallLoadListPath"] = input_data['Load']['OuterwallLoadListPath']
    dict["Load"]["OuterWalls"] = input_data['Load']['OuterWalls']

    #スラブ荷重リストの出力
    slab_load_mark = []; slab_load_name = []; slab_load_slab_T = []
    slab_load_unit_weight = [];slab_load_DL = [];slab_load_LL1 = [];
    slab_load_LL2 = [];slab_load_LL3 = [];slab_load_LL4 = []
    slab_load_snow = []
    for i in range(len(input_data['Load']['SlabLoadList'])):
        slab_load_mark.append(input_data['Load']['SlabLoadList'][i]['Mark'])
        slab_load_name.append(input_data['Load']['SlabLoadList'][i]['Name'])
        slab_load_slab_T.append(input_data['Load']['SlabLoadList'][i]['SlabT'])
        slab_load_unit_weight.append(input_data['Load']['SlabLoadList'][i]['WeightPerVol'])
        slab_load_DL.append(input_data['Load']['SlabLoadList'][i]['DL'])
        slab_load_LL1.append(input_data['Load']['SlabLoadList'][i]['LL1'])
        slab_load_LL2.append(input_data['Load']['SlabLoadList'][i]['LL2'])
        slab_load_LL3.append(input_data['Load']['SlabLoadList'][i]['LL3'])
        slab_load_LL4.append(input_data['Load']['SlabLoadList'][i]['LL4'])
        slab_load_snow.append(input_data['Load']['SlabLoadList'][i]['Snow'])

    slab_load_data = pd.DataFrame({'//Mark': slab_load_mark, 'Name': slab_load_name, 'SlabT(mm)': slab_load_slab_T,
                                   'WeightPerVol(kN/m3)': slab_load_unit_weight, 'DL(N/m2)': slab_load_DL, 'LL1(N/m2)': slab_load_LL1,
                                   'LL2(N/m2)': slab_load_LL2, 'LL3(N/m2)': slab_load_LL3, 'LL4(N/m2)': slab_load_LL4,
                                   'Snow': slab_load_snow})
    slab_load_data.to_csv("slab-load.csv", index=False)

    #スラブ荷重
    dict["Load"]["SlabLoadListPath"] = input_data['Load']['SlabLoadListPath']
    dict["Load"]["SlabLoads"] = input_data['Load']['SlabLoads']

    #断面選定方針
    dict["SelectionStrategy"] = {}
    dict["SelectionStrategy"]["Margin"] = input_data['Margin']
    dict["SelectionStrategy"]["BaseplateListPath"] = input_data['BaseplateListPath']
    dict["SelectionStrategy"]["ConvergencePriority"] = input_data['ConvergencePriority']
    dict["SelectionStrategy"]["Sections"] = input_data['SelectionStrategy']["Sections"]

    with open('generator_case1.json', 'w') as f:
        json.dump(dict,f, indent=2)


