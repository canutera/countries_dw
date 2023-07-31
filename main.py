from src.countries_hook import CountriesHook
file_format = 'parquet'
(CountriesHook()
    .parse_countries()
    .parse_tables()
    .save_tables()
)
