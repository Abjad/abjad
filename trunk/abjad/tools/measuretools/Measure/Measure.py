import copy
from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools import mathtools
from abjad.tools.containertools.FixedDurationContainer import FixedDurationContainer


class Measure(FixedDurationContainer):
    r'''.. versionadded:: 1.1

    Abjad model of a measure::

        >>> measure = Measure((4, 8), "c'8 d' e' f'")

    ::

        >>> measure
        Measure(4/8, [c'8, d'8, e'8, f'8])

    ::

        >>> f(measure)
        {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }

    Return measure object.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_always_format_time_signature', '_automatically_adjust_time_signature',
        '_measure_number', )

    ### INITIALIZER ###

    def __init__(self, time_signature, music=None, **kwargs):
        # set time signature adjustment indicator before contents initialization
        self._automatically_adjust_time_signature = False
        FixedDurationContainer.__init__(self, time_signature, music)
        self._always_format_time_signature = False
        self._measure_number = None
        time_signature = contexttools.TimeSignatureMark(time_signature)
        time_signature.attach(self)
        self._initialize_keyword_values(**kwargs)

    ### SPECIAL METHODS ###

    def __add__(self, arg):
        '''Add two measures together in-score or outside-of-score.
        Wrapper around measuretools.fuse_measures.
        '''
        assert isinstance(arg, type(self))
        from abjad.tools import measuretools
        new = measuretools.fuse_measures([self, arg])
        return new

    def __delitem__(self, i):
        '''Container item deletion with optional time signature adjustment.
        '''
        old_time_signature = contexttools.get_effective_time_signature(self)
        old_denominator = getattr(old_time_signature, 'denominator', None)
        FixedDurationContainer.__delitem__(self, i)
        self._conditionally_adjust_time_signature(old_denominator)

    def __getnewargs__(self):
        time_signature = contexttools.get_effective_time_signature(self)
        return (time_signature.pair, )

    def __repr__(self):
        '''String form of measure with parentheses for interpreter display.
        '''
        class_name = type(self).__name__
        forced_time_signature = contexttools.get_time_signature_mark_attached_to_component(self)
        summary = self._summary
        length = len(self)
        if forced_time_signature and length:
            return '%s(%s, [%s])' % (class_name, forced_time_signature, summary)
        elif forced_time_signature:
            return '%s(%s)' % (class_name, forced_time_signature)
        elif length:
            return '%s([%s])' % (class_name, summary)
        else:
            return '%s()' % class_name

    def __setitem__(self, i, expr):
        '''Container setitem logic with optional time signature adjustment.

        Measure setitem logic now adjusts time signatue automatically
        when ``adjust_time_signature_automatically`` is true.
        '''
        old_time_signature = contexttools.get_effective_time_signature(self)
        old_denominator = getattr(old_time_signature, 'denominator', None)
        FixedDurationContainer.__setitem__(self, i, expr)
        self._conditionally_adjust_time_signature(old_denominator)

    def __str__(self):
        '''String form of measure with pipes for single string display.
        '''
        forced_time_signature = contexttools.get_effective_time_signature(self)
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

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        '''Display form of measure used for spanners to display
        potentially many spanned measures one after the other.
        '''
        return '|%s(%s)|' % (contexttools.get_effective_time_signature(self), len(self))

    # essentially the same as container version of method;
    # the definition given here adds one line to remove
    # time signature immediately after instantiation
    # because the mark-copying code will then provide time signature.
    def _copy_with_marks_but_without_children_or_spanners(self):
        from abjad.tools import marktools
        new = type(self)(*self.__getnewargs__())
        # only the following line differs from Conatainer
        contexttools.detach_time_signature_marks_attached_to_component(new)
        if getattr(self, '_override', None) is not None:
            new._override = copy.copy(self.override)
        if getattr(self, '_set', None) is not None:
            new._set = copy.copy(self.set)
        for mark in marktools.get_marks_attached_to_component(self):
            new_mark = copy.copy(mark)
            new_mark.attach(new)
        new.is_parallel = self.is_parallel
        return new

    ### PRIVATE METHODS ###

    def _check_duration(self):
        from abjad.tools import contexttools
        effective_time_signature = contexttools.get_effective_time_signature(self)
        if effective_time_signature.has_non_power_of_two_denominator and effective_time_signature.suppress:
            raise Exception('Can not suppress time signature with non-power of two denominator.')
        if effective_time_signature.duration < self.preprolated_duration:
            raise OverfullContainerError
        if self.preprolated_duration < effective_time_signature.duration:
            raise UnderfullContainerError

    def _conditionally_adjust_time_signature(self, old_denominator):
        if self.automatically_adjust_time_signature:
            naive_time_signature = self.preprolated_duration
            better_time_signature = mathtools.NonreducedFraction(naive_time_signature)
            better_time_signature = better_time_signature.with_denominator(old_denominator)
            better_time_signature = contexttools.TimeSignatureMark(better_time_signature)
            contexttools.detach_time_signature_marks_attached_to_component(self)
            better_time_signature.attach(self)

    def _format_content_pieces(self):
        result = []
        # the class name test here functions to exclude scaleDurations from anonymous and dynamic measures
        # TODO: subclass this prooperly on anonymous and dynamic measures
        if self.has_non_power_of_two_denominator and self._class_name == 'Measure':
            result.append("\t\\scaleDurations #'(%s . %s) {" % (
                self.implied_prolation.numerator,
                self.implied_prolation.denominator))
            result.extend( ['\t' + x for x in FixedDurationContainer._format_content_pieces(self)])
            result.append('\t}')
        else:
            result.extend(FixedDurationContainer._format_content_pieces(self))
        return result

    def _format_opening_slot(self, format_contributions):
        r'''This is the slot where LilyPond grob \override commands live.
        This is also the slot where LilyPond \time commands live.
        '''
        result = []
        result.append(('comments', format_contributions.get('opening', {}).get('comments', [])))
        result.append(('grob overrides', format_contributions.get('grob overrides', [])))
        result.append(('context settings', format_contributions.get('context settings', [])))
        result.append(('context marks', format_contributions.get('opening', {}).get('context marks', [])))
        #result.append(formattools.get_comment_format_contributions_for_slot(self, 'opening'))
        #result.append(formattools.get_grob_override_format_contributions(self))
        #result.append(formattools.get_context_setting_format_contributions(self))
        #result.append(formattools.get_context_mark_format_contributions_for_slot(self, 'opening'))
        return self._format_slot_contributions_with_indent(result)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def has_non_power_of_two_denominator(self):
        '''True when measure time signature denominator is not an integer power of 2::

            >>> measure = Measure((5, 9), "c'8 d' e' f' g'")
            >>> measure.has_non_power_of_two_denominator
            True

        Otherwise false::

            >>> measure = Measure((5, 8), "c'8 d' e' f' g'")
            >>> measure.has_non_power_of_two_denominator
            False

        Return boolean.
        '''
        return contexttools.get_effective_time_signature(self).has_non_power_of_two_denominator

    @property
    def has_power_of_two_denominator(self):
        '''True when measure time signature denominator is an integer power of 2::

            >>> measure = Measure((5, 8), "c'8 d' e' f' g'")
            >>> measure.has_power_of_two_denominator
            True

        Otherwise false::

            >>> measure = Measure((5, 9), "c'8 d' e' f' g'")
            >>> measure.has_power_of_two_denominator
            False

        Return boolean.
        '''
        return not self.has_non_power_of_two_denominator

    @property
    def implied_prolation(self):
        '''Implied prolation of measure time signature::

            >>> measure = Measure((5, 12), "c'8 d' e' f' g'")

        ::

            >>> measure.implied_prolation
            Multiplier(2, 3)

        Return multiplier.
        '''
        return contexttools.get_effective_time_signature(self).implied_prolation

    @property
    def is_full(self):
        '''True when prolated duration equals time signature duration::

            >>> measure = Measure((4, 8), "c'8 d'8 e'8 f'8")

        ::

            >>> measure.is_full
            True

        Otherwise false.

        Return boolean.
        '''
        return FixedDurationContainer.is_full.fget(self)

    @property
    def is_misfilled(self):
        '''.. versionadded:: 2.9

        True when measure is either underfull or overfull::

            >>> measure = Measure((3, 4), "c' d' e' f'")

        ::

            >>> measure
            Measure(3/4, [c'4, d'4, e'4, f'4])

        ::

            >>> measure.is_misfilled
            True

        Otherwise false::

            >>> measure = Measure((3, 4), "c' d' e'")

        ::

            >>> measure
            Measure(3/4, [c'4, d'4, e'4])

        ::

            >>> measure.is_misfilled
            False

        Return boolean.
        '''
        return FixedDurationContainer.is_overfull.fget(self)

    @property
    def is_overfull(self):
        '''.. versionadded:: 1.1

        True when prolated duration is greater than time signature duration::

            >>> measure = Measure((3, 4), "c'4 d' e' f'")

        ::

            >>> measure.is_overfull
            True

        Otherwise false.

        Return boolean.
        '''
        return FixedDurationContainer.is_overfull.fget(self)

    @property
    def is_underfull(self):
        '''.. versionadded:: 1.1

        True when prolated duration is less than time signature duration::

            >>> measure = Measure((3, 4), "c'4 d'")

        ::

            >>> measure.is_underfull
            True

        Otherwise false.

        Return boolean.
        '''
        return FixedDurationContainer.is_underfull.fget(self)

    @property
    def lilypond_format(self):
        self._check_duration()
        return self._format_component()

    @property
    def measure_number(self):
        r'''1-indexed measure number::

            >>> staff = Staff()
            >>> staff.append(Measure((3, 4), "c' d' e'"))
            >>> staff.append(Measure((2, 4), "f' g'"))

        ::

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

        Return positive integer.
        '''
        self._update_prolated_offset_values_of_entire_score_tree_if_necessary()
        return self._measure_number

    @property
    def preprolated_duration(self):
        '''Preprolated duration of measure::

            >>> measure = Measure((5, 12), "c'8 d' e' f' g'")

        ::

            >>> measure.preprolated_duration
            Duration(5, 12)

        Equal measure contents duration times time signature multiplier.

        Return duration.
        '''
        from abjad.tools import contexttools
        return contexttools.get_effective_time_signature(self).implied_prolation * self.contents_duration

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def always_format_time_signature():
        def fget(self):
            '''.. versionadded:: 2.9

            Read / write flag to indicate whether time signature
            should appear in LilyPond format even when not expected.

            Set to true when necessary to print the same signature repeatedly.

            Default to false.

            Return boolean.
            '''
            return self._always_format_time_signature
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._always_format_time_signature = expr
        return property(**locals())

    @apply
    def automatically_adjust_time_signature():
        def fget(self):
            '''.. versionadded:: 2.9

            Read / write flag to indicate whether time signature
            should update automatically following contents-changing operations::

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

            Return boolean.
            '''
            return self._automatically_adjust_time_signature
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._automatically_adjust_time_signature = expr
        return property(**locals())

    @property
    def target_duration(self):
        r'''.. versionadded:: 2.9

        Read-only target duration of measure always equal to duration of effective time signature.
        '''
        return contexttools.get_effective_time_signature(self).duration
