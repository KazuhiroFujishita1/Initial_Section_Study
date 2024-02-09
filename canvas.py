#%%

import os
import json

from calc import * 
from calc_stress import *
from member_class import *
from set_initial_section import *
from calc_weight import *
from update_section import *
from output_section_data import *

class Config:
    def __init__(self):
        self.zoom = 1.0 
        self.centerX = 0.0 
        self.centerY = 0.0 
        self.width = 600.0 
        self.height = 600.0 
        self.margin = 50.0 
        self.fontSize = 8.0 

class Line:
    def __init__(self):
        self.x1 = 0.0
        self.y1 = 0.0
        self.x2 = 0.0
        self.y2 = 0.0

class MomentLine:
    def __init__(self, line):
        self.line = line
        self.m1 = 0.0
        self.m2 = 0.0
        self.m0 = 0.0
    
    def dumps(self):
        return { "line": self.line.__dict__, 
                 "m1" : self.m1, 
                 "m2" : self.m2, 
                 "m0" : self.m0 }

class LineText:
    def __init__(self, line):
        self.x1 = line.x1
        self.y1 = line.y1
        self.x2 = line.x2
        self.y2 = line.y2


class DrawingLayer:
    def __init__(self):
        self.lines = []
        self.momentLines = []
        self.lineTexts = []
    
    def dumps(self):
        return { "lines" :  list(map(lambda x: x.__dict__, self.lines)),
                 "momentLines" : list(map(lambda x: x.dumps(), self.momentLines)), 
                 "lineTexts" : list(map(lambda x: x.__dict__, self.lineTexts)) 
               }

class Tree:
    def __init__(self):
        self.path = ""
        self.displayName = ""
        self.labelNames = []

class Label:
    def __init__(self):
        self.no = 0
        self.name = ""

class Entities:
    def __init__(self):
        self.layers = []
    
    def dumps(self):
        return { "layers" : list(map(lambda x: x.dumps(), self.layers)) }


class Flags:
    def __init__(self):
        self.config = Config()
        self.entities = Entities()
        self.tree = []
        self.labels = []
    def dumps(self):
        return { "config" : self.config.__dict__ ,
                 "entities" : self.entities.__dict__,
                 "tree" : list(map(lambda x: x.__dict__, self.tree)),
                 "labels" : list(map(lambda x: x.__dict__, self.labels)) 
               }

class Column2D:
    def __init__(self, node_i, node_j, column, direction):
        self.column = column
        if direction == "X":
            self.x1 = node_i.x
            self.y1 = node_i.z
            self.x2 = node_j.x
            self.y2 = node_j.z
            self.m1 = -column.M_Lx[0]
            self.m2 = -column.M_Lx[1]

        elif direction == "Y":
            self.x1 = node_i.y
            self.y1 = node_i.z
            self.x2 = node_j.y
            self.y2 = node_j.z
            self.m1 = -column.M_Ly[0]
            self.m2 = -column.M_Ly[1]

        else:
            raise "Undefined direction"

class Beam2D:
    def __init__(self, node_i, node_j, beam, direction):
        self.beam = beam
        if direction == "X":
            self.x1 = node_i.x
            self.y1 = node_i.z
            self.x2 = node_j.x
            self.y2 = node_j.z
            self.m1 = beam.M_Lx[0]
            self.m2 = beam.M_Lx[1]
            self.m0 = beam.M0#1/2*(beam.M_Sx[0]+beam.M_Sx[1])

        elif direction == "Y":
            self.x1 = node_i.y
            self.y1 = node_i.z
            self.x2 = node_j.y
            self.y2 = node_j.z
            self.m1 = beam.M_Ly[0]
            self.m2 = beam.M_Ly[1]
            self.m0 = beam.M0#1/2*(beam.M_Sy[0]+beam.M_Sy[1])

        else:
            raise "Undefined direction"

