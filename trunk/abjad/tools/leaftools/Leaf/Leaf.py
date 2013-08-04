# -*- encoding: utf-8 -*-
import abc
import copy
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.componenttools.Component import Component


class Leaf(Component):

    ### CLASS VARIABLES ##

    __metaclass__ = abc.ABCMeta

    # TODO: see if _grace and _after_grace can be removed #
    __slots__ = (
        '_after_grace', 
        '_grace', 
        '_leaf_index',
        '_lilypond_duration_multiplier', 
        '_written_duration',
        '_written_pitch_indication_is_nonsemantic',
        '_written_pitch_indication_is_at_sounding_pitch',
        'after_grace', 
        'grace',
        )

    ### INITIALIZER ###

    def __init__(self, written_duration, lilypond_duration_multiplier=None):
        Component.__init__(self)
        self._lilypond_duration_multiplier = lilypond_duration_multiplier
        self._leaf_index = None
        self.written_duration = durationtools.Duration(written_duration)
        self.written_pitch_indication_is_nonsemantic = False
        self.written_pitch_indication_is_at_sounding_pitch = True

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        '''Get new arguments.

        Return tuple.
        '''
        result = []
        result.append(self.written_duration)
        if self.lilypond_duration_multiplier is not None:
            result.append(self.lilypond_duration_multiplier)
        return tuple(result)

    def __repr__(self):
        '''Interpreter representation of leaf.

        Return string.
        '''
        return '{}({!r})'.format(
            self._class_name, self._compact_representation)

    def __str__(self):
        '''String representation of leaf.

        Return string.
        '''
        return self._compact_representation

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        return '({})'.format(self._formatted_duration)

    @property
    def _duration_in_seconds(self):
        from abjad.tools import contexttools
        tempo = self.get_effective_context_mark(contexttools.TempoMark)
        if tempo is not None and not tempo.is_imprecise:
            result = self.get_duration() / tempo.duration / tempo.units_per_minute * 60
            return durationtools.Duration(result)
        raise MissingTempoError

    @property
    def _format_pieces(self):
        return self.lilypond_format.split('\n')

    @property
    def _formatted_duration(self):
        duration_string = self.written_duration.lilypond_duration_string
        if self.lilypond_duration_multiplier is not None:
            return '{} * {}'.format(
                duration_string, self.lilypond_duration_multiplier)
        else:
            return duration_string

    @property
    def _multiplied_duration(self):
        if self.written_duration:
            if self.lilypond_duration_multiplier is not None:
                multiplied_duration = self.written_duration
                multiplied_duration *= self.lilypond_duration_multiplier
                return multiplied_duration
            else:
                return durationtools.Duration(self.written_duration)
        else:
            return None

    @property
    def _preprolated_duration(self):
        return self._multiplied_duration

    ### PRIVATE METHODS ###

    def _copy_override_and_set_from_leaf(self, leaf):
        if getattr(leaf, '_override', None) is not None:
            self._override = copy.copy(leaf.override)
        if getattr(leaf, '_set', None) is not None:
            self._set = copy.copy(leaf.set)

    def _copy_with_marks_but_without_children_or_spanners(self):
        new = Component._copy_with_marks_but_without_children_or_spanners(self)
        for grace_container in self.get_grace_containers():
            new_grace_container = \
                grace_container._copy_with_children_and_marks_but_without_spanners()
            new_grace_container(new)
        return new

    def _format_after_slot(leaf, format_contributions):
        result = []
        result.append(('spanners', 
            format_contributions.get('after', {}).get('spanners', [])))
        result.append(('context marks', 
            format_contributions.get('after', {}).get('context marks', [])))
        result.append(('lilypond command marks',
            format_contributions.get(
                'after', {}).get('lilypond command marks', [])))
        result.append(('comments', 
            format_contributions.get('after', {}).get('comments', [])))
        return result

    def _format_agrace_body(leaf):
        result = []
        if hasattr(leaf, '_after_grace'):
            after_grace = leaf.after_grace
            if len(after_grace):
                result.append(after_grace.lilypond_format)
        return ['agrace body', result]

    def _format_agrace_opening(leaf):
        result = []
        if hasattr(leaf, '_after_grace'):
            if len(leaf.after_grace):
                result.append(r'\afterGrace')
        return ['agrace opening', result]

    def _format_before_slot(leaf, format_contributions):
        result = []
        result.append(leaf._format_grace_body())
        result.append(('comments', 
            format_contributions.get('before', {}).get('comments', [])))
        result.append(('lilypond command marks',
            format_contributions.get(
                'before', {}).get('lilypond command marks', [])))
        result.append(('context marks', 
            format_contributions.get('before', {}).get('context marks', [])))
        result.append(('grob overrides', 
            format_contributions.get('grob overrides', [])))
        result.append(('context settings', 
            format_contributions.get('context settings', [])))
        result.append(('spanners', 
            format_contributions.get('before', {}).get('spanners', [])))
        return result

    def _format_close_brackets_slot(leaf, format_contributions):
        return []

    def _format_closing_slot(leaf, format_contributions):
        result = []
        result.append(leaf._format_agrace_body())
        result.append(('spanners', 
            format_contributions.get('closing', {}).get('spanners', [])))
        result.append(('lilypond command marks',
            format_contributions.get(
                'closing', {}).get('lilypond command marks', [])))
        result.append(('context marks', 
            format_contributions.get('closing', {}).get('context marks', [])))
        result.append(('comments', 
            format_contributions.get('closing', {}).get('comments', [])))
        return result

    def _format_contents_slot(leaf, format_contributions):
        result = []
        result.append(leaf._format_leaf_body(format_contributions))
        return result


    def _format_grace_body(leaf):
        result = []
        if hasattr(leaf, '_grace'):
            grace = leaf.grace
            if len(grace):
                result.append(grace.lilypond_format)
        return ['grace body', result]

    def _format_leaf_body(leaf, format_contributions):
        result = leaf._format_leaf_nucleus()[1]
        right = format_contributions.get('right', {})
        if right:
            result.extend(right.get('stem tremolos', []))
            result.extend(right.get('articulations', []))
            result.extend(right.get('lilypond command marks', []))
            result.extend(right.get('context marks', []))
            result.extend(right.get('spanners', []))
            result.extend(right.get('comments', []))
        result = [' '.join(result)]
        markup = right.get('markup')
        if markup:
            if len(markup) == 1:
                result[0] += ' {}'.format(markup[0])
            else:
                result.extend('\t{}'.format(x) for x in markup)
        return ['leaf body', result]

    # TODO: subclass this properly for chord
    def _format_leaf_nucleus(leaf):
        from abjad.tools.chordtools.Chord import Chord
        if not isinstance(leaf, Chord):
            return ['nucleus', leaf._body]
        result =  []
        chord = leaf
        note_heads = chord.note_heads
        if any('\n' in x.lilypond_format for x in note_heads):
            for note_head in note_heads:
                format = note_head.lilypond_format
                format_list = format.split('\n')
                format_list = ['\t' + x for x in format_list]
                result.extend(format_list)
            result.insert(0, '<')
            result.append('>')
            result = '\n'.join(result)
            result += str(chord._formatted_duration)
        else:
            result.extend([x.lilypond_format for x in note_heads])
            result = '<%s>%s' % (' '.join(result), chord._formatted_duration)
        # single string, but wrapped in list bc contribution
        return ['nucleus', [result]]

    def _format_open_brackets_slot(leaf, format_contributions):
        return []

    def _format_opening_slot(leaf, format_contributions):
        result = []
        result.append(('comments', 
            format_contributions.get('opening', {}).get('comments', [])))
        result.append(('context marks', 
            format_contributions.get('opening', {}).get('context marks', [])))
        result.append(('lilypond command marks',
            format_contributions.get(
                'opening', {}).get('lilypond command marks', [])))
        result.append(('spanners', 
            format_contributions.get('opening', {}).get('spanners', [])))
        result.append(leaf._format_agrace_opening())
        return result

    def _process_contribution_packet(self, contribution_packet):
        result = ''
        for contributor, contributions in contribution_packet:
            if contributions:
                if isinstance(contributor, tuple):
                    contributor = '\t' + contributor[0] + ':\n'
                else:
                    contributor = '\t' + contributor + ':\n'
                result += contributor
                for contribution in contributions:
                    contribution = '\t\t' + contribution + '\n'
                    result += contribution
        return result

    def _report_format_contributors(self):
        format_contributions = formattools.get_all_format_contributions(self)
        report = ''
        report += 'slot 1:\n'
        report += self._process_contribution_packet(
            self._format_before_slot(format_contributions))
        report += 'slot 3:\n'
        report += self._process_contribution_packet(
            self._format_opening_slot(format_contributions))
        report += 'slot 4:\n'
        report += '\tleaf body:\n'
        report += '\t\t' + self._format_contents_slot(
            format_contributions)[0][1][0] + '\n'
        report += 'slot 5:\n'
        report += self._process_contribution_packet(
            self._format_closing_slot(format_contributions))
        report += 'slot 7:\n'
        report += self._process_contribution_packet(
            self._format_after_slot(format_contributions))
        return report

    def _to_tuplet_with_ratio(self, proportions, is_diminution=True):
        from abjad.tools import componenttools
        from abjad.tools import leaftools
        from abjad.tools import notetools
        from abjad.tools import selectiontools
        from abjad.tools import tuplettools
        # check input
        proportions = mathtools.Ratio(proportions)
        # find target duration of fixed-duration tuplet
        target_duration = self.written_duration
        # find basic prolated duration of note in tuplet
        basic_prolated_duration = target_duration / sum(proportions)
        # find basic written duration of note in tuplet
        basic_written_duration = \
            basic_prolated_duration.equal_or_greater_assignable
        # find written duration of each note in tuplet
        written_durations = [x * basic_written_duration for x in proportions]
        # make tuplet notes
        try:
            notes = [notetools.Note(0, x) for x in written_durations]
        except AssignabilityError:
            denominator = target_duration._denominator
            note_durations = [durationtools.Duration(x, denominator) 
                for x in proportions]
            notes = notetools.make_notes(0, note_durations)
        # make tuplet
        tuplet = tuplettools.FixedDurationTuplet(target_duration, notes)
        # fix tuplet contents if necessary
        tuplet._fix()
        # change prolation if necessary
        if not tuplet.multiplier == 1:
            if is_diminution:
                if not tuplet.is_diminution:
                    tuplet._diminished_to_augmented()
            else:
                if tuplet.is_diminution:
                    tuplet._diminished_to_augmented()
        # give leaf position in score structure to tuplet
        componenttools.move_parentage_and_spanners_from_components_to_components(
            [self], [tuplet])
        # return tuplet
        return tuplet

    ### PUBLIC PROPERTIES ###

    @apply
    def lilypond_duration_multiplier():
        def fget(self):
            '''LilyPond duration multiplier.

            Return multiplier or none.
            '''
            return self._lilypond_duration_multiplier
        def fset(self, expr):
            if expr is None:
                self._lilypond_duration_multiplier = None
            else:
                lilypond_duration_multiplier = durationtools.Multiplier(expr)
                assert 0 <= lilypond_duration_multiplier
                self._lilypond_duration_multiplier = lilypond_duration_multiplier
        return property(**locals())

    @property
    def leaf_index(self):
        '''Leaf index.

        Return nonnegative integer.
        '''
        self._update_prolated_offset_values_of_entire_score_tree_if_necessary()
        return self._leaf_index

    @apply
    def written_duration():
        def fget(self):
            '''Written duration of leaf.

            Return duration.
            '''
            return self._written_duration
        def fset(self, expr):
            rational = durationtools.Duration(expr)
            if not rational.is_assignable:
                message = 'not assignable duration: "%s".'
                raise AssignabilityError(message % str(rational))
            self._written_duration = rational
        return property(**locals())

    @apply
    def written_pitch_indication_is_at_sounding_pitch():
        def fget(self):
            r'''True when written pitch is at sounding pitch.
            False when written pitch is transposed.

            Return boolean.
            '''
            return self._written_pitch_indication_is_at_sounding_pitch
        def fset(self, arg):
            if not isinstance(arg, bool):
                raise TypeError
            self._written_pitch_indication_is_at_sounding_pitch = arg
        return property(**locals())

    @apply
    def written_pitch_indication_is_nonsemantic():
        def fget(self):
            r'''True when pitch is nonsemantic.

            Set to true when using leaves only graphically.

            Setting this value to true sets sounding pitch indicator to false.

            Return boolean.
            '''
            return self._written_pitch_indication_is_nonsemantic
        def fset(self, arg):
            if not isinstance(arg, bool):
                raise TypeError
            self._written_pitch_indication_is_nonsemantic = arg
            if arg == True:
                self.written_pitch_indication_is_at_sounding_pitch = False
        return property(**locals())

    ### PUBLIC METHODS ###

    def detach_grace_containers(self, kind=None):
        r'''Detach grace containers attached to leaf.

        Return tuple of detached grace containers.
        '''
        grace_containers = self.get_grace_containers(kind=kind)
        for grace_container in grace_containers:
            grace_container.detach()
        return grace_containers

    def get_grace_containers(self, kind=None):
        r'''Get grace containers attached to leaf.

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> grace_container = leaftools.GraceContainer(
            ...     [Note("cs'16")], 
            ...     kind='grace',
            ...     )
            >>> grace_container.attach(staff[1])
            Note("d'8")
            >>> after_grace = leaftools.GraceContainer(
            ...     [Note("ds'16")], 
            ...     kind='after'
            ...     )
            >>> after_grace.attach(staff[1])
            Note("d'8")

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'8
                \grace {
                    cs'16
                }
                \afterGrace
                d'8
                {
                    ds'16
                }
                e'8
                f'8
            }

        ::

            >>> show(staff) # doctest: +SKIP

        Example 1. Get all grace containers attached to leaf:

        ::

            >>> staff[1].get_grace_containers()
            (GraceContainer(cs'16), GraceContainer(ds'16))

        Example 2. Get only (proper) grace containers attached to leaf:

        ::

            >>> staff[1].get_grace_containers(kind='grace')
            (GraceContainer(cs'16),)

        Example 3. Get only after grace containers attached to leaf:

        ::

            >>> staff[1].get_grace_containers(kind='after')
            (GraceContainer(ds'16),)

        Return tuple.
        '''
        result = []
        if kind in (None, 'grace') and hasattr(self, '_grace'):
            result.append(self._grace)
        if kind in (None, 'after') and hasattr(self, '_after_grace'):
            result.append(self._after_grace)
        return tuple(result)

    def select_tie_chain(self):
        r'''Select tie chain.
        '''
        from abjad.tools import leaftools
        from abjad.tools import spannertools
        spanner_classes = (spannertools.TieSpanner,)
        for component in self.select_parentage():
            tie_spanners = component._get_spanners(spanner_classes)
            if len(tie_spanners) == 1:
                tie_spanner = tie_spanners.pop()
                return leaftools.TieChain(music=tie_spanner.leaves)
            elif 1 < len(tie_spanners):
                raise ExtraSpannerError
        else:
            return leaftools.TieChain(music=self)

    def shorten(self, duration):
        r'''Shorten leaf by `duration`.
        '''
        from abjad.tools import leaftools
        duration = self.get_duration() - duration
        prolation = self.select_parentage().prolation
        preprolated_duration = duration / prolation
        leaftools.set_preprolated_leaf_duration(self, preprolated_duration)
