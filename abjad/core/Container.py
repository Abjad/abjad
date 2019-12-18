import collections
import typing

import uqbar.graphs

from abjad import exceptions, rhythmtrees
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.system.Tag import Tag
from abjad.top.inspect import inspect
from abjad.top.iterate import iterate
from abjad.top.mutate import mutate
from abjad.top.parse import parse
from abjad.top.select import select
from abjad.utilities.Duration import Duration

from .Component import Component
from .Leaf import Leaf
from .Note import Note
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
        >>> isinstance(container, collections.abc.Iterable)
        True

    ..  container:: example

        Containers are not sequences because containers do not implement
        reverse:

        >>> container = abjad.Container("c'4 e'4 d'4 e'8 f'8")
        >>> isinstance(container, collections.abc.Sequence)
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
            - \marcato
            ^ \markup { Allegro }
            d'4
            e'4
            f'4
        }

    """

    ### CLASS VARIABLES ###

    _allowable_format_slots = (
        "absolute_before",
        "before",
        "opening",
        "closing",
        "after",
    )

    __documentation_section__ = "Containers"

    __slots__ = (
        "_identifier",
        "_components",
        "_formatter",
        "_named_children",
        "_name",
        "_is_simultaneous",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        identifier: str = None,
        simultaneous: bool = None,
        name: str = None,
        tag: Tag = None,
    ) -> None:
        components = components or []
        Component.__init__(self, tag=tag)
        self._named_children: dict = {}
        self._is_simultaneous = None
        # sets name temporarily for _find_correct_effective_context:
        self._name = name
        self._initialize_components(components)
        self.identifier = identifier
        self.simultaneous = simultaneous
        # sets name permanently after _initalize_components:
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
            >>> abjad.slur(leaves)
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
            >>> start_slur = abjad.StartSlur()
            >>> leaf = abjad.select(voice).leaf(0)
            >>> abjad.attach(start_slur, leaf)

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

            >>> abjad.inspect(voice).wellformed()
            True

            First tuplet must have start slur removed:

            >>> abjad.detach(abjad.StartSlur, tuplet_1[0])
            (StartSlur(),)

            >>> abjad.show(tuplet_1) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet_1)
                \times 2/3 {
                    c'4
                    d'4
                    e'4
                }

            >>> abjad.inspect(tuplet_1).wellformed()
            True

        Returns none.
        """
        components = self[i]
        if not isinstance(components, Selection):
            components = select([components])
        components._set_parents(None)

    def __getitem__(self, argument) -> typing.Union[Component, Selection]:
        """
        Gets item or slice identified by ``argument``.

        Traverses top-level items only.
        """
        if isinstance(argument, int):
            return self.components.__getitem__(argument)
        elif isinstance(argument, slice) and not self.simultaneous:
            return select(self.components.__getitem__(argument))
        elif isinstance(argument, slice) and self.simultaneous:
            return select(self.components.__getitem__(argument))
        elif isinstance(argument, str):
            if argument not in self._named_children:
                raise ValueError(f"can not find component named {argument!r}.")
            elif 1 < len(self._named_children.__getitem__(argument)):
                raise ValueError(f"multiple components named {argument!r}.")
            return self._named_children.__getitem__(argument)[0]
        raise ValueError(f"can not get container at {argument!r}.")

    def __getnewargs__(self) -> tuple:
        """
        Gets new container arguments.
        """
        return [], self.identifier, self.simultaneous, self.name, self.tag

    def __graph__(self, **keywords):
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
                    attributes={"color": "grey75", "penwidth": 2},
                )
                all_are_leaves = True
                pending_node_order = []
                for child in component:
                    if not isinstance(child, Leaf):
                        all_are_leaves = False
                    child_node, child_node_order = recurse(child, this_leaf_cluster)
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

        node_order = []
        node_mapping = {}
        graph = uqbar.graphs.Graph(
            name="G",
            attributes={"style": "rounded"},
            edge_attributes={},
            node_attributes={"fontname": "Arial", "shape": "none"},
        )
        leaf_cluster = uqbar.graphs.Graph(name="leaves")
        component_node, node_order = recurse(self, leaf_cluster)
        if len(leaf_cluster) == 1:
            graph.append(leaf_cluster[0])
        elif len(leaf_cluster):
            graph.append(leaf_cluster)
        graph._node_order = node_order
        return graph

    def __iter__(self):
        """
        Iterates container.

        ..  container:: example

            Abjad containers are iterables:

            >>> import collections
            >>> container = abjad.Container()
            >>> isinstance(container, collections.abc.Iterable)
            True

        ..  container:: example

            Abjad containers are not sequences:

            >>> import collections
            >>> container = abjad.Container()
            >>> isinstance(container, collections.abc.Sequence)
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
            if not inspect(component).parentage().orphan:
                return False
        return True

    def _as_graphviz_node(self):
        node = Component._as_graphviz_node(self)
        node[0].append(
            uqbar.graphs.TableRow(
                [uqbar.graphs.TableCell(type(self).__name__, attributes={"border": 0})]
            )
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
            message = "can not eject contents of in-score container."
            raise Exception(message)
        contents = self[:]
        for component in contents:
            component._set_parent(None)
        self._components[:] = []
        return contents

    def _format_after_slot(self, bundle):
        result = []
        result.append(("commands", bundle.after.commands))
        result.append(("comments", bundle.after.comments))
        return tuple(result)

    def _format_before_slot(self, bundle):
        result = []
        result.append(("comments", bundle.before.comments))
        result.append(("commands", bundle.before.commands))
        return tuple(result)

    def _format_close_brackets_slot(self, bundle):
        result = []
        if self.simultaneous:
            if self.identifier:
                brackets_close = [f">>  {self.identifier}"]
            else:
                brackets_close = [">>"]
        else:
            if self.identifier:
                brackets_close = [f"}}   {self.identifier}"]
            else:
                brackets_close = ["}"]
        if self.tag is not None:
            brackets_close = LilyPondFormatManager.tag(brackets_close, tag=self.tag)
        result.append([("close brackets", ""), brackets_close])
        return tuple(result)

    def _format_closing_slot(self, bundle):
        result = []
        result.append(("grob reverts", bundle.grob_reverts))
        result.append(("commands", bundle.closing.commands))
        result.append(("comments", bundle.closing.comments))
        return self._format_slot_contributions_with_indent(result)

    def _format_content_pieces(self):
        indent = LilyPondFormatManager.indent
        strings = []
        for component in self.components:
            string = component.__format__(format_specification="lilypond")
            for string in string.split("\n"):
                if string.isspace():
                    string = ""
                else:
                    string = indent + string
                strings.append(string)
        return strings

    def _format_contents_slot(self, bundle):
        result = []
        result.append([("contents", "_contents"), self._format_content_pieces()])
        return tuple(result)

    def _format_open_brackets_slot(self, bundle):
        result = []
        if self.simultaneous:
            if self.identifier:
                brackets_open = [f"<<  {self.identifier}"]
            else:
                brackets_open = ["<<"]
        else:
            if self.identifier:
                brackets_open = [f"{{   {self.identifier}"]
            else:
                brackets_open = ["{"]
        if self.tag is not None:
            brackets_open = LilyPondFormatManager.tag(brackets_open, tag=self.tag)
        result.append([("open brackets", ""), brackets_open])
        return tuple(result)

    def _format_opening_slot(self, bundle):
        result = []
        result.append(("comments", bundle.opening.comments))
        result.append(("commands", bundle.opening.commands))
        result.append(("grob overrides", bundle.grob_overrides))
        result.append(("context settings", bundle.context_settings))
        return self._format_slot_contributions_with_indent(result)

    def _get_abbreviated_string_format(self):
        if 0 < len(self):
            summary = str(len(self))
        else:
            summary = ""
        if self.simultaneous:
            open_bracket_string, close_bracket_string = "<<", ">>"
        else:
            open_bracket_string, close_bracket_string = "{", "}"
        name = self.name
        if name is not None:
            name = f'-"{name}"'
        else:
            name = ""
        if hasattr(self, "_lilypond_type"):
            result = "<{}{}{}{}{}>"
            result = result.format(
                self.lilypond_type,
                name,
                open_bracket_string,
                summary,
                close_bracket_string,
            )
        else:
            result = "<{}{}{}{}>"
            result = result.format(
                name, open_bracket_string, summary, close_bracket_string
            )
        return result

    def _get_compact_representation(self):
        if not self:
            return "{ }"
        return f"{{ {self._get_contents_summary()} }}"

    def _get_contents_duration(self):
        if self.simultaneous:
            return max([Duration(0)] + [x._get_preprolated_duration() for x in self])
        else:
            duration = Duration(0)
            for x in self:
                duration += x._get_preprolated_duration()
            return duration

    def _get_contents_summary(self):
        if 0 < len(self):
            result = []
            for x in self.components:
                if hasattr(x, "_get_compact_representation_with_tie"):
                    result.append(x._get_compact_representation_with_tie())
                elif hasattr(x, "_get_compact_representation"):
                    result.append(x._get_compact_representation())
                else:
                    result.append(str(x))
            return " ".join(result)
        else:
            return ""

    def _get_duration_in_seconds(self):
        if self.simultaneous:
            return max([Duration(0)] + [x._get_duration(in_seconds=True) for x in self])
        else:
            duration = Duration(0)
            for leaf in iterate(self).leaves():
                duration += leaf._get_duration(in_seconds=True)
            return duration

    def _get_format_specification(self):
        repr_text = None
        repr_args_values = []
        repr_kwargs_names = self._get_repr_kwargs_names()
        storage_format_args_values = []
        if self:
            repr_args_values.append(self._get_contents_summary())
            lilypond_format = " ".join(format(x, "lilypond") for x in self)
            lilypond_format = lilypond_format.replace("\n", " ")
            lilypond_format = lilypond_format.replace("\t", " ")
            lilypond_format = lilypond_format.replace("  ", " ")
            storage_format_args_values.append(lilypond_format)
            if not self[:].are_leaves():
                repr_text = self._get_abbreviated_string_format()
        return FormatSpecification(
            client=self,
            repr_args_values=repr_args_values,
            repr_kwargs_names=repr_kwargs_names,
            repr_text=repr_text,
            storage_format_args_values=storage_format_args_values,
        )

    def _get_on_beat_anchor_voice(self):
        from .OnBeatGraceContainer import OnBeatGraceContainer

        container = self._parent
        if container is None:
            return None
        if not container.simultaneous:
            return None
        if not len(container) == 2:
            return None
        index = container.index(self)
        if index == 0 and isinstance(container[1], OnBeatGraceContainer):
            return container[1]
        if index == 1 and isinstance(container[0], OnBeatGraceContainer):
            return container[0]
        return None

    def _get_preprolated_duration(self):
        return self._get_contents_duration()

    def _get_repr_kwargs_names(self):
        return ["simultaneous", "name"]

    def _initialize_components(self, components):
        if isinstance(components, collections.abc.Iterable) and not isinstance(
            components, str
        ):
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
                    message = f"must be component: {component!r}."
                    raise Exception(message)
        if self._all_are_orphan_components(components):
            self._components = list(components)
            self[:]._set_parents(self)
        elif isinstance(components, str):
            parsed = self._parse_string(components)
            self._components = []
            self.simultaneous = parsed.simultaneous
            if (
                parsed.simultaneous
                or not select(parsed[:]).are_contiguous_logical_voice()
            ):
                while len(parsed):
                    self.append(parsed.pop(0))
            else:
                self[:] = parsed[:]
        else:
            raise TypeError(f"can't initialize container from {components!r}.")

    def _is_on_beat_anchor_voice(self):
        from .Voice import Voice

        wrapper = self._parent
        if wrapper is None:
            return False
        if not isinstance(self, Voice):
            return False
        return wrapper._is_on_beat_wrapper()

    def _is_on_beat_wrapper(self):
        from .OnBeatGraceContainer import OnBeatGraceContainer
        from .Voice import Voice

        if not self.simultaneous:
            return False
        if len(self) != 2:
            return False
        if isinstance(self[0], OnBeatGraceContainer) and isinstance(self[1], Voice):
            return True
        if isinstance(self[0], Voice) and isinstance(self[1], OnBeatGraceContainer):
            return True
        return False

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
        for component in self:
            if isinstance(component, Leaf):
                logical_tie = component._get_logical_tie()
                if logical_tie.is_trivial or logical_tie[-1] is component:
                    yield logical_tie
            else:
                assert isinstance(component, Container)
                yield component

    def _parse_string(self, string):
        from abjad.parser.ReducedLyParser import ReducedLyParser
        from abjad.lilypondfile.LilyPondFile import LilyPondFile

        user_input = string.strip()
        if user_input.startswith("abj:"):
            parser = ReducedLyParser()
            parsed = parser(user_input[4:])
            if parser._toplevel_component_count == 1:
                parent = inspect(parsed).parentage().parent
                if parent is None:
                    parsed = Container([parsed])
                else:
                    parsed = parent
        elif user_input.startswith("rtm:"):
            parsed = rhythmtrees.parse_rtm_syntax(user_input[4:])
        else:
            if not user_input.startswith("<<") or not user_input.endswith(">>"):
                user_input = f"{{ {user_input} }}"
            parsed = parse(user_input)
            if isinstance(parsed, LilyPondFile):
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
        for item in list(self._iterate_topmost()):
            item._scale(multiplier)

    def _set_item(self, i, argument):
        from .BeforeGraceContainer import BeforeGraceContainer

        argument_indicators = []
        for component in iterate(argument).components():
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
        assert all(isinstance(_, Component) for _ in argument)
        if any(isinstance(_, BeforeGraceContainer) for _ in argument):
            raise Exception("must attach grace container to note or chord.")
        if self._check_for_cycles(argument):
            raise exceptions.ParentageError("attempted to induce cycles.")
        if (
            i.start == i.stop
            and i.start is not None
            and i.stop is not None
            and i.start <= -len(self)
        ):
            start, stop = 0, 0
        else:
            start, stop, stride = i.indices(len(self))
        del self[start:stop]
        self._components.__setitem__(slice(start, start), argument)
        for component in argument:
            component._set_parent(self)
        for indicator in argument_indicators:
            if hasattr(indicator, "_update_effective_context"):
                indicator._update_effective_context()

    def _split_at_index(self, i):
        """
        Splits container to the left of index ``i``.

        Preserves tuplet multiplier when container is a tuplet.

        Preserves time signature denominator when container is a measure.

        Resizes resizable containers.

        Returns split parts.
        """
        from .Tuplet import Tuplet

        # partition my components
        left_components = self[:i]
        right_components = self[i:]
        # instantiate new left and right containers
        if isinstance(self, Tuplet):
            multiplier = self.multiplier
            left = type(self)(multiplier, [])
            mutate(left_components).wrap(left)
            right = type(self)(multiplier, [])
            mutate(right_components).wrap(right)
        else:
            left = self.__copy__()
            mutate(left_components).wrap(left)
            right = self.__copy__()
            mutate(right_components).wrap(right)
        # save left and right containers together for iteration
        halves = (left, right)
        nonempty_halves = [half for half in halves if len(half)]
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
        # return new left and right containers
        return halves

    def _split_by_duration(self, duration):
        if self.simultaneous:
            return self._split_simultaneous_by_duration(duration=duration)
        duration = Duration(duration)
        assert 0 <= duration, repr(duration)
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
        # any duration-crossing leaf will be at end of list
        bottom = duration_crossing_descendants[-1]
        did_split_leaf = False
        # if split point necessitates leaf split
        if isinstance(bottom, Leaf):
            assert isinstance(bottom, Leaf)
            did_split_leaf = True
            timespan = inspect(bottom).timespan()
            start_offset = timespan.start_offset
            split_point_in_bottom = global_split_point - start_offset
            new_leaves = bottom._split_by_durations([split_point_in_bottom])
            for leaf in new_leaves:
                timespan = inspect(leaf).timespan()
                if timespan.stop_offset == global_split_point:
                    leaf_left_of_split = leaf
                if timespan.start_offset == global_split_point:
                    leaf_right_of_split = leaf
            duration_crossing_containers = duration_crossing_descendants[:-1]
            if not len(duration_crossing_containers):
                # return left_list, right_list
                raise Exception("how did we get here?")
        # if split point falls between leaves
        # then find leaf to immediate right of split point
        # in order to start upward crawl through duration-crossing containers
        else:
            duration_crossing_containers = duration_crossing_descendants[:]
            for leaf in iterate(bottom).leaves():
                timespan = inspect(leaf).timespan()
                if timespan.start_offset == global_split_point:
                    leaf_right_of_split = leaf
                    leaf_left_of_split = inspect(leaf).leaf(-1)
                    break
            else:
                raise Exception("can not split empty container {bottom!r}.")
        assert leaf_left_of_split is not None
        assert leaf_right_of_split is not None
        # find component to right of split
        # that is also immediate child of last duration-crossing container
        for component in inspect(leaf_right_of_split).parentage():
            parent = inspect(component).parentage().parent
            if parent is duration_crossing_containers[-1]:
                highest_level_component_right_of_split = component
                break
        else:
            raise ValueError("should not be able to get here.")
        # crawl back up through duration-crossing containers and split each
        previous = highest_level_component_right_of_split
        for container in reversed(duration_crossing_containers):
            assert isinstance(container, Container)
            index = container.index(previous)
            left, right = container._split_at_index(index)
            previous = right
        # reapply tie here if crawl above killed tie applied to leaves
        if did_split_leaf:
            if isinstance(leaf_left_of_split, Note):
                if (
                    inspect(leaf_left_of_split).parentage().root
                    is inspect(leaf_right_of_split).parentage().root
                ):
                    leaves_around_split = (
                        leaf_left_of_split,
                        leaf_right_of_split,
                    )
                    selection = select(leaves_around_split)
                    selection._attach_tie_to_leaves()
        # return list-wrapped halves of container
        return [left], [right]

    def _split_simultaneous_by_duration(self, duration):
        assert self.simultaneous
        left_components, right_components = [], []
        for component in self[:]:
            halves = component._split_by_duration(duration=duration)
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
            mutate(self).replace(containers)
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
    def identifier(self) -> typing.Optional[str]:
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
    def simultaneous(self) -> typing.Optional[bool]:
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

            >>> container.simultaneous is None
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

            >>> container.simultaneous = True
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

    @simultaneous.setter
    def simultaneous(self, argument):
        if argument is None:
            return
        assert isinstance(argument, bool), repr(argument)
        if argument and not all(isinstance(_, Container) for _ in self):
            message = "simultaneous containers must contain"
            message += " only other containers."
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
        for parent in inspect(self).parentage()[1:]:
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
        elif isinstance(argument, collections.abc.Iterable):
            argument_ = []
            for item in argument:
                if isinstance(item, str):
                    item = self._parse_string(item)
                argument_.append(item)
            argument = argument_
        self.__setitem__(
            slice(len(self), len(self)), argument.__getitem__(slice(0, len(argument))),
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
            message = f"component {component!r} not in container {self!r}."
            raise ValueError(message)

    def insert(self, i, component) -> None:
        r"""
        Inserts ``component`` at index ``i`` in container.

        ..  container:: example

            Inserts note.

            >>> container = abjad.Container([])
            >>> container.extend("fs16 cs' e' a'")
            >>> container.extend("cs''16 e'' cs'' a'")
            >>> container.extend("fs'16 e' cs' fs")
            >>> start_slur = abjad.StartSlur(direction=abjad.Down)
            >>> abjad.slur(container[:], start_slur=start_slur)
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

            >>> container.insert(-4, abjad.Note("e'4"))
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

        """
        assert isinstance(i, int)
        if isinstance(component, str):
            selection = self._parse_string(component)
            assert len(selection) == 1, repr(selection)
            component = selection[0]
        self.__setitem__(slice(i, i), [component])
        return

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
        del self[i]
        return component

    def remove(self, component) -> None:
        r"""
        Removes ``component`` from container.

        ..  container:: example

            Removes note from container:

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

            >>> note = container[2]
            >>> note
            Note("f'4")

            >>> container.remove(note)
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'4
                    d'4
                    e'4
                }

        """
        i = self.index(component)
        del self[i]
