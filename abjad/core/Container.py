import collections
import typing
import uqbar.graphs
from abjad import enums
from abjad import exceptions
from abjad.top.inspect import inspect
from abjad.top.iterate import iterate
from abjad.top.select import select
from abjad.utilities.Duration import Duration
from .Component import Component
from .Selection import Selection


class Container(Component):
    r"""
    Container.

    ..  container:: example

        Intializes from string:

        >>> container = abjad.Container("c'4 e'4 d'4 e'8 f'8")
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(container)
            {
                c'4
                e'4
                d'4
                e'8
                f'8
            }

    ..  container:: example

        Intializes from components:

        >>> notes = [
        ...     abjad.Note("c'4"),
        ...     abjad.Note("e'4"),
        ...     abjad.Note("d'4"),
        ...     abjad.Note("e'8"),
        ...     abjad.Note("f'8"),
        ...     ]
        >>> container = abjad.Container(notes)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(container)
            {
                c'4
                e'4
                d'4
                e'8
                f'8
            }

    ..  container:: example

        Intializes from selections:

        >>> notes = [
        ...     abjad.Note("c'4"),
        ...     abjad.Note("e'4"),
        ...     abjad.Note("d'4"),
        ...     abjad.Note("e'8"),
        ...     abjad.Note("f'8"),
        ...     ]
        >>> selection = abjad.select(notes)
        >>> container = abjad.Container(selection)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(container)
            {
                c'4
                e'4
                d'4
                e'8
                f'8
            }

    ..  container:: example

        Intializes from mixed components and selections:

        >>> items = [
        ...     abjad.Note("c'4"),
        ...     abjad.select(abjad.Note("e'4")),
        ...     abjad.select(abjad.Note("d'4")),
        ...     abjad.Note("e'8"),
        ...     abjad.Note("f'8"),
        ...     ]
        >>> container = abjad.Container(items)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(container)
            {
                c'4
                e'4
                d'4
                e'8
                f'8
            }

    ..  container:: example

        Containers are iterables:

        >>> import collections
        >>> container = abjad.Container("c'4 e'4 d'4 e'8 f'8")
        >>> isinstance(container, collections.Iterable)
        True

    ..  container:: example

        Containers are not sequences because containers do not implement
        reverse:

        >>> container = abjad.Container("c'4 e'4 d'4 e'8 f'8")
        >>> isinstance(container, collections.Sequence)
        False

    ..  container:: example

        Formatting positions contributions strictly one-per-line:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Articulation('^'), staff[0])
        >>> abjad.attach(abjad.Markup('Allegro', direction=abjad.Up), staff[0])
        >>> abjad.attach(abjad.StemTremolo(), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            :16
            -\marcato
            ^ \markup { Allegro }
            d'4
            e'4
            f'4
        }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = (
        '_identifier',
        '_components',
        '_formatter',
        '_named_children',
        '_name',
        '_is_simultaneous',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        identifier: str = None,
        is_simultaneous: bool = None,
        name: str = None,
        ) -> None:
        components = components or []
        Component.__init__(self)
        self._named_children: dict = {}
        self._is_simultaneous = None
        self._initialize_components(components)
        self.identifier = identifier
        self.is_simultaneous = is_simultaneous
        # NOTE: name must be set up *after* parent
        self._name = None
        self.name = name

    ### SPECIAL METHODS ###

    def __contains__(self, argument) -> bool:
        """
        Is true when ``argument`` appears in container.
        """
        if isinstance(argument, str):
            return argument in self._named_children
        else:
            for component in self.components:
                if component is argument:
                    return True
            else:
                return False

    def __delitem__(self, i):
        r"""
        Deletes components(s) at index ``i`` in container.

        ..  container:: example

            Deletes first tuplet in voice:

            >>> voice = abjad.Voice()
            >>> voice.append(abjad.Tuplet((2, 3), "c'4 d'4 e'4"))
            >>> voice.append(abjad.Tuplet((2, 3), "e'4 d'4 c'4"))
            >>> leaves = abjad.select(voice).leaves()
            >>> abjad.attach(abjad.Slur(), leaves)
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    \times 2/3 {
                        c'4
                        (
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        e'4
                        d'4
                        c'4
                        )
                    }
                }

            >>> tuplet_1 = voice[0]
            >>> del(voice[0])

            First tuplet no longer appears in voice:

                >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    \times 2/3 {
                        e'4
                        (
                        d'4
                        c'4
                        )
                    }
                }

            >>> abjad.inspect(voice).is_well_formed()
            True

            First tuplet is no longer slurred but is still well-formed:

            >>> abjad.show(tuplet_1) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet_1)
                \times 2/3 {
                    c'4
                    d'4
                    e'4
                }

            >>> abjad.inspect(tuplet_1).is_well_formed()
            True

        Withdraws component(s) from crossing spanners.

        Preserves spanners that component(s) cover(s).

        Returns none.
        """
        components = self[i]
        if not isinstance(components, Selection):
            components = select([components])
        if not self.is_simultaneous:
            components._withdraw_from_crossing_spanners()
        components._set_parents(None)

    def __getitem__(self, argument) -> typing.Union[Component, Selection]:
        """
        Gets item or slice identified by ``argument``.

        Traverses top-level items only.
        """
        if isinstance(argument, int):
            return self.components.__getitem__(argument)
        elif isinstance(argument, slice) and not self.is_simultaneous:
            return select(self.components.__getitem__(argument))
        elif isinstance(argument, slice) and self.is_simultaneous:
            return select(self.components.__getitem__(argument))
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

    def __getnewargs__(self) -> tuple:
        """
        Gets new container arguments.
        """
        return [], self.identifier, self.is_simultaneous, self.name

    def __graph__(self, spanner=None, **keywords):
        """
        Graphviz graph representation of container.

        Returns Graphviz graph.
        """
        def recurse(component, leaf_cluster):
            component_node = component._as_graphviz_node()
            node_mapping[component] = component_node
            node_order = [component_node.name]
            if isinstance(component, Container):
                graph.append(component_node)
                this_leaf_cluster = uqbar.graphs.Graph(
                    name=component_node.name,
                    attributes={
                        'color': 'grey75',
                        'penwidth': 2,
                        },
                    )
                all_are_leaves = True
                pending_node_order = []
                for child in component:
                    if not isinstance(child, abjad.Leaf):
                        all_are_leaves = False
                    child_node, child_node_order = recurse(
                        child, this_leaf_cluster)
                    pending_node_order.extend(child_node_order)
                    edge = uqbar.graphs.Edge()
                    edge.attach(component_node, child_node)
                if all_are_leaves:
                    pending_node_order.reverse()
                node_order.extend(pending_node_order)
                if len(this_leaf_cluster):
                    leaf_cluster.append(this_leaf_cluster)
            else:
                leaf_cluster.append(component_node)
            return component_node, node_order

        import abjad
        node_order = []
        node_mapping = {}
        graph = uqbar.graphs.Graph(
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
        leaf_cluster = uqbar.graphs.Graph(name='leaves')
        component_node, node_order = recurse(self, leaf_cluster)
        if len(leaf_cluster) == 1:
            graph.append(leaf_cluster[0])
        elif len(leaf_cluster):
            graph.append(leaf_cluster)
        graph._node_order = node_order

        if spanner:
            pairs = abjad.sequence(spanner.leaves).nwise()
            for component_one, component_two in pairs:
                node_one = node_mapping[component_one]
                node_two = node_mapping[component_two]
                edge = uqbar.graphs.Edge(
                    attributes={
                        'constraint': False,
                        'penwidth': 5,
                        },
                    )
                edge.attach(node_one, node_two)
            for component in spanner.leaves:
                node = node_mapping[component]
                table = node[0]
                table.attributes['border'] = 4
                table.attributes['bgcolor'] = 'grey80'
                if isinstance(component, Container):
                    for child in abjad.iterate(component)._depth_first():
                        if child is component:
                            continue
                        node = node_mapping[child]
                        table = node[0]
                        table.attributes['bgcolor'] = 'grey80'

        return graph

    def __iter__(self):
        """
        Iterates container.

        ..  container:: example

            Abjad containers are iterables:

            >>> import collections
            >>> container = abjad.Container()
            >>> isinstance(container, collections.Iterable)
            True

        ..  container:: example

            Abjad containers are not sequences:

            >>> import collections
            >>> container = abjad.Container()
            >>> isinstance(container, collections.Sequence)
            False

        Yields container elements.

        Returns generator.
        """
        return iter(self.components)

    def __len__(self) -> int:
        """
        Gets number of components in container.
        """
        return len(self.components)

    def __setitem__(self, i, argument) -> None:
        """
        Sets container ``i`` equal to ``argument``.
        Finds spanners that dominate self[i] and children of self[i].
        Replaces contents at self[i] with 'argument'.
        Reattaches spanners to new contents.
        Always leaves score tree in tact.
        """
        if isinstance(argument, str):
            argument = self._parse_string(argument)
            if isinstance(i, int):
                assert len(argument) == 1, repr(argument)
                argument = argument[0]
        return self._set_item(i, argument)

    ### PRIVATE METHODS ###

    @staticmethod
    def _all_are_orphan_components(argument):
        for component in argument:
            if not isinstance(component, Component):
                return False
            if not inspect(component).parentage().is_orphan:
                return False
        return True

    def _append_without_withdrawing_from_crossing_spanners(self, component):
        """
        Not composer-safe.
        """
        self._set_item(
            slice(len(self), len(self)),
            [component],
            withdraw_components_from_crossing_spanners=False,
            )

    def _as_graphviz_node(self):
        import abjad
        node = Component._as_graphviz_node(self)
        node[0].append(
            uqbar.graphs.TableRow([
                uqbar.graphs.TableCell(
                    type(self).__name__,
                    attributes={'border': 0},
                    ),
                ])
            )
        return node

    def _copy_with_children(self):
        new_container = self.__copy__()
        for component in self:
            if isinstance(component, Container):
                new_component = component._copy_with_children()
            else:
                new_component = component.__copy__()
            new_container.append(new_component)
        return new_container

    def _eject_contents(self):
        if inspect(self).parentage().parent is not None:
            message = 'can not eject contents of in-score container.'
            raise Exception(message)
        contents = self[:]
        for component in contents:
            component._set_parent(None)
        self._components[:] = []
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
            if self.identifier:
                brackets_close = [f'>>  {self.identifier}']
            else:
                brackets_close = ['>>']
        else:
            if self.identifier:
                brackets_close = [f'}}   {self.identifier}']
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
        import abjad
        indent = abjad.LilyPondFormatManager.indent
        result = []
        for component in self.components:
            string = component.__format__(
                format_specification='lilypond'
                )
            parts = string.split('\n')
            result.extend(parts)
        result = [indent + _ for _ in result]
        return result

    def _format_contents_slot(self, bundle):
        result = []
        result.append(
            [
                ('contents', '_contents'),
                self._format_content_pieces()
                ])
        return tuple(result)

    def _format_open_brackets_slot(self, bundle):
        result = []
        if self.is_simultaneous:
            if self.identifier:
                brackets_open = [f'<<  {self.identifier}']
            else:
                brackets_open = ['<<']
        else:
            if self.identifier:
                brackets_open = [f'{{   {self.identifier}']
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
        import abjad
        indent = abjad.LilyPondFormatManager.indent
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
        if hasattr(self, '_lilypond_type'):
            result = '<{}{}{}{}{}>'
            result = result.format(
                self.lilypond_type,
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

    def _get_compact_representation(self):
        if not self:
            return '{ }'
        return '{{ {} }}'.format(self._get_contents_summary())

    def _get_contents_duration(self):
        if self.is_simultaneous:
            return max(
                [Duration(0)] +
                [x._get_preprolated_duration() for x in self]
                )
        else:
            duration = Duration(0)
            for x in self:
                duration += x._get_preprolated_duration()
            return duration

    def _get_contents_summary(self):
        if 0 < len(self):
            result = []
            for x in self.components:
                if hasattr(x, '_get_compact_representation_with_tie'):
                    result.append(x._get_compact_representation_with_tie())
                elif hasattr(x, '_get_compact_representation'):
                    result.append(x._get_compact_representation())
                else:
                    result.append(str(x))
            return ' '.join(result)
        else:
            return ''

    def _get_duration_in_seconds(self):
        if self.is_simultaneous:
            return max(
                [Duration(0)] +
                [x._get_duration(in_seconds=True) for x in self]
                )
        else:
            duration = Duration(0)
            for leaf in iterate(self).leaves():
                duration += leaf._get_duration(in_seconds=True)
            return duration

    def _get_format_specification(self):
        import abjad
        repr_text = None
        repr_args_values = []
        repr_kwargs_names = self._get_repr_kwargs_names()
        storage_format_args_values = []
        if self:
            repr_args_values.append(self._get_contents_summary())
            lilypond_format = ' '.join(format(x, 'lilypond') for x in self)
            lilypond_format = lilypond_format.replace('\n', ' ')
            lilypond_format = lilypond_format.replace('\t', ' ')
            lilypond_format = lilypond_format.replace('  ', ' ')
            storage_format_args_values.append(lilypond_format)
            if not self[:].are_leaves():
                repr_text = self._get_abbreviated_string_format()
        return abjad.FormatSpecification(
            client=self,
            repr_args_values=repr_args_values,
            repr_kwargs_names=repr_kwargs_names,
            repr_text=repr_text,
            storage_format_args_values=storage_format_args_values,
            #storage_format_kwargs_names=[],
            )

    def _get_preprolated_duration(self):
        return self._get_contents_duration()

    def _get_repr_kwargs_names(self):
        return ['is_simultaneous', 'name']

    def _get_spanners_that_dominate_component_pair(self, left, right):
        """
        Returns spanners that dominant component pair.
        Returns set (spanner, index) pairs.
        ``left`` must be an Abjad component or None.
        ``right`` must be an Abjad component or None.

        If both ``left`` and ``right`` are components,
        then ``left`` and ``right`` must be logical-voice-contiguous.

        This is a version of Selection._get_dominant_spanners().
        This version is useful for finding spanners that dominant
        a zero-length slice between components, as in staff[2:2].
        """
        if left is None or right is None:
            return []
        left_descendants = inspect(left).descendants()
        left_contained = inspect(left_descendants).spanners()
        right_descendants = inspect(right).descendants()
        right_contained = inspect(right_descendants).spanners()
        dominant_spanners = set(left_contained) & set(right_contained)
        dominant_spanners = list(dominant_spanners)
        right_start_offset = inspect(right).timespan().start_offset
        components_after_gap = []
        for component in inspect(right).lineage():
            if inspect(component).timespan().start_offset == right_start_offset:
                components_after_gap.append(component)
        receipt = []
        for spanner in dominant_spanners:
            for component in components_after_gap:
                if component in spanner:
                    index = spanner._index(component)
                    receipt.append((spanner, index))
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
            spanners_receipt = self._get_spanners_that_dominate_component_pair(
                left,
                right,
                )
        else:
            selection = self[start:stop]
            spanners_receipt = selection._get_dominant_spanners()
        assert isinstance(spanners_receipt, list), repr(spanners_receipt)
        return spanners_receipt

    def _initialize_components(self, components):
        if (isinstance(components, collections.Iterable) and
            not isinstance(components, str)):
            components_ = []
            for item in components:
                if isinstance(item, Selection):
                    components_.extend(item)
                elif isinstance(item, str):
                    parsed = self._parse_string(item)
                    components_.append(parsed)
                else:
                    components_.append(item)
            components = components_
            for component in components:
                if not isinstance(component, Component):
                    message = f'must be component: {component!r}.'
                    raise Exception(component)
        if self._all_are_orphan_components(components):
            self._components = list(components)
            self[:]._set_parents(self)
        elif isinstance(components, str):
            parsed = self._parse_string(components)
            self._components = []
            self.is_simultaneous = parsed.is_simultaneous
            if (
                parsed.is_simultaneous or
                not select(parsed[:]).are_contiguous_logical_voice()
                ):
                while len(parsed):
                    self.append(parsed.pop(0))
            else:
                self[:] = parsed[:]
        else:
            message = 'can not initialize container from {!r}.'
            message = message.format(components)
            raise TypeError(message)

    def _is_one_of_my_first_leaves(self, leaf):
        return leaf in self._get_descendants_starting_with()

    def _is_one_of_my_last_leaves(self, leaf):
        return leaf in self._get_descendants_stopping_with()

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

    def _iterate_topmost(self):
        import abjad
        for component in self:
            if isinstance(component, abjad.Leaf):
                ties = inspect(component).spanners(abjad.Tie)
                if not ties or tuple(ties)[0].leaves[-1] is component:
                    yield inspect(component).logical_tie()
            else:
                assert isinstance(component, abjad.Container)
                yield component

    def _move_spanners_to_children(self):
        for spanner in inspect(self).spanners():
            i = spanner._index(self)
            spanner._components.__setitem__(slice(i, i + 1), self[:])
            for component in self:
                component._append_spanner(spanner)
            self._remove_spanner(spanner)
        return self

    def _parse_string(self, string):
        import abjad
        user_input = string.strip()
        if user_input.startswith('abj:'):
            parser = abjad.parser.ReducedLyParser()
            parsed = parser(user_input[4:])
            if parser._toplevel_component_count == 1:
                parent = inspect(parsed).parentage().parent
                if parent is None:
                    parsed = Container([parsed])
                else:
                    parsed = parent
        elif user_input.startswith('rtm:'):
            parsed = abjad.rhythmtrees.parse_rtm_syntax(user_input[4:])
        else:
            if (
                not user_input.startswith('<<') or
                not user_input.endswith('>>')
                ):
                user_input = '{{ {} }}'.format(user_input)
            parsed = abjad.parse(user_input)
            if isinstance(parsed, abjad.LilyPondFile):
                parsed = Container(parsed.items[:])
            assert isinstance(parsed, Container)
        return parsed

    @staticmethod
    def _remove_powers_of_two(n):
        assert isinstance(n, int), repr(n)
        assert not n <= 0, repr(n)
        while n % 2 == 0:
            n //= 2
        return n

    def _scale(self, multiplier):
        self._scale_contents(multiplier)

    def _scale_contents(self, multiplier):
        for item in  list(self._iterate_topmost()):
            item._scale(multiplier)

    def _set_item(
        self,
        i,
        argument,
        withdraw_components_from_crossing_spanners=True,
        ):
        """
        This method exists because __setitem__ can not accept keywords.

        Note that setting
        withdraw_components_from_crossing_spanners=False constitutes a
        composer-unsafe use of this method.

        Only private methods should set this keyword.
        """
        import abjad
        argument_indicators = []
        for component in abjad.iterate(argument).components():
            wrappers = inspect(component).wrappers()
            argument_indicators.extend(wrappers)
        if isinstance(i, int):
            argument = [argument]
            if i < 0:
                i = len(self) + i
            i = slice(i, i + 1)
        prototype = (Component, Selection)
        assert all(isinstance(_, prototype) for _ in argument)
        new_argument = []
        for item in argument:
            if isinstance(item, Selection):
                new_argument.extend(item)
            else:
                new_argument.append(item)
        argument = new_argument
        assert all(isinstance(_, abjad.Component) for _ in argument)
        if any(isinstance(_, abjad.GraceContainer) for _ in argument):
            message = 'must attach grace container to note or chord.'
            raise Exception(message)
        if self._check_for_cycles(argument):
            raise exceptions.ParentageError('attempted to induce cycles.')
        if (i.start == i.stop and
            i.start is not None and
            i.stop is not None and
            i.start <= -len(self)):
            start, stop = 0, 0
        else:
            start, stop, stride = i.indices(len(self))
        old_components = self[start:stop]
        spanners_receipt = self._get_spanners_that_dominate_slice(start, stop)
        for component in old_components:
            for child in abjad.iterate([component]).components():
                for spanner in inspect(child).spanners():
                    spanner._remove(child)
        del(self[start:stop])
        # must withdraw before setting in self!
        # otherwise circular withdraw ensues!
        if withdraw_components_from_crossing_spanners:
            selection = select(argument)
            if selection.are_contiguous_logical_voice():
                selection._withdraw_from_crossing_spanners()
        self._components.__setitem__(slice(start, start), argument)
        for component in argument:
            component._set_parent(self)
        for spanner, index in spanners_receipt:
            for component in reversed(argument):
                # attach spanners only to leaves
                leaves = select(component).leaves()
                for leaf in reversed(leaves):
                    spanner._insert(index, leaf)
                    leaf._append_spanner(spanner)
        for indicator in argument_indicators:
            if hasattr(indicator, '_update_effective_context'):
                indicator._update_effective_context()

    def _split_at_index(self, i, fracture_spanners=False):
        """
        Splits container to the left of index ``i``.

        Preserves tuplet multiplier when container is a tuplet.

        Preserves time signature denominator when container is a measure.

        Resizes resizable containers.

        Returns split parts.
        """
        import abjad
        # partition my components
        left_components = self[:i]
        right_components = self[i:]
        # instantiate new left and right containers
        if isinstance(self, abjad.Measure):
            time_signature = self._get_effective(abjad.TimeSignature)
            denominator = time_signature.denominator
            left_duration = sum([_._get_duration() for _ in left_components])
            left_pair = abjad.NonreducedFraction(left_duration)
            left_pair = left_pair.with_multiple_of_denominator(denominator)
            left_time_signature = abjad.TimeSignature(left_pair)
            left = type(self)(left_time_signature, [])
            abjad.mutate(left_components).wrap(left)
            left.implicit_scaling = self.implicit_scaling
            right_duration = sum([_._get_duration() for _ in right_components])
            right_pair = abjad.NonreducedFraction(right_duration)
            right_pair = right_pair.with_multiple_of_denominator(denominator)
            right_time_signature = abjad.TimeSignature(right_pair)
            right = type(self)(right_time_signature, [])
            abjad.mutate(right_components).wrap(right)
            right.implicit_scaling = self.implicit_scaling
        elif isinstance(self, abjad.Tuplet):
            multiplier = self.multiplier
            left = type(self)(multiplier, [])
            abjad.mutate(left_components).wrap(left)
            right = type(self)(multiplier, [])
            abjad.mutate(right_components).wrap(right)
        else:
            left = self.__copy__()
            abjad.mutate(left_components).wrap(left)
            right = self.__copy__()
            abjad.mutate(right_components).wrap(right)
        # save left and right containers together for iteration
        halves = (left, right)
        nonempty_halves = [half for half in halves if len(half)]
        # give my attached spanners to my children
        self._move_spanners_to_children()
        # incorporate left and right parents in score if possible
        selection = select(self)
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        if parent is not None:
            parent._components.__setitem__(slice(start, stop + 1), nonempty_halves)
            for part in nonempty_halves:
                part._set_parent(parent)
        else:
            left._set_parent(None)
            right._set_parent(None)
        # fracture spanners if requested
        if fracture_spanners:
            for spanner in inspect(left).spanners():
                index = spanner._index(left)
                spanner._fracture(index, direction=enums.Right)
        # return new left and right containers
        return halves

    def _split_by_duration(
        self,
        duration,
        fracture_spanners=False,
        tie_split_notes=True,
        repeat_ties=False,
        ):
        import abjad
        if self.is_simultaneous:
            return self._split_simultaneous_by_duration(
                duration=duration,
                fracture_spanners=fracture_spanners,
                tie_split_notes=tie_split_notes,
                repeat_ties=repeat_ties,
                )
        # check input
        duration = Duration(duration)
        assert 0 <= duration, repr(duration)
        # if zero duration then return empty list and self
        if duration == 0:
            return [], self
        # get split point score offset
        timespan = inspect(self).timespan()
        global_split_point = timespan.start_offset + duration
        # get any duration-crossing descendents
        cross_offset = timespan.start_offset + duration
        duration_crossing_descendants = []
        for descendant in inspect(self).descendants():
            timespan = inspect(descendant).timespan()
            start_offset = timespan.start_offset
            stop_offset = timespan.stop_offset
            if start_offset < cross_offset < stop_offset:
                duration_crossing_descendants.append(descendant)
        # get any duration-crossing measure descendents
        measures = [
            _ for _ in duration_crossing_descendants
            if isinstance(_, abjad.Measure)
            ]
        # if we must split a power-of-two measure at non-power-of-two
        # split point then go ahead and transform the power-of-two measure
        # to non-power-of-two equivalent now;
        # code that crawls and splits later on will be happier
        if len(measures) == 1:
            measure = measures[0]
            timespan = inspect(measure).timespan()
            start_offset = timespan.start_offset
            split_point_in_measure = global_split_point - start_offset
            if measure.has_non_power_of_two_denominator:
                pass
            elif not abjad.mathtools.is_nonnegative_integer_power_of_two(
                split_point_in_measure.denominator):
                non_power_of_two_factors = self._remove_powers_of_two(
                    split_point_in_measure.denominator
                    )
                non_power_of_two_factors = abjad.mathtools.factors(
                    non_power_of_two_factors)
                non_power_of_two_product = 1
                for non_power_of_two_factor in non_power_of_two_factors:
                    non_power_of_two_product *= non_power_of_two_factor
                measure._scale_denominator(non_power_of_two_product)
                # rederive duration crossers with possibly new measure contents
                timespan = inspect(self).timespan()
                cross_offset = timespan.start_offset + duration
                duration_crossing_descendants = []
                for descendant in inspect(self).descendants():
                    timespan = inspect(descendant).timespan()
                    start_offset = timespan.start_offset
                    stop_offset = timespan.stop_offset
                    if start_offset < cross_offset < stop_offset:
                        duration_crossing_descendants.append(descendant)
        elif 1 < len(measures):
            message = 'measures can not nest.'
            raise Exception(message)
        # any duration-crossing leaf will be at end of list
        bottom = duration_crossing_descendants[-1]
        did_split_leaf = False
        # if split point necessitates leaf split
        if isinstance(bottom, abjad.Leaf):
            assert isinstance(bottom, abjad.Leaf)
            did_split_leaf = True
            timespan = inspect(bottom).timespan()
            start_offset = timespan.start_offset
            split_point_in_bottom = global_split_point - start_offset
            left_list, right_list = bottom._split_by_durations(
                [split_point_in_bottom],
                fracture_spanners=fracture_spanners,
                tie_split_notes=tie_split_notes,
                repeat_ties=repeat_ties,
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
            for leaf in abjad.iterate(bottom).leaves():
                timespan = inspect(leaf).timespan()
                if timespan.start_offset == global_split_point:
                    leaf_right_of_split = leaf
                    leaf_left_of_split = inspect(leaf).leaf(-1)
                    break
            else:
                message = 'can not split empty container {!r}.'
                message = message.format(bottom)
                raise Exception(message)
        assert leaf_left_of_split is not None
        assert leaf_right_of_split is not None
        # find component to right of split
        # that is also immediate child of last duration-crossing container
        agent = inspect(leaf_right_of_split)
        parentage = agent.parentage(include_self=True)
        for component in parentage:
            parent = inspect(component).parentage().parent
            if parent is duration_crossing_containers[-1]:
                highest_level_component_right_of_split = component
                break
        else:
            message = 'should not be able to get here.'
            raise ValueError(message)
        # crawl back up through duration-crossing containers
        # and fracture spanners if requested
        if fracture_spanners:
            agent = inspect(leaf_right_of_split)
            start_offset = agent.timespan().start_offset
            for parent in agent.parentage():
                timespan = inspect(parent).timespan()
                if timespan.start_offset == start_offset:
                    for spanner in inspect(parent).spanners():
                        index = spanner._index(parent)
                        spanner._fracture(index, direction=enums.Left)
                if parent is component:
                    break
        # crawl back up through duration-crossing containers and split each
        previous = highest_level_component_right_of_split
        for container in reversed(duration_crossing_containers):
            assert isinstance(container, abjad.Container)
            index = container.index(previous)
            left, right = container._split_at_index(
                index,
                fracture_spanners=fracture_spanners,
                )
            previous = right
        # NOTE: If logical tie here is convenience, then fusing is good.
        #       If logical tie here is user-given, then fusing is less good.
        #       Maybe later model difference between user logical ties and not.
        left_logical_tie = inspect(leaf_left_of_split).logical_tie()
        right_logical_tie = inspect(leaf_right_of_split).logical_tie()
        left_logical_tie._fuse_leaves_by_immediate_parent()
        right_logical_tie._fuse_leaves_by_immediate_parent()
        # reapply tie here if crawl above killed tie applied to leaves
        if did_split_leaf:
            if (
                tie_split_notes and
                isinstance(leaf_left_of_split, abjad.Note)
                ):
                if (
                    inspect(leaf_left_of_split).parentage().root is
                    inspect(leaf_right_of_split).parentage().root
                    ):
                    leaves_around_split = (
                        leaf_left_of_split,
                        leaf_right_of_split,
                        )
                    selection = select(leaves_around_split)
                    selection._attach_tie_to_leaf_pair(
                        repeat_ties=repeat_ties,
                        )
        # return list-wrapped halves of container
        return [left], [right]

    def _split_simultaneous_by_duration(
        self,
        duration,
        fracture_spanners=False,
        tie_split_notes=True,
        repeat_ties=False,
        ):
        import abjad
        assert self.is_simultaneous
        left_components, right_components = [], []
        for component in self[:]:
            halves = component._split_by_duration(
                duration=duration,
                fracture_spanners=fracture_spanners,
                tie_split_notes=tie_split_notes,
                repeat_ties=repeat_ties,
                )
            left_components_, right_components_ = halves
            left_components.extend(left_components_)
            right_components.extend(right_components_)
        left_components = select(left_components)
        right_components = select(right_components)
        left_container = self.__copy__()
        right_container = self.__copy__()
        left_container.extend(left_components)
        right_container.extend(right_components)
        if inspect(self).parentage().parent is not None:
            containers = select([left_container, right_container])
            abjad.mutate(self).replace(containers)
        # return list-wrapped halves of container
        return [left_container], [right_container]

    ### PUBLIC PROPERTIES ###

    @property
    def components(self) -> tuple:
        """
        Gets components in container.
        """
        return self._components

    @property
    def identifier(self)  -> typing.Optional[str]:
        r"""
        Gets and sets bracket comment.

        ..  container:: example

            >>> container = abjad.Container(
            ...     "c'4 d'4 e'4 f'4",
            ...     identifier='%*% AB',
            ...     )
            >>> abjad.show(container) # doctest: +SKIP

            >>> abjad.f(container)
            {   %*% AB
                c'4
                d'4
                e'4
                f'4
            }   %*% AB

        """
        return self._identifier

    @identifier.setter
    def identifier(self, argument):
        assert isinstance(argument, (str, type(None))), repr(argument)
        self._identifier: typing.Optional[str] = argument

    @property
    def is_simultaneous(self) -> typing.Optional[bool]:
        r"""
        Is true when container is simultaneous.

        ..  container:: example

            Gets simultaneity status of container:

            >>> container = abjad.Container()
            >>> container.append(abjad.Voice("c'8 d'8 e'8"))
            >>> container.append(abjad.Voice('g4.'))
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                    }
                    \new Voice
                    {
                        g4.
                    }
                }

            >>> container.is_simultaneous is None
            True

        ..  container:: example

            Sets simultaneity status of container:

            >>> container = abjad.Container()
            >>> container.append(abjad.Voice("c'8 d'8 e'8"))
            >>> container.append(abjad.Voice('g4.'))
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                    }
                    \new Voice
                    {
                        g4.
                    }
                }

            >>> container.is_simultaneous = True
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                <<
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                    }
                    \new Voice
                    {
                        g4.
                    }
                >>

        """
        return self._is_simultaneous

    @is_simultaneous.setter
    def is_simultaneous(self, argument):
        if argument is None:
            return
        assert isinstance(argument, bool), repr(argument)
        if argument and not all(isinstance(_, Container) for _ in self):
            message = 'simultaneous containers must contain'
            message += ' only other containers.'
            raise ValueError(message)
        self._is_simultaneous = argument
        self._update_later(offsets=True)

    @property
    def name(self) -> typing.Optional[str]:
        r"""
        Gets and sets name of container.

        ..  container:: example

            Gets container name:

            >>> container = abjad.Container("c'4 d'4 e'4 f'4")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> container.name is None
            True

        ..  container:: example

            Sets container name:

            >>> container = abjad.Container(
            ...     "c'4 d'4 e'4 f'4",
            ...     name='Special',
            ...     )
            >>> abjad.show(container) # doctest: +SKIP

            >>> container.name
            'Special'

            Container name does not appear in LilyPond output:

            >>> abjad.f(container)
            {
                c'4
                d'4
                e'4
                f'4
            }

        """
        return self._name

    @name.setter
    def name(self, argument):
        assert isinstance(argument, (str, type(None)))
        old_name = self._name
        for parent in inspect(self).parentage(include_self=False):
            named_children = parent._named_children
            if old_name is not None:
                named_children[old_name].remove(self)
                if not named_children[old_name]:
                    del named_children[old_name]
            if argument is not None:
                if argument not in named_children:
                    named_children[argument] = [self]
                else:
                    named_children[argument].append(self)
        self._name = argument

    ### PUBLIC METHODS ###

    def append(self, component) -> None:
        r"""
        Appends ``component`` to container.

        ..  container:: example

            Appends note to container:

            >>> container = abjad.Container("c'4 ( d'4 f'4 )")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> container.append(abjad.Note("e'4"))
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'4
                }

        """
        if isinstance(component, str):
            selection = self._parse_string(component)
            assert len(selection) == 1
            component = selection[0]
        self.__setitem__(slice(len(self), len(self)), [component])

    def extend(self, argument) -> None:
        r"""
        Extends container with ``argument``.

        ..  container:: example

            Extends container with three notes:

            >>> container = abjad.Container("c'4 ( d'4 f'4 )")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> notes = [abjad.Note("e'32"), abjad.Note("d'32"), abjad.Note("e'16")]
            >>> container.extend(notes)
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'32
                    d'32
                    e'16
                }

        """
        if isinstance(argument, str):
            argument = self._parse_string(argument)
        elif isinstance(argument, collections.Iterable):
            argument_ = []
            for item in argument:
                if isinstance(item, str):
                    item = self._parse_string(item)
                argument_.append(item)
            argument = argument_
        self.__setitem__(
            slice(len(self), len(self)),
            argument.__getitem__(slice(0, len(argument)))
            )

    def index(self, component) -> int:
        r"""
        Returns index of ``component`` in container.

        ..  container:: example

            Gets index of last element in container:

            >>> container = abjad.Container("c'4 d'4 f'4 e'4")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'4
                    d'4
                    f'4
                    e'4
                }

            >>> note = container[-1]
            >>> note
            Note("e'4")

            >>> container.index(note)
            3

        """
        for i, element in enumerate(self.components):
            if element is component:
                return i
        else:
            message = 'component {!r} not in Abjad container {!r}.'
            message = message.format(component, self)
            raise ValueError(message)

    def insert(self, i, component, fracture_spanners=False) -> None:
        r"""
        Inserts ``component`` at index ``i`` in container.

        ..  container:: example

            Inserts note. Does not fracture spanners:

            >>> container = abjad.Container([])
            >>> container.extend("fs16 cs' e' a'")
            >>> container.extend("cs''16 e'' cs'' a'")
            >>> container.extend("fs'16 e' cs' fs")
            >>> slur = abjad.Slur(direction=abjad.Down)
            >>> abjad.attach(slur, container[:])
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    fs16
                    _ (
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
                    fs16
                    )
                }

            >>> container.insert(-4, abjad.Note("e'4"), fracture_spanners=False)
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    fs16
                    _ (
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
                    fs16
                    )
                }

        ..  container:: example

            Inserts note. Fractures spanners:

            >>> container = abjad.Container([])
            >>> container.extend("fs16 cs' e' a'")
            >>> container.extend("cs''16 e'' cs'' a'")
            >>> container.extend("fs'16 e' cs' fs")
            >>> slur = abjad.Slur(direction=abjad.Down)
            >>> abjad.attach(slur, container[:])
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    fs16
                    _ (
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
                    fs16
                    )
                }

            >>> container.insert(-4, abjad.Note("e'4"), fracture_spanners=True)
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    fs16
                    _ (
                    cs'16
                    e'16
                    a'16
                    cs''16
                    e''16
                    cs''16
                    a'16
                    )
                    e'4
                    fs'16
                    _ (
                    e'16
                    cs'16
                    fs16
                    )
                }

        """
        assert isinstance(i, int)
        if isinstance(component, str):
            selection = self._parse_string(component)
            assert len(selection) == 1, repr(selection)
            component = selection[0]
        if not fracture_spanners:
            self.__setitem__(slice(i, i), [component])
            return
        assert isinstance(component, Component)
        component._set_parent(self)
        self._components.insert(i, component)
        previous_leaf = component._get_leaf(-1)
        if previous_leaf:
            for spanner in inspect(previous_leaf).spanners():
                index = spanner._index(previous_leaf)
                spanner._fracture(index, direction=enums.Right)
        next_leaf = component._get_leaf(1)
        if next_leaf:
            for spanner in inspect(next_leaf).spanners():
                index = spanner._index(next_leaf)
                spanner._fracture(index, direction=enums.Left)

    def pop(self, i=-1):
        r"""
        Pops component from container at index ``i``.

        ..  container:: example

            Pops last element from container:

            >>> container = abjad.Container("c'4 ( d'4 f'4 ) e'4")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'4
                }

            >>> container.pop()
            Note("e'4")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

        Returns component.
        """
        component = self[i]
        del(self[i])
        return component

    def remove(self, component) -> None:
        r"""
        Removes ``component`` from container.

        ..  container:: example

            Removes note from container:

            >>> container = abjad.Container("c'4 ( d'4 f'4 ) e'4")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'4
                }

            >>> note = container[2]
            >>> note
            Note("f'4")

            >>> container.remove(note)
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'4
                    (
                    d'4
                    )
                    e'4
                }

        """
        i = self.index(component)
        del(self[i])
