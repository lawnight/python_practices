s = 'n_jj,n_jn,n_ch,n_wh,n_qy,n_gx,o_jj,o_jn,o_ch,o_wh,o_qy,o_gx,date'





array = s.split(',')


print('+","+'.join(['item["%s"][0]'%i for i in array]))