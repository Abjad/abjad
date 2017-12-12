import copy
from .Container import Container


class Measure(Container):
    r'''Measure.

    ..  container:: example

        >>> measure = abjad.Measure((4, 8), "c'8 d'8 e'8 f'8")
        >>> abjad.show(measure) # doctest: +SKIP

    ..  docs::

        >>> abjad.f(measure)
        { % measure
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        } % measure

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_always_format_time_signature',
        '_automatically_adjust_time_signature',
        '_measure_number',
        '_implicit_scaling',
        )

    _bracket_comment = ' % measure'

    _is_counttime_component = True

    ### INITIALIZER ###

    def __init__(
        self,
        time_signature=None,
        components=None,
        implicit_scaling=False,
        ):
        import abjad
        # set time signature adjustment before contents initialization
        self._automatically_adjust_time_signature = False
        time_signature = time_signature or abjad.TimeSignature((4, 4))
        time_signature = abjad.TimeSignature(time_signature)
        self.implicit_scaling = bool(implicit_scaling)
        Container.__init__(self, components)
        self._always_format_time_signature = False
        self._measure_number = None
        time_signature = abjad.TimeSignature(time_signature)
        abjad.attach(time_signature, self)

    ### SPECIAL METHODS ###

    def __delitem__(self, i):
        r'''Deletes measure item `i`.

        ..  container:: example

            >>> measure = abjad.Measure((4, 8), "c'8 d'8 e'8 f'8")
            >>> measure.automatically_adjust_time_signature = True
            >>> abjad.show(measure) # doctest: +SKIP

            >>> del(measure[1])
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

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
        Container.__delitem__(self, i)
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

            >>> measure = abjad.Measure((3, 8), "c'8 d'8 e'8")
            >>> abjad.show(measure) # doctest: +SKIP

            >>> measure
            Measure((3, 8), "c'8 d'8 e'8")

        Returns string.
        '''
        import abjad
        class_name = type(self).__name__
        indicator = self._get_indicator(abjad.TimeSignature)
        forced_time_signature = indicator
        forced_time_signature = forced_time_signature.pair
        summary = self._get_contents_summary()
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

    def __setitem__(self, i, argument):
        r'''Sets measure item `i` to `argument`.

        ..  container:: example

            >>> measure = abjad.Measure((4, 8), "c'8 d'8 e'8 f'8")
            >>> measure.automatically_adjust_time_signature = True
            >>> abjad.show(measure) # doctest: +SKIP

            >>> measure[1] = abjad.Note("ds'8.")
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

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
        Container.__setitem__(self, i, argument)
        self._conditionally_adjust_time_signature(old_denominator)

    ### PRIVATE METHODS ###

    def _all_contents_are_scalable_by_multiplier(self, multiplier):
        import abjad
        multiplier = abjad.Multiplier(multiplier)
        for component in self:
            if isinstance(component, abjad.Leaf):
                candidate_duration = multiplier * component.written_duration
                if not candidate_duration.is_assignable:
                    return False
        return True

    def _append_spacer_skip(self):
        import abjad
        if not self.is_underfull:
            return
        target_duration = self.time_signature.duration
        duration = self._get_duration()
        skip = abjad.Skip((1, 1))
        time_signature_multiplier = self.time_signature.implied_prolation
        new_duration = target_duration - duration
        new_multiplier = new_duration.__div__(time_signature_multiplier)
        abjad.attach(new_multiplier, skip)
        self.append(skip)

    def _as_graphviz_node(self):
        import abjad
        node = abjad.Component._as_graphviz_node(self)
        fraction = abjad.NonreducedFraction(
            self.time_signature.numerator,
            self.time_signature.denominator,
            )
        node[0].extend([
            abjad.graphtools.GraphvizTableRow([
                abjad.graphtools.GraphvizTableCell(
                    label=type(self).__name__,
                    attributes={'border': 0},
                    ),
                ]),
            abjad.graphtools.GraphvizTableHorizontalRule(),
            abjad.graphtools.GraphvizTableRow([
                abjad.graphtools.GraphvizTableCell(
                    label=str(fraction),
                    attributes={'border': 0},
                    ),
                ]),
            ])
        return node

    def _check_duration(self):
        effective_time_signature = self.time_signature
        if (effective_time_signature.has_non_power_of_two_denominator and
            effective_time_signature.suppress):
            message = 'can not suppress time signature'
            message += ' with non-power-of-two denominator.'
            raise Exception(message)
        if effective_time_signature.duration < self._get_preprolated_duration():
            raise OverfullContainerError
        if self._get_preprolated_duration() < effective_time_signature.duration:
            raise UnderfullContainerError

    def _conditionally_adjust_time_signature(self, old_denominator):
        import abjad
        if self.automatically_adjust_time_signature:
            naive_time_signature = self._get_preprolated_duration()
            better_time_signature = \
                abjad.NonreducedFraction(naive_time_signature)
            better_time_signature = \
                better_time_signature.with_denominator(old_denominator)
            better_time_signature = abjad.TimeSignature(better_time_signature)
            abjad.detach(abjad.TimeSignature, self)
            abjad.attach(better_time_signature, self)

    # essentially the same as container version of method;
    # the definition given here adds one line to remove
    # time signature immediately after instantiation
    # because the indicator-copying code will then provide time signature.
    def _copy_with_indicators_but_without_children_or_spanners(self):
        import abjad
        new = type(self)(*self.__getnewargs__())
        # only the following line differs from Container
        abjad.detach(abjad.TimeSignature, new)
        if getattr(self, '_lilypond_grob_name_manager', None) is not None:
            new._lilypond_grob_name_manager = copy.copy(abjad.override(self))
        if getattr(self, '_lilypond_setting_name_manager', None) is not None:
            new._lilypond_setting_name_manager = copy.copy(abjad.setting(self))
        for indicator in self._get_indicators():
            new_indicator = copy.copy(indicator)
            abjad.attach(new_indicator, new)
        new.is_simultaneous = self.is_simultaneous
        new.implicit_scaling = self.implicit_scaling
        return new

    @staticmethod
    def _duration_to_time_signature(
        duration,
        denominators=None,
        factor=None,
        ):
        import abjad
        duration = abjad.Duration(duration)
        if denominators is not None:
            if factor is not None:
                denominators = [
                    d for d in denominators
                    if factor in abjad.mathtools.factors(d)
                    ]
            for desired_denominator in sorted(denominators):
                nonreduced_fraction = abjad.NonreducedFraction(duration)
                candidate_pair = \
                    nonreduced_fraction.with_denominator(desired_denominator)
                if candidate_pair.denominator == desired_denominator:
                    return abjad.TimeSignature(candidate_pair)
        if factor is not None:
            if factor in abjad.mathtools.factors(duration.denominator):
                return abjad.TimeSignature(duration)
            else:
                time_signature_numerator = factor * duration.numerator
                time_signature_denominator = factor * duration.denominator
                return abjad.TimeSignature(
                    (time_signature_numerator, time_signature_denominator))
        else:
            return abjad.TimeSignature(duration)

    def _format_content_pieces(self):
        import abjad
        result = []
        if (self.has_non_power_of_two_denominator and
            type(self) is Measure and
            self.implicit_scaling):
            indent = abjad.LilyPondFormatManager.indent
            string = "{}\\scaleDurations #'({} . {}) {{"
            string = string.format(
                indent,
                self.implied_prolation.numerator,
                self.implied_prolation.denominator,
                )
            result.append(string)
            pieces = Container._format_content_pieces(self)
            pieces = [indent + _ for _ in pieces]
            result.extend(pieces)
            result.append(indent + '}')
        else:
            result.extend(Container._format_content_pieces(self))
        return result

    def _format_opening_slot(self, bundle):
        result = []
        result.append(('comments', bundle.opening.comments))
        result.append(('grob overrides', bundle.grob_overrides))
        result.append(('context settings', bundle.context_settings))
        result.append(('indicators', bundle.opening.indicators))
        return self._format_slot_contributions_with_indent(result)

    def _get_compact_representation(self):
        if not self:
            return '| {!s} |'.format(self.time_signature)
        return '| {!s} {} |'.format(
            self.time_signature,
            self._get_contents_summary(),
            )

    def _get_format_specification(self):
        names = []
        if self.implicit_scaling:
            names.append('implicit_scaling')
        return abjad.FormatSpecification(
            client=self,
            repr_args_values=[
                self.time_signature.pair,
                self._get_contents_summary(),
                ],
            storage_format_args_values=[
                self.time_signature,
                self._get_contents_summary(),
                ],
            storage_format_kwargs_names=names,
            )

    def _get_lilypond_format(self):
        self._check_duration()
        return self._format_component()

    def _get_preprolated_duration(self):
        time_signature_prolation = 1
        if self.implicit_scaling:
            time_signature_prolation = self.time_signature.implied_prolation
        return time_signature_prolation * self._get_contents_duration()

    # TODO: see if self._scale can be combined with
    #       with self.scale_and_adjust_time_signature()
    def _scale(self, multiplier=None):
        import abjad
        if multiplier is None:
            return
        multiplier = abjad.Multiplier(multiplier)
        old_time_signature = self.time_signature
        if (abjad.mathtools.is_nonnegative_integer_power_of_two(multiplier) and
            1 <= multiplier):
            old_numerator = old_time_signature.numerator
            old_denominator = old_time_signature.denominator
            new_denominator = old_denominator // multiplier.numerator
            pair = (old_numerator, new_denominator)
            new_time_signature = abjad.TimeSignature(pair)
        else:
            old_denominator = old_time_signature.denominator
            old_duration = old_time_signature.duration
            new_duration = multiplier * old_duration
            new_time_signature = self._duration_to_time_signature(
                new_duration,
                [old_denominator],
                multiplier.denominator,
                )
        abjad.detach(abjad.TimeSignature, self)
        abjad.attach(new_time_signature, self)
        contents_multiplier_denominator = \
            abjad.mathtools.greatest_power_of_two_less_equal(
                multiplier.denominator)
        pair = (multiplier.numerator, contents_multiplier_denominator)
        contents_multiplier = abjad.Multiplier(*pair)
        self._scale_contents(contents_multiplier)

    def _scale_denominator(self, factor):
        import abjad
        # save old time signature duration
        old_time_signature_duration = self.time_signature.duration
        # find new time signature
        new_time_signature = self._duration_to_time_signature(
            old_time_signature_duration,
            factor=factor,
            )
        # scale contents of measures in argument
        multiplier = new_time_signature.implied_prolation.reciprocal
        self._scale(multiplier)
        # assign new time signature
        abjad.detach(abjad.TimeSignature, self)
        abjad.attach(new_time_signature, self)
        if new_time_signature.has_non_power_of_two_denominator:
            self.implicit_scaling = True

    ### PUBLIC PROPERTIES ###

    @property
    def always_format_time_signature(self):
        '''Gets and sets flag to indicate whether time signature
        should appear in LilyPond format even when not expected.

        ..  container:: example

            >>> measure = abjad.Measure((4, 8), "c'8 d'8 e'8 f'8")
            >>> measure.always_format_time_signature
            False

        Set to true when necessary to print the same signature repeatedly.

        Defaults to false.

        Returns true or false.
        '''
        return self._always_format_time_signature

    @always_format_time_signature.setter
    def always_format_time_signature(self, argument):
        assert isinstance(argument, bool)
        self._always_format_time_signature = argument

    @property
    def automatically_adjust_time_signature(self):
        '''Gets and sets flag to indicate whether time signature
        should update automatically following mutation.

        ..  container:: example

            >>> measure = abjad.Measure((3, 4), "c' d' e'")
            >>> abjad.show(measure) # doctest: +SKIP

            >>> measure.automatically_adjust_time_signature = True
            >>> measure.append('r')
            >>> abjad.show(measure) # doctest: +SKIP

        Defaults to false.

        Returns true or false.
        '''
        return self._automatically_adjust_time_signature

    @automatically_adjust_time_signature.setter
    def automatically_adjust_time_signature(self, argument):
        assert isinstance(argument, bool)
        self._automatically_adjust_time_signature = argument

    @property
    def has_non_power_of_two_denominator(self):
        r'''Is true when measure time signature denominator
        is not an integer power of 2.

        ..  container:: example

            >>> measure = abjad.Measure((5, 9), "c'8 d' e' f' g'")
            >>> measure.implicit_scaling = True
            >>> abjad.show(measure) # doctest: +SKIP

            >>> measure.has_non_power_of_two_denominator
            True

        Otherwise false:

        ..  container:: example

            >>> measure = abjad.Measure((5, 8), "c'8 d' e' f' g'")
            >>> abjad.show(measure) # doctest: +SKIP

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

            >>> measure = abjad.Measure((5, 8), "c'8 d' e' f' g'")
            >>> abjad.show(measure) # doctest: +SKIP

            >>> measure.has_power_of_two_denominator
            True

        Otherwise false:

        ..  container:: example

            >>> measure = abjad.Measure((5, 9), "c'8 d' e' f' g'")
            >>> measure.implicit_scaling = True
            >>> abjad.show(measure) # doctest: +SKIP

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
    def implicit_scaling(self, argument):
        assert isinstance(argument, bool)
        self._implicit_scaling = argument

    @property
    def implied_prolation(self):
        r'''Implied prolation of measure.

        ..  container:: example

            Measures with implicit scaling scale the duration of their
            contents:

            >>> measure = abjad.Measure((5, 12), "c'8 d'8 e'8 f'8 g'8")
            >>> measure.implicit_scaling = True
            >>> abjad.show(measure) # doctest: +SKIP

            >>> measure.implied_prolation
            Multiplier(2, 3)

            >>> for note in measure:
            ...     note, abjad.inspect(note).get_duration()
            (Note("c'8"), Duration(1, 12))
            (Note("d'8"), Duration(1, 12))
            (Note("e'8"), Duration(1, 12))
            (Note("f'8"), Duration(1, 12))
            (Note("g'8"), Duration(1, 12))

        ..  container:: example

            Measures without implicit scaling turned on do not
            scale the duration of their contents:

            >>> measure = abjad.Measure((5, 12), [])
            >>> measure.implicit_scaling = False

            >>> measure.implied_prolation
            Multiplier(1, 1)

        Returns positive multiplier.
        '''
        import abjad
        if self.implicit_scaling:
            time_signature = self.time_signature
            return time_signature.implied_prolation
        return abjad.Multiplier(1)

    @property
    def is_full(self):
        r'''Is true when measure duration equals time signature duration.

        ..  container:: example

            >>> measure = abjad.Measure((4, 8), "c'8 d'8 e'8 f'8")
            >>> abjad.show(measure) # doctest: +SKIP

            >>> measure.is_full
            True

        Otherwise false.

        Returns true or false.
        '''
        return self._get_preprolated_duration() == self.target_duration

    @property
    def is_misfilled(self):
        '''Is true when measure is either underfull or overfull.

        ..  container:: example

            >>> measure = abjad.Measure((3, 4), "c'4 d'4 e'4 f'4")
            >>> measure.is_misfilled
            True

        Otherwise false:

        ..  container:: example

            >>> measure = abjad.Measure((3, 4), "c' d' e'")
            >>> abjad.show(measure) # doctest: +SKIP

            >>> measure.is_misfilled
            False

        Returns true or false.
        '''
        return not self.is_full

    @property
    def is_overfull(self):
        '''Is true when measure duration is greater than time signature
        duration.

        ..  container:: example

            >>> measure = abjad.Measure((3, 4), "c'4 d' e' f'")

            >>> measure.is_overfull
            True

        Otherwise false.

        Returns true or false.
        '''
        return self.target_duration < self._get_preprolated_duration()

    @property
    def is_underfull(self):
        '''Is true when measure duration is less than time signature duration.

        ..  container:: example

            >>> measure = abjad.Measure((3, 4), "c'4 d'")

            >>> measure.is_underfull
            True

        Otherwise false.

        Returns true or false.
        '''
        return self._get_preprolated_duration() < self.target_duration

    @property
    def measure_number(self):
        r'''Gets 1-indexed measure number.

        ..  container:: example

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Measure((3, 4), "c' d' e'"))
            >>> staff.append(abjad.Measure((2, 4), "f' g'"))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    { % measure
                        \time 3/4
                        c'4
                        d'4
                        e'4
                    } % measure
                    { % measure
                        \time 2/4
                        f'4
                        g'4
                    } % measure
                }

            >>> staff[0].measure_number
            1

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

            >>> measure = abjad.Measure((3, 4), "c'4 d'4 e'4")
            >>> measure.target_duration
            Duration(3, 4)

        Returns duration.
        '''
        return self.time_signature.duration

    @property
    def time_signature(self):
        r'''Gets effective time signature of measure.

        ..  container:: example

            >>> measure = abjad.Measure((3, 4), "c'4 d'4 e'4")
            >>> measure.time_signature
            TimeSignature((3, 4))

        Returns time signature or none.
        '''
        import abjad
        return self._get_effective(abjad.TimeSignature)

    ### PUBLIC METHODS ###

    @classmethod
    def from_selections(class_, selections, time_signatures=None):
        r'''Makes a selection of measures from `selections`.

        Returns selections.
        '''
        import abjad
        assert len(selections)
        if not time_signatures:
            time_signatures = [_.get_duration() for _ in selections]
        assert len(selections) == len(time_signatures)
        durations = [_.get_duration() for _ in selections]
        assert durations == [abjad.Duration(_) for _ in time_signatures]
        maker = abjad.MeasureMaker()
        measures = maker(time_signatures)
        temporary_voice = abjad.Voice(measures)
        abjad.mutate(temporary_voice).replace_measure_contents(selections)
        temporary_voice[:] = []
        return measures

    # TODO: see if self._scale can be combined with
    #       with self.scale_and_adjust_time_signature()
    def scale_and_adjust_time_signature(self, multiplier=None):
        r'''Scales `measure` by `multiplier` and adjusts time signature.

        ..  container:: example

            Scales measure by non-power-of-two multiplier:

            >>> measure = abjad.Measure((3, 8), "c'8 d'8 e'8")
            >>> measure.implicit_scaling = True
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(measure)
                { % measure
                    \time 3/8
                    c'8
                    d'8
                    e'8
                } % measure

            >>> measure.scale_and_adjust_time_signature(abjad.Multiplier(2, 3))
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(measure)
                { % measure
                    \time 3/12
                    \scaleDurations #'(2 . 3) {
                        c'8
                        d'8
                        e'8
                    }
                } % measure

        Returns none.
        '''
        import abjad
        if multiplier == 0:
            raise ZeroDivisionError
        old_time_signature = self.time_signature
        old_pair = old_time_signature.pair
        old_multiplier = old_time_signature.implied_prolation
        old_multiplier_pair = old_multiplier.pair
        multiplied_pair = abjad.NonreducedFraction(old_multiplier_pair)
        multiplied_pair = multiplied_pair.multiply_without_reducing(multiplier)
        multiplied_pair = multiplied_pair.pair
        reduced_pair = abjad.NonreducedFraction(old_multiplier_pair)
        reduced_pair = reduced_pair.multiply_with_cross_cancelation(multiplier)
        reduced_pair = reduced_pair.pair
        if reduced_pair != multiplied_pair:
            new_pair = abjad.NonreducedFraction(old_pair)
            new_pair = new_pair.multiply(multiplier, preserve_numerator=True)
            new_time_signature = abjad.TimeSignature(new_pair)
            abjad.detach(abjad.TimeSignature, self)
            abjad.attach(new_time_signature, self)
            remaining_multiplier = abjad.Multiplier(reduced_pair)
            if remaining_multiplier != abjad.Multiplier(1):
                self._scale_contents(remaining_multiplier)
        elif self._all_contents_are_scalable_by_multiplier(multiplier):
            self._scale_contents(multiplier)
            if (old_time_signature.has_non_power_of_two_denominator or
                not abjad.mathtools.is_nonnegative_integer_power_of_two(
                    multiplier)):
                new_pair = abjad.NonreducedFraction(old_pair)
                new_pair = new_pair.multiply_with_cross_cancelation(multiplier)
                new_pair = new_pair.pair
            # multiplier is a negative power of two, like 1/2, 1/4, etc.
            elif multiplier < abjad.Multiplier(0):
                new_pair = abjad.NonreducedFraction.multiply_without_reducing(
                    old_pair,
                    multiplier,
                    )
            # multiplier is a nonnegative power of two, like 0, 1, 2, 4, etc.
            elif abjad.Multiplier(0) < multiplier:
                new_pair = abjad.NonreducedFraction(old_pair)
                new_pair = new_pair.multiply(
                    multiplier,
                    preserve_numerator=True,
                    )
            elif multiplier == abjad.Multiplier(0):
                raise ZeroDivisionError
            new_time_signature = abjad.TimeSignature(new_pair)
            abjad.detach(abjad.TimeSignature, self)
            abjad.attach(new_time_signature, self)
            if new_time_signature.has_non_power_of_two_denominator:
                self.implicit_scaling = True
        else:
            new_pair = abjad.NonreducedFraction(old_pair)
            new_pair = new_pair.multiply(multiplier, preserve_numerator=True)
            new_time_signature = abjad.TimeSignature(new_pair)
            abjad.detach(abjad.TimeSignature, self)
            abjad.attach(new_time_signature, self)
            if new_time_signature.has_non_power_of_two_denominator:
                self.implicit_scaling = True
            implied_prolation = new_time_signature.implied_prolation
            remaining_multiplier = multiplier / implied_prolation
            if remaining_multiplier != abjad.Multiplier(1):
                self._scale_contents(remaining_multiplier)
