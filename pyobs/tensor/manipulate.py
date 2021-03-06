#################################################################################
#
# manipulate.py: methods for the manipulation of the shape of observables
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
import pyobs

__all__ = ['reshape','concatenate','transpose','sort','diag','repeat','tile','stack']

def reshape(x,new_shape):
    """
    Change the shape of the observable

    Parameters:
      x (obs) : observables to be reshaped
      new_shape (tuple): the new shape of the observable

    Returns:
      obs : reshaped observable

    Notes:
      This function acts exclusively on the mean
      value.
    """
    res = pyobs.observable(x)
    res.shape = new_shape
    res.mean = numpy.reshape(x.mean, new_shape)
    return res

def concatenate(x,y,axis=0):
    """
    Join two arrays along an existing axis

    Parameters:
       x, y (obs): the two observable to concatenate
       axis (int, optional): the axis along which the 
             observables will be joined. Default is 0.
    
    Returns:
       obs : the concatenated observable
    
    Notes:
       If `x` and `y` contain information from separate
       ensembles, they are merged accordingly by keeping
       only the minimal amount of data in memory.
    """
    if x.size==0 and x.shape==[]: 
        return pyobs.observable(y)
    if y.size==0 and y.shape==[]:
        return pyobs.observable(x)
    
    if len(x.shape)!=len(y.shape): # pragma: no cover
        raise pyobs.PyobsError(f'Incompatible dimensions between {x.shape} and {y.shape}')
    for d in range(len(x.shape)): # pragma: no cover
        if (d!=axis) and (x.shape[d]!=y.shape[d]):
            raise pyobs.PyobsError(f'Incompatible dimensions between {x.shape} and {y.shape} for axis={axis}')
    f = lambda xx,yy: numpy.concatenate((xx,yy), axis=axis)
    mean = f(x.mean,y.mean)
    gx = pyobs.gradient(lambda xx: f(xx,numpy.zeros(y.shape)), x.mean, gtype='extend')
    gy = pyobs.gradient(lambda yy: f(numpy.zeros(x.shape),yy), y.mean, gtype='extend')
    return pyobs.derobs([x,y], mean, [gx,gy])

def transpose(x,axes=None):
    """
    Transpose a tensor along specific axes.
    For an array a with two axes, gives the matrix transpose.

    Parameters:
       x (obs): input observable
       axes (tuple or list of ints, optional): If specified, 
            it must be a tuple or list which contains a 
            permutation of [0,1,..,N-1] where N is the number of axes of `x`. 
            For more details read the documentation of `numpy.transpose`

    Returns:
       obs : the transposed observable
    """
    f = lambda x: numpy.transpose(x, axes)
    gx = pyobs.gradient(f, x.mean, gtype='slice')
    return pyobs.derobs([x], f(x.mean), [gx])

def sort(x,axis=-1):
    """
    Sort a tensor along a specific axis.
    
    Parameters:
       x (obs): input observable
       axis (int, optional): the axis which is sorted. Default is -1, the
       last axis.

    Returns:
       obs : the sorted observable
    """
    mean = numpy.sort(x.mean,axis)
    idx = numpy.argsort(x.mean,axis)
    gx = pyobs.gradient(lambda x: numpy.take_along_axis(x,idx,axis), x.mean) # non-optimized for large number of observables
    return pyobs.derobs([x],mean,[gx])

def diag(x):
    """
    Extract the diagonal of 2-D array or construct a diagonal matrix from a 1-D array.
    
    Parameters:
       x (obs): input observable

    Returns:
       obs : the diagonally projected or extended observable
    """
    if len(x.shape)>2: # pragma: no cover
        raise pyobs.PyobsError(f'Unexpected matrix with shape {x.shape}; only 1-D and 2-D arrays are supported')
    f = lambda x: numpy.diag(x)
    if len(x.shape)==2:
        gx = pyobs.gradient(f, x.mean, gtype='slice')
    else:
        gx = pyobs.gradient(f, x.mean) # non-optimized for large number of observables
    return pyobs.derobs([x],f(x.mean),[gx])

def repeat(x,repeats,axis=None):
    """
    Repeats elements of an observables.
    
    Parameters:
       x (observable): input observable
       repeats (int): the number of repetitions of each element
       axis (int, optional): the axis along which to repeat the values.
    
    Returns:
       observable: output with same shape as `x` except along the axis 
                   with repeated elements.
    """
    f = lambda x: numpy.repeat(x, repeats=repeats, axis=axis)
    mean = f(x.mean)
    gx = pyobs.gradient(f, x.mean, gtype='full') # non-optimized for large number of observables
    return pyobs.derobs([x],mean,[gx])

def tile(x, reps):
    """
    Constructs an observable by repeating `x` `reps` times.
    
    Notes:
       Check the documentation of `numpy.tile` for more details 
       on the input arguments and function behavior.
    """
    f = lambda x: numpy.tile(x, reps)
    gx = pyobs.gradient(f, x.mean, gtype='full') # non-optimized for large number of observables
    return pyobs.derobs([x], f(x.mean), [gx])

def stack(obs, axis=0):
    """
    Join a list of observables along a new axis.
    
    Parameters:
       obs (list of observables): each observable must have the same shape
       axis (int, optional): the axis along which the observables are stacked
   
    Returns:
       observable: the stacked observables
    """
    pyobs.check_type(obs,'obs',list)
    pyobs.check_type(obs[0],'obs',pyobs.observable)
    arr = [o.mean for o in obs]
    f = lambda x: numpy.stack(x, axis=axis)
    grads = []
    for j in range(len(obs)):
        arr0 = [numpy.zeros(obs[i].shape) for i in range(0,j)]
        arr1 = [numpy.zeros(obs[i].shape) for i in range(j+1,len(obs))]
        grads += [pyobs.gradient(lambda x: f(arr0+[x]+arr1), obs[j].mean, gtype='extend')]
    return pyobs.derobs(obs, f(arr), grads)
