r"""We deal with the representation of elements of the monster group. 

Conway :cite:`Con85` has constructed a ``196884``-dimensional rational 
representation :math:`\rho` of the monster :math:`\mathbb{M}` based on 
representations of two subgroups 
:math:`G_{x0} = 2_+^{1+24}.\mbox{Co}_1` and 
:math:`N_0 = 2^{2+11+22}.( M_{24} \times S_3)` of 
:math:`\mathbb{M}` which generate :math:`\mathbb{M}`. 
Here :math:`G_{x0}` has a normal extraspecial ``2``-subgroup 
:math:`2_+^{1+24}` with factor group :math:`\mbox{Co}_1`, where
:math:`\mbox{Co}_1` is the automorphism group of the Leech lattice
modulo ``2``. The group :math:`N_0` has a normal subgroup
:math:`2^{2+11+22}`, which is a certain ``2`` group and the factor
group is a direct product of the Mathieu group :math:`M_{24}`
and the symmetric permutation group :math:`S_3` of ``3`` elements.

The group :math:`N_{x0} = N_0 \cap G_{x0}` has index ``3`` in
:math:`N_{0}` and structure :math:`2^{1+24} . 2^{11} . M_{24}`.
It is generated by elements  :math:`x_\delta`, :math:`x_\pi`, 
:math:`x_e`, :math:`y_e`, :math:`z_e`, for all
:math:`x_\delta \in \mathcal{C}^*`, 
:math:`\pi \in {{\rm Aut}_{{\rm St}} \mathcal{P}}` and 
:math:`e \in  \mathcal{P}`.

Here  :math:`\mathcal{C}^*` is the Golay cocode defined in
section  :ref:`golay-label`, :math:`\mathcal{P}` is the Parker
loop defined in section  :ref:`parker-loop-label`, and 
:math:`{{\rm Aut}_{{\rm St}} \mathcal{P}}` is the automorphism 
group of  :math:`\mathcal{P}` defined in section  
:ref:`aut_ploop_label`.
The group :math:`N_{0}` has a subgroup isomorphic to
:math:`{{\rm Aut}_{{\rm St}} \mathcal{P}}` generated by the
generators  :math:`x_\delta, \delta \in \mathcal{C}^*`
and :math:`x_\pi,  \pi \in {{\rm Aut}_{{\rm St}} \mathcal{P}}`.
The generators  :math:`x_\delta` generate the subgroup of diagonal
automorphisms of :math:`{{\rm Aut}_{{\rm St}} \mathcal{P}}`. 


The group :math:`N_{0}` is generated by :math:`N_{x0}` and by 
another element :math:`\tau` of :math:`N_{0}` or order ``3``. The
group :math:`G_{x0}` is generated by :math:`N_{x0}` and by another
element  :math:`\xi` of :math:`G_{x0}` or order ``3``. The elements
:math:`x_\delta`, :math:`x_\pi`, :math:`x_e`, 
:math:`y_e`, :math:`z_e`,  :math:`\tau` and  :math:`\xi`  
generate the monster group  :math:`\mathbb{M}`.
In this  package we use the definitions of the generators 
in  :cite:`Seysen20`, which incorporate a modification of 
:cite:`Con85` made in :cite:`Iva09`. 
This leads to simpler relations in  :math:`N_{0}`.
The generators :math:`x_e`, :math:`y_e`, and :math:`z_e` in  
:cite:`Seysen20` correspond to the generators
:math:`x_e \cdot z_{-1}^{|e/4|}`, :math:`y_e \cdot x_{-1}^{|e/4|}`,
and  :math:`z_e \cdot y_{-1}^{|e/4|}`` in :cite:`Con85`.
 
For dealing with the monster :math:`\mathbb{M}` the user must 
first create an instance ``M`` of class |MMGroup|, which 
represents an instance of the monster group :math:`\mathbb{M}`::

      M = MMGroup()


A user can create several disjoint instances of :math:`\mathbb{M}`. Elements
of the monster are created by calling that instance ``M`` as a function with
a variable number of arguments. Here each argument describes an element of
:math:`\mathbb{M}` which is (usually) one of the generators listed above.
The the function returns the product of all these elements as an instance
of class |MMGroupWord|. Instances of class  |MMGroupWord| model elements
of (an instance of) the Monster group :math:`\mathbb{M}`.

An argument passed to an instance ``M`` of class  |MMGroup| may be a pair 
``(tag, value)``, where ``tag`` is a single small letter describing the 
type of the generator of :math:`\mathbb{M}`, and ``value`` is an 
integer describing the value of that generator. Alternatively, ``value``
may be an instance of the appropriate algebraic structure used for
indexing a generator of a given type as indicted in the table below.

Math papers may use (at least) Latin or Greek letters for labelling
objects, but most programming languages are restricted to ASCII characters.
Assuming that ``M`` is an instance of class  |MMGroup| representing
a monster group, the following table shows how to create generating
elements of ``M``: 


.. table:: Construction of generating elements of the monster
  :widths: 10 90


  ===================  ==========================================================
  Element              Construction as an element of ``M``, 
                       with ``M`` of type |MMGroup|
  ===================  ==========================================================
  :math:`x_\delta`     ``M(('d', delta))``, ``delta`` an instance of class
                       |Cocode|; 

                       ``M(('d', delta))`` returns 
                       ``M('d', Cocode(delta))`` for ``0 <= delta < 0x1000``. 

  :math:`x_\pi`        ``M(pi)``, ``pi`` an instance of class |AutPL|;

                       ``M(('d', c), ('p', n))`` returns 
                       ``M(AutPL(('d', c), ('p', n)))``.

  :math:`x_e`          ``M(('x', e))``, ``x`` an  instance of class |PLoop|;

                       ``M(('x', e))`` returns ``M(('x', PLoop(e)))`` for
                       ``0 <= e < 0x2000``.

  :math:`y_e`          ``M(('y', e))``,  ``e`` as in case :math:`x_e`. 

  :math:`z_e`          ``M(('z', e))``,  ``e`` as in case :math:`x_e`. 

  :math:`\tau^e`       ``M(('t', e))``, exponent  ``e`` is an integer 
                       which is taken modulo ``3``.

  :math:`\xi^e`        ``M(('l', e))``,  exponent  ``e`` is an integer 
                       which is taken modulo ``3``.
  ===================  ==========================================================


More possibilities for constructing elements of an instance of class 
|MMGroup| are given in the description of that class. An element ``g``
of an instance of the monster group is modelled as in instance of class 
|MMGroupWord|. ``g.group`` is the group where ``g`` belongs to; that 
group is an instance of class |MMGroup|. Multiplication and 
exponentiation of group elements works a usual.  

Internally, an element of  :math:`\mathbb{M}` is represented as a word
in the generators given above. 
In such a word we always reduce substrings of generators of the 
subgroup :math:`N_0` of :math:`\mathbb{M}` to a standard form, 
which is easy. We apply no relations to the remaining generator
:math:`\xi`, except for :math:`\xi^3=1`.
Reducing an arbitrary word in :math:`\mathbb{M}` to a standard form
is beyond or current capabilities of computing in the monster group,
see  :cite:`Wilson13` for background.

Future versions of this package may implement the following reduction
strategies for words of generators of :math:`\mathbb{M}` :

 * Substrings of generators of the subgroup 
   :math:`G_{x0} = 2_+^{1+24}.\mbox{Co}_1` may be reduced to a
   standard form. Yet this
   is considerably more difficult than reducing elements of
   the subgroup :math:`N_0`. Here the geometric information 
   about the Leech lattice in :cite:`Iva99` will be helpful

   Here we will use a fast algorithm for computing in the real
   Clifford group :math:`\mathcal{C}_{12}`,
   see :cite:`NRS01`  and  :cite:`AG04`.


 * Sufficiently long words of generators of :math:`\mathbb{M}` may
   be shortened with high probability, see :cite:`Wilson13`.

"""
# References in the __docstr__ see file docs/source/references.bib


