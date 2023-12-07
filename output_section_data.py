import csv

#検討した仮定断面の出力
def output_section_data(columns,beams,beam_select_mode):
    #csvファイル名
    output_file = 'output_section'

    #csvファイルにデータを書き込む
    with open(output_file + '_'+ str(beam_select_mode)+ '.csv', mode='w',newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['<selected_beam_section>'])
        writer.writerow(['No','H','B','t1','t2','I','Z','Zp','F'])
        for i in beams:
            writer.writerow([i.no,i.H,i.B,i.t1,i.t2,i.I,i.Z,i.Zp,i.F])
        writer.writerow(['<selected_column_section>'])
        writer.writerow(['No','H','t','A','Ix','Iy','Z','F'])
        for i in columns:
            writer.writerow([i.no,i.H,i.t,i.A,i.Ix,i.Iy,i.Z,i.F])