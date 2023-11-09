import pandas as pd
import numpy as np

def max_len_of_columns(df) -> pd.DataFrame:
    '''Function to get len size of each column in a dataframe'''
    measurer = np.vectorize(len)
    _dict = dict(zip(df.columns, measurer(df.values.astype(str)).max(axis=0)))
    return pd.DataFrame([_dict])

def assemble_yml_for_each_table(obj:object, tables:list) -> str:
    '''Prints a yml file to declare sources at a schema.yml file fo a model
    adds name and descriptions for each table and respective columns

    tables must be a pd.DataFrame
    
    '''
    tab = '  '
    yml = f'''
version: 2
sources:
    - name: source
    description: description
    database: database
    +schema: schema
    tables: 
'''
    _name = '- name: '
    tables.sort()
    for table in tables:
        df = getattr(obj, table)
        level = 3
        yml += tab*level + _name + table + '\n'
        level += 1 
        yml += tab*level + 'description: description' + '\n'
        yml += tab*level + 'columns:' + '\n'
        level += 1 
        for column in df.columns:
            yml += tab*level + _name + column +'\n'
            level += 1 
            yml += tab*level + 'description: description' + '\n\n'
            level -= 1 



    return yml