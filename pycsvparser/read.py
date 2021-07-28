"""
read.py

Part of pycsvparser

Contains functions for reading data from files.

Required 3rd party packages:
  csv

Author: Christopher Brittin

"""

import csv
import configparser
import ast

def _parse_file(fin,container,parser,comment=None, delimiter=',', 
        quotechar = ' ', quoting=csv.QUOTE_NONE,skip_header=0):
    """
    Wrapper for parsing files. 
    
    Parameters
    ----------
    fin: <str> Path to input file
    container: A data structure used to hold the data. container type must be 
        compatible with the parser.
    parser: <function> A function that parses each row in the csv file
    delimiter: <str,optional,default:' '> row delimeter
    

    """
    with open(fin, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for i in range(skip_header): next(reader)
        for row in reader:
            if comment and row[0][0] == comment: continue
            parser(container,row)
        
def parse_file(func):#fin,container,parser,comment=None, delimiter=',', 
    #    quotechar = ' ', quoting=csv.QUOTE_NONE,skip_header=0):
    """
    Wrapper for parsing files. 
    
    Parameters
    ----------
    fin: <str> Path to input file
    container: A data structure used to hold the data. container type must be 
        compatible with the parser.
    parser: <function> A function that parses each row in the csv file
    delimiter: <str,optional,default:' '> row delimeter
    

    """
    
    def wrapper(fin,container,comment=None, delimiter=',', 
            quotechar = ' ', quoting=csv.QUOTE_NONE,skip_header=0,**kwargs):
        with open(fin, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            for i in range(skip_header): next(reader)
            for row in reader:
                if comment and row[0][0] == comment: continue
                func(row,container,**kwargs)
            
    return wrapper

@parse_file
def into_list(row,container,**kwargs):
    container.append(row[0]) 

@parse_file
def into_list_dtype(row,container,**kwargs): 
    container.append(kwargs['dtype'](row[0])) 

@parse_file
def into_list_multi(row,container,**kwargs):
    container.append(row)

def _into_list(fin,dtype=None,multi_dim=False,**kwargs):
    """
    Read data from file into a list. 

    Parameters
    ----------
    fIn : <str> Path to input file
    dtype: <dtype, optional, defalut: None> data type of list entries
    multi_dim : <bool,optional,default:False> Read items as list
    kwargs: see parse_file function
    """
    if multi_dim:
        if dtype: 
            def parser(container,row):
                container.append([r for r in map(dtype,row)])
        else:
            def parser(container,row):
                container.append(row)
    else:
        if dtype: 
            def parser(container,row):
                container.append(dtype(row[0]))
        else:
            def parser(container,row):
                container.append(row[0])
    container = []
    parse_file(fin,container,parser,**kwargs)
    return container

def into_dict(fin,ktype=None,itype=None,multi_dim=False,**kwargs):
    """
    Read data from file into a dictionary. By default
    first element of each row is assigned to the key
    and the second element is assigned to the value.

    Parameters
    ----------
    fin : <str> Path to input file
    ktype: <dtype, optional, defalut: None> data type of keys
    itype: <dtype, optional, defalut: None> data type of items
    multi_dim : <bool,optional,default:False> Read items as list
    kwargs: see parse_file function
    """
    if multi_dim:
        if itype: 
            def parser(container,row):
                container[row[0]] = [r for r in map(itype,row[1:])]
        else:
            def parser(container,row):
                container[row[0]] = row[1:]
    else:
        if itype: 
            def parser(container,row):
                container[row[0]] = itype(row[1])
        else:
            def parser(container,row):
                container[row[0]] = row[1]

    container = {}
    parse_file(fin,container,parser,**kwargs)
    if ktype: container = dict([(ktype(k),v) for (k,v) in container.items()])
    return container


def into_map(fin,ktype=None,itype=None,multi_dim=True,**kwargs):
    """
    Creates a dictionary map where all elements in the row are mapped to 
    the first element in the row
    
    Parameters
    ----------
    fin : <str> Path to input file
    ktype: <dtype, optional, defalut: None> data type of keys
    itype: <dtype, optional, defalut: None> data type of items
    multi_dim : <bool,optional,default:True> Read keys as list
    kwargs: see parse_file function
    """
    
    if multi_dim:
        if ktype: 
            def parser(container,row):
                for r in map(ktype,row[1:]): container[r] = row[0]
        else:
            def parser(container,row):
                for r in row[1:]: container[r] = row[0]
    else:
        if ktype: 
            def parser(container,row):
                container[ktype(row[1])] = row[0]
        else:
            def parser(container,row):
                container[row[1]] = row[0]

    container = {}
    parse_file(fin,container,parser,**kwargs)
    if itype: container = dict([(k,itype(v)) for (k,v) in container.items()])
    return container


