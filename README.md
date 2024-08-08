# Bioeconomy Jobs 

## Instalación


1. **Clona este repositorio**:

    ```sh
    git clone https://github.com/brianamaya01/bioeconomy_jobs.git
    cd bioeconomy_jobs
    ```

2. **Crea y activa un entorno virtual (opcional pero recomendado)**:

    ```sh
    python3.11 -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. **Instala las dependencias**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Descarga los modelos de spaCy**:

    ```sh
    python -m spacy download es_core_news_md
    python -m spacy download en_core_web_sm
    python -m spacy download pt_core_news_md
    ```

## Códigos 

1. Para ordenar las palabras clave asociadas a bioeconomía clean_bioeconomy_keywords.py, las palabras limpias para estan en tidy_data\keywords 
2. Para acceder a empleos a partir de las palabras clave se usó jobs_linkedin_keywords.py y jobs_bioeconomy_careers.py
3. Para acceder a tesauros en español se usaron thesaurus_keywords_fao.py y thesaurus_snipes_f1.py, thesaurus_snipes_f2.py  
4. Se realizó una prueba de clasificación con la libreria Spacy para revisar si las palabras clasificadas se encuentran en empleos actuales. Requiere de mejoras. 

