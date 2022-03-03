# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 12:50:43 2022

@author: Franco Fabián
"""

'''
Importar librerías
'''
# Importar librería Pandas

import pandas as pd

'''
Importar bases
'''

# Ruta del directorio: D:\upp

ruta='D:\presentaciones\python'

# Ruta de archivos de entrada: D:\upp\Input

ruta_input=ruta+'\Input'

# Ruta de archivos de salida: D:\upp\Output

ruta_output=ruta+'\Output'

# Importar base

b1=pd.read_excel(ruta_input+"/Primera_base.xlsx",sheet_name='Hoja1',nrows=75,header=0)

'''
Exportar bases
'''

b1.to_excel(ruta_output+'/Base_exportada.xlsx', sheet_name='taller' , index= False)

'''
Generar variables
'''

monto_coor=3000

meses_activo10=['mar','abr','may','jun','jul','ago','set','oct','nov','dic']

b1['p1']=22

b1['p2']='22'

#b1['pl']=b1['Pliego']

# Eliminar espacios de nombres de variables

#b1.columns = b1.columns.str.rstrip()

'''
Multiplicar variables
'''

b1['cas_total'] = b1['Coordinadores de Residencia']*monto_coor

b1['cas_total_2'] = b1['Coordinadores de Residencia']*10000

b1['resultado'] = b1['Coordinadores de Residencia']*b1['Testudiantes_residentes']

'''
Generar variables usando for
'''

for mes in meses_activo10:
    b1['cas_coor_'+mes] = b1['Coordinadores de Residencia']*monto_coor

'''
Renombrar variables
'''

b1.rename(columns={'Código Modular':'cod_mod'},inplace=True)

'''
Verificar y cambiar tipo de variables
'''

print(b1.dtypes)

b1.p2=b1.p2.astype(int)

'''
Eliminar variables
'''

del b1['Ugel']

'''
Usar mínimo
'''

# Valor proyectado de UIT para el 2022

UIT_2022=4600

# Porcentaje para monto techo en EsSalud CAS

UIT_porc=0.55

# Tope de EsSalud = 228

tope_essalud=round(0.09*UIT_porc*UIT_2022)

#b1['essalud_coor']=round(0.09*monto_coor)

b1['essalud_coor']=min(round(0.09*monto_coor),tope_essalud)

'''
Usar condicional
'''

b1.loc[(b1['cargo']=='Coordinador(a) de residencia estudiantil')&(b1['Contratado_airshp']==1),'n_coor_cont'] = '1'
b1.loc[(b1['cargo']=='Personal de cocina')&(b1['Contratado_airshp']==1),'n_coci_cont'] = '1'
b1.loc[(b1['cargo']=='Personal de limpieza y mantenimiento')&(b1['Contratado_airshp']==1),'n_limp_cont'] = '1'
b1.loc[(b1['cargo']=='Personal de seguridad')&(b1['Contratado_airshp']==1),'n_segu_cont'] = '1'
b1.loc[(b1['cargo']=='Promotor(a) de Bienestar')&(b1['Contratado_airshp']==1),'n_prom_cont'] = '1'
b1.loc[(b1['cargo']=='Responsable de bienestar SRE')&(b1['Contratado_airshp']==1),'n_resp_cont'] = '1'

'''
Quitar valores NA
'''

#b1 = b1.dropna()

#b1 = b1.dropna(subset=['n_coor_cont'])

# Reemplzar NA por 0

b1 = b1.fillna(0)

#b1 = b1.fillna('')

'''
Agrupar (collapse)
'''
print(b1.dtypes)

b1.n_coor_cont=b1.n_coor_cont.astype(int)
b1.n_coci_cont=b1.n_coci_cont.astype(int)
b1.n_limp_cont=b1.n_limp_cont.astype(int)
b1.n_segu_cont=b1.n_segu_cont.astype(int)
b1.n_prom_cont=b1.n_prom_cont.astype(int)
b1.n_resp_cont=b1.n_resp_cont.astype(int)

# Agrupar usando el método groupby

b1_g=b1.groupby(['cod_mod'])[['n_coor_cont','n_coci_cont','n_limp_cont','n_segu_cont','n_prom_cont','n_resp_cont']].sum()

'''
Combinar (merge)
'''

# Importar segunda base

b2=pd.read_excel(ruta_input+"/Segunda_base.xlsx",sheet_name='Hoja1',header=0)

# Combinar usando inner

b1_g_b2=pd.merge(b1_g, b2, on ='cod_mod', how ="inner")

'''
Usar melt para pasar a long (reshape long)
'''
# Importar base

b3=pd.read_excel(ruta_input+"/Tercera_base.xlsx",sheet_name='Hoja1',header=0)

# Pasar a long

b_long=pd.melt(b3, id_vars=['cod_pliego', 'cod_ue', 'cod_ugel','nom_pliego','nom_ue','ugel'], value_vars=b3.columns[[x.startswith('name') for x in b3.columns]].tolist(), var_name='s', value_name='name')

'''
Extraer números de una cadena
'''

b_long['valor']=b_long.s.str.extract('(\d+)')

b_long['mes']=b_long['s'].str.extract('(?:.*_)([0-9]+)')

#b_long['valor2'] = b_long['s'].str[6:]

'''
Usar pivot para pasar a wide (reshape wide)
'''

b_wide=b_long.pivot(index=['cod_pliego', 'cod_ue', 'cod_ugel','valor','nom_pliego','nom_ue','ugel'], columns='mes', values='name')

# Quitar índice

b_wide_ri= b_wide.reset_index()

'''
Agregar ceros a la izquierda
'''

b_wide_ri.cod_ugel=b_wide_ri.cod_ugel.astype(str)

print(b_wide_ri.dtypes)

b_wide_ri['cod_ugel']= b_wide_ri['cod_ugel'].str.zfill(10)

'''
Ordenar por variables
'''

# Ordenar usando el método sort

b_ord=b_wide_ri.sort_values(by=['cod_ugel'])

# Odenar base

b_f=b_ord[['cod_pliego','nom_pliego','cod_ue','nom_ue','cod_ue','nom_ue','cod_ugel','ugel']]



