"""
@name: test_read.py
@description:
Testing functions for read functions

@author: Christopher Brittin
@email: "cabrittin"+ <at>+ "gmail"+ "."+ "com"
@date: 2019-12-05
"""

import sys
sys.path.append('pycsvparser')

from pycsvparser import read


f1 = 'data/test1.csv'
f2 = 'data/test2.csv'
f3 = 'data/test3.csv'
f4 = 'data/test4.csv'

print("Read into list")
d = read.into_list(f1)
print(d)

print("Read into list int")
d = read.into_list(f1,dtype=int)
print(d)


print("Read into multi_dim list")
d = read.into_list(f2, multi_dim=True, skip_header=1)
print(d)

print("Read into dict")
d = read.into_dict(f2,skip_header=1)
print(d)

print("Read into multi_dim dict")
d = read.into_dict(f3,multi_dim=True,skip_header=1)
print(d)

print("Read into multi_dim dict itype=int")
d = read.into_dict(f3,itype=int,multi_dim=True,skip_header=1)
print(d)

print("Read into multi_dim dict ktype=int,itype=int")
d = read.into_dict(f4,ktype=int,itype=int,multi_dim=True,skip_header=1)
print(d)

print("Read into map ktype=int")
d = read.into_map(f3,ktype=int,skip_header=1)
print(d)

print("Read into map ktype=int,itype=int")
d = read.into_map(f4,ktype=int,itype=int,multi_dim=False,skip_header=1)
print(d)

