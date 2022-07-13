from wsgiref import headers
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
import pandas as pd
  
def remove_tokens(data):
    data = data.str.replace('s/s','')
    data = data.str.replace('*','')
    data = data.str.strip()
    return data

# Loading dataet
df = pd.read_csv('precios.txt', names=['Nombre','Valor','Producto'], skiprows=0, sep='$')
df_conversion = pd.read_csv('conversion.csv')

# Transform dataset
df_obj = df.select_dtypes(['object'])
df[df_obj.columns] = df_obj.apply(lambda x: remove_tokens(x))

# Show dataset
print(df_conversion)
print(df)

for i, row in df.iterrows():

    nombre_to_lookup = row['Nombre']
    
    conversion_row_found = df_conversion.loc[df_conversion['Nombre'] == nombre_to_lookup]
    
    if conversion_row_found['Producto'].any():
        df.at[i,'Producto'] = conversion_row_found['Producto'].values[0]
    else:
        df.at[i,'Producto'] = ''
    
print(df_conversion)
print(df)
