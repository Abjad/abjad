from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.containertools.Container import Container
from abjad.tools.tuplettools.Tuplet._TupletFormatter import _TupletFormatter
import fractions


class Tuplet(Container):
    r'''Abjad model of a tuplet:

    ::

        abjad> tuplet = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
        abjad> f(tuplet)
        \times 2/3 {
            c'8
            d'8
            e'8
        }

    Return tuplet object.
    '''

    __slots__ = ('_force_fraction', '_is_invisible', '_multiplier', '_preferred_denominator',
        '_signifier', )

    def __init__(self, multiplier, music = None, **kwargs):
        Container.__init__(self, music)
        self.multiplier = multiplier
        self._force_fraction = None
        self._formatter = _TupletFormatter(self)
        self._is_invisible = None
        self._preferred_denominator = None
        self._signifier = '*'
        self._initialize_keyword_values(**kwargs)

    ### OVERLOADS ###

    def __add__(self, arg):
        '''Add two tuplets of same type and with same multiplier.
        '''
        from abjad.tools import tuplettools
        assert isinstance(arg, type(self))
        new = tuplettools.fuse_tuplets([self, arg])
        return new

    def __getnewargs__(self):
        return (self.multiplier, )

    def __repr__(self):
        return '%s(%s, [%s])' % (type(self).__name__, self.multiplier, self._summary)

    def __str__(self):
        if 0 < len(self):
            return '{%s %s %s %s}' % (self._signifier, self.ratio_string, self._summary, self._signifier)
        else:
            return '{%s %s %s}' % (self._signifier, self.multiplier, self._signifier)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _is_visible(self):
        return not self.is_invisible

    @property
    def _multiplier_fraction_string(self):
        if self.preferred_denominator is not None:
            inverse_multiplier = fractions.Fraction(
                self.multiplier.denominator, self.multiplier.numerator)
            d, n = durationtools.rational_to_duration_pair_with_specified_integer_denominator(
                inverse_multiplier, self.preferred_denominator)
        else:
            n, d = self.multiplier.numerator, self.multiplier.denominator
        return '%s/%s' % (n, d)

    @property
    def _summary(self):
        if 0 < len(self):
            return ', '.join([str(x) for x in self._music])
        else:
            #return ' '
            return ''

    ### PUBLIC ATTRIBUTES ###

    @apply
    def force_fraction():
        def fget(self):
            r'''Read / write boolean to force ``n:m`` fraction in LilyPond format::

                abjad> tuplet = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")

            ::

                abjad> tuplet.force_fraction is None
                True

            ::

                abjad> f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }


            ::

                abjad> tuplet.force_fraction = True

            ::

                abjad> f(tuplet)
                \fraction \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

            Return boolean or none.
            '''
            return self._force_fraction
        def fset(self, arg):
            if isinstance(arg, (bool, type(None))):
                self._force_fraction = arg
            else:
                raise TypeError('bad type for tuplet force fraction: "%s".' % arg)
        return property(**locals())

    @property
    def is_augmentation(self):
        '''True when multiplier is greater than 1.
        Otherwise false::

            abjad> t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
            abjad> t.is_augmentation
            False

        Return boolean.
        '''
        if self.multiplier:
            return 1 < self.multiplier
        else:
            return False

    @property
    def is_binary(self):
        '''Read-only boolean true when multiplier numerator is power of two. Otherwise false::

            abjad> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
            abjad> tuplet.is_binary
            True

        Return boolean.
        '''
        if self.multiplier:
            return mathtools.is_nonnegative_integer_power_of_two(self.multiplier.numerator)
        else:
            return True

    @property
    def is_diminution(self):
        '''True when multiplier is less than 1.  Otherwise false::

            abjad> t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
            abjad> t.is_diminution
            True

        Return boolean.
        '''
        if self.multiplier:
            return self.multiplier < 1
        else:
            return False

    @apply
    def is_invisible():
        def fget(self):
            r'''Read / write boolean to render as LilyPond ``\scaledDurations``
            construct instead of tuplet::

                abjad> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")

            ::

                abjad> f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

            ::

                abjad> tuplet.is_invisible = True

            ::

            
                \scaleDurations #'(2 . 3) {
                    c'8
                    d'8
                    e'8
                }

            This has the effect of rendering no
            no tuplet bracket and no tuplet number while preserving the rhythmic
            value of the tuplet and the contents of the tuplet.

            Return boolean or none.
            '''
            return self._is_invisible
        def fset(self, arg):
            assert isinstance(arg, (bool, type(None)))
            self._is_invisible = arg
        return property(**locals())

    @property
    def is_nonbinary(self):
        '''Read-only boolean true when multiplier numerator is not power of two. Otherwise false::

            abjad> tuplet = Tuplet((3, 5), "c'8 d'8 e'8 f'8 g'8")
            abjad> tuplet.is_nonbinary
            True

        Return boolean.
        '''
        return not self.is_binary

    @property
    def is_trivial(self):
        '''True when tuplet multiplier is one. Otherwise false::

            abjad> tuplet = Tuplet((1, 1), "c'8 d'8 e'8")
            abjad> tuplet.is_trivial
            True
        
        Return boolean.
        '''
        return self.multiplier == 1

    @property
    def multiplied_duration(self):
        '''Read-only multiplied duration of tuplet::

            abjad> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
            abjad> tuplet.multiplied_duration
            Duration(1, 4)

        Return duration.
        '''
        return self.multiplier * self.contents_duration

    @apply
    def multiplier():
        def fget(self):
            r'''Read / write tuplet multiplier::

                abjad> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
                abjad> tuplet.multiplier
                Fraction(2, 3)

            Return fraction.
            ''' 
            return self._multiplier
        def fset(self, expr):
            if isinstance(expr, (int, long)):
                rational = fractions.Fraction(expr)
            elif isinstance(expr, tuple):
                rational = fractions.Fraction(*expr)
            elif isinstance(expr, fractions.Fraction):
                rational = fractions.Fraction(expr)
            else:
                raise ValueError('can not set tuplet multiplier: "%s".' % str(expr))
            if 0 < rational:
                self._multiplier = rational
            else:
                raise ValueError('tuplet multiplier must be positive: "%s".' % rational)
        return property(**locals())

    @apply
    def preferred_denominator():
        def fget(self):
            r'''.. versionadded:: 2.0

            Integer denominator in terms of which tuplet fraction should format::

                abjad> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
                abjad> tuplet.preferred_denominator = 4

            ::

                abjad> f(tuplet)
                \times 4/6 {
                    c'8
                    d'8
                    e'8
                }

            Return positive integer or none.
            '''
            return self._preferred_denominator
        def fset(self, arg):
            if isinstance(arg, (int, long)):
                if not 0 < arg:
                    raise ValueError('tuplet preferred denominator must be positive: "%s".' % arg)
            elif not isinstance(arg, type(None)):
                raise TypeError('bad tuplet preferred denominator type: "%s".' % arg)
            self._preferred_denominator = arg
        return property(**locals())

    @property
    def preprolated_duration(self):
        '''Duration prior to prolation:

        ::

            abjad> t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
            abjad> t.preprolated_duration
            Duration(1, 4)

        Return duration.
        '''
        return self.multiplied_duration

    @property
    def ratio_string(self):
        '''Read-only tuplet multiplier formatted with colon as ratio::

            abjad> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
            abjad> tuplet.ratio_string
            '3:2'

        Return string.
        '''
        multiplier = self.multiplier
        if multiplier is not None:
            return '%s:%s' % (multiplier.denominator, multiplier.numerator)
        else:
            return None
