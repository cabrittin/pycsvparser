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


class parse_file(object):
    def __init__(self,fname,mode='r',comment=None,skip_header=0,delimiter=',',**kwargs):
        self.__fname__ = fname
        self.__mode__ = mode
        self.comment = comment
        self.skip_header = skip_header
        self.delimiter = delimiter

    def __call__(self,func,**kwargs):
        def wrapper(container,comment=None, 
                quotechar = ' ', quoting=csv.QUOTE_NONE,**kwargs):
            with open(self.__fname__,self.__mode__) as csvfile:
                reader = csv.reader(csvfile, delimiter=self.delimiter,
                                    quotechar=quotechar,quoting=quoting)
                for i in range(self.skip_header): next(reader)
                indexer = 0
                for row in reader:
                    if self.comment and row[0][0] == self.comment: continue
                    func(container,row=row,indexer=indexer,**kwargs)
                    indexer += 1
            return None
        return wrapper

def count_lines(fname,**kwargs):
    @parse_file(fname)
    def row_count(counter,**kwargs):
        counter += 1
    
    counter = 0
    row_count(counter)
    return counter

def into_list(fname,dtype=None,multi_dim=False,delimiter=',',skip_header=0,**kwargs):
    """
    Read data from file into a list. 

    Parameters
    ----------
    fname : <str> Path to input file
    dtype: <dtype, optional, defalut: None> data type of list entries
    multi_dim : <bool,optional,default:False> Read items as list
    kwargs: see parse_file function
    """
    container = []
    if multi_dim:
        if dtype: 
            @parse_file(fname,dytpe=dtype,delimiter=delimiter,skip_header=skip_header)
            def row_into_container(container,row=None,**kwargs):
                container.append([r for r in map(kwargs['dtype'],row)])
        else:
            @parse_file(fname,delimiter=delimiter,skip_header=skip_header)
            def row_into_container(container,row=None,**kwargs):
                container.append(row) 
    else:
        if dtype: 
            @parse_file(fname,dtype=dtype,delimiter=delimiter,skip_header=skip_header)
            def row_into_container(container,row=None,**kwargs):
                container.append(kwargs['dtype'](row[0]))
        else:
            @parse_file(fname,delimiter=delimiter,skip_header=skip_header)
            def row_into_container(container,row=None,**kwargs):
                container.append(row[0]) 
    row_into_container(container)
    return container

def into_dict(fname,dtype=None,multi_dim=False,**kwargs):
    """
    Read data from file into a list. 

    Parameters
    ----------
    fname : <str> Path to input file
    dtype: <dtype, optional, defalut: None> data type of list entries
    multi_dim : <bool,optional,default:False> Read items as list
    kwargs: see parse_file function
    """
    container = {}
    if multi_dim:
        if dtype: 
            @parse_file(fname,dytpe=dtype)
            def row_into_container(container,row=None,**kwargs):
                container[row[0]] = [r for r in map(kwargs['dtype'],row[1:])]
        else:
            @parse_file(fname)
            def row_into_container(container,row=None,**kwargs):
                container[row[0]] = row[1:] 
    else:
        if dtype: 
            @parse_file(fname,dtype=dtype)
            def row_into_container(container,row=None,dtype=dtype,**kwargs):
                container[row[0]] = dtype(row[1])
        else:
            @parse_file(fname)
            def row_into_container(container,row=None,**kwargs):
                container[row[0]] = row[1] 
    row_into_container(container)
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

def into_lr_dict(fin):
    """
    Creates left/rigth dictionary for cells

    Parameters
    ----------
    fIn : str
      Path to file specifying left/right cells. Should have format
      'left_cell,right_cell'
    """   
    lr = into_dict(fin)
    _keys = list(lr.keys())
    for key in _keys:
        lr[lr[key]] = key
    return lr

