import csv

#検討した仮定断面の出力
def output_section_data(columns,beams,beam_select_mode):
    #csvファイル名
    output_file = 'output_section'

    #csvファイルにデータを書き込む
    with open(output_file + '_'+ str(beam_select_mode)+ '.csv', mode='w',newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['<selected_beam_section>'])
        writer.writerow(['No','H','B','t1','t2','I','Z','Zp','F','ML','MS','QL','QS'])
        for i in beams:
            writer.writerow([i.no,i.H,i.B,i.t1,i.t2,i.I,i.Z,i.Zp,i.F,i.ML,i.Ms,i.QL,i.Qs])
        writer.writerow(['<selected_column_section>'])
        writer.writerow(['No','H','t','A','Ix','Iy','Zp','F','D',
                         'NL','NSx','NSy','MLx','MLy','MSx','MSy','QLx','QLy','QSx','QSy'])
        for i in columns:
            writer.writerow([i.no,i.H,i.t,i.A,i.Ix,i.Iy,i.Zp,i.F,i.D_x,
                             i.NL,i.NSx,i.NSy,i.MLx,i.MLy,i.MSx,i.MSy,i.QLx,i.QLy,i.QSx,i.QSy])

#全データの出力
def output_whole_data(columns,beams,beam_select_mode):
    #csvファイル名
    output_file = 'output_whole_data'

    #csvファイルにデータを書き込む
    with open(output_file + '.csv', mode='w',newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['<beam_data>'])
        writer.writerow(['No','i','j','length','I','K','phai','stiff_ratio','Ci','Cj','category','direction',
                         'story','M0','Q0','unit_weight','weight','Z','Zp','B','H','t1','t2','init_group',
                         'Mp','M_Lx','M_Lx0','M_Ly','M_Ly0','M_Sx','M_Sy','Q_Lx','Q_Ly','Q_Sx','Q_Sy','N_Lx',
                         'N_Ly','N_Sx','N_Sy','ML','QL','Ms','Qs'])
        for i in beams:
            writer.writerow([i.no,i.i,i.j,i.length,i.I,i.K,i.pai,i.stiff_ratio,i.Ci,i.Cj,i.category,
                             i.direction,i.story,i.M0,i.Q0,i.unit_weight,i.weight,i.Z,i.Zp,i.B,i.H,i.t1,i.t2,
                             i.init_group,i.Mp,i.M_Lx,i.M_Lx0,i.M_Ly,i.M_Ly0,i.M_Sx,i.M_Sy,i.Q_Lx,i.Q_Ly,
                             i.Q_Sx,i.Q_Sy,i.N_Lx,i.N_Ly,i.N_Sx,i.N_Sy,i.ML,i.QL,i.Ms,i.Qs])
        writer.writerow(['<column_data>'])
        writer.writerow(['No','i','j','story','length','A','Ix','Iy','Z','Zp','H','t','stiff_ratio_x','stiff_ratio_y','F',
                         'base_K','load_area','init_group','Mpx','Mpy','unit_weight','weight','D_x','D_y','M_Lx','M_Ly',
                         'M_Sx','M_Sy','Q_Lx','Q_Ly','Q_Sx','Q_Sy','N_Lx','N_Ly','N_Sx','N_Sy','MLx','MLy','QLx','QLy',
                         'NL','MSx','MSy','QSx','QSy','NSx','NSy'])
        for i in columns:
            writer.writerow([i.no,i.i,i.j,i.story,i.length,i.A,i.Ix,i.Iy,i.Z,i.Zp,i.H,i.t,i.stiff_ratio_x,i.stiff_ratio_y,
                             i.F,i.base_K,i.load_area,i.init_group,i.Mpx,i.Mpy,i.unit_weight,i.weight,i.D_x,i.D_y,i.M_Lx,i.M_Ly,
                             i.M_Sx,i.M_Sy,i.Q_Lx,i.Q_Ly,i.Q_Sx,i.Q_Sy,i.N_Lx,i.N_Ly,i.N_Sx,i.N_Sy,i.MLx,i.MLy,i.QLx,i.QLy,i.NL,
                             i.MSx,i.MSy,i.QSx,i.QSy,i.NSx,i.NSy])
