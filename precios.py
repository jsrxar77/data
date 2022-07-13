import pandas as pd
  
def remove_tokens(data):
    data = data.str.replace('s/s','')
    data = data.str.replace('*','')
    data = data.str.strip()
    return data

# Loading dataframes
df_precios = pd.read_csv('precios.txt', names=['Nombre','Valor','Producto'], skiprows=0, sep='$')
df_conversion = pd.read_excel('conversiones.xlsx')
# df_conversion = pd.read_csv('conversiones.csv')

# Transform dataframes: remove extra characters 
df_obj = df_precios.select_dtypes(['object'])
df_precios[df_obj.columns] = df_obj.apply(lambda x: remove_tokens(x))

# Transform dataframes: get the right product 
for i, row in df_precios.iterrows():

    nombre_to_lookup = row['Nombre']
    
    df_filtered_conversion_found = df_conversion.loc[df_conversion['Nombre'] == nombre_to_lookup]
    
    if df_filtered_conversion_found['Producto'].any():
        df_precios.at[i,'Producto'] = df_filtered_conversion_found['Producto'].values[0]
    else:
        df_precios.at[i,'Producto'] = ''
    
# Show dataset
print(df_conversion)
print(df_precios)

# Export to excel
df_precios.to_excel('precios-final.xlsx')