class FrameMembers:
    def __init__(self):
        self.columns = []
        self.beams = []

    def to_frame_layer(self):
        layer = DrawingLayer()
        lines = []
        for column2d in self.columns:
            line = Line()
            line.x1 = column2d.x1
            line.y1 = column2d.y1
            line.x2 = column2d.x2
            line.y2 = column2d.y2
            lines.append(line)

        for beam2d in self.beams:
            line = Line()
            line.x1 = beam2d.x1
            line.y1 = beam2d.y1
            line.x2 = beam2d.x2
            line.y2 = beam2d.y2
            lines.append(line)
        layer.lines = lines  
        return layer


    def to_moment_layer(self):
        layer = DrawingLayer()
        moment_lines = []
        line_texts = []
        for column2d in self.columns:
            line = Line()
            line.x1 = column2d.x1
            line.y1 = column2d.y1
            line.x2 = column2d.x2
            line.y2 = column2d.y2
            moment_line = MomentLine(line)
            moment_line.line = line
            moment_line.m1 = column2d.m1 
            moment_line.m2 = column2d.m2 
            moment_lines.append(moment_line)

            line_text1 = LineText(line)
            line_text1.text = "%.0f" % column2d.m1
            line_text1.ratio = 0.1
            line_text1.textAnchor = "start"
            line_text1.dominantBaseLine = "text-after-edge"
            line_text2 = LineText(line)
            line_text2.text = "%.0f" % column2d.m2
            line_text2.ratio = 0.9
            line_text2.textAnchor = "end"
            line_text2.dominantBaseLine = "text-before-edge"
            line_texts.append(line_text1)
            line_texts.append(line_text2)

        for beam2d in self.beams:
            line = Line()
            line.x1 = beam2d.x1
            line.y1 = beam2d.y1
            line.x2 = beam2d.x2
            line.y2 = beam2d.y2
            moment_line = MomentLine(line)
            moment_line.line = line
            moment_line.m1 = beam2d.m1 
            moment_line.m2 = beam2d.m2 
            moment_line.m0 = beam2d.m0
            moment_lines.append(moment_line)
            
            line_text1 = LineText(line)
            line_text1.text = "%.0f" % beam2d.m1
            line_text1.ratio = 0.1
            line_text1.textAnchor = "start"
            line_text1.dominantBaseLine = "text-before-edge"
            line_text2 = LineText(line)
            line_text2.text = "%.0f" % beam2d.m2
            line_text2.ratio = 0.9
            line_text2.textAnchor = "end"
            line_text2.dominantBaseLine = "text-after-edge"
            
            line_text3 = LineText(line)
            line_text3.text = "%.0f" % (-0.5 * (abs(beam2d.m2) + abs(beam2d.m1)) + beam2d.m0)
            line_text3.ratio = 0.5
            line_text3.textAnchor = "middle"
            line_text3.dominantBaseLine = "text-before-edge"

            line_texts.append(line_text1)
            line_texts.append(line_text2)
            line_texts.append(line_text3)

        layer.momentLines = moment_lines  
        layer.lineTexts = line_texts  
        return layer




def output_visualize_json(nodes, columns, beams):
    # X方向フレーム
    dic_x_frame = {}

    # Y方向フレーム
    dic_y_frame = {}
    
    for node in nodes:
        if not (node.y in dic_x_frame):
            dic_x_frame[node.y] = FrameMembers()

        if not (node.x in dic_y_frame):
            dic_y_frame[node.x] = FrameMembers()


    for column in columns:
        node_i = nodes[column.i - 1]
        node_j = nodes[column.j - 1]
        if node_i.y == node_j.y:
            column2d = Column2D(node_i, node_j, column, "X")
            dic_x_frame[node_i.y].columns.append(column2d)
            
        if node_i.x == node_j.x:
            column2d = Column2D(node_i, node_j, column, "Y")
            dic_y_frame[node_i.x].columns.append(column2d)

    for beam in beams:
        node_i = nodes[beam.i - 1]
        node_j = nodes[beam.j - 1]
        if node_i.y == node_j.y:
            beam2d = Beam2D(node_i, node_j, beam, "X")
            dic_x_frame[node_i.y].beams.append(beam2d)
                                                
        if node_i.x == node_j.x:                
            beam2d = Beam2D(node_i, node_j, beam, "Y")
            dic_y_frame[node_i.x].beams.append(beam2d)



    trees = []
    for x_frame_key in sorted(dic_x_frame.keys(), key=lambda key: key):
        frame_layer = dic_x_frame[x_frame_key].to_frame_layer()
        moment_layer = dic_x_frame[x_frame_key].to_moment_layer()
        
        entities = Entities()
        entities.layers.append(frame_layer)
        entities.layers.append(moment_layer)
        
        path = "%s/X%d.json" % (destDir, x_frame_key * 1000.0)
        with open(path, mode='w') as f:
            f.write(json.dumps(entities.dumps()))

        tree = Tree()
        tree.path = path
        tree.displayName = path 
        tree.labelNames = [ "X" ]
        trees.append(tree)

    for y_frame_key in sorted(dic_y_frame.keys(), key=lambda key: key):
        frame_layer = dic_y_frame[y_frame_key].to_frame_layer()
        moment_layer = dic_y_frame[y_frame_key].to_moment_layer()
        
        entities = Entities()
        entities.layers.append(frame_layer)
        entities.layers.append(moment_layer)
        path = "%s/Y%d.json" % (destDir, y_frame_key * 1000.0)
        
        with open(path, mode='w') as f:
            f.write(json.dumps(entities.dumps()))
        tree = Tree()
        tree.path = path
        tree.displayName = path 
        tree.labelNames = [ "Y" ]
        trees.append(tree)

    return trees


destDir = "drawing"
if not os.path.exists(destDir):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs(destDir)

nodes, beams, columns, layers, maximum_height = start()

trees = output_visualize_json(nodes, columns, beams)
flags = Flags()
flags.tree = trees
xlabel = Label()
ylabel = Label()
xlabel.no = 1
xlabel.name = "X" 
ylabel.no = 2
ylabel.name = "Y" 
flags.labels.append(xlabel)
flags.labels.append(ylabel)

path = "%s/flags.json" % destDir
with open(path, mode='w') as f:
    f.write(json.dumps(flags.dumps()))




# %%
