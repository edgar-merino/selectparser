#! python
# -*- coding: utf-8 -*-

'''
Get the tables used on a valid SQL SELECT statement from a SQL script file. 
This utility is implemented using sqlparser library.
'''

# standard libraries
import sys, os, re
# third party libraries
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword

def remove_outer_par(text):
    '''Remove outer parenthesis around a string'''
    count=0
    ret=''
    for chr in text:
        if chr=='(':
            if count > 0:
                ret += chr
            count += 1
        elif chr==')':
            count -= 1
            if count > 0:
                ret += chr
            elif count == 0:
                return ret
        elif chr != ' ' and count == 0:
            return text
        else:
            ret+=chr
    return ret

def get_tables_from_sql(sql, level=0):
    '''List of tables from a valid SQL select statement, subqueries used on
    columns are not parsed'''
    statements = list(sqlparse.parse(sql))
    first=True
    result=[]
    for statement in statements:
        key=None
        for item in statement.tokens:
            if first:
                if isinstance(item, IdentifierList) or isinstance(item, Identifier):
                    #print('-'*level, item.value)
                    return item.value.split(',')
                first=False
            if item.ttype is Keyword and (item.value.upper() == 'FROM' or 'JOIN' in item.value.upper()):
                key=item.value
            if key is not None and item.ttype is None:
                result.extend(get_tables_from_sql(remove_outer_par(item.value), level+1))
                key=None
    return result

def get_tables_from_script(infile):
    '''List of tables from a valid SQL select statement on the specified file, 
    subqueries used on columns are not parsed. Only one sentece per file is 
    allowed'''
    if not os.path.isfile(infile):
        raise Exception(f"File {infile} does not exists, please verify")

    sql=open(infile).read()
    sql=re.sub('--.*','',sql)

    result=get_tables_from_sql(sql)
    return result

if __name__ == '__main__':
    """Get the tables used on a SQL SELECT statement from a SQL script file"""
    if len(sys.argv) < 2:
        print("No file provided, please verify.")
        sys.exit(1)

    infile=sys.argv[1]

    result=get_tables_from_script(infile)
    print(result)
