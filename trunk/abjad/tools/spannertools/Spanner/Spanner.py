import copy
import abc
from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import lilypondproxytools
from abjad.tools.abctools import AbjadObject


class Spanner(AbjadObject):
    '''.. versionadded:: 1.1

    Any type of notation object that stretches horizontally
    and encompasses some number of notes, rest, chords, tuplets,
    measures, voices or other Abjad components.

    Beams, slurs, hairpins, trills, glissandi and piano pedal brackets
    all stretch horizontally on the page to encompass multiple notes
    and all implement as Abjad spanners.
    That is, these spanner all have an obvious graphic reality with
    definite start-, stop- and midpoints.

    Abjad also implements a number of spanners of a different type,
    such as tempo and instrument spanners, which mark a group of notes,
    rests, chords or measues as carrying a certain tempo or being
    played by a certain instrument.

    The spanner class described here
    abstracts the functionality that all such spanners, both graphic
    and nongraphics, share.
    This shared functionality includes methods to add, remove, inspect
    and test components governed by the spanner, as well as basic
    formatting properties.
    The other spanner classes, such as beam and glissando, all inherit from
    this class and receive the functionality implemented here.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, components=None):
        self._components = []
        self._contiguity_constraint = 'thread'
        self._initialize_components(components)

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''.. versionadded:: 2.9

        Call spanner on `expr` as a shortcut to extend spanner::

            >>> staff = Staff("c'8 d'8 e'8 f'8")

        ::

            >>> beam = beamtools.BeamSpanner()
            >>> beam(staff[:])
            BeamSpanner(c'8, d'8, e'8, f'8)

        ::

            >>> f(staff)
            \new Staff {
                c'8 [
                d'8
                e'8
                f'8 ]
            }

        The method is provided as an experimental way of unifying 
        spanner and mark attachment syntax.

        Return spanner.
        '''
        self.extend(expr)
        return self

    def __contains__(self, expr):
        for x in self._components:
            if x is expr:
                return True
        else:
            return False

    def __copy__(self, *args):
        new = type(self)(*self.__getnewargs__())
        if getattr(self, '_override', None) is not None:
            new._override = copy.copy(self.override)
        if getattr(self, '_set', None) is not None:
            new._set = copy.copy(self.set)
        self._copy_keyword_args(new)
        return new

    __deepcopy__ = __copy__

    def __getitem__(self, expr):
        return self._components.__getitem__(expr)

    def __getnewargs__(self):
        return ()

    def __len__(self):
        return self._components.__len__()

    def __lt__(self, other):
        '''Trivial comparison to allow doctests to work.
        '''
        if not isinstance(other, Spanner):
            raise TypeError
        return repr(self) < repr(other)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._compact_summary)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _compact_summary(self):
        len_self = len(self)
        if not len_self:
            return ''
        elif 0 < len_self <= 8:
            return ', '.join([x._compact_representation for x in self])
        else:
            left = ', '.join([x._compact_representation for x in self[:2]])
            right = ', '.join([x._compact_representation for x in self[-2:]])
            number_in_middle = len_self - 4
            middle = ', ... [%s] ..., ' % number_in_middle
            return left + middle + right

    @property
    def _summary(self):
        if 0 < len(self):
            return ', '.join([str(x) for x in self])
        else:
            return ' '

    ### PRIVATE METHODS ###

    def _block_all_components(self):
        '''Not composer-safe.
        '''
        for component in self:
            self._block_component(component)

    def _block_component(self, component):
        '''Not composer-safe.
        '''
        component._spanners.remove(self)

    def _copy(self, components):
        '''Return copy of spanner with components.
        Components must be an iterable of components already contained in spanner.
        '''
        my_components = self._components[:]
        self._components = []
        result = copy.deepcopy(self)
        self._components = my_components
        for component in components:
            assert component in self
        for component in components:
            result._components.append(component)
        result._unblock_all_components()
        return result

    @abc.abstractmethod
    def _copy_keyword_args(self, new):
        raise NotImplemented

    def _duration_offset_in_me(self, leaf):
        return leaf.start_offset - self.start_offset

    def _format_after_leaf(self, leaf):
        result = []
        if self._is_my_last_leaf(leaf):
            result.extend(getattr(self, '_reverts', []))
        return result

    def _format_before_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.extend(getattr(self, '_overrides', []))
        return result

    def _format_right_of_leaf(self, leaf):
        result = []
        return result

    def _fracture_left(self, i):
        left = self._copy(self[:i])
        right = self._copy(self[i:])
        self._block_all_components()
        return self, left, right

    def _fracture_right(self, i):
        left = self._copy(self[:i+1])
        right = self._copy(self[i+1:])
        self._block_all_components()
        return self, left, right

    def _fuse_by_reference(self, spanner):
        result = self._copy(self[:])
        result.extend(spanner.components)
        self._block_all_components()
        spanner._block_all_components()
        return [(self, spanner, result)]

    def _initialize_components(self, components):
        from abjad.tools import iterationtools
        if isinstance(components, componenttools.Component):
            components = [components]
        elif not components:
            components = []
        # TODO: Author staff-level contiguity check in tools/check.
        #       Include optional staff-level contiguity check here.
        if self._contiguity_constraint == 'thread':
            leaves = list(iterationtools.iterate_leaves_in_expr(components))
            assert componenttools.all_are_thread_contiguous_components(leaves)
        self.extend(components)

    def _insert(self, i, component):
        '''Insert component in spanner at index i.
        Not composer-safe and may mangle spanners.
        '''
        component._spanners.add(self)
        self._components.insert(i, component)

    # TODO: author tests.
    def _is_exterior_leaf(self, leaf):
        '''True if leaf is first or last in spanner.
        True if next leaf or prev leaf is none.
        False otherwise.
        '''
        if self._is_my_first_leaf(leaf):
            return True
        elif self._is_my_last_leaf(leaf):
            return True
        elif not leaftools.get_nth_leaf_in_thread_from_leaf(leaf, -1) and \
            not leaftools.get_nth_leaf_in_thread_from_leaf(leaf, 1):
            return True
        else:
            return False

    def _is_my_first(self, leaf, klass):
        from abjad.tools import spannertools
        for component in spannertools.iterate_components_in_spanner(self, klass=klass):
            if component is leaf:
                return True
            else:
                return False

    def _is_my_first_leaf(self, leaf):
        from abjad.tools import spannertools
        try:
            first_leaf = spannertools.get_nth_leaf_in_spanner(self, 0)
            return leaf is first_leaf
        except IndexError:
            return False

    def _is_my_last(self, leaf, klass):
        from abjad.tools import spannertools
        components = spannertools.iterate_components_in_spanner(self, klass=klass, reverse=True)
        for component in components:
            if component is leaf:
                return True
            else:
                return False

    def _is_my_last_leaf(self, leaf):
        from abjad.tools import spannertools
        try:
            last_leaf = spannertools.get_nth_leaf_in_spanner(self, -1)
            return leaf is last_leaf
        except IndexError:
            return False

    def _is_my_only(self, leaf, klass):
        from abjad.tools import spannertools
        i, components = None, spannertools.iterate_components_in_spanner(self, klass=klass)
        for i, component in enumerate(components):
            if 0 < i:
                return False
        return i == 0

    def _is_my_only_leaf(self, leaf):
        return self._is_my_first_leaf(leaf) and self._is_my_last_leaf(leaf)

    def _remove(self, component):
        '''Remove 'component' from spanner.
        Remove spanner from component's aggregator.
        Not composer-safe and may leave discontiguous spanners.
        '''
        self._sever_component(component)

    def _remove_component(self, component):
        '''Not composer-safe.
        '''
        for i, x in enumerate(self._components):
            if x is component:
                self._components.pop(i)
                break
        else:
            raise ValueError('component "{}" not in spanner components list.'.format(component))

    def _reverse_components(self):
        r'''Reverse order of spanner components.

        Not composer-safe because reversing the order of spanner components
        could scramble components of some other spanner.

        Call method only as part of a full component- and spanner-reversal routine.

        Spanner subclasses with mapping variables (like the 'durations' list
        attaching to durated complex beam spanners) should override this method
        to reverse mapping elements.
        '''
        self._components.reverse()

    def _sever_all_components(self):
        '''Not composer-safe.
        '''
        for n in reversed(range(len(self))):
            component = self[n]
            self._sever_component(component)

    def _sever_component(self, component):
        '''Not composer-safe.
        '''
        self._block_component(component)
        self._remove_component(component)

    def _unblock_all_components(self):
        '''Not composer-safe.
        '''
        for component in self:
            self._unblock_component(component)

    def _unblock_component(self, component):
        '''Not composer-safe.
        '''
        component._spanners.add(self)

    ### PUBLIC PROPERTIES ###

    @property
    def components(self):
        '''Return read-only tuple of components in spanner. ::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> spanner = beamtools.BeamSpanner(voice[:2])
            >>> spanner.components
            (Note("c'8"), Note("d'8"))

        .. versionchanged:: 1.1
            Now returns an (immutable) tuple instead of a (mutable) list.
        '''
        return tuple(self._components[:])

    @property
    def duration_in_seconds(self):
        '''Sum of duration of all leaves in spanner, in seconds.'''
        duration = durationtools.Duration(0)
        for leaf in self.leaves:
            duration += leaf.duration_in_seconds
        return duration

    @property
    def leaves(self):
        '''Return read-only tuple of leaves in spanner. ::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> spanner = beamtools.BeamSpanner(voice[:2])
            >>> spanner.leaves
            (Note("c'8"), Note("d'8"))

        .. note:: When dealing with large, complex scores accessing
            this attribute can take some time. Best to make a local
            copy with leaves = spanner.leaves first. Or use spanner-
            specific iteration tools.
        '''
        from abjad.tools import iterationtools
        result = []
        for component in self._components:
            # EXPERIMENTAL: expand to allow staff-level spanner eventually #
            for node in iterationtools.iterate_components_depth_first(component):
                if isinstance(node, leaftools.Leaf):
                    result.append(node)
        result = tuple(result)
        return result

    @property
    def override(self):
        '''LilyPond grob override component plug-in.
        '''
        if not hasattr(self, '_override'):
            self._override = lilypondproxytools.LilyPondGrobOverrideComponentPlugIn()
        return self._override

    @property
    def preprolated_duration(self):
        '''Sum of preprolated duration of all components in spanner.
        '''
        return sum([component.preprolated_duration for component in self])

    @property
    def prolated_duration(self):
        '''Sum of prolated duration of all components in spanner.
        '''
        return sum([component.prolated_duration for component in self])

    @property
    def set(self):
        '''LilyPond context setting component plug-in.
        '''
        if not hasattr(self, '_set'):
            self._set = lilypondproxytools.LilyPondContextSettingComponentPlugIn()
        return self._set

    @property
    def start_offset(self):
        '''Read-only start offset of spanner.
        '''
        if len(self):
            return self[0].start_offset
        else:
            return Duration(0)

    @property
    def stop_offset(self):
        '''Read-only stop offset of spanner.
        '''
        if len(self):
            return self[-1].stop_offset
        else:
            return Duration(0)

    @property
    def written_duration(self):
        '''Sum of written duration of all components in spanner.
        '''
        return sum([component.written_duration for component in self])

    ### PUBLIC METHODS ###

    def append(self, component):
        '''Add `component` to right of spanner.

        ::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> spanner = beamtools.BeamSpanner(voice[:2])
            >>> spanner
            BeamSpanner(c'8, d'8)

        ::

            >>> spanner.append(voice[2])
            >>> spanner
            BeamSpanner(c'8, d'8, e'8)

        Return none.
        '''
        if self._contiguity_constraint == 'thread':
            components = self[-1:] + [component]
            assert componenttools.all_are_thread_contiguous_components(components)
        component._spanners.add(self)
        self._components.append(component)

    def append_left(self, component):
        '''Add `component` to left of spanner.

        ::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> spanner = beamtools.BeamSpanner(voice[2:])
            >>> spanner
            BeamSpanner(e'8, f'8)

        ::

            >>> spanner.append_left(voice[1])
            >>> spanner
            BeamSpanner(d'8, e'8, f'8)

        Return none.
        '''
        components = [component] + self[:1]
        assert componenttools.all_are_thread_contiguous_components(components)
        component._spanners.add(self)
        self._components.insert(0, component)

    def clear(self):
        r'''Remove all components from spanner::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> spanner = beamtools.BeamSpanner(voice[:])
            >>> spanner
            BeamSpanner(c'8, d'8, e'8, f'8)

        ::

            >>> spanner.clear()
            >>> spanner
            BeamSpanner()

        Return none.
        '''
        self._sever_all_components()

    def extend(self, components):
        '''Add iterable `components` to right of spanner::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> spanner = beamtools.BeamSpanner(voice[:2])
            >>> spanner
            BeamSpanner(c'8, d'8)

        ::

            >>> spanner.extend(voice[2:])
            >>> spanner
            BeamSpanner(c'8, d'8, e'8, f'8)

        Return none.
        '''
        component_input = self[-1:]
        component_input.extend(components)
        if self._contiguity_constraint == 'thread':
            assert componenttools.all_are_thread_contiguous_components(component_input)
        for component in components:
            self.append(component)

    def extend_left(self, components):
        '''Add iterable `components` to left of spanner::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> spanner = beamtools.BeamSpanner(voice[2:])
            >>> spanner
            BeamSpanner(e'8, f'8)

        ::

            >>> spanner.extend_left(voice[:2])
            >>> spanner
            BeamSpanner(c'8, d'8, e'8, f'8)

        Return none.
        '''
        component_input = components + self[:1]
        assert componenttools.all_are_thread_contiguous_components(component_input)
        for component in reversed(components):
            self.append_left(component)

    def fracture(self, i, direction=None):
        r'''Fracture spanner at `direction` of component at index `i`.

        Valid values for `direction` are ``Left``, ``Right`` and ``None``.

        Return original, left and right spanners. ::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> beam = beamtools.BeamSpanner(voice[:])
            >>> beam
            BeamSpanner(c'8, d'8, e'8, f'8)

        ::

            >>> beam.fracture(1, direction=Left)
            (BeamSpanner(c'8, d'8, e'8, f'8), BeamSpanner(c'8), BeamSpanner(d'8, e'8, f'8))

        ::

            >>> print voice.lilypond_format
            \new Voice {
                c'8 [ ]
                d'8 [
                e'8
                f'8 ]
            }

        Set `direction=None` to fracture on both left and right sides.

        Return tuple.
        '''
        if i < 0:
            i = len(self) + i
        if direction == Left:
            return self._fracture_left(i)
        elif direction == Right:
            return self._fracture_right(i)
        elif direction is None:
            left = self._copy(self[:i])
            right = self._copy(self[i+1:])
            center = self._copy(self[i:i+1])
            self._block_all_components()
            return self, left, center, right
        else:
            raise ValueError('direction {!r} must be Left, Right or None.'.format(direction))

    def fuse(self, spanner):
        r'''Fuse contiguous spanners.

        Return new spanner. ::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> left_beam = beamtools.BeamSpanner(voice[:2])
            >>> right_beam = beamtools.BeamSpanner(voice[2:])

        ::

            >>> print voice.lilypond_format
            \new Voice {
                c'8 [
                d'8 ]
                e'8 [
                f'8 ]
            }

        ::

            >>> left_beam.fuse(right_beam)
            [(BeamSpanner(c'8, d'8), BeamSpanner(e'8, f'8), BeamSpanner(c'8, d'8, e'8, f'8))]

        ::

            >>> print voice.lilypond_format
            \new Voice {
                c'8 [
                d'8
                e'8
                f'8 ]
            }

        Return list.
        '''
        return self._fuse_by_reference(spanner)

    def index(self, component):
        '''Return nonnegative integer index of `component` in spanner::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> spanner = beamtools.BeamSpanner(voice[2:])
            >>> spanner
            BeamSpanner(e'8, f'8)

        ::

            >>> spanner.index(voice[-2])
            0

        Return nonnegative integer.
        '''
        for i, x in enumerate(self._components):
            if x is component:
                return i
        else:
            raise IndexError

    def pop(self):
        '''Remove and return rightmost component in spanner::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> spanner = beamtools.BeamSpanner(voice[:])
            >>> spanner
            BeamSpanner(c'8, d'8, e'8, f'8)

        ::

            >>> spanner.pop()
            Note("f'8")

        ::

            >>> spanner
            BeamSpanner(c'8, d'8, e'8)

        Return component.
        '''
        component = self[-1]
        self._sever_component(component)
        return component

    def pop_left(self):
        '''Remove and return leftmost component in spanner::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> spanner = beamtools.BeamSpanner(voice[:])
            >>> spanner
            BeamSpanner(c'8, d'8, e'8, f'8)

        ::

            >>> spanner.pop_left()
            Note("c'8")

        ::

            >>> spanner
            BeamSpanner(d'8, e'8, f'8)

        Return component.
        '''
        component = self[0]
        self._sever_component(component)
        return component