from __future__ import absolute_import, division, print_function
from __future__ import  unicode_literals



import sys
import os
import collections
import re
import warnings
from numbers import Integral
import numpy as np
from random import randint, sample


from mmgroup.structures.parse_atoms import ihex, TaggedAtom
from mmgroup.structures.abstract_group import AbstractGroupWord
from mmgroup.structures.abstract_group import AbstractGroup
from mmgroup.structures.parse_atoms import  AtomDict      

try:
    from mmgroup.mat24 import MAT24_ORDER, pow_ploop
except (ImportError, ModuleNotFoundError):
    from mmgroup.dev.mat24.mat24_ref import Mat24    
    MAT24_ORDER = Mat24.MAT24_ORDER
    pow_ploop = Mat24.pow_ploop
    del Mat24


from mmgroup.structures.ploop import Cocode, PLoop
from mmgroup.structures.autpl import StdAutPlGroup, autpl_from_obj

from mmgroup.generators import mm_group_mul_words

# Functions to be imported from module mmgroup.mm_order
check_mm_order = None
check_mm_equal = None


###########################################################################
# Importing functions check_mm_order and check_mm_equal 
###########################################################################

def import_mm_order_functions():
    """Import functions ``check_mm_order, check_mm_equal``.

    We import these functions from module ``mmgroup.mm_order``
    on demand. This avoids an infinite recursion of imports.
    """
    global check_mm_order, check_mm_equal
    from mmgroup.mm_order import check_mm_order as f
    check_mm_order = f
    from mmgroup.mm_order import check_mm_equal as f
    check_mm_equal = f

