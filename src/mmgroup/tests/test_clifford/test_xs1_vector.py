from __future__ import absolute_import, division, print_function
from __future__ import  unicode_literals



from random import randint #, shuffle, sample
from functools import reduce
from operator import __or__
from numbers import Integral

import numpy as np
import pytest

from mmgroup.structures.qs_matrix import qs_pauli_matrix
from mmgroup.structures.xs1_co1 import Xs12_Co1, str_leech3
from mmgroup.structures.xs1_co1 import get_error_pool
from mmgroup.structures.autpl import AutPL
from mmgroup.mat24 import MAT24_ORDER, ploop_theta
from mmgroup.mat24_xi import xi_op_leech
from mmgroup.tests.spaces.clifford_space import Space_ZY
from mmgroup.clifford12 import xp2co1_chain_short_3, xp2co1_elem_to_qs
from mmgroup.clifford12 import xp2co1_short_2to3, xp2co1_short_3to2
from mmgroup.clifford12 import xp2co1_find_chain_short_3

MMSpace3 = Space_ZY.mmspace
MMGroup3 = MMSpace3.group



STD_V3  = 0x8000004





#####################################################################
# Creating test vectors
#####################################################################


def rand_tuple(tag):
    if tag in "BC":
        i0 = i1 = randint(0, 23)
        while i1 == i0:
            i1 = randint(0, 23)
        return tag, i0, i1
    if tag == "T":
        return tag, randint(0, 758), randint(0, 63),
    if tag in "XY":
        return tag, randint(0, 2047), randint(0, 23),
    if tag == "d":
        return tag, randint(0, 0xfff)
    if tag == "p":
        return tag, randint(0,  MAT24_ORDER - 1)
    if tag in  "xy":
        return tag, randint(0, 0x1fff)
    if tag ==  "l":
        return tag, randint(1, 2)
    raise ValueError("Illegal tag %s for group or vector" % tag)
        

def rand_element(s):
    return [rand_tuple(tag) for tag in s]

def create_test_vectors():
    vector_data = [ 
      (0x001, (1, "B", 2, 3)),
      (0x001, (1, "C", 0, 16)),
      (0xabf, (1, "C", 15, 19)),
      (0x001, (1, "T", 643, 51)),
      (0x001, (1, "T", 199, 7)),
      (0x001, (1, "X", 0, 23)),
      (0x001, (1, "X", 137, 23)),
      (0x001, (1, "X", 1897, 1)),
    ]
    group_data = [
      [('x', 0x1f24), ('d', 0xf75)],
      [('x', 0x124), ('d', 0x555)],
      [('d', 0x124)],
      [('d', 0x800)],
      [('p', 187654344)],
      [('d', 0xd79), ('p', 205334671)],
      [('p', 205334671), ('d', 0xd79)],
      [('d', 0xd79), ('x', 0x1123)],
      [('y', 0x1d79)],
      [('y', 0x586)],
      [('l', 1)],
      [('l', 2)],
    ]
    for i in range(1):
        p = {0:2, 1:3, 2:0, 3:1, 4:4, 6:6, 8:8}
        #print("AutPL", [hex(x) for x in AutPL(p).rep])
        yield 256, (1, "B", 2, 3),  [("p", p)]
    for x4096, x24 in vector_data:
        for g in group_data:
            yield x4096, x24, g
    for x in "BCTX":
        for j in range(50):
            sign = -1**j
            d = randint(0, 0xfff)
            t = rand_tuple(x)
            yield d, ((sign,) + t),  rand_element("lydpdpxdpylx")    


#####################################################################
# Simulate the mapping of Leech lattice vectors modulo 3
#####################################################################



def tuple_to_leech3(sign, tag, i0, i1):
    x2 = MMSpace3.index_to_short_mod2(tag, i0, i1)
    x3 = xp2co1_short_2to3(x2)
    if sign == -1:
        x3 ^= 0xffffffffffff
    return x3
    


def short3_abs_equal(x1, x2):
    x1, x2 = int(x1), int(x2)
    return not bool((x1 ^ (x1 >> 24)  ^ x2 ^ (x2 >> 24)) & 0xffffff)

def map_v3(v, g, expected = None, verbose = 1):
    src = np.zeros(3, dtype = np.uint64)
    dest = np.zeros(3, dtype = np.uint64)
    src[0] = 0x8000004
    dest[0] = g.short3
    src[2] = v if isinstance(v, Integral) else tuple_to_leech3(*v)
    src[1] = xp2co1_find_chain_short_3(src[0], src[2])
    qstate = g.qs
    qstate_base = qstate.copy().gate_h(0x800800)
    xp2co1_chain_short_3(qstate, src, dest)
    ok = dest[-1] != 0
    if not expected is None:
        ok = ok and short3_abs_equal(dest[-1], expected)
    if verbose or not ok:
        print("Map a short Leech vector v by an element g of Xs2Co1:")
        if not isinstance(v, Integral):
            print("v = %s = %s" % (v, str_leech3(src[2])))
        else:
            print("v = %s" % str_leech3(src[2]))
        print("g =", str(g))
        for i in range(3):
            print(" ",  str_leech3(src[i]), "->", str_leech3(dest[i]))
        for i in range(3):
            v2 =  xp2co1_short_3to2(src[i])       
            v2c = qstate_base.pauli_conjugate(v2);
            v3c = xp2co1_short_2to3(v2c)
            print("   %s -> 0x%06x -> 0x%06x -> %s" %
                (str_leech3(src[i]), v2, v2c, str_leech3(v3c)))
            print("    Debug data pool:\n    ", 
                    [hex(x) for x in get_error_pool(15)])
        print("")
        if not expected == None:
            print("Expected result: %s" % str_leech3(expected))
        print("Obtained result: %s\n" % str_leech3(dest[-1]))
        if not ok:
            ERR = "Mapping of Leech vector failed"
            raise ValueError(ERR)
    return dest[-1]


