from __future__ import absolute_import, division, print_function
from __future__ import  unicode_literals


"""Modelling an abstract group

Yet to be documented

"""
import sys
import re
import warnings
from copy import deepcopy
from random import sample, randint
from numbers import Integral, Number

from mmgroup.structures.parse_atoms import  eval_atom_expression        
from mmgroup.structures.parity import Parity



####################################################################
####################################################################
### Class AbstractGroup and helpers for that class
####################################################################
####################################################################

####################################################################
### Class AbstractGroupWord
####################################################################


class AbstractGroupWord(object):
    """Model an element of an abstract group.

    Users should not refer to this class directly. They should create 
    a group as an instance of subclass of class AbstractGroup and use 
    the methods of that group for creating elements.

    The standard group operations '*' '/' (=right multiplication with
    the inverse) and '**' are implemented here.

    g1 ** g2  means  g2**(-1) * g1 * g2  for group elements g1, g2.

    Here a group is an instance of (a subclass of) class AbstractGroup. 

    For each word a group 'g' should be passed as a keyword argument 
    'group = g'. If a class of type 'AbstractGroup' contains one 
    instance only, the corresponding subclass of this class may 
    contain a class attribute 'group' referring to that group. Then 
    the user  may contruct elements of that group using the 
    constructor of that subclass of this class.
    """
    __slots__ = "group"
    def __init__(self, *args, **kwds):
        try:
            self.group = kwds['group']
        except:
            assert isinstance(self.group, AbstractGroup)

    # There is no need to modify an methods below this line.
    # You should overwrite the corresonding methods in the
    # subclasses of class AbstractGroup insead.
 
    def __eq__(self, other):    
        return( isinstance(other, AbstractGroupWord) 
            and  self.group == other.group
            and  self.group._equal_words(self, other)
        )

    def __ne__(self, other): 
        return not self.__eq__(other)

    def copy(self):
        """Return a deep copy of the group element"""
        return self.group.copy_word(self)

    def __imul__(self, other):
        """Implementation of the group multiplication"""
        g = self.group
        return g._imul(self, g._to_group(other))

    def __mul__(self, other):
        """Implementation of the group multiplication"""
        g = self.group
        try:
            return g._imul(g.copy_word(self), g._to_group(other))
        except (TypeError, NotImplementedError) as exc:
            try:
                myself = other.group._to_group(self)
                return myself.__imul__(other)
            except:
                raise exc
    def __rmul__(self, other):
        """Implementation of the reverse group multiplication"""
        g = self.group
        if isinstance(other, Parity):
            return other
        try:
            return g._imul(g._to_group(other), self)
        except (TypeError, NotImplementedError) as exc:
            try:
                myself = other.group._to_group(self)
                return other.__imul__(myself)
            except:
                raise exc

    def __itruediv__(self, other):
        """Implementation of the group division

        Here self / other    means    self * other**(-1) .
        """
        g = self.group
        return g._imul(self, g._invert(g._to_group(other)))

    def __truediv__(self, other):
        """Implementation of the group division

        Here self / other    means    self * other**(-1) .
        """
        g = self.group
        return g._imul(g.copy_word(self), g._invert(g._to_group(other)))

    def __rtruediv__(self, other):
        """Implementation of the reverse group division

        Here self / other    means    self * other**(-1) .
        """
        g = self.group
        return g._imul(g.copy_word(g._to_group(other)), g._invert(self))
      
    def __pow__(self, exp):
        """Implementation of the power operation

        This is exponentiation for integer eponents and conjugation
        if the exponent is a group element.
        """
        g = self.group
        if isinstance(exp, Integral):
            if exp > 0:
                res, start = g.copy_word(self), self
            elif exp == 0:
                return g.neutral()
            else:
                start, exp = g._invert(self), -exp
                res = g.copy_word(start) 
            for i in range(int(exp).bit_length() - 2, -1, -1):
                res = g._imul(res, res)
                if exp & (1 << i):
                    res = g._imul(res, start) 
            return res      
        elif isinstance(exp, AbstractGroupWord):
            e = self.group._to_group(exp) 
            return g._imul(g._imul(g._invert(e), self), e)
        elif isinstance(exp, Parity):
            one = self.group.neutral()
            if self * self == one:
                return self if other.value & 1 else one
            raise ValueError("Group element has not order 1 or 2")
        else:
            return NotImplemented


    def reduce(self, copy = False):
        """Reduce a group element

        If group elements are implemented as words, some functions
        may produce unreduced words. This function  reduces the
        group element in place.

        Note that all operators return reduced words. Functions return
        reduced words unless stated otherwise. However, reducing all
        words representing the same group element to the same word may 
        be beyond the capabilties of a program. 

        If ``copy`` is set then a reduced copy of the element is 
        returned, in case that the input element is not already 
        reduced.
        """
        return self.group.reduce(self, copy)

    def str(self):
        """Represent group element as a string"""
        try:
            return self.group.str_word(self)
        except NotImplementedError:
            return super(AbstractGroupWord, str)()
    __repr__ = str

    def as_tuples(self):
        """Convert group element to a list of tuples

        For a group element ``g`` the following should hold:

        ``g.group.word(*g.as_tuples()) == g`` .

        So passing the tuples in the list returned by this method
        as arguments to ``g.group`` or to ``g.group.word`` 
        reconstructs the element ``g``.

        This shows how to convert a group element to a list of tuples
        and vice versa.
        """
        return self.group.as_tuples(self)




