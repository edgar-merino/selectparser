# selectparser

Get the tables used on a valid SQL SELECT statement from a SQL script file. This utility is implemented using sqlparser library.

## Usage

### Standalone execution

``python selectparser.py <filename>``

Where:

- ``filename`` File with the SQL SELECT sentence to analyze

#### Output

Prints the list of tables used within the SELECT sentence including sub queries.
Sub-selects used on columns are not yet implemented.


### Libraries

```python
from selectparser import get_tables_from_sql, get_tables_from_script

get_tables_from_sql('select * from table') # returns ['table']
get_tables_from_script(filename)           # returns the tables used on filename script
```

## RST Links and references
- sqlparser project: https://github.com/andialbrecht/sqlparse


## Copyright & License

Copyright (c) 2021, Edgar Merino. MIT License.

