from abjad.tools.containertools.Container._ContainerFormatter import _ContainerFormatter
from abjad.tools.componenttools._Component import _Component
import copy


class Container(_Component):
    '''Abjad model of a music container:

    ::

        abjad> container = Container("c'8 d'8 e'8 f'8")
        abjad> f(container)
        {
            c'8
            d'8
            e'8
            f'8
        }

    Return container object.
    '''

    __slots__ = ('_formatter', '_music', '_parallel', )

    def __init__(self, music = None, **kwargs):
        _Component.__init__(self)
        self._parallel = False
        self._initialize_music(music)
        self._formatter = _ContainerFormatter(self)
        self._initialize_keyword_values(**kwargs)

    ### OVERLOADS ###

    def __add__(self, expr):
        '''Concatenate containers self and expr.
        The operation c = a + b returns a new Container c with
        the content of both a and b.
        The operation is non-commutative: the content of the first
        operand will be placed before the content of the second operand.
        '''
        from abjad.tools import componenttools
        from abjad.tools import containertools
        left = componenttools.copy_components_and_fracture_crossing_spanners([self])[0]
        right = componenttools.copy_components_and_fracture_crossing_spanners([expr])[0]
        return containertools.fuse_like_named_contiguous_containers_in_expr([left, right])

    def __contains__(self, expr):
        '''True if expr is in container, otherwise False.'''
        for x in self._music:
            if x is expr:
                return True
        else:
            return False

    def __copy__(self, *args):
        new = _Component.__copy__(self, *args)
        new.is_parallel = self.is_parallel
        return new

    def __deepcopy__(self, memo):
        new = self.__copy__()
        for component in self.music:
            new_component = copy.deepcopy(component)
            new.append(new_component)
        return new

    def __delitem__(self, i):
        '''Find component(s) at index or slice 'i' in container.
        Detach component(s) from parentage.
        Withdraw component(s) from crossing spanners.
        Preserve spanners that component(s) cover(s).
        '''
        from abjad.tools.componenttools._switch_components_to_parent import _switch_components_to_parent
        from abjad.tools.spannertools._withdraw_components_in_expr_from_crossing_spanners import _withdraw_components_in_expr_from_crossing_spanners
        components = self[i]
        if not isinstance(components, list):
            components = [components]
        _withdraw_components_in_expr_from_crossing_spanners(components)
        _switch_components_to_parent(components, None)

    def __getitem__(self, i):
        '''Return component at index i in container.
        Shallow traversal of container for numeric indices only.
        '''
        return self._music[i]

    def __iadd__(self, expr):
        '''__iadd__ avoids unnecessary copying of structures.
        '''
        from abjad.tools import componenttools
        from abjad.tools import containertools
        return containertools.fuse_like_named_contiguous_containers_in_expr([self,
            componenttools.copy_components_and_fracture_crossing_spanners([expr])[0]])

    def __imul__(self, total):
        '''Multiply contents of container 'total' times.
        Return multiplied container.
        '''
        from abjad.tools import containertools
        return containertools.repeat_contents_of_container(self, total = total)

    def __len__(self):
        '''Return nonnegative integer number of components in container.
        '''
        return len(self._music)

    def __radd__(self, expr):
        '''Extend container by contents of expr to the right.
        '''
        return self + expr

    def __repr__(self):
        '''String format of container for interpreter display.
        '''
        return self._compact_representation

    def __setitem__(self, i, expr):
        '''Set 'expr' in self at nonnegative integer index i.
        Or, set 'expr' in self at slice i.
        Find spanners that dominate self[i] and children of self[i].
        Replace contents at self[i] with 'expr'.
        Reattach spanners to new contents.
        This operation leaves all score trees always in tact.
        '''
        from abjad.tools import componenttools
        from abjad.tools import spannertools
        from abjad.tools.spannertools._withdraw_components_in_expr_from_crossing_spanners import _withdraw_components_in_expr_from_crossing_spanners
        # item assignment
        if isinstance(i, int):
            assert componenttools.all_are_components([expr])
            old = self[i]
            spanners_receipt = spannertools.get_spanners_that_dominate_components([old])
            # must withdraw from spanners before parentage!
            # otherwise begin / end assessments don't work!
            _withdraw_components_in_expr_from_crossing_spanners([expr])
            expr._parentage._switch(self)
            self._music.insert(i, expr)
            componenttools.remove_component_subtree_from_score_and_spanners([old])
            for spanner, index in spanners_receipt:
                spanner._insert(index, expr)
                expr._spanners.add(spanner)
        # slice assignment
        else:
            if isinstance(expr, str):
                expr = self._parse_string(expr)[:]
            assert componenttools.all_are_components(expr)
            if i.start == i.stop and i.start is not None \
                and i.stop is not None and i.start <= -len(self):
                start, stop = 0, 0
            else:
                start, stop, stride = i.indices(len(self))
            old = self[start:stop]
            spanners_receipt = spannertools.get_spanners_that_dominate_container_components_from_to(
                self, start, stop)
            componenttools.remove_component_subtree_from_score_and_spanners(old)
            # must withdraw before setting in self!
            # otherwise circular withdraw ensues!
            _withdraw_components_in_expr_from_crossing_spanners(expr)
            # to make pychecker happy
            #self._music[start:start] = expr
            self._music.__setitem__(slice(start, start), expr)
            for component in expr:
                component._parentage._switch(self)
            for spanner, index in spanners_receipt:
                for component in reversed(expr):
                    spanner._insert(index, component)
                    component._spanners.add(spanner)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _compact_representation(self):
        '''Compact form used in spanner display.
        '''
        if not self.is_parallel:
            return '{%s}' % self._summary
        else:
            return '<<%s>>' % self._summary

    @property
    def _summary(self):
        '''Formatted summary of container contents for repr output.
        '''
        if 0 < len(self):
            return ', '.join([str(x) for x in self._music])
        else:
            #return ' '
            return ''

    ### PUBLIC ATTRIBUTES ###

    @property
    def contents_duration(self):
        from abjad.tools import durationtools
        if self.is_parallel:
            return max([durationtools.Duration(0)] + [x.preprolated_duration for x in self])
        else:
            duration = durationtools.Duration(0)
            for x in self:
                duration += x.preprolated_duration
            return duration

    @property
    def duration_in_seconds(self):
        from abjad.tools import durationtools
        if self.is_parallel:
            return max([durationtools.Duration(0)] + [x.duration_in_seconds for x in self])
        else:
            duration = durationtools.Duration(0)
            for leaf in self.leaves:
                duration += leaf.duration_in_seconds
            return duration

    @apply
    def is_parallel():
        def fget(self):
            r'''Get parallel container::

                abjad> container = Container([Voice("c'8 d'8 e'8"), Voice('g4.')])

            ::

                abjad> f(container)
                {
                    \new Voice {
                        c'8
                        d'8
                        e'8
                    }
                    \new Voice {
                        g4.
                    }
                }

            ::

                abjad> container.is_parallel
                False

            Return boolean.

            Set parallel container::

                abjad> container.is_parallel = True

            ::

                abjad> f(container)
                <<
                    \new Voice {
                        c'8
                        d'8
                        e'8
                    }
                    \new Voice {
                        g4.
                    }
                >>

            Return none.
            '''
            return self._parallel
        def fset(self, expr):
            from abjad.tools.contexttools._Context import _Context
            from abjad.tools import componenttools
            #assert isinstance(expr, (bool, type(None)))
            assert isinstance(expr, bool)
            if expr == True:
                assert componenttools.all_are_components(self._music, klasses = (_Context, ))
            self._parallel = expr
            self._mark_entire_score_tree_for_later_update('prolated')
        return property(**locals())

    @property
    def leaves(self):
        '''Read-only tuple of leaves in container::

            abjad> container = Container("c'8 d'8 e'8")

        ::

            abjad> container.leaves
            (Note("c'8"), Note("d'8"), Note("e'8"))

        Return tuple of zero or more leaves.
        '''
        from abjad.tools import leaftools
        return tuple(leaftools.iterate_leaves_forward_in_expr(self))

    @property
    def music(self):
        '''Read-only tuple of components in container::

            abjad> container = Container("c'8 d'8 e'8")

        ::

            abjad> container.music
            (Note("c'8"), Note("d'8"), Note("e'8"))

        Return tuple or zero or more components.
        '''
        return tuple(self._music)

    @property
    def preprolated_duration(self):
        return self.contents_duration

    ### PRIVATE METHODS ###

    def _initialize_music(self, music):
        from abjad.tools import componenttools
        from abjad.tools.componenttools._switch_components_to_parent import _switch_components_to_parent
        music = music or []
        if componenttools.all_are_contiguous_components_in_same_thread(music):
            parent, index, stop_index = componenttools.get_parent_and_start_stop_indices_of_components(
                music)
            self._music = list(music)
            _switch_components_to_parent(self._music, self)
            if parent is not None:
                parent._music.insert(index, self)
                self._parentage._switch(parent)
        elif isinstance(music, str):
            parsed = self._parse_string(music)
            self._music = []
            self.is_parallel = parsed.is_parallel
            if self.is_parallel:
                for x in parsed:
                    self.append(x)
            else:
                self[:] = parsed.music
        else:
            raise TypeError('can not initialize container from "%s".' % str(music))

    def _is_one_of_my_first_leaves(self, leaf):
        return leaf in self._navigator._contemporaneous_start_contents

    def _is_one_of_my_last_leaves(self, leaf):
        return leaf in self._navigator._contemporaneous_stop_contents

    def _parse_string(self, string):
        from abjad.tools.lilypondparsertools import LilyPondParser
        user_input = string.strip()
        if not user_input.startswith(('{', '\\new', '\\context')) and not user_input.endswith('}'):
            user_input = '{ %s }' % user_input
        parsed = LilyPondParser()(user_input)
        assert isinstance(parsed, Container)
        return parsed

    ### PUBLIC METHODS ###

    def append(self, component):
        r'''Append `component` to container::

            abjad> container = Container("c'8 d'8 e'8")
            abjad> beam = spannertools.BeamSpanner(container.music)

        ::

            abjad> f(container)
            {
                c'8 [
                d'8
                e'8 ]
            }

        ::

            abjad> container.append(Note("f'8"))

        ::

            abjad> f(container)
            {
                c'8 [
                d'8
                e'8 ]
                f'8
            }

        Return none.
        '''
        # to make pychecker happy
        #self[len(self):len(self)] = [component]
        self.__setitem__(slice(len(self), len(self)), [component])

    def extend(self, expr):
        '''Extend `expr` against container::

            abjad> container = Container("c'8 d'8 e'8")
            abjad> beam = spannertools.BeamSpanner(container.music)

        ::

            abjad> f(container)
            {
                c'8 [
                d'8
                e'8 ]
            }

        ::

            abjad> container.extend([Note("cs'8"), Note("ds'8"), Note("es'8")])

        ::

            abjad> f(container)
            {
                c'8 [
                d'8
                e'8 ]
                cs'8
                ds'8
                es'8
            }

        Return none.

        .. versionadded:: 2.3
            ``expr`` may now be a LilyPond input string.
        '''
        #return self
        # to make pychecker happy
        #self[len(self):len(self)] = expr[:]
        self.__setitem__(slice(len(self), len(self)), expr.__getitem__(slice(0, len(expr))))

    def index(self, component):
        '''Index `component` in container::

            abjad> container = Container("c'8 d'8 e'8")

        ::

            abjad> note = container[-1]
            abjad> note
            Note("e'8")

        ::

            abjad> container.index(note)
            2

        Return nonnegative integer.
        '''
        for i, element in enumerate(self._music):
            if element is component:
                return i
        else:
            raise ValueError('component "%s" not in Abjad container.' % component)

    def insert(self, i, component):
        '''Insert `component` in container at index `i`::

            abjad> container = Container("c'8 d'8 e'8")
            abjad> beam = spannertools.BeamSpanner(container.music)

        ::

            abjad> f(container)
            {
                c'8 [
                d'8
                e'8 ]
            }

        ::

            abjad> container.insert(1, Note("cs'8"))

        ::

            abjad> f(container)
            {
                c'8 [
                cs'8
                d'8
                e'8 ]
            }

        Return none.
        '''
        # to make pychecker happy
        #self[i:i] = [component]
        self.__setitem__(slice(i, i), [component])
        
    def pop(self, i = -1):
        '''Pop component at index `i` from container::

            abjad> container = Container("c'8 d'8 e'8")
            abjad> beam = spannertools.BeamSpanner(container.music)

        ::

            abjad> f(container)
            {
                c'8 [
                d'8
                e'8 ]
            }

        ::

            abjad> container.pop(-1)
            Note("e'8")

        ::

            abjad> f(container)
            {
                c'8 [
                d'8 ]
            }

        Return component.
        '''
        component = self[i]
        del(self[i])
        return component

    def remove(self, component):
        '''Remove `component` from container::

            abjad> container = Container("c'8 d'8 e'8")
            abjad> beam = spannertools.BeamSpanner(container.music)

        ::

            abjad> f(container)
            {
                c'8 [
                d'8
                e'8 ]
            }

        ::

            abjad> note = container[-1]
            abjad> note
            Note("e'8")

        ::

            abjad> container.remove(note)

        ::

            abjad> f(container)
            {
                c'8 [
                d'8 ]
            }

        Return none.
        '''
        i = self.index(component)
        del(self[i])
        #return component
