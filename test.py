"""
A file for creating unit tests

Run in spyder with
 !python -m pytest test.py
"""

from djsetslow import ListSet, IDsSet
from unionfind import UFNaive, UFFast
import numpy as np
import matplotlib.pyplot as plt
import time
    
def site_example(DJSet):
    """
    Test the example from the web site on all types of disjoint sets
    Parameters
    ----------
    DJSet: Class
        A class type for a disjoint set.  Assumed to have a constructor
        with the number of elements, and the methods union(i, j) and
        find(i, j)
    """
    s = DJSet(10)
    s.union(0, 2)
    s.union(1, 8)
    s.union(8, 7)
    assert(not s.find(0, 3))
    assert(s.find(1, 7))
    s.union(1, 6)
    s.union(0, 1)
    assert(s.find(0, 7))
    assert(not s.find(1, 9))

def test_site_example_ListSet():
    site_example(ListSet)

def test_site_example_IDsSet():
    site_example(IDsSet)

def test_site_example_UFNaive():
    site_example(UFNaive)

def test_site_example_UFFast():
    site_example(UFFast)

def do_stress_test(N, set_types):
    np.random.seed(0)
    # Create a random partition with at most 50 components
    n_part = np.random.randint(min(N, 50))
    bds = np.sort(np.random.permutation(N)[0:n_part])
    n_ops = min(N*N, 40*int(np.log2(N))*N)
    djsets = [s(N) for s in set_types]
    times = np.zeros((n_ops, len(set_types)))
    ops = np.zeros(n_ops)
    for op in range(n_ops):
        ## Randomly choose two elements in the collection
        i = np.random.randint(N)
        j = np.random.randint(N)
        ops[op] = np.random.randint(2)
        if ops[op] == 0:
            ## Do a union on i and j for each type of disjoint set
            for k, djset in enumerate(djsets):
                tic = time.time()
                djset.union(i, j)
                times[op, k] = time.time()-tic
        else:
            # Do a find, and check to make sure all different data 
            # structures agree on the find at this point
            find_res = []
            for k, djset in enumerate(djsets):
                tic = time.time()
                find_res.append(djset.find(i, j))
                times[op, k] = time.time()-tic
            # Make sure they all came up with the same answer by 
            # forming a set and making sure it only has one element
            assert(len(set(find_res)) == 1)
    return times[ops == 0, :], times[ops == 1, :]

def test_stress100():
    do_stress_test(100, [IDsSet, UFNaive, UFFast])
