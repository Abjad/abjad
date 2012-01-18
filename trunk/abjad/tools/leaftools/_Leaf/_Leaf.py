from abjad.tools import durationtools
from abjad.tools.componenttools._Component import _Component
from abjad.core._StrictComparator import _StrictComparator
import copy
import fractions
import operator


class _Leaf(_Component, _StrictComparator):

    # TODO: see if _grace and _after_grace can be removed #
    __slots__ = ('_after_grace', '_grace', '_leaf_index',
        '_duration_multiplier', '_written_duration',
        '_written_pitch_indication_is_nonsemantic',
        '_written_pitch_indication_is_at_sounding_pitch',
        'after_grace', 'grace', )

    def __init__(self, written_duration, duration_multiplier = None):
        _Component.__init__(self)
        self._duration_multiplier = duration_multiplier
        self._leaf_index = None
        self.written_duration = durationtools.Duration(durationtools.duration_token_to_duration_pair(written_duration))
        self.written_pitch_indication_is_nonsemantic = False
        self.written_pitch_indication_is_at_sounding_pitch = True

    ### OVERLOADS ###

    def __and__(self, arg):
        return self._operate(arg, operator.__and__)

    def __copy__(self, *args):
        from abjad.tools import gracetools
        new = _Component.__copy__(self, *args)
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

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_pieces(self):
        return self.format.split('\n')

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

    def _operate(self, arg, operator):
        assert isinstance(arg, _Leaf)
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

    ### PUBLIC ATTRIBUTES ###

    @property
    def duration_in_seconds(self):
        from abjad.exceptions import MissingTempoError
        from abjad.tools import contexttools
        tempo = contexttools.get_effective_tempo(self)
        if tempo is not None:
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
    def format(self):
        from abjad.tools.leaftools._format_leaf import _format_leaf
        return _format_leaf(self)

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