###########################################################################
# Word class for the group MM
###########################################################################





class MMGroupWord(AbstractGroupWord):
    """Models an element of the monster group :math:`\mathbb{M}`

    Let ``M`` be an instance of class ``MMGroup``, and let ``g1``, 
    ``g2`` be elements of ``M``.  Then
    ``g1 * g2``  means group multiplication, and ``g1 ** n`` means
    exponentiation of ``g1`` with the integer ``n``. ``g1 ** (-1)`` 
    is the inverse of ``g``. ``g1 / g2`` means ``g1 * g2 ** (-1)``.
    We have ``1 * g1 == g1 * 1 == g1`` and ``1 / g1 == g1 ** (-1)``.

    ``g1 ** g2`` means ``g2**(-1) * g1 * g2``.   

    Let ``V`` be a vector space that is a representation of ``M``,
    see class |MMSpace| for details. An element ``g1`` of ``M`` 
    operates on the vector space  ``V`` by right multiplication.  

    :var group:
        This attribute contains the group to which the element belongs.
        That group is an instance of class |MMGroup|.

    .. warning::
       The constructor of this class is not for public use! You
       may call an instance ``M`` of class  |MMGroup| for
       constructing elements of the instance ``M`` of the monster 
       group.
  
    """
    MIN_LEN = 16
    __slots__ = "_group", "length", "_data", "reduced"
    def __init__(self, data, **kwds):
        self.group = kwds['group']
        self.length = len(data)
        self._data = np.array(data, dtype = np.uint32) 
        self.reduced = 0 
        self._extend(self.MIN_LEN)
                  
    def _extend(self, length):
        len_ = len(self._data)
        if length > len_:
            ap = np.zeros(max(length - len_, len_), dtype = np.uint32)
            self._data = np.append(self._data, ap)
             
    @property
    def data(self):
        return self._data[:self.length]
        
    def __len__(self):
        return self.length
        
    def __getitem__(self,i):
        if 0 <= i < self.length:
            return self._data[i] 
        if -self.length <= i < 0:
            return self._data[i + self.length]
        raise IndexError
        
    def is_reduced(self):
        """Return ``True`` if the element of the monster group is reduced

        An element ``g`` of the monster group represented by an instance
        of this class may be reduced by calling
        ``g.reduce()``.
        """
        return self.length == self.reduced

    def order(self, max_order = 119):
        """Return the order of the element of the monster group

        We use the method in :cite:`LPWW98`, section 7, for computing
        the order of an element of the monster.

        If the argument ``max_order`` is present then the order of the 
        element is checked up to (and including) ``max_order`` only.  
        Then the function returns ``0`` if the order is greater than 
        ``max_order``. By default, the function returns the exact 
        order of the element.
        """
        if check_mm_order is None:
            import_mm_order_functions()
        return check_mm_order(self, max_order)

