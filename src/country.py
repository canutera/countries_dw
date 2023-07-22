import pandas as pd
from typing import Literal

class Country:
    '''
    en: a base class to parse a country dictionary of countries api
    pt: uma classe base para analisar um dicionário recebido da countries api

    Attributes
    ----------
    fields_to_parse : list[str]
        name of keys in dictionary to be parsed

    name_table : pd.DataFrame
        table containing common and official names of country

    lang_table : pd.DataFrame
        table containing official languages of country



    '''
    fields_to_parse: list = ['name', 'independent', 'unMember', 'currencies', 'capital', 'region',
                             'subregion', 'languages', 'translations', 'latlng', 'landlocked', 'borders', 'area',
                             'demonyms', 'flag', 'maps', 'population', 'gini', 'car', 'timezones', 'continents', 'flags',
                             'startOfWeek', 'capitalInfo', 'postalCode', 'coatOfArms']
    name_table: pd.DataFrame
    top_level_domain_table: pd.DataFrame
    lang_table: pd.DataFrame

    def __repr__(self):
        return f'Country ({self.common_name})'

    def __init__(self, country_dict: dict) -> None:
        self.country_dict = country_dict
        self.common_name = country_dict['name']['common']
    
    def parse_tables(self)->None:
        '''parses and sets attributes tables of a Country object
        '''
        self.name_table = self.get_table_name()
        self.top_level_domain_table = self.make_table_from_list('tld')
        self.code_table = self.create_code_table()
        self.independency_table = self.create_independency_table()
        self.un_membership_table = self.create_un_membership_table()
        self.currency_table = self.make_table_from_list('currencies')
        self.idd_table = self.make_table_from_dict('idd')
        self.lang_table = self.create_language_table()

    def print_fields(self):
        '''en: Print all available fields from a country
        pt_br: Printa todos os campos de um pais
        '''
        for i in self.fields_to_parse:
            print(f'{i}: {self.country_dict[i]}')

    def make_table_from_dict(self, field: str) -> pd.DataFrame:
        '''
        en: Makes a table from a dict, the key will be the name of the columns and the value will be the value inside the cell. Return a one line pd.DataFrame
        pt_br: Faz uma tabela a partir de um dicionário, a chave será o nome da coluna e o valor será o valor da célula. Retorn um pd.DataFrame de tamanho 1
        '''
        if not isinstance(self.country_dict[field], dict):
            raise TypeError('O valor do campo informado não é um dicionário')
        country_record = {i: [self.country_dict[field][i]] for i in self.country_dict[field] if not isinstance(self.country_dict[field][i], dict)}
        return pd.DataFrame(country_record)

    def make_key_value_table_from_dict(self, field: str, columns=['col1', 'col2']) -> pd.DataFrame:
        '''
        en: Makes a table from a dict, where every key is a columns and the values are another column. Column names can be especified
        pt_br: Faz uma tabela a partir de um dicionário, onde todas as chaves são uma coluna e os valores são outra.  Os nome de coluna podem ser especificados
        '''
        assert len(columns) == 2, 'Informe somente duas colunas. len(columns) must be 2.'
        _dict = self.country_dict[field]
        return pd.DataFrame(
            {
                columns[0]: [i for i in _dict],
                columns[1]: [_dict[i] for i in _dict],
            }
        )

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
        dic['common'] = [self.common_name] * len(self.country_dict[field])
        return pd.DataFrame(dic)[['common', field]]

    def get_table_name(self, cols: Literal['common', 'official', None] = None) -> pd.DataFrame:
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
        if cols is None:
            return self.make_table_from_dict('name')
        if isinstance(cols, str):
            cols = [cols]
        return self.make_table_from_dict('name')[cols]

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
        common_name = self.get_table_name('common')
        self.lang_table = common_name.merge(langs, how='cross')
        return self.lang_table

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

        fields = ["cca2", "ccn3", "cca3", "cioc", "status"]
        self.code_table = pd.DataFrame(
            {i: [self.country_dict[i]] for i in fields})
        return self.get_table_name('common').merge(self.code_table, how='cross')

    def create_independency_table(self):
        '''creates a table containing common name and independency flag (y/n)

        returns
        -------
        pd.DataFrame
        '''
        fields = ['independent']
        self.code_table = pd.DataFrame(
            {i: ['y' if self.country_dict[i] else 'n'] for i in fields})
        return self.get_table_name('common').merge(self.code_table, how='cross')

    def create_un_membership_table(self):
        '''creates a table containing common name and unMember flag (y/n)

        returns
        -------
        pd.DataFrame
        '''
        fields = ['unMember']
        self.code_table = pd.DataFrame(
            {i: ['y' if self.country_dict[i] else 'n'] for i in fields})
        return self.get_table_name('common').merge(self.code_table, how='cross')