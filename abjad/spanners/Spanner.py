import copy
import typing
from abjad import enums
from abjad import typings
from abjad.core.Chord import Chord
from abjad.core.Component import Component
from abjad.core.Leaf import Leaf
from abjad.core.MultimeasureRest import MultimeasureRest
from abjad.core.Note import Note
from abjad.core.Rest import Rest
from abjad.core.Skip import Skip
from abjad.core.Selection import Selection
from abjad.indicators.BeamCount import BeamCount
from abjad.indicators.Dynamic import Dynamic
from abjad.indicators.HairpinIndicator import HairpinIndicator
from abjad.indicators.StartBeam import StartBeam
from abjad.indicators.StartPhrasingSlur import StartPhrasingSlur
from abjad.indicators.StartSlur import StartSlur
from abjad.indicators.StartTextSpan import StartTextSpan
from abjad.indicators.StopBeam import StopBeam
from abjad.indicators.StopHairpin import StopHairpin
from abjad.indicators.StopSlur import StopSlur
from abjad.indicators.StopPhrasingSlur import StopPhrasingSlur
from abjad.indicators.StopTextSpan import StopTextSpan
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.system.Tag import Tag
from abjad.system.Tags import Tags
from abjad.system.Wrapper import Wrapper
from abjad.timespans import Timespan
from abjad.top.attach import attach
from abjad.top.detach import detach
from abjad.top.inspect import inspect
from abjad.top.iterate import iterate
from abjad.top.override import override
from abjad.top.select import select
from abjad.top.setting import setting
from abjad.top.tweak import tweak
from abjad.utilities.Duration import Duration
from abjad.utilities.Expression import Expression
from abjad.utilities.Sequence import Sequence
abjad_tags = Tags()