####################################################################
### Class AbstractGroup
####################################################################


class AbstractGroup(object):
    """Model an abstract group"""
    word_type = AbstractGroupWord  # type of an element (=word) in the group

    def __init__(self, *data, **kwds):
        """Creating instances is only possible for concrete groups

         
        """
        pass

    ### The following methods must be overwritten ####################

    def __call__(self, *args):
        """Convert args to group elements and return their product
        """
        raise NotImplementedError




    def _imul(self, g1, g2):
        """Return product g1 * g2 of group elements g1 and g2.

        g1 may be destroyed but not g2.

        This method is called for elements g1 and g2 of the group
        'self' only. It should return the reduced product.
        """
        raise NotImplementedError("No multiplication in abstract group")


    def _invert(self, g1):
        """Return inverse g1**(-1) of group element g1.

        g1 must not be destroyed.

        This method is called for elements g1 of the group
        'self' only. It should return the reduced inverse.
        """
        raise NotImplementedError("No inversion in abstract group")
        
    ### The following methods should be overwritten ###################

    def copy_word(self, g1):
        """Return deep copy of group element ``g1``"""
        g_copy = deepcopy(g1)
        # Even a deep copy of an element is still in the same group
        g_copy.group = g1.group
        return g_copy

    def _equal_words(self, g1, g2):
        """Return True iff elements g1 and g2 are equal 

        This method is called for elements g1 and g2 of the group
        'self' only.
		
        In concrete group this method should be overwritten with
        a comparison of the relevant attributes of g1 and g2.

        Caution:
        Non-reduced words may be considered unequal even if they
        represent the same element. Use g1.reduce() or g1 * 1 to
        obtain the reduced form of g1. See method reduce() for
        details.
        """
        return g1 == g2


    def reduce(self, g, copy = False):
        """Reduce the word ``g`` which is an element of the group

        We assume that the representation of a group element
        is not always given in a unique form that we call
        the reduced form. 

        This method tries to achieve this goal. Group elements
        are reduced by any operator, except for the
        ``==`` and  ``!=`` operators. 

        For test purposes, is is useful to obtain a group 
        element in non-reduced form. Applications should
        create reduced group elements only.

        One way to obtain avoid reduction is to call method 
        ``word()`` of this class with elements separated by 
        commas. Then no reduction takes place across the factors
        separated by commas. 

        If argument ``copy`` is True, a reduced copy of ``g``
        should be returned if ``g`` is not reduced.
        """
        return g




    def as_tuples(self, g):
        """Convert group element ``g`` to a list of tuples.

        The returned tuple should represent a reduced word.

        The sequence:: 

            l = g.group.as_tuples(g) 
            g1 = g.group(*l)

        should compute a group element ``g1`` with ``g1 == g``.
        """
        raise NotImplementedError("Abstract method")


    def str_word(self, g):
        """Convert group atom ``g`` to a string

        For an element ``g`` of this group ``g.group.str_word(g)``
        should be equivalent   to ``g.str()``.
        """
        raise NotImplementedError

                 
    ### The following methods need not be overwritten #################

    def neutral(self):
        """Return neutral element of the group"""
        return self.__call__()


  
    def _to_group(self, g):
        """Convert the object ``g`` to an element of this group

        This function tries the conversions on ``g``. This function
        is applied in a group operation.
        """
        if isinstance(g, AbstractGroupWord) and g.group == self:
            return g
        if g == 1:
            return self.neutral()
        err = "Cannot convert type '%s' object to group element"
        raise TypeError(err % type(g))
           


    ### The following methods should not be overwritten ###############




    def __contains__(self, other):
        """Return True iff 'other' is an element of the group"""
        try:
            if not isinstance(other, self.word_type): 
                 return False
            if other.group != self: 
                 return False
            return True
        except:
            return False


