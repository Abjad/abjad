import fractions
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools import mathtools
from abjad.tools.containertools.Container import Container


class Tuplet(Container):
    r'''Abjad model of a tuplet:

    ::

        >>> tuplet = Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")

    ::

        >>> tuplet
        Tuplet(2/3, [c'8, d'8, e'8])

    ::

        >>> f(tuplet)
        \times 2/3 {
            c'8
            d'8
            e'8
        }

    ::

        >>> show(tuplet) # doctest: +SKIP

    Tuplets, like any counttime container, may nest arbitrarily:

    ::

        >>> second_tuplet = Tuplet((4, 7), "g'4. ( a'16 )")
        >>> tuplet.insert(1, second_tuplet)

    ::

        >>> f(tuplet)
        \times 2/3 {
            c'8
            \times 4/7 {
                g'4. (
                a'16 )
            }
            d'8
            e'8
        }


    ::

        >>> show(tuplet) # doctest: +SKIP

    ::

        >>> third_tuplet = Tuplet((4, 5), "e''32 [ ef''32 d''32 cs''32 cqs''32 ]")
        >>> second_tuplet.insert(1, third_tuplet)

    ::

        >>> f(tuplet)
        \times 2/3 {
            c'8
            \times 4/7 {
                g'4. (
                \times 4/5 {
                    e''32 [
                    ef''32
                    d''32
                    cs''32
                    cqs''32 ]
                }
                a'16 )
            }
            d'8
            e'8
        }

    ::

        >>> show(tuplet) # doctest: +SKIP

    Return tuplet object.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_force_fraction', '_is_invisible', '_multiplier', '_preferred_denominator',
        '_signifier', )

    ### INITIALIZER ###

    def __init__(self, multiplier, music=None, **kwargs):
        Container.__init__(self, music)
        self.multiplier = multiplier
        self._force_fraction = None
        self._is_invisible = None
        self._preferred_denominator = None
        self._signifier = '*'
        self._initialize_keyword_values(**kwargs)

    ### SPECIAL METHODS ###

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

    ### READ-ONLY PRIVATE PROPERTIES ###

    # TODO: make public
    @property
    def _is_visible(self):
        return not self.is_invisible

    @property
    def _multiplier_fraction_string(self):
        if self.preferred_denominator is not None:
            inverse_multiplier = durationtools.Multiplier(
                self.multiplier.denominator, self.multiplier.numerator)
            nonreduced_fraction = mathtools.NonreducedFraction(inverse_multiplier)
            nonreduced_fraction = nonreduced_fraction.with_denominator(self.preferred_denominator)
            d, n = nonreduced_fraction.pair
        else:
            n, d = self.multiplier.numerator, self.multiplier.denominator
        return '%s/%s' % (n, d)

    @property
    def _summary(self):
        if 0 < len(self):
            return ', '.join([str(x) for x in self._music])
        else:
            return ''

    ### PRIVATE METHODS ###

    def _format_after_slot(self, format_contributions):
        '''Read-only tuple of format contributions to appear immediately after self closing.
        '''
        result = []
        result.append(('grob reverts', format_contributions.get('grob reverts', [])))
        result.append(('lilypond command marks',
            format_contributions.get('after', {}).get('lilypond command marks', [])))
        result.append(('comments', format_contributions.get('after', {}).get('comments', [])))
        return tuple(result)

    def _format_before_slot(self, format_contributions):
        result = []
        result.append(('comments', format_contributions.get('before', {}).get('comments', [])))
        result.append(('lilypond command marks',
            format_contributions.get('before', {}).get('lilypond command marks', [])))
        result.append(('grob overrides', format_contributions.get('grob overrides', [])))
        return tuple(result)

    def _format_close_brackets_slot(self, format_contributions):
        '''Read-only tuple of format contributions used to generate self closing.
        '''
        result = []
        if self.multiplier:
            result.append([('self_brackets', 'close'), '}'])
        return tuple(result)

    def _format_closing_slot(self, format_contributions):
        '''Read-only tuple of format contributions to appear immediately before self closing.
        '''
        result = []
        result.append(('lilypond command marks',
            format_contributions.get('closing', {}).get('lilypond command marks', [])))
        result.append(('comments', format_contributions.get('closing', {}).get('comments', [])))
        return self._format_slot_contributions_with_indent(result)

    def _format_lilypond_fraction_command_string(self):
        if self._is_visible:
            if self.is_augmentation or self.has_non_power_of_two_denominator or self.force_fraction:
                return r'\fraction '
        return ''

    def _format_open_brackets_slot(self, format_contributions):
        result = []
        if self.multiplier:
            if self.is_invisible:
                multiplier = self.multiplier
                n, d = multiplier.numerator, multiplier.denominator
                contributor = (self, 'is_invisible')
                contributions = [r"\scaleDurations #'(%s . %s) {" % (n, d)]
                result.append([contributor, contributions])
            else:
                contributor = ('self_brackets', 'open')
                if self.multiplier != 1:
                    contributions = [r'%s\times %s %s' % (
                        self._format_lilypond_fraction_command_string(),
                        self._multiplier_fraction_string,
                        '{'
                        )]
                else:
                    contributions = ['{']
                result.append([contributor, contributions])
        return tuple(result)

    def _format_opening_slot(self, format_contributions):
        '''Read-only tuple of format contributions to appear immediately after self opening.
        '''
        result = []
        result.append(('comments', format_contributions.get('opening', {}).get('comments', [])))
        result.append(('lilypond command marks',
            format_contributions.get('opening', {}).get('lilypond command marks', [])))
        return self._format_slot_contributions_with_indent(result)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def has_non_power_of_two_denominator(self):
        '''Read-only boolean true when multiplier numerator is not power of two. Otherwise false::

            >>> tuplet = Tuplet((3, 5), "c'8 d'8 e'8 f'8 g'8")
            >>> tuplet.has_non_power_of_two_denominator
            True

        Return boolean.
        '''
        return not self.has_power_of_two_denominator

    @property
    def has_power_of_two_denominator(self):
        '''Read-only boolean true when multiplier numerator is power of two. Otherwise false::

            >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
            >>> tuplet.has_power_of_two_denominator
            True

        Return boolean.
        '''
        if self.multiplier:
            return mathtools.is_nonnegative_integer_power_of_two(self.multiplier.numerator)
        else:
            return True

    @property
    def implied_prolation(self):
        r'''Tuplet implied prolation.

        Defined equal to tuplet multiplier.

        Return multiplier.
        '''
        return self.multiplier

    @property
    def is_augmentation(self):
        '''True when multiplier is greater than 1.
        Otherwise false::

            >>> t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
            >>> t.is_augmentation
            False

        Return boolean.
        '''
        if self.multiplier:
            return 1 < self.multiplier
        else:
            return False

    @property
    def is_diminution(self):
        '''True when multiplier is less than 1.  Otherwise false::

            >>> t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
            >>> t.is_diminution
            True

        Return boolean.
        '''
        if self.multiplier:
            return self.multiplier < 1
        else:
            return False

    @property
    def is_trivial(self):
        '''True when tuplet multiplier is one. Otherwise false::

            >>> tuplet = Tuplet((1, 1), "c'8 d'8 e'8")
            >>> tuplet.is_trivial
            True

        Return boolean.
        '''
        return self.multiplier == 1

    @property
    def lilypond_format(self):
        self._update_marks_of_entire_score_tree_if_necessary()
        return self._format_component()

    @property
    def multiplied_duration(self):
        '''Read-only multiplied duration of tuplet::

            >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
            >>> tuplet.multiplied_duration
            Duration(1, 4)

        Return duration.
        '''
        return self.multiplier * self.contents_duration

    @property
    def preprolated_duration(self):
        '''Duration prior to prolation:

        ::

            >>> t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
            >>> t.preprolated_duration
            Duration(1, 4)

        Return duration.
        '''
        return self.multiplied_duration

    @property
    def ratio_string(self):
        '''Read-only tuplet multiplier formatted with colon as ratio::

            >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
            >>> tuplet.ratio_string
            '3:2'

        Return string.
        '''
        multiplier = self.multiplier
        if multiplier is not None:
            return '%s:%s' % (multiplier.denominator, multiplier.numerator)
        else:
            return None

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def force_fraction():
        def fget(self):
            r'''Read / write boolean to force ``n:m`` fraction in LilyPond format::

                >>> tuplet = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")

            ::

                >>> tuplet.force_fraction is None
                True

            ::

                >>> f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }


            ::

                >>> tuplet.force_fraction = True

            ::

                >>> f(tuplet)
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

    @apply
    def is_invisible():
        def fget(self):
            r'''Read / write boolean to output LilyPond ``\scaledDurations``
            instead of tuplet:

            ::

                >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")

            ::

                >>> f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

            ::

                >>> tuplet.is_invisible = True

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

    @apply
    def multiplier():
        def fget(self):
            r'''Read / write tuplet multiplier::

                >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
                >>> tuplet.multiplier
                Multiplier(2, 3)

            Return multiplier.
            '''
            return self._multiplier
        def fset(self, expr):
            if isinstance(expr, (int, long, fractions.Fraction)):
                rational = durationtools.Multiplier(expr)
            elif isinstance(expr, tuple):
                rational = durationtools.Multiplier(expr)
            else:
                raise ValueError('can not set tuplet multiplier: {!r}.'.format(expr))
            if 0 < rational:
                self._multiplier = rational
            else:
                raise ValueError('tuplet multiplier must be positive: {!r}.'.format(expr))
        return property(**locals())

    @apply
    def preferred_denominator():
        def fget(self):
            r'''.. versionadded:: 2.0

            Integer denominator in terms of which tuplet fraction should format::

                >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
                >>> tuplet.preferred_denominator = 4

            ::

                >>> f(tuplet)
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
