import copy
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools.componenttools.Component import Component


class Container(Component):
    '''Abjad model of a music container:

    ::

        >>> container = Container("c'8 d'8 e'8 f'8")
        >>> f(container)
        {
            c'8
            d'8
            e'8
            f'8
        }

    Return container object.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_formatter', '_music', '_named_children', '_parallel', )

    _default_mandatory_input_arguments = ([], )

    ### INITIALIZER ###

    def __init__(self, music=None, **kwargs):
        Component.__init__(self)
        self._named_children = {}
        self._parallel = False
        self._initialize_music(music)
        self._initialize_keyword_values(**kwargs)

    ### SPECIAL METHODS ###

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
        new = Component.__copy__(self, *args)
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
        from abjad.tools.componenttools._switch_components_to_parent import \
            _switch_components_to_parent
        from abjad.tools.spannertools._withdraw_components_in_expr_from_crossing_spanners import \
            _withdraw_components_in_expr_from_crossing_spanners
        components = self[i]
        if not isinstance(components, list):
            components = [components]
        _withdraw_components_in_expr_from_crossing_spanners(components)
        _switch_components_to_parent(components, None)

    def __getitem__(self, i):
        '''Return component at index i in container.
        Shallow traversal of container for numeric indices only.
        '''
        if isinstance(i, (int, slice)):
            return self._music[i]
        elif isinstance(i, str):
            if i not in self._named_children:
                raise MissingNamedComponentError
            elif 1 < len(self._named_children[i]):
                raise ExtraNamedComponentError
            return self._named_children[i][0]
        raise ValueError

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
        return containertools.repeat_contents_of_container(self, total=total)

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
        from abjad.tools import gracetools
        from abjad.tools import spannertools
        from abjad.tools.spannertools._withdraw_components_in_expr_from_crossing_spanners import \
            _withdraw_components_in_expr_from_crossing_spanners
        # item assignment
        if isinstance(i, int):
            if isinstance(expr, str):
                expr = self._parse_string(expr)[:]
                assert len(expr) == 1
                expr = expr[0]
            assert componenttools.all_are_components([expr])
            if any([isinstance(x, gracetools.GraceContainer) for x in [expr]]):
                raise GraceContainerError('must attach grace container to note or chord.')
            old = self[i]
            spanners_receipt = spannertools.get_spanners_that_dominate_components([old])
            # must withdraw from spanners before parentage!
            # otherwise begin / end assessments don't work!
            _withdraw_components_in_expr_from_crossing_spanners([expr])
            expr._switch(self)
            self._music.insert(i, expr)
            componenttools.remove_component_subtree_from_score_and_spanners([old])
            for spanner, index in spanners_receipt:
                spanner._insert(index, expr)
                expr._spanners.add(spanner)
        # slice assignment
        else:
            if isinstance(expr, str):
                expr = self._parse_string(expr)[:]
            elif isinstance(expr, list) and len(expr) == 1 and isinstance(expr[0], str):
                expr = self._parse_string(expr[0])[:]
            assert componenttools.all_are_components(expr)
            if any([isinstance(x, gracetools.GraceContainer) for x in expr]):
                raise GraceContainerError('must attach grace container to note or chord.')
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
                component._switch(self)
            for spanner, index in spanners_receipt:
                for component in reversed(expr):
                    spanner._insert(index, component)
                    component._spanners.add(spanner)

    ### READ-ONLY PRIVATE PROPERTIES ###

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
            return ''

    ### PRIVATE METHODS ###

    def _format_content_pieces(self):
        result = []
        for m in self._music:
            result.extend(m.lilypond_format.split('\n'))
        result = ['\t' + x for x in result]
        return result
        
    def _format_before_slot(self, format_contributions):
        result = []
        result.append(('comments', format_contributions.get('before', {}).get('comments', [])))
        result.append(('lilypond command marks', format_contributions.get('before', {}).get('lilypond command marks', [])))
        #result.append(formattools.get_comment_format_contributions_for_slot(self, 'before'))
        #result.append(formattools.get_lilypond_command_mark_format_contributions_for_slot(self, 'before'))
        return tuple(result)

    def _format_open_brackets_slot(self, format_contributions):
        result = []
        if self.is_parallel:
            brackets_open = ['<<']
        else:
            brackets_open = ['{']
        result.append([('open brackets', ''), brackets_open])
        return tuple(result)

    def _format_opening_slot(self, format_contributions):
        result = []
        result.append(('comments', format_contributions.get('opening', {}).get('comments', [])))
        result.append(('lilypond command marks', format_contributions.get('opening', {}).get('lilypond command marks', [])))
        result.append(('grob overrides', format_contributions.get('grob overrides', [])))
        result.append(('context settings', format_contributions.get('context settings', [])))
        #result.append(formattools.get_comment_format_contributions_for_slot(self, 'opening'))
        #result.append(formattools.get_lilypond_command_mark_format_contributions_for_slot(self, 'opening'))
        #result.append(formattools.get_grob_override_format_contributions(self))
        #result.append(formattools.get_context_setting_format_contributions(self))
        return self._format_slot_contributions_with_indent(result)

    def _format_contents_slot(self, format_contributions):
        result = []
        result.append([('contents', '_contents'), self._format_content_pieces()])
        return tuple(result)

    def _format_closing_slot(self, format_contributions):
        result = []
        result.append(('grob reverts', format_contributions.get('grob reverts', [])))
        result.append(('lilypond command marks', format_contributions.get('closing', {}).get('lilypond command marks', [])))
        result.append(('comments', format_contributions.get('closing', {}).get('comments', [])))
        #result.append(formattools.get_grob_revert_format_contributions(self))
        #result.append(formattools.get_lilypond_command_mark_format_contributions_for_slot(self, 'closing'))
        #result.append(formattools.get_comment_format_contributions_for_slot(self, 'closing'))
        return self._format_slot_contributions_with_indent(result)

    def _format_close_brackets_slot(self, format_contributions):
        result = []
        if self.is_parallel:
            brackets_close = ['>>']
        else:
            brackets_close = ['}']
        result.append([('close brackets', ''), brackets_close])
        return tuple(result)

    def _format_after_slot(self, format_contributions):
        result = []
        result.append(('lilypond command marks', format_contributions.get('after', {}).get('lilypond command marks', [])))
        result.append(('comments', format_contributions.get('after', {}).get('comments', [])))
        #result.append(formattools.get_lilypond_command_mark_format_contributions_for_slot(self, 'after'))
        #result.append(formattools.get_comment_format_contributions_for_slot(self, 'after'))
        return tuple(result)

    def _format_slot_contributions_with_indent(self, slot):
        result = []
        for contributor, contributions in slot:
            result.append((contributor, tuple(['\t' + x for x in contributions])))
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def contents_duration(self):
        if self.is_parallel:
            return max([durationtools.Duration(0)] + [x.preprolated_duration for x in self])
        else:
            duration = durationtools.Duration(0)
            for x in self:
                duration += x.preprolated_duration
            return duration

    @property
    def duration_in_seconds(self):
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

                >>> container = Container([Voice("c'8 d'8 e'8"), Voice('g4.')])

            ::

                >>> f(container)
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

                >>> container.is_parallel
                False

            Return boolean.

            Set parallel container::

                >>> container.is_parallel = True

            ::

                >>> f(container)
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
            from abjad.tools.contexttools.Context import Context
            from abjad.tools import componenttools
            #assert isinstance(expr, (bool, type(None)))
            assert isinstance(expr, bool)
            if expr == True:
                assert componenttools.all_are_components(self._music, klasses=(Context, ))
            self._parallel = expr
            self._mark_entire_score_tree_for_later_update('prolated')
        return property(**locals())

    @property
    def leaves(self):
        '''Read-only tuple of leaves in container::

            >>> container = Container("c'8 d'8 e'8")

        ::

            >>> container.leaves
            (Note("c'8"), Note("d'8"), Note("e'8"))

        Return tuple of zero or more leaves.
        '''
        from abjad.tools import iterationtools
        return tuple(iterationtools.iterate_leaves_in_expr(self))

    @property
    def music(self):
        '''Read-only tuple of components in container::

            >>> container = Container("c'8 d'8 e'8")

        ::

            >>> container.music
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
        if music is None:
            music = []
        if componenttools.all_are_contiguous_components_in_same_thread(music):
            parent, index, stop_index = componenttools.get_parent_and_start_stop_indices_of_components(
                music)
            self._music = list(music)
            _switch_components_to_parent(self._music, self)
            if parent is not None:
                parent._music.insert(index, self)
                self._switch(parent)
        elif isinstance(music, str):
            parsed = self._parse_string(music)
            self._music = []
            self.is_parallel = parsed.is_parallel
            if parsed.is_parallel or not componenttools.all_are_thread_contiguous_components(parsed[:]):
                while len(parsed):
                    self.append(parsed.pop(0))
            else:
                self[:] = parsed[:]
        else:
            raise TypeError('can not initialize container from "%s".' % str(music))

    def _is_one_of_my_first_leaves(self, leaf):
        from abjad.tools import componenttools
        return leaf in componenttools.get_improper_descendents_of_component_that_start_with_component(self)

    def _is_one_of_my_last_leaves(self, leaf):
        from abjad.tools import componenttools
        return leaf in componenttools.get_improper_descendents_of_component_that_stop_with_component(self)

    def _parse_string(self, string):
        from abjad.tools import lilypondparsertools
        from abjad.tools import rhythmtreetools
        user_input = string.strip()
        if user_input.startswith('abj:'):
            parsed = lilypondparsertools.parse_reduced_ly_syntax(user_input.partition('abj:')[-1])
        elif user_input.startswith('rtm:'):
            parsed = rhythmtreetools.parse_rtm_syntax(user_input.partition('rtm:')[-1])
        else:
            if not user_input.startswith('<<') and not user_input.endswith('>>'):
                user_input = '{ %s }' % user_input
            parsed = lilypondparsertools.LilyPondParser()(user_input)
            assert isinstance(parsed, Container)
        return parsed

    ### PUBLIC METHODS ###

    def append(self, component):
        r'''Append `component` to container::

            >>> container = Container("c'8 d'8 e'8")
            >>> beam = beamtools.BeamSpanner(container.music)

        ::

            >>> f(container)
            {
                c'8 [
                d'8
                e'8 ]
            }

        ::

            >>> container.append(Note("f'8"))

        ::

            >>> f(container)
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

            >>> container = Container("c'8 d'8 e'8")
            >>> beam = beamtools.BeamSpanner(container.music)

        ::

            >>> f(container)
            {
                c'8 [
                d'8
                e'8 ]
            }

        ::

            >>> container.extend([Note("cs'8"), Note("ds'8"), Note("es'8")])

        ::

            >>> f(container)
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

            >>> container = Container("c'8 d'8 e'8")

        ::

            >>> note = container[-1]
            >>> note
            Note("e'8")

        ::

            >>> container.index(note)
            2

        Return nonnegative integer.
        '''
        for i, element in enumerate(self._music):
            if element is component:
                return i
        else:
            raise ValueError('component {!r} not in Abjad container {!r}.'.format(component, self))

    def insert(self, i, component):
        '''Insert `component` in container at index `i`::

            >>> container = Container("c'8 d'8 e'8")
            >>> beam = beamtools.BeamSpanner(container.music)

        ::

            >>> f(container)
            {
                c'8 [
                d'8
                e'8 ]
            }

        ::

            >>> container.insert(1, Note("cs'8"))

        ::

            >>> f(container)
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
        
    def pop(self, i=-1):
        '''Pop component at index `i` from container::

            >>> container = Container("c'8 d'8 e'8")
            >>> beam = beamtools.BeamSpanner(container.music)

        ::

            >>> f(container)
            {
                c'8 [
                d'8
                e'8 ]
            }

        ::

            >>> container.pop(-1)
            Note("e'8")

        ::

            >>> f(container)
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

            >>> container = Container("c'8 d'8 e'8")
            >>> beam = beamtools.BeamSpanner(container.music)

        ::

            >>> f(container)
            {
                c'8 [
                d'8
                e'8 ]
            }

        ::

            >>> note = container[-1]
            >>> note
            Note("e'8")

        ::

            >>> container.remove(note)

        ::

            >>> f(container)
            {
                c'8 [
                d'8 ]
            }

        Return none.
        '''
        i = self.index(component)
        del(self[i])
        #return component
