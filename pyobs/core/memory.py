#################################################################################
#
# memory.py: routines for the monitoring of the memory used by the library
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

import sys, os, numpy

book = {}
MB=1024.**2
GB=1024.**2

def get_size(obj):
    size=sys.getsizeof(obj)
    if isinstance(obj,dict):
        size += sum([get_size(v) for v in obj.values()])
        size += sum([get_size(k) for k in obj.keys()])
    elif isinstance(obj,numpy.ndarray):
        size += obj.nbytes
    elif hasattr(obj,'__dict__'):
        size += get_size(obj.__dict__)
    elif hasattr(obj,'__iter__') and not isinstance(obj,(str,bytes,bytearray)):
        size += sum([get_size(i) for i in obj])
    return size

def add(obj):
    book[id(obj)] = get_size(obj)
    
def rm(obj):
    del book[id(obj)]

def get(obj):
    size=book[id(obj)]
    if size>MB:
        return f'{size/MB:.0f} MB'
    else:
        return f'{size/1024.:.0f} KB'
    
def memory():
    size=0
    for k in book.keys():
        size += book[k]
    if size>MB:
        print(f'pyobs allocated memory {size/MB:.0f} MB\n')
    else:
        print(f'pyobs allocated memory {size/1024.:.0f} KB\n')
        
def sysmem():
    # -a: All users; -m: Sort by memory usage; -c: prints only executable name; -x: prints all background processes
    # -orss: rss is resident set size
    cmd="ps -c -a -x -m -orss | awk '{ sum += $1 } END {print sum}'"
    out=os.popen(cmd).readlines()[0].rsplit()[0]
    size=int(out)
    print(f'System allocated memory {size/GB:.2f} GB \n') 
