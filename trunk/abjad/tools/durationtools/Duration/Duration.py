from fractions import Fraction


# TODO: allow Duration('8..') initialization
class Duration(Fraction):
    '''.. versionadded:: 2.0

    Abjad model of musical duration::

        abjad> Duration(15, 16)
        Duration(15, 16)

    Durations inherit from built-in ``Fraction``.
    '''

    def __new__(klass, *args):
        from abjad.tools import mathtools
        if isinstance(args[0], tuple):
            n, d = args[0]
            try:
                self = Fraction.__new__(klass, n, d)
            except TypeError:
                if mathtools.is_integer_equivalent_number(n) and \
                    mathtools.is_integer_equivalent_number(d):
                    self = Fraction.__new__(klass, int(n), int(d))
                else:
                    raise TypeError
        else:
            try:
                self = Fraction.__new__(klass, *args)
            except TypeError:
                if all([mathtools.is_integer_equivalent_number(x) for x in args]):
                    args = [int(x) for x in args]
                    self = Fraction.__new__(klass, *args)
                else:
                    raise TypeError
        return self

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s, %s)' % (type(self).__name__, self.numerator, self.denominator)

    def __abs__(self, *args):
        return type(self)(Fraction.__abs__(self, *args))

    def __add__(self, *args):
        return type(self)(Fraction.__add__(self, *args))

    def __div__(self, *args):
        return type(self)(Fraction.__div__(self, *args))

    def __divmod__(self, *args):
        return type(self)(Fraction.__divmod__(self, *args))

    def __mod__(self, *args):
        return type(self)(Fraction.__mod__(self, *args))

    def __mul__(self, *args):
        return type(self)(Fraction.__mul__(self, *args))

    def __neg__(self, *args):
        return type(self)(Fraction.__neg__(self, *args))

    def __pos__(self, *args):
        return type(self)(Fraction.__pos__(self, *args))

    def __pow__(self, *args):
        return type(self)(Fraction.__pow__(self, *args))

    def __radd__(self, *args):
        return type(self)(Fraction.__radd__(self, *args))

    def __rdiv__(self, *args):
        return type(self)(Fraction.__rdiv__(self, *args))

    def __rdivmod__(self, *args):
        return type(self)(Fraction.__rdivmod__(self, *args))

    def __rmod__(self, *args):
        return type(self)(Fraction.__rmod__(self, *args))

    def __rmul__(self, *args):
        return type(self)(Fraction.__rmul__(self, *args))

    def __rpow__(self, *args):
        return type(self)(Fraction.__rpow__(self, *args))

    def __rsub__(self, *args):
        return type(self)(Fraction.__rsub__(self, *args))

    def __rtruediv__(self, *args):
        return type(self)(Fraction.__rtruediv__(self, *args))

    def __sub__(self, *args):
        return type(self)(Fraction.__sub__(self, *args))

    def __truediv__(self, *args):
        return type(self)(Fraction.__truediv__(self, *args))
