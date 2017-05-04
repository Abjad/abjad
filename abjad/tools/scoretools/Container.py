# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import systemtools
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.scoretools.Component import Component


class Container(Component):
    r'''A container.

    ..  container:: example

        Intializes from string:

        ::

            >>> container = Container("c'4 e'4 d'4 e'8 f'8")
            >>> show(container) # doctest: +SKIP

        ..  doctest::

            >>> f(container)
            {
                c'4
                e'4
                d'4
                e'8
                f'8
            }

    ..  container:: example

        Intializes from components:

        ::

            >>> notes = [
            ...     Note("c'4"),
            ...     Note("e'4"),
            ...     Note("d'4"),
            ...     Note("e'8"),
            ...     Note("f'8"),
            ...     ]
            >>> container = Container(notes)
            >>> show(container) # doctest: +SKIP

        ..  doctest::

            >>> f(container)
            {
                c'4
                e'4
                d'4
                e'8
                f'8
            }

    ..  container:: example

        Intializes from selections:

        ::

            >>> notes = [
            ...     Note("c'4"),
            ...     Note("e'4"),
            ...     Note("d'4"),
            ...     Note("e'8"),
            ...     Note("f'8"),
            ...     ]
            >>> selection = select(notes)
            >>> container = Container(selection)
            >>> show(container) # doctest: +SKIP

        ..  doctest::

            >>> f(container)
            {
                c'4
                e'4
                d'4
                e'8
                f'8
            }

    ..  container:: example

        Intializes from mixed components and selections:

        ::

            >>> items = [
            ...     Note("c'4"),
            ...     select(Note("e'4")),
            ...     select(Note("d'4")),
            ...     Note("e'8"),
            ...     Note("f'8"),
            ...     ]
            >>> container = Container(items)
            >>> show(container) # doctest: +SKIP

        ..  doctest::

            >>> f(container)
            {
                c'4
                e'4
                d'4
                e'8
                f'8
            }

    ..  container:: example

        Containers are iterables:

        ::

            >>> import collections
            >>> container = Container("c'4 e'4 d'4 e'8 f'8")
            >>> isinstance(container, collections.Iterable)
            True

    ..  container:: example

        Containers are not sequences because containers do not implement
        reverse:

        ::

            >>> container = Container("c'4 e'4 d'4 e'8 f'8")
            >>> isinstance(container, collections.Sequence)
            False

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = (
        '_formatter',
        '_music',
        '_named_children',
        '_name',
        '_is_simultaneous',
        )

    ### INITIALIZER ###

    def __init__(self, music=None, is_simultaneous=None, name=None):
        music = music or []
        Component.__init__(self, name=name)
        self._named_children = {}
        self._is_simultaneous = False
        self._initialize_music(music)
        self.is_simultaneous = is_simultaneous

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        r'''Is true when `argument` appears in container.
        Otherwise false.

        Returns true or false.
        '''
        if isinstance(argument, str):
            return argument in self._named_children
        else:
            for x in self._music:
                if x is argument:
                    return True
            else:
                return False

    def __delitem__(self, i):
        r'''Deletes components(s) at index `i` in container.

        ..  container:: example

            Deletes first tuplet in voice:

            ::

                >>> voice = Voice()
                >>> voice.append(Tuplet((2, 3), "c'4 d'4 e'4"))
                >>> voice.append(Tuplet((2, 3), "e'4 d'4 c'4"))
                >>> leaves = iterate(voice).by_leaf()
                >>> attach(Slur(), list(leaves))
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    \times 2/3 {
                        c'4 (
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        e'4
                        d'4
                        c'4 )
                    }
                }

            ::

                >>> tuplet_1 = voice[0]
                >>> del(voice[0])

            First tuplet no longer appears in voice:

                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    \times 2/3 {
                        e'4 (
                        d'4
                        c'4 )
                    }
                }

            ::

                >>> inspect_(voice).is_well_formed()
                True

            First tuplet is no longer slurred but is still well-formed:

            ::

                >>> show(tuplet_1) # doctest: +SKIP

            ..  doctest::

                >>> f(tuplet_1)
                \times 2/3 {
                    c'4
                    d'4
                    e'4
                }

            ::

                >>> inspect_(tuplet_1).is_well_formed()
                True

        Withdraws component(s) from crossing spanners.

        Preserves spanners that component(s) cover(s).

        Returns none.
        '''
        components = self[i]
        if not isinstance(components, selectiontools.Selection):
            components = selectiontools.Selection([components])
        if not self.is_simultaneous:
            components._withdraw_from_crossing_spanners()
        components._set_parents(None)

    def __getitem__(self, argument):
        r'''Gets item or slice identified by `argument`.

        Traverses top-level items only.

        Returns component.
        '''
        if isinstance(argument, int):
            return self._music.__getitem__(argument)
        elif isinstance(argument, slice) and not self.is_simultaneous:
            return selectiontools.Selection(self._music.__getitem__(argument))
        elif isinstance(argument, slice) and self.is_simultaneous:
            return selectiontools.Selection(self._music.__getitem__(argument))
        elif isinstance(argument, str):
            if argument not in self._named_children:
                message = 'can not find component named {!r}.'
                message = message.format(argument)
                raise ValueError(message)
            elif 1 < len(self._named_children.__getitem__(argument)):
                message = 'multiple components named {!r}.'
                message = message.format(argument)
                raise ValueError(message)
            return self._named_children.__getitem__(argument)[0]
        message = 'can not get container at {!r}.'
        message = message.format(argument)
        raise ValueError(message)

    def __graph__(self, spanner=None, **keywords):
        r'''Graphviz graph representation of container.

        Returns Graphviz graph.
        '''
        def recurse(component, leaf_cluster):
            component_node = component._as_graphviz_node()
            node_mapping[component] = component_node
            node_order = [component_node.name]
            if isinstance(component, scoretools.Container):
                graph.append(component_node)
                this_leaf_cluster = graphtools.GraphvizSubgraph(
                    name=component_node.name,
                    attributes={
                        'color': 'grey75',
                        'penwidth': 2,
                        },
                    )
                all_are_leaves = True
                pending_node_order = []
                for child in component:
                    if not isinstance(child, scoretools.Leaf):
                        all_are_leaves = False
                    child_node, child_node_order = recurse(
                        child, this_leaf_cluster)
                    pending_node_order.extend(child_node_order)
                    edge = graphtools.GraphvizEdge()
                    edge.attach(component_node, child_node)
                if all_are_leaves:
                    pending_node_order.reverse()
                node_order.extend(pending_node_order)
                if len(this_leaf_cluster):
                    leaf_cluster.append(this_leaf_cluster)
            else:
                leaf_cluster.append(component_node)
            return component_node, node_order

        from abjad.tools import graphtools
        from abjad.tools import scoretools
        node_order = []
        node_mapping = {}
        graph = graphtools.GraphvizGraph(
            name='G',
            attributes={
                'style': 'rounded',
                },
            edge_attributes={
                },
            node_attributes={
                'fontname': 'Arial',
                'shape': 'none',
                },
            )
        leaf_cluster = graphtools.GraphvizSubgraph(name='leaves')
        component_node, node_order = recurse(self, leaf_cluster)
        if len(leaf_cluster) == 1:
            graph.append(leaf_cluster[0])
        elif len(leaf_cluster):
            graph.append(leaf_cluster)
        graph._node_order = node_order

        if spanner:
            pairs = sequencetools.Sequence(spanner.components).nwise()
            for component_one, component_two in pairs:
                node_one = node_mapping[component_one]
                node_two = node_mapping[component_two]
                edge = graphtools.GraphvizEdge(
                    attributes={
                        'constraint': False,
                        'penwidth': 5,
                        },
                    )
                edge.attach(node_one, node_two)
            for component in spanner.components:
                node = node_mapping[component]
                table = node[0]
                table.attributes['border'] = 4
                table.attributes['bgcolor'] = 'grey80'
                if isinstance(component, Container):
                    for child in iterate(component).depth_first():
                        if child is component:
                            continue
                        node = node_mapping[child]
                        table = node[0]
                        table.attributes['bgcolor'] = 'grey80'

        return graph

    def __iter__(self):
        r'''Iterates container.

        ..  container:: example

            Abjad containers are iterables:

            ::

                >>> import collections
                >>> container = Container()
                >>> isinstance(container, collections.Iterable)
                True

        ..  container:: example

            Abjad containers are not sequences:

            ::

                >>> import collections
                >>> container = Container()
                >>> isinstance(container, collections.Sequence)
                False

        Yields container elements.

        Returns generator.
        '''
        return iter(self._music)

    def __len__(self):
        r'''Gets number of items in container.

        Returns nonnegative integer.
        '''
        return len(self._music)

    def __setitem__(self, i, argument):
        r'''Sets container `i` equal to `argument`.
        Finds spanners that dominate self[i] and children of self[i].
        Replaces contents at self[i] with 'argument'.
        Reattaches spanners to new contents.
        Always leaves score tree in tact.

        Returns none.
        '''
        return self._set_item(i, argument)

    ### PRIVATE METHODS ###

    def _append_without_withdrawing_from_crossing_spanners(self, component):
        '''Not composer-safe.
        '''
        self._set_item(slice(len(self), len(self)), [component],
            withdraw_components_from_crossing_spanners=False)

    def _as_graphviz_node(self):
        from abjad.tools import graphtools
        node = Component._as_graphviz_node(self)
        node[0].append(
            graphtools.GraphvizTableRow([
                graphtools.GraphvizTableCell(
                    label=type(self).__name__,
                    attributes={'border': 0},
                    ),
                ])
            )
        return node

    def _copy_with_children_and_indicators_but_without_spanners(self):
        new = self._copy_with_indicators_but_without_children_or_spanners()
        for component in self:
            new_component = \
                component._copy_with_children_and_indicators_but_without_spanners()
            new.append(new_component)
        return new

    def _copy_with_indicators_but_without_children_or_spanners(self):
        new = Component._copy_with_indicators_but_without_children_or_spanners(
            self)
        new.is_simultaneous = self.is_simultaneous
        return new

    def _eject_contents(self):
        if inspect_(self).get_parentage().parent is not None:
            message = 'can not eject contents of in-score container.'
            raise Exception(message)
        contents = self[:]
        for component in contents:
            component._set_parent(None)
        self._music[:] = []
        return contents

    def _format_after_slot(self, bundle):
        result = []
        result.append(('commands', bundle.after.commands))
        result.append(('comments', bundle.after.comments))
        return tuple(result)

    def _format_before_slot(self, bundle):
        result = []
        result.append(('comments', bundle.before.comments))
        result.append(('commands', bundle.before.commands))
        return tuple(result)

    def _format_close_brackets_slot(self, bundle):
        result = []
        if self.is_simultaneous:
            brackets_close = ['>>']
        else:
            brackets_close = ['}']
        result.append([('close brackets', ''), brackets_close])
        return tuple(result)

    def _format_closing_slot(self, bundle):
        result = []
        result.append(('grob reverts', bundle.grob_reverts))
        result.append(('commands', bundle.closing.commands))
        result.append(('comments', bundle.closing.comments))
        return self._format_slot_contributions_with_indent(result)

    def _format_content_pieces(self):
        from abjad.tools import systemtools
        indent = systemtools.LilyPondFormatManager.indent
        result = []
        for m in self._music:
            result.extend(format(m).split('\n'))
        result = [indent + x for x in result]
        return result

    def _format_contents_slot(self, bundle):
        result = []
        result.append([('contents', '_contents'), self._format_content_pieces()])
        return tuple(result)

    def _format_open_brackets_slot(self, bundle):
        result = []
        if self.is_simultaneous:
            brackets_open = ['<<']
        else:
            brackets_open = ['{']
        result.append([('open brackets', ''), brackets_open])
        return tuple(result)

    def _format_opening_slot(self, bundle):
        result = []
        result.append(('comments', bundle.opening.comments))
        result.append(('commands', bundle.opening.commands))
        result.append(('grob overrides', bundle.grob_overrides))
        result.append(('context settings', bundle.context_settings))
        return self._format_slot_contributions_with_indent(result)

    def _format_slot_contributions_with_indent(self, slot):
        from abjad.tools import systemtools
        indent = systemtools.LilyPondFormatManager.indent
        result = []
        for contributor, contributions in slot:
            result.append(
                (contributor, tuple([indent + x for x in contributions])))
        return tuple(result)

    def _get_abbreviated_string_format(self):
        if 0 < len(self):
            summary = str(len(self))
        else:
            summary = ''
        if self.is_simultaneous:
            open_bracket_string, close_bracket_string = '<<', '>>'
        else:
            open_bracket_string, close_bracket_string = '{', '}'
        name = self.name
        if name is not None:
            name = '-"{}"'.format(name)
        else:
            name = ''
        if hasattr(self, '_context_name'):
            result = '<{}{}{}{}{}>'
            result = result.format(
                self.context_name,
                name,
                open_bracket_string,
                summary,
                close_bracket_string,
                )
        else:
            result = '<{}{}{}{}>'
            result = result.format(
                name,
                open_bracket_string,
                summary,
                close_bracket_string,
                )
        return result

    def _get_format_specification(self):
        from abjad.tools import scoretools
        repr_text = None
        repr_args_values = []
        repr_kwargs_names = []
        if self.is_simultaneous:
            repr_kwargs_names.append('is_simultaneous')
        storage_format_args_values = []
        if self:
            repr_args_values.append(self._contents_summary)
            lilypond_format = ' '.join(format(x, 'lilypond') for x in self)
            lilypond_format = lilypond_format.replace('\n', ' ')
            lilypond_format = lilypond_format.replace('\t', ' ')
            lilypond_format = lilypond_format.replace('  ', ' ')
            storage_format_args_values.append(lilypond_format)
            if not all(isinstance(x, scoretools.Leaf) for x in self):
                repr_text = self._get_abbreviated_string_format()
        return systemtools.FormatSpecification(
            client=self,
            repr_args_values=repr_args_values,
            repr_kwargs_names=repr_kwargs_names,
            repr_text=repr_text,
            storage_format_args_values=storage_format_args_values,
            storage_format_kwargs_names=[],
            )

    def _get_spanners_that_dominate_component_pair(self, left, right):
        r'''Returns spanners that dominant component pair.
        Returns set (spanner, index) pairs.
        `left` must be an Abjad component or None.
        `right` must be an Abjad component or None.

        If both `left` and `right` are components,
        then `left` and `right` must be logical-voice-contiguous.

        This is a version of Selection._get_dominant_spanners().
        This version is useful for finding spanners that dominant
        a zero-length slice between components, as in staff[2:2].
        '''
        if left is None or right is None:
            return set([])
        left_contained = left._get_descendants()._get_spanners()
        right_contained = right._get_descendants()._get_spanners()
        dominant_spanners = left_contained & right_contained
        right_start_offset = right._get_timespan().start_offset
        components_after_gap = []
        for component in right._get_lineage():
            if component._get_timespan().start_offset == right_start_offset:
                components_after_gap.append(component)
        receipt = set([])
        for spanner in dominant_spanners:
            for component in components_after_gap:
                if component in spanner:
                    index = spanner._index(component)
                    receipt.add((spanner, index))
                    continue
        return receipt

    def _get_spanners_that_dominate_slice(self, start, stop):
        if start == stop:
            if start == 0:
                left = None
            else:
                left = self[start - 1]
            if len(self) <= stop:
                right = None
            else:
                right = self[stop]
            if left is None:
                left = self._get_sibling(-1)
            if right is None:
                right = self._get_sibling(1)
            spanners_receipt = \
                self._get_spanners_that_dominate_component_pair(left, right)
        else:
            selection = self[start:stop]
            spanners_receipt = selection._get_dominant_spanners()
        return spanners_receipt

    def _get_spanners_that_span_slice(self, start, stop):
        if start == stop:
            if start == 0:
                left = None
            else:
                left = self[start - 1]
            if len(self) <= stop:
                right = None
            else:
                right = self[stop]
            if left is None:
                left = self._get_sibling(-1)
            if right is None:
                right = self._get_sibling(1)
            print(left, right)
        else:
            selection = self[start:stop]
            print(selection)

    def _iterate_bottom_up(self):
        def recurse(node):
            if isinstance(node, Container):
                for x in node:
                    for y in recurse(x):
                        yield y
            yield node
        return recurse(self)

    def _iterate_top_down(self):
        def recurse(node):
            yield node
            if isinstance(node, Container):
                for x in node:
                    for y in recurse(x):
                        yield y
        return recurse(self)

    def _scale_contents(self, multiplier):
        for argument in iterate(self[:]).by_topmost_logical_ties_and_components():
            argument._scale(multiplier)

    def _set_item(
        self,
        i,
        argument,
        withdraw_components_from_crossing_spanners=True,
        ):
        r'''This method exists because __setitem__ can not accept keywords.

        Note that setting
        withdraw_components_from_crossing_spanners=False constitutes a
        composer-unsafe use of this method.

        Only private methods should set this keyword.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        # cache indicators attached to components in argument
        expr_indicators = []
        for component in iterate(argument).by_class():
            indicators = component._get_indicators(unwrap=False)
            expr_indicators.extend(indicators)
        # item assignment
        if isinstance(i, int):
            if isinstance(argument, str):
                argument = self._parse_string(argument)[:]
                assert len(argument) == 1, repr(argument)
                argument = argument[0]
            else:
                argument = [argument]
            if i < 0:
                i = len(self) + i
            i = slice(i, i + 1)
        else:
            if isinstance(argument, str):
                argument = self._parse_string(argument)[:]
            elif (isinstance(argument, list) and
                len(argument) == 1 and
                isinstance(argument[0], str)):
                argument = self._parse_string(argument[0])[:]
        prototype = (scoretools.Component, selectiontools.Selection)
        assert all(isinstance(x, prototype) for x in argument)
        new_expr = []
        for item in argument:
            if isinstance(item, selectiontools.Selection):
                new_expr.extend(item)
            else:
                new_expr.append(item)
        argument = new_expr
        assert all(isinstance(x, scoretools.Component) for x in argument)
        if any(isinstance(x, scoretools.GraceContainer) for x in argument):
            message = 'must attach grace container to note or chord.'
            raise Exception(message)
        if self._check_for_cycles(argument):
            raise ParentageError('Attempted to induce cycles.')
        if (
            i.start == i.stop and
            i.start is not None and
            i.stop is not None and
            i.start <= -len(self)
            ):
            start, stop = 0, 0
        else:
            start, stop, stride = i.indices(len(self))
        old = self[start:stop]
        spanners_receipt = self._get_spanners_that_dominate_slice(start, stop)
        #print('RECEIPT', spanners_receipt, self, argument)
        for component in old:
            for child in iterate([component]).by_class():
                for spanner in child._get_spanners():
                    spanner._remove(child)
        del(self[start:stop])
        # must withdraw before setting in self!
        # otherwise circular withdraw ensues!
        if withdraw_components_from_crossing_spanners:
            selection = selectiontools.Selection(argument)
            if selection._all_are_contiguous_components_in_same_logical_voice(
                selection):
                selection._withdraw_from_crossing_spanners()
        self._music.__setitem__(slice(start, start), argument)
        for component in argument:
            component._set_parent(self)
        for spanner, index in spanners_receipt:
            for component in reversed(argument):
                spanner._insert(index, component)
                component._spanners.add(spanner)
        for indicator in expr_indicators:
            if hasattr(indicator, '_update_effective_context'):
                indicator._update_effective_context()

    ### PRIVATE METHODS ###

    @staticmethod
    def _all_are_orphan_components(argument):
        from abjad.tools import scoretools
        for component in argument:
            if not isinstance(component, scoretools.Component):
                return False
            if not component._get_parentage().is_orphan:
                return False
        return True

    @staticmethod
    def _flatten_selections(music):
        components = []
        for item in music:
            if isinstance(item, selectiontools.Selection):
                components.extend(item)
            else:
                components.append(item)
        return components

    def _initialize_music(self, music):
        Selection = selectiontools.Selection
        music = music or []
        if isinstance(music, list):
            music = self._flatten_selections(music)
        if self._all_are_orphan_components(music):
            self._music = list(music)
            self[:]._set_parents(self)
        elif Selection._all_are_contiguous_components_in_same_logical_voice(
            music):
            music = selectiontools.Selection(music)
            parent, start, stop = music._get_parent_and_start_stop_indices()
            self._music = list(music)
            self[:]._set_parents(self)
            assert parent is not None
            parent._music.insert(start, self)
            self._set_parent(parent)
        elif isinstance(music, str):
            parsed = self._parse_string(music)
            self._music = []
            self.is_simultaneous = parsed.is_simultaneous
            if (parsed.is_simultaneous or
                not Selection._all_are_contiguous_components_in_same_logical_voice(
                    parsed[:])):
                while len(parsed):
                    self.append(parsed.pop(0))
            else:
                self[:] = parsed[:]
        else:
            message = 'can not initialize container from {!r}.'
            message = message.format((music))
            raise TypeError(message)

    def _is_one_of_my_first_leaves(self, leaf):
        return leaf in self._get_descendants_starting_with()

    def _is_one_of_my_last_leaves(self, leaf):
        return leaf in self._get_descendants_stopping_with()

    def _move_spanners_to_children(self):
        for spanner in self._get_spanners():
            i = spanner._index(self)
            spanner._components.__setitem__(slice(i, i + 1), self[:])
            for component in self:
                component._spanners.add(spanner)
            self._spanners.discard(spanner)
        return self

    def _parse_string(self, string):
        from abjad.tools import lilypondfiletools
        from abjad.tools import lilypondparsertools
        from abjad.tools import rhythmtreetools
        from abjad.tools.topleveltools import parse
        user_input = string.strip()
        if user_input.startswith('abj:'):
            parser = lilypondparsertools.ReducedLyParser()
            parsed = parser(user_input[4:])
            if parser._toplevel_component_count == 1:
                parsed = Container([parsed])
        elif user_input.startswith('rtm:'):
            parsed = rhythmtreetools.parse_rtm_syntax(user_input[4:])
        else:
            if (
                not user_input.startswith('<<') or
                not user_input.endswith('>>')
                ):
                user_input = '{{ {} }}'.format(user_input)
            parsed = parse(user_input)
            if isinstance(parsed, lilypondfiletools.LilyPondFile):
                parsed = Container(parsed.items[:])
            assert isinstance(parsed, Container)
        return parsed

    def _scale(self, multiplier):
        self._scale_contents(multiplier)

    def _split_at_index(self, i, fracture_spanners=False):
        r'''Splits container to the left of index `i`.

        Preserves tuplet multiplier when container is a tuplet.

        Preserves time signature denominator when container is a measure.

        Resizes resizable containers.

        Returns split parts.
        '''
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        # partition my music
        left_music = self[:i]
        right_music = self[i:]
        # instantiate new left and right containers
        if isinstance(self, scoretools.Measure):
            time_signature = self._get_effective(
                indicatortools.TimeSignature)
            denominator = time_signature.denominator
            left_duration = sum([x._get_duration() for x in left_music])
            left_pair = mathtools.NonreducedFraction(left_duration)
            left_pair = left_pair.with_multiple_of_denominator(denominator)
            left_time_signature = indicatortools.TimeSignature(left_pair)
            left = type(self)(left_time_signature, left_music)
            left.implicit_scaling = self.implicit_scaling
            right_duration = sum([x._get_duration() for x in right_music])
            right_pair = mathtools.NonreducedFraction(right_duration)
            right_pair = right_pair.with_multiple_of_denominator(denominator)
            right_time_signature = indicatortools.TimeSignature(right_pair)
            right = type(self)(right_time_signature, right_music)
            right.implicit_scaling = self.implicit_scaling
        elif isinstance(self, scoretools.FixedDurationTuplet):
            multiplier = self.multiplier
            left = type(self)(1, left_music)
            right = type(self)(1, right_music)
            target_duration = multiplier * left._contents_duration
            left.target_duration = target_duration
            target_duration = multiplier * right._contents_duration
            right.target_duration = target_duration
        elif isinstance(self, scoretools.Tuplet):
            multiplier = self.multiplier
            left = type(self)(multiplier, left_music)
            right = type(self)(multiplier, right_music)
        else:
            left = type(self)(left_music)
            right = type(self)(right_music)
        # save left and right containers together for iteration
        halves = (left, right)
        nonempty_halves = [half for half in halves if len(half)]
        # give my attached spanners to my children
        self._move_spanners_to_children()
        # incorporate left and right parents in score if possible
        selection = selectiontools.Selection(self)
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        if parent is not None:
            parent._music.__setitem__(slice(start, stop + 1), nonempty_halves)
            for part in nonempty_halves:
                part._set_parent(parent)
        else:
            left._set_parent(None)
            right._set_parent(None)
        # fracture spanners if requested
        if fracture_spanners:
            for spanner in left._get_spanners():
                index = spanner._index(left)
                spanner._fracture(index, direction=Right)
        # return new left and right containers
        return halves

    def _split_by_duration(
        self,
        duration,
        fracture_spanners=False,
        tie_split_notes=True,
        use_messiaen_style_ties=False,
        ):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        # check input
        duration = durationtools.Duration(duration)
        assert 0 <= duration, repr(duration)
        # if zero duration then return empty list and self
        if duration == 0:
            return [], self
        # get split point score offset
        global_split_point = self._get_timespan().start_offset + duration
        # get any duration-crossing descendents
        cross_offset = self._get_timespan().start_offset + duration
        duration_crossing_descendants = []
        for descendant in self._get_descendants():
            start_offset = descendant._get_timespan().start_offset
            stop_offset = descendant._get_timespan().stop_offset
            if start_offset < cross_offset < stop_offset:
                duration_crossing_descendants.append(descendant)
        # get any duration-crossing measure descendents
        measures = [
            x for x in duration_crossing_descendants
            if isinstance(x, scoretools.Measure)
            ]
        # if we must split a power-of-two measure at non-power-of-two
        # split point then go ahead and transform the power-of-two measure
        # to non-power-of-two equivalent now;
        # code that crawls and splits later on will be happier
        if len(measures) == 1:
            measure = measures[0]
            split_point_in_measure = \
                global_split_point - measure._get_timespan().start_offset
            if measure.has_non_power_of_two_denominator:
                if not measure.implied_prolation == \
                    split_point_in_measure.implied_prolation:
                    raise NotImplementedError
            elif not mathtools.is_nonnegative_integer_power_of_two(
                split_point_in_measure.denominator):
                non_power_of_two_factors = mathtools.remove_powers_of_two(
                    split_point_in_measure.denominator)
                non_power_of_two_factors = mathtools.factors(
                    non_power_of_two_factors)
                non_power_of_two_product = 1
                for non_power_of_two_factor in non_power_of_two_factors:
                    non_power_of_two_product *= non_power_of_two_factor
                scoretools.scale_measure_denominator_and_adjust_measure_contents(
                    measure, non_power_of_two_product)
                # rederive duration crosses with possibly new measure contents
                cross_offset = self._get_timespan().start_offset + duration
                duration_crossing_descendants = []
                for descendant in self._get_descendants():
                    start_offset = descendant._get_timespan().start_offset
                    stop_offset = descendant._get_timespan().stop_offset
                    if start_offset < cross_offset < stop_offset:
                        duration_crossing_descendants.append(descendant)
        elif 1 < len(measures):
            message = 'measures can not nest.'
            raise Exception(message)
        # any duration-crossing leaf will be at end of list
        bottom = duration_crossing_descendants[-1]
        did_split_leaf = False
        # if split point necessitates leaf split
        if isinstance(bottom, scoretools.Leaf):
            assert isinstance(bottom, scoretools.Leaf)
            did_split_leaf = True
            split_point_in_bottom = \
                global_split_point - bottom._get_timespan().start_offset
            left_list, right_list = bottom._split_by_duration(
                split_point_in_bottom,
                fracture_spanners=fracture_spanners,
                tie_split_notes=tie_split_notes,
                use_messiaen_style_ties=use_messiaen_style_ties,
                )
            right = right_list[0]
            leaf_right_of_split = right
            leaf_left_of_split = left_list[-1]
            duration_crossing_containers = duration_crossing_descendants[:-1]
            if not len(duration_crossing_containers):
                return left_list, right_list
        # if split point falls between leaves
        # then find leaf to immediate right of split point
        # in order to start upward crawl through duration-crossing containers
        else:
            duration_crossing_containers = duration_crossing_descendants[:]
            for leaf in iterate(bottom).by_leaf():
                if leaf._get_timespan().start_offset == global_split_point:
                    leaf_right_of_split = leaf
                    leaf_left_of_split = leaf_right_of_split._get_leaf(-1)
                    break
            else:
                message = 'can not split empty container {!r}.'
                message = message.format(bottom)
                raise Exception(message)
        # find component to right of split that is also immediate child of
        # last duration-crossing container
        for component in \
            leaf_right_of_split._get_parentage(include_self=True):
            if component._parent is duration_crossing_containers[-1]:
                highest_level_component_right_of_split = component
                break
        else:
            message = 'should we be able to get here?'
            raise ValueError(message)
        # crawl back up through duration-crossing containers and
        # fracture spanners if requested
        if fracture_spanners:
            start_offset = leaf_right_of_split._get_timespan().start_offset
            for parent in leaf_right_of_split._get_parentage():
                if parent._get_timespan().start_offset == start_offset:
                    for spanner in parent._get_spanners():
                        index = spanner._index(parent)
                        spanner._fracture(index, direction=Left)
                if parent is component:
                    break
        # crawl back up through duration-crossing containers and split each
        previous = highest_level_component_right_of_split
        for duration_crossing_container in \
            reversed(duration_crossing_containers):
            assert isinstance(
                duration_crossing_container, scoretools.Container)
            i = duration_crossing_container.index(previous)
            left, right = duration_crossing_container._split_at_index(
                i,
                fracture_spanners=fracture_spanners,
                )
            previous = right
        # NOTE: If logical tie here is convenience, then fusing is good.
        #       If logical tie here is user-given, then fusing is less good.
        #       Maybe later model difference between user logical ties and not.
        left_logical_tie = leaf_left_of_split._get_logical_tie()
        right_logical_tie = leaf_right_of_split._get_logical_tie()
        left_logical_tie._fuse_leaves_by_immediate_parent()
        right_logical_tie._fuse_leaves_by_immediate_parent()
        # reapply tie here if crawl above killed tie applied to leaves
        if did_split_leaf:
            if (
                tie_split_notes and
                isinstance(leaf_left_of_split, scoretools.Note)
                ):
                if (
                    leaf_left_of_split._get_parentage().root is
                    leaf_right_of_split._get_parentage().root
                    ):
                    leaves_around_split = \
                        (leaf_left_of_split, leaf_right_of_split)
                    selection = selectiontools.Selection(
                        leaves_around_split)
                    selection._attach_tie_spanner_to_leaf_pair(
                        use_messiaen_style_ties=use_messiaen_style_ties,
                        )
        # return pair of left and right list-wrapped halves of container
        return ([left], [right])

    ### PUBLIC METHODS ###

    def append(self, component):
        r'''Appends `component` to container.

        ..  container:: example

            Appends note to container:

            ::

                >>> container = Container("c'4 ( d'4 f'4 )")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'4 (
                    d'4
                    f'4 )
                }

            ::

                >>> container.append(Note("e'4"))
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'4 (
                    d'4
                    f'4 )
                    e'4
                }

        Returns none.
        '''
        self.__setitem__(slice(len(self), len(self)), [component])

    def extend(self, argument):
        r'''Extends container with `argument`.

        ..  container:: example

            Extends container with three notes:

            ::

                >>> container = Container("c'4 ( d'4 f'4 )")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'4 (
                    d'4
                    f'4 )
                }

            ::

                >>> notes = [Note("e'32"), Note("d'32"), Note("e'16")]
                >>> container.extend(notes)
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'4 (
                    d'4
                    f'4 )
                    e'32
                    d'32
                    e'16
                }

        Returns none.
        '''
        self.__setitem__(
            slice(len(self), len(self)),
            argument.__getitem__(slice(0, len(argument)))
            )

    def index(self, component):
        r'''Returns index of `component` in container.

        ..  container:: example

            Gets index of last element in container:

            ::

                >>> container = Container("c'4 d'4 f'4 e'4")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'4
                    d'4
                    f'4
                    e'4
                }

            ::

                >>> note = container[-1]
                >>> note
                Note("e'4")

            ::

                >>> container.index(note)
                3

        Returns nonnegative integer.
        '''
        for i, element in enumerate(self._music):
            if element is component:
                return i
        else:
            message = 'component {!r} not in Abjad container {!r}.'
            message = message.format(component, self)
            raise ValueError(message)

    def insert(self, i, component, fracture_spanners=False):
        r'''Inserts `component` at index `i` in container.

        ..  container:: example

            Inserts note. Does not fracture spanners:

            ::

                >>> container = Container([])
                >>> container.extend("fs16 cs' e' a'")
                >>> container.extend("cs''16 e'' cs'' a'")
                >>> container.extend("fs'16 e' cs' fs")
                >>> slur = spannertools.Slur(direction=Down)
                >>> attach(slur, container[:])
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    fs16 _ (
                    cs'16
                    e'16
                    a'16
                    cs''16
                    e''16
                    cs''16
                    a'16
                    fs'16
                    e'16
                    cs'16
                    fs16 )
                }

            ::

                >>> container.insert(-4, Note("e'4"), fracture_spanners=False)
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    fs16 _ (
                    cs'16
                    e'16
                    a'16
                    cs''16
                    e''16
                    cs''16
                    a'16
                    e'4
                    fs'16
                    e'16
                    cs'16
                    fs16 )
                }

        ..  container:: example

            Inserts note. Fractures spanners:

            ::

                >>> container = Container([])
                >>> container.extend("fs16 cs' e' a'")
                >>> container.extend("cs''16 e'' cs'' a'")
                >>> container.extend("fs'16 e' cs' fs")
                >>> slur = spannertools.Slur(direction=Down)
                >>> attach(slur, container[:])
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    fs16 _ (
                    cs'16
                    e'16
                    a'16
                    cs''16
                    e''16
                    cs''16
                    a'16
                    fs'16
                    e'16
                    cs'16
                    fs16 )
                }

            ::

                >>> container.insert(-4, Note("e'4"), fracture_spanners=True)
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    fs16 _ (
                    cs'16
                    e'16
                    a'16
                    cs''16
                    e''16
                    cs''16
                    a'16 )
                    e'4
                    fs'16 _ (
                    e'16
                    cs'16
                    fs16 )
                }

        Returns none.
        '''
        from abjad.tools import scoretools
        assert isinstance(i, int)
        if not fracture_spanners:
            self.__setitem__(slice(i, i), [component])
            return
        assert isinstance(component, scoretools.Component)
        component._set_parent(self)
        self._music.insert(i, component)
        previous_leaf = component._get_leaf(-1)
        if previous_leaf:
            for spanner in previous_leaf._get_spanners():
                index = spanner._index(previous_leaf)
                spanner._fracture(index, direction=Right)
        next_leaf = component._get_leaf(1)
        if next_leaf:
            for spanner in next_leaf._get_spanners():
                index = spanner._index(next_leaf)
                spanner._fracture(index, direction=Left)

    def pop(self, i=-1):
        r'''Pops component from container at index `i`.

        ..  container:: example

            Pops last element from container:

            ::

                >>> container = Container("c'4 ( d'4 f'4 ) e'4")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'4 (
                    d'4
                    f'4 )
                    e'4
                }

            ::

                >>> container.pop()
                Note("e'4")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'4 (
                    d'4
                    f'4 )
                }

        Returns component.
        '''
        component = self[i]
        del(self[i])
        return component

    def remove(self, component):
        r'''Removes `component` from container.

        ..  container:: example

            Removes note from container:

            ::

                >>> container = Container("c'4 ( d'4 f'4 ) e'4")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'4 (
                    d'4
                    f'4 )
                    e'4
                }

            ::

                >>> note = container[2]
                >>> note
                Note("f'4")

            ::

                >>> container.remove(note)
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'4 (
                    d'4 )
                    e'4
                }

        Returns none.
        '''
        i = self.index(component)
        del(self[i])

    def reverse(self):
        r'''Reverses contents of container.

        ..  container:: example

            Reverses staff:

            ::

                >>> staff = Staff("c'8 [ d'8 ] e'8 ( f'8 )")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8 [
                    d'8 ]
                    e'8 (
                    f'8 )
                }

            ::

                >>> staff.reverse()
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff)) # doctest: +SKIP
                \new Staff {
                    f'8 (
                    e'8 )
                    d'8 [
                    c'8 ]
                }

        Returns none.
        '''
        self._music.reverse()
        self._update_later(offsets=True)
        spanners = self._get_descendants()._get_spanners()
        for s in spanners:
            s._components.sort(key=lambda x: x._get_timespan().start_offset)

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        if not self:
            return '{ }'
        return '{{ {} }}'.format(self._contents_summary)

    @property
    def _contents_duration(self):
        if self.is_simultaneous:
            return max([durationtools.Duration(0)] +
                [x._preprolated_duration for x in self])
        else:
            duration = durationtools.Duration(0)
            for x in self:
                duration += x._preprolated_duration
            return duration

    @property
    def _contents_summary(self):
        if 0 < len(self):
            result = []
            for x in self._music:
                if hasattr(x, '_compact_representation_with_tie'):
                    result.append(x._compact_representation_with_tie)
                elif hasattr(x, '_compact_representation'):
                    result.append(x._compact_representation)
                else:
                    result.append(str(x))
            return ' '.join(result)
        else:
            return ''

    @property
    def _duration_in_seconds(self):
        if self.is_simultaneous:
            return max([durationtools.Duration(0)] +
                [x._get_duration(in_seconds=True) for x in self])
        else:
            duration = durationtools.Duration(0)
            for leaf in iterate(self).by_leaf():
                duration += leaf._get_duration(in_seconds=True)
            return duration

    @property
    def _preprolated_duration(self):
        return self._contents_duration

    ### PUBLIC PROPERTIES ###

    @property
    def is_simultaneous(self):
        r'''Is true when container is simultaneous. Otherwise false.

        ..  container:: example

            Gets simultaneity status of container:

            ::

                >>> container = Container()
                >>> container.append(Voice("c'8 d'8 e'8"))
                >>> container.append(Voice('g4.'))
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
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

                >>> container.is_simultaneous
                False

        ..  container:: example

            Sets simultaneity status of container:

            ::

                >>> container = Container()
                >>> container.append(Voice("c'8 d'8 e'8"))
                >>> container.append(Voice('g4.'))
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
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

                >>> container.is_simultaneous = True
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
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

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._is_simultaneous

    @is_simultaneous.setter
    def is_simultaneous(self, argument):
        from abjad.tools import scoretools
        if argument is None:
            return
        assert isinstance(argument, bool), repr(argument)
        prototype = scoretools.Context
        if argument and not all(isinstance(x, prototype) for x in self):
            message = 'simultaneous containers must contain only contexts.'
            raise ValueError(message)
        self._is_simultaneous = argument
        self._update_later(offsets=True)

    @property
    def name(self):
        r'''Gets and sets name of container.

        ..  container:: example

            Gets container name:

            ::

                >>> container = Container("c'4 d'4 e'4 f'4")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }

            ::

                >>> container.name is None
                True

        ..  container:: example

            Sets container name:

            ::

                >>> container = Container("c'4 d'4 e'4 f'4", name='Special')
                >>> show(container) # doctest: +SKIP

            ::

                >>> container.name
                'Special'

            Container name does not appear in LilyPond output:

            ::

                >>> f(container)
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }

        Defaults to none.

        Set to string or none.

        Returns string or none.
        '''
        return Component.name.fget(self)

    @name.setter
    def name(self, arg):
        return Component.name.fset(self, arg)
