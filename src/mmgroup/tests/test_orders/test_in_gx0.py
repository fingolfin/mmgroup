import numpy as np
import pytest

from mmgroup import MM
import mmgroup.mm_order

from mmgroup.mat24 import ploop_theta
from mmgroup.generators import gen_leech3to2_type4
from mmgroup.generators import gen_leech2_reduce_type4
from mmgroup.clifford12 import chk_qstate12
from mmgroup.clifford12 import uint64_parity
from mmgroup.clifford12 import leech3matrix_watermark_perm_num
from mmgroup.clifford12 import leech2matrix_solve_eqn


from mmgroup.mm_order import get_order_vector
from mmgroup import MM0Group, MM0, MM
from mmgroup.mm import mm_vector

from mmgroup.mm15 import op_copy as mm_op15_copy
from mmgroup.mm15 import op_compare as mm_op15_compare
from mmgroup.mm15 import op_word as mm_op15_word
from mmgroup.mm15 import op_word_tag_A as mm_op15_word_tag_A 
from mmgroup.mm15 import op_omega as mm_op15_omega 
from mmgroup.mm15 import op_order_find_in_Gx0 as mm_op15_order_find_in_Gx0
from mmgroup.mm15 import op_order_find_in_Qx0 as mm_op15_order_find_in_Qx0
from mmgroup.mm15 import op_order_check_in_Gx0 as mm_op15_order_check_in_Gx0
from mmgroup.mm15 import op_norm_A as mm_op15_norm_A
from mmgroup.mm15 import op_eval_A_rank_mod3 as mm_op15_eval_A_rank_mod3 

from mmgroup.mm import mm_aux_mmv_extract_sparse_signs


###########################################################################
# Python implementation of check_mm_in_g_x0() using low-level functions
###########################################################################

# Here we implement the python version of function check_mm_in_g_x0()
# that has been used in the development phase.

get_order_vector()
from mmgroup.mm_order import get_order_tag_vector, check_mm_in_g_x0
from mmgroup.mm_order import OFS_NORM_A, OFS_DIAG_VA, OFS_WATERMARK_PERM
from mmgroup.mm_order import OFS_TAGS_Y, OFS_SOLVE_Y, OFS_TAGS_X
from mmgroup.mm_order import OFS_SOLVE_X, OFS_TAG_SIGN 

FAST =  False

err_in_g_x0 = 0 


ORDER_VECTOR = get_order_vector()
ORDER_TAGS = get_order_tag_vector()


def find_in_Q_x0(w):
    global err_in_g_x0
    if FAST:
        v = ORDER_VECTOR.data
        res = mm_op15_order_find_in_Qx0(w, ORDER_TAGS, v)
    w_x = mm_aux_mmv_extract_sparse_signs(15, w, 
        ORDER_TAGS[OFS_TAGS_X:], 24)
    if w_x < 0:
        err_in_g_x0 = 7
        return None
    x = leech2matrix_solve_eqn(ORDER_TAGS[OFS_SOLVE_X:], 24, w_x)
    w_sign = ((x >> 12) & 0x7ff) ^ (x & 0x800)
    aa = np.array(ORDER_TAGS[OFS_TAG_SIGN:] ^ (w_sign << 14),
        dtype = np.uint32)
    sign = mm_aux_mmv_extract_sparse_signs(15, w, aa, 1)
    if sign < 0:
        err_in_g_x0 = 8
        return None
    x &= 0xffffff
    sign ^= uint64_parity(x & (x >> 12) & 0x7ff)
    x ^=  (sign & 1) << 24
    x ^= ploop_theta(x >> 12)
    #print("final x =", hex(x))
    return x


def find_in_G_x0(w):
    global err_in_g_x0
    g1i = np.zeros(11, dtype = np.uint32)
    if FAST:
        v = ORDER_VECTOR.data
        res =  mm_op15_order_find_in_Gx0(w, ORDER_TAGS, v, g1i)
        assert res >= 0
        if res >= 0x100:
            err_in_g_x0 = res - 0x100
            return None
        return g1i[:res]

    if mm_op15_norm_A(w) != ORDER_TAGS[OFS_NORM_A]:
        err_in_g_x0 = 1
        return None        
    w3 = mm_op15_eval_A_rank_mod3(w, ORDER_TAGS[OFS_DIAG_VA])
    w3 &= 0xffffffffffff
    if w3 == 0: 
        err_in_g_x0 = 2
        return None
    w_type4 = gen_leech3to2_type4(w3)
    if w_type4 == 0: 
        err_in_g_x0 = 3
        return None
    wA = np.array(w[:2*24], copy = True)
    len_g1 = gen_leech2_reduce_type4(w_type4, g1i)
    assert 0 <= len_g1 <= 6 
    res = mm_op15_word_tag_A(wA, g1i, len_g1, 1)
    assert res == 0
    perm_num = leech3matrix_watermark_perm_num(15, 
        ORDER_TAGS[OFS_WATERMARK_PERM:], wA)
    if perm_num < 0: 
        err_in_g_x0 = 4
        return None
    if perm_num > 0:
        g1i[len_g1] = 0xA0000000 + perm_num 
        res = mm_op15_word_tag_A(wA, g1i[len_g1:], 1, 1)
        assert res  == 0
        len_g1 += 1
    v_y = mm_aux_mmv_extract_sparse_signs(15, wA, 
        ORDER_TAGS[OFS_TAGS_Y:], 11)
    if v_y < 0:
        err_in_g_x0 = 5
        return None
    y = leech2matrix_solve_eqn(ORDER_TAGS[OFS_SOLVE_Y:], 11, v_y)
    if y > 0:
        g1i[len_g1] = 0xC0000000 + y
        res = mm_op15_word_tag_A(wA, g1i[len_g1:], 1, 1)
        assert res  == 0
        len_g1 += 1
    if (wA != ORDER_VECTOR.data[:2*24]).all():
        err_in_g_x0 = 6
        return None
    #print("g1i", g1i[:len_g1])
    return g1i[:len_g1]


