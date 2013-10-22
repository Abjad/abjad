# -*- encoding: utf-8 -*-
import copy
from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools import mathtools
from abjad.tools.containertools.FixedDurationContainer \
    import FixedDurationContainer


class Measure(FixedDurationContainer):
    r'''A measure.

    ..  container:: example

        >>> measure = Measure((4, 8), "c'8 d' e' f'")
        >>> show(measure) # doctest: +SKIP

    ..  doctest::

        >>> f(measure)
        {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_always_format_time_signature', 
        '_automatically_adjust_time_signature',
        '_measure_number',
        )

    _is_counttime_component = True

    ### INITIALIZER ###

    def __init__(self, time_signature, music=None, **kwargs):
        # set time signature adjustment indicator before 
        # contents initialization
        self._automatically_adjust_time_signature = False
        FixedDurationContainer.__init__(self, time_signature, music)
        self._always_format_time_signature = False
        self._measure_number = None
        time_signature = contexttools.TimeSignatureMark(time_signature)
        time_signature.attach(self)
        self._initialize_keyword_values(**kwargs)

    ### SPECIAL METHODS ###

    # TODO: remove in favor of measuretools.fuse_measures()
    def __add__(self, arg):
        r'''Add two measures together in-score or outside-of-score.

        Wrapper around ``measuretools.fuse_measures()``.
        '''
        assert isinstance(arg, type(self))
        from abjad.tools import measuretools
        from abjad.tools import selectiontools
        measures = selectiontools.SliceSelection([self, arg])
        new = measuretools.fuse_measures(measures)
        return new

    def __delitem__(self, i):
        r'''Container item deletion with optional time signature adjustment.
        '''
        old_time_signature = self.time_signature
        old_denominator = getattr(old_time_signature, 'denominator', None)
        FixedDurationContainer.__delitem__(self, i)
        self._conditionally_adjust_time_signature(old_denominator)

    def __getnewargs__(self):
        time_signature = self.time_signature
        return (time_signature.pair, )

    def __repr__(self):
        r'''Interpreter representation of measure.

        Returns string.
        '''
        class_name = self._class_name
        forced_time_signature = self._get_mark(contexttools.TimeSignatureMark)
        summary = self._summary
        length = len(self)
        if forced_time_signature and length:
            return '%s(%s, [%s])' % (
                class_name, forced_time_signature, summary)
        elif forced_time_signature:
            return '%s(%s)' % (class_name, forced_time_signature)
        elif length:
            return '%s([%s])' % (class_name, summary)
        else:
            return '%s()' % class_name

    def __setitem__(self, i, expr):
        r'''Container setitem logic with optional time signature adjustment.

        Measure setitem logic now adjusts time signatue automatically
        when ``adjust_time_signature_automatically`` is true.
        '''
        old_time_signature = self.time_signature
        old_denominator = getattr(old_time_signature, 'denominator', None)
        FixedDurationContainer.__setitem__(self, i, expr)
        self._conditionally_adjust_time_signature(old_denominator)

    def __str__(self):
        r'''String form of measure with pipes for single string display.
        '''
        forced_time_signature = self.time_signature
        summary = self._space_delimited_summary
        length = len(self)
        if forced_time_signature and length:
            return '|%s %s|' % (forced_time_signature, summary)
        elif forced_time_signature:
            return '|%s|' % forced_time_signature
        elif length:
            return '|%s|' % summary
        else:
            return '| |'

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        r'''Display form of measure used for spanners to display
        potentially many spanned measures one after the other.
        '''
        return '|{}({})|'.format(
            self.time_signature,
            len(self),
            )

    # essentially the same as container version of method;
    # the definition given here adds one line to remove
    # time signature immediately after instantiation
    # because the mark-copying code will then provide time signature.
    def _copy_with_marks_but_without_children_or_spanners(self):
        from abjad.tools import marktools
        new = type(self)(*self.__getnewargs__())
        # only the following line differs from Conatainer
        for mark in new._get_marks(contexttools.TimeSignatureMark):
            mark.detach()
        if getattr(self, '_override', None) is not None:
            new._override = copy.copy(self.override)
        if getattr(self, '_set', None) is not None:
            new._set = copy.copy(self.set)
        for mark in self._get_marks():
            new_mark = copy.copy(mark)
            new_mark.attach(new)
        new.is_simultaneous = self.is_simultaneous
        return new

    @property
    def _one_line_input_string(self):
        time_signature = self.time_signature
        pair = (time_signature.numerator, time_signature.denominator)
        contents_string = ' '.join([str(x) for x in self])
        result = '%s(%s, %r)' % (type(self).__name__, pair, contents_string)
        return result

    @property
    def _preprolated_duration(self):
        from abjad.tools import contexttools
        time_signature = self.time_signature
        return time_signature.implied_prolation * self._contents_duration

    ### PRIVATE METHODS ###

    def _all_contents_are_scalable_by_multiplier(self, multiplier):
        from abjad.tools import leaftools
        multiplier = durationtools.Multiplier(multiplier)
        for component in self:
            if isinstance(component, leaftools.Leaf):
                candidate_duration = multiplier * component.written_duration
                if not candidate_duration.is_assignable:
                    return False
        return True

    def _check_duration(self):
        from abjad.tools import contexttools
        effective_time_signature = self.time_signature
        if effective_time_signature.has_non_power_of_two_denominator and \
            effective_time_signature.suppress:
            message = 'Can not suppress time signature'
            message += ' with non-power of two denominator.'
            raise Exception(message)
        if effective_time_signature.duration < self._preprolated_duration:
            raise OverfullContainerError
        if self._preprolated_duration < effective_time_signature.duration:
            raise UnderfullContainerError

    def _conditionally_adjust_time_signature(self, old_denominator):
        if self.automatically_adjust_time_signature:
            naive_time_signature = self._preprolated_duration
            better_time_signature = \
                mathtools.NonreducedFraction(naive_time_signature)
            better_time_signature = \
                better_time_signature.with_denominator(old_denominator)
            better_time_signature = \
                contexttools.TimeSignatureMark(better_time_signature)
            for mark in self._get_marks(contexttools.TimeSignatureMark):
                mark.detach()
            better_time_signature.attach(self)

    def _format_content_pieces(self):
        result = []
        # the class name test here functions to exclude scaleDurations 
        # from anonymous and dynamic measures
        # TODO: subclass this prooperly on anonymous and dynamic measures
        if self.has_non_power_of_two_denominator and type(self) is Measure:
            result.append("\t\\scaleDurations #'(%s . %s) {" % (
                self.implied_prolation.numerator,
                self.implied_prolation.denominator))
            result.extend( ['\t' + x 
                for x in FixedDurationContainer._format_content_pieces(self)])
            result.append('\t}')
        else:
            result.extend(FixedDurationContainer._format_content_pieces(self))
        return result

    def _format_opening_slot(self, format_contributions):
        r'''This is the slot where LilyPond grob \override commands live.
        This is also the slot where LilyPond \time commands live.
        '''
        result = []
        result.append(('comments', 
            format_contributions.get('opening', {}).get('comments', [])))
        result.append(('grob overrides', 
            format_contributions.get('grob overrides', [])))
        result.append(('context settings', 
            format_contributions.get('context settings', [])))
        result.append(('context marks', 
            format_contributions.get('opening', {}).get('context marks', [])))
        return self._format_slot_contributions_with_indent(result)

    @staticmethod
    def _get_likely_multiplier_of_components(components):
        pass
        from abjad.tools import componenttools
        from abjad.tools import iterationtools
        from abjad.tools import leaftools
        from abjad.tools import selectiontools
        from abjad.tools import sequencetools
        assert all(isinstance(x, componenttools.Component) for x in components)
        chain_duration_numerators = []
        for expr in \
            iterationtools.iterate_topmost_tie_chains_and_components_in_expr(
            components):
            if isinstance(expr, selectiontools.TieChain):
                chain_duration = expr._preprolated_duration
                chain_duration_numerators.append(chain_duration.numerator)
        if len(sequencetools.truncate_runs_in_sequence(
            chain_duration_numerators)) == 1:
            numerator = chain_duration_numerators[0]
            denominator = mathtools.greatest_power_of_two_less_equal(numerator)
            likely_multiplier = durationtools.Multiplier(numerator, denominator)
            return likely_multiplier

    # TODO: see if self._scale can be combined with
    #       with self.scale_and_adjust_time_signature()
    def _scale(self, multiplier=None):
        from abjad.tools import containertools
        from abjad.tools import contexttools
        from abjad.tools import iterationtools
        from abjad.tools import timesignaturetools
        if multiplier is None:
            return
        multiplier = durationtools.Multiplier(multiplier)
        old_time_signature = self.time_signature
        if mathtools.is_nonnegative_integer_power_of_two(multiplier) and \
            1 <= multiplier:
            old_numerator = old_time_signature.numerator
            old_denominator = old_time_signature.denominator
            new_denominator = old_denominator / multiplier.numerator
            pair = (old_numerator, new_denominator)
            new_time_signature = contexttools.TimeSignatureMark(pair)
        else:
            old_denominator = old_time_signature.denominator
            old_duration = old_time_signature.duration
            new_duration = multiplier * old_duration
            new_time_signature = \
                timesignaturetools.duration_and_possible_denominators_to_time_signature(
                new_duration, [old_denominator], multiplier.denominator)
        for mark in self._get_marks(contexttools.TimeSignatureMark):
            mark.detach()
        new_time_signature.attach(self)
        contents_multiplier_denominator = \
            mathtools.greatest_power_of_two_less_equal(multiplier.denominator)
        pair = (multiplier.numerator, contents_multiplier_denominator)
        contents_multiplier = durationtools.Multiplier(*pair)
        self._scale_contents(contents_multiplier)

    ### PUBLIC PROPERTIES ###

    @apply
    def always_format_time_signature():
        def fget(self):
            '''Read / write flag to indicate whether time signature
            should appear in LilyPond format even when not expected.

            Set to true when necessary to print the same signature repeatedly.

            Default to false.

            Returns boolean.
            '''
            return self._always_format_time_signature
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._always_format_time_signature = expr
        return property(**locals())

    @apply
    def automatically_adjust_time_signature():
        def fget(self):
            '''Read / write flag to indicate whether time signature
            should update automatically following contents-changing 
            operations:

            ::

                >>> measure = Measure((3, 4), "c' d' e'")

            ::

                >>> measure
                Measure(3/4, [c'4, d'4, e'4])

            ::

                >>> measure.automatically_adjust_time_signature = True
                >>> measure.append('r')

            ::

                >>> measure
                Measure(4/4, [c'4, d'4, e'4, r4])

            Default to false.

            Returns boolean.
            '''
            return self._automatically_adjust_time_signature
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._automatically_adjust_time_signature = expr
        return property(**locals())

    @property
    def has_non_power_of_two_denominator(self):
        r'''True when measure time signature denominator 
        is not an integer power of 2:

        ::

            >>> measure = Measure((5, 9), "c'8 d' e' f' g'")
            >>> measure.has_non_power_of_two_denominator
            True

        Otherwise false:

        ::

            >>> measure = Measure((5, 8), "c'8 d' e' f' g'")
            >>> measure.has_non_power_of_two_denominator
            False

        Returns boolean.
        '''
        time_signature = self.time_signature
        return time_signature.has_non_power_of_two_denominator

    @property
    def has_power_of_two_denominator(self):
        r'''True when measure time signature denominator 
        is an integer power of 2:

        ::

            >>> measure = Measure((5, 8), "c'8 d' e' f' g'")
            >>> measure.has_power_of_two_denominator
            True

        Otherwise false:

        ::

            >>> measure = Measure((5, 9), "c'8 d' e' f' g'")
            >>> measure.has_power_of_two_denominator
            False

        Returns boolean.
        '''
        return not self.has_non_power_of_two_denominator

    @property
    def implied_prolation(self):
        r'''Implied prolation of measure time signature:

        ::

            >>> measure = Measure((5, 12), "c'8 d' e' f' g'")

        ::

            >>> measure.implied_prolation
            Multiplier(2, 3)

        Returns multiplier.
        '''
        time_signature = self.time_signature
        return time_signature.implied_prolation

    @property
    def is_full(self):
        r'''True when prolated duration equals time signature duration:

        ::

            >>> measure = Measure((4, 8), "c'8 d'8 e'8 f'8")

        ::

            >>> measure.is_full
            True

        Otherwise false.

        Returns boolean.
        '''
        return FixedDurationContainer.is_full.fget(self)

    @property
    def is_misfilled(self):
        '''True when measure is either underfull or overfull:

        ::

            >>> measure = Measure((3, 4), "c' d' e' f'")

        ::

            >>> measure
            Measure(3/4, [c'4, d'4, e'4, f'4])

        ::

            >>> measure.is_misfilled
            True

        Otherwise false:

        ::

            >>> measure = Measure((3, 4), "c' d' e'")

        ::

            >>> measure
            Measure(3/4, [c'4, d'4, e'4])

        ::

            >>> measure.is_misfilled
            False

        Returns boolean.
        '''
        return FixedDurationContainer.is_overfull.fget(self)

    @property
    def is_overfull(self):
        '''True when prolated duration is greater than time signature duration:

        ::

            >>> measure = Measure((3, 4), "c'4 d' e' f'")

        ::

            >>> measure.is_overfull
            True

        Otherwise false.

        Returns boolean.
        '''
        return FixedDurationContainer.is_overfull.fget(self)

    @property
    def is_underfull(self):
        '''True when prolated duration is less than time signature duration:

        ::

            >>> measure = Measure((3, 4), "c'4 d'")

        ::

            >>> measure.is_underfull
            True

        Otherwise false.

        Returns boolean.
        '''
        return FixedDurationContainer.is_underfull.fget(self)

    @property
    def lilypond_format(self):
        self._check_duration()
        return self._format_component()

    @property
    def measure_number(self):
        r'''1-indexed measure number:

        ::

            >>> staff = Staff()
            >>> staff.append(Measure((3, 4), "c' d' e'"))
            >>> staff.append(Measure((2, 4), "f' g'"))

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 3/4
                    c'4
                    d'4
                    e'4
                }
                {
                    \time 2/4
                    f'4
                    g'4
                }
            }

        ::

            >>> staff[0].measure_number
            1

        ::

            >>> staff[1].measure_number
            2

        Returns positive integer.
        '''
        self._update_now(offsets=True)
        return self._measure_number

    @property
    def target_duration(self):
        r'''Target duration of measure always equal to duration 
        of effective time signature.

        Returns duration.
        '''
        return self.time_signature.duration

    @property
    def time_signature(self):
        r'''Effective time signature of measure.

        Returns time signature or none.
        '''
        from abjad.tools import contexttools
        return self._get_effective_context_mark(contexttools.TimeSignatureMark)

    ### PUBLIC METHODS ###

    # TODO: see if self._scale can be combined with
    #       with self.scale_and_adjust_time_signature()
    def scale_and_adjust_time_signature(self, multiplier=None):
        r'''Scales `measure` by `multiplier` and adjusts time signature:

        ..  container:: example

            **Example 1.** Scale measure by non-power-of-two multiplier:

            ::

                >>> measure = Measure((3, 8), "c'8 d'8 e'8")
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> f(measure)
                {
                    \time 3/8
                    c'8
                    d'8
                    e'8
                }

            ::

                >>> measure.scale_and_adjust_time_signature(Multiplier(2, 3))
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> f(measure)
                {
                    \time 3/12
                    \scaleDurations #'(2 . 3) {
                        c'8
                        d'8
                        e'8
                    }
                }

        Returns none.
        '''
        from abjad.tools import containertools
        from abjad.tools import contexttools
        if multiplier == 0:
            raise ZeroDivisionError
        old_time_signature = self.time_signature
        old_pair = \
            (old_time_signature.numerator, old_time_signature.denominator)
        old_multiplier = old_time_signature.implied_prolation
        old_multiplier_pair = \
            (old_multiplier.numerator, old_multiplier.denominator)
        multiplied_pair = mathtools.NonreducedFraction(old_multiplier_pair)
        multiplied_pair = multiplied_pair.multiply_without_reducing(multiplier)
        multiplied_pair = multiplied_pair.pair
        reduced_pair = mathtools.NonreducedFraction(old_multiplier_pair)
        reduced_pair = reduced_pair.multiply_with_cross_cancelation(multiplier)
        reduced_pair = reduced_pair.pair
        if reduced_pair != multiplied_pair:
            new_pair = mathtools.NonreducedFraction(old_pair)
            new_pair = \
                new_pair.multiply_with_numerator_preservation(multiplier)
            new_time_signature = contexttools.TimeSignatureMark(new_pair)
            for mark in self._get_marks(contexttools.TimeSignatureMark):
                mark.detach()
            new_time_signature.attach(self)
            remaining_multiplier = durationtools.Multiplier(reduced_pair)
            if remaining_multiplier != durationtools.Multiplier(1):
                self._scale_contents(remaining_multiplier)
        elif self._all_contents_are_scalable_by_multiplier(multiplier):
            self._scale_contents(multiplier)
            if old_time_signature.has_non_power_of_two_denominator or \
                not mathtools.is_nonnegative_integer_power_of_two(multiplier):
                new_pair = mathtools.NonreducedFraction(old_pair)
                new_pair = new_pair.multiply_with_cross_cancelation(multiplier)
                new_pair = new_pair.pair
            # multiplier is a negative power of two, like 1/2, 1/4, etc.
            elif multiplier < durationtools.Multiplier(0):
                new_pair = \
                    durationtools.multiply_duration_pair(old_pair, multiplier)
            # multiplier is a nonnegative power of two, like 0, 1, 2, 4, etc.
            elif durationtools.Multiplier(0) < multiplier:
                new_pair = mathtools.NonreducedFraction(old_pair)
                new_pair = new_pair.multiply_with_numerator_preservation(
                    multiplier)
            elif multiplier == durationtools.Multiplier(0):
                raise ZeroDivisionError
            new_time_signature = contexttools.TimeSignatureMark(new_pair)
            for mark in self._get_marks(contexttools.TimeSignatureMark):
                mark.detach()
            new_time_signature.attach(self)
        else:
            new_pair = mathtools.NonreducedFraction(old_pair)
            new_pair = new_pair.multiply_with_numerator_preservation(
                multiplier)
            new_time_signature = contexttools.TimeSignatureMark(new_pair)
            for mark in self._get_marks(contexttools.TimeSignatureMark):
                mark.detach()
            new_time_signature.attach(self)
            remaining_multiplier = \
                multiplier / new_time_signature.implied_prolation
            if remaining_multiplier != durationtools.Multiplier(1):
                self._scale_contents(remaining_multiplier)
