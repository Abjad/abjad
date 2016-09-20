# -*- coding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import mathtools
from abjad.tools import systemtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import mutate
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import set_
from abjad.tools.scoretools.FixedDurationContainer \
    import FixedDurationContainer


class Measure(FixedDurationContainer):
    r'''A measure.

    ..  container:: example

        >>> measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
        >>> show(measure) # doctest: +SKIP

    ..  doctest::

        >>> print(format(measure))
        {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = (
        '_always_format_time_signature',
        '_automatically_adjust_time_signature',
        '_measure_number',
        '_implicit_scaling',
        )

    _is_counttime_component = True

    ### INITIALIZER ###

    def __init__(
        self,
        time_signature=None,
        music=None,
        implicit_scaling=False,
        ):
        # set time signature adjustment before contents initialization
        self._automatically_adjust_time_signature = False
        time_signature = time_signature or (4, 4)
        self.implicit_scaling = bool(implicit_scaling)
        FixedDurationContainer.__init__(self, time_signature, music)
        self._always_format_time_signature = False
        self._measure_number = None
        time_signature = indicatortools.TimeSignature(time_signature)
        attach(time_signature, self)

    ### SPECIAL METHODS ###

    def __delitem__(self, i):
        r'''Deletes measure item `i`.

        ..  container:: example

            ::

                >>> measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
                >>> measure.automatically_adjust_time_signature = True
                >>> show(measure) # doctest: +SKIP

            ::

                >>> del(measure[1])
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                {
                    \time 3/8
                    c'8
                    e'8
                    f'8
                }

        Returns none.
        '''
        old_time_signature = self.time_signature
        old_denominator = getattr(old_time_signature, 'denominator', None)
        FixedDurationContainer.__delitem__(self, i)
        self._conditionally_adjust_time_signature(old_denominator)

    def __getnewargs__(self):
        r'''Gets new arguments of measure.

        Returns pair.
        '''
        time_signature = self.time_signature
        return (time_signature.pair,)

    def __repr__(self):
        r'''Gets interpreter representation of measure.

        ..  container:: example

            ::

                >>> measure = Measure((3, 8), "c'8 d'8 e'8")
                >>> show(measure) # doctest: +SKIP

            ::

                >>> measure
                Measure((3, 8), "c'8 d'8 e'8")

        Returns string.
        '''
        class_name = type(self).__name__
        indicator = self._get_indicator(indicatortools.TimeSignature)
        forced_time_signature = indicator
        forced_time_signature = forced_time_signature.pair
        summary = self._contents_summary
        if forced_time_signature and len(self):
            if self.implicit_scaling:
                result = '{}({!s}, {!r}, implicit_scaling=True)'
                result = result.format(
                    class_name,
                    forced_time_signature,
                    summary,
                    )
            else:
                result = '{}({!s}, {!r})'
                result = result.format(
                    class_name,
                    forced_time_signature,
                    summary,
                    )
            return result
        elif forced_time_signature:
            if self.implicit_scaling:
                string = '{}({!s}, implicit_scaling=True)'
            else:
                string = '{}({!s})'
            string = string.format(class_name, forced_time_signature)
            return string
        else:
            if self.implicit_scaling:
                return '{}(implicit_scaling=True)'.format(class_name)
            else:
                return '{}()'.format(class_name)

    def __setitem__(self, i, expr):
        r'''Sets measure item `i` to `expr`.

        ..  container:: example

            ::

                >>> measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
                >>> measure.automatically_adjust_time_signature = True
                >>> show(measure) # doctest: +SKIP

            ::

                >>> measure[1] = Note("ds'8.")
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                {
                    \time 9/16
                    c'8
                    ds'8.
                    e'8
                    f'8
                }

        Returns none.
        '''
        old_time_signature = self.time_signature
        old_denominator = getattr(old_time_signature, 'denominator', None)
        FixedDurationContainer.__setitem__(self, i, expr)
        self._conditionally_adjust_time_signature(old_denominator)

    ### PRIVATE METHODS ###

    def _all_contents_are_scalable_by_multiplier(self, multiplier):
        from abjad.tools import scoretools
        multiplier = durationtools.Multiplier(multiplier)
        for component in self:
            if isinstance(component, scoretools.Leaf):
                candidate_duration = multiplier * component.written_duration
                if not candidate_duration.is_assignable:
                    return False
        return True

    def _as_graphviz_node(self):
        from abjad.tools import documentationtools
        from abjad.tools import scoretools
        node = scoretools.Component._as_graphviz_node(self)
        fraction = mathtools.NonreducedFraction(
            self.time_signature.numerator,
            self.time_signature.denominator,
            )
        node[0].extend([
            documentationtools.GraphvizTableRow([
                documentationtools.GraphvizTableCell(
                    label=type(self).__name__,
                    attributes={'border': 0},
                    ),
                ]),
            documentationtools.GraphvizTableHorizontalRule(),
            documentationtools.GraphvizTableRow([
                documentationtools.GraphvizTableCell(
                    label=str(fraction),
                    attributes={'border': 0},
                    ),
                ]),
            ])
        return node

    def _check_duration(self):
        effective_time_signature = self.time_signature
        if effective_time_signature.has_non_power_of_two_denominator and \
            effective_time_signature.suppress:
            message = 'can not suppress time signature'
            message += ' with non-power-of-two denominator.'
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
                indicatortools.TimeSignature(better_time_signature)
            detach(indicatortools.TimeSignature, self)
            attach(better_time_signature, self)

    # essentially the same as container version of method;
    # the definition given here adds one line to remove
    # time signature immediately after instantiation
    # because the indicator-copying code will then provide time signature.
    def _copy_with_indicators_but_without_children_or_spanners(self):
        from abjad.tools import indicatortools
        new = type(self)(*self.__getnewargs__())
        # only the following line differs from Container
        detach(indicatortools.TimeSignature, new)
        if getattr(self, '_lilypond_grob_name_manager', None) is not None:
            new._lilypond_grob_name_manager = copy.copy(override(self))
        if getattr(self, '_lilypond_setting_name_manager', None) is not None:
            new._lilypond_setting_name_manager = copy.copy(set_(self))
        for indicator in self._get_indicators():
            new_indicator = copy.copy(indicator)
            attach(new_indicator, new)
        new.is_simultaneous = self.is_simultaneous
        new.implicit_scaling = self.implicit_scaling
        return new

    @staticmethod
    def _duration_and_possible_denominators_to_time_signature(
        duration,
        denominators=None,
        factor=None,
        ):
        # check input
        duration = durationtools.Duration(duration)
        if denominators is not None:
            if factor is not None:
                denominators = [
                    d for d in denominators
                    if factor in mathtools.factors(d)
                    ]
            for desired_denominator in sorted(denominators):
                nonreduced_fraction = mathtools.NonreducedFraction(duration)
                candidate_pair = \
                    nonreduced_fraction.with_denominator(desired_denominator)
                if candidate_pair.denominator == desired_denominator:
                    return indicatortools.TimeSignature(candidate_pair)
        if factor is not None:
            if factor in mathtools.factors(duration.denominator):
                return indicatortools.TimeSignature(duration)
            else:
                time_signature_numerator = factor * duration.numerator
                time_signature_denominator = factor * duration.denominator
                return indicatortools.TimeSignature(
                    (time_signature_numerator, time_signature_denominator))
        else:
            return indicatortools.TimeSignature(duration)

    def _format_content_pieces(self):
        from abjad.tools import systemtools
        result = []
        if self.has_non_power_of_two_denominator and \
            type(self) is Measure and \
            self.implicit_scaling:
            indent = systemtools.LilyPondFormatManager.indent
            string = "{}\\scaleDurations #'({} . {}) {{"
            string = string.format(
                indent,
                self.implied_prolation.numerator,
                self.implied_prolation.denominator,
                )
            result.append(string)
            pieces = FixedDurationContainer._format_content_pieces(self)
            pieces = [indent + x for x in pieces]
            result.extend(pieces)
            result.append(indent + '}')
        else:
            result.extend(FixedDurationContainer._format_content_pieces(self))
        return result

    def _format_opening_slot(self, bundle):
        result = []
        result.append(('comments', bundle.opening.comments))
        result.append(('grob overrides', bundle.grob_overrides))
        result.append(('context settings', bundle.context_settings))
        result.append(('indicators', bundle.opening.indicators))
        return self._format_slot_contributions_with_indent(result)

    def _get_format_specification(self):
        names = []
        if self.implicit_scaling:
            names.append('implicit_scaling')
        return systemtools.FormatSpecification(
            client=self,
            repr_args_values=[
                self.time_signature.pair,
                self._contents_summary,
                ],
            storage_format_args_values=[
                self.time_signature,
                self._contents_summary,
                ],
            storage_format_kwargs_names=names,
            )

    @staticmethod
    def _get_likely_multiplier_of_components(components):
        pass
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        from abjad.tools import sequencetools
        assert all(isinstance(x, scoretools.Component) for x in components)
        logical_tie_duration_numerators = []
        for expr in \
            iterate(components).by_topmost_logical_ties_and_components():
            if isinstance(expr, selectiontools.LogicalTie):
                logical_tie_duration = expr._preprolated_duration
                logical_tie_duration_numerators.append(
                    logical_tie_duration.numerator)
        if len(sequencetools.remove_repeated_elements(
            logical_tie_duration_numerators)) == 1:
            numerator = logical_tie_duration_numerators[0]
            denominator = mathtools.greatest_power_of_two_less_equal(numerator)
            likely_multiplier = durationtools.Multiplier(
                numerator, denominator)
            return likely_multiplier

    # TODO: see if self._scale can be combined with
    #       with self.scale_and_adjust_time_signature()
    def _scale(self, multiplier=None):
        from abjad.tools import indicatortools
        if multiplier is None:
            return
        multiplier = durationtools.Multiplier(multiplier)
        old_time_signature = self.time_signature
        if mathtools.is_nonnegative_integer_power_of_two(multiplier) and \
            1 <= multiplier:
            old_numerator = old_time_signature.numerator
            old_denominator = old_time_signature.denominator
            new_denominator = old_denominator // multiplier.numerator
            pair = (old_numerator, new_denominator)
            new_time_signature = indicatortools.TimeSignature(pair)
        else:
            old_denominator = old_time_signature.denominator
            old_duration = old_time_signature.duration
            new_duration = multiplier * old_duration
            new_time_signature = \
                self._duration_and_possible_denominators_to_time_signature(
                    new_duration,
                    [old_denominator],
                    multiplier.denominator,
                    )
        detach(indicatortools.TimeSignature, self)
        attach(new_time_signature, self)
        contents_multiplier_denominator = \
            mathtools.greatest_power_of_two_less_equal(multiplier.denominator)
        pair = (multiplier.numerator, contents_multiplier_denominator)
        contents_multiplier = durationtools.Multiplier(*pair)
        self._scale_contents(contents_multiplier)

    ### PUBLIC METHODS ###

    @classmethod
    def from_selections(class_, selections, time_signatures=None):
        r'''Makes a selection of measures from `selections`.

        Returns selections.
        '''
        from abjad.tools import scoretools
        assert len(selections)
        if not time_signatures:
            time_signatures = [_.get_duration() for _ in selections]
        assert len(selections) == len(time_signatures)
        assert [_.get_duration() for _ in selections] == \
            [durationtools.Duration(_) for _ in time_signatures]
        measures = scoretools.make_spacer_skip_measures(time_signatures)
        temporary_voice = scoretools.Voice(measures)
        mutate(temporary_voice).replace_measure_contents(selections)
        temporary_voice[:] = []
        return measures

    # TODO: see if self._scale can be combined with
    #       with self.scale_and_adjust_time_signature()
    def scale_and_adjust_time_signature(self, multiplier=None):
        r'''Scales `measure` by `multiplier` and adjusts time signature.

        ..  container:: example

            Scales measure by non-power-of-two multiplier:

            ::

                >>> measure = Measure((3, 8), "c'8 d'8 e'8")
                >>> measure.implicit_scaling = True
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
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

                >>> print(format(measure))
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
        from abjad.tools import indicatortools
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
            new_time_signature = indicatortools.TimeSignature(new_pair)
            detach(indicatortools.TimeSignature, self)
            attach(new_time_signature, self)
            remaining_multiplier = durationtools.Multiplier(reduced_pair)
            if remaining_multiplier != durationtools.Multiplier(1):
                self._scale_contents(remaining_multiplier)
        elif self._all_contents_are_scalable_by_multiplier(multiplier):
            self._scale_contents(multiplier)
            if (
                old_time_signature.has_non_power_of_two_denominator or
                not mathtools.is_nonnegative_integer_power_of_two(multiplier)
                ):
                new_pair = mathtools.NonreducedFraction(old_pair)
                new_pair = new_pair.multiply_with_cross_cancelation(multiplier)
                new_pair = new_pair.pair
            # multiplier is a negative power of two, like 1/2, 1/4, etc.
            elif multiplier < durationtools.Multiplier(0):
                new_pair = \
                    mathtools.NonreducedFraction.multiply_without_reducing(
                        old_pair, multiplier)
            # multiplier is a nonnegative power of two, like 0, 1, 2, 4, etc.
            elif durationtools.Multiplier(0) < multiplier:
                new_pair = mathtools.NonreducedFraction(old_pair)
                new_pair = new_pair.multiply_with_numerator_preservation(
                    multiplier)
            elif multiplier == durationtools.Multiplier(0):
                raise ZeroDivisionError
            new_time_signature = indicatortools.TimeSignature(new_pair)
            detach(indicatortools.TimeSignature, self)
            attach(new_time_signature, self)
            if new_time_signature.has_non_power_of_two_denominator:
                self.implicit_scaling = True
        else:
            new_pair = mathtools.NonreducedFraction(old_pair)
            new_pair = new_pair.multiply_with_numerator_preservation(
                multiplier)
            new_time_signature = indicatortools.TimeSignature(new_pair)
            detach(indicatortools.TimeSignature, self)
            attach(new_time_signature, self)
            if new_time_signature.has_non_power_of_two_denominator:
                self.implicit_scaling = True
            remaining_multiplier = \
                multiplier / new_time_signature.implied_prolation
            if remaining_multiplier != durationtools.Multiplier(1):
                self._scale_contents(remaining_multiplier)

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        if not self:
            return '| {!s} |'.format(self.time_signature)
        return '| {!s} {} |'.format(
            self.time_signature,
            self._contents_summary,
            )

    @property
    def _lilypond_format(self):
        self._check_duration()
        return self._format_component()

    @property
    def _one_line_input_string(self):
        time_signature = self.time_signature
        pair = (time_signature.numerator, time_signature.denominator)
        contents_string = ' '.join([str(x) for x in self])
        result = '{}({}, {!r}, implicit_scaling={})'
        result = result.format(
            type(self).__name__,
            pair,
            contents_string,
            self.implicit_scaling,
            )
        return result

    @property
    def _preprolated_duration(self):
        time_signature_prolation = 1
        if self.implicit_scaling:
            time_signature_prolation = self.time_signature.implied_prolation
        return time_signature_prolation * self._contents_duration

    ### PUBLIC PROPERTIES ###

    @property
    def always_format_time_signature(self):
        '''Gets and sets flag to indicate whether time signature
        should appear in LilyPond format even when not expected.

        ..  container:: example

            ::

                >>> measure.always_format_time_signature
                False

        Set to true when necessary to print the same signature repeatedly.

        Defaults to false.

        Returns true or false.
        '''
        return self._always_format_time_signature

    @always_format_time_signature.setter
    def always_format_time_signature(self, expr):
        assert isinstance(expr, bool)
        self._always_format_time_signature = expr

    @property
    def automatically_adjust_time_signature(self):
        '''Gets and sets flag to indicate whether time signature
        should update automatically following mutation.

        ..  container:: example

            ::

                >>> measure = Measure((3, 4), "c' d' e'")
                >>> show(measure) # doctest: +SKIP

            ::

                >>> measure.automatically_adjust_time_signature = True
                >>> measure.append('r')
                >>> show(measure) # doctest: +SKIP

        Defaults to false.

        Returns true or false.
        '''
        return self._automatically_adjust_time_signature

    @automatically_adjust_time_signature.setter
    def automatically_adjust_time_signature(self, expr):
        assert isinstance(expr, bool)
        self._automatically_adjust_time_signature = expr

    @property
    def has_non_power_of_two_denominator(self):
        r'''Is true when measure time signature denominator
        is not an integer power of 2.

        ..  container:: example

            ::

                >>> measure = Measure((5, 9), "c'8 d' e' f' g'")
                >>> measure.implicit_scaling = True
                >>> show(measure) # doctest: +SKIP

            ::

                >>> measure.has_non_power_of_two_denominator
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> measure = Measure((5, 8), "c'8 d' e' f' g'")
                >>> show(measure) # doctest: +SKIP

            ::

                >>> measure.has_non_power_of_two_denominator
                False

        Returns true or false.
        '''
        time_signature = self.time_signature
        return time_signature.has_non_power_of_two_denominator

    @property
    def has_power_of_two_denominator(self):
        r'''Is true when measure time signature denominator
        is an integer power of 2.

        ..  container:: example

            ::

                >>> measure = Measure((5, 8), "c'8 d' e' f' g'")
                >>> show(measure) # doctest: +SKIP

            ::

                >>> measure.has_power_of_two_denominator
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> measure = Measure((5, 9), "c'8 d' e' f' g'")
                >>> measure.implicit_scaling = True
                >>> show(measure) # doctest: +SKIP

            ::

                >>> measure.has_power_of_two_denominator
                False

        Returns true or false.
        '''
        return not self.has_non_power_of_two_denominator

    @property
    def implicit_scaling(self):
        r'''Is true when measure should scale contents. Otherwise false.

        Returns true or false.
        '''
        return self._implicit_scaling

    @implicit_scaling.setter
    def implicit_scaling(self, arg):
        assert isinstance(arg, bool)
        self._implicit_scaling = arg

    @property
    def implied_prolation(self):
        r'''Implied prolation of measure.

        ..  container:: example

            Measures with implicit scaling scale the duration of their
            contents:

            ::

                >>> measure = Measure((5, 12), "c'8 d'8 e'8 f'8 g'8")
                >>> measure.implicit_scaling = True
                >>> show(measure) # doctest: +SKIP

            ::

                >>> measure.implied_prolation
                Multiplier(2, 3)

            ::

                >>> for note in measure:
                ...     note, inspect_(note).get_duration()
                (Note("c'8"), Duration(1, 12))
                (Note("d'8"), Duration(1, 12))
                (Note("e'8"), Duration(1, 12))
                (Note("f'8"), Duration(1, 12))
                (Note("g'8"), Duration(1, 12))

        ..  container:: example

            Measures without implicit scaling turned on do not
            scale the duration of their contents:

            ::

                >>> measure = Measure((5, 12), [])
                >>> measure.implicit_scaling = False

            ::

                >>> measure.implied_prolation
                Multiplier(1, 1)

        Returns positive multiplier.
        '''
        if self.implicit_scaling:
            time_signature = self.time_signature
            return time_signature.implied_prolation
        return durationtools.Multiplier(1)

    @property
    def is_full(self):
        r'''Is true when measure duration equals time signature duration.

        ..  container:: example

            ::

                >>> measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
                >>> show(measure) # doctest: +SKIP

            ::

                >>> measure.is_full
                True

        Otherwise false.

        Returns true or false.
        '''
        return FixedDurationContainer.is_full.fget(self)

    @property
    def is_misfilled(self):
        '''Is true when measure is either underfull or overfull.

        ..  container:: example

            ::

                >>> measure = Measure((3, 4), "c'4 d'4 e'4 f'4")
                >>> measure.is_misfilled
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> measure = Measure((3, 4), "c' d' e'")
                >>> show(measure) # doctest: +SKIP

            ::

                >>> measure.is_misfilled
                False

        Returns true or false.
        '''
        return FixedDurationContainer.is_overfull.fget(self)

    @property
    def is_overfull(self):
        '''Is true when measure duration is greater than time signature
        duration.

        ..  container:: example

            ::

                >>> measure = Measure((3, 4), "c'4 d' e' f'")

            ::

                >>> measure.is_overfull
                True

        Otherwise false.

        Returns true or false.
        '''
        return FixedDurationContainer.is_overfull.fget(self)

    @property
    def is_underfull(self):
        '''Is true when measure duration is less than time signature duration.

        ..  container:: example

            ::

                >>> measure = Measure((3, 4), "c'4 d'")

            ::

                >>> measure.is_underfull
                True

        Otherwise false.

        Returns true or false.
        '''
        return FixedDurationContainer.is_underfull.fget(self)

    @property
    def measure_number(self):
        r'''Gets 1-indexed measure number.

        ..  container:: example

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((3, 4), "c' d' e'"))
                >>> staff.append(Measure((2, 4), "f' g'"))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
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
        r'''Gets target duration of measure.

        Target duration of measure is always equal to duration
        of effective time signature.

        ..  container:: example

            ::

                >>> measure = Measure((3, 4), "c'4 d'4 e'4")
                >>> measure.target_duration
                Duration(3, 4)

        Returns duration.
        '''
        return self.time_signature.duration

    @property
    def time_signature(self):
        r'''Gets effective time signature of measure.

        ..  container:: example

            ::

                >>> measure.time_signature
                TimeSignature((3, 4))

        Returns time signature or none.
        '''
        from abjad.tools import indicatortools
        return self._get_effective(indicatortools.TimeSignature)