###########################################################################
# Atoms for the group M
###########################################################################


tag_dict = {
        "d": 0x10000000, 
        "p": 0x20000000, 
        "x": 0x30000000, 
        "y": 0x40000000, 
        "t": 0x50000000, 
        "l": 0x60000000, 
}




tags = " dpxytl"

def gen_d(tag, d = "r"):
    if isinstance(d, Integral ):
        return [0x10000000 + (d & 0xfff)]
    elif isinstance(d, str):
        cocode = randint(int('n' in d), 0xfff) 
        if "o" in d and not "e" in d:
            cocode |= 1 
        if "e" in d and not "o" in d:
            ccocode &= ~1
        return [0x10000000 + (cocode & 0xfff)]
    else:
        cocode = Cocode(d).cocode
        return [0x10000000 + (cocode & 0xfff)]

def gen_p(tag, perm = "r"):
    if isinstance(perm, Integral):
        if not 0 <= perm < MAT24_ORDER:
            raise ValueError("Bad permutation number for Mathieu group")
        return [0x20000000 + perm]
    elif isinstance(perm, str):
        perm = randint(0, MAT24_ORDER-1)
        return [0x20000000 + perm]
    else:
        cocode, perm_num = autpl_from_obj(perm)
        return  [0x10000000 + (cocode & 0xfff), 0x20000000 + perm_num]


def gen_ploop_element(r):
    if isinstance(r, Integral):
        return  r & 0x1fff
    elif isinstance(r, str):
        return randint(0, 0x1fff) 
    else:
        return PLoop(r).ord

def gen_xy(tag, r = "r"):
    return [ tag_dict[tag] + gen_ploop_element(r)]

def gen_z(tag, r = "r"):
    pl = pow_ploop(gen_ploop_element(r), 3)
    return [tag_dict['x'] + pl, tag_dict['y'] + pl]

def gen_tl(tag, r = "r"):
    e = r
    if isinstance(r, str):
        e = randint(int('n' in r), 2) 
    return  [ tag_dict[tag] + e % 3] 


gen_tag_dict = {
        "d": gen_d, 
        "p": gen_p, 
        "x": gen_xy, 
        "y" :gen_xy, 
        "z" :gen_z, 
        "t": gen_tl, 
        "l": gen_tl, 
}


def gen_atom(tag = None, number = "r"):
    """Return list of integers representing element of monster group

    This is the workhorse form method MMGroup.atom().
    See that method for documentation.
    """
    if not tag:
         return []
    try: 
        gen_function = gen_tag_dict[tag]
    except KeyError:
        err = "Illegal tag %s for MM group atom"
        raise ValueError(err % tag)
    return gen_function(tag, number)


###########################################################################
# The class representing the group MM
###########################################################################


def cocode_to_mmgroup(g, c):
    return g.word_type([0x10000000 + c.cocode], group = g)

def autpl_to_mmgroup(g, aut):
    return g.word_type([0x10000000 + (aut.cocode & 0xfff), 
                  0x20000000 + aut.perm_num], group = g)


