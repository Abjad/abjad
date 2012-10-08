import abc
import copy
import fractions
import operator
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools import sequencetools
from abjad.tools.componenttools.Component import Component


class Leaf(Component):

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    # TODO: see if _grace and _after_grace can be removed #
    __slots__ = ('_after_grace', '_grace', '_leaf_index',
        '_duration_multiplier', '_written_duration',
        '_written_pitch_indication_is_nonsemantic',
        '_written_pitch_indication_is_at_sounding_pitch',
        'after_grace', 'grace', )

    ### INITIALIZER ###

    def __init__(self, written_duration, duration_multiplier=None):
        Component.__init__(self)
        self._duration_multiplier = duration_multiplier
        self._leaf_index = None
        self.written_duration = durationtools.Duration(
            durationtools.duration_token_to_duration_pair(written_duration))
        self.written_pitch_indication_is_nonsemantic = False
        self.written_pitch_indication_is_at_sounding_pitch = True

    ### SPECIAL METHODS ###

    def __and__(self, arg):
        return self._operate(arg, operator.__and__)

    def __copy__(self, *args):
        from abjad.tools import gracetools
        new = Component.__copy__(self, *args)
        for grace_container in gracetools.get_grace_containers_attached_to_leaf(self):
            new_grace_container = copy.deepcopy(grace_container)
            new_grace_container(new)
        return new

    __deepcopy__ = __copy__

    def __getnewargs__(self):
        result = []
        result.append(self.written_duration)
        if self.duration_multiplier is not None:
            result.append(self.duration_multiplier)
        return tuple(result)

    def __or__(self, arg):
        return self._operate(arg, operator.__or__)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self._compact_representation)

    def __str__(self):
        return self._compact_representation

    def __sub__(self, arg):
        return self._operate(arg, operator.__sub__)

    def __xor__(self, arg):
        return self._operate(arg, operator.__xor__)

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        return '({})'.format(self._formatted_duration)

    @property
    def _format_pieces(self):
        return self.lilypond_format.split('\n')

    @property
    def _formatted_duration(self):
        duration_string = durationtools.assignable_rational_to_lilypond_duration_string(self.written_duration)
        if self.duration_multiplier is not None:
            return '%s * %s' % (duration_string, self.duration_multiplier)
        else:
            return duration_string

    ### PRIVATE METHODS ###

    def _copy_override_and_set_from_leaf(self, leaf):
        if getattr(leaf, '_override', None) is not None:
            self._override = copy.copy(leaf.override)
        if getattr(leaf, '_set', None) is not None:
            self._set = copy.copy(leaf.set)

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
        if any(['\n' in x.lilypond_format for x in note_heads]):
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

    def _format_after_slot(leaf, format_contributions):
        result = []
        result.append(('spanners', format_contributions.get('after', {}).get('spanners', [])))
        result.append(('context marks', format_contributions.get('after', {}).get('context marks', [])))
        result.append(('lilypond command marks', format_contributions.get('after', {}).get('lilypond command marks', [])))
        result.append(('comments', format_contributions.get('after', {}).get('comments', [])))
        #result.append(formattools.get_spanner_format_contributions_for_slot(leaf, 'after'))
        #result.append(formattools.get_context_mark_format_contributions_for_slot(leaf, 'after'))
        #result.append(formattools.get_lilypond_command_mark_format_contributions_for_slot(leaf, 'after'))
        #result.append(formattools.get_comment_format_contributions_for_slot(leaf, 'after'))
        return result

    def _format_before_slot(leaf, format_contributions):
        result = []
        result.append(leaf._format_grace_body())
        result.append(('comments', format_contributions.get('before', {}).get('comments', [])))
        result.append(('lilypond command marks', format_contributions.get('before', {}).get('lilypond command marks', [])))
        result.append(('context marks', format_contributions.get('before', {}).get('context marks', [])))
        result.append(('grob overrides', format_contributions.get('grob overrides', [])))
        result.append(('context settings', format_contributions.get('context settings', [])))
        result.append(('spanners', format_contributions.get('before', {}).get('spanners', [])))
        #result.append(formattools.get_comment_format_contributions_for_slot(leaf, 'before'))
        #result.append(formattools.get_lilypond_command_mark_format_contributions_for_slot(leaf, 'before'))
        #result.append(formattools.get_context_mark_format_contributions_for_slot(leaf, 'before'))
        #result.append(formattools.get_grob_override_format_contributions(leaf))
        #result.append(formattools.get_context_setting_format_contributions(leaf))
        #result.append(formattools.get_spanner_format_contributions_for_slot(leaf, 'before'))
        return result

    def _format_close_brackets_slot(leaf, format_contributions):
        return []

    def _format_closing_slot(leaf, format_contributions):
        result = []
        result.append(leaf._format_agrace_body())
        result.append(('lilypond command marks', format_contributions.get('closing', {}).get('lilypond command marks', [])))
        result.append(('context marks', format_contributions.get('closing', {}).get('context marks', [])))
        result.append(('comments', format_contributions.get('closing', {}).get('comments', [])))
        #result.append(formattools.get_lilypond_command_mark_format_contributions_for_slot(leaf, 'closing'))
        #result.append(formattools.get_context_mark_format_contributions_for_slot(leaf, 'closing'))
        #result.append(formattools.get_comment_format_contributions_for_slot(leaf, 'closing'))
        return result

    def _format_contents_slot(leaf, format_contributions):
        result = []
        result.append(leaf._format_leaf_body(format_contributions))
        return result

    def _format_open_brackets_slot(leaf, format_contributions):
        return []

    def _format_opening_slot(leaf, format_contributions):
        result = []
        result.append(('comments', format_contributions.get('opening', {}).get('comments', [])))
        result.append(('context marks', format_contributions.get('opening', {}).get('context marks', [])))
        result.append(('lilypond command marks', format_contributions.get('opening', {}).get('lilypond command marks', [])))
        #result.append(formattools.get_comment_format_contributions_for_slot(leaf, 'opening'))
        #result.append(formattools.get_lilypond_command_mark_format_contributions_for_slot(leaf, 'opening'))
        #result.append(formattools.get_context_mark_format_contributions_for_slot(leaf, 'opening'))
        result.append(leaf._format_agrace_opening())
        return result

    def _operate(self, arg, operator):
        assert isinstance(arg, Leaf)
        from abjad.tools import leaftools
        from abjad.tools import pitchtools
        self_pairs = set(pitchtools.list_named_chromatic_pitches_in_expr(self))
        arg_pairs = set(pitchtools.list_named_chromatic_pitches_in_expr(arg))
        pairs = operator(self_pairs, arg_pairs)
        if len(pairs) == 0:
            pairs = [None]
        elif len(pairs) == 1:
            pairs = list(pairs)
        else:
            pairs = [tuple(pairs)]
        leaves = leaftools.make_leaves(pairs, self.written_duration)
        leaf = leaves[0]
        return leaf

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
        report += self._process_contribution_packet(self._format_before_slot(format_contributions))
        report += 'slot 3:\n'
        report += self._process_contribution_packet(self._format_opening_slot(format_contributions))
        report += 'slot 4:\n'
        report += '\tleaf body:\n'
        report += '\t\t' + self._format_contents_slot(format_contributions)[0][1][0] + '\n'
        report += 'slot 5:\n'
        report += self._process_contribution_packet(self._format_closing_slot(format_contributions))
        report += 'slot 7:\n'
        report += self._process_contribution_packet(self._format_after_slot(format_contributions))
        return report

    ### PUBLIC PROPERTIES ###

    @property
    def duration_in_seconds(self):
        from abjad.tools import contexttools
        tempo = contexttools.get_effective_tempo(self)
        if tempo is not None and not tempo.is_imprecise:
            return self.prolated_duration / tempo.duration / tempo.units_per_minute * 60
        raise MissingTempoError

    @apply
    def duration_multiplier():
        def fget(self):
            return self._duration_multiplier
        def fset(self, expr):
            if expr is None:
                self._duration_multiplier = None
            else:
                duration_multiplier = fractions.Fraction(expr)
                assert 0 <= duration_multiplier
                self._duration_multiplier = duration_multiplier
        return property(**locals())

    @property
    def leaf_index(self):
        self._update_prolated_offset_values_of_entire_score_tree_if_necessary()
        return self._leaf_index

    @property
    def multiplied_duration(self):
        if self.written_duration:
            if self.duration_multiplier is not None:
                return self.written_duration * self.duration_multiplier
            else:
                return durationtools.Duration(self.written_duration)
        else:
            return None

    @property
    def preprolated_duration(self):
        return self.multiplied_duration

    @apply
    def written_duration():
        def fget(self):
            return self._written_duration
        def fset(self, expr):
            rational = durationtools.Duration(expr)
            if not durationtools.is_assignable_rational(rational):
                raise AssignabilityError('not assignable duration: "%s".' % str(rational))
            self._written_duration = rational
        return property(**locals())

    @apply
    def written_pitch_indication_is_at_sounding_pitch():
        def fset(self, arg):
            '''Read / write flag to be set to false when pitch indication is transposed.
            '''
            if not isinstance(arg, bool):
                raise TypeError
            self._written_pitch_indication_is_at_sounding_pitch = arg
        def fget(self):
            return self._written_pitch_indication_is_at_sounding_pitch
        return property(**locals())

    @apply
    def written_pitch_indication_is_nonsemantic():
        def fset(self, arg):
            '''Read / write flag to be set when using leaves only graphically.

            setting this value to true sets sounding pitch indicator to false.
            '''
            if not isinstance(arg, bool):
                raise TypeError
            self._written_pitch_indication_is_nonsemantic = arg
            if arg == True:
                self.written_pitch_indication_is_at_sounding_pitch = False
        def fget(self):
            return self._written_pitch_indication_is_nonsemantic
        return property(**locals())
