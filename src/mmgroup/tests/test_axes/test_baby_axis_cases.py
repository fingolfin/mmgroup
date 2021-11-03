
from random import randint
import numpy as np
from collections import defaultdict

import datetime
import time
import pytest

from mmgroup import MM0, MMSpace, MMV
from mmgroup.mm15 import op_2A_axis_type as mm_op15_2A_axis_type

from mmgroup.generators import gen_leech2_reduce_type2
from mmgroup.generators import gen_leech2_reduce_type2_ortho
from mmgroup.tests.test_axes.test_import import AXES, BABY_AXES
from mmgroup.tests.test_axes.test_reduce_axis import short, span, radical
from mmgroup.tests.test_axes.test_reduce_axis import leech_type
from mmgroup.tests.test_axes.test_reduce_axis import eval_A_vstart

V = MMV(15)


V_START_TUPLE = ("I", 3, 2)
V_START = V(*V_START_TUPLE)
V_OPP = V_START * MM0('x', 0x200)

v_start = 0x200


FINAL_2A0_AXES = [  V_OPP * MM0('t', e) for e in range(3) ]


#######################################################################################


def reduce_2A0(v):
    vt = mm_op15_2A_axis_type(v.data) & 0xffffff
    return [vt ^ v_start]

def reduce_2B(v):
    return span(v, 4)

def reduce_4A(v):
    return [mm_op15_2A_axis_type(v.data) & 0xffffff]

def reduce_4BC(v):
    return radical(v, 1)

def reduce_6A(v):
    vt = mm_op15_2A_axis_type(v.data) & 0xffffff
    a = short(v, 5)
    return [v ^ vt for v in a]

def reduce_6C(v):
    return span(v, 3)



def reduce_10A(v):
    v2 = short(v, 1)
    assert len(v2) == 100, hex(len(v2))
    v0 = short(v, 3)
    assert len(v0) == 1, hex(len(v0))
    return [x ^ v0[0] for x in v2]



reduce_cases = {
   "2A1": reduce_2A0,
   "2A0": reduce_2A0,
   "2B1": reduce_2B,
   "2B0": reduce_2B,
   "4A1": reduce_4A,
   "4B1": reduce_4BC,
   "4C1": reduce_4BC,
   "6A1": reduce_6A,
   "6C1": reduce_6C,
   "10A1": reduce_10A,
}



#######################################################################################


reduce_targets = {
   "2A1": None,    
   "2A0": ["2A1"],    
   "2B1": ["2A1"],    
   "2B0": ["2A0"],    
   "4A1": ["2A1"],    
   "4B1": ["2B1"],    
   "4C1": ["2B1"],    
   "6A1": ["4A1"],    
   "6C1": ["4A1"],    
   "10A1": ["6A1"],    
}

#######################################################################################

def baby_axis_type(v, e = 0):
    axis_type = v.axis_type(e)
    axis_type += str(int(eval_A_vstart(v.data) != 0))   
    return axis_type



#for v in FINAL_2A0_AXES:
#    print(baby_axis_type(v), v)



@pytest.mark.axes
def test_cases(verbose = 0):
    if verbose: print("\n")
    r = np.zeros(10, dtype = np.uint32)
    for axis_type, g_str in BABY_AXES.items():
        if verbose:
            print("Test reduction of axis type %s" % axis_type)
        # Construct an axis v of the given axi type
        v = V_OPP * MM0(g_str)
        target_axes = reduce_targets[axis_type]
        if target_axes is None:
            if verbose:
                print("  Reduction terminates here")
            continue
        nfound = 0
        dict_found = defaultdict(int)
        for w in reduce_cases[axis_type](v):
            if leech_type(w) != 4 or leech_type(w ^ v_start) != 2:
                continue
            w ^= v_start
            len_r = gen_leech2_reduce_type2_ortho(w, r)
            assert len_r >= 0
            v1 = v * MM0('a', r[:len_r])
            nfound += 1
            ok = False
            if axis_type == "2A0":
                e = 1 + (v1["C",3,2] == 2)
                v2 = v1 * MM0('t', e)
                ok = v2 == V_OPP
                dict_found = {"2A1":1}
            else:
                for e in [1,2]:
                    t_axis_type = baby_axis_type(v1, e)
                    #print(t_axis_type, target_axes)
                    if t_axis_type in target_axes:
                        ok = True
                        dict_found[t_axis_type] += 1
            assert ok
        assert nfound > 0
        if verbose:
            if len(dict_found):
                print("  Reduced to axis types", dict(dict_found))

 


