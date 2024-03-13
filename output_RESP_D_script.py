import csv
import json
import yaml

def output_RESP_D_script(columns,beams,beam_select_mode,nodes,layers,column_groups,beam_groups):
    #設定yamlファイルの読み込み
    with open("generate_JSON_condition.yaml", 'r') as yml_file:
        input_data = yaml.safe_load(yml_file)
    print(input_data)
    # csvファイル名
    output_file_column_csv = input_data['Output_file_column_name']
    output_file_girder_csv = input_data['Output_file_girder_name']

    # csvファイルにデータを書き込む

    #柱グループ諸元の出力
    with open(output_file_column_csv + '.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONE, escapechar='\\')
        writer.writerow(['//Floor', 'Mark', 'Shape', 'H', 'B', 'tw', 'tf', 'r', 'MAT'])
        for column_group in column_groups:
            if columns[column_group.ID[0] - 1].F == 295:
                if columns[column_group.ID[0] - 1].H <= 550:#柱せい550mm以下はBCR
                    temp_text = "BCR295"#F値が235ならSS400
                elif columns[column_group.ID[0] - 1].H > 550:#柱せい550mmを超える場合BCP
                    temp_text = "BCP295"
                else:
                    temp_text = "Error"
            elif columns[column_group.ID[0]-1].F == 325:
                temp_text = "BCP325"#F値が325ならBCP325
            else:
                temp_text = "Error"

            writer.writerow([str(columns[column_group.ID[0]-1].story)+str("F"),column_group.group_name,"Box",
                                 columns[column_group.ID[0]-1].H,columns[column_group.ID[0]-1].t,
                             columns[column_group.ID[0]-1].t,columns[column_group.ID[0]-1].r,temp_text])

    #梁グループ諸元の出力
    #対象架構の最上層の検出
    max_story_name = str(len(layers)+1) +"F"

    with open(output_file_girder_csv + '.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONE, escapechar='\\')
        writer.writerow(['//Floor', 'Mark', 'Shape', 'H', 'B', 'tw', 'tf', 'r', 'MAT'])
        for beam_group in beam_groups:
            if beams[beam_group.ID[0] - 1].F == 235:
                temp_text = "SS400"#F値が235ならSS400
            elif beams[beam_group.ID[0]-1].F == 325:
                temp_text = "SM490"#F値が325ならSM490
            else:
                temp_text = "Error"

            if str(beams[beam_group.ID[0]-1].story)+str("F") != max_story_name:
                writer.writerow([str(beams[beam_group.ID[0]-1].story)+str("F"),beam_group.group_name,"H",
                                 beams[beam_group.ID[0]-1].H,beams[beam_group.ID[0]-1].B,beams[beam_group.ID[0]-1].t1,
                             beams[beam_group.ID[0]-1].t2,beams[beam_group.ID[0]-1].r,temp_text])
            elif str(beams[beam_group.ID[0]-1].story)+str("F") == max_story_name:#最上層はRFとする
                writer.writerow(["RF",beam_group.group_name,"H",
                                 beams[beam_group.ID[0]-1].H,beams[beam_group.ID[0]-1].B,beams[beam_group.ID[0]-1].t1,
                             beams[beam_group.ID[0]-1].t2,beams[beam_group.ID[0]-1].r,temp_text])

    #jsonファイル出力
    #各構面に関するデータ整理
    #X方向構面
    #重複座標を削除
    X_axis=[];Y_axis=[];Z_axis=[]
    X_axis_name=[];Y_axis_name=[];Z_axis_name=[]
    for node in nodes:
        X_axis.append(round(node.x,3))
        Y_axis.append(round(node.y,3))
        Z_axis.append(round(node.z,3))
    X_axis = set(X_axis)
    Y_axis = set(Y_axis)
    Z_axis = set(Z_axis)
    X_axis = sorted(X_axis,reverse=True)
    Y_axis = sorted(Y_axis,reverse=True)
    Z_axis = sorted(Z_axis,reverse=True)
    X_axis_diff=[];Y_axis_diff=[];Z_axis_diff=[]

    #構面間座標の算定
    if len(X_axis) > 2:
        for no in range(len(X_axis)-1):
            X_axis_diff.append(X_axis[no]-X_axis[no+1])
            X_axis_name.append("X"+str(len(X_axis)-no))
        X_axis_diff.append(0)
        X_axis_name.append("X1")
    elif len(X_axis)<=2:
        for no in range(len(X_axis)):
            X_axis_diff.append(X_axis[no])
            X_axis_name.append("X"+str(len(X_axis)-no))
    if len(Y_axis) > 2:
        for no in range(len(Y_axis)-1):
            Y_axis_diff.append(Y_axis[no] - Y_axis[no+1])
            Y_axis_name.append("Y"+str(len(Y_axis)-no))
        Y_axis_diff.append(0)
        Y_axis_name.append("Y1")
    elif len(Y_axis) <= 2:
        for no in range(len(Y_axis)):
            Y_axis_diff.append(Y_axis[no])
            Y_axis_name.append("Y"+str(len(X_axis)-no))
    if len(Z_axis) > 2:
        for no in range(len(Z_axis)-1):
            Z_axis_diff.append(Z_axis[no] - Z_axis[no+1])
            if str(len(Z_axis)-no)+"F" != max_story_name:
                Z_axis_name.append(str(len(Z_axis)-no)+"F")
            elif str(len(Z_axis)-no)+"F" == max_story_name:
                Z_axis_name.append("RF")
        Z_axis_diff.append(0)
        Z_axis_name.append("1F")
    elif len(Z_axis) <= 2:
        for no in range(len(Z_axis)):
            Z_axis_diff.append(Z_axis[no])
            Z_axis_name.append("Z" + str(len(Z_axis) - no))


    #jsonファイルの書き出し
    dict = {"Model":{}}#jsonのベースディクショナリ

    #構面情報の代入
    X_frame = [];Y_frame = [];Z_frame = []
    for axis_x_no in range(len(X_axis_name)):
        x_axis_info = {}
        x_axis_info["Name"] = X_axis_name[len(X_axis_name)-axis_x_no-1]
        x_axis_info["RelativePosition"] = round(X_axis_diff[len(X_axis_name)-axis_x_no-1],3)
        X_frame.append(x_axis_info)
    for axis_y_no in range(len(Y_axis_name)):
        y_axis_info = {}
        y_axis_info["Name"] = Y_axis_name[len(Y_axis_name)-axis_y_no-1]
        y_axis_info["RelativePosition"] = round(Y_axis_diff[len(Y_axis_name)-axis_y_no-1],3)
        Y_frame.append(y_axis_info)
    for axis_z_no in range(len(Z_axis_name)):
        z_axis_info = {}
        z_axis_info["Name"] = Z_axis_name[len(Z_axis_name)-axis_z_no-1]
        z_axis_info["RelativeHeight"] = round(Z_axis_diff[len(Z_axis_name)-axis_z_no-1],3)
        Z_frame.append(z_axis_info)
    dict["Model"]["Yframes"] = X_frame
    dict["Model"]["Xframes"] = Y_frame
    dict["Model"]["Stories"] = Z_frame

    X_frame_dict = {};Y_frame_dict = {};Z_frame_dict = {}
    for temp in range(len(X_axis)):
        X_frame_dict[X_axis[temp]] = X_axis_name[temp]
    for temp in range(len(Y_axis)):
        Y_frame_dict[Y_axis[temp]] = Y_axis_name[temp]
    for temp in range(len(Z_axis)):
        Z_frame_dict[Z_axis[temp]] = Z_axis_name[temp]

    #節点情報のリスト化・代入
    node_info = []
    for node in nodes:
        temp = {}
        temp["Id"] = int(node.no)
        temp["Floor"] = str(Z_frame_dict[node.z])
        temp["AxisX"] = str(X_frame_dict[node.x])
        temp["AxisY"] = str(Y_frame_dict[node.y])
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
        temp["Mark"] = column.group_name
        column_info.append(temp)

    dict["Model"]["MemberArrangement"]["Columns"] = column_info

    # 梁情報のリスト化・代入
    beam_info = []
    for beam in beams:
        temp = {}
        temp["StartNodeId"] = int(beam.i)
        temp["EndNodeId"] = int(beam.j)
        temp["Mark"] = beam.group_name
        beam_info.append(temp)

    dict["Model"]["MemberArrangement"]["Girders"] = beam_info

    #モデル各種構造諸元の代入
    dict["Model"]["StructureType"] = "S"
    dict["Model"]["SteelStructureCondition"] = {"ColumnBaseType":"Fix"}
    dict["Model"]["MarkRules"] = []#一旦markrulesの代入は保留（よくわからない）

    #荷重情報の入力
    dict["Load"]={}
    dict["Load"]["OuterwallLoadListPath"] = input_data['Load']['OuterwallLoadListPath']
    dict["Load"]["OuterWalls"] = input_data['Load']['OuterWalls']
    #スラブ荷重
    dict["Load"]["SlabLoadListPath"] = input_data['Load']['SlabLoadListPath']
    dict["Load"]["SlabLoads"] = input_data['Load']['SlabLoads']

    #断面選定方針
    dict["SelectionStrategy"] = {}
    dict["SelectionStrategy"]["Margin"] = input_data['Margin']
    dict["SelectionStrategy"]["BaseplateListPath"] = input_data['BaseplateListPath']
    dict["SelectionStrategy"]["Sections"] = input_data['SelectionStrategy']["Sections"]

    with open('generator_case1.json', 'w') as f:
        json.dump(dict,f, indent=2)


