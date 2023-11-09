from hook.countries_hook import CountriesHook
file_format = 'csv'
(CountriesHook()
    .parse_countries()
    .parse_tables()
    .save_tables(file_format, index=False)
)
