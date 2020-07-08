import collections
import typing

from .. import exceptions
from ..bundle import LilyPondFormatBundle
from ..duration import Duration
from ..storage import FormatSpecification
from ..tags import Tag
from .Component import Component


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

            >>> abjad.wellformed(voice)
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

            >>> abjad.wellformed(tuplet_1)
            True

        Returns none.
        """
        result = self[i]
        if isinstance(result, Component):
            result._set_parent(None)
            return
        for component in result:
            component._set_parent(None)

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        Traverses top-level items only.
        """
        from ..selectx import Selection

        if isinstance(argument, int):
            return self.components.__getitem__(argument)
        elif isinstance(argument, slice):
            return Selection(self.components.__getitem__(argument))
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

    # TODO: teach uqbar about iox._graph_container() and remove Container.__graph__()
    def __graph__(self, **keywords):
        """
        Graphviz graph representation of container.

        Returns Graphviz graph.
        """
        from ..iox import _graph_container

        return _graph_container(self)

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
        self._set_item(i, argument)

    ### PRIVATE METHODS ###

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
        if self._parent is not None:
            raise Exception("can not eject contents of in-score container.")
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
            brackets_close = Tag.tag(brackets_close, tag=self.tag)
        result.append([("close brackets", ""), brackets_close])
        return tuple(result)

    def _format_closing_slot(self, bundle):
        result = []
        result.append(("grob reverts", bundle.grob_reverts))
        result.append(("commands", bundle.closing.commands))
        result.append(("comments", bundle.closing.comments))
        return self._format_slot_contributions_with_indent(result)

    def _format_content_pieces(self):
        indent = LilyPondFormatBundle.indent
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
            brackets_open = Tag.tag(brackets_open, tag=self.tag)
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
            for component in self:
                duration += component._get_preprolated_duration()
            return duration

    def _get_contents_summary(self):
        if 0 < len(self):
            result = []
            for component in self.components:
                if hasattr(component, "_get_compact_representation"):
                    result.append(component._get_compact_representation())
                else:
                    result.append(str(component))
            return " ".join(result)
        else:
            return ""

    def _get_descendants_starting_with(self):
        result = []
        result.append(self)
        if self.simultaneous:
            for x in self:
                result.extend(x._get_descendants_starting_with())
        elif self:
            result.extend(self[0]._get_descendants_starting_with())
        return result

    def _get_descendants_stopping_with(self):
        result = []
        result.append(self)
        if self.simultaneous:
            for x in self:
                result.extend(x._get_descendants_stopping_with())
        elif self:
            result.extend(self[-1]._get_descendants_stopping_with())
        return result

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

    def _get_preprolated_duration(self):
        return self._get_contents_duration()

    def _get_repr_kwargs_names(self):
        return ["simultaneous", "name"]

    def _get_subtree(self):
        result = [self]
        for component in self:
            result.extend(component._get_subtree())
        return result

    def _initialize_components(self, components):
        if isinstance(components, collections.abc.Iterable) and not isinstance(
            components, str
        ):
            components_ = []
            for item in components:
                if hasattr(item, "_items"):
                    components_.extend(item)
                elif isinstance(item, str):
                    parsed = self._parse_string(item)
                    components_.append(parsed)
                else:
                    components_.append(item)
            components = components_
            for component in components:
                if not isinstance(component, Component):
                    raise Exception(f"must be component: {component!r}.")
        if isinstance(components, str):
            parsed = self._parse_string(components)
            self._components = []
            self.simultaneous = parsed.simultaneous
            self[:] = parsed[:]
        else:
            for component in components:
                if component._parent is not None:
                    raise Exception(f"must not have parent: {component!r}.")
            self._components = list(components)
            self[:]._set_parents(self)

    def _is_one_of_my_first_leaves(self, leaf):
        return leaf in self._get_descendants_starting_with()

    def _is_one_of_my_last_leaves(self, leaf):
        return leaf in self._get_descendants_stopping_with()

    def _parse_string(self, string):
        user_input = string.strip()
        if not user_input.startswith("<<") or not user_input.endswith(">>"):
            user_input = f"{{ {user_input} }}"
        parsed = self._parse_lilypond_string(user_input)
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
        for item in list(self):
            item._scale(multiplier)

    def _set_item(self, i, argument):
        argument_wrappers = []
        for component in self._get_components(argument):
            wrappers = component._get_indicators(unwrap=False)
            argument_wrappers.extend(wrappers)
        if isinstance(i, int):
            argument = [argument]
            if i < 0:
                i = len(self) + i
            i = slice(i, i + 1)
        new_argument = []
        for item in argument:
            if hasattr(item, "_items"):
                new_argument.extend(item)
            else:
                new_argument.append(item)
        argument = new_argument
        assert all(isinstance(_, Component) for _ in argument)
        if any(hasattr(_, "_main_leaf") for _ in argument):
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
        for wrapper in argument_wrappers:
            wrapper._update_effective_context()

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
        parent = self._parent
        while parent is not None:
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
            parent = parent._parent
        self._name = argument

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
            raise ValueError(f"component {component!r} not in container {self!r}.")

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