class MMGroup(AbstractGroup):
    r"""An instance ``M`` of this class models an instance of the monster

    :param: None

    :return: An instance of the monster group 
    :rtype:  an instance of class |MMGroup|

    This means that ``M = MMGroup()`` creates an instance ``M`` of the 
    monster group  :math:`\mathbb{M}`. For generating an element ``g`` 
    of ``M`` one must call ``M`` as a function with a variable number 
    of arguments. Depending on its type, each argument is evaluated to
    an element of ``M`` as indicated in the table below, and the
    product of these elements is returned. 

    Elements of the monster group are implemented as instances of class
    ``MMGroupWord``. The preferred way to construct an element of the 
    monster group is to call an instance of class |MMGroup|.  

    .. table:: Legal types for constructing an element of the monster
      :widths: 25 75

      +---------------------+-------------------------------------------+
      | type                | Evaluates to                              |
      +=====================+===========================================+
      | tuple (``tag, i``)  | ``M((tag, i))`` is equivalent to          |
      |                     | ``M.atom(tag, i)``                        |
      +---------------------+-------------------------------------------+
      | class |AutPL|       | The automorphism :math:`\pi` of the       | 
      |                     | Parker loop represented as an instance    |
      |                     | of class |AutPL| is mapped to             |
      |                     | :math:`x_\pi \in \mathbb{M}`              |
      +---------------------+-------------------------------------------+
      | class |MMGroupWord| | A deep copy of the given element of       | 
      |                     | :math:`\mathbb{M}` is returned.           |
      +---------------------+-------------------------------------------+
      | ``str``             | For an element ``g`` of ``M`` we have     |
      |                     | ``M(str(g)) == g``. This is helpful for   |
      |                     | rereading printed elements of ``M``.      |
      +---------------------+-------------------------------------------+

    See class |MMGroupWord| for the group operation on an instance
    ``M`` of  class |MMGroup|.

    Two elements ``g1, g2`` of the monster group can be tested for 
    equality with the ``==`` operator as usual. Here we use the 
    method given in :cite:`Wil03` for checking ``g1 * g2**(-1) == 1``.

    Elements ``g1``, ``g2`` that belong to different instances of
    class |MMGroup| are considered unequal.
    """
    word_type = MMGroupWord
    tags, formats = " dpxytl", [None, ihex, str, ihex, ihex, str, str]
    atom_parser = {}               # see method parse()
    conversions = {
        Cocode: cocode_to_mmgroup,
        #AutPlElement: autpl_to_mmgroup,
    }
    FRAME = re.compile(r"^M?\<(.+)\>$") # see method parse()
    STR_FORMAT = r"M<%s>"

    def __init__(self):
        """ TODO: Yet to be documented     


        """
        super(MMGroup, self).__init__()
        self.atom_parser = AtomDict(self.atom)
        self.set_preimage(StdAutPlGroup,  tuple)

    def atom(self, tag = None, i = "r"):
        r"""Return an atomic element of this group
        
        Here ``tag`` determines the type of the atomic group element,
        and the ``i`` is number of the atomic element of that type.
        Depending on the tag, ``i`` is the number of an element of one of 
        the structures |PLoop|, |Cocode|, or the number of an element of 
        the Mathieu  group ``M_24``, as explained in class |AutPL|.
        An element :math:`\pi` of the group |AutPL| is mapped to the
        element :math:`x_\pi` of the Monster group.
        
        The number ``i`` may also be an instance of the appropriate class
        |PLoop|, |Cocode|, or |AutPL|, as indicated in the table below.

        .. table:: Atomic elements of the Monster group
          :widths: 8 20 72


          +-------+-----------------+----------------------------------------+
          | Tag   | Number  ``i``   | Type of element                        |
          +=======+=================+========================================+
          |``'p'``| ``0-244823039`` | The standard representative            |
          |       |                 | ``AutPL(('p',i))`` of the  ``i``-th    |
          |       |                 | element of the Mathieu group           |
          |       |                 | ``M_24`` in |AutPL|. ``i`` may also    |
          |       |                 | be an instance of class |AutPL|.       |
          +-------+-----------------+----------------------------------------+
          |``'d'``| ``0-0xfff``     | The diagonal automorphism ``Cocode(i)``| 
          |       |                 | in |AutPL|. ``i`` may also             |
          |       |                 | be an instance of class |Cocode|.      |
          +-------+-----------------+----------------------------------------+
          |``'x'``| ``0-0x1fff``    | The element :math:`x_e`,  with         |
          |       |                 | ``e = PLoop(i)``.  ``i`` may also      |
          |       |                 | be an instance of class |PLoop|.       |
          +-------+-----------------+----------------------------------------+
          |``'y'``| ``0-0x1fff``    | The element :math:`y_e`,               |
          |       |                 | ``e = PLoop(i)``;                      |
          |       |                 | similar to tag ``'x'``.                |
          +-------+-----------------+----------------------------------------+
          |``'z'``| ``0-0x1fff``    | The element :math:`z_e`,               |
          |       |                 | ``e = PLoop(i)``;                      |
          |       |                 | similar to tag ``'x'``.                |
          +-------+-----------------+----------------------------------------+
          |``'t'``| ``0-2``         | The element :math:`\tau^i`,            |
          +-------+-----------------+----------------------------------------+
          |``'l'``| ``0-2``         | The element :math:`\xi^i`,             |
          +-------+-----------------+----------------------------------------+
        
        Remarks
        
        In ``i`` is the string ``'r'`` then a random element with the   
        given tag is generated.  If ``i`` is the string ``'n'`` then
        a random element with the given tag is generated, which is 
        different from  ``1`` with a very high probability.

        If ``tag == 'd'`` then  ``i = 'o'`` generates a random odd 
        and ``i = 'e'`` generates a  random even diagonal automorphism.  
        
        If the ``tag`` is ``'p'`` and ``i`` is an instance of class 
        |AutPL| then the returned atom is determined by the instance of 
        class |AutPL|; so it is not necessarily the standard 
        representative of an element of the Mathieu group ``M_24``. 

        The exponent ``i`` for a tag ``'t'`` or ``'l'`` is reduced
        modulo ``3``. 
        """
        return self.word_type(gen_atom(tag, i), group = self)


    def as_tuples(self, g):
        assert g.group == self
        # g = g.reduce(copy = True)
        data = g.data
        if len(data) and max(data) >= 0x70000000:
            raise ValueError("Illegal group element")
        return [(tags[a >> 28], a & 0xfffffff)  
                   for a in data if (a >> 28)]

    @classmethod
    def str_atom(cls, a):
        itag = (a >> 28) & 0xF
        if itag in [0, 8]: 
            return "1"
        if itag >= 8:
            return "(1/%s)" % cls.str_atom(a ^ 0x80000000)
        try:
            tag = cls.tags[itag]  
        except:
            return "(unknown)"
        fmt = cls.formats[itag]
        return tag + "_" + fmt(a & 0xfffffff)
        
   
    def str_word(self, g, fmt = None):
        s = "*".join(map(self.str_atom, g.data)) if len(g) else "1"
        return (fmt if fmt else self.STR_FORMAT) % s

    def reduce(self, g1, copy = False):
        l1 = g1.length
        if g1.reduced < l1:
            if copy:
                g1 = self.copy_word(g1)
            l_tail = l1 - g1.reduced
            g1._extend(l1 + l_tail + 1)
            g1._data[l1 : l1 + l_tail] = g1._data[g1.reduced : l1]
            tail =  g1._data[l1:]
            l1 = mm_group_mul_words(g1._data, g1.reduced, tail, l_tail, 1)
            g1.reduced = g1.length = l1
        return g1

    def _imul_nonreduced(self, g1, g2):
        l1, l2 = g1.length, g2.length
        g1._extend(l1 + l2 + 1)
        g1._data[l1 : l1 + l2] = g2._data[:l2]
        g1.length = l1 + l2
        return g1
        
    def _imul(self, g1, g2):
        l1, l2 = g1.length, g2.length
        g1._extend(2*(l1 + l2) + 1)
        g1._data[l1 : l1 + l2] = g2._data[:l2]
        l1 += l2
        l_tail = l1 - g1.reduced
        g1._data[l1 : l1 + l_tail] = g1._data[g1.reduced : l1]
        tail = g1._data[l1:]
        l1 = mm_group_mul_words(g1._data, g1.reduced, tail, l_tail, 1)
        g1.reduced = g1.length = l1
        return g1

    def _invert(self, g1):
        w = self.word_type(np.flip(g1.data) ^ 0x80000000, group=self)
        return self.reduce(w)

    def copy_word(self, g1):
        result = self.word_type(g1.data, group = self)
        result.reduced = g1.reduced
        return result

    def _equal_words(self, g1, g2):
        if check_mm_equal is None:
            import_mm_order_functions()
        return g1.group == g2.group and check_mm_equal(g1, g2)



