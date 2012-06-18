from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.mathtools.NonreducedFraction import NonreducedFraction
import fractions


# TODO: refactor to inherit from mathtools.BoundedObject, too
class Division(NonreducedFraction):
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

    .. todo:: initialize divisions from other divisions.

    Divisions are immutable.
    '''

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

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        return fractions.Fraction(self.numerator, self.denominator)

    @property
    def is_closed(self):
        return self.is_left_closed and self.is_right_closed

    @property
    def is_half_closed(self):
        return not self.is_left_closed == self.is_right_closed

    @property
    def is_half_open(self):
        return not self.is_left_open == self.is_right_open

    @property
    def is_open(self):
        return not self.is_left_closed and not self.is_right_closed

    ### READ / WRITE PUBLIC PROPERTIES ### 

    @apply
    def is_left_closed():
        def fget(self):
            return self._is_left_closed
        def fset(self, is_left_closed):
            assert isinstance(is_left_closed, bool), is_left_closed
            self._is_left_closed = is_left_closed
        return property(**locals())

    @apply
    def is_left_open():
        def fget(self):
            return not self.is_left_closed
        def fset(self, is_left_open):
            assert isinstance(is_left_open, bool), is_left_open
            self._is_left_closed = not is_left_open
        return property(**locals())

    @apply
    def is_right_closed():
        def fget(self):
            return self._is_right_closed
        def fset(self, is_right_closed):
            assert isinstance(is_right_closed, bool), is_right_closed
            self._is_right_closed = is_right_closed
        return property(**locals())

    @apply
    def is_right_open():
        def fget(self):
            return not self.is_right_closed
        def fset(self, is_right_open):
            assert isinstance(is_right_open, bool), is_right_open
            self._is_right_closed = not is_right_open
        return property(**locals())