def low_level_check_mm_in_g_x0(g):
    """Check if ``g`` is in the subgroup ``G_x0`` of the monster
   
    If ``g`` is in the subgroup ``G_x0`` of the monster then the
    function changes the word representing ``g`` to a (uniquely 
    defined) word in the generators of the subgroup ``G_x0`` and
    returns ``g``.  
    
    Otherwise the function does not change ``g`` and returns ``None``.
    
    ``g`` must be an instance of class 
    ``mmgroup.mm_group.MMGroupWord``.
    """
    global err_in_g_x0
    err_in_g_x0 = 0
    assert isinstance(g, (MM0, MM))
    v = ORDER_VECTOR.data
    w = mm_vector(15)
    work = mm_vector(15)
    mm_op15_copy(v, w)
    res = mm_op15_word(w.data, g.mmdata, len(g), 1, work)
    assert res == 0
    if FAST:
        g1 = np.zeros(11, dtype = np.uint32)
        res = chk_qstate12(mm_op15_order_check_in_Gx0(w, g1))
        if res >= 0x100:
            err_in_g_x0 = res - 0x100
            return None
        assert res < 11
        g._extend(res)
        g.length = res
        g._data[:res] = g1[:res]
        g.reduced = 0
        g.reduce()
        return g

    g1i = find_in_G_x0(w)
    if g1i is None:
        return None
    res = mm_op15_word(w, g1i, len(g1i), 1, work)
    assert res == 0

    x = find_in_Q_x0(w)
    if x == None:
        return None

    g2i = np.array([0x90000000 + (x & 0xfff), 
        0xB0000000 + ((x >> 12) & 0x1fff)], dtype = np.uint32)
    res = mm_op15_word(w, g2i, 2, 1, work)  
    assert res == 0   
    g1i = np.append(g1i, g2i)
 
    assert res == 0   
    if mm_op15_compare(v, w):
        #print("vW", v, "\n",  w)
        err_in_g_x0 = 9
        return None

    g._extend(11)
    g.length = len(g1i)
    g.reduced = 0
    for i in range(len(g1i)):
        g._data[i] = g1i[len(g1i) - 1 - i] ^ 0x80000000
    g.reduce()
    return g
    



###########################################################################
# Test data for function  check_mm_in_g_x0() 
###########################################################################


def in_gx0_testdata():
    """Test data for testing function mgroup.mm_order.check_mm_in_g_x0

    The function yields pairs ``(g, b)``. Here ``g`` an element of the
    monster group ``MM``, and ``b`` is True iff ``g`` is in the
    subgroup ``G_x0`` of the monster group.
    """
    # Yield some fixed test data
    testdata = [
      ([], True),
      ([('d', 2)], True),
      ([('d', 0x801)], True),
      ([('x', 0xA71)], True),
      ([('x', 0x1A71)], True),
      ([('y', 0xCD1)], True),
      ([('y', 0xCD1), ('x', 0x1B7f)], True),
      ([('p', 'r')], True),
      ([('l', 1)], True),
      ([(tag, 'n') for tag in "xydpl"*3], True),
      ([('t', 1)], False),
      ("M0<y_4d1h*x_0b7fh>", True),
    ]
    for g, in_g_x0 in testdata:
       yield MM0(g), in_g_x0
    # Yield elements ``g0 * t * g1``, where ``t`` is the triality 
    # element or its inverse, and ``g0 , g1`` are in ``G_x0``.
    for i in range(8):
        e = [1 + ((i >> j) & 1) for j in range(3)]
        g = [('p', 'r'), ('y', 'r'), ('l', e[0]), ('t', e[1]), ('l', e[2]),
             ('p', 'r'), ('y', 'r'), ('x', 'r'), ('d', 'r'), ]
        yield  MM0(g), False
    # Yield some less obvious examples. Let ``d`` be a random 2A 
    # involution and ``z`` be the 2B involution in the center of
    # ``G_x0``. Then ``g = z * d`` has even order ``o``, and we 
    # yield ``g ** (o/2)``, which is in ``G_x0``.
    z, d0 = MM0('x', 0x1000), MM0('d', [2,3])
    for n in range(5):
        g0 = MM0([(tag, 'n') for tag in "xydplt"*2])
        d =  d0 ** g0
        g = z * d
        o = g.order()
        assert o & 1 == 0
        yield g ** (o >> 1), True
    # Yield some elements of ``G_x0``.
    for n in range(10):
        for i in range(2,5):
            yield MM0([(tag, 'n') for tag in "xydpl"*i]), True
    

###########################################################################
# Test function  check_mm_in_g_x0() 
###########################################################################


@pytest.mark.orders
def test_in_gx0(verbose = 0):
    print("Testing function check_mm_in_g_x0()")
    for n, (g, in_g_x0) in enumerate(in_gx0_testdata()):
        g = MM0(g)
        if verbose:
            print("Test", n+1)
            print("g =", g)
        g1 = check_mm_in_g_x0(g.copy())
        if verbose:
            print("reduced", g1)
            if g1 is None:
                r = err_in_g_x0
                print("Reason for non-membership:", r)
        if in_g_x0:
            assert g1 is not None
        else:
            assert g1 is None
        if g1:
            assert g == g1 
        assert g1 == low_level_check_mm_in_g_x0(g)
        assert g.in_G_x0() == in_g_x0