#####################################################################
# Test multiplication of vectors with elements of G_{x1}
#####################################################################


@pytest.mark.qstate
def test_vector(verbose = 0):
    for ntest, (x4096, x24, g) in enumerate(create_test_vectors()):
        if verbose:
            print("\nTEST %s" % (ntest+1))
            print("vector =", x4096, x24)
        vm = x24[0] * Space_ZY.unit(x4096, x24[1:])
        vm_old = vm.copy()
        if verbose:
            print("vm =", vm.as_tuples())
            print("vm =", vm)
            vm.dump()
        v3 = vm.as_mmspace_vector() 
        if verbose:
            print("g =", g)
        g3 = MMGroup3(*g)
        try:
            gm = Xs12_Co1(*g)
        except ValueError:
            print("\nError in constructing group element g")
            print("Debug data pool:\n", 
                    [hex(x) for x in get_error_pool(15)])
            raise
        gm_old = gm
        if verbose:
            print("gm = ", gm)
            print("g3 = ", g3)
        try:
            wm = vm * gm
            if verbose:
                print("w = vm * gm = ", wm)
        except ValueError:
            print("Debug data pool:\n", 
                    [hex(x) for x in get_error_pool(15)])
            map_v3(x24, gm, wm.short3, verbose = 1)
            raise
        w3_op =  wm.as_mmspace_vector()
        w3_mult =  v3 * g3
        if verbose:
            print("w3_op =", w3_op)
            print("w3_op data =")
            wm.dump()
            print("w3_mult =", w3_mult)
        ok =  w3_op == w3_mult 
        assert vm == vm_old
        assert gm == gm_old
        if not ok:
            print("\nError in TEST %s" % (ntest+1))
            print("vector =", x4096, x24)
            print("v =", hex(x4096), "(x)", x24)
            print("rep of v:", vm)
            print("v =", v3)
            print("g = ", g)
            print("rep of g:", gm)
            print("Output w = v * g\nexpected:", w3_mult)
            print("obtained:", w3_op)
            print("rep:", wm)
            map_v3(x24, gm, verbose = 1)
            if not ok:
               ERR = "Vector multiplication test in group G_{x0} failed"
               raise ValueError(ERR)
            
            
            
            
            
#####################################################################
# Test conjugation with the element xi of group G_{x1}
#####################################################################



def ref_conjugate_xi(x, exp):
    x ^= ploop_theta(x >> 12)
    res = xi_op_leech(x, exp)
    return res ^  ploop_theta(res >> 12) 


def conjugate_xi(x, exp):
    elem_l = Xs12_Co1(('l', exp))
    mat_l = elem_l.qs.gate_h(0x800800)
    mat_x = qs_pauli_matrix(12, x)
    mat_res = mat_l.inv() @ mat_x @ mat_l
    return mat_res.pauli_vector()
   
@pytest.mark.qstate
def test_conjugate_xi(verbose = 0):
    for exp in [1, 2]:
        for lb_x in range(25):
            x = 1 << lb_x
            y_ref = ref_conjugate_xi(x, exp)
            y  = conjugate_xi(x, exp)
            ok = y == y_ref
            if verbose or not ok:
                print("conjugate x= 0x%06x with xi**%d" % (x, exp))
                print("expected: 0x%06x" % y_ref) 
                print("obtained: 0x%06x" % y) 
                if not ok:
                    ERR = "Error in conjugating with element l"
                    raise ValueError(ERR)

                

#####################################################################
# Test multiplication ind inversion of elements of G_{x1}
#####################################################################
           

def create_test_elements():
    for i in range(50):
        g1 = rand_element("xydplyplyplxydp")
        g2 = rand_element("xydplyplyplxydp")
        yield g1, g2

@pytest.mark.qstate
def test_group(verbose = 0):
    unit = Xs12_Co1()
    for ntest, (g1, g2) in enumerate(create_test_elements()):
        gm1 = Xs12_Co1(*g1)    
        gm2 = Xs12_Co1(*g2)    
        gm3_ref = Xs12_Co1(*(g1 + g2))    
        gm3 = gm1 * gm2
        ok = gm3 == gm3_ref 
        if verbose or not ok:
            print("\nTEST %s" % (ntest+1))
            print("element g1 =", g1)
            print("element g2 =", g2)
            print("element g1 * g2")
            print("expected:", gm3_ref)
            print("obtained:", gm3)
            if not ok:
                ERR = "Multiplication in group G_{x1} failed"
                raise ValueError(ERR)
        gq1 = gm1.qs
        gq2 = gm2.qs
        gq3 = gm3.qs  
        gq3_ref = gq1 @ gq2
        sign_q  = int(gq3 == -gq3_ref)
        assert sign_q  or  gq3_ref == gq3       

        gleech1 = gm1.leech_op
        gleech2 = gm2.leech_op
        gleech3 = gm3.leech_op  
        gleech3_ref = gleech1 @ gleech2 / 8
        sign_leech  = int((gleech3 == -gleech3_ref).all())
        assert  (gleech3 @ gleech3.T == 64 * np.eye(24)).all()       
        assert sign_leech  or  (gleech3_ref == gleech3).all()

                
        gm1i =  gm1**(-1) 
        ok = gm1 * gm1i == unit
        if verbose or not ok:
            print("g1\n",  gm1) 
            print("g1 ** -1 obtained\n",  gm1**(-1)) 
            if not ok:            
                ERR = "Inversion in group G_{x1} failed"
                raise ValueError(ERR)
            
            
