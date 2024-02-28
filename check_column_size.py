import math
import pandas as pd
import numpy as np
from member_class import *

def check_column_size(nodes,columns,layers):
#上層の柱から順に確認
    for layer in layers:
        for column in columns:
            if column.story == layer.story:
                if nodes[column.i-1].z > nodes[column.j-1].z:  # i端側がj端側よりも高い場合
                    temp = nodes[column.i-1].column_no_each_node_x#i端部材no
                    temp2 = nodes[column.i-1].column_no_each_node_y
                else:
                    temp = nodes[column.j-1].column_no_each_node_x
                    temp2 = nodes[column.j-1].column_no_each_node_y#j端部材no

                for j in temp:
                    if j != column.no:#自分以外の柱が上側に取りついている場合、その柱のサイズを確認
                        temp_upper_section_area = (columns[j-1].H)**2 - (columns[j-1].H-2*columns[j-1].t)**2
                        temp_lower_section_area = column.H**2 - (column.H-2*column.t)**2
                        #仮に下側の柱が上側の柱よりもサイズが小さい場合、上側の柱諸元と同等に修正
                        if temp_upper_section_area > temp_lower_section_area:
                            column.selected_section_no = columns[j-1].selected_section_no
                            column.A = columns[j-1].A
                            column.Ix = columns[j-1].Ix
                            column.Iy = columns[j-1].Iy
                            column.unit_weight = columns[j-1].unit_weight
                            column.weight = columns[j-1].weight  # 部材自重
                            column.base_K = columns[j-1].base_K
                            column.H = columns[j-1].H
                            column.t = columns[j-1].t
                            column.r = columns[j-1].r
                            column.Zp = columns[j-1].Zp
                            column.F = columns[j-1].F

                        # 柱の剛度の算定(単位cm3）
                            column.KX = column.Ix / column.length * 1000000.0
                            column.KY = column.Iy / column.length * 1000000.0

                for j in temp2:
                    if j != column.no: #自分以外の柱が上側に取りついている場合、その柱のサイズを確認
                        temp_upper_section_area = (columns[j-1].H)**2 - (columns[j-1].H-2*columns[j-1].t)**2
                        temp_lower_section_area = column.H**2 - (column.H-2*column.t)**2
                        # 仮に下側の柱が上側の柱よりもサイズが小さい場合、上側の柱諸元と同等に修正
                        if temp_upper_section_area > temp_lower_section_area:
                            column.selected_section_no = columns[j - 1].selected_section_no
                            column.A = columns[j - 1].A
                            column.Ix = columns[j - 1].Ix
                            column.Iy = columns[j - 1].Iy
                            column.unit_weight = columns[j - 1].unit_weight
                            column.weight = columns[j - 1].weight  # 部材自重
                            column.base_K = columns[j - 1].base_K
                            column.H = columns[j - 1].H
                            column.t = columns[j - 1].t
                            column.r = columns[j - 1].r
                            column.Zp = columns[j - 1].Zp
                            column.F = columns[j - 1].F

                        # 柱の剛度の算定(単位cm3）
                            column.KX = column.Ix / column.length * 1000000.0
                            column.KY = column.Iy / column.length * 1000000.0
