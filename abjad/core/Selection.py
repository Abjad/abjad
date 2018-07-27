import collections
import copy
import inspect
import itertools
import typing
from abjad import enums
from abjad import exceptions
from abjad import mathtools
from abjad.mathtools.Ratio import Ratio
from abjad.pitch.PitchSet import PitchSet
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.top.attach import attach
from abjad.top.inspect import inspect as abjad_inspect
from abjad.top.iterate import iterate
from abjad.top.mutate import mutate
from abjad.top.new import new
from abjad.utilities.CyclicTuple import CyclicTuple
from abjad.utilities.Duration import Duration
from abjad.utilities.DurationInequality import DurationInequality
from abjad.utilities.LengthInequality import LengthInequality
from abjad.utilities.OrderedDict import OrderedDict
from abjad.utilities.Pattern import Pattern
from abjad.utilities.PitchInequality import PitchInequality
from abjad.utilities.Sequence import Sequence
from abjad.utilities.Expression import Expression
from .Chord import Chord
from .Component import Component
from .Leaf import Leaf
from .MultimeasureRest import MultimeasureRest
from .Note import Note
from .Rest import Rest
from .Skip import Skip


class Selection(AbjadValueObject, collections.Sequence):
    r"""
    Selection of items (components / or other selections).

    ..  container:: example

        Selects runs:

        ..  container:: example

            >>> string = r"c'4 \times 2/3 { d'8 r8 e'8 } r16 f'16 g'8 a'4"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            >>> result = abjad.select(staff).runs()

            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'4"), Note("d'8")])
            Selection([Note("e'8")])
            Selection([Note("f'16"), Note("g'8"), Note("a'4")])

        ..  container:: example expression

            >>> selector = abjad.select().runs()
            >>> result = selector(staff)

            >>> selector.print(result)
            Selection([Note("c'4"), Note("d'8")])
            Selection([Note("e'8")])
            Selection([Note("f'16"), Note("g'8"), Note("a'4")])

            >>> selector.color(result)
            >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad_color_music "red"
                c'4
                \times 2/3 {
                    \abjad_color_music "red"
                    d'8
                    r8
                    \abjad_color_music "blue"
                    e'8
                }
                r16
                \abjad_color_music "red"
                f'16
                \abjad_color_music "red"
                g'8
                \abjad_color_music "red"
                a'4
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Selections'

    __slots__ = (
        '_expression',
        '_items',
        )

    ### INITIALIZER ###

    def __init__(self, items=None):
        if items is None:
            items = []
        if isinstance(items, Component):
            items = [items]
        items = tuple(items)
        self._check(items)
        self._items = tuple(items)
        self._expression = None

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Cocatenates ``argument`` to selection.

        Returns new selection.
        """
        assert isinstance(argument, collections.Iterable)
        items = self.items + tuple(argument)
        return type(self)(items=items)

    def __contains__(self, argument):
        """
        Is true when ``argument`` is in selection.

        Returns true or false.
        """
        return argument in self.items

    def __eq__(self, argument):
        """
        Is true when selection and ``argument`` are of the same type
        and when items in selection equal item in ``argument``.

        Returns true or false.
        """
        if isinstance(argument, type(self)):
            return self.items == argument.items
        elif isinstance(argument, collections.Sequence):
            return self.items == tuple(argument)
        return False

    def __format__(self, format_specification=''):
        """
        Formats duration.

        Returns string.
        """
        if format_specification in ('', 'storage'):
            return StorageFormatManager(self).get_storage_format()
        raise ValueError(repr(format_specification))

    def __getitem__(self, argument):
        r"""
        Gets item, slice or pattern ``argument`` in selection.

        ..  container:: example

            Gets every other leaf:

            ..  container:: example

                >>> string = r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8"
                >>> staff = abjad.Staff(string)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> pattern = abjad.index([0], 2)
                >>> for leaf in abjad.select(staff).leaves()[pattern]:
                ...     leaf
                ...
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Rest('r8')

            ..  container:: example expression

                >>> selector = abjad.select().leaves()[pattern]
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Rest('r8')

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    d'8
                    ~
                    \abjad_color_music "blue"
                    d'8
                    e'8
                    ~
                    \abjad_color_music "red"
                    e'8
                    ~
                    e'8
                    \abjad_color_music "blue"
                    r8
                    f'8
                }

        ..  container:: example

            Gets every other logical tie:

            ..  container:: example

                >>> string = r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8"
                >>> staff = abjad.Staff(string)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> pattern = abjad.index([0], 2)
                >>> selection = abjad.select(staff).logical_ties(pitched=True)
                >>> for logical_tie in selection[pattern]:
                ...     logical_tie
                ...
                LogicalTie([Note("c'8")])
                LogicalTie([Note("e'8"), Note("e'8"), Note("e'8")])

            ..  container:: example expression

                >>> selector = abjad.select().logical_ties(pitched=True)
                >>> selector = selector[pattern]
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Note("c'8")])
                LogicalTie([Note("e'8"), Note("e'8"), Note("e'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    d'8
                    ~
                    d'8
                    \abjad_color_music "blue"
                    e'8
                    ~
                    \abjad_color_music "blue"
                    e'8
                    ~
                    \abjad_color_music "blue"
                    e'8
                    r8
                    f'8
                }

        ..  container:: example

            Gets note 1 (or nothing) in each pitched logical tie:

            ..  container:: example

                >>> staff = abjad.Staff(r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> getter = abjad.select().leaves()[abjad.index([1])]
                >>> for selection in abjad.select(staff).logical_ties(
                ...     pitched=True,
                ...     ).map(getter):
                ...     selection
                ...
                Selection(items=())
                Selection([Note("d'8")])
                Selection([Note("e'8")])
                Selection(items=())

            ..  container:: example expression

                >>> getter = abjad.select().leaves()[abjad.index([1])]
                >>> selector = abjad.select().logical_ties(pitched=True)
                >>> selector = selector.map(getter)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection(items=())
                Selection([Note("d'8")])
                Selection([Note("e'8")])
                Selection(items=())

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                d'8
                ~
                \abjad_color_music "blue"
                d'8
                e'8
                ~
                \abjad_color_music "red"
                e'8
                ~
                e'8
                r8
                f'8
            }

        ..  container:: example

            >>> abjad.select().leaves()[:2]
            abjad.select().leaves()[:2]

        Returns a single item (or expression) when ``argument`` is an integer.

        Returns new selection (or expression) when ``argument`` is a slice.

        Returns new selection (or expression) when ``argument`` is a pattern.
        """
        if self._expression:
            method = Expression._make___getitem___string_template
            template = method(argument)
            template = template.format(self._expression.template)
            return self._update_expression(
                inspect.currentframe(),
                template=template,
                )
        if isinstance(argument, Pattern):
            items = Sequence(self.items).retain_pattern(argument)
            result = type(self)(items)
        else:
            result = self.items.__getitem__(argument)
            if isinstance(result, tuple):
                result = type(self)(result)
        return result

    def __getstate__(self):
        """
        Gets state of selection.

        Returns dictionary.
        """
        if hasattr(self, '__dict__'):
            state = vars(self).copy()
        else:
            state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, '__slots__', ()):
                try:
                    state[slot] = getattr(self, slot)
                except AttributeError:
                    pass
        return state

    def __hash__(self):
        """
        Hashes selection.

        Redefined in tandem with __eq__.
        """
        return super().__hash__()

    def __illustrate__(self):
        """
        Attempts to illustrate selection.

        Evaluates the storage format of the selection (to sever any references
        to the source score from which the selection was taken). Then tries to
        wrap the result in a staff; in the case that notes of only C4 are found
        then sets the staff context name to ``'RhythmicStaff'``. If this works
        then the staff is wrapped in a LilyPond file and the file is returned.
        If this doesn't work then the method raises an exception.

        The idea is that the illustration should work for simple selections of
        that represent an essentially contiguous snippet of a single voice of
        music.

        Returns LilyPond file.
        """
        import abjad
        components = mutate(self).copy()
        staff = abjad.Staff(components)
        found_different_pitch = False
        for pitch in iterate(staff).pitches():
            if pitch != abjad.NamedPitch("c'"):
                found_different_pitch = True
                break
        if not found_different_pitch:
            staff.lilypond_type = 'RhythmicStaff'
        score = abjad.Score([staff])
        lilypond_file = abjad.LilyPondFile.new(score)
        return lilypond_file

    def __len__(self):
        """
        Gets number of items in selection.

        Returns nonnegative integer.
        """
        return len(self.items)

    def __radd__(self, argument):
        """
        Concatenates selection to ``argument``.

        Returns newly created selection.
        """
        assert isinstance(argument, collections.Iterable)
        items = tuple(argument) + self.items
        return type(self)(items=items)

    def __repr__(self):
        """
        Gets interpreter representation of selection.

        Returns string.
        """
        return super().__repr__()

    def __setstate__(self, state):
        """
        Sets state of selection.

        Returns none.
        """
        for key, value in state.items():
            setattr(self, key, value)

    ### PRIVATE METHODS ###

    def _attach_tie_to_leaf_pair(self, repeat_ties=False):
        from abjad.spanners.Tie import Tie
        assert len(self) == 2
        left_leaf, right_leaf = self
        assert isinstance(left_leaf, Leaf), left_leaf
        assert isinstance(right_leaf, Leaf), right_leaf
        left_logical_tie = left_leaf._get_logical_tie()
        right_logical_tie = right_leaf._get_logical_tie()
        if left_logical_tie == right_logical_tie:
            return
        try:
            left_tie = left_leaf._get_spanner(Tie)
        except exceptions.MissingSpannerError:
            left_tie = None
        try:
            right_tie = right_leaf._get_spanner(Tie)
        except exceptions.MissingSpannerError:
            right_tie = None
        if left_tie is not None and right_tie is not None:
            result = left_tie._copy(left_tie[:])
            left_tie._block_all_leaves()
            right_tie._block_all_leaves()
            result._extend(right_tie)
        elif left_tie is not None and right_tie is None:
            left_tie._append(right_leaf)
        elif left_tie is None and right_tie is not None:
            leaves = [left_leaf] + right_tie[:1]
            leaves = Selection(leaves)
            assert leaves.are_contiguous_logical_voice()
            left_leaf._append_spanner(right_tie)
            right_tie._leaves.insert(0, left_leaf)
        elif left_tie is None and right_tie is None:
            tie = Tie(repeat=repeat_ties)
            leaves = Selection([left_leaf, right_leaf])
            attach(tie, leaves)

    def _attach_tie_to_leaves(self, repeat_ties=False):
        pairs = Sequence(self).nwise()
        for leaf_pair in pairs:
            selection = Selection(leaf_pair)
            selection._attach_tie_to_leaf_pair(
                repeat_ties=repeat_ties,
                )

    @staticmethod
    def _check(items):
        for item in items:
            if not isinstance(item, (Component, Selection)):
                raise TypeError(f'components / selections only: {items!r}.')

    @classmethod
    def _components(
        class_,
        argument,
        prototype=None,
        head=None,
        tail=None,
        trim=None,
        grace_notes=None,
        ):
        prototype = prototype or Component
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        result = []
        generator = iterate(argument).components(
            prototype,
            grace_notes=grace_notes,
            )
        components = list(generator)
        if components:
            if trim in (True, enums.Left):
                components = Selection._trim_subresult(components, trim)
            if head is not None:
                components = Selection._head_filter_subresult(components, head)
            if tail is not None:
                components = Selection._tail_filter_subresult(components, tail)
            result.extend(components)
        return class_(result)

    def _copy(self):
        from .Container import Container
        assert self.are_contiguous_logical_voice()
        new_components = []
        for component in self:
            if isinstance(component, Container):
                new_component = component._copy_with_children()
            else:
                new_component = component.__copy__()
            new_components.append(new_component)
        new_components = type(self)(new_components)
        # find spanners
        spanner_to_pairs = OrderedDict()
        for i, component in enumerate(iterate(self).components()):
            for spanner in abjad_inspect(component).spanners():
                pairs = spanner_to_pairs.setdefault(spanner, [])
                wrappers = []
                if wrappers:
                    for wrapper in wrappers:
                        pairs.append((i, wrapper))
                else:
                    pairs.append((i, None))
        # copy spanners
        new_spanner_to_pairs = OrderedDict()
        for spanner, pairs in spanner_to_pairs.items():
            new_spanner = copy.copy(spanner)
            new_spanner_to_pairs[new_spanner] = pairs
        # make reversed map
        index_to_pairs = OrderedDict()
        for new_spanner, pairs in new_spanner_to_pairs.items():
            for (i, wrapper) in pairs:
                pairs = index_to_pairs.setdefault(i, [])
                pair = (new_spanner, wrapper)
                pairs.append(pair)
        # add new components to new spanners
        new_components_ = iterate(new_components).components()
        for i, new_component in enumerate(new_components_):
            for pair in index_to_pairs.get(i, []):
                new_spanner, wrapper = pair
                if new_component not in new_spanner:
                    new_spanner._append(new_component)
        return new_components

    def _fuse(self):
        from .Measure import Measure
        from .Tuplet import Tuplet
        assert self.are_contiguous_logical_voice()
        if self.are_leaves():
            return self._fuse_leaves()
        elif all(isinstance(_, Tuplet) for _ in self):
            return self._fuse_tuplets()
        elif all(isinstance(_, Measure) for _ in self):
            return self._fuse_measures()
        else:
            raise Exception('can not fuse.')

    def _fuse_leaves(self):
        assert self.are_leaves()
        assert self.are_contiguous_logical_voice()
        leaves = self
        if len(leaves) <= 1:
            return leaves
        total_preprolated = leaves._get_preprolated_duration()
        for leaf in leaves[1:]:
            parent = leaf._parent
            if parent:
                index = parent.index(leaf)
                del(parent[index])
        return leaves[0]._set_duration(total_preprolated)

    def _fuse_measures(self):
        from .Measure import Measure
        assert self.are_contiguous_same_parent(prototype=Measure)
        if len(self) == 0:
            return None
        # TODO: instantiate a new measure
        #       instead of returning a reference to existing measure
        if len(self) == 1:
            return self[0]
        implicit_scaling = self[0].implicit_scaling
        assert all(
            x.implicit_scaling == implicit_scaling for x in self)
        selection = Selection(self)
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        old_denominators = []
        new_duration = Duration(0)
        for measure in self:
            effective_time_signature = measure.time_signature
            old_denominators.append(effective_time_signature.denominator)
            new_duration += effective_time_signature.duration
        new_time_signature = measure._duration_to_time_signature(
            new_duration,
            old_denominators,
            )
        components = []
        for measure in self:
            # scale before reassignment to prevent logical tie scale drama
            signature = measure.time_signature
            prolation = signature.implied_prolation
            multiplier = prolation / new_time_signature.implied_prolation
            measure._scale_contents(multiplier)
            measure_components = measure[:]
            measure_components._set_parents(None)
            components += measure_components
        new_measure = Measure(new_time_signature, components)
        new_measure.implicit_scaling = self[0].implicit_scaling
        if parent is not None:
            self._give_dominant_spanners([new_measure])
        self._set_parents(None)
        if parent is not None:
            parent.insert(start, new_measure)
        return new_measure

    def _fuse_tuplets(self):
        from .Container import Container
        from .Tuplet import Tuplet
        assert self.are_contiguous_same_parent(prototype=Tuplet)
        if len(self) == 0:
            return None
        first = self[0]
        first_multiplier = first.multiplier
        first_type = type(first)
        for tuplet in self[1:]:
            if tuplet.multiplier != first_multiplier:
                message = 'tuplets must carry same multiplier.'
                raise ValueError(message)
            if type(tuplet) != first_type:
                message = 'tuplets must be same type.'
                raise TypeError(message)
        assert isinstance(first, Tuplet)
        new_tuplet = Tuplet(first_multiplier, [])
        wrapped = False
        if (abjad_inspect(self[0]).parentage().root is not
            abjad_inspect(self[-1]).parentage().root):
            dummy_container = Container(self)
            wrapped = True
        mutate(self).swap(new_tuplet)
        if wrapped:
            del(dummy_container[:])
        return new_tuplet

    def _get_component(self, prototype=None, n=0, recurse=True):
        prototype = prototype or (Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        if 0 <= n:
            if recurse:
                components = iterate(self).components(prototype)
            else:
                components = self.items
            for i, x in enumerate(components):
                if i == n:
                    return x
        else:
            if recurse:
                components = iterate(self).components(
                    prototype, reverse=True)
            else:
                components = reversed(self.items)
            for i, x in enumerate(components):
                if i == abs(n) - 1:
                    return x

    def _get_crossing_spanners(self):
        """
        Assert logical-voice-contiguous components.
        Collect spanners that attach to any component in selection.
        Returns unordered set of crossing spanners.
        A spanner P crosses a list of logical-voice-contiguous components C
        when P and C share at least one component and when it is the
        case that NOT ALL of the components in P are also in C.
        In other words, there is some intersection -- but not total
        intersection -- between the components of P and C.
        """
        assert self.are_contiguous_logical_voice()
        all_components = set(iterate(self).components())
        contained_spanners = []
        for leaf in iterate(self).leaves():
            spanners = leaf._get_spanners()
            contained_spanners.extend(spanners)
        ids = []
        contained_spanners_ = []
        for spanner in contained_spanners:
            if id(spanner) not in ids:
                contained_spanners_.append(spanner)
            ids.append(id(spanner))
        contained_spanners = contained_spanners_
        crossing_spanners = []
        for contained_spanner in contained_spanners:
            spanner_components = set(contained_spanner[:])
            if not spanner_components.issubset(all_components):
                crossing_spanners.append(contained_spanner)
        return crossing_spanners

    def _get_dominant_spanners(self):
        """
        Returns spanners that dominate components in selection.
        Returns set of (spanner, index) pairs.
        Each (spanner, index) pair gives a spanner which dominates
        all components in selection together with the start index
        at which spanner first encounters selection.
        Use this helper to lift spanners temporarily from components
        in selection and perform some action to the underlying
        score tree before reattaching spanners.
        score components.
        """
        assert self.are_contiguous_logical_voice()
        receipt = []
        if len(self) == 0:
            return receipt
        first, last = self[0], self[-1]
        start_components = first._get_descendants_starting_with()
        stop_components = last._get_descendants_stopping_with()
        stop_components = set(stop_components)
        for component in start_components:
            if isinstance(component, Leaf):
                for spanner in component._get_spanners():
                    if set(spanner[:]) & stop_components != set():
                        index = spanner._index(component)
                        receipt.append((spanner, index))
        return receipt

    def _get_format_specification(self):
        values = []
        if self.items:
            values = [list(self.items)]
        return FormatSpecification(
            client=self,
            storage_format_args_values=values,
            )

    def _get_offset_lists(self):
        start_offsets, stop_offsets = [], []
        for component in self:
            start_offsets.append(
                abjad_inspect(component).timespan().start_offset)
            stop_offsets.append(
                abjad_inspect(component).timespan().stop_offset)
        return start_offsets, stop_offsets

    def _get_parent_and_start_stop_indices(self):
        assert self.are_contiguous_same_parent()
        if self:
            first, last = self[0], self[-1]
            parent = first._parent
            if parent is not None:
                first_index = parent.index(first)
                last_index = parent.index(last)
                return parent, first_index, last_index
        return None, None, None

    def _get_preprolated_duration(self):
        return sum(component._get_preprolated_duration() for component in self)

    def _get_spanner(self, prototype=None):
        spanners = self._get_spanners(prototype=prototype)
        if not spanners:
            raise exceptions.MissingSpannerError
        elif len(spanners) == 1:
            return spanners.pop()
        else:
            raise exceptions.ExtraSpannerError

    def _get_spanners(self, prototype=None):
        from abjad.spanners.Spanner import Spanner
        prototype = prototype or (Spanner,)
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        assert isinstance(prototype, tuple)
        result, ids = [], []
        for leaf in self:
            spanners = leaf._get_spanners(prototype)
            for spanner in spanners:
                if id(spanner) not in ids:
                    result.append(spanner)
                ids.append(id(spanner))
        return result

    @staticmethod
    def _get_template(frame, selector):
        try:
            frame_info = inspect.getframeinfo(frame)
            function_name = frame_info.function
            arguments = Expression._wrap_arguments(frame)
        finally:
            del frame
        template = f'.{function_name}({arguments})'
        return selector.template + template

    def _give_components_to_empty_container(self, container):
        """
        Not composer-safe.
        """
        from .Container import Container
        assert self.are_contiguous_same_parent()
        assert isinstance(container, Container)
        assert not container
        components = []
        for component in self:
            components.extend(getattr(component, 'components', ()))
        container._components.extend(components)
        container[:]._set_parents(container)

    def _give_dominant_spanners(self, recipients):
        """
        Find all spanners dominating components.
        Insert each component in recipients into each dominant spanner.
        Remove components from each dominating spanner.
        Returns none.
        Not composer-safe.
        """
        assert self.are_contiguous_logical_voice()
        assert Selection(recipients).are_contiguous_logical_voice()
        receipt = self._get_dominant_spanners()
        for spanner, index in receipt:
            for recipient in reversed(recipients):
                spanner._insert(index, recipient)
            for component in self:
                spanner._remove(component)

    def _give_position_in_parent_to_container(self, container):
        """
        Not composer-safe.
        """
        from .Container import Container
        assert self.are_contiguous_same_parent()
        assert isinstance(container, Container)
        parent, start, stop = self._get_parent_and_start_stop_indices()
        if parent is not None:
            parent._components.__setitem__(slice(start, start), [container])
            container._set_parent(parent)
            self._set_parents(None)

    @staticmethod
    def _head_filter_subresult(result, head):
        result_ = []
        for item in result:
            if isinstance(item, Component):
                logical_tie = abjad_inspect(item).logical_tie()
                if head == (item is logical_tie.head):
                    result_.append(item)
                else:
                    pass
            elif isinstance(item, Selection):
                if not all(isinstance(_, Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in item:
                    logical_tie = abjad_inspect(component).logical_tie()
                    if head == logical_tie.head:
                        selection.append(item)
                    else:
                        pass
                selection = Selection(selection)
                result_.append(selection)
            else:
                raise TypeError(item)
        assert isinstance(result_, list), repr(result_)
        return Selection(result_)

    def _iterate_components(self, recurse=True, reverse=False):
        if recurse:
            return iterate(self).components()
        else:
            return self._iterate_top_level_components(reverse=reverse)

    def _iterate_top_level_components(self, reverse=False):
        if reverse:
            for component in reversed(self):
                yield component
        else:
            for component in self:
                yield component

    def _set_parents(self, new_parent):
        """
        Not composer-safe.
        """
        for component in self.items:
            component._set_parent(new_parent)

    @staticmethod
    def _tail_filter_subresult(result, tail):
        result_ = []
        for item in result:
            if isinstance(item, Component):
                logical_tie = abjad_inspect(item).logical_tie()
                if tail == (item is logical_tie.tail):
                    result_.append(item)
                else:
                    pass
            elif isinstance(item, Selection):
                if not all(isinstance(_, Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in item:
                    logical_tie = abjad_inspect(component).logical_tie()
                    if tail == logical_tie.tail:
                        selection.append(item)
                    else:
                        pass
                selection = Selection(selection)
                result_.append(selection)
            else:
                raise TypeError(item)
        assert isinstance(result_, list), repr(result_)
        return Selection(result_)

    @staticmethod
    def _trim_subresult(result, trim):
        assert trim in (True, enums.Left)
        prototype = (MultimeasureRest, Rest, Skip)
        result_ = []
        found_good_component = False
        for item in result:
            if isinstance(item, Component):
                if not isinstance(item, prototype):
                    found_good_component = True
            elif isinstance(item, Selection):
                if not all(isinstance(_, Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in item:
                    if not isinstance(component, prototype):
                        found_good_component = True
                    if found_good_component:
                        selection.append(component)
                item = Selection(selection)
            else:
                raise TypeError(item)
            if found_good_component:
                result_.append(item)
        if trim is enums.Left:
            result = Selection(result_)
        else:
            result__ = []
            found_good_component = False
            for item in reversed(result_):
                if isinstance(item, Component):
                    if not isinstance(item, prototype):
                        found_good_component = True
                elif isinstance(item, Selection):
                    if not all(isinstance(_, Component) for _ in item):
                        raise NotImplementedError(item)
                    selection = []
                    for component in reversed(item):
                        if not isinstance(component, prototype):
                            found_good_component = True
                        if found_good_component:
                            selection.insert(0, component)
                    item = Selection(selection)
                else:
                    raise TypeError(item)
                if found_good_component:
                    result__.insert(0, item)
            assert isinstance(result__, list), repr(result__)
            result = Selection(result__)
        return result

    def _update_expression(
        self,
        frame,
        evaluation_template=None,
        lone=None,
        map_operand=None,
        template=None,
        ):
        callback = Expression._frame_to_callback(
            frame,
            evaluation_template=evaluation_template,
            map_operand=map_operand,
            )
        callback = new(callback, lone=lone)
        expression = self._expression.append_callback(callback)
        if template is None:
            template = self._get_template(frame, self._expression)
        return new(expression, template=template)

    def _withdraw_from_crossing_spanners(self):
        """
        Not composer-safe.
        """
        assert self.are_contiguous_logical_voice()
        crossing_spanners = self._get_crossing_spanners()
        components_including_children = Selection(self).components()
        for crossing_spanner in list(crossing_spanners):
            spanner_components = crossing_spanner.leaves[:]
            for component in components_including_children:
                if component in spanner_components:
                    crossing_spanner._leaves.remove(component)
                    component._remove_spanner(crossing_spanner)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        """
        Gets items.

        ..  container:: example

            >>> abjad.Staff("c'4 d'4 e'4 f'4")[:].items
            (Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4"))

        Returns tuple.
        """
        return self._items

    ### PUBLIC METHODS ###

    def are_contiguous_logical_voice(self, prototype=None, allow_orphans=True):
        """
        Is true when items in selection are contiguous components in the
        same logical voice.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> staff[:].are_contiguous_logical_voice()
            True

            >>> selection = staff[:1] + staff[-1:]
            >>> selection.are_contiguous_logical_voice()
            False

        Returns true or false.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if not isinstance(self, collections.Iterable):
            return False
        prototype = prototype or (Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        assert isinstance(prototype, tuple)
        if len(self) == 0:
            return True
        all_are_orphans_of_correct_type = True
        if allow_orphans:
            for component in self:
                if not isinstance(component, prototype):
                    all_are_orphans_of_correct_type = False
                    break
                if not abjad_inspect(component).parentage().is_orphan:
                    all_are_orphans_of_correct_type = False
                    break
            if all_are_orphans_of_correct_type:
                return True
        if not allow_orphans:
            if any(abjad_inspect(x).parentage().is_orphan for x in self):
                return False
        first = self[0]
        if not isinstance(first, prototype):
            return False
        first_parentage = abjad_inspect(first).parentage()
        first_logical_voice = first_parentage.logical_voice
        first_root = first_parentage.root
        previous = first
        for current in self[1:]:
            current_parentage = abjad_inspect(current).parentage()
            current_logical_voice = current_parentage.logical_voice
            # false if wrong type of component found
            if not isinstance(current, prototype):
                return False
            # false if in different logical voices
            if current_logical_voice != first_logical_voice:
                return False
            # false if components are in same score and are discontiguous
            if current_parentage.root == first_root:
                if not previous._is_immediate_temporal_successor_of(current):
                    return False
            previous = current
        return True

    def are_leaves(self):
        """
        Is true when items in selection are all leaves.

        ..  container:: example

            >>> abjad.Staff("c'4 d'4 e'4 f'4")[:].are_leaves()
            True

        Returns true or false.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return all(isinstance(_, Leaf) for _ in self)

    def are_logical_voice(self, prototype=None, allow_orphans=True):
        """
        Is true when items in selection are all components in the same
        logical voice.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> staff[:].are_logical_voice()
            True

            >>> selection = staff[:1] + staff[-1:]
            >>> selection.are_logical_voice()
            True

        Returns true or false.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        prototype = prototype or (Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        assert isinstance(prototype, tuple)
        if len(self) == 0:
            return True
        all_are_orphans_of_correct_type = True
        if allow_orphans:
            for component in self:
                if not isinstance(component, prototype):
                    all_are_orphans_of_correct_type = False
                    break
                if not abjad_inspect(component).parentage().is_orphan:
                    all_are_orphans_of_correct_type = False
                    break
            if all_are_orphans_of_correct_type:
                return True
        first = self[0]
        if not isinstance(first, prototype):
            return False
        orphan_components = True
        if not abjad_inspect(first).parentage().is_orphan:
            orphan_components = False
        same_logical_voice = True
        first_signature = abjad_inspect(first).parentage().logical_voice
        for component in self[1:]:
            parentage = abjad_inspect(component).parentage()
            if not parentage.is_orphan:
                orphan_components = False
            if not allow_orphans and orphan_components:
                return False
            if parentage.logical_voice != first_signature:
                same_logical_voice = False
            if not allow_orphans and not same_logical_voice:
                return False
            if (allow_orphans and
                not orphan_components and
                not same_logical_voice
                ):
                return False
        return True

    def are_contiguous_same_parent(self, prototype=None, allow_orphans=True):
        """
        Is true when items in selection are all contiguous components in
        the same parent.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> staff[:].are_contiguous_same_parent()
            True

            >>> selection = staff[:1] + staff[-1:]
            >>> selection.are_contiguous_same_parent()
            False

        Returns true or false.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        prototype = prototype or (Component, )
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        assert isinstance(prototype, tuple)
        if len(self) == 0:
            return True
        all_are_orphans_of_correct_type = True
        if allow_orphans:
            for component in self:
                if not isinstance(component, prototype):
                    all_are_orphans_of_correct_type = False
                    break
                if not abjad_inspect(component).parentage().is_orphan:
                    all_are_orphans_of_correct_type = False
                    break
            if all_are_orphans_of_correct_type:
                return True
        first = self[0]
        if not isinstance(first, prototype):
            return False
        first_parent = first._parent
        if first_parent is None:
            if allow_orphans:
                orphan_components = True
            else:
                return False
        same_parent = True
        strictly_contiguous = True
        previous = first
        for current in self[1:]:
            if not isinstance(current, prototype):
                return False
            if not abjad_inspect(current).parentage().is_orphan:
                orphan_components = False
            if current._parent is not first_parent:
                same_parent = False
            if not previous._is_immediate_temporal_successor_of(current):
                strictly_contiguous = False
            if ((not allow_orphans or
                (allow_orphans and not orphan_components)) and
                (not same_parent or not strictly_contiguous)):
                return False
            previous = current
        return True

    def chord(self, n):
        r"""
        Selects chord ``n``.

        ..  container:: example

            Selects chord -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = abjad.select(staff).chord(-1)

                >>> result
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = abjad.select().chord(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<fs' gs'>16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            \abjad_color_music "green"
                            <fs' gs'>16
                        }
                    }   % measure
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.chords()[n]

    def chords(self):
        r"""
        Selects chords.

        ..  container:: example

            Selects chords:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = abjad.select(staff).chords()

                >>> for item in result:
                ...     item
                ...
                Chord("<a'' b''>16")
                Chord("<d' e'>4")
                Chord("<d' e'>16")
                Chord("<a'' b''>16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Chord("<a'' b''>16")
                Chord("<fs' gs'>4")
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = abjad.select().chords()
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<a'' b''>16")
                Chord("<d' e'>4")
                Chord("<d' e'>16")
                Chord("<a'' b''>16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Chord("<a'' b''>16")
                Chord("<fs' gs'>4")
                Chord("<fs' gs'>16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            \abjad_color_music "red"
                            <a'' b''>16
                            c'16
                            \abjad_color_music "blue"
                            <d' e'>4
                            ~
                            \abjad_color_music "red"
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            \abjad_color_music "blue"
                            <a'' b''>16
                            d'16
                            \abjad_color_music "red"
                            <e' fs'>4
                            ~
                            \abjad_color_music "blue"
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            \abjad_color_music "red"
                            <a'' b''>16
                            e'16
                            \abjad_color_music "blue"
                            <fs' gs'>4
                            ~
                            \abjad_color_music "red"
                            <fs' gs'>16
                        }
                    }   % measure
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.components(Chord)

    def components(self, prototype=None, grace_notes=None, reverse=False):
        r"""
        Selects components.

        ..  container:: example

            Selects notes:

            ..  container:: example

                >>> staff = abjad.Staff("c'4 d'8 ~ d'16 e'16 ~ e'8 r4 g'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).components(abjad.Note)

                >>> for item in result:
                ...     item
                ...
                Note("c'4")
                Note("d'8")
                Note("d'16")
                Note("e'16")
                Note("e'8")
                Note("g'8")

            ..  container:: example expression

                >>> selector = abjad.select().components(abjad.Note)
                >>> result = selector(staff)

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

                >>> selector.print(result)
                Note("c'4")
                Note("d'8")
                Note("d'16")
                Note("e'16")
                Note("e'8")
                Note("g'8")

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'4
                    \abjad_color_music "blue"
                    d'8
                    ~
                    \abjad_color_music "red"
                    d'16
                    \abjad_color_music "blue"
                    e'16
                    ~
                    \abjad_color_music "red"
                    e'8
                    r4
                    \abjad_color_music "blue"
                    g'8
                }

        Returns new selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        generator = iterate(self).components(
            prototype=prototype,
            reverse=reverse,
            grace_notes=grace_notes,
            )
        return type(self)(generator)

    def filter(self, predicate=None):
        r"""
        Filters selection by ``predicate``.

        ..  container:: example

            Selects runs with duration equal to 2/8:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> inequality = abjad.DurationInequality('==', (2, 8))
                >>> result = abjad.select(staff).runs().filter(inequality)

                >>> for item in result:
                ...     item
                ...
                Selection([Note("d'8"), Note("e'8")])

            ..  container:: example expression

                >>> selector = abjad.select().runs().filter(inequality)
                >>> result = selector(staff)

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

                >>> selector.print(result)
                Selection([Note("d'8"), Note("e'8")])

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    r8
                    \abjad_color_music "red"
                    d'8
                    \abjad_color_music "red"
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        Returns new selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if predicate is None:
            return type(self)(self)
        return type(self)([_ for _ in self if predicate(_)])

    def filter_duration(self, operator, duration):
        r"""
        Filters selection by ``operator`` and ``duration``.

        ..  container:: example

            Selects runs with duration equal to 2/8:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).runs()
                >>> result = result.filter_duration('==', (2, 8))

                >>> for item in result:
                ...     item
                ...
                Selection([Note("d'8"), Note("e'8")])

            ..  container:: example expression

                >>> selector = abjad.select().runs()
                >>> selector = selector.filter_duration('==', (2, 8))
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("d'8"), Note("e'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    r8
                    \abjad_color_music "red"
                    d'8
                    \abjad_color_music "red"
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        ..  container:: example

            Selects runs with duration less than 3/8:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).runs()
                >>> result = result.filter_duration('<', (3, 8))

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8")])
                Selection([Note("d'8"), Note("e'8")])

            ..  container:: example expresison

                >>> selector = abjad.select().runs()
                >>> selector = selector.filter_duration('<', (3, 8))
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8")])
                Selection([Note("d'8"), Note("e'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    r8
                    \abjad_color_music "blue"
                    d'8
                    \abjad_color_music "blue"
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        Returns new selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.filter(DurationInequality(operator, duration))

    def filter_length(self, operator, length):
        r"""
        Filters selection by ``operator`` and ``length``.

        ..  container:: example

            Selects notes runs with length greater than 1:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).runs().filter_length('>', 1)

                >>> for item in result:
                ...     item
                ...
                Selection([Note("d'8"), Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

            ..  container:: example expression

                >>> selector = abjad.select().runs().filter_length('>', 1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("d'8"), Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    r8
                    \abjad_color_music "red"
                    d'8
                    \abjad_color_music "red"
                    e'8
                    r8
                    \abjad_color_music "blue"
                    f'8
                    \abjad_color_music "blue"
                    g'8
                    \abjad_color_music "blue"
                    a'8
                }

        ..  container:: example

            Selects runs with length less than 3:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).runs().filter_length('<', 3)

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8")])
                Selection([Note("d'8"), Note("e'8")])

            ..  container:: example expression

                >>> selector = abjad.select().runs().filter_length('<', 3)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8")])
                Selection([Note("d'8"), Note("e'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    r8
                    \abjad_color_music "blue"
                    d'8
                    \abjad_color_music "blue"
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.filter(LengthInequality(operator, length))

    def filter_pitches(self, operator, pitches):
        r"""
        Filters selection by ``operator`` and ``pitches``.

        ..  container:: example

            Selects leaves with pitches intersecting C4:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 ~ d'8 e'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> staff.extend("r8 <c' e' g'>8 ~ <c' e' g'>4")
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.filter_pitches('&', 'C4')

                >>> for item in result:
                ...     item
                ...
                Note("c'8")
                Chord("<c' e' g'>8")
                Chord("<c' e' g'>4")

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.filter_pitches('&', 'C4')
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("c'8")
                Chord("<c' e' g'>8")
                Chord("<c' e' g'>4")

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    d'8
                    ~
                    d'8
                    e'8
                    r8
                    \abjad_color_music "blue"
                    <c' e' g'>8
                    ~
                    \abjad_color_music "red"
                    <c' e' g'>4
                }

        ..  container:: example

            Selects leaves with pitches intersecting C4 or E4:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 ~ d'8 e'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> staff.extend("r8 <c' e' g'>8 ~ <c' e' g'>4")
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.filter_pitches('&', 'C4 E4')

                >>> for item in result:
                ...     item
                ...
                Note("c'8")
                Note("e'8")
                Chord("<c' e' g'>8")
                Chord("<c' e' g'>4")

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.filter_pitches('&', 'C4 E4')
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("c'8")
                Note("e'8")
                Chord("<c' e' g'>8")
                Chord("<c' e' g'>4")

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    d'8
                    ~
                    d'8
                    \abjad_color_music "blue"
                    e'8
                    r8
                    \abjad_color_music "red"
                    <c' e' g'>8
                    ~
                    \abjad_color_music "blue"
                    <c' e' g'>4
                }

        ..  container:: example

            Selects logical ties with pitches intersecting C4:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 ~ d'8 e'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> staff.extend("r8 <c' e' g'>8 ~ <c' e' g'>4")
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).logical_ties()
                >>> result = result.filter_pitches('&', 'C4')

                >>> for item in result:
                ...     item
                ...
                LogicalTie([Note("c'8")])
                LogicalTie([Chord("<c' e' g'>8"), Chord("<c' e' g'>4")])

            ..  container:: example expression

                >>> selector = abjad.select().logical_ties()
                >>> selector = selector.filter_pitches('&', 'C4')
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Note("c'8")])
                LogicalTie([Chord("<c' e' g'>8"), Chord("<c' e' g'>4")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    d'8
                    ~
                    d'8
                    e'8
                    r8
                    \abjad_color_music "blue"
                    <c' e' g'>8
                    ~
                    \abjad_color_music "blue"
                    <c' e' g'>4
                }

        Returns new selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.filter(PitchInequality(operator, pitches))

    def filter_preprolated(self, operator, duration):
        r"""
        Filters selection by ``operator`` and preprolated ``duration``.

        ..  container:: example

            Selects runs with duration equal to 2/8:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).runs()
                >>> result = result.filter_preprolated('==', (2, 8))

                >>> for item in result:
                ...     item
                ...
                Selection([Note("d'8"), Note("e'8")])

            ..  container:: example expression

                >>> selector = abjad.select().runs()
                >>> selector = selector.filter_preprolated('==', (2, 8))
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("d'8"), Note("e'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    r8
                    \abjad_color_music "red"
                    d'8
                    \abjad_color_music "red"
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        ..  container:: example

            Selects runs with duration less than 3/8:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).runs()
                >>> result = result.filter_preprolated('<', (3, 8))

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8")])
                Selection([Note("d'8"), Note("e'8")])

            ..  container:: example expresison

                >>> selector = abjad.select().runs()
                >>> selector = selector.filter_preprolated('<', (3, 8))
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8")])
                Selection([Note("d'8"), Note("e'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    r8
                    \abjad_color_music "blue"
                    d'8
                    \abjad_color_music "blue"
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        Returns new selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        inequality = DurationInequality(
            operator,
            duration,
            preprolated=True,
            )
        return self.filter(inequality)

    def flatten(self, depth=1):
        r"""
        Flattens selection to ``depth``.

        ..  container:: example

            Selects first two leaves of each tuplet:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> getter = abjad.select().leaves()[:2]
                >>> result = abjad.select(staff).tuplets().map(getter)

                >>> for item in result:
                ...     item
                Selection([Rest('r16'), Note("bf'16")])
                Selection([Rest('r16'), Note("bf'16")])
                Selection([Rest('r16'), Note("bf'16")])

            ..  container:: example expression

                >>> selector = abjad.select().tuplets().map(getter)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Rest('r16'), Note("bf'16")])
                Selection([Rest('r16'), Note("bf'16")])
                Selection([Rest('r16'), Note("bf'16")])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \abjad_color_music "red"
                            r16
                            \abjad_color_music "red"
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            \abjad_color_music "blue"
                            r16
                            \abjad_color_music "blue"
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \abjad_color_music "red"
                            r16
                            \abjad_color_music "red"
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        ..  container:: example

            Selects first two leaves of all tuplets:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> getter = abjad.select().leaves()[:2]
                >>> result = abjad.select(staff).tuplets().map(getter)
                >>> result = result.flatten()

                >>> for item in result:
                ...     item
                Rest('r16')
                Note("bf'16")
                Rest('r16')
                Note("bf'16")
                Rest('r16')
                Note("bf'16")

            ..  container:: example expression

                >>> selector = abjad.select().tuplets().map(getter).flatten()
                >>> result = selector(staff)

                >>> selector.print(result)
                Rest('r16')
                Note("bf'16")
                Rest('r16')
                Note("bf'16")
                Rest('r16')
                Note("bf'16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \abjad_color_music "red"
                            r16
                            \abjad_color_music "blue"
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            \abjad_color_music "red"
                            r16
                            \abjad_color_music "blue"
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \abjad_color_music "red"
                            r16
                            \abjad_color_music "blue"
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        Returns new selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return type(self)(Sequence(self).flatten(depth=depth))

    def group(self):
        r"""
        Groups selection.

        ..  container:: example

            ..  container:: example

                >>> staff = abjad.Staff(r'''
                ...     c'8 ~ c'16 c'16 r8 c'16 c'16
                ...     d'8 ~ d'16 d'16 r8 d'16 d'16
                ...     ''')
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff, strict=89) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves(pitched=True).group()

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("c'16"), Note("c'16"), Note("c'16"), Note("c'16"), Note("d'8"), Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves(pitched=True).group()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Selection([Note("c'8"), Note("c'16"), Note("c'16"), Note("c'16"), Note("c'16"), Note("d'8"), Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])])

                >>> selector.color(result)
                >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "green"
                    c'8
                    ~
                    \abjad_color_music "green"
                    c'16
                    \abjad_color_music "green"
                    c'16
                    r8
                    \abjad_color_music "green"
                    c'16
                    \abjad_color_music "green"
                    c'16
                    \abjad_color_music "green"
                    d'8
                    ~
                    \abjad_color_music "green"
                    d'16
                    \abjad_color_music "green"
                    d'16
                    r8
                    \abjad_color_music "green"
                    d'16
                    \abjad_color_music "green"
                    d'16
                }

        Returns nested selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.group_by()

    def group_by(self, predicate=None):
        r'''
        Groups items in selection by ``predicate``.

        ..  container:: example

            Wraps selection in selection when ``predicate`` is none:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     c'8 ~ c'16 c'16 r8 c'16 c'16
                ...     d'8 ~ d'16 d'16 r8 d'16 d'16
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves(pitched=True)
                >>> result = result.group_by()

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("c'16"), Note("c'16"), Note("c'16"), Note("c'16"), Note("d'8"), Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves(pitched=True).group_by()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Selection([Note("c'8"), Note("c'16"), Note("c'16"), Note("c'16"), Note("c'16"), Note("d'8"), Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "green"
                    c'8
                    ~
                    \abjad_color_music "green"
                    c'16
                    \abjad_color_music "green"
                    c'16
                    r8
                    \abjad_color_music "green"
                    c'16
                    \abjad_color_music "green"
                    c'16
                    \abjad_color_music "green"
                    d'8
                    ~
                    \abjad_color_music "green"
                    d'16
                    \abjad_color_music "green"
                    d'16
                    r8
                    \abjad_color_music "green"
                    d'16
                    \abjad_color_music "green"
                    d'16
                }

        Returns nested selection (or expression).
        '''
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                evaluation_template='group_by',
                map_operand=predicate,
                )
        items = []
        if predicate is None:
            def predicate(argument):
                return True
        pairs = itertools.groupby(self, predicate)
        for count, group in pairs:
            item = type(self)(group)
            items.append(item)
        return type(self)(items)

    def group_by_contiguity(self):
        r'''
        Groups items in selection by contiguity.

        ..  container:: example

            Groups pitched leaves by contiguity:

            ..  container:: example

                >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
                >>> staff = abjad.Staff(string)
                >>> abjad.setting(staff).auto_beaming = False
                >>> staff.extend("r8 <c' e' g'>8 ~ <c' e' g'>4")
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves(pitched=True)
                >>> result = result.group_by_contiguity()

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("d'8")])
                Selection([Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])
                Selection([Chord("<c' e' g'>8"), Chord("<c' e' g'>4")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves(pitched=True)
                >>> selector = selector.group_by_contiguity()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Note("d'8")])
                Selection([Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])
                Selection([Chord("<c' e' g'>8"), Chord("<c' e' g'>4")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "red"
                    d'8
                    r8
                    \times 2/3 {
                        \abjad_color_music "blue"
                        e'8
                        r8
                        \abjad_color_music "red"
                        f'8
                    }
                    \abjad_color_music "red"
                    g'8
                    \abjad_color_music "red"
                    a'8
                    r8
                    r8
                    \abjad_color_music "blue"
                    <c' e' g'>8
                    ~
                    \abjad_color_music "blue"
                    <c' e' g'>4
                }

        ..  container:: example

            Groups sixteenths by contiguity:

            ..  container:: example

                >>> staff = abjad.Staff("c'4 d'16 d' d' d' e'4 f'16 f' f' f'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.filter_duration('==', (1, 16))
                >>> result = result.group_by_contiguity()

                >>> for item in result:
                ...     item
                ...
                Selection([Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])
                Selection([Note("f'16"), Note("f'16"), Note("f'16"), Note("f'16")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.filter_duration('==', (1, 16))
                >>> selector = selector.group_by_contiguity()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])
                Selection([Note("f'16"), Note("f'16"), Note("f'16"), Note("f'16")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'4
                    \abjad_color_music "red"
                    d'16
                    \abjad_color_music "red"
                    d'16
                    \abjad_color_music "red"
                    d'16
                    \abjad_color_music "red"
                    d'16
                    e'4
                    \abjad_color_music "blue"
                    f'16
                    \abjad_color_music "blue"
                    f'16
                    \abjad_color_music "blue"
                    f'16
                    \abjad_color_music "blue"
                    f'16
                }

        ..  container:: example

            Groups short-duration logical ties by contiguity; then gets leaf 0
            in each group:

            ..  container:: example

                >>> staff = abjad.Staff("c'4 d'8 ~ d'16 e'16 ~ e'8 f'4 g'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).logical_ties()
                >>> result = result.filter_duration('<', (1, 4))
                >>> result = result.group_by_contiguity()
                >>> result = result.map(abjad.select().leaves()[0])

                >>> for item in result:
                ...     item
                Note("d'8")
                Note("g'8")

            ..  container:: example expression

                >>> selector = abjad.select().logical_ties()
                >>> selector = selector.filter_duration('<', (1, 4))
                >>> selector = selector.group_by_contiguity()
                >>> selector = selector.map(abjad.select().leaves()[0])
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("d'8")
                Note("g'8")

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'4
                    \abjad_color_music "red"
                    d'8
                    ~
                    d'16
                    e'16
                    ~
                    e'8
                    f'4
                    \abjad_color_music "blue"
                    g'8
                }

        ..  container:: example

            Groups pitched leaves pitch; then regroups each group by
            contiguity:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     c'8 ~ c'16 c'16 r8 c'16 c'16
                ...     d'8 ~ d'16 d'16 r8 d'16 d'16
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves(pitched=True)
                >>> result = result.group_by_pitch()
                >>> result = result.map(abjad.select().group_by_contiguity())
                >>> result = result.flatten()

                >>> for item in result:
                ...     item
                Selection([Note("c'8"), Note("c'16"), Note("c'16")])
                Selection([Note("c'16"), Note("c'16")])
                Selection([Note("d'8"), Note("d'16"), Note("d'16")])
                Selection([Note("d'16"), Note("d'16")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves(pitched=True)
                >>> selector = selector.group_by_pitch()
                >>> selector = selector.map(
                ...     abjad.select().group_by_contiguity()
                ...     )
                >>> selector = selector.flatten()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Note("c'16"), Note("c'16")])
                Selection([Note("c'16"), Note("c'16")])
                Selection([Note("d'8"), Note("d'16"), Note("d'16")])
                Selection([Note("d'16"), Note("d'16")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    ~
                    \abjad_color_music "red"
                    c'16
                    \abjad_color_music "red"
                    c'16
                    r8
                    \abjad_color_music "blue"
                    c'16
                    \abjad_color_music "blue"
                    c'16
                    \abjad_color_music "red"
                    d'8
                    ~
                    \abjad_color_music "red"
                    d'16
                    \abjad_color_music "red"
                    d'16
                    r8
                    \abjad_color_music "blue"
                    d'16
                    \abjad_color_music "blue"
                    d'16
                }

        ..  container:: example

            Groups pitched logical ties by contiguity; then regroups each group
            by pitch:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     c'8 ~ c'16 c'16 r8 c'16 c'16
                ...     d'8 ~ d'16 d'16 r8 d'16 d'16
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> getter = abjad.select().group_by_pitch()

                >>> result = abjad.select(staff).logical_ties(pitched=True)
                >>> result = result.group_by_contiguity()
                >>> result = result.map(getter).flatten()

                >>> for item in result:
                ...     item
                ...
                Selection([LogicalTie([Note("c'8"), Note("c'16")]), LogicalTie([Note("c'16")])])
                Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])
                Selection([LogicalTie([Note("d'8"), Note("d'16")]), LogicalTie([Note("d'16")])])
                Selection([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")])])

            ..  container:: example expression

                >>> selector = abjad.select().logical_ties(pitched=True)
                >>> selector = selector.group_by_contiguity()
                >>> selector = selector.map(getter).flatten()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([LogicalTie([Note("c'8"), Note("c'16")]), LogicalTie([Note("c'16")])])
                Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])
                Selection([LogicalTie([Note("d'8"), Note("d'16")]), LogicalTie([Note("d'16")])])
                Selection([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")])])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    ~
                    \abjad_color_music "red"
                    c'16
                    \abjad_color_music "red"
                    c'16
                    r8
                    \abjad_color_music "blue"
                    c'16
                    \abjad_color_music "blue"
                    c'16
                    \abjad_color_music "red"
                    d'8
                    ~
                    \abjad_color_music "red"
                    d'16
                    \abjad_color_music "red"
                    d'16
                    r8
                    \abjad_color_music "blue"
                    d'16
                    \abjad_color_music "blue"
                    d'16
                }

        Returns new selection (or expression).
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result, selection = [], []
        selection.extend(self[:1])
        for item in self[1:]:
            this_timespan = abjad_inspect(selection[-1]).timespan()
            that_timespan = abjad_inspect(item).timespan()
            if this_timespan.stop_offset == that_timespan.start_offset:
                selection.append(item)
            else:
                result.append(type(self)(selection))
                selection = [item]
        if selection:
            result.append(type(self)(selection))
        return type(self)(result)

    def group_by_duration(self):
        r"""
        Groups items in selection by duration.

        ..  container:: example

            Groups logical ties by duration:

            ..  container:: example

                >>> string = "c'4 ~ c'16 d' ~ d' d' e'4 ~ e'16 f' ~ f' f'"
                >>> staff = abjad.Staff(string)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).logical_ties()
                >>> result = result.group_by_duration()

                >>> for item in result:
                ...     item
                ...
                Selection([LogicalTie([Note("c'4"), Note("c'16")])])
                Selection([LogicalTie([Note("d'16"), Note("d'16")])])
                Selection([LogicalTie([Note("d'16")])])
                Selection([LogicalTie([Note("e'4"), Note("e'16")])])
                Selection([LogicalTie([Note("f'16"), Note("f'16")])])
                Selection([LogicalTie([Note("f'16")])])

            ..  container:: example expression

                >>> selector = abjad.select().logical_ties().group_by_duration()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([LogicalTie([Note("c'4"), Note("c'16")])])
                Selection([LogicalTie([Note("d'16"), Note("d'16")])])
                Selection([LogicalTie([Note("d'16")])])
                Selection([LogicalTie([Note("e'4"), Note("e'16")])])
                Selection([LogicalTie([Note("f'16"), Note("f'16")])])
                Selection([LogicalTie([Note("f'16")])])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'4
                    ~
                    \abjad_color_music "red"
                    c'16
                    \abjad_color_music "blue"
                    d'16
                    ~
                    \abjad_color_music "blue"
                    d'16
                    \abjad_color_music "red"
                    d'16
                    \abjad_color_music "blue"
                    e'4
                    ~
                    \abjad_color_music "blue"
                    e'16
                    \abjad_color_music "red"
                    f'16
                    ~
                    \abjad_color_music "red"
                    f'16
                    \abjad_color_music "blue"
                    f'16
                }

        Returns nested selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        def predicate(argument):
            return abjad_inspect(argument).duration()
        return self.group_by(predicate)

    def group_by_length(self):
        r"""
        Groups items in selection by length.

        ..  container:: example

            Groups logical ties by length:

            ..  container:: example

                >>> string = "c'4 ~ c'16 d' ~ d' d' e'4 ~ e'16 f' ~ f' f'"
                >>> staff = abjad.Staff(string)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).logical_ties().group_by_length()

                >>> for item in result:
                ...     item
                ...
                Selection([LogicalTie([Note("c'4"), Note("c'16")]), LogicalTie([Note("d'16"), Note("d'16")])])
                Selection([LogicalTie([Note("d'16")])])
                Selection([LogicalTie([Note("e'4"), Note("e'16")]), LogicalTie([Note("f'16"), Note("f'16")])])
                Selection([LogicalTie([Note("f'16")])])

            ..  container:: example expression

                >>> selector = abjad.select().logical_ties().group_by_length()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([LogicalTie([Note("c'4"), Note("c'16")]), LogicalTie([Note("d'16"), Note("d'16")])])
                Selection([LogicalTie([Note("d'16")])])
                Selection([LogicalTie([Note("e'4"), Note("e'16")]), LogicalTie([Note("f'16"), Note("f'16")])])
                Selection([LogicalTie([Note("f'16")])])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'4
                    ~
                    \abjad_color_music "red"
                    c'16
                    \abjad_color_music "red"
                    d'16
                    ~
                    \abjad_color_music "red"
                    d'16
                    \abjad_color_music "blue"
                    d'16
                    \abjad_color_music "red"
                    e'4
                    ~
                    \abjad_color_music "red"
                    e'16
                    \abjad_color_music "red"
                    f'16
                    ~
                    \abjad_color_music "red"
                    f'16
                    \abjad_color_music "blue"
                    f'16
                }

        Returns nested selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        def predicate(argument):
            if isinstance(argument, Leaf):
                return 1
            return len(argument)
        return self.group_by(predicate)

    def group_by_measure(self):
        r"""
        Groups items in selection by measure.

        ..  container:: example

            Groups leaves by logical measure:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.group_by_measure()

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("d'8")])
                Selection([Note("e'8"), Note("f'8")])
                Selection([Note("g'8"), Note("a'8"), Note("b'8")])
                Selection([Note("c''8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.group_by_measure()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Note("d'8")])
                Selection([Note("e'8"), Note("f'8")])
                Selection([Note("g'8"), Note("a'8"), Note("b'8")])
                Selection([Note("c''8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "red"
                    d'8
                    \abjad_color_music "blue"
                    e'8
                    \abjad_color_music "blue"
                    f'8
                    \time 3/8
                    \abjad_color_music "red"
                    g'8
                    \abjad_color_music "red"
                    a'8
                    \abjad_color_music "red"
                    b'8
                    \time 1/8
                    \abjad_color_music "blue"
                    c''8
                }

        ..  container:: example

            Groups leaves by logical measure and joins pairs of consecutive
            groups:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.group_by_measure()
                >>> result = result.partition_by_counts([2], cyclic=True)
                >>> result = result.map(abjad.select().flatten())

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")])
                Selection([Note("g'8"), Note("a'8"), Note("b'8"), Note("c''8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.group_by_measure()
                >>> selector = selector.partition_by_counts([2], cyclic=True)
                >>> selector = selector.map(abjad.select().flatten())
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")])
                Selection([Note("g'8"), Note("a'8"), Note("b'8"), Note("c''8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "red"
                    d'8
                    \abjad_color_music "red"
                    e'8
                    \abjad_color_music "red"
                    f'8
                    \time 3/8
                    \abjad_color_music "blue"
                    g'8
                    \abjad_color_music "blue"
                    a'8
                    \abjad_color_music "blue"
                    b'8
                    \time 1/8
                    \abjad_color_music "blue"
                    c''8
                }

        ..  container:: example

            Groups leaves by logical measure; then gets item 0 in each group:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.group_by_measure()
                >>> result = result.map(abjad.select()[0])

                >>> for item in result:
                ...     item
                Note("c'8")
                Note("e'8")
                Note("g'8")
                Note("c''8")

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.group_by_measure()
                >>> selector = selector.map(abjad.select()[0])
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("c'8")
                Note("e'8")
                Note("g'8")
                Note("c''8")

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad_color_music "red"
                    c'8
                    d'8
                    \abjad_color_music "blue"
                    e'8
                    f'8
                    \time 3/8
                    \abjad_color_music "red"
                    g'8
                    a'8
                    b'8
                    \time 1/8
                    \abjad_color_music "blue"
                    c''8
                }

        ..  container:: example

            Groups leaves by logical measure; then gets item -1 in each group:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.group_by_measure()
                >>> result = result.map(abjad.select()[-1])

                >>> for item in result:
                ...     item
                ...
                Note("d'8")
                Note("f'8")
                Note("b'8")
                Note("c''8")

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.group_by_measure()
                >>> selector = selector.map(abjad.select()[-1])
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("d'8")
                Note("f'8")
                Note("b'8")
                Note("c''8")

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    c'8
                    \abjad_color_music "red"
                    d'8
                    e'8
                    \abjad_color_music "blue"
                    f'8
                    \time 3/8
                    g'8
                    a'8
                    \abjad_color_music "red"
                    b'8
                    \time 1/8
                    \abjad_color_music "blue"
                    c''8
                }

        ..  container:: example

            Works with implicit time signatures:

            ..  container:: example

                >>> staff = abjad.Staff("c'4 d' e' f' g' a' b' c''")
                >>> abjad.setting(staff).auto_beaming = False
                >>> score = abjad.Score([staff])
                >>> scheme = abjad.SchemeMoment((1, 16))
                >>> abjad.setting(score).proportional_notation_duration = scheme
                >>> abjad.show(score) # doctest: +SKIP

                >>> result = abjad.select(score).leaves()
                >>> result = result.group_by_measure()

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])
                Selection([Note("g'4"), Note("a'4"), Note("b'4"), Note("c''4")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.group_by_measure()
                >>> result = selector(score)

                >>> selector.print(result)
                Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])
                Selection([Note("g'4"), Note("a'4"), Note("b'4"), Note("c''4")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'4
                    \abjad_color_music "red"
                    d'4
                    \abjad_color_music "red"
                    e'4
                    \abjad_color_music "red"
                    f'4
                    \abjad_color_music "blue"
                    g'4
                    \abjad_color_music "blue"
                    a'4
                    \abjad_color_music "blue"
                    b'4
                    \abjad_color_music "blue"
                    c''4
                }

        Returns new selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        def _get_first_component(argument):
            if isinstance(argument, Component):
                return argument
            else:
                component = argument[0]
                assert isinstance(component, Component)
                return component
        def _get_measure_number(argument):
            first_component = _get_first_component(argument)
            assert first_component._measure_number is not None
            return first_component._measure_number
        selections = []
        first_component = _get_first_component(self)
        first_component._update_measure_numbers()
        pairs = itertools.groupby(self, _get_measure_number)
        for value, group in pairs:
            selection = type(self)(group)
            selections.append(selection)
        return type(self)(selections)

    def group_by_pitch(self):
        r"""
        Groups items in selection by pitches.

        ..  container:: example

            Groups logical ties by pitches:

            ..  container:: example

                >>> string = "c'4 ~ c'16 d' ~ d' d' e'4 ~ e'16 f' ~ f' f'"
                >>> staff = abjad.Staff(string)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).logical_ties().group_by_pitch()

                >>> for item in result:
                ...     item
                ...
                Selection([LogicalTie([Note("c'4"), Note("c'16")])])
                Selection([LogicalTie([Note("d'16"), Note("d'16")]), LogicalTie([Note("d'16")])])
                Selection([LogicalTie([Note("e'4"), Note("e'16")])])
                Selection([LogicalTie([Note("f'16"), Note("f'16")]), LogicalTie([Note("f'16")])])

            ..  container:: example expression

                >>> selector = abjad.select().logical_ties().group_by_pitch()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([LogicalTie([Note("c'4"), Note("c'16")])])
                Selection([LogicalTie([Note("d'16"), Note("d'16")]), LogicalTie([Note("d'16")])])
                Selection([LogicalTie([Note("e'4"), Note("e'16")])])
                Selection([LogicalTie([Note("f'16"), Note("f'16")]), LogicalTie([Note("f'16")])])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'4
                    ~
                    \abjad_color_music "red"
                    c'16
                    \abjad_color_music "blue"
                    d'16
                    ~
                    \abjad_color_music "blue"
                    d'16
                    \abjad_color_music "blue"
                    d'16
                    \abjad_color_music "red"
                    e'4
                    ~
                    \abjad_color_music "red"
                    e'16
                    \abjad_color_music "blue"
                    f'16
                    ~
                    \abjad_color_music "blue"
                    f'16
                    \abjad_color_music "blue"
                    f'16
                }

        Returns nested selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        def predicate(argument):
            return PitchSet.from_selection(argument)
        return self.group_by(predicate)

    def leaf(self, n):
        r"""
        Selects leaf ``n``.

        ..  container:: example

            Selects leaf -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = abjad.select(staff).leaf(-1)

                >>> result
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = abjad.select().leaf(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<fs' gs'>16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            \abjad_color_music "green"
                            <fs' gs'>16
                        }
                    }   % measure
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.leaves()[n]

    def leaves(
        self,
        prototype=None,
        grace_notes: bool = False,
        head: bool = None,
        pitched: bool = None,
        reverse: bool = False,
        tail: bool = None,
        trim: typing.Union[bool, enums.HorizontalAlignment] = None,
        ):
        r'''
        Selects leaves (without grace notes).

        ..  container:: example

            Selects leaves:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { r8 d' e' } f' r
                ...     r f' \times 2/3 { e' d' r8 }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()

                >>> for item in result:
                ...     item
                ...
                Rest('r8')
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Rest('r8')
                Rest('r8')
                Note("f'8")
                Note("e'8")
                Note("d'8")
                Rest('r8')

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Rest('r8')
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Rest('r8')
                Rest('r8')
                Note("f'8")
                Note("e'8")
                Note("d'8")
                Rest('r8')

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        \abjad_color_music "red"
                        r8
                        \abjad_color_music "blue"
                        d'8
                        \abjad_color_music "red"
                        e'8
                    }
                    \abjad_color_music "blue"
                    f'8
                    \abjad_color_music "red"
                    r8
                    \abjad_color_music "blue"
                    r8
                    \abjad_color_music "red"
                    f'8
                    \times 2/3 {
                        \abjad_color_music "blue"
                        e'8
                        \abjad_color_music "red"
                        d'8
                        \abjad_color_music "blue"
                        r8
                    }
                }

        ..  container:: example

            Selects pitched leaves:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { r8 d' e' } f' r
                ...     r f' \times 2/3 { e' d' r8 }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves(pitched=True)

                >>> for item in result:
                ...     item
                ...
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Note("f'8")
                Note("e'8")
                Note("d'8")

            ..  container:: example expression

                >>> selector = abjad.select().leaves(pitched=True)
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Note("f'8")
                Note("e'8")
                Note("d'8")

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        r8
                        \abjad_color_music "red"
                        d'8
                        \abjad_color_music "blue"
                        e'8
                    }
                    \abjad_color_music "red"
                    f'8
                    r8
                    r8
                    \abjad_color_music "blue"
                    f'8
                    \times 2/3 {
                        \abjad_color_music "red"
                        e'8
                        \abjad_color_music "blue"
                        d'8
                        r8
                    }
                }

        ..  container:: example

            Trimmed leaves are the correct selection for ottava spanners.

            Selects trimmed leaves:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { r8 d' e' } f' r
                ...     r f' \times 2/3 { e' d' r8 }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves(trim=True)

                >>> for item in result:
                ...     item
                ...
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Rest('r8')
                Rest('r8')
                Note("f'8")
                Note("e'8")
                Note("d'8")

            ..  container:: example expression

                >>> selector = abjad.select().leaves(trim=True)
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Rest('r8')
                Rest('r8')
                Note("f'8")
                Note("e'8")
                Note("d'8")

                >>> abjad.attach(abjad.OctavationSpanner(), result)

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        r8
                        \ottava #1
                        \abjad_color_music "red"
                        d'8
                        \abjad_color_music "blue"
                        e'8
                    }
                    \abjad_color_music "red"
                    f'8
                    \abjad_color_music "blue"
                    r8
                    \abjad_color_music "red"
                    r8
                    \abjad_color_music "blue"
                    f'8
                    \times 2/3 {
                        \abjad_color_music "red"
                        e'8
                        \abjad_color_music "blue"
                        d'8
                        \ottava #0
                        r8
                    }
                }

        ..  container:: example

            Set ``trim`` to ``abjad.Left`` to trim rests at left (and preserve
            rests at right):

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { r8 d' e' } f' r
                ...     r f' \times 2/3 { e' d' r8 }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves(trim=abjad.Left)

                >>> for item in result:
                ...     item
                ...
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Rest('r8')
                Rest('r8')
                Note("f'8")
                Note("e'8")
                Note("d'8")
                Rest('r8')

            ..  container:: example expression

                >>> selector = abjad.select().leaves(trim=abjad.Left)
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Rest('r8')
                Rest('r8')
                Note("f'8")
                Note("e'8")
                Note("d'8")
                Rest('r8')

                >>> abjad.attach(abjad.OctavationSpanner(), result)

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        r8
                        \ottava #1
                        \abjad_color_music "red"
                        d'8
                        \abjad_color_music "blue"
                        e'8
                    }
                    \abjad_color_music "red"
                    f'8
                    \abjad_color_music "blue"
                    r8
                    \abjad_color_music "red"
                    r8
                    \abjad_color_music "blue"
                    f'8
                    \times 2/3 {
                        \abjad_color_music "red"
                        e'8
                        \abjad_color_music "blue"
                        d'8
                        \abjad_color_music "red"
                        r8
                        \ottava #0
                    }
                }

        ..  container:: example

            REGRESSION: selects trimmed leaves (even when there are no rests to
            trim):

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { c'8 d' e' } f' r
                ...     r f' \times 2/3 { e' d' c' }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves(trim=True)

                >>> for item in result:
                ...     item
                ...
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Rest('r8')
                Rest('r8')
                Note("f'8")
                Note("e'8")
                Note("d'8")
                Note("c'8")

            ..  container:: example expression

                >>> selector = abjad.select().leaves(trim=True)
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Rest('r8')
                Rest('r8')
                Note("f'8")
                Note("e'8")
                Note("d'8")
                Note("c'8")

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        \abjad_color_music "red"
                        c'8
                        \abjad_color_music "blue"
                        d'8
                        \abjad_color_music "red"
                        e'8
                    }
                    \abjad_color_music "blue"
                    f'8
                    \abjad_color_music "red"
                    r8
                    \abjad_color_music "blue"
                    r8
                    \abjad_color_music "red"
                    f'8
                    \times 2/3 {
                        \abjad_color_music "blue"
                        e'8
                        \abjad_color_music "red"
                        d'8
                        \abjad_color_music "blue"
                        c'8
                    }
                }

        ..  container:: example

            Selects leaves in tuplets:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { r8 d' e' } f' r
                ...     r f' \times 2/3 { e' d' r8 }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).components(abjad.Tuplet)
                >>> result = result.leaves()

                >>> for item in result:
                ...     item
                ...
                Rest('r8')
                Note("d'8")
                Note("e'8")
                Note("e'8")
                Note("d'8")
                Rest('r8')

            ..  container:: example expression

                >>> selector = abjad.select().components(abjad.Tuplet)
                >>> selector = selector.leaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Rest('r8')
                Note("d'8")
                Note("e'8")
                Note("e'8")
                Note("d'8")
                Rest('r8')

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        \abjad_color_music "red"
                        r8
                        \abjad_color_music "blue"
                        d'8
                        \abjad_color_music "red"
                        e'8
                    }
                    f'8
                    r8
                    r8
                    f'8
                    \times 2/3 {
                        \abjad_color_music "blue"
                        e'8
                        \abjad_color_music "red"
                        d'8
                        \abjad_color_music "blue"
                        r8
                    }
                }

        ..  container:: example

            Selects trimmed leaves in tuplets:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { r8 d' e' } f' r
                ...     r f' \times 2/3 { e' d' r8 }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).components(abjad.Tuplet)
                >>> result = result.leaves(trim=True)

                >>> for item in result:
                ...     item
                ...
                Note("d'8")
                Note("e'8")
                Note("e'8")
                Note("d'8")

            ..  container:: example expression

                >>> selector = abjad.select().components(abjad.Tuplet)
                >>> selector = selector.leaves(trim=True)
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("d'8")
                Note("e'8")
                Note("e'8")
                Note("d'8")

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        r8
                        \abjad_color_music "red"
                        d'8
                        \abjad_color_music "blue"
                        e'8
                    }
                    f'8
                    r8
                    r8
                    f'8
                    \times 2/3 {
                        \abjad_color_music "red"
                        e'8
                        \abjad_color_music "blue"
                        d'8
                        r8
                    }
                }

        ..  container:: example

            Pitched heads is the correct selection for most articulations.

            Selects pitched heads in tuplets:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { c'8 d' ~ d' } e' r
                ...     r e' \times 2/3 { d' ~ d' c' }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).components(abjad.Tuplet)
                >>> result = result.leaves(head=True, pitched=True)

                >>> for item in result:
                ...     item
                ...
                Note("c'8")
                Note("d'8")
                Note("d'8")
                Note("c'8")

            ..  container:: example expression

                >>> selector = abjad.select().components(abjad.Tuplet)
                >>> selector = selector.leaves(head=True, pitched=True)
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("c'8")
                Note("d'8")
                Note("d'8")
                Note("c'8")

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        \abjad_color_music "red"
                        c'8
                        \abjad_color_music "blue"
                        d'8
                        ~
                        d'8
                    }
                    e'8
                    r8
                    r8
                    e'8
                    \times 2/3 {
                        \abjad_color_music "red"
                        d'8
                        ~
                        d'8
                        \abjad_color_music "blue"
                        c'8
                    }
                }

        ..  container:: example

            Pitched tails in the correct selection for laissez vibrer.

            Selects pitched tails in tuplets:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { c'8 d' ~ d' } e' r
                ...     r e' \times 2/3 { d' ~ d' c' }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).components(abjad.Tuplet)
                >>> result = result.leaves(tail=True, pitched=True)

                >>> for item in result:
                ...     item
                ...
                Note("c'8")
                Note("d'8")
                Note("d'8")
                Note("c'8")

            ..  container:: example expression

                >>> selector = abjad.select()
                >>> selector = selector.components(abjad.Tuplet)
                >>> selector = selector.leaves(tail=True, pitched=True)
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("c'8")
                Note("d'8")
                Note("d'8")
                Note("c'8")

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        \abjad_color_music "red"
                        c'8
                        d'8
                        ~
                        \abjad_color_music "blue"
                        d'8
                    }
                    e'8
                    r8
                    r8
                    e'8
                    \times 2/3 {
                        d'8
                        ~
                        \abjad_color_music "red"
                        d'8
                        \abjad_color_music "blue"
                        c'8
                    }
                }

        ..  container:: example

            Chord heads are the correct selection for arpeggios.

            Selects chord heads in tuplets:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { <c' e' g'>8 ~ <c' e' g'> d' } e' r
                ...     r <g d' fs'> \times 2/3 { e' <c' d'> ~ <c' d'> }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).components(abjad.Tuplet)
                >>> result = result.leaves(abjad.Chord, head=True)

                >>> for item in result:
                ...     item
                ...
                Chord("<c' e' g'>8")
                Chord("<c' d'>8")

            ..  container:: example expression

                >>> selector = abjad.select().components(abjad.Tuplet)
                >>> selector = selector.leaves(abjad.Chord, head=True)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<c' e' g'>8")
                Chord("<c' d'>8")

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        \abjad_color_music "red"
                        <c' e' g'>8
                        ~
                        <c' e' g'>8
                        d'8
                    }
                    e'8
                    r8
                    r8
                    <g d' fs'>8
                    \times 2/3 {
                        e'8
                        \abjad_color_music "blue"
                        <c' d'>8
                        ~
                        <c' d'>8
                    }
                }

        Returns new selection (or expression).
        '''
        assert trim in (True, False, enums.Left, None)
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if pitched:
            prototype = (Chord, Note)
        elif prototype is None:
            prototype = Leaf
        return self._components(
            self,
            prototype=prototype,
            head=head,
            tail=tail,
            trim=trim,
            grace_notes=grace_notes,
            )

    def logical_ties(
        self,
        grace_notes=False,
        nontrivial=None,
        pitched=None,
        reverse=False,
        ):
        r'''
        Selects logical ties (without grace notes).

        ..  container:: example

            Selects logical ties:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).logical_ties()

                >>> for item in result:
                ...     item
                ...
                LogicalTie([Note("c'8")])
                LogicalTie([Note("d'8"), Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Rest('r8')])
                LogicalTie([Note("f'8"), Note("f'8")])
                LogicalTie([Rest('r8')])

            ..  container:: example expression

                >>> selector = abjad.select().logical_ties()
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Note("c'8")])
                LogicalTie([Note("d'8"), Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Rest('r8')])
                LogicalTie([Note("f'8"), Note("f'8")])
                LogicalTie([Rest('r8')])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "blue"
                    d'8
                    ~
                    {
                        \abjad_color_music "blue"
                        d'8
                        \abjad_color_music "red"
                        e'8
                        \abjad_color_music "blue"
                        r8
                        \abjad_color_music "red"
                        f'8
                        ~
                    }
                    \abjad_color_music "red"
                    f'8
                    \abjad_color_music "blue"
                    r8
                }

        ..  container:: example

            Selects pitched logical ties:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).logical_ties(pitched=True)

                >>> for item in result:
                ...     item
                ...
                LogicalTie([Note("c'8")])
                LogicalTie([Note("d'8"), Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'8"), Note("f'8")])

            ..  container:: example expression

                >>> selector = abjad.select().logical_ties(pitched=True)
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Note("c'8")])
                LogicalTie([Note("d'8"), Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'8"), Note("f'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "blue"
                    d'8
                    ~
                    {
                        \abjad_color_music "blue"
                        d'8
                        \abjad_color_music "red"
                        e'8
                        r8
                        \abjad_color_music "blue"
                        f'8
                        ~
                    }
                    \abjad_color_music "blue"
                    f'8
                    r8
                }

        ..  container:: example

            Selects pitched nontrivial logical ties:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).logical_ties(
                ...     pitched=True,
                ...     nontrivial=True,
                ...     )

                >>> for item in result:
                ...     item
                LogicalTie([Note("d'8"), Note("d'8")])
                LogicalTie([Note("f'8"), Note("f'8")])

            ..  container:: example expression

                >>> selector = abjad.select().logical_ties(
                ...     pitched=True,
                ...     nontrivial=True,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Note("d'8"), Note("d'8")])
                LogicalTie([Note("f'8"), Note("f'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    \abjad_color_music "red"
                    d'8
                    ~
                    {
                        \abjad_color_music "red"
                        d'8
                        e'8
                        r8
                        \abjad_color_music "blue"
                        f'8
                        ~
                    }
                    \abjad_color_music "blue"
                    f'8
                    r8
                }

        ..  container:: example

            Selects pitched logical ties (starting) in each tuplet:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { c'8 d' e'  ~ } e' f' ~
                ...     \times 2/3 { f' g' a' ~ } a' b' ~
                ...     \times 2/3 { b' c'' d'' }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> getter = abjad.select().logical_ties(pitched=True)
                >>> result = abjad.select(staff).components(abjad.Tuplet)
                >>> result = result.map(getter)

                >>> for item in result:
                ...     item
                ...
                Selection([LogicalTie([Note("c'8")]), LogicalTie([Note("d'8")]), LogicalTie([Note("e'8"), Note("e'8")])])
                Selection([LogicalTie([Note("g'8")]), LogicalTie([Note("a'8"), Note("a'8")])])
                Selection([LogicalTie([Note("c''8")]), LogicalTie([Note("d''8")])])

            ..  container:: example expression

                >>> selector = abjad.select().components(abjad.Tuplet)
                >>> selector = selector.map(getter)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([LogicalTie([Note("c'8")]), LogicalTie([Note("d'8")]), LogicalTie([Note("e'8"), Note("e'8")])])
                Selection([LogicalTie([Note("g'8")]), LogicalTie([Note("a'8"), Note("a'8")])])
                Selection([LogicalTie([Note("c''8")]), LogicalTie([Note("d''8")])])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        \abjad_color_music "red"
                        c'8
                        \abjad_color_music "red"
                        d'8
                        \abjad_color_music "red"
                        e'8
                        ~
                    }
                    \abjad_color_music "red"
                    e'8
                    f'8
                    ~
                    \times 2/3 {
                        f'8
                        \abjad_color_music "blue"
                        g'8
                        \abjad_color_music "blue"
                        a'8
                        ~
                    }
                    \abjad_color_music "blue"
                    a'8
                    b'8
                    ~
                    \times 2/3 {
                        b'8
                        \abjad_color_music "red"
                        c''8
                        \abjad_color_music "red"
                        d''8
                    }
                }

        ..  container:: example

            Selects pitched logical ties (starting) in each of the last two
            tuplets:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { c'8 d' e'  ~ } e' f' ~
                ...     \times 2/3 { f' g' a' ~ } a' b' ~
                ...     \times 2/3 { b' c'' d'' }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> getter = abjad.select().logical_ties(pitched=True)
                >>> result = abjad.select(staff).components(abjad.Tuplet)[-2:]
                >>> result = result.map(getter)

                >>> for item in result:
                ...     item
                ...
                Selection([LogicalTie([Note("g'8")]), LogicalTie([Note("a'8"), Note("a'8")])])
                Selection([LogicalTie([Note("c''8")]), LogicalTie([Note("d''8")])])

            ..  container:: example expression

                >>> selector = abjad.select().components(abjad.Tuplet)[-2:]
                >>> selector = selector.map(getter)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([LogicalTie([Note("g'8")]), LogicalTie([Note("a'8"), Note("a'8")])])
                Selection([LogicalTie([Note("c''8")]), LogicalTie([Note("d''8")])])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        c'8
                        d'8
                        e'8
                        ~
                    }
                    e'8
                    f'8
                    ~
                    \times 2/3 {
                        f'8
                        \abjad_color_music "red"
                        g'8
                        \abjad_color_music "red"
                        a'8
                        ~
                    }
                    \abjad_color_music "red"
                    a'8
                    b'8
                    ~
                    \times 2/3 {
                        b'8
                        \abjad_color_music "blue"
                        c''8
                        \abjad_color_music "blue"
                        d''8
                    }
                }

        Returns new selection (or expression).
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        generator = iterate(self).logical_ties(
            nontrivial=nontrivial,
            pitched=pitched,
            reverse=reverse,
            grace_notes=grace_notes,
            )
        return type(self)(generator)

    def map(self, expression=None):
        r'''
        Maps ``expression`` to items in selection.

        ..  container:: example

            Selects each tuplet as a separate selection:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { r8 d' e' } f' r
                ...     r f' \times 2/3 { e' d' r8 }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).components(abjad.Tuplet)
                >>> result = result.map(abjad.select())

                >>> for item in result:
                ...     item
                ...
                Selection([Tuplet(Multiplier(2, 3), "r8 d'8 e'8")])
                Selection([Tuplet(Multiplier(2, 3), "e'8 d'8 r8")])

            ..  container:: example expression

                >>> selector = abjad.select().components(abjad.Tuplet)
                >>> selector = selector.map(abjad.select())
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Tuplet(Multiplier(2, 3), "r8 d'8 e'8")])
                Selection([Tuplet(Multiplier(2, 3), "e'8 d'8 r8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        \abjad_color_music "red"
                        r8
                        \abjad_color_music "red"
                        d'8
                        \abjad_color_music "red"
                        e'8
                    }
                    f'8
                    r8
                    r8
                    f'8
                    \times 2/3 {
                        \abjad_color_music "blue"
                        e'8
                        \abjad_color_music "blue"
                        d'8
                        \abjad_color_music "blue"
                        r8
                    }
                }

        ..  container:: example

            Selects leaves in each component:

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     \times 2/3 { r8 d' e' } f' r
                ...     r f' \times 2/3 { e' d' r8 }
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = staff[:].map(abjad.select().leaves())

                >>> for item in result:
                ...     item
                ...
                Selection([Rest('r8'), Note("d'8"), Note("e'8")])
                Selection([Note("f'8")])
                Selection([Rest('r8')])
                Selection([Rest('r8')])
                Selection([Note("f'8")])
                Selection([Note("e'8"), Note("d'8"), Rest('r8')])

            ..  container:: example expression:

                >>> selector = abjad.select().map(abjad.select().leaves())
                >>> result = selector(staff[:])

                >>> selector.print(result)
                Selection([Rest('r8'), Note("d'8"), Note("e'8")])
                Selection([Note("f'8")])
                Selection([Rest('r8')])
                Selection([Rest('r8')])
                Selection([Note("f'8")])
                Selection([Note("e'8"), Note("d'8"), Rest('r8')])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3 {
                        \abjad_color_music "red"
                        r8
                        \abjad_color_music "red"
                        d'8
                        \abjad_color_music "red"
                        e'8
                    }
                    \abjad_color_music "blue"
                    f'8
                    \abjad_color_music "red"
                    r8
                    \abjad_color_music "blue"
                    r8
                    \abjad_color_music "red"
                    f'8
                    \times 2/3 {
                        \abjad_color_music "blue"
                        e'8
                        \abjad_color_music "blue"
                        d'8
                        \abjad_color_music "blue"
                        r8
                    }
                }

        ..  container:: example

            Gets item 0 in each note run:

            ..  container:: example

                >>> string = r"c'4 \times 2/3 { d'8 r8 e'8 } r16 f'16 g'8 a'4"
                >>> staff = abjad.Staff(string)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).runs()
                >>> result = result.map(abjad.select()[0])

                >>> for item in result:
                ...     item
                ...
                Note("c'4")
                Note("e'8")
                Note("f'16")

            ..  container:: example expression

                >>> selector = abjad.select().runs()
                >>> selector = selector.map(abjad.select()[0])
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("c'4")
                Note("e'8")
                Note("f'16")

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'4
                    \times 2/3 {
                        d'8
                        r8
                        \abjad_color_music "blue"
                        e'8
                    }
                    r16
                    \abjad_color_music "red"
                    f'16
                    g'8
                    a'4
                }

        Returns new selection (or expression).
        '''
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                evaluation_template='map',
                map_operand=expression,
                )
        if expression is None:
            return type(self)(self)
        return type(self)([expression(_) for _ in self])

    def note(self, n):
        r"""
        Selects note ``n``.

        ..  container:: example

            Selects note -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = abjad.select(staff).note(-1)

                >>> result
                Note("e'16")

            ..  container:: example expression

                >>> selector = abjad.select().note(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("e'16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            \abjad_color_music "green"
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.notes()[n]

    def notes(self):
        r"""
        Selects notes.

        ..  container:: example

            Selects notes:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = abjad.select(staff).notes()

                >>> for item in result:
                ...     item
                ...
                Note("bf'16")
                Note("c'16")
                Note("bf'16")
                Note("d'16")
                Note("bf'16")
                Note("e'16")

            ..  container:: example expression

                >>> selector = abjad.select().notes()
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("bf'16")
                Note("c'16")
                Note("bf'16")
                Note("d'16")
                Note("bf'16")
                Note("e'16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            \abjad_color_music "red"
                            bf'16
                            <a'' b''>16
                            \abjad_color_music "blue"
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            \abjad_color_music "red"
                            bf'16
                            <a'' b''>16
                            \abjad_color_music "blue"
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            \abjad_color_music "red"
                            bf'16
                            <a'' b''>16
                            \abjad_color_music "blue"
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.components(Note)

    def nontrivial(self):
        r"""
        Filters selection by length greater than 1.

        ..  container:: example

            Selects nontrivial runs:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).runs().nontrivial()

                >>> for item in result:
                ...     item
                ...
                Selection([Note("d'8"), Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

            ..  container:: example expression

                >>> selector = abjad.select().runs().nontrivial()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("d'8"), Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    r8
                    \abjad_color_music "red"
                    d'8
                    \abjad_color_music "red"
                    e'8
                    r8
                    \abjad_color_music "blue"
                    f'8
                    \abjad_color_music "blue"
                    g'8
                    \abjad_color_music "blue"
                    a'8
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.filter_length('>', 1)

    def partition_by_counts(
        self,
        counts,
        cyclic=False,
        enchain=False,
        fuse_overhang=False,
        nonempty=False,
        overhang=False,
        ):
        r"""
        Partitions selection by ``counts``.

        ..  container:: example

            Partitions leaves into a single part of length 3; truncates
            overhang:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Rest('r8'), Note("d'8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Rest('r8'), Note("d'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "red"
                    r8
                    \abjad_color_music "red"
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        ..  container:: example

            Cyclically partitions leaves into parts of length 3; truncates
            overhang:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves().partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Rest('r8'), Note("d'8")])
                Selection([Note("e'8"), Rest('r8'), Note("f'8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves().partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Rest('r8'), Note("d'8")])
                Selection([Note("e'8"), Rest('r8'), Note("f'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "red"
                    r8
                    \abjad_color_music "red"
                    d'8
                    \abjad_color_music "blue"
                    e'8
                    \abjad_color_music "blue"
                    r8
                    \abjad_color_music "blue"
                    f'8
                    g'8
                    a'8
                }

        ..  container:: example

            Cyclically partitions leaves into parts of length 3; returns
            overhang at end:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves().partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Rest('r8'), Note("d'8")])
                Selection([Note("e'8"), Rest('r8'), Note("f'8")])
                Selection([Note("g'8"), Note("a'8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves().partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Rest('r8'), Note("d'8")])
                Selection([Note("e'8"), Rest('r8'), Note("f'8")])
                Selection([Note("g'8"), Note("a'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "red"
                    r8
                    \abjad_color_music "red"
                    d'8
                    \abjad_color_music "blue"
                    e'8
                    \abjad_color_music "blue"
                    r8
                    \abjad_color_music "blue"
                    f'8
                    \abjad_color_music "red"
                    g'8
                    \abjad_color_music "red"
                    a'8
                }

        ..  container:: example

            Cyclically partitions leaves into parts of length 3; fuses overhang
            to last part:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves().partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     fuse_overhang=True,
                ...     overhang=True,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Rest('r8'), Note("d'8")])
                Selection([Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves().partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     fuse_overhang=True,
                ...     overhang=True,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Rest('r8'), Note("d'8")])
                Selection([Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "red"
                    r8
                    \abjad_color_music "red"
                    d'8
                    \abjad_color_music "blue"
                    e'8
                    \abjad_color_music "blue"
                    r8
                    \abjad_color_music "blue"
                    f'8
                    \abjad_color_music "blue"
                    g'8
                    \abjad_color_music "blue"
                    a'8
                }

        ..  container:: example

            Cyclically partitions leaves into parts of length 3; returns
            overhang at end:

            ..  container:: example

                >>> string = "c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8"
                >>> staff = abjad.Staff(string)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves().partition_by_counts(
                ...     [1, 2, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8")])
                Selection([Rest('r8'), Note("d'8")])
                Selection([Note("e'8"), Rest('r8'), Note("f'8")])
                Selection([Note("g'8")])
                Selection([Note("a'8"), Note("b'8")])
                Selection([Rest('r8'), Note("c''8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves().partition_by_counts(
                ...     [1, 2, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8")])
                Selection([Rest('r8'), Note("d'8")])
                Selection([Note("e'8"), Rest('r8'), Note("f'8")])
                Selection([Note("g'8")])
                Selection([Note("a'8"), Note("b'8")])
                Selection([Rest('r8'), Note("c''8")])

                >>> selector.color(result, ['red', 'blue', 'cyan'])
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "blue"
                    r8
                    \abjad_color_music "blue"
                    d'8
                    \abjad_color_music "cyan"
                    e'8
                    \abjad_color_music "cyan"
                    r8
                    \abjad_color_music "cyan"
                    f'8
                    \abjad_color_music "red"
                    g'8
                    \abjad_color_music "blue"
                    a'8
                    \abjad_color_music "blue"
                    b'8
                    \abjad_color_music "cyan"
                    r8
                    \abjad_color_music "cyan"
                    c''8
                }

        Returns nested selection (or expression):

            >>> type(result).__name__
            'Selection'

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = []
        groups = Sequence(self).partition_by_counts(
            [abs(_) for _ in counts],
            cyclic=cyclic,
            enchain=enchain,
            overhang=overhang,
            )
        groups = list(groups)
        if overhang and fuse_overhang and 1 < len(groups):
            last_count = counts[(len(groups) - 1) % len(counts)]
            if len(groups[-1]) != last_count:
                last_group = groups.pop()
                groups[-1] += last_group
        subresult = []
        if cyclic:
            counts = CyclicTuple(counts)
        for i, group in enumerate(groups):
            try:
                count = counts[i]
            except:
                raise Exception(counts, i)
            if count < 0:
                continue
            items = type(self)(group)
            subresult.append(items)
        if nonempty and not subresult:
            group = type(self)(groups[0])
            subresult.append(group)
        result.extend(subresult)
        return type(self)(result)

    def partition_by_durations(
        self,
        durations,
        cyclic=False,
        fill=None,
        in_seconds=False,
        overhang=False,
        ):
        r"""
        Partitions selection by ``durations``.

        ..  container:: example

            Cyclically partitions leaves into parts equal to exactly 3/8;
            returns overhang at end:

            ..  container:: example

                >>> staff = abjad.Staff(
                ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
                ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
                ...     )
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves().partition_by_durations(
                ...     [abjad.Duration(3, 8)],
                ...     cyclic=True,
                ...     fill=abjad.Exact,
                ...     in_seconds=False,
                ...     overhang=True,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("d'8"), Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])
                Selection([Note("b'8"), Note("c''8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves().partition_by_durations(
                ...     [abjad.Duration(3, 8)],
                ...     cyclic=True,
                ...     fill=abjad.Exact,
                ...     in_seconds=False,
                ...     overhang=True,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Note("d'8"), Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])
                Selection([Note("b'8"), Note("c''8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 2/8
                        \abjad_color_music "red"
                        c'8
                        \abjad_color_music "red"
                        d'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        e'8
                        \abjad_color_music "blue"
                        f'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "blue"
                        g'8
                        \abjad_color_music "blue"
                        a'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        b'8
                        \abjad_color_music "red"
                        c''8
                    }   % measure
                }

        ..  container:: example

            Partitions leaves into one part equal to exactly 3/8; truncates
            overhang:

            ..  container:: example

                >>> staff = abjad.Staff(
                ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
                ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
                ...     )
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.partition_by_durations(
                ...     [abjad.Duration(3, 8)],
                ...     cyclic=False,
                ...     fill=abjad.Exact,
                ...     in_seconds=False,
                ...     overhang=False,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("d'8"), Note("e'8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.partition_by_durations(
                ...     [abjad.Duration(3, 8)],
                ...     cyclic=False,
                ...     fill=abjad.Exact,
                ...     in_seconds=False,
                ...     overhang=False,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Note("d'8"), Note("e'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 2/8
                        \abjad_color_music "red"
                        c'8
                        \abjad_color_music "red"
                        d'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        e'8
                        f'8
                    }   % measure
                    {   % measure
                        g'8
                        a'8
                    }   % measure
                    {   % measure
                        b'8
                        c''8
                    }   % measure
                }

        ..  container:: example

            Cyclically partitions leaves into parts equal to (or just less
            than) 3/16 and 1/16; returns overhang at end:

            ..  container:: example

                >>> staff = abjad.Staff(
                ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
                ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
                ...     )
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.partition_by_durations(
                ...     [abjad.Duration(3, 16), abjad.Duration(1, 16)],
                ...     cyclic=True,
                ...     fill=abjad.More,
                ...     in_seconds=False,
                ...     overhang=True,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("d'8")])
                Selection([Note("e'8")])
                Selection([Note("f'8"), Note("g'8")])
                Selection([Note("a'8")])
                Selection([Note("b'8"), Note("c''8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.partition_by_durations(
                ...     [abjad.Duration(3, 16), abjad.Duration(1, 16)],
                ...     cyclic=True,
                ...     fill=abjad.More,
                ...     in_seconds=False,
                ...     overhang=True,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Note("d'8")])
                Selection([Note("e'8")])
                Selection([Note("f'8"), Note("g'8")])
                Selection([Note("a'8")])
                Selection([Note("b'8"), Note("c''8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 2/8
                        \abjad_color_music "red"
                        c'8
                        \abjad_color_music "red"
                        d'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "blue"
                        e'8
                        \abjad_color_music "red"
                        f'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        g'8
                        \abjad_color_music "blue"
                        a'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        b'8
                        \abjad_color_music "red"
                        c''8
                    }   % measure
                }

        ..  container:: example

            Cyclically partitions leaves into parts equal to (or just less
            than) 3/16; truncates overhang:

            ..  container:: example

                >>> staff = abjad.Staff(
                ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
                ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
                ...     )
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.partition_by_durations(
                ...     [abjad.Duration(3, 16)],
                ...     cyclic=True,
                ...     fill=abjad.Less,
                ...     in_seconds=False,
                ...     overhang=False,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8")])
                Selection([Note("d'8")])
                Selection([Note("e'8")])
                Selection([Note("f'8")])
                Selection([Note("g'8")])
                Selection([Note("a'8")])
                Selection([Note("b'8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.partition_by_durations(
                ...     [abjad.Duration(3, 16)],
                ...     cyclic=True,
                ...     fill=abjad.Less,
                ...     in_seconds=False,
                ...     overhang=False,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8")])
                Selection([Note("d'8")])
                Selection([Note("e'8")])
                Selection([Note("f'8")])
                Selection([Note("g'8")])
                Selection([Note("a'8")])
                Selection([Note("b'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 2/8
                        \abjad_color_music "red"
                        c'8
                        \abjad_color_music "blue"
                        d'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        e'8
                        \abjad_color_music "blue"
                        f'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        g'8
                        \abjad_color_music "blue"
                        a'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        b'8
                        c''8
                    }   % measure
                }

        ..  container:: example

            Partitions leaves into a single part equal to (or just less than)
            3/16; truncates overhang:

            ..  container:: example

                >>> staff = abjad.Staff(
                ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
                ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
                ...     )
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.partition_by_durations(
                ...     [abjad.Duration(3, 16)],
                ...     cyclic=False,
                ...     fill=abjad.Less,
                ...     in_seconds=False,
                ...     overhang=False,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.partition_by_durations(
                ...     [abjad.Duration(3, 16)],
                ...     cyclic=False,
                ...     fill=abjad.Less,
                ...     in_seconds=False,
                ...     overhang=False,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 2/8
                        \abjad_color_music "red"
                        c'8
                        d'8
                    }   % measure
                    {   % measure
                        e'8
                        f'8
                    }   % measure
                    {   % measure
                        g'8
                        a'8
                    }   % measure
                    {   % measure
                        b'8
                        c''8
                    }   % measure
                }

        ..  container:: example

            Cyclically partitions leaves into parts equal to exactly 1.5
            seconds; truncates overhang:

            ..  container:: example

                >>> staff = abjad.Staff(
                ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
                ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
                ...     )
                >>> abjad.setting(staff).auto_beaming = False
                >>> mark = abjad.MetronomeMark((1, 4), 60)
                >>> leaf = abjad.inspect(staff).leaf(0)
                >>> abjad.attach(mark, leaf, context='Staff')
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.partition_by_durations(
                ...     [1.5],
                ...     cyclic=True,
                ...     fill=abjad.Exact,
                ...     in_seconds=True,
                ...     overhang=False,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("d'8"), Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.partition_by_durations(
                ...     [1.5],
                ...     cyclic=True,
                ...     fill=abjad.Exact,
                ...     in_seconds=True,
                ...     overhang=False,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Note("d'8"), Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 2/8
                        \tempo 4=60
                        \abjad_color_music "red"
                        c'8
                        \abjad_color_music "red"
                        d'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        e'8
                        \abjad_color_music "blue"
                        f'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "blue"
                        g'8
                        \abjad_color_music "blue"
                        a'8
                    }   % measure
                    {   % measure
                        b'8
                        c''8
                    }   % measure
                }

        ..  container:: example

            Cyclically partitions leaves into parts equal to exactly 1.5
            seconds; returns overhang at end:

            ..  container:: example

                >>> staff = abjad.Staff(
                ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
                ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
                ...     )
                >>> abjad.setting(staff).auto_beaming = False
                >>> mark = abjad.MetronomeMark((1, 4), 60)
                >>> leaf = abjad.inspect(staff).leaf(0)
                >>> abjad.attach(mark, leaf, context='Staff')
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.partition_by_durations(
                ...     [1.5],
                ...     cyclic=True,
                ...     fill=abjad.Exact,
                ...     in_seconds=True,
                ...     overhang=True,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("d'8"), Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])
                Selection([Note("b'8"), Note("c''8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.partition_by_durations(
                ...     [1.5],
                ...     cyclic=True,
                ...     fill=abjad.Exact,
                ...     in_seconds=True,
                ...     overhang=True,
                ...     )

                >>> selector.print(result)
                Selection([Note("c'8"), Note("d'8"), Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])
                Selection([Note("b'8"), Note("c''8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 2/8
                        \tempo 4=60
                        \abjad_color_music "red"
                        c'8
                        \abjad_color_music "red"
                        d'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        e'8
                        \abjad_color_music "blue"
                        f'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "blue"
                        g'8
                        \abjad_color_music "blue"
                        a'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        b'8
                        \abjad_color_music "red"
                        c''8
                    }   % measure
                }

        ..  container:: example

            Partitions leaves into a single part equal to exactly 1.5 seconds;
            truncates overhang:

            ..  container:: example

                >>> staff = abjad.Staff(
                ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
                ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
                ...     )
                >>> abjad.setting(staff).auto_beaming = False
                >>> mark = abjad.MetronomeMark((1, 4), 60)
                >>> leaf = abjad.inspect(staff).leaf(0)
                >>> abjad.attach(mark, leaf, context='Staff')
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.partition_by_durations(
                ...     [1.5],
                ...     cyclic=False,
                ...     fill=abjad.Exact,
                ...     in_seconds=True,
                ...     overhang=False,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("d'8"), Note("e'8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.partition_by_durations(
                ...     [1.5],
                ...     cyclic=False,
                ...     fill=abjad.Exact,
                ...     in_seconds=True,
                ...     overhang=False,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Note("d'8"), Note("e'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 2/8
                        \tempo 4=60
                        \abjad_color_music "red"
                        c'8
                        \abjad_color_music "red"
                        d'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        e'8
                        f'8
                    }   % measure
                    {   % measure
                        g'8
                        a'8
                    }   % measure
                    {   % measure
                        b'8
                        c''8
                    }   % measure
                }

        ..  container:: example

            Cyclically partitions leaves into parts equal to (or just less
            than) 0.75 seconds; truncates overhang:

            ..  container:: example

                >>> staff = abjad.Staff(
                ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
                ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
                ...     )
                >>> abjad.setting(staff).auto_beaming = False
                >>> mark = abjad.MetronomeMark((1, 4), 60)
                >>> leaf = abjad.inspect(staff).leaf(0)
                >>> abjad.attach(mark, leaf, context='Staff')
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.partition_by_durations(
                ...     [0.75],
                ...     cyclic=True,
                ...     fill=abjad.Less,
                ...     in_seconds=True,
                ...     overhang=False,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8")])
                Selection([Note("d'8")])
                Selection([Note("e'8")])
                Selection([Note("f'8")])
                Selection([Note("g'8")])
                Selection([Note("a'8")])
                Selection([Note("b'8")])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.partition_by_durations(
                ...     [0.75],
                ...     cyclic=True,
                ...     fill=abjad.Less,
                ...     in_seconds=True,
                ...     overhang=False,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8")])
                Selection([Note("d'8")])
                Selection([Note("e'8")])
                Selection([Note("f'8")])
                Selection([Note("g'8")])
                Selection([Note("a'8")])
                Selection([Note("b'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 2/8
                        \tempo 4=60
                        \abjad_color_music "red"
                        c'8
                        \abjad_color_music "blue"
                        d'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        e'8
                        \abjad_color_music "blue"
                        f'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        g'8
                        \abjad_color_music "blue"
                        a'8
                    }   % measure
                    {   % measure
                        \abjad_color_music "red"
                        b'8
                        c''8
                    }   % measure
                }

        ..  container:: example

            Partitions leaves into one part equal to (or just less than) 0.75
            seconds; truncates overhang:

            ..  container:: example

                >>> staff = abjad.Staff(
                ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
                ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
                ...     )
                >>> abjad.setting(staff).auto_beaming = False
                >>> mark = abjad.MetronomeMark((1, 4), 60)
                >>> leaf = abjad.inspect(staff).leaf(0)
                >>> abjad.attach(mark, leaf, context='Staff')
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.partition_by_durations(
                ...     [0.75],
                ...     cyclic=False,
                ...     fill=abjad.Less,
                ...     in_seconds=True,
                ...     overhang=False,
                ...     )

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8")])

            ..  container:: example

                >>> selector = abjad.select().leaves()
                >>> selector = selector.partition_by_durations(
                ...     [0.75],
                ...     cyclic=False,
                ...     fill=abjad.Less,
                ...     in_seconds=True,
                ...     overhang=False,
                ...     )
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 2/8
                        \tempo 4=60
                        \abjad_color_music "red"
                        c'8
                        d'8
                    }   % measure
                    {   % measure
                        e'8
                        f'8
                    }   % measure
                    {   % measure
                        g'8
                        a'8
                    }   % measure
                    {   % measure
                        b'8
                        c''8
                    }   % measure
                }

        Interprets ``fill`` as ``Exact`` when ``fill`` is none.

        Parts must equal ``durations`` exactly when ``fill`` is ``Exact``.

        Parts must be less than or equal to ``durations`` when ``fill`` is
        ``Less``.

        Parts must be greater or equal to ``durations`` when ``fill`` is
        ``More``.

        Reads ``durations`` cyclically when ``cyclic`` is true.

        Reads component durations in seconds when ``in_seconds`` is true.

        Returns remaining components at end in final part when ``overhang``
        is true.

        Returns nested selection (or expression):

            >>> type(result).__name__
            'Selection'

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        fill = fill or enums.Exact
        durations = [Duration(_) for _ in durations]
        if cyclic:
            durations = CyclicTuple(durations)
        result = []
        part = []
        current_duration_index = 0
        target_duration = durations[current_duration_index]
        cumulative_duration = Duration(0)
        components_copy = list(self)
        while True:
            try:
                component = components_copy.pop(0)
            except IndexError:
                break
            component_duration = component._get_duration()
            if in_seconds:
                component_duration = abjad_inspect(component).duration(
                    in_seconds=True)
            candidate_duration = cumulative_duration + component_duration
            if candidate_duration < target_duration:
                part.append(component)
                cumulative_duration = candidate_duration
            elif candidate_duration == target_duration:
                part.append(component)
                result.append(part)
                part = []
                cumulative_duration = Duration(0)
                current_duration_index += 1
                try:
                    target_duration = durations[current_duration_index]
                except IndexError:
                    break
            elif target_duration < candidate_duration:
                if fill is enums.Exact:
                    raise Exception('must partition exactly.')
                elif fill is enums.Less:
                    result.append(part)
                    part = [component]
                    if in_seconds:
                        cumulative_duration = sum([
                            abjad_inspect(_).duration(in_seconds=True)
                            for _ in part
                            ])
                    else:
                        cumulative_duration = sum([
                            abjad_inspect(_).duration() for _ in part
                            ])
                    current_duration_index += 1
                    try:
                        target_duration = durations[current_duration_index]
                    except IndexError:
                        break
                    if target_duration < cumulative_duration:
                        message = 'target duration {}'
                        message += ' is less than cumulative duration {}.'
                        message = message.format(
                            target_duration,
                            cumulative_duration,
                            )
                        raise Exception(message)
                elif fill is enums.More:
                    part.append(component)
                    result.append(part)
                    part = []
                    cumulative_duration = Duration(0)
                    current_duration_index += 1
                    try:
                        target_duration = durations[current_duration_index]
                    except IndexError:
                        break
        if len(part):
            if overhang:
                result.append(part)
        if len(components_copy):
            if overhang:
                result.append(components_copy)
        result = [type(self)(_) for _ in result]
        return type(self)(result)

    def partition_by_ratio(self, ratio):
        r"""
        Partitions selection by ``ratio``.

        ..  container:: example

            Partitions leaves by a ratio of 1:1:

            ..  container:: example

                >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
                >>> staff = abjad.Staff(string)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.partition_by_ratio((1, 1))

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("d'8"), Rest('r8'), Note("e'8"), Rest('r8')])
                Selection([Note("f'8"), Note("g'8"), Note("a'8"), Rest('r8')])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.partition_by_ratio((1, 1))
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Note("d'8"), Rest('r8'), Note("e'8"), Rest('r8')])
                Selection([Note("f'8"), Note("g'8"), Note("a'8"), Rest('r8')])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "red"
                    d'8
                    \abjad_color_music "red"
                    r8
                    \times 2/3 {
                        \abjad_color_music "red"
                        e'8
                        \abjad_color_music "red"
                        r8
                        \abjad_color_music "blue"
                        f'8
                    }
                    \abjad_color_music "blue"
                    g'8
                    \abjad_color_music "blue"
                    a'8
                    \abjad_color_music "blue"
                    r8
                }

        ..  container:: example

            Partitions leaves by a ratio of 1:1:1:

            ..  container:: example

                >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
                >>> staff = abjad.Staff(string)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves()
                >>> result = result.partition_by_ratio((1, 1, 1))

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("d'8"), Rest('r8')])
                Selection([Note("e'8"), Rest('r8'), Note("f'8")])
                Selection([Note("g'8"), Note("a'8"), Rest('r8')])

            ..  container:: example expression

                >>> selector = abjad.select().leaves()
                >>> selector = selector.partition_by_ratio((1, 1, 1))
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Note("d'8"), Rest('r8')])
                Selection([Note("e'8"), Rest('r8'), Note("f'8")])
                Selection([Note("g'8"), Note("a'8"), Rest('r8')])

                >>> selector.color(result, ['red', 'blue', 'cyan'])
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "red"
                    d'8
                    \abjad_color_music "red"
                    r8
                    \times 2/3 {
                        \abjad_color_music "blue"
                        e'8
                        \abjad_color_music "blue"
                        r8
                        \abjad_color_music "blue"
                        f'8
                    }
                    \abjad_color_music "cyan"
                    g'8
                    \abjad_color_music "cyan"
                    a'8
                    \abjad_color_music "cyan"
                    r8
                }

        Returns nested selection (or expression):

            >>> type(result).__name__
            'Selection'

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        ratio = ratio or Ratio((1,))
        counts = mathtools.partition_integer_by_ratio(len(self), ratio)
        parts = Sequence(self).partition_by_counts(counts=counts)
        selections = [type(self)(_) for _ in parts]
        return type(self)(selections)

    def rest(self, n):
        r"""
        Selects rest ``n``.

        ..  container:: example

            Selects rest -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = abjad.select(staff).rest(-1)

                >>> result
                Rest('r16')

            ..  container:: example expression

                >>> selector = abjad.select().rest(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Rest('r16')

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \abjad_color_music "green"
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return  self.rests()[n]

    def rests(self):
        r"""
        Selects rests.

        ..  container:: example

            Selects rests:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = abjad.select(staff).rests()

                >>> for item in result:
                ...     item
                ...
                Rest('r16')
                Rest('r16')
                Rest('r16')

            ..  container:: example expression

                >>> selector = abjad.select().rests()
                >>> result = selector(staff)

                >>> selector.print(result)
                Rest('r16')
                Rest('r16')
                Rest('r16')

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \abjad_color_music "red"
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            \abjad_color_music "blue"
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \abjad_color_music "red"
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.components((MultimeasureRest, Rest))

    def run(self, n):
        r"""
        Selects run ``n``.

        ..  container:: example

            Selects run -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = abjad.select(staff).run(-1)

                >>> result
                Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = abjad.select().run(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            c'16
                            c'16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            d'16
                            d'16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            \abjad_color_music "green"
                            e'16
                            \abjad_color_music "green"
                            e'16
                            \abjad_color_music "green"
                            e'16
                            \abjad_color_music "green"
                            <fs' gs'>4
                            ~
                            \abjad_color_music "green"
                            <fs' gs'>16
                        }
                    }   % measure
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.runs()[n]

    def runs(self):
        r"""
        Selects runs.

        ..  container:: example

            Selects runs:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = abjad.select(staff).runs()

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16")])
                Selection([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = abjad.select().runs()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16")])
                Selection([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            \abjad_color_music "red"
                            c'16
                            \abjad_color_music "red"
                            c'16
                            \abjad_color_music "red"
                            c'16
                            \abjad_color_music "red"
                            <d' e'>4
                            ~
                            \abjad_color_music "red"
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            \abjad_color_music "blue"
                            d'16
                            \abjad_color_music "blue"
                            d'16
                            \abjad_color_music "blue"
                            d'16
                            \abjad_color_music "blue"
                            <e' fs'>4
                            ~
                            \abjad_color_music "blue"
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            \abjad_color_music "red"
                            e'16
                            \abjad_color_music "red"
                            e'16
                            \abjad_color_music "red"
                            e'16
                            \abjad_color_music "red"
                            <fs' gs'>4
                            ~
                            \abjad_color_music "red"
                            <fs' gs'>16
                        }
                    }   % measure
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = Selection.leaves(self, pitched=True)
        result = result.group_by_contiguity().map(Selection)
        return result

    def top(self):
        r"""
        Selects top components.

        ..  container:: example

            Selects top components (up from leaves):

            ..  container:: example

                >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
                >>> staff = abjad.Staff(string)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).leaves().top()

                >>> for item in result:
                ...     item
                ...
                Note("c'8")
                Note("d'8")
                Rest('r8')
                Tuplet(Multiplier(2, 3), "e'8 r8 f'8")
                Note("g'8")
                Note("a'8")
                Rest('r8')

            ..  container:: example expression

                >>> selector = abjad.select().leaves().top()
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("c'8")
                Note("d'8")
                Rest('r8')
                Tuplet(Multiplier(2, 3), "e'8 r8 f'8")
                Note("g'8")
                Note("a'8")
                Rest('r8')

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "blue"
                    d'8
                    \abjad_color_music "red"
                    r8
                    \times 2/3 {
                        \abjad_color_music "blue"
                        e'8
                        \abjad_color_music "blue"
                        r8
                        \abjad_color_music "blue"
                        f'8
                    }
                    \abjad_color_music "red"
                    g'8
                    \abjad_color_music "blue"
                    a'8
                    \abjad_color_music "red"
                    r8
                }

        """
        from .Context import Context
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = []
        for component in iterate(self).components(Component):
            parentage = abjad_inspect(component).parentage()
            for component_ in parentage:
                if isinstance(component_, Context):
                    break
                parent = abjad_inspect(component_).parentage().parent
                if isinstance(parent, Context) or parent is None:
                    if component_ not in result:
                        result.append(component_)
                    break
        return type(self)(result)

    def tuplet(self, n):
        r"""
        Selects tuplet ``n``.

        ..  container:: example

            Selects tuplet -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = abjad.select(staff).tuplet(-1)

                >>> result
                Tuplet(Multiplier(10, 9), "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16")

            ..  container:: example expression

                >>> selector = abjad.select().tuplet(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Tuplet(Multiplier(10, 9), "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \abjad_color_music "green"
                            r16
                            \abjad_color_music "green"
                            bf'16
                            \abjad_color_music "green"
                            <a'' b''>16
                            \abjad_color_music "green"
                            e'16
                            \abjad_color_music "green"
                            <fs' gs'>4
                            ~
                            \abjad_color_music "green"
                            <fs' gs'>16
                        }
                    }   % measure
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.tuplets()[n]

    def tuplets(self):
        r"""
        Selects tuplets.

        ..  container:: example

            Selects tuplets:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = abjad.select(staff).tuplets()

                >>> for item in result:
                ...     item
                ...
                Tuplet(Multiplier(10, 9), "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16")
                Tuplet(Multiplier(8, 9), "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16")
                Tuplet(Multiplier(10, 9), "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16")

            ..  container:: example expression

                >>> selector = abjad.select().tuplets()
                >>> result = selector(staff)

                >>> selector.print(result)
                Tuplet(Multiplier(10, 9), "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16")
                Tuplet(Multiplier(8, 9), "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16")
                Tuplet(Multiplier(10, 9), "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \abjad_color_music "red"
                            r16
                            \abjad_color_music "red"
                            bf'16
                            \abjad_color_music "red"
                            <a'' b''>16
                            \abjad_color_music "red"
                            c'16
                            \abjad_color_music "red"
                            <d' e'>4
                            ~
                            \abjad_color_music "red"
                            <d' e'>16
                        }
                        \times 8/9 {
                            \abjad_color_music "blue"
                            r16
                            \abjad_color_music "blue"
                            bf'16
                            \abjad_color_music "blue"
                            <a'' b''>16
                            \abjad_color_music "blue"
                            d'16
                            \abjad_color_music "blue"
                            <e' fs'>4
                            ~
                            \abjad_color_music "blue"
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \abjad_color_music "red"
                            r16
                            \abjad_color_music "red"
                            bf'16
                            \abjad_color_music "red"
                            <a'' b''>16
                            \abjad_color_music "red"
                            e'16
                            \abjad_color_music "red"
                            <fs' gs'>4
                            ~
                            \abjad_color_music "red"
                            <fs' gs'>16
                        }
                    }   % measure
                }

        """
        from .Tuplet import Tuplet
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.components(Tuplet)

    def with_next_leaf(self):
        r"""
        Extends selection with next leaf.

        ..  container:: example

            Selects runs (each with next leaf):

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).runs()
                >>> result = result.map(abjad.select().with_next_leaf())

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Rest('r8')])
                Selection([Note("d'8"), Note("e'8"), Rest('r8')])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

            ..  container:: example expression

                >>> selector = abjad.select().runs()
                >>> selector = selector.map(abjad.select().with_next_leaf())
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Rest('r8')])
                Selection([Note("d'8"), Note("e'8"), Rest('r8')])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "red"
                    r8
                    \abjad_color_music "blue"
                    d'8
                    \abjad_color_music "blue"
                    e'8
                    \abjad_color_music "blue"
                    r8
                    \abjad_color_music "red"
                    f'8
                    \abjad_color_music "red"
                    g'8
                    \abjad_color_music "red"
                    a'8
                }

        ..  container:: example

            Selects pitched tails (each with next leaf):

            ..  container:: example

                >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> getter = abjad.select()[-1].select().with_next_leaf()
                >>> result = abjad.select(staff).logical_ties(pitched=True)
                >>> result = result.map(getter)

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Rest('r8')])
                Selection([Note("d'8"), Note("e'8")])
                Selection([Note("e'8"), Rest('r8')])
                Selection([Note("f'8")])

            ..  container:: example expression

                >>> selector = abjad.select().logical_ties(pitched=True)
                >>> selector = selector.map(getter)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Rest('r8')])
                Selection([Note("d'8"), Note("e'8")])
                Selection([Note("e'8"), Rest('r8')])
                Selection([Note("f'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "red"
                    r8
                    d'8
                    ~
                    \abjad_color_music "blue"
                    d'8
                    \abjad_color_music "blue"
                    e'8
                    ~
                    \abjad_color_music "red"
                    e'8
                    \abjad_color_music "red"
                    r8
                    \abjad_color_music "blue"
                    f'8
                }

        ..  container:: example

            Pitched logical ties (each with next leaf) is the correct selection
            for single-pitch sustain pedal applications.

            Selects pitched logical ties (each with next leaf):

            ..  container:: example

                >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = abjad.select(staff).logical_ties(pitched=True)
                >>> result = result.map(abjad.select().with_next_leaf())

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Rest('r8')])
                Selection([Note("d'8"), Note("d'8"), Note("e'8")])
                Selection([Note("e'8"), Note("e'8"), Rest('r8')])
                Selection([Note("f'8")])

            ..  container:: example expression

                >>> selector = abjad.select().logical_ties(pitched=True)
                >>> selector = selector.map(abjad.select().with_next_leaf())
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Rest('r8')])
                Selection([Note("d'8"), Note("d'8"), Note("e'8")])
                Selection([Note("e'8"), Note("e'8"), Rest('r8')])
                Selection([Note("f'8")])

                >>> for item in result:
                ...     abjad.attach(abjad.PianoPedalSpanner(), item)
                ...

                >>> selector.color(result)
                >>> manager = abjad.override(staff).sustain_pedal_line_spanner
                >>> manager.staff_padding = 6
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override SustainPedalLineSpanner.staff-padding = #6
                    autoBeaming = ##f
                }
                {
                    \set Staff.pedalSustainStyle = #'mixed
                    \abjad_color_music "red"
                    c'8
                    \sustainOn
                    \abjad_color_music "red"
                    r8
                    \sustainOff
                    \set Staff.pedalSustainStyle = #'mixed
                    \abjad_color_music "blue"
                    d'8
                    ~
                    \sustainOn
                    \abjad_color_music "blue"
                    d'8
                    \set Staff.pedalSustainStyle = #'mixed
                    \abjad_color_music "blue"
                    \abjad_color_music "red"
                    e'8
                    ~
                    \sustainOff
                    \sustainOn
                    \abjad_color_music "red"
                    e'8
                    \abjad_color_music "red"
                    r8
                    \sustainOff
                    \set Staff.pedalSustainStyle = #'mixed
                    \abjad_color_music "blue"
                    f'8
                    \sustainOn
                    \sustainOff
                }

        Returns new selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        leaves = list(self.leaves())
        next_leaf = leaves[-1]._get_leaf(1)
        if next_leaf is not None:
            leaves.append(next_leaf)
        return type(self)(leaves)

    def with_previous_leaf(self):
        r"""
        Extends selection with previous leaf.

        ..  container:: example

            Selects runs (each with previous leaf):

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> getter = abjad.select().with_previous_leaf()
                >>> result = abjad.select(staff).runs().map(getter)

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8")])
                Selection([Rest('r8'), Note("d'8"), Note("e'8")])
                Selection([Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

            ..  container:: example expression

                >>> selector = abjad.select().runs().map(getter)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8")])
                Selection([Rest('r8'), Note("d'8"), Note("e'8")])
                Selection([Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "blue"
                    r8
                    \abjad_color_music "blue"
                    d'8
                    \abjad_color_music "blue"
                    e'8
                    \abjad_color_music "red"
                    r8
                    \abjad_color_music "red"
                    f'8
                    \abjad_color_music "red"
                    g'8
                    \abjad_color_music "red"
                    a'8
                }

        ..  container:: example

            Selects pitched heads (each with previous leaf):

            ..  container:: example

                >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> getter = abjad.select()[0].select().with_previous_leaf()
                >>> result = abjad.select(staff).logical_ties(pitched=True)
                >>> result = result.map(getter)

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8")])
                Selection([Rest('r8'), Note("d'8")])
                Selection([Note("d'8"), Note("e'8")])
                Selection([Rest('r8'), Note("f'8")])

            ..  container:: example expression

                >>> selector = abjad.select().logical_ties(pitched=True)
                >>> selector = selector.map(getter)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8")])
                Selection([Rest('r8'), Note("d'8")])
                Selection([Note("d'8"), Note("e'8")])
                Selection([Rest('r8'), Note("f'8")])

                >>> selector.color(result)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad_color_music "red"
                    c'8
                    \abjad_color_music "blue"
                    r8
                    \abjad_color_music "blue"
                    d'8
                    ~
                    \abjad_color_music "red"
                    d'8
                    \abjad_color_music "red"
                    e'8
                    ~
                    e'8
                    \abjad_color_music "blue"
                    r8
                    \abjad_color_music "blue"
                    f'8
                }

        Returns new selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        leaves = list(self.leaves())
        previous_leaf = leaves[0]._get_leaf(-1)
        if previous_leaf is not None:
            leaves.insert(0, previous_leaf)
        return type(self)(leaves)
