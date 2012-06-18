from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.mathtools.BoundedObject import BoundedObject
from abjad.tools.mathtools.NonreducedFraction import NonreducedFraction
import fractions


class Division(NonreducedFraction, BoundedObject):
    r'''.. versionadded:: 1.0

    Bounded nonreduced fraction.

    Initialize from string::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.Division('[5, 8)')
        Division('[5, 8)')

    Initialize from pair and optional open / closed keywords::

        >>> specificationtools.Division((5, 8), is_right_open=True)
        Division('[5, 8)')

    Initialize from other division:

        >>> specificationtools.Division(_)
        Division('[5, 8)')

    Examples follow.
    '''

    ### CLASS ATTRIBUTES ###

    # slots definition does nothing here because multiple inheritance 
    # breaks with multiple slots base classes
    __slots__ = ()

    ### INITIALIZER ###

    def __new__(klass, arg, is_left_open=None, is_right_open=None):
        from experimental import specificationtools
        if isinstance(arg, str):
            triple = specificationtools.interval_string_to_pair_and_indicators(arg)
            pair, is_left_open, is_right_open = triple
        else:
            pair = arg
        self = NonreducedFraction.__new__(klass, pair)
        if is_left_open is None:
            is_left_open = getattr(pair, 'is_left_open', False)
        if is_right_open is None:
            is_right_open = getattr(pair, 'is_right_open', False)
        self.is_left_open = is_left_open
        self.is_right_open = is_right_open
        return self

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if not self.pair == expr.pair:
            return False
        if not self.is_left_closed == expr.is_left_closed:
            return False
        if not self.is_right_closed == expr.is_right_closed:
            return False
        return True

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, str(self))

    def __str__(self):
        if self.is_left_open:
            left_symbol = '('
        else:
            left_symbol = '['
        if self.is_right_open:
            right_symbol = ')'
        else:
            right_symbol = ']'
        return '{}{}, {}{}'.format(left_symbol, self.numerator, self.denominator, right_symbol)

    ### PRIVATE METHODS ###

    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        string = '{}({!r})'.format(self._tools_package_qualified_class_name, str(self))
        return [string]

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        return fractions.Fraction(self.numerator, self.denominator)
