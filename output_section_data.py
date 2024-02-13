import csv

#検討した仮定断面の出力
def output_section_data(columns,beams,beam_select_mode):
    #csvファイル名
    output_file = 'output_section'

    #csvファイルにデータを書き込む
    with open(output_file + '_'+ str(beam_select_mode)+ '.csv', mode='w',newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['<selected_beam_section>'])
        writer.writerow(['No','H(mm)','B(mm)','t1(mm)','t2(mm)','stiffness_ratio_i','stiffness_ratio_j','initial_H(mm)','initial_B(mm)',
                         'initial_t1(mm)','initial_t2(mm)','initial_stiffness_ratio_i','initial_stiffness_ratio_j','I(m4)','Z(m3)','Zp(m3)','F(N/mm2)',
                         'M_Lx_i(kNm)','M_Lx_j(kNm)','M_Lx0(kNm)','M_Ly_i(kNm)','M_Ly_j(kNm)','M_Ly0(kNm)','M_Sx_i(kNm)','M_Sx_j(kNm)','M_Sy_i(kNm)','M_Sy_j(kNm)',
                         'Q_Lx_i(kN)','Q_Lx_j(kN)',
                         'Q_Ly_i(kN)','Q_Ly_j(kN)','Q_Sx(kN)','Q_Sy(kN)','N_Lx(kN)',
                         'N_Ly(kN)','N_Sx(kN)','N_Sy(kN)','ML(kNm)','QL(kN)','Ms(kNm)','Qs(kN)','long-term deflection_x(m)','long-term deflection_y(m)'])
        for i in beams:
            writer.writerow([i.no,'{:.2f}'.format(i.H),'{:.2f}'.format(i.B),'{:.2f}'.format(i.t1),'{:.2f}'.format(i.t2),
                             '{:.2f}'.format(i.eq_beam_stiff_ratio_i),'{:.2f}'.format(i.eq_beam_stiff_ratio_j),
                             '{:.2f}'.format(i.H_initial), '{:.2f}'.format(i.B_initial), '{:.2f}'.format(i.t1_initial), '{:.2f}'.format(i.t2_initial),
                             '{:.2f}'.format(i.eq_beam_stiff_ratio_i_initial),'{:.2f}'.format(i.eq_beam_stiff_ratio_j_initial),i.I,i.Z,i.Zp
                                ,i.F,'{:.2f}'.format(i.M_Lx[0]) if len(i.M_Lx) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Lx[1]) if len(i.M_Lx) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Lx0) if type(i.M_Lx0) is not list else '0.00',
                             '{:.2f}'.format(i.M_Ly[0]) if len(i.M_Ly) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Ly[1]) if len(i.M_Ly) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Ly0) if type(i.M_Ly0) is not list else '0.00',
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
                             '{:.2f}'.format(i.Qs),
                             '{:.2f}'.format(i.Qs),i.delta_x if type(i.delta_x) is not list else '0.00',
                             i.delta_y if type(i.delta_y) is not list else '0.00'])
        writer.writerow(['<selected_column_section>'])
        writer.writerow(['No','H(mm)','t(mm)','A(m2)','Ix(m2)','Iy(m2)','Zp(m2)','stiffness_ratio','initial_H(mm)',
                         'initial_t(mm)','initial_stiffness_ratio','F(N/mm2)','D_x','D_y',
                         'M_Lx_i(kNm)','M_Lx_j(kNm)','M_Ly_i(kNm)','M_Ly_j(kNm)',
                         'M_Sx_i(kNm)','M_Sx_j(kNm)','M_Sy_i(kNm)','M_Sy_j(kNm)','Q_Lx_i(kN)','Q_Lx_j(kN)','Q_Ly_i(kN)','Q_Ly_j(kN)','Q_Sx(kN)','Q_Sy(kN)',
                         'N_Lx(kN)','N_Ly(kN)','N_Sx(kN)','N_Sy(kN)','MLx(kNm)','MLy(kNm)','QLx(kN)','QLy(kN)',
                         'NL(kN)','MSx(kNm)','MSy(kNm)','QSx(kN)','QSy(kN)','NSx(kN)','NSy(kN)'])
        for i in columns:
            writer.writerow([i.no,i.H,i.t,i.A,i.Ix,i.Iy,i.Zp,'{:.2f}'.format(i.stiff_ratio_x),i.H_initial,i.t_initial,'{:.2f}'.format(i.stiff_ratio_x_initial),
                             i.F,'{:.2f}'.format(i.D_x),'{:.2f}'.format(i.D_y),
                             '{:.2f}'.format(i.M_Lx[0]), '{:.2f}'.format(i.M_Lx[1]), '{:.2f}'.format(i.M_Ly[0]),
                             '{:.2f}'.format(i.M_Ly[1]),
                             '{:.2f}'.format(i.M_Sx[0]), '{:.2f}'.format(i.M_Sx[1]), '{:.2f}'.format(i.M_Sy[0]),
                             '{:.2f}'.format(i.M_Sy[1]),
                             '{:.2f}'.format(i.Q_Lx[0]), '{:.2f}'.format(i.Q_Lx[1]), '{:.2f}'.format(i.Q_Ly[0]),
                             '{:.2f}'.format(i.Q_Ly[1]),
                             '{:.2f}'.format(i.Q_Sx), '{:.2f}'.format(i.Q_Sy), '{:.2f}'.format(i.N_Lx),
                             '{:.2f}'.format(i.N_Ly), '{:.2f}'.format(i.N_Sx),
                             '{:.2f}'.format(i.N_Sy), '{:.2f}'.format(i.MLx), '{:.2f}'.format(i.MLy),
                             '{:.2f}'.format(i.QLx), '{:.2f}'.format(i.QLy),
                             '{:.2f}'.format(i.NL), '{:.2f}'.format(i.MSx), '{:.2f}'.format(i.MSy),
                             '{:.2f}'.format(i.QSx), '{:.2f}'.format(i.QSy), '{:.2f}'.format(i.NSx),
                             '{:.2f}'.format(i.NSy)])

