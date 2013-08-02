# -*- encoding: utf-8 -*-
import fractions
import math
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.containertools.Container import Container


class Tuplet(Container):
    r'''Abjad model of a tuplet:

    ::

        >>> tuplet = Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")

    ::

        >>> tuplet
        Tuplet(2/3, [c'8, d'8, e'8])

    ..  doctest::

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

    ..  doctest::

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

        >>> third_tuplet = Tuplet(
        ...     (4, 5), "e''32 [ ef''32 d''32 cs''32 cqs''32 ]")
        >>> second_tuplet.insert(1, third_tuplet)

    ..  doctest::

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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_force_fraction',
        '_is_invisible',
        '_multiplier',
        '_preferred_denominator',
        '_signifier',
        )

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

    def __getnewargs__(self):
        return (self.multiplier, )

    def __repr__(self):
        '''Interpreter representation of tuplet.

        Return string.
        '''
        return '%s(%s, [%s])' % (
            self._class_name,
            self.multiplier,
            self._summary,
            )

    def __str__(self):
        '''String representation of tuplet.

        Return string.
        '''
        if 0 < len(self):
            return '{%s %s %s %s}' % (
                self._signifier,
                self.ratio_string,
                self._summary,
                self._signifier,
                )
        else:
            return '{%s %s %s}' % (
                self._signifier,
                self.multiplier,
                self._signifier,
                )

    ### PRIVATE PROPERTIES ###

    @property
    def _has_power_of_two_denominator(self):
        if self.multiplier:
            return mathtools.is_nonnegative_integer_power_of_two(
                self.multiplier.numerator)
        else:
            return True

    # TODO: remove in favor of "not self.is_invisible"
    @property
    def _is_visible(self):
        return not self.is_invisible

    @property
    def _multiplier_fraction_string(self):
        if self.preferred_denominator is not None:
            inverse_multiplier = durationtools.Multiplier(
                self.multiplier.denominator, self.multiplier.numerator)
            nonreduced_fraction = \
                mathtools.NonreducedFraction(inverse_multiplier)
            nonreduced_fraction = nonreduced_fraction.with_denominator(
                self.preferred_denominator)
            d, n = nonreduced_fraction.pair
        else:
            n, d = self.multiplier.numerator, self.multiplier.denominator
        return '%s/%s' % (n, d)

    @property
    def _preprolated_duration(self):
        return self.multiplied_duration

    @property
    def _summary(self):
        if 0 < len(self):
            return ', '.join([str(x) for x in self._music])
        else:
            return ''

    ### PRIVATE METHODS ###

    def _format_after_slot(self, format_contributions):
        r'''Tuple of format contributions to appear 
        immediately after self closing.
        '''
        result = []
        result.append(('grob reverts', 
            format_contributions.get('grob reverts', [])))
        result.append(('lilypond command marks',
            format_contributions.get(
                'after', {}).get('lilypond command marks', [])))
        result.append(('comments', 
            format_contributions.get('after', {}).get('comments', [])))
        return tuple(result)

    def _format_before_slot(self, format_contributions):
        result = []
        result.append(('comments', 
            format_contributions.get('before', {}).get('comments', [])))
        result.append(('lilypond command marks',
            format_contributions.get(
                'before', {}).get('lilypond command marks', [])))
        result.append(('grob overrides', 
            format_contributions.get('grob overrides', [])))
        return tuple(result)

    def _format_close_brackets_slot(self, format_contributions):
        r'''Tuple of format contributions used to 
        generate self closing.
        '''
        result = []
        if self.multiplier:
            result.append([('self_brackets', 'close'), '}'])
        return tuple(result)

    def _format_closing_slot(self, format_contributions):
        r'''Tuple of format contributions to appear 
        immediately before self closing.
        '''
        result = []
        result.append(('lilypond command marks',
            format_contributions.get(
                'closing', {}).get('lilypond command marks', [])))
        result.append(('comments', 
            format_contributions.get('closing', {}).get('comments', [])))
        return self._format_slot_contributions_with_indent(result)

    def _format_lilypond_fraction_command_string(self):
        if self._is_visible:
            if self.is_augmentation or \
                (not self._has_power_of_two_denominator) or \
                self.force_fraction:
                return r"\tweak #'text #tuplet-number::calc-fraction-text"
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
                    contributions = []
                    fraction_command_string = \
                        self._format_lilypond_fraction_command_string()
                    if fraction_command_string:
                        contributions.append(fraction_command_string)
                    contributions.append(r'\times {} {{'.format(
                        self._multiplier_fraction_string
                        ))
                else:
                    contributions = ['{']
                result.append([contributor, contributions])
        return tuple(result)

    def _format_opening_slot(self, format_contributions):
        r'''Tuple of format contributions to appear 
        immediately after self opening.
        '''
        result = []
        result.append(('comments', 
            format_contributions.get('opening', {}).get('comments', [])))
        result.append(('lilypond command marks',
            format_contributions.get(
                'opening', {}).get('lilypond command marks', [])))
        return self._format_slot_contributions_with_indent(result)

    ### PUBLIC PROPERTIES ###

    @apply
    def force_fraction():
        def fget(self):
            r'''Read / write boolean to force ``n:m`` fraction in 
            LilyPond format:

            ::

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
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 2/3 {
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
                message = 'bad type for tuplet force fraction: "%s".'
                raise TypeError(message % arg)
        return property(**locals())

    @property
    def implied_prolation(self):
        r'''Tuplet implied prolation.

        Defined equal to tuplet multiplier.

        Return multiplier.
        '''
        return self.multiplier

    @property
    def is_augmentation(self):
        r'''True when multiplier is greater than 1.
        Otherwise false:

        ::

            >>> t = tuplettools.FixedDurationTuplet(
            ...     Duration(2, 8), "c'8 d'8 e'8")
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
        r'''True when multiplier is less than 1.  Otherwise false:

        ::

            >>> t = tuplettools.FixedDurationTuplet(
            ...     Duration(2, 8), "c'8 d'8 e'8")
            >>> t.is_diminution
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
            no tuplet bracket and no tuplet number while preserving the 
            rhythmic value of the tuplet and the contents of the tuplet.

            Return boolean or none.
            '''
            return self._is_invisible
        def fset(self, arg):
            assert isinstance(arg, (bool, type(None)))
            self._is_invisible = arg
        return property(**locals())

    @property
    def is_trivial(self):
        r'''True when tuplet multiplier is one. Otherwise false:

        ::

            >>> tuplet = Tuplet((1, 1), "c'8 d'8 e'8")
            >>> tuplet.is_trivial
            True

        Return boolean.
        '''
        return self.multiplier == 1

    @property
    def lilypond_format(self):
        '''LilyPond format.

        Return string.
        '''
        self._update_marks_of_entire_score_tree_if_necessary()
        return self._format_component()

    @property
    def multiplied_duration(self):
        r'''Multiplied duration of tuplet:

        ::

            >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
            >>> tuplet.multiplied_duration
            Duration(1, 4)

        Return duration.
        '''
        return self.multiplier * self._contents_duration

    @apply
    def multiplier():
        def fget(self):
            r'''Read / write tuplet multiplier:

            ::

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
                message = 'can not set tuplet multiplier: {!r}.'
                raise ValueError(message.format(expr))
            if 0 < rational:
                self._multiplier = rational
            else:
                message = 'tuplet multiplier must be positive: {!r}.'
                raise ValueError(message.format(expr))
        return property(**locals())

    @apply
    def preferred_denominator():
        def fget(self):
            r'''Integer denominator in terms of which tuplet fraction 
            should format:

            ::

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
                    message = 'tuplet preferred denominator must be positive: "%s".'
                    raise ValueError(message % arg)
            elif not isinstance(arg, type(None)):
                message = 'bad tuplet preferred denominator type: "%s".'
                raise TypeError(message % arg)
            self._preferred_denominator = arg
        return property(**locals())

    @property
    def ratio_string(self):
        r'''Tuplet multiplier formatted with colon as ratio:

        ::

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

    ### PUBLIC METHODS ###

    @staticmethod
    def from_duration_and_ratio(
        duration,
        proportions,
        avoid_dots=True,
        decrease_durations_monotonically=True,
        is_diminution=True,
        ):
        r'''Make tuplet from `duration` and `proportions`.

        Example set 1. Make augmented tuplet from `duration` and `proportions` 
        and avoid dots.

        Return tupletted leaves strictly without dots when all `proportions` 
        equal ``1``:

        ::

            >>> print Tuplet.from_duration_and_ratio(
            ...     Duration(3, 16), [1, 1, 1, -1, -1], avoid_dots=True,
            ...     is_diminution=False)
            {@ 5:6 c'32, c'32, c'32, r32, r32 @}

        Allow tupletted leaves to return with dots when some `proportions` 
        do not equal ``1``:

        ::

            >>> print Tuplet.from_duration_and_ratio(
            ...     Duration(3, 16), [1, -2, -2, 3, 3], avoid_dots=True,
            ...     is_diminution=False)
            {@ 11:12 c'64, r32, r32, c'32., c'32. @}

        Interpret nonassignable `proportions` according to
        `decrease_durations_monotonically`:

        ::

            >>> print Tuplet.from_duration_and_ratio(
            ...     Duration(3, 16), [5, -1, 5], avoid_dots=True,
            ...     decrease_durations_monotonically=False,
            ...     is_diminution=False)
            {@ 11:12 c'64, c'16, r64, c'64, c'16 @}

        Example set 2. Make augmented tuplet from `duration` and `proportions` 
        and encourage dots:

        ::

            >>> Tuplet.from_duration_and_ratio(
            ...     Duration(3, 16), [1, 1, 1, -1, -1], avoid_dots=False,
            ...     is_diminution=False)
            FixedDurationTuplet(3/16, [c'64., c'64., c'64., r64., r64.])

        Interpret nonassignable `proportions` according to
        `decrease_durations_monotonically`:

        ::

            >>> Tuplet.from_duration_and_ratio(
            ...     Duration(3, 16), [5, -1, 5], avoid_dots=False,
            ...     decrease_durations_monotonically=False,
            ...     is_diminution=False)
            FixedDurationTuplet(3/16, [c'32..., r128., c'32...])

        Example set 3. Make diminished tuplet from `duration` and nonzero 
        integer `proportions`.

        Return tupletted leaves strictly without dots when all `proportions` 
        equal ``1``:

        ::

            >>> print Tuplet.from_duration_and_ratio(
            ...     Duration(3, 16), [1, 1, 1, -1, -1], avoid_dots=True,
            ...     is_diminution=True)
            {@ 5:3 c'16, c'16, c'16, r16, r16 @}

        Allow tupletted leaves to return with dots when some `proportions` 
        do not equal ``1``:

        ::

            >>> print Tuplet.from_duration_and_ratio(
            ...     Duration(3, 16), [1, -2, -2, 3, 3], avoid_dots=True,
            ...     is_diminution=True)
            {@ 11:6 c'32, r16, r16, c'16., c'16. @}

        Interpret nonassignable `proportions` according to
        `decrease_durations_monotonically`:

        ::

            >>> print Tuplet.from_duration_and_ratio(
            ...     Duration(3, 16), [5, -1, 5], avoid_dots=True,
            ...     decrease_durations_monotonically=False,
            ...     is_diminution=True)
            {@ 11:6 c'32, c'8, r32, c'32, c'8 @}

        Example set 4. Make diminished tuplet from `duration` and 
        `proportions` and encourage dots:

        ::

            >>> Tuplet.from_duration_and_ratio(
            ...     Duration(3, 16), [1, 1, 1, -1, -1], avoid_dots=False,
            ...     is_diminution=True)
            FixedDurationTuplet(3/16, [c'32., c'32., c'32., r32., r32.])

        Interpret nonassignable `proportions` according to `direction`:

        ::

            >>> Tuplet.from_duration_and_ratio(
            ...     Duration(3, 16), [5, -1, 5], avoid_dots=False,
            ...     decrease_durations_monotonically=False,
            ...     is_diminution=True)
            FixedDurationTuplet(3/16, [c'16..., r64., c'16...])

        Reduce `proportions` relative to each other.

        Interpret negative `proportions` as rests.

        Return fixed-duration tuplet.
        '''
        from abjad.tools import leaftools
        from abjad.tools import notetools
        from abjad.tools import resttools
        from abjad.tools import tuplettools
        # coerce duration and proportions
        duration = durationtools.Duration(duration)
        proportions = mathtools.Ratio(proportions)
        # reduce proportions relative to each other
        proportions = \
            sequencetools.divide_sequence_elements_by_greatest_common_divisor(
                proportions)
        # find basic prolated duration of note in tuplet
        basic_prolated_duration = duration / mathtools.weight(proportions)
        # find basic written duration of note in tuplet
        if avoid_dots:
            basic_written_duration = \
                basic_prolated_duration.equal_or_greater_power_of_two
        else:
            basic_written_duration = \
                basic_prolated_duration.equal_or_greater_assignable
        # find written duration of each note in tuplet
        written_durations = [x * basic_written_duration for x in proportions]
        # make tuplet leaves
        try:
            notes = [notetools.Note(0, x) 
                if 0 < x else resttools.Rest(abs(x)) for x in written_durations]
        except AssignabilityError:
            denominator = duration._denominator
            note_durations = [durationtools.Duration(x, denominator) 
                for x in proportions]
            pitches = [None if note_duration < 0 else 0 
                for note_duration in note_durations]
            leaf_durations = [abs(note_duration) 
                for note_duration in note_durations]
            notes = leaftools.make_leaves(
                pitches,
                leaf_durations,
                decrease_durations_monotonically=decrease_durations_monotonically,
                )
        # make tuplet
        tuplet = tuplettools.FixedDurationTuplet(duration, notes)
        # fix tuplet contents if necessary
        tuplettools.fix_contents_of_tuplets_in_expr(tuplet)
        # change prolation if necessary
        if not tuplet.multiplier == 1:
            if is_diminution:
                if not tuplet.is_diminution:
                    tuplettools.change_augmented_tuplets_in_expr_to_diminished(
                        tuplet)
            else:
                if tuplet.is_diminution:
                    tuplettools.change_diminished_tuplets_in_expr_to_augmented(
                        tuplet)
        # return tuplet
        return tuplet


    @staticmethod
    def from_ratio_and_nonreduced_fraction(proportions, (n, d)):
        r'''Divide nonreduced fraction `(n, d)` according to `proportions`.

        Example 1. Make container when no prolation is necessary:

        ::

            >>> ratio = [1]
            >>> Tuplet.from_ratio_and_nonreduced_fraction(ratio, (7, 16))
            {c'4..}

        Example 2. Make fixed-duration tuplet when prolation is necessary:

        ::

            >>> ratio = [1, 2]
            >>> Tuplet.from_ratio_and_nonreduced_fraction(ratio, (7, 16))
            FixedDurationTuplet(7/16, [c'8, c'4])

        ::

            >>> ratio = [1, 2, 4]
            >>> Tuplet.from_ratio_and_nonreduced_fraction(ratio, (7, 16))
            FixedDurationTuplet(7/16, [c'16, c'8, c'4])

        ::

            >>> ratio = [1, 2, 4, 1]
            >>> Tuplet.from_ratio_and_nonreduced_fraction(ratio, (7, 16))
            FixedDurationTuplet(7/16, [c'16, c'8, c'4, c'16])

        ::

            >>> ratio = [1, 2, 4, 1, 2]
            >>> Tuplet.from_ratio_and_nonreduced_fraction(ratio, (7, 16))
            FixedDurationTuplet(7/16, [c'16, c'8, c'4, c'16, c'8])

        ::

            >>> ratio = [1, 2, 4, 1, 2, 4]
            >>> Tuplet.from_ratio_and_nonreduced_fraction(ratio, (7, 16))
            FixedDurationTuplet(7/16, [c'16, c'8, c'4, c'16, c'8, c'4])

        Note that method interprets `d` as tuplet denominator.

        Return tuplet or container.
        '''
        from abjad.tools import containertools
        from abjad.tools import notetools
        from abjad.tools import resttools
        from abjad.tools import tuplettools
        proportions = mathtools.NonreducedRatio(proportions)
        duration = durationtools.Duration(n, d)
        if len(proportions) == 1:
            if 0 < proportions[0]:
                try:
                    note = notetools.Note(0, duration)
                    return containertools.Container([note])
                except AssignabilityError:
                    notes = notetools.make_notes(0, duration)
                    return containertools.Container(notes)
            elif proportions[0] < 0:
                try:
                    rest = resttools.Rest(duration)
                    return containertools.Container([rest])
                except AssignabilityError:
                    rests = resttools.make_rests(duration)
                    return containertools.Container(rests)
            else:
                raise ValueError('no divide zero values.')
        if 1 < len(proportions):
            exponent = int(
                math.log(mathtools.weight(proportions), 2) - math.log(n, 2))
            denominator = int(d * 2 ** exponent)
            music = []
            for x in proportions:
                if not x:
                    raise ValueError('no divide zero values.')
                if 0 < x:
                    try:
                        note = notetools.Note(0, (x, denominator))
                        music.append(note)
                    except AssignabilityError:
                        notes = notetools.make_notes(0, (x, denominator))
                        music.extend(notes)
                else:
                    rests = resttools.Rest((-x, denominator))
                    music.append(rests)
            return tuplettools.FixedDurationTuplet(duration, music)
