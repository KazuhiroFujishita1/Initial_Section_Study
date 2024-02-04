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
def output_whole_data(columns,beams,nodes,layers):
    #csvファイル名
    output_file = 'output_whole_data'

    #csvファイルにデータを書き込む
    with open(output_file + '.csv', mode='w',newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['<beam_data>'])
        writer.writerow(['No','i','j','length','I','K','initial_eq_beam_stiff_ratio_i','initial_eq_beam_stiff_ratio_j','eq_beam_stiff_ratio_i','eq_beam_stiff_ratio_j','phai','phai2','Ci','Cj','beam_category','direction',
                         'story','M0','Q0','unit_weight','weight','Z','Zp','initial_B','initial_H','initial_t1','initial_t2','B','H','t1','t2','init_group','boundary_i','boundary_j',
                         'Mp','M_Lx_i','M_Lx_j','M_Lx0','M_Ly_i','M_Ly_j','M_Ly0','M_Sx_i','M_Sx_j','M_Sy_i','M_Sy_j','Q_Lx_i','Q_Lx_j',
                         'Q_Ly_i','Q_Ly_j','Q_Sx','Q_Sy','N_Lx',
                         'N_Ly','N_Sx','N_Sy','ML','QL','Ms','Qs'])
        for i in beams:
            writer.writerow([i.no,i.i,i.j,'{:.2f}'.format(i.length),'{:10}'.format(i.I),'{:.2f}'.format(float(i.K)),'{:.2f}'.format(i.eq_beam_stiff_ratio_i_initial),
                             '{:.2f}'.format(i.eq_beam_stiff_ratio_j_initial),'{:.2f}'.format(i.eq_beam_stiff_ratio_i),'{:.2f}'.format(i.eq_beam_stiff_ratio_j),
                             i.pai,i.pai2,'{:.2f}'.format(i.Ci),'{:.2f}'.format(i.Cj),i.category,
                             i.direction,i.story,'{:.2f}'.format(i.M0),'{:.2f}'.format(i.Q0),'{:.2f}'.format(i.unit_weight),
                             '{:.2f}'.format(i.weight),'{:10}'.format(i.Z),'{:10}'.format(i.Zp),i.B_initial,i.H_initial,i.t1_initial,
                             i.t2_initial,i.B,i.H,i.t1,i.t2,i.init_group,i.boundary_i,i.boundary_j,i.Mp,
                             '{:.2f}'.format(i.M_Lx[0]) if len(i.M_Lx) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Lx[1]) if len(i.M_Lx) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Lx0) if type(i.M_Lx0) is float else '0.00',
                             '{:.2f}'.format(i.M_Ly[0]) if len(i.M_Ly) > 0 else '0.00'
                             ,'{:.2f}'.format(i.M_Ly[1]) if len(i.M_Ly) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Ly0) if type(i.M_Ly0) is float else '0.00',
                             '{:.2f}'.format(i.M_Sx[0]) if len(i.M_Sx) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Sx[1]) if len(i.M_Sx) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Sy[0]) if len(i.M_Sy) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Sy[1]) if len(i.M_Sy) > 0 else '0.00',
                             '{:.2f}'.format(i.Q_Lx[0]) if len(i.Q_Lx) > 0 else '0.00',
                             '{:.2f}'.format(i.Q_Lx[1]) if len(i.Q_Lx) > 0 else '0.00',
                             '{:.2f}'.format(i.Q_Ly[0]) if len(i.Q_Ly) > 0 else '0.00',
                             '{:.2f}'.format(i.Q_Ly[1]) if len(i.Q_Ly) > 0 else '0.00',
                            '{:.2f}'.format(i.Q_Sx),
                             '{:.2f}'.format(i.Q_Sy),
                             '{:.2f}'.format(i.N_Lx) if len(i.N_Lx) > 0 else '0.00',
                             '{:.2f}'.format(i.N_Ly) if len(i.N_Ly) > 0 else '0.00',
                             '{:.2f}'.format(i.N_Sx) if len(i.N_Sx) > 0 else '0.00',
                             '{:.2f}'.format(i.N_Sy) if len(i.N_Sy) > 0 else '0.00',
                             '{:.2f}'.format(i.ML),
                             '{:.2f}'.format(i.QL),
                             '{:.2f}'.format(i.Ms),
                             '{:.2f}'.format(i.Qs)])

        writer.writerow(['<column_data>'])
        writer.writerow(['No','i','j','story','length','A','Ix','Iy','Z','Zp','initial_H','initial_t','initial_stiff_ratio_x','initial_stiff_ratio_y','H','t','stiff_ratio_x','stiff_ratio_y','F',
                         'base_K','load_area','init_group','Mpx','Mpy','unit_weight','weight','D_x','D_y','M_Lx','M_Ly',
                         'M_Sx','M_Sy','Q_Lx','Q_Ly','Q_Sx','Q_Sy','N_Lx','N_Ly','N_Sx','N_Sy','MLx','MLy','QLx','QLy',
                         'NL','MSx','MSy','QSx','QSy','NSx','NSy','required_area','decrement_ratio_x','decrement_ratio_y',
                         'minimum_selected_section_no','tc1','tc2x','tc2y','tc'])
        for i in columns:
            writer.writerow([i.no,i.i,i.j,i.story,i.length,i.A,i.Ix,i.Iy,i.Z,i.Zp,i.H_initial,i.t_initial,i.stiff_ratio_x_initial,i.stiff_ratio_y_initial,i.H,i.t,i.stiff_ratio_x,i.stiff_ratio_y,
                             i.F,i.base_K,i.load_area,i.init_group,i.Mpx,i.Mpy,i.unit_weight,i.weight,i.D_x,i.D_y,i.M_Lx,i.M_Ly,
                             i.M_Sx,i.M_Sy,i.Q_Lx,i.Q_Ly,i.Q_Sx,i.Q_Sy,i.N_Lx,i.N_Ly,i.N_Sx,i.N_Sy,i.MLx,i.MLy,i.QLx,i.QLy,i.NL,
                             i.MSx,i.MSy,i.QSx,i.QSy,i.NSx,i.NSy,i.required_area,i.decrement_ratio_x,i.decrement_ratio_y,
                             i.minimum_selected_section_no,i.tc1,i.tc2x,i.tc2y,i.tc])
        writer.writerow(['<node_data>'])
        writer.writerow(
            ['no','x','y','z','beam_no_each_node_x','column_no_each_node_x','column_no_each_node_y','member_no_each_node_x',
             'beam_no_each_node2_x','member_no_each_node2_x','beam_no_each_node_y','beam_no_each_node2_y','member_no_each_node_y',
             'member_no_each_noe2_y','node_member_stiff_x','node_member_stiff_y','node_member_stiff2_x','node_member_stiff2_y',
             'req_Mpx','req_Mpy'])
        for i in nodes:
            writer.writerow([i.no, i.x, i.y, i.z, i.beam_no_each_node_x, i.column_no_each_node_x, i.column_no_each_node_y, i.member_no_each_node_x,
                             i.beam_no_each_node2_x, i.member_no_each_node2_x, i.beam_no_each_node_y, i.beam_no_each_node2_y, i.member_no_each_node_y,
            i.member_no_each_node2_y, i.node_member_stiff_x, i.node_member_stiff_y, i.node_member_stiff2_x, i.node_member_stiff2_y,
                             i.req_Mpx,i.req_Mpy])
        writer.writerow(['<layer_data>'])
        writer.writerow(
            ['story','height','shear_force_x','shear_force_y','omega1','omega2','omega1_seismic','omega2_seismic','floor_area','outerwall_length',
             'weight','cum_weight','alpha_i','Ai','Ci','Qi','horizontal_disp_x','horizontal_disp_y','horizontal_angle_x,','horizontal_angle_y','column_num',
             'req_D_sum_x','req_D_sum_y','req_D_x','req_D_y','D_sum_x','D_sum_y','D_max_x','D_max_y',
             'k_limit1_x','k_limit1_y','I_limit1_x','I_limit1_y'])
        for i in layers:
            writer.writerow([i.story, i.height, i.shear_force_x, i.shear_force_y, i.omega1, i.omega2, i.omega1_seismic, i.omega2_seismic,i.floor_area,i.outerwall_length,
                             i.weight, i.cum_weight, i.alpha_i, i.Ai, i.Ci, i.Qi, i.horizontal_disp_x, i.horizontal_disp_y, i.horizontal_angle_x, i.horizontal_angle_y, i.column_num,
            i.req_D_sum_x, i.req_D_sum_y, i.req_D_x, i.req_D_y, i.D_sum_x, i.D_sum_y, i.D_max_x, i.D_max_y, i.k_limit1_x, i.k_limit1_y, i.I_limit1_x, i.I_limit1_y])