#全データの出力
def output_whole_data(columns,beams,nodes,layers):
    #csvファイル名
    output_file = 'output_whole_data'

    #csvファイルにデータを書き込む
    with open(output_file + '.csv', mode='w',newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['<beam_data>'])
        writer.writerow(['No','i','j','length(m)','I(m4)','K(cm3)','initial_eq_beam_stiff_ratio_i','initial_eq_beam_stiff_ratio_j','eq_beam_stiff_ratio_i','eq_beam_stiff_ratio_j','phai','phai2','Ci(kNm)','Cj(kNm)','beam_category','beam_direction',
                         'beam_belong_story','M0(kNm)','Q0(kN)','unit_weight(kg/m)','weight(kg)','Z(m3)','Zp(m3)','initial_B(mm)','initial_H(mm)','initial_t1(mm)','initial_t2(mm)',
                         'B(mm)','H(mm)','t1(mm)','t2(mm)','init_group','boundary_i','boundary_j',
                         'Mp(kNm)','M_Lx_i(kNm)','M_Lx_j(kNm)','M_Lx0(kNm)','M_Ly_i(kNm)','M_Ly_j(kNm)','M_Ly0(kNm)','M_Sx_i(kNm)','M_Sx_j(kNm)','M_Sy_i(kNm)','M_Sy_j(kNm)','Q_Lx_i(kN)','Q_Lx_j(kN)',
                         'Q_Ly_i(kN)','Q_Ly_j(kN)','Q_Sx(kN)','Q_Sy(kN)','N_Lx(kN)',
                         'N_Ly(kN)','N_Sx(kN)','N_Sy(kN)','ML(kNm)','QL(kN)','Ms(kNm)','Qs(kN)','beam_deflection_x(m)','beam_deflection_y(m)','beam_deflection_x(after_revision)(m)','beam_deflection_y(after_revision)(m)',
                         'beam_bending_stress(N/mm2)(long)','beam_shear_stress(N/mm2)(long)','beam_bending_stress(N/mm2)(short)','beam_shear_stress(N/mm2)(short)'])
        for i in beams:
            writer.writerow([i.no,i.i,i.j,'{:.2f}'.format(i.length),'{:10}'.format(i.I),'{:.2f}'.format(float(i.K)),'{:.2f}'.format(i.eq_beam_stiff_ratio_i_initial),
                             '{:.2f}'.format(i.eq_beam_stiff_ratio_j_initial),'{:.2f}'.format(i.eq_beam_stiff_ratio_i),'{:.2f}'.format(i.eq_beam_stiff_ratio_j),
                             i.pai,i.pai2,'{:.2f}'.format(i.Ci),'{:.2f}'.format(i.Cj),i.category,
                             i.direction,i.story,'{:.2f}'.format(i.M0),'{:.2f}'.format(i.Q0),'{:.2f}'.format(i.unit_weight),
                             '{:.2f}'.format(i.weight),'{:10}'.format(i.Z),'{:10}'.format(i.Zp),i.B_initial,i.H_initial,i.t1_initial,
                             i.t2_initial,i.B,i.H,i.t1,i.t2,i.init_group,i.boundary_i,i.boundary_j,
                             '{:.2f}'.format(i.Mp) if type(i.Mp) is float else '0.00',
                             '{:.2f}'.format(i.M_Lx[0]) if len(i.M_Lx) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Lx[1]) if len(i.M_Lx) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Lx0) if type(i.M_Lx0) is not list else '0.00',
                             '{:.2f}'.format(i.M_Ly[0]) if len(i.M_Ly) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Ly[1]) if len(i.M_Ly) > 0 else '0.00',
                             '{:.2f}'.format(i.M_Ly0) if type(i.M_Ly0) is not list else '0.00',
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
                             '{:.2f}'.format(i.Qs),i.delta_x,i.delta_y,i.rev_delta_x,i.rev_delta_y,
                             '{:.2f}'.format(i.sigma_b_L) if type(i.sigma_b_L) is not list else '0.00',
                             '{:.2f}'.format(i.tau_L) if type(i.tau_L) is not list else '0.00',
                             '{:.2f}'.format(i.sigma_b_s) if type(i.sigma_b_s) is not list else '0.00',
                             '{:.2f}'.format(i.tau_s) if type(i.tau_s) is not list else '0.00'])

        writer.writerow(['<column_data>'])
        writer.writerow(['No','i','j','story','length(m)','A(m2)','Ix(m4)','Iy(m4)','Z(m3)','Zp(m3)','initial_H(mm)','initial_t(mm)',
                         'initial_stiff_ratio_x','initial_stiff_ratio_y','initial_base_K','H(mm)','t(mm)','stiff_ratio_x','stiff_ratio_y','F(N/mm2)',
                         'base_K(cm3)','load_area(m2)','init_group','Mpx(kNm)','Mpy(kNm)','unit_weight(kg/m)','weight(kg)',
                         'y0_x','y1_x','y2_x','y3_x','y0_y','y1_y','y2_y','y3_y','k','a',
                         'D_x','D_y','M_Lx_i(kNm)','M_Lx_j(kNm)','M_Ly_i(kNm)','M_Ly_j(kNm)',
                         'M_Sx_i(kNm)','M_Sx_j(kNm)','M_Sy_i(kNm)','M_Sy_j(kNm)','Q_Lx_i(kN)','Q_Lx_j(kN)','Q_Ly_i(kN)','Q_Ly_j(kN)','Q_Sx(kN)','Q_Sy(kN)',
                         'N_Lx(kN)','N_Ly(kN)','N_Sx(kN)','N_Sy(kN)','MLx(kNm)','MLy(kNm)','QLx(kN)','QLy(kN)',
                         'NL(kN)','MSx(kNm)','MSy(kNm)','QSx(kN)','QSy(kN)','NSx(kN)','NSy(kN)','required_area(m2)','decrement_ratio_x','decrement_ratio_y',
                         'minimum_selected_section_no','tc1(mm)','tc2x(mm)','tc2y(mm)','tc(mm)'])
        for i in columns:
            writer.writerow([i.no,i.i,i.j,i.story,i.length,i.A,i.Ix,i.Iy,i.Z,i.Zp,i.H_initial,i.t_initial,'{:.2f}'.format(i.stiff_ratio_x_initial),'{:.2f}'.format(i.stiff_ratio_y_initial),
                             i.base_K_initial,i.H,i.t,'{:.2f}'.format(i.stiff_ratio_x),'{:.2f}'.format(i.stiff_ratio_y),
                             i.F,i.base_K,'{:.2f}'.format(i.load_area),i.init_group,'{:.2f}'.format(i.Mpx),'{:.2f}'.format(i.Mpy),
                             '{:.2f}'.format(i.unit_weight),'{:.2f}'.format(i.weight),i.y0_x,i.y1_x,i.y2_x,i.y3_x,i.y0_y,i.y1_y,i.y2_y,i.y3_y,
                             '{:.2f}'.format(i.kk),'{:.2f}'.format(i.a),
                             '{:.2f}'.format(i.D_x),'{:.2f}'.format(i.D_y),
                             '{:.2f}'.format(i.M_Lx[0]),'{:.2f}'.format(i.M_Lx[1]),'{:.2f}'.format(i.M_Ly[0]),'{:.2f}'.format(i.M_Ly[1]),
                             '{:.2f}'.format(i.M_Sx[0]),'{:.2f}'.format(i.M_Sx[1]),'{:.2f}'.format(i.M_Sy[0]),'{:.2f}'.format(i.M_Sy[1]),
                             '{:.2f}'.format(i.Q_Lx[0]),'{:.2f}'.format(i.Q_Lx[1]),'{:.2f}'.format(i.Q_Ly[0]),'{:.2f}'.format(i.Q_Ly[1]),
                             '{:.2f}'.format(i.Q_Sx),'{:.2f}'.format(i.Q_Sy),'{:.2f}'.format(i.N_Lx),'{:.2f}'.format(i.N_Ly),'{:.2f}'.format(i.N_Sx),
                             '{:.2f}'.format(i.N_Sy),'{:.2f}'.format(i.MLx),'{:.2f}'.format(i.MLy),'{:.2f}'.format(i.QLx),'{:.2f}'.format(i.QLy),
                             '{:.2f}'.format(i.NL),'{:.2f}'.format(i.MSx),'{:.2f}'.format(i.MSy),'{:.2f}'.format(i.QSx),'{:.2f}'.format(i.QSy),'{:.2f}'.format(i.NSx),
                            '{:.2f}'.format(i.NSy),'{:.2f}'.format(i.required_area),'{:.2f}'.format(i.decrement_ratio_x),'{:.2f}'.format(i.decrement_ratio_y),
                             '{:.2f}'.format(i.minimum_selected_section_no),'{:.2f}'.format(i.tc1),'{:.2f}'.format(i.tc2x),
                             '{:.2f}'.format(i.tc2y),'{:.2f}'.format(i.tc)])
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
            ['story','height(m)','shear_force_x(kN)','shear_force_y(kN)','omega1','omega2','omega1_seismic','omega2_seismic','floor_area(m2)',
             'outerwall_length(m)','weight(kN)','cum_weight(kN)','alpha_i','Ai','Ci','Qi(kN)','horizontal_disp_x(mm)','horizontal_disp_y(mm)','horizontal_angle_x(rad),','horizontal_angle_y(rad)','column_num',
             'req_D_sum_x','req_D_sum_y','req_D_x','req_D_y','D_sum_x','D_sum_y','D_max_x','D_max_y',
             'k_limit1_x','k_limit1_y','I_limit1_x(m4)','I_limit1_y(m4)'])
        for i in layers:
            writer.writerow([i.story, '{:.2f}'.format(i.height), '{:.2f}'.format(i.shear_force_x), '{:.2f}'.format(i.shear_force_y),
                             '{:.2f}'.format(i.omega1), '{:.2f}'.format(i.omega2), '{:.2f}'.format(i.omega1_seismic), '{:.2f}'.format(i.omega2_seismic),
                             '{:.2f}'.format(i.floor_area),'{:.2f}'.format(i.outerwall_length),
                             '{:.2f}'.format(i.weight), '{:.2f}'.format(i.cum_weight), '{:.2f}'.format(i.alpha_i), '{:.2f}'.format(i.Ai),
                             '{:.2f}'.format(i.Ci), '{:.2f}'.format(i.Qi), '{:.2f}'.format(i.horizontal_disp_x), '{:.2f}'.format(i.horizontal_disp_y),
                             '{:.2f}'.format(i.horizontal_angle_x), '{:.2f}'.format(i.horizontal_angle_y), i.column_num,
            '{:.2f}'.format(i.req_D_sum_x), '{:.2f}'.format(i.req_D_sum_y), '{:.2f}'.format(i.req_D_x), '{:.2f}'.format(i.req_D_y),
                             '{:.2f}'.format(i.D_sum_x), '{:.2f}'.format(i.D_sum_y), '{:.2f}'.format(i.D_max_x), '{:.2f}'.format(i.D_max_y),
                             '{:.2f}'.format(i.k_limit1_x), '{:.2f}'.format(i.k_limit1_y), i.I_limit1_x, i.I_limit1_y])