class Spanner(object):
    """
    Spanner.

    Any object that stretches horizontally and encompasses leaves.

    Usually at the context of the voice (not staff or higher).

    Examples include beams, slurs, hairpins and trills.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contiguity_constraint',
        '_deactivate',
        '_ignore_attachment_test',
        '_ignore_before_attach',
        '_leaves',
        '_lilypond_setting_name_manager',
        '_tag',
        '_tweaks',
        '_wrappers',
        )

    _empty_chord = '<>'

    ### INITIALIZER ###

    def __init__(self) -> None:
        self._contiguity_constraint: typing.Optional[str] = 'logical voice'
        self._deactivate = None
        self._ignore_attachment_test = None
        self._ignore_before_attach = None
        self._leaves: typing.List[Leaf] = []
        self._lilypond_setting_name_manager = None
        self._tag = None
        self._tweaks = None
        self._wrappers: typing.List[Wrapper] = []

    ### SPECIAL METHODS ###

    def __contains__(self, argument) -> bool:
        """
        Is true when spanner contains ``argument``.
        """
        for leaf in self.leaves:
            if leaf is argument:
                return True
        else:
            return False

    #def __copy__(self, *arguments) -> 'Spanner':
    def __copy__(self, *arguments):
        """
        Copies spanner.

        Does not copy spanner leaves.
        """
        new = type(self)(*self.__getnewargs__())
        if getattr(self, '_lilypond_setting_name_manager', None) is not None:
            new._lilypond_setting_name_manager = copy.copy(setting(self))
        if getattr(self, '_tweaks', None) is not None:
            new._tweaks = copy.copy(tweak(self))
        self._copy_keywords(new)
        return new

    def __format__(self, format_specification='') -> str:
        """
        Formats object.
        """
        return StorageFormatManager(self).get_storage_format()

    def __getitem__(self, argument) -> typing.Union[Leaf, Selection]:
        """
        Gets leaf or selection identified by ``argument``.
        """
        if isinstance(argument, slice):
            leaves = self.leaves.__getitem__(argument)
            return select(leaves)
        return self.leaves.__getitem__(argument)

    def __getnewargs__(self) -> typing.Tuple:
        """
        Gets new arguments.
        """
        return ()

    def __getstate__(self) -> dict:
        """
        Gets state of spanner.
        """
        state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, '__slots__', ()):
                state[slot] = getattr(self, slot, None)
        return state

    def __iter__(self) -> typing.Iterator:
        """
        Iterates leaves in spanner.
        """
        return iter(self.leaves)

    def __len__(self) -> int:
        """
        Gets number of leaves in spanner.
        """
        return len(self.leaves)

    def __lt__(self, argument) -> bool:
        """
        Is true when spanner is less than ``argument``.

        Trivial comparison to allow doctests to work.
        """
        assert isinstance(argument, Spanner), repr(argument)
        return repr(self) < repr(argument)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __setstate__(self, state) -> None:
        """
        Sets state of spanner.
        """
        for key, value in state.items():
            setattr(self, key, value)

    ### PRIVATE METHODS ###

    def _add_direction(self, string):
        if getattr(self, 'direction', False):
            string = f'{self.direction} {string}'
        return string

    def _append(self, leaf):
        if self._ignore_attachment_test:
            pass
        elif not self._attachment_test(leaf):
            raise Exception(f'can not attach {self!r} to {leaf!r}.')
        if self._contiguity_constraint == 'logical voice':
            leaves = self[-1:] + [leaf]
            leaves = select(leaves)
            if not leaves.are_contiguous_logical_voice():
                raise Exception(type(self), leaves)
        leaf._append_spanner(self)
        self._leaves.append(leaf)

    def _at_least_two_leaves(self, argument):
        leaves = select(argument).leaves()
        if 1 < len(leaves):
            return True
        return [
            'Requires at least two leaves.',
            f'Not just {leaves!r}.',
            ]

    def _attach(
        self,
        argument,
        deactivate=None,
        tag=None,
        ):
        assert not self, repr(self)
        assert isinstance(argument, Selection), repr(argument)
        assert argument.are_leaves(), repr(argument)
        self._extend(argument)
        self._deactivate = deactivate
        if tag is not None:
            tag = Tag(tag)
        self._tag = tag

    def _attachment_test(self, argument):
        return isinstance(argument, Leaf)

    def _attachment_test_all(self, argument):
        return True

    def _before_attach(self, argument):
        pass

    def _block_all_leaves(self):
        """
        Not composer-safe.
        """
        for leaf in self:
            self._block_leaf(leaf)

    def _block_leaf(self, leaf):
        """
        Not composer-safe.
        """
        leaf._remove_spanner(self)

    def _constrain_contiguity(self):
        """
        Not composer-safe.
        """
        self._contiguity_constraint = 'logical_voice'

    def _copy(self, leaves):
        """
        Returns copy of spanner with ``leaves``.

        ``leaves`` must already be contained in spanner.
        """
        my_leaf = self._leaves[:]
        self._leaves = []
        result = copy.copy(self)
        self._leaves = my_leaf
        for leaf in leaves:
            assert leaf in self
        for leaf in leaves:
            result._leaves.append(leaf)
        result._unblock_all_leaves()
        return result

    def _copy_keywords(self, new):
        pass

    def _detach(self):
        self._sever_all_leaves()

    def _extend(self, leaves):
        leaf_input = list(self[-1:])
        leaf_input.extend(leaves)
        leaf_input = select(leaf_input)
        if self._contiguity_constraint == 'logical voice':
            if not leaf_input.are_contiguous_logical_voice():
                message = f'{self!r} leaves must be contiguous:\n'
                message += f'  {leaf_input}'
                raise Exception(message)
        for leaf in leaves:
            self._append(leaf)

    def _fracture(self, i, direction=None):
        """
        Fractures spanner at ``direction`` of leaf at index ``i``.

        Valid values for ``direction`` are ``Left``, ``Right`` and ``None``.

        Set ``direction=None`` to fracture on both left and right sides.

        Returns tuple of original, left and right spanners.
        """
        if i < 0:
            i = len(self) + i
        if direction is enums.Left:
            return self._fracture_left(i)
        elif direction is enums.Right:
            return self._fracture_right(i)
        elif direction is None:
            left = self._copy(self[:i])
            right = self._copy(self[i + 1:])
            center = self._copy(self[i:i + 1])
            self._block_all_leaves()
            return self, left, center, right
        else:
            message = f'direction {direction!r} must be left, right or none.'
            raise ValueError(message)

    def _fracture_left(self, i):
        left = self._copy(self[:i])
        right = self._copy(self[i:])
        self._block_all_leaves()
        return self, left, right

    def _fracture_right(self, i):
        left = self._copy(self[:i + 1])
        right = self._copy(self[i + 1:])
        self._block_all_leaves()
        return self, left, right

    def _get_basic_lilypond_format_bundle(self, leaf):
        bundle = LilyPondFormatBundle()
        return bundle

    def _get_compact_summary(self):
        if not len(self):
            return ''
        elif 0 < len(self) <= 8:
            return ', '.join([str(_) for _ in self])
        else:
            left = ', '.join([str(_) for _ in self[:2]])
            right = ', '.join([str(_) for _ in self[-2:]])
            number = len(self) - 4
            middle = f', ... [{number}] ..., '
            return left + middle + right

    def _get_format_specification(self):
        agent = StorageFormatManager(self)
        names = list(agent.signature_keyword_names)
        if self._get_compact_summary() == '':
            values = []
        else:
            values = [self._get_compact_summary()]
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=values,
            storage_format_kwargs_names=names,
            )

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        return bundle

    def _get_preprolated_duration(self):
        return sum([_._get_preprolated_duration() for _ in self])

    def _get_summary(self):
        if 0 < len(self):
            return ', '.join([str(_) for _ in self])
        else:
            return ' '

    def _get_timespan(self, in_seconds=False):
        if len(self):
            timespan_ = self[0]._get_timespan(in_seconds=in_seconds)
            start_offset = timespan_.start_offset
            timespan_ = self[-1]._get_timespan(in_seconds=in_seconds)
            stop_offset = timespan_.stop_offset
        else:
            start_offset = Duration(0)
            stop_offset = Duration(0)
        return Timespan(
            start_offset=start_offset,
            stop_offset=stop_offset,
            )

    def _index(self, leaf):
        return self._leaves.index(leaf)

    def _insert(self, i, leaf):
        """
        Not composer-safe.
        """
        if not isinstance(leaf, Leaf):
            raise Exception(f'spanners attach only to leaves: {leaf!s}.')
        leaf._append_spanner(self)
        self._leaves.insert(i, leaf)

    def _is_exterior_leaf(self, leaf):
        """
        Is true if leaf is first or last in spanner.
        Is true if next leaf or previous leaf is none.
        """
        if leaf is self[0]:
            return True
        elif leaf is self[-1]:
            return True
        elif not leaf._leaf(-1) and not leaf._leaf(1):
            return True
        else:
            return False

    def _is_interior_leaf(self, leaf):
        if leaf not in self.leaves:
            return False
        if len(self.leaves) < 3:
            return False
        leaf_count = len(self.leaves)
        first_index = 0
        last_index = leaf_count - 1
        leaf_index = list(self.leaves).index(leaf)
        if first_index < leaf_index < last_index:
            return True
        return False

    def _is_my_only(self, leaf):
        return len(self) == 1 and leaf is self[0]

    def _remove(self, leaf):
        """
        Not composer-safe.
        """
        self._sever_leaf(leaf)

    def _remove_leaf(self, leaf):
        """
        Not composer-safe.
        """
        for i, leaf_ in enumerate(self.leaves):
            if leaf_ is leaf:
                self._leaves.pop(i)
                break
        else:
            raise ValueError(f'{leaf!r} not in spanner.')

    def _sever_all_leaves(self):
        """
        Not composer-safe.
        """
        for i in reversed(range(len(self))):
            leaf = self[i]
            self._sever_leaf(leaf)

    def _sever_leaf(self, leaf):
        """
        Not composer-safe.
        """
        self._block_leaf(leaf)
        self._remove_leaf(leaf)

    def _start_offset_in_me(self, leaf):
        leaf_start_offset = inspect(leaf).timespan().start_offset
        self_start_offset = inspect(self).timespan().start_offset
        return leaf_start_offset - self_start_offset

    def _stop_command_string(self):
        return self._stop_command

    def _stop_offset_in_me(self, leaf):
        leaf_start_offset = self._start_offset_in_me(leaf)
        leaf_stop_offset = leaf_start_offset + leaf._get_duration()
        return leaf_stop_offset

    @staticmethod
    def _tag_hide(strings):
        return LilyPondFormatManager.tag(
            strings,
            deactivate=False,
            tag=abjad_tags.HIDE_TO_JOIN_BROKEN_SPANNERS,
            )

    @staticmethod
    def _tag_show(strings):
        return LilyPondFormatManager.tag(
            strings,
            deactivate=True,
            tag=abjad_tags.SHOW_TO_JOIN_BROKEN_SPANNERS,
            )

    def _tweaked_start_command_strings(self):
        strings = []
        contributions = tweak(self)._list_format_contributions()
        strings.extend(contributions)
        start_command = self._start_command
        start_command = self._add_direction(start_command)
        strings.append(start_command)
        return strings

    def _unblock_all_leaves(self):
        """
        Not composer-safe.
        """
        for leaf in self:
            self._unblock_leaf(leaf)

    def _unblock_leaf(self, leaf):
        """
        Not composer-safe.
        """
        leaf._append_spanner(self)

    def _unconstrain_contiguity(self):
        """
        Not composer-safe.
        """
        self._contiguity_constraint = None

    ### PUBLIC PROPERTIES ###

    @property
    def leaves(self) -> Selection:
        """
        Gets leaves in spanner.
        """
        for leaf in self._leaves:
            if not isinstance(leaf, Leaf):
                message = f'spanners attach only to leaves (not {leaf!s}).'
                raise Exception(message)
        return select(self._leaves)

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        """
        Gets tweaks.
        """
        return self._tweaks

def beam(
    argument: typing.Union[Component, Selection],
    *,
    beam_lone_notes: bool = None,
    #beam_rests: bool = None,
    beam_rests: typing.Optional[bool] = True,
    durations: typing.Sequence[Duration] = None,
    selector: typings.Selector = 
        'abjad.select().leaves(do_not_iterate_grace_containers=True)',
    span_beam_count: int = None,
    start_beam: StartBeam = None,
    stemlet_length: typings.Number = None,
    stop_beam: StopBeam = None,
    tag: str = None,
    ) -> None:
    r"""
    Attaches beam indicators.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d' e' f'")
        >>> abjad.beam(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                [
                d'8
                e'8
                f'8
                ]
            }

    """
    # import allows eval statement
    import abjad
    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    original_leaves = iterate(argument).leaves(
        do_not_iterate_grace_containers=True
        )
    original_leaves = list(original_leaves)

    silent_prototype = (MultimeasureRest, Rest, Skip)

    def _is_beamable(argument, beam_rests=False):
        if isinstance(argument, (Chord, Note)):
            if 0 < argument.written_duration.flag_count:
                return True
        if beam_rests and isinstance(argument, silent_prototype):
            return True
        return False
    
    leaves = []
    for leaf in original_leaves:
        if not _is_beamable(leaf, beam_rests=beam_rests):
            continue
        leaves.append(leaf)
    #print(leaves, 'LLL')
    runs = []
    run = []
    run.extend(leaves[:1])
    for leaf in leaves[1:]:
        this_index = original_leaves.index(run[-1])
        that_index = original_leaves.index(leaf)
        if this_index +1 == that_index:
            run.append(leaf)
        else:
            selection = select(run)
            runs.append(selection)
            run = [leaf]
    if run:
        selection = select(run)
        runs.append(selection)
    runs = select(runs)
    #print(runs, 'RRR', len(runs))
    #print()
    if not beam_lone_notes:
        runs = runs.nontrivial()
    for run in runs:
        #print(run, 'RRR')
        if all(isinstance(_, silent_prototype) for _ in run):
            continue
        start_leaf = run[0]
        stop_leaf = run[-1]
        start_beam_ = start_beam or StartBeam()
        stop_beam_ = stop_beam or StopBeam()
        detach(StartBeam, start_leaf)
        attach(start_beam_, start_leaf, tag=tag)
        detach(StopBeam, stop_leaf)
        attach(stop_beam_, stop_leaf, tag=tag)

        #for leaf in run:
        #    print(leaf, inspect(leaf).indicators())

        if stemlet_length is None:
            continue
        staff = inspect(start_leaf).parentage().get(Staff)
        lilypond_type = getattr(staff, 'lilypond_type', 'Staff')
        string = r'\override {}.Stem.stemlet-length = {}'
        string = string.format(lilypond_type, stemlet_length)
        literal = LilyPondLiteral(string)
        for indicator in inspect(start_leaf).indicators():
            if indicator == literal:
                break
        else:
            attach(literal, start_leaf, tag=tag)
        staff = inspect(stop_leaf).parentage().get(Staff)
        lilypond_type = getattr(staff, 'lilypond_type', 'Staff')
        string = rf'\revert {lilypond_type}.Stem.stemlet-length'
        literal = LilyPondLiteral(string)
        for indicator in inspect(stop_leaf).indicators():
            if indicator == literal:
                break
        else:
            attach(literal, stop_leaf, tag=tag)

    if not durations:
        return

    if len(original_leaves) == 1:
        return

    def _leaf_neighbors(leaf, original_leaves):
        assert leaf is not original_leaves[0]
        assert leaf is not original_leaves[-1]
        this_index = original_leaves.index(leaf) 
        previous_leaf = original_leaves[this_index - 1]
        previous = 0
        if _is_beamable(previous_leaf, beam_rests=beam_rests):
            previous = previous_leaf.written_duration.flag_count
        next_leaf = original_leaves[this_index + 1]
        next_ = 0
        if _is_beamable(next_leaf, beam_rests=beam_rests):
            next_ = next_leaf.written_duration.flag_count
        return previous, next_

    span_beam_count = span_beam_count or 1
    durations = [Duration(_) for _ in durations]
    leaf_durations = [inspect(_).duration() for _ in original_leaves]
    leaf_durations = Sequence(leaf_durations)
    parts = leaf_durations.partition_by_weights(
        durations,
        overhang=True,
        )
    part_counts = [len(_) for _ in parts]
    original_leaves = Sequence(original_leaves)
    parts = original_leaves.partition_by_counts(
        part_counts,
        )
    total_parts = len(parts)
    for i, part in enumerate(parts):
        is_first_part = False
        if i == 0:
            is_first_part = True
        is_last_part = False
        if i == total_parts - 1:
            is_last_part = True
        first_leaf = part[0]
        flag_count = first_leaf.written_duration.flag_count
        if len(part) == 1:
            if not _is_beamable(first_leaf, beam_rests=False):
                continue
            left = flag_count
            right = flag_count
            beam_count = BeamCount(left, right)
            attach(beam_count, first_leaf, tag=tag)
            continue
        if _is_beamable(first_leaf, beam_rests=False):
            if is_first_part:
                left = 0
            else:
                left = span_beam_count
            beam_count = BeamCount(left, flag_count)
            attach(beam_count, first_leaf, tag=tag)
        last_leaf = part[-1]
        if _is_beamable(last_leaf, beam_rests=False):
            flag_count = last_leaf.written_duration.flag_count
            if is_last_part:
                left = flag_count
                right = 0
            else:
                previous, next_ = _leaf_neighbors(last_leaf, original_leaves)
                if previous == next_ == 0:
                    left = right = flag_count
                elif previous == 0:
                    left = 0
                    right = flag_count
                elif next_ == 0:
                    left = flag_count
                    right = 0
                elif previous == flag_count:
                    left = flag_count
                    right = min(span_beam_count, next_)
                elif flag_count == next_:
                    left = min(previous, flag_count)
                    right = flag_count
                else:
                    left = flag_count
                    right = min(previous, flag_count)
            beam_count = BeamCount(left, right)
            attach(beam_count, last_leaf, tag=tag)

        # TODO: eventually remove middle leaf beam counts?
        for middle_leaf in part[1:-1]:
            if not _is_beamable(middle_leaf, beam_rests=beam_rests):
                continue
            if isinstance(middle_leaf, silent_prototype):
                continue
            flag_count = middle_leaf.written_duration.flag_count
            previous, next_ = _leaf_neighbors(middle_leaf, original_leaves)
            if previous == next_ == 0:
                left = right = flag_count
            elif previous == 0:
                left = 0
                right = flag_count
            elif next_ == 0:
                left = flag_count
                right = 0
            elif previous == flag_count:
                left = flag_count
                right = min(flag_count, next_)
            elif flag_count == next_:
                left = min(previous, flag_count)
                right = flag_count
            else:
                left = min(previous, flag_count)
                right = flag_count
            beam_count = BeamCount(left, right)
            attach(beam_count, middle_leaf, tag=tag)

def hairpin(
    descriptor: str,
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.Selector = 'abjad.select().leaves()',
    ) -> None:
    r"""
    Attaches hairpin indicators.

    ..  container:: example

        With three-part string descriptor:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.hairpin('p < f', staff[:])
        >>> abjad.override(staff[0]).dynamic_line_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \once \override DynamicLineSpanner.staff-padding = #4
                c'4
                \p
                \<
                d'4
                e'4
                f'4
                \f
            }

    ..  container:: example

        With two-part string descriptor:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.hairpin('< !', staff[:])
        >>> abjad.override(staff[0]).dynamic_line_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \once \override DynamicLineSpanner.staff-padding = #4
                c'4
                \<
                d'4
                e'4
                f'4
                \!
            }

    ..  container:: example

        With dynamic objects:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start = abjad.Dynamic('niente', command=r'\!')
        >>> hairpin = abjad.HairpinIndicator('o<|')
        >>> abjad.tweak(hairpin).color = 'blue'
        >>> stop = abjad.Dynamic('"f"')
        >>> abjad.hairpin([start, hairpin, stop], staff[:])
        >>> abjad.override(staff[0]).dynamic_line_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \once \override DynamicLineSpanner.staff-padding = #4
                c'4
                \!
                - \tweak color #blue
                - \tweak circled-tip ##t
                - \tweak stencil #abjad-flared-hairpin
                \<
                d'4
                e'4
                f'4
                _ #(make-dynamic-script
                    (markup
                        #:whiteout
                        #:line (
                            #:general-align Y -2 #:normal-text #:larger "“"
                            #:hspace -0.4
                            #:dynamic "f"
                            #:hspace -0.2
                            #:general-align Y -2 #:normal-text #:larger "”"
                            )
                        )
                    )
            }

    """
    import abjad

    indicators: typing.List = []
    start_dynamic: typing.Optional[Dynamic]
    hairpin: typing.Optional[HairpinIndicator]
    stop_dynamic: typing.Optional[Dynamic]
    known_shapes = HairpinIndicator('<').known_shapes
    if isinstance(descriptor, str):
        for string in descriptor.split():
            if string in known_shapes:
                hairpin = HairpinIndicator(string)
                indicators.append(hairpin)
            elif string == '!':
                stop_hairpin = StopHairpin()
                indicators.append(stop_hairpin)
            else:
                dynamic = Dynamic(string)
                indicators.append(dynamic)
    else:
        assert isinstance(descriptor, list), repr(descriptor)
        indicators = descriptor

    start_dynamic, hairpin, stop_dynamic = None, None, None
    if len(indicators) == 1:
        if isinstance(indicators[0], Dynamic):
            start_dynamic = indicators[0]
        else:
            hairpin = indicators[0]
    elif len(indicators) == 2:
        if isinstance(indicators[0], Dynamic):
            start_dynamic = indicators[0]
            hairpin = indicators[1]
        else:
            hairpin = indicators[0]
            stop_dynamic = indicators[1]
    elif len(indicators) == 3:
        start_dynamic, hairpin, stop_dynamic = indicators
    else:
        raise Exception(indicators)

    if start_dynamic is not None:
        assert isinstance(start_dynamic, Dynamic), repr(start_dynamic)

    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]

    if start_dynamic is not None:
        attach(start_dynamic, start_leaf)
    if hairpin is not None:
        attach(hairpin, start_leaf)
    if stop_dynamic is not None:
        attach(stop_dynamic, stop_leaf)

def phrasing_slur(
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.Selector = 'abjad.select().leaves()',
    start_phrasing_slur: StartPhrasingSlur = None,
    stop_phrasing_slur: StopPhrasingSlur = None,
    ) -> None:
    r"""
    Attaches phrasing slur indicators.

    ..  container:: example

        Single spanner:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.phrasing_slur(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                \(
                d'4
                e'4
                f'4
                \)
            }


    """
    # import allows eval statement
    import abjad
    start_phrasing_slur = StartPhrasingSlur()
    stop_phrasing_slur = StopPhrasingSlur()

    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]

    start_phrasing_slur = start_phrasing_slur or StartPhrasingSlur()
    stop_phrasing_slur = stop_phrasing_slur or StopPhrasingSlur()
    
    attach(start_phrasing_slur, start_leaf)
    attach(stop_phrasing_slur, stop_leaf)

def slur(
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.Selector = 'abjad.select().leaves()',
    start_slur: StartSlur = None,
    stop_slur: StopSlur = None,
    ) -> None:
    r"""
    Attaches slur indicators.

    ..  container:: example

        Single spanner:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.slur(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                (
                d'4
                e'4
                f'4
                )
            }


    """
    # import allows eval statement
    import abjad
    start_slur = start_slur or StartSlur()
    stop_slur = stop_slur or StopSlur()

    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]

    attach(start_slur, start_leaf)
    attach(stop_slur, stop_leaf)

def text_spanner(
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.Selector = 'abjad.select().leaves()',
    start_text_span: StartTextSpan = None,
    stop_text_span: StopTextSpan = None,
    ) -> None:
    r"""
    Attaches text span indicators.

    ..  container:: example

        Single spanner:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('pont.').upright(),
        ...     right_text=abjad.Markup('tasto').upright(),
        ...     style='solid-line-with-arrow',
        ...     )
        >>> abjad.text_spanner(staff[:], start_text_span=start_text_span)
        >>> abjad.override(staff[0]).text_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \once \override TextSpanner.staff-padding = #4
                c'4
                - \abjad-solid-line-with-arrow
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.5
                        }
                    }
                - \tweak bound-details.right.text \markup {
                    \upright
                        tasto
                    }
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    ..  container:: example

        Enchained spanners:

        >>> staff = abjad.Staff("c'4 d' e' f' r")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('pont.').upright(),
        ...     style='dashed-line-with-arrow',
        ...     )
        >>> abjad.text_spanner(staff[:3], start_text_span=start_text_span)
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('tasto').upright(),
        ...     right_text=abjad.Markup('pont.').upright(),
        ...     style='dashed-line-with-arrow',
        ...     )
        >>> abjad.text_spanner(staff[-3:], start_text_span=start_text_span)
        >>> abjad.override(staff).text_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextSpanner.staff-padding = #4
            }
            {
                c'4
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.5
                        }
                    }
                \startTextSpan
                d'4
                e'4
                \stopTextSpan
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                tasto
                            \hspace
                                #0.5
                        }
                    }
                - \tweak bound-details.right.text \markup {
                    \upright
                        pont.
                    }
                \startTextSpan
                f'4
                r4
                \stopTextSpan
            }

        >>> staff = abjad.Staff("c'4 d' e' f' r")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('pont.').upright(),
        ...     style='dashed-line-with-arrow',
        ...     )
        >>> abjad.text_spanner(staff[:3], start_text_span=start_text_span)
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('tasto').upright(),
        ...     style='solid-line-with-hook',
        ...     )
        >>> abjad.text_spanner(staff[-3:], start_text_span=start_text_span)
        >>> abjad.override(staff).text_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextSpanner.staff-padding = #4
            }
            {
                c'4
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.5
                        }
                    }
                \startTextSpan
                d'4
                e'4
                \stopTextSpan
                - \abjad-solid-line-with-hook
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                tasto
                            \hspace
                                #0.5
                        }
                    }
                \startTextSpan
                f'4
                r4
                \stopTextSpan
            }

    """
    import abjad
    start_text_span = start_text_span or StartTextSpan()
    stop_text_span = stop_text_span or StopTextSpan()

    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    
    attach(start_text_span, start_leaf)
    attach(stop_text_span, stop_leaf)
