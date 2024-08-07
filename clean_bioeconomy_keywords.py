import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('raw_data/keywords/bioeconomy_keywords.csv')

df['BIOEC_MMC'] = pd.to_numeric(df['BIOEC_MMC'], errors='coerce')

# 1. Filtrar en BIOEC_MMC lo que no sea 0
df_filtered = df[df['BIOEC_MMC'] != 0]

# 2. Filtrar en sectors todo menos los vacíos o que tenga "NA"
df_filtered = df_filtered[(df_filtered['sectors'] != '') & (df_filtered['sectors'] != 'NA')]

# 3. Quedarte con las columnas necesarias
columns_to_keep = ['sectors', 'keyword_en_minusc', 'keyword_es_minusc', 'keyword_pt_minusc']
df_selected = df_filtered[columns_to_keep]

# Renombrar las columnas para eliminar el sufijo _minusc
df_selected = df_selected.rename(columns={
    'keyword_en_minusc': 'keyword_en',
    'keyword_es_minusc': 'keyword_es',
    'keyword_pt_minusc': 'keyword_pt'
})

# 4. Crear 4 bases en CSV
# Todas las columnas seleccionadas
df_selected.to_csv('tidy_data/all_keywords.csv', index=False)

# Solo sectors y keyword_en
df_selected[['sectors', 'keyword_en']].to_csv('tidy_data/in_en_keywords.csv', index=False)

# Solo sectors y keyword_es
df_selected[['sectors', 'keyword_es']].to_csv('tidy_data/in_es_keywords.csv', index=False)

# Solo sectors y keyword_pt
df_selected[['sectors', 'keyword_pt']].to_csv('tidy_data/in_pt_keywords.csv', index=False)
