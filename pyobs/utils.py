#################################################################################
#
# utils.py: generic utility routines
# Copyright (C) 2020 Mattia Bruno
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#################################################################################

import numpy
import sys

__all__ = ['PyobsError','check_type','check_not_type',
        'is_verbose','set_verbose','valerr']

verbose=[]

class PyobsError(Exception):
    pass

def is_verbose(func):
    if func in verbose:
        return True
    return False

def set_verbose(func):
    if func not in verbose:
        verbose.append(func)

def valerr(v,e):
    if e>0:
        dec = -int(numpy.floor( numpy.log10(e) ))
    else:
        dec = 1
    if (dec>0):
        outstr = f'{v:.{dec+1}f}({e*10**(dec+1):02.0f})'
    elif (dec==0):
        outstr = f'{v:.{dec+1}f}({e:02.{dec+1}f})'
    else:
        outstr = f'{v:.0f}({e:.0f})'
    return outstr

def check_type(obj,s,*t):
    c=0
    for tt in t:
        if not type(obj) is tt:
            c+=1
    if c==len(t):
        raise TypeError(f'Unexpected type for {s} [{t}]')

def check_not_type(obj,s,t):
    if type(obj) is t:
        raise TypeError(f'Unexpected type for {s}')
    
#def sort_data(idx,data):
#    out = numpy.zeros(numpy.shape(data))
#    new_idx = list(numpy.sort(idx))
#    for i in range(len(new_idx)):
#        j=idx.index(new_idx[i])
#        out[i,:] = data[j,:]
#    return [new_idx, out]
