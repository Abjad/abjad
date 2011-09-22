from abjad.core import LilyPondContextSettingComponentPlugIn
from abjad.core import LilyPondGrobOverrideComponentPlugIn
from abjad.core import _StrictComparator
from abjad.tools import durationtools
from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface
from abjad.tools.spannertools.Spanner._SpannerOffsetInterface import _SpannerOffsetInterface
import copy


class Spanner(_StrictComparator):
    '''Any type of notation object that stretches horizontally
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

    def __init__(self, components = None):
        '''Apply spanner to components. Init dedicated duration interface.
        '''
        self._components = []
        self._contiguity_constraint = 'thread'
        self._format = _SpannerFormatInterface(self)
        self._offset = _SpannerOffsetInterface(self)
        #self._override = LilyPondGrobOverrideComponentPlugIn()
        #self._set = LilyPondContextSettingComponentPlugIn()
        self._initialize_components(components)

    ### OVERLOADS ###

    def __contains__(self, expr):
        #return self._components.__contains__(expr)
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
        return new

    # TODO: uncomment when copy regime is finished
    #__deepcopy__ = __copy__

    def __getitem__(self, expr):
        return self._components.__getitem__(expr)

    def __getnewargs__(self):
        return ()

    def __len__(self):
        return self._components.__len__()

    def __lt__(self, other):
        '''Trivial comparison to allow doctests to work.'''
        if not isinstance(other, Spanner):
            raise TypeError
        return repr(self) < repr(other)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._compact_summary)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _compact_summary(self):
        len_self = len(self)
        if not len_self:
            #return ' '
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
        for component in self:
            self._block_component(component)

    def _block_component(self, component):
        #component.spanners._spanners.remove(self)
        component._spanners.remove(self)

    # TODO: Remove call to self.leaes #
    def _duration_offset_in_me(self, leaf):
        leaves = list(self.leaves)
        assert leaf in leaves
        prev = leaves[:leaves.index(leaf)]
        return sum([leaf.prolated_duration for leaf in prev])

    def _fracture_left(self, i):
        #left = self.copy(0, i - 1)
        #left = self.copy(self[:i])
        left = self._copy(self[:i])
        #right = self.copy(i, len(self))
        #right = self.copy(self[i:])
        right = self._copy(self[i:])
        self._block_all_components()
        return self, left, right

    def _fracture_right(self, i):
        #left = self.copy(0, i)
        #left = self.copy(self[:i+1])
        left = self._copy(self[:i+1])
        #right = self.copy(i + 1, len(self))
        #right = self.copy(self[i+1:])
        right = self._copy(self[i+1:])
        self._block_all_components()
        return self, left, right

    def _fuse_by_reference(self, spanner):
        #result = self.copy()
        #result = self.copy(self[:])
        result = self._copy(self[:])
        result.extend(spanner.components)
        self._block_all_components()
        spanner._block_all_components()
        return [(self, spanner, result)]

    def _initialize_components(self, components):
        from abjad.tools.componenttools._Component import _Component
        from abjad.tools import componenttools
        from abjad.tools import leaftools
        components = components or []
        if isinstance(components, _Component):
            components = [components]
        # TODO: Author staff-level contiguity check in tools/check. #
        #         Include optional staff-level contiguity check here. #
        if self._contiguity_constraint == 'thread':
            leaves = list(leaftools.iterate_leaves_forward_in_expr(components))
            assert componenttools.all_are_thread_contiguous_components(leaves)
        self.extend(components)

    def _insert(self, i, component):
        '''Insert component in spanner at index i.
        Not composer-safe and may mangle spanners.
        '''
        component._spanners.add(self)
        self._components.insert(i, component)

    def _is_exterior_leaf(self, leaf):
        '''True if leaf is first or last in spanner.
        True if next leaf or prev leaf is None.
        False otherwise.

        .. todo:: Write Spanner._is_exterior_leaf() tests.
        '''
        if self._is_my_first_leaf(leaf):
            return True
        elif self._is_my_last_leaf(leaf):
            return True
        elif not leaf._navigator._prev_bead or not leaf._navigator._next_bead:
            return True
        else:
            return False

    def _is_my_first_leaf(self, leaf):
        from abjad.tools.spannertools.get_nth_leaf_in_spanner import get_nth_leaf_in_spanner
        # ! Full-leaf traversal extremely inefficient !
        #leaves = self.leaves
        #return leaves and leaf is leaves[0]
        try:
            first_leaf = get_nth_leaf_in_spanner(self, 0)
            return leaf is first_leaf
        except IndexError:
            return False

    def _is_my_last_leaf(self, leaf):
        from abjad.tools.spannertools.get_nth_leaf_in_spanner import get_nth_leaf_in_spanner
        # ! Full-leaf traversal extremely inefficient !
        #leaves = self.leaves
        #return leaves and leaf is leaves[-1]
        try:
            last_leaf = get_nth_leaf_in_spanner(self, -1)
            return leaf is last_leaf
        except IndexError:
            False

    def _is_my_only_leaf(self, leaf):
        return self._is_my_first_leaf(leaf) and self._is_my_last_leaf(leaf)

    # TODO: Remove call to self.leaves #
    def _is_my_first(self, leaf, klass):
        if isinstance(leaf, klass):
            leaves = list(self.leaves)
            i = leaves.index(leaf)
            for x in leaves[:i]:
                if isinstance(x, klass):
                    return False
            return True
        return False

    # TODO: Remove call to self.leaves #
    def _is_my_last(self, leaf, klass):
        if isinstance(leaf, klass):
            leaves = list(self.leaves)
            i = leaves.index(leaf)
            for x in leaves[i + 1:]:
                if isinstance(x, klass):
                    return False
            return True
        return False

    # TODO: Remove call to self.leaves #
    def _is_my_only(self, leaf, klass):
        return isinstance(leaf, klass) and len(self.leaves) == 1

    def _remove(self, component):
        '''Remove 'component' from spanner.
        Remove spanner from component's aggregator.
        Not composer-safe and may leave discontiguous spanners.
        '''
        self._sever_component(component)

    def _remove_component(self, component):
        #self._components.remove(component)
        for i, x in enumerate(self._components):
            if x is component:
                self._components.pop(i)
                break
        else:
            raise ValueError('component "%s" not in spanner components list.' % component)

    def _sever_all_components(self):
        for n in reversed(range(len(self))):
            component = self[n]
            self._sever_component(component)

    def _sever_component(self, component):
        self._block_component(component)
        self._remove_component(component)

    def _unblock_all_components(self):
        for component in self:
            self._unblock_component(component)

    def _unblock_component(self, component):
        #component.spanners._add(self)
        component._spanners.add(self)

    ### PUBLIC ATTRIBUTES ###

    @property
    def components(self):
        '''Return read-only tuple of components in spanner. ::

            abjad> voice = Voice("c'8 d'8 e'8 f'8")
            abjad> spanner = spannertools.Spanner(voice[:2])
            abjad> spanner.components
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

            abjad> voice = Voice("c'8 d'8 e'8 f'8")
            abjad> spanner = spannertools.Spanner(voice[:2])
            abjad> spanner.leaves
            (Note("c'8"), Note("d'8"))

        .. versionchanged:: 1.1
            Now returns an (immutable) tuple instead of a (mutable) list.

        .. note:: When dealing with large, complex scores accessing
            this attribute can take some time. Best to make a local
            copy with leaves = spanner.leaves first. Or use spanner-
            specific iteration tools.
        '''

        from abjad.tools.leaftools._Leaf import _Leaf
        from abjad.tools import componenttools
        result = []
        for component in self._components:
            # EXPERIMENTAL: expand to allow staff-level spanner eventually #
            for node in componenttools.iterate_components_depth_first(component):
                if isinstance(node, _Leaf):
                    result.append(node)
        result = tuple(result)
        return result

    @property
    def offset(self):
        '''.. versionadded:: 1.1

        Return read-only reference to spanner offset interface.

        Spanner offset interface implements ``start`` and ``stop`` attributes. ::

            abjad> voice = Voice("c'8 d'8 e'8 f'8")
            abjad> spanner = spannertools.Spanner(voice[2:])
            abjad> spanner
            Spanner(e'8, f'8)

        ::

            abjad> spanner._offset.start
            Offset(1, 4)

        ::

            abjad> spanner._offset.stop
            Offset(1, 2)

        Return duration.
        '''

        return self._offset

    @property
    def override(self):
        '''LilyPond grob override component plug-in.
        '''
        if not hasattr(self, '_override'):
            self._override = LilyPondGrobOverrideComponentPlugIn()
        return self._override

    @property
    def preprolated_duration(self):
        '''Sum of preprolated duration of all components in spanner.'''
        return sum([component.preprolated_duration for component in self])

    @property
    def prolated_duration(self):
        '''Sum of prolated duration of all components in spanner.'''
        return sum([component.prolated_duration for component in self])

    @property
    def set(self):
        '''LilyPond context setting component plug-in.
        '''
        if not hasattr(self, '_set'):
            self._set = LilyPondContextSettingComponentPlugIn()
        return self._set

    @property
    def written_duration(self):
        '''Sum of written duration of all components in spanner.'''
        return sum([component.written_duration for component in self])

    ### PUBLIC METHODS ###

    def append(self, component):
        '''Add `component` to right of spanner.

        ::

            abjad> voice = Voice("c'8 d'8 e'8 f'8")
            abjad> spanner = spannertools.Spanner(voice[:2])
            abjad> spanner
            Spanner(c'8, d'8)

        ::

            abjad> spanner.append(voice[2])
            abjad> spanner
            Spanner(c'8, d'8, e'8)

        Return none.
        '''

        if self._contiguity_constraint == 'thread':
            from abjad.tools import componenttools
            components = self[-1:] + [component]
            assert componenttools.all_are_thread_contiguous_components(components)
        #component.spanners._add(self)
        component._spanners.add(self)
        self._components.append(component)

    def append_left(self, component):
        '''Add `component` to left of spanner.

        ::

            abjad> voice = Voice("c'8 d'8 e'8 f'8")
            abjad> spanner = spannertools.Spanner(voice[2:])
            abjad> spanner
            Spanner(e'8, f'8)

        ::

            abjad> spanner.append_left(voice[1])
            abjad> spanner
            Spanner(d'8, e'8, f'8)

        Return none.
        '''

        from abjad.tools import componenttools
        components = [component] + self[:1]
        assert componenttools.all_are_thread_contiguous_components(components)
        #component.spanners._add(self)
        component._spanners.add(self)
        self._components.insert(0, component)

    def clear(self):
        r'''Remove all components from spanner::

            abjad> voice = Voice("c'8 d'8 e'8 f'8")
            abjad> spanner = spannertools.Spanner(voice[:])
            abjad> spanner
            Spanner(c'8, d'8, e'8, f'8)

        ::

            abjad> spanner.clear()
            abjad> spanner
            Spanner()

        Return none.
        '''

        self._sever_all_components()

    #def copy(self, start = None, stop = None):
    #def copy(self, components):
    def _copy(self, components):
        '''Return copy of spanner with `components`.

        `components` must be an iterable of components already
        contained in spanner.
        '''

        my_components = self._components[:]
        self._components = []
        result = copy.deepcopy(self)
        self._components = my_components

#      if stop is not None:
#         for component in self[start:stop + 1]:
#            result._components.append(component)
#      else:
#         for component in self:
#            result._components.append(component)

        for component in components:
            assert component in self
        for component in components:
            result._components.append(component)

        result._unblock_all_components()
        return result

    def extend(self, components):
        '''Add iterable `components` to right of spanner::

            abjad> voice = Voice("c'8 d'8 e'8 f'8")
            abjad> spanner = spannertools.Spanner(voice[:2])
            abjad> spanner
            Spanner(c'8, d'8)

        ::

            abjad> spanner.extend(voice[2:])
            abjad> spanner
            Spanner(c'8, d'8, e'8, f'8)

        Return none.
        '''

        from abjad.tools import componenttools
        input = self[-1:]
        input.extend(components)
        if self._contiguity_constraint == 'thread':
            assert componenttools.all_are_thread_contiguous_components(input)
        for component in components:
            self.append(component)

    def extend_left(self, components):
        '''Add iterable `components` to left of spanner::

            abjad> voice = Voice("c'8 d'8 e'8 f'8")
            abjad> spanner = spannertools.Spanner(voice[2:])
            abjad> spanner
            Spanner(e'8, f'8)

        ::

            abjad> spanner.extend_left(voice[:2])
            abjad> spanner
            Spanner(c'8, d'8, e'8, f'8)

        Return none.
        '''

        from abjad.tools import componenttools
        input = components + self[:1]
        assert componenttools.all_are_thread_contiguous_components(input)
        for component in reversed(components):
            self.append_left(component)

    def fracture(self, i, direction = 'both'):
        r'''Fracture spanner at `direction` of component at index `i`.

        Valid values for `direction` are ``'left'``, ``'right'`` and ``'both'``.

        Return original, left and right spanners. ::

            abjad> voice = Voice("c'8 d'8 e'8 f'8")
            abjad> beam = spannertools.BeamSpanner(voice[:])
            abjad> beam
            BeamSpanner(c'8, d'8, e'8, f'8)

        ::

            abjad> beam.fracture(1, direction = 'left')
            (BeamSpanner(c'8, d'8, e'8, f'8), BeamSpanner(c'8), BeamSpanner(d'8, e'8, f'8))

        ::

            abjad> print voice.format
            \new Voice {
                c'8 [ ]
                d'8 [
                e'8
                f'8 ]
            }

        Return tuple.
        '''

        if i < 0:
            i = len(self) + i
        if direction == 'left':
            return self._fracture_left(i)
        elif direction == 'right':
            return self._fracture_right(i)
        elif direction == 'both':
            #left = self.copy(0, i - 1)
            #left = self.copy(self[:i])
            left = self._copy(self[:i])
            #right = self.copy(i + 1, len(self))
            #right = self.copy(self[i+1:])
            right = self._copy(self[i+1:])
            #center = self.copy(i, i)
            #center = self.copy(self[i:i+1])
            center = self._copy(self[i:i+1])
            self._block_all_components()
            return self, left, center, right
        else:
            raise ValueError(
                'direction %s must be left, right or both.' % direction)

    def fuse(self, spanner):
        r'''Fuse contiguous spanners.

        Return new spanner. ::

            abjad> voice = Voice("c'8 d'8 e'8 f'8")
            abjad> left_beam = spannertools.BeamSpanner(voice[:2])
            abjad> right_beam = spannertools.BeamSpanner(voice[2:])

        ::

            abjad> print voice.format
            \new Voice {
                c'8 [
                d'8 ]
                e'8 [
                f'8 ]
            }

        ::

            abjad> left_beam.fuse(right_beam)
            [(BeamSpanner(c'8, d'8), BeamSpanner(e'8, f'8), BeamSpanner(c'8, d'8, e'8, f'8))]

        ::

            abjad> print voice.format
            \new Voice {
                c'8 [
                d'8
                e'8
                f'8 ]
            }

        .. todo:: Return (immutable) tuple instead of (mutable) list.
        '''

        return self._fuse_by_reference(spanner)

    def index(self, component):
        '''Return nonnegative integer index of `component` in spanner. ::

            abjad> voice = Voice("c'8 d'8 e'8 f'8")
            abjad> spanner = spannertools.Spanner(voice[2:])
            abjad> spanner
            Spanner(e'8, f'8)

        ::

            abjad> spanner.index(voice[-2])
            0

        Return nonnegative integer.
        '''

        #return self._components.index(component)
        for i, x in enumerate(self._components):
            if x is component:
                return i
        else:
            raise IndexError

    def pop(self):
        '''Remove and return rightmost component in spanner. ::

            abjad> voice = Voice("c'8 d'8 e'8 f'8")
            abjad> spanner = spannertools.Spanner(voice[:])
            abjad> spanner
            Spanner(c'8, d'8, e'8, f'8)

        ::

            abjad> spanner.pop()
            Note("f'8")

        ::

            abjad> spanner
            Spanner(c'8, d'8, e'8)

        Return component.
        '''

        component = self[-1]
        self._sever_component(component)
        return component

    def pop_left(self):
        '''Remove and return leftmost component in spanner. ::

            abjad> voice = Voice("c'8 d'8 e'8 f'8")
            abjad> spanner = spannertools.Spanner(voice[:])
            abjad> spanner
            Spanner(c'8, d'8, e'8, f'8)

        ::

            abjad> spanner.pop_left()
            Note("c'8")

        ::

            abjad> spanner
            Spanner(d'8, e'8, f'8)

        Return component.
        '''

        component = self[0]
        self._sever_component(component)
        return component
