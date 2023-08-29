import pandas as pd
from typing import Literal
    
def key_error_decorator(function):
    '''this decorator catches KeyError when parsing, e.g. countries that are islands do not have borders'''
    def wrapper(*args, **kwargs):
        try: 
            return function(*args, **kwargs)
        except KeyError as err:
            return pd.DataFrame()
    return wrapper
            

# TODO: colocar nome dos atributos, ou seja, explique todas as tabelas

class Country:
    '''
    en: a base class to parse a country dictionary of countries api
    pt: uma classe base para analisar um dicionário recebido da countries api


    '''
    def __repr__(self):
        return f'Country ({self.common_name})'

    def __init__(self, country_dict: dict) -> None:
        self.country_dict = country_dict
        self.common_name = country_dict['name']['common']
        self.parse_tables()
    
    def parse_tables(self) -> None:
        '''parses and sets attribute tables of a Country object
        '''
        self.names = self.create_name_table()
        self.native_names = self.create_native_names_table()
        self.top_level_domains = self.make_table_from_list('tld')
        self.codes = self.create_code_table()
        self.independency_table = self.create_independency_table()
        self.un_membership_table = self.create_un_membership_table()
        self.currencies = self.make_table_from_dict_of_dicts('currencies', 'currency_code')

        try: 
            # Heard Island and McDonald Islands, Antarctica do not have suffixes
            self.idds = self.make_table_from_dict_field('idd').explode('suffixes', ignore_index=True)
        except KeyError: 
            self.idds = self.make_table_from_dict_field('idd')

        self.capital = self.create_capital_info_table()
        self.alt_spellings = self.make_table_from_list('altSpellings')
        self.regions = self.create_region_table()
        self.languages = self.create_language_table()
        self.translations = self.make_table_from_dict_of_dicts('translations', 'language_code')
        self.lat_lng = self.create_lat_lng_table()
        self.general_information = self.create_general_information_table()
        self.borders = self.make_table_from_list('borders')
        self.demonyms = self.make_table_from_dict_of_dicts('demonyms', 'language_code')
        self.maps = self.make_key_value_table_from_dict('maps', ['site', 'link'])
        self.gini_index = self.make_key_value_table_from_dict('gini', ['year', 'index'])
        self.car_information = self.create_car_information_table()
        self.timezones = self.make_table_from_list('timezones')
        self.continents = self.make_table_from_list('continents')
        self.flags = self.make_key_value_table_from_dict('flags', ['image_format', 'link'])
        self.coat_of_arms = self.make_key_value_table_from_dict('coatOfArms', ['image_format', 'link'])
        self.postal_codes = self.make_table_from_dict_field('postalCode')
         

    def print_fields(self):
        '''en: Print all available fields from a country
        pt_br: Printa todos os campos de um pais
        '''
        for i in self.fields_to_parse:
            print(f'{i}: {self.country_dict[i]}')

    @key_error_decorator
    def make_table_from_dict_field(self, field: str) -> pd.DataFrame:
        '''
        en: Makes a table from a dict, the key will be the name of the columns and the value will be the value inside the cell. Return a one line pd.DataFrame
        pt_br: Faz uma tabela a partir de um dicionário, a chave será o nome da coluna e o valor será o valor da célula. Retorn um pd.DataFrame de tamanho 1

        Parameters
        ----------
        field : str
            key from country dict

        returns
        -------
            pd.DataFrame 
        '''
        if not isinstance(self.country_dict[field], dict):
            raise TypeError('O valor do campo informado não é um dicionário')
        country_record = {i: [self.country_dict[field][i]] for i in self.country_dict[field] if not isinstance(self.country_dict[field][i], dict)}
        
        table = pd.DataFrame(country_record)
        common_name = self.names[['common_name']]
        return common_name.merge(table, how='cross')
    
    def make_table_from_dict(self, _dict: dict) -> pd.DataFrame:
        '''
        Makes a table from a dict but instead of passing a string field, the dict itself is passed. 
        The key will be the name of the columns and the value will be the value inside the cell. Return a one line pd.DataFrame

        Parameters
        ----------
        _dict : dict
            dict to be parsed

        returns
        -------
            pd.DataFrame 
        '''
        if not isinstance(_dict, dict):
            raise TypeError('O valor informado para o _dict não é um dicionário')
        country_record = {i: [_dict[i]] for i in _dict if not isinstance(_dict[i], dict)}
        return pd.DataFrame(country_record)
    
    @key_error_decorator
    def make_key_value_table_from_dict(self, field: str, columns=['col1', 'col2']) -> pd.DataFrame:
        '''
        Makes a table from a dict, where every key is a columns and the values are another column. 
        Column names can be especified, but len of columns must be 2.

        Parameters
        ----------
        field : str
            key from country dict
        
        columns : list[str]
            columns names to be used in the dataframe

        returns
        -------
            pd.DataFrame 
    

        '''
        assert len(columns) == 2, 'Informe somente duas colunas. len(columns) must be 2.'
        _dict = self.country_dict[field]
        table = pd.DataFrame(
            {
                columns[0]: [i for i in _dict],
                columns[1]: [_dict[i] for i in _dict],
            }
        )
        common_name = self.names[['common_name']]
        return common_name.merge(table, how='cross')
    
    @key_error_decorator
    def make_table_from_list(self, field: str):
        '''
        used to parse a field from dictionary where the value is a list

        Parameters
        ----------
        field : str
            a string value to access a key in a country dictionary

        Returns
        -------
        pd.DataFrame
            a DataFrame with key value as column name and list as values and a common name column

        Example
        -------
        When parsing 'timezones' fields from Brazil, the value from timezones is a list of 4 timezones.
        The result DataFrame should look like this
        >>> hook = CountriesHook()
        >>> country = Country(hook.raw_data[64])
        >>> print(country.make_table_from_list('timezones'))
            common      timezones
        0   Brazil      'UTC-05:00'
        1   Brazil      'UTC-04:00'
        2   Brazil      'UTC-03:00'
        3   Brazil      'UTC-02:00'


        '''
        if not isinstance(self.country_dict[field], list):
            raise TypeError(
                f'this field key did not return a list, returned: {self.country_dict[field]}')
        dic = {field: self.country_dict[field]}
        dic['common_name'] = [self.common_name] * len(self.country_dict[field])
        return pd.DataFrame(dic)[['common_name', field]]

    def create_name_table(self, cols: Literal['common', 'official', None] = None) -> pd.DataFrame:
        '''
        returns a table with common and official names of country

        cols works like a select, to choose which column you want

        if cols is None, both are returned

        cols : Literal['common', 'official', None]
            parameter to choose which column is needed

        returns
        -------
        pd.DataFrame
            a Dataframe with selected names


        '''
        field = 'name'
        if not isinstance(self.country_dict[field], dict):
            raise TypeError('O valor do campo informado não é um dicionário')
        country_record = {i: [self.country_dict[field][i]] for i in self.country_dict[field] if not isinstance(self.country_dict[field][i], dict)}
        
        table = pd.DataFrame(country_record)
        if isinstance(cols, str):
            cols = [cols]
            table = table[cols]
        if isinstance(cols, list|tuple):
            table = table[cols]
            
        return (table
                    .rename(
                        dict(zip(table.columns, [f'{i}_name' for i in table.columns])),
                        axis=1
                    )
                )
    
    @key_error_decorator
    def create_native_names_table(self):
        native_names = self.country_dict['name']['nativeName']
        return (self.names[['common_name']]
                    .merge(pd.concat([self.make_table_from_dict_and_keep_key(native_names, i, 'language_code') for i in native_names], ignore_index=True),
                        how='cross'
                        )
                )

    def create_language_table(self):
        '''
        en: creates a fact table from languages
        pt: cria uma tabela fato de idioma 

        returns
        -------
        pd.DataFrame 
          a Dataframe with the languages of the country
        '''
        langs = self.make_key_value_table_from_dict(
            'languages', ['lang_code', 'lang'])
        # common_name = self.create_name_table('common')
        # lang_table = common_name.merge(langs, how='cross')
        return langs



    def create_code_table(self):
        '''creates a code table containing:
        - cca2 (alpha2Code)   ISO 3166-1 alpha-2 two-letter country codes
        - cca3 (alpha3Code)   ISO 3166-1 alpha-3 three-letter country codes
        - ccn3 (numericCode)  ISO 3166-1 numeric code (UN M49)
        - cioc                Code of the International Olympic Committee
        - status              only granted to countries members of UN
        - and common name of country

        returns
        -------
        pd.DataFrame

        '''

        fields = ["cca2", "ccn3", "cca3", "cioc", 'fifa', "status"]
        code_table = pd.DataFrame(
            {i: [self.country_dict[i]] for i in fields if i in self.country_dict})
        return self.names[['common_name']].merge(code_table, how='cross')
    
    @key_error_decorator
    def create_independency_table(self):
        '''creates a table containing common name and independency flag (y/n)

        returns
        -------
        pd.DataFrame
        '''
        fields = ['independent']
        independency_table = pd.DataFrame(
            {i: ['y' if self.country_dict[i] else 'n'] for i in fields})
        return self.names[['common_name']].merge(independency_table, how='cross')

    def create_un_membership_table(self):
        '''creates a table containing common name and unMember flag (y/n)

        returns
        -------
        pd.DataFrame
        '''
        fields = ['unMember']
        un_table = pd.DataFrame(
            {i: ['y' if self.country_dict[i] else 'n'] for i in fields})
        return self.create_name_table('common').merge(un_table, how='cross')
    
    def make_table_from_dict_and_keep_key(self, _dict, key, column_name):
            '''similar to make_table_from_dict, but key is a useful information, so it will also be kept'''
            key_df = pd.DataFrame({column_name: [key]})
            return (self.make_table_from_dict(_dict[key])
                        .merge(key_df, how='cross')
                    )
    @key_error_decorator
    def make_table_from_dict_of_dicts(self, field, column_name):
        '''this function parses fields that contain a dict of dicts as value

        Parameters
        ----------
        field : str
            key from country dict
        
        column_name : str 
            name to be used in the column that stores key values from dict

        returns
        -------
            pd.DataFrame 
        '''
       
        
        dicts = self.country_dict[field]
        table = pd.concat([self.make_table_from_dict_and_keep_key(dicts, i, column_name) for i in dicts])
        return self.create_name_table('common').merge(table, how='cross')
    
    @key_error_decorator
    def create_region_table(self):
        '''creates a table containing common name and region information (y/n)

        returns
        -------
        pd.DataFrame
        '''
        fields = ['region', 'subregion']
        region_table = pd.DataFrame(
            {i: [self.country_dict[i]] for i in fields})
        return self.create_name_table('common').merge(region_table, how='cross')
    
    def create_lat_lng_table(self):
        '''creates table with coordinates of country
        
        returns
        -------
            pd.DataFrame

        '''
        coordinates = self.country_dict['latlng']
        table = pd.DataFrame({'latitude':[coordinates[0]], 'longitude':[coordinates[1]]})
        return self.create_name_table('common').merge(table, how='cross')
    
    def create_general_information_table(self):
        '''creates a table containing common name and if country is landlocked (do not have access to sea), population,
         area, flag, and start of week (y/n)

        returns
        -------
            pd.DataFrame
        '''
        fields = ['landlocked', 'area', 'flag', 'population', 'startOfWeek']
        region_table = pd.DataFrame(
            {i: [self.country_dict[i]] for i in fields})
        return self.create_name_table('common').merge(region_table, how='cross')
    
    @key_error_decorator
    def create_car_information_table(self):
        '''creates table with signs and driving side in country
        
        returns
        -------
            pd.DataFrame

        '''
        car_info = self.country_dict['car']
        side = pd.DataFrame({'side': [car_info['side']]}) 
        signs = pd.DataFrame({'signs': car_info['signs']})
        table = side.merge(signs, how='cross')
        return self.create_name_table('common').merge(table, how='cross')
    
    @key_error_decorator
    def create_capital_info_table(self):
        ''' creates table with capital information of country
        
        returns 
        -------
            pd.DataFrame
        '''
        capital = self.make_table_from_list('capital')
        coordinates = self.country_dict['capitalInfo']['latlng']
        table = pd.DataFrame({'latitude':[coordinates[0]], 'longitude':[coordinates[1]]})
        return capital.merge(table, how='cross')
