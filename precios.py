import pandas as pd
  
def remove_tokens(data):
    data = data.str.replace('s/s','')
    data = data.str.replace('*','')

    # removing emoticons and...
    data = data.str.encode('ascii', 'ignore').str.decode('ascii')

    data = data.str.strip()

    return data

# Loading dataframes
df_precios = pd.read_csv('precios.txt', names=['Nombre','Valor','Producto'], skiprows=0, sep='$')

df_conversion = pd.read_excel('conversiones.xlsx')

# Transform dataframes: remove extra characters 
df_precios_obj = df_precios.select_dtypes(['object'])

df_precios[df_precios_obj.columns] = df_precios_obj.apply(lambda x: remove_tokens(x))

# Transform dataframes: get the right product 
for i, row in df_precios.iterrows():

    nombre_to_lookup = row['Nombre']
    
    df_filtered_conversion_found = df_conversion.loc[df_conversion['Nombre'] == nombre_to_lookup]
    
    if df_filtered_conversion_found['Producto'].any():
        df_precios.at[i,'Producto'] = df_filtered_conversion_found['Producto'].values[0]
    else:
        df_precios.at[i,'Producto'] = ''

# Export to excel
df_precios_final = df_precios.sort_values(by="Producto", ascending=True)

df_precios_final = df_precios_final[['Producto','Valor','Nombre']]

df_precios_final.to_excel('precios-final.xlsx', index = False)
