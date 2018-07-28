import collections
from abjad import enums
from abjad.system.AbjadObject import AbjadObject


class Iteration(AbjadObject):
    r"""
    Iteration.

    ..  container:: example

        Iterates leaves:

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    e'4
                    d'4
                    f'4
                }

        ..  container:: example

            >>> for leaf in abjad.iterate(staff).leaves():
            ...     leaf
            Note("c'4")
            Note("e'4")
            Note("d'4")
            Note("f'4")

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Collaborators'

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client=None):
        assert not isinstance(client, str), repr(client)
        self._client = client

    ### PRIVATE METHODS ###

    def _depth_first(
        self,
        capped=True,
        direction=None,
        forbid=None,
        unique=True,
        ):
        r"""
        Iterates depth first.

        ..  container:: example

            Iterates depth first:

            ..  container:: example

                >>> score = abjad.Score([])
                >>> score.append(abjad.Staff("c''4 ~ c''8 d''8 r4 ef''4"))
                >>> score.append(abjad.Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8"))
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            c''4
                            ~
                            c''8
                            d''8
                            r4
                            ef''4
                        }
                        \new Staff
                        {
                            r8
                            g'4.
                            ~
                            g'8
                            r16
                            f'8.
                            ~
                            f'8
                        }
                    >>

            ..  container:: example

                >>> for component in abjad.iterate(score)._depth_first():
                ...     component
                ...
                <Score<<2>>>
                Staff("c''4 ~ c''8 d''8 r4 ef''4")
                Note("c''4")
                Note("c''8")
                Note("d''8")
                Rest('r4')
                Note("ef''4")
                Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8")
                Rest('r8')
                Note("g'4.")
                Note("g'8")
                Rest('r16')
                Note("f'8.")
                Note("f'8")

        ..  container:: example

            Iterates depth first in reverse:

            ..  container:: example

                >>> score = abjad.Score([])
                >>> score.append(abjad.Staff("c''4 ~ c''8 d''8 r4 ef''4"))
                >>> score.append(abjad.Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8"))
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            c''4
                            ~
                            c''8
                            d''8
                            r4
                            ef''4
                        }
                        \new Staff
                        {
                            r8
                            g'4.
                            ~
                            g'8
                            r16
                            f'8.
                            ~
                            f'8
                        }
                    >>

            ..  container:: example

                >>> agent = abjad.iterate(score)
                >>> for component in agent._depth_first(direction=abjad.Right):
                ...     component
                ...
                <Score<<2>>>
                Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8")
                Note("f'8")
                Note("f'8.")
                Rest('r16')
                Note("g'8")
                Note("g'4.")
                Rest('r8')
                Staff("c''4 ~ c''8 d''8 r4 ef''4")
                Note("ef''4")
                Rest('r4')
                Note("d''8")
                Note("c''8")
                Note("c''4")

        ..  container:: example

            Iterates depth first with grace notes:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
                        \grace {
                            cf''16
                            bf'16
                        }
                        \afterGrace
                        d'8
                        {
                            af'16
                            gf'16
                        }
                        e'8
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for component in abjad.iterate(voice)._depth_first():
                ...     component
                ...
                Voice("c'8 d'8 e'8 f'8")
                Note("c'8")
                Note("d'8")
                GraceContainer("cf''16 bf'16")
                Note("cf''16")
                Note("bf'16")
                AfterGraceContainer("af'16 gf'16")
                Note("af'16")
                Note("gf'16")
                Note("e'8")
                Note("f'8")

        Returns generator.
        """
        import abjad
        if direction is None:
            direction = enums.Left
        def _next_node_depth_first(component, total):
            """
            If client has unvisited components, return next unvisited
            component in client.

            If client has no univisited components, return client's parent.
            """
            # if component is a container with not-yet-returned children
            if (isinstance(component, abjad.Container) and
                0 < len(component) and total < len(component)):
                # return next not-yet-returned child
                return component[total], 0
            # if component is a leaf with grace container attached
            elif getattr(component, '_grace_container', None) is not None:
                return component._grace_container, 0
            # if component is a leaf with after grace container attached
            elif (getattr(component, '_after_grace_container', None)
                is not None):
                return component._after_grace_container, 0
            # if component is grace container with all children returned
            elif hasattr(component, '_carrier'):
                carrier = component._carrier
                # if grace container has no carrier
                if carrier is None:
                    return None, None
                # if there's also an after grace container
                if (not isinstance(component, abjad.AfterGraceContainer) and
                    carrier._after_grace_container is not None):
                    return carrier._after_grace_container, 0
                carrier_parent = carrier._parent
                if carrier_parent is None:
                    return None, None
                # advance to next node in carrier parent
                return carrier_parent, carrier_parent.index(carrier) + 1
            else:
                parent = component._parent
                if parent is None:
                    return None, None
                return parent, parent.index(component) + 1
        def _previous_node_depth_first(component, total=0):
            """
            If client has unvisited components, return previous unvisited
            component in client.

            If client has no univisited components, return client's parent.
            """
            if (isinstance(component, abjad.Container) and
                0 < len(component) and total < len(component)):
                return component[len(component) - 1 - total], 0
            else:
                parent = component._parent
                if parent is not None:
                    return parent, len(parent) - parent.index(component)
                else:
                    return None, None
        def _handle_forbidden_node(node, queue):
            node_parent = node._parent
            if node_parent is not None:
                rank = node_parent.index(node) + 1
                node = node_parent
            else:
                node, rank = None, None
            queue.pop()
            return node, rank
        def _advance_node_depth_first(node, rank, direction):
            if direction is enums.Left:
                node, rank = _next_node_depth_first(node, rank)
            else:
                node, rank = _previous_node_depth_first(node, rank)
            return node, rank
        def _is_node_forbidden(node, forbid):
            if forbid is None:
                return False
            elif forbid == 'simultaneous':
                return getattr(node, 'is_simultaneous', False)
            else:
                return isinstance(node, forbid)
        def _find_yield(node, rank, queue, unique):
            if hasattr(node, 'components'):
                try:
                    visited = node is queue[-1]
                except IndexError:
                    visited = False
                if not visited or unique is not True:
                    queue.append(node)
                    return node
                elif rank == len(node):
                    queue.pop()
                    return None
            else:
                return node
        assert isinstance(self.client, abjad.Component)
        component = self.client
        client_parent, node, rank = component._parent, component, 0
        queue = collections.deque([])
        while node is not None and not (capped and node is client_parent):
            result = _find_yield(node, rank, queue, unique)
            if result is not None:
                yield result
            if _is_node_forbidden(node, forbid):
                node, rank = _handle_forbidden_node(node, queue)
            else:
                node, rank = _advance_node_depth_first(
                    node, rank, direction)
        queue.clear()

    def _logical_voice(self, prototype=None, reverse=False):
        r"""
        Iterates logical voice.

        ..  container:: example

            Iterates logical voice from first leaf in score:

            ..  container:: example

                >>> container_1 = abjad.Container([
                ...     abjad.Voice("c'8 d'8"),
                ...     abjad.Voice("e'8 f'8"),
                ...     ])
                >>> container_1.is_simultaneous = True
                >>> container_1[0].name = 'Voice 1'
                >>> abjad.override(container_1[0]).stem.direction = abjad.Down
                >>> container_1[1].name = 'Voice 2'
                >>> container_2 = abjad.Container([
                ...     abjad.Voice("g'8 a'8"),
                ...     abjad.Voice("b'8 c''8"),
                ...     ])
                >>> container_2.is_simultaneous = True
                >>> container_2[0].name = 'Voice 1'
                >>> abjad.override(container_2[0]).stem.direction = abjad.Down
                >>> container_2[1].name = 'Voice 2'
                >>> staff = abjad.Staff([container_1, container_2])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        <<
                            \context Voice = "Voice 1"
                            \with
                            {
                                \override Stem.direction = #down
                            }
                            {
                                c'8
                                d'8
                            }
                            \context Voice = "Voice 2"
                            {
                                e'8
                                f'8
                            }
                        >>
                        <<
                            \context Voice = "Voice 1"
                            \with
                            {
                                \override Stem.direction = #down
                            }
                            {
                                g'8
                                a'8
                            }
                            \context Voice = "Voice 2"
                            {
                                b'8
                                c''8
                            }
                        >>
                    }

            ..  container:: example

                >>> selector = abjad.select().leaves()
                >>> leaves = selector(staff)
                >>> leaf = leaves[0]
                >>> for note in abjad.iterate(leaf)._logical_voice(
                ...     prototype=abjad.Note,
                ...     ):
                ...     note
                ...
                Note("c'8")
                Note("d'8")
                Note("g'8")
                Note("a'8")

        ..  container:: example

            Iterates logical voice from second leaf in score:

                >>> container_1 = abjad.Container([
                ...     abjad.Voice("c'8 d'8"),
                ...     abjad.Voice("e'8 f'8"),
                ...     ])
                >>> container_1.is_simultaneous = True
                >>> container_1[0].name = 'Voice 1'
                >>> abjad.override(container_1[0]).stem.direction = abjad.Down
                >>> container_1[1].name = 'Voice 2'
                >>> container_2 = abjad.Container([
                ...     abjad.Voice("g'8 a'8"),
                ...     abjad.Voice("b'8 c''8"),
                ...     ])
                >>> container_2.is_simultaneous = True
                >>> container_2[0].name = 'Voice 1'
                >>> abjad.override(container_2[0]).stem.direction = abjad.Down
                >>> container_2[1].name = 'Voice 2'
                >>> staff = abjad.Staff([container_1, container_2])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        <<
                            \context Voice = "Voice 1"
                            \with
                            {
                                \override Stem.direction = #down
                            }
                            {
                                c'8
                                d'8
                            }
                            \context Voice = "Voice 2"
                            {
                                e'8
                                f'8
                            }
                        >>
                        <<
                            \context Voice = "Voice 1"
                            \with
                            {
                                \override Stem.direction = #down
                            }
                            {
                                g'8
                                a'8
                            }
                            \context Voice = "Voice 2"
                            {
                                b'8
                                c''8
                            }
                        >>
                    }

            ..  container:: example

                >>> leaf = leaves[1]
                >>> agent = abjad.iterate(leaf)
                >>> for note in agent._logical_voice(
                ...     prototype=abjad.Note,
                ...     ):
                ...     note
                ...
                Note("d'8")
                Note("g'8")
                Note("a'8")

        ..  container:: example

            Iterates all components in logical voice:

            ..  container:: example

                >>> container_1 = abjad.Container([
                ...     abjad.Voice("c'8 d'8"),
                ...     abjad.Voice("e'8 f'8"),
                ...     ])
                >>> container_1.is_simultaneous = True
                >>> container_1[0].name = 'Voice 1'
                >>> abjad.override(container_1[0]).stem.direction = abjad.Down
                >>> container_1[1].name = 'Voice 2'
                >>> container_2 = abjad.Container([
                ...     abjad.Voice("g'8 a'8"),
                ...     abjad.Voice("b'8 c''8"),
                ...     ])
                >>> container_2.is_simultaneous = True
                >>> container_2[0].name = 'Voice 1'
                >>> abjad.override(container_2[0]).stem.direction = abjad.Down
                >>> container_2[1].name = 'Voice 2'
                >>> staff = abjad.Staff([container_1, container_2])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        <<
                            \context Voice = "Voice 1"
                            \with
                            {
                                \override Stem.direction = #down
                            }
                            {
                                c'8
                                d'8
                            }
                            \context Voice = "Voice 2"
                            {
                                e'8
                                f'8
                            }
                        >>
                        <<
                            \context Voice = "Voice 1"
                            \with
                            {
                                \override Stem.direction = #down
                            }
                            {
                                g'8
                                a'8
                            }
                            \context Voice = "Voice 2"
                            {
                                b'8
                                c''8
                            }
                        >>
                    }

            ..  container:: example

                >>> leaf = leaves[0]
                >>> for component in abjad.iterate(leaf)._logical_voice():
                ...     component
                ...
                Note("c'8")
                Voice("c'8 d'8", name='Voice 1')
                Note("d'8")
                Voice("g'8 a'8", name='Voice 1')
                Note("g'8")
                Note("a'8")

        ..  container:: example

            Iterates all components in logical voice in reverse:

            ..  container:: example

                >>> container_1 = abjad.Container([
                ...     abjad.Voice("c'8 d'8"),
                ...     abjad.Voice("e'8 f'8"),
                ...     ])
                >>> container_1.is_simultaneous = True
                >>> container_1[0].name = 'Voice 1'
                >>> abjad.override(container_1[0]).stem.direction = abjad.Down
                >>> container_1[1].name = 'Voice 2'
                >>> container_2 = abjad.Container([
                ...     abjad.Voice("g'8 a'8"),
                ...     abjad.Voice("b'8 c''8"),
                ...     ])
                >>> container_2.is_simultaneous = True
                >>> container_2[0].name = 'Voice 1'
                >>> abjad.override(container_2[0]).stem.direction = abjad.Down
                >>> container_2[1].name = 'Voice 2'
                >>> staff = abjad.Staff([container_1, container_2])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        <<
                            \context Voice = "Voice 1"
                            \with
                            {
                                \override Stem.direction = #down
                            }
                            {
                                c'8
                                d'8
                            }
                            \context Voice = "Voice 2"
                            {
                                e'8
                                f'8
                            }
                        >>
                        <<
                            \context Voice = "Voice 1"
                            \with
                            {
                                \override Stem.direction = #down
                            }
                            {
                                g'8
                                a'8
                            }
                            \context Voice = "Voice 2"
                            {
                                b'8
                                c''8
                            }
                        >>
                    }

            ..  container:: example

                >>> leaf = leaves[-1]
                >>> for note in abjad.iterate(leaf)._logical_voice(
                ...     prototype=abjad.Note,
                ...     reverse=True,
                ...     ):
                ...     note
                ...
                Note("c''8")
                Note("b'8")
                Note("f'8")
                Note("e'8")

                >>> leaf = leaves[-1]
                >>> for component in abjad.iterate(leaf)._logical_voice(
                ...     reverse=True,
                ...     ):
                ...     component
                ...
                Note("c''8")
                Voice("b'8 c''8", name='Voice 2')
                Note("b'8")
                Voice("e'8 f'8", name='Voice 2')
                Note("f'8")
                Note("e'8")

        Returns generator.
        """
        import abjad
        prototype = prototype or abjad.Component
        parentage = abjad.inspect(self.client).parentage()
        logical_voice = parentage.logical_voice
        if reverse:
            direction = enums.Right
        else:
            direction = enums.Left
        for component in abjad.iterate(self.client)._depth_first(
            capped=False,
            direction=direction,
            ):
            if not isinstance(component, prototype):
                continue
            parentage = abjad.inspect(component).parentage()
            if parentage.logical_voice == logical_voice:
                yield component

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        """
        Gets client.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.iterate(staff[:2]).client
            Selection([Note("c'4"), Note("d'4")])

        Returns component or selection.
        """
        return self._client

    ### PUBLIC METHODS ###

    def components(self, prototype=None, grace_notes=None, reverse=False):
        r"""
        Iterates components.

        ..  container:: example

            Iterates notes:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> staff.append(abjad.Measure((2, 8), "c'8 d'8"))
                >>> staff.append(abjad.Measure((2, 8), "e'8 f'8"))
                >>> staff.append(abjad.Measure((2, 8), "g'8 a'8"))
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        {   % measure
                            \time 2/8
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
                    }

            ..  container:: example

                >>> agent = abjad.iterate(staff)
                >>> for note in agent.components(prototype=abjad.Note):
                ...     note
                ...
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Note("g'8")
                Note("a'8")

        ..  container:: example

            Iterates grace notes and nongrace notes:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
                        \grace {
                            cf''16
                            bf'16
                        }
                        \afterGrace
                        d'8
                        {
                            af'16
                            gf'16
                        }
                        e'8
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for component in abjad.iterate(voice).components():
                ...     component
                ...
                Voice("c'8 d'8 e'8 f'8")
                Note("c'8")
                Note("cf''16")
                Note("bf'16")
                Note("d'8")
                Note("af'16")
                Note("gf'16")
                Note("e'8")
                Note("f'8")

        ..  container:: example

            Iterates components in reverse:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
                        \grace {
                            cf''16
                            bf'16
                        }
                        \afterGrace
                        d'8
                        {
                            af'16
                            gf'16
                        }
                        e'8
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for component in abjad.iterate(voice).components(
                ...     reverse=True,
                ...     ):
                ...     component
                ...
                Voice("c'8 d'8 e'8 f'8")
                Note("f'8")
                Note("e'8")
                Note("gf'16")
                Note("af'16")
                Note("d'8")
                Note("bf'16")
                Note("cf''16")
                Note("c'8")

        Returns generator.
        """
        import abjad
        argument = self.client
        prototype = prototype or abjad.Component
        grace_container, after_grace_container = None, None
        if grace_notes is not False and isinstance(argument, abjad.Leaf):
            inspection = abjad.inspect(argument)
            grace_container = inspection.grace_container()
            after_grace_container = inspection.after_grace_container()
        if not reverse:
            if grace_notes is not False and grace_container:
                for component in grace_container:
                    for component_ in abjad.iterate(component).components(
                        prototype,
                        grace_notes=grace_notes,
                        reverse=reverse,
                        ):
                        yield component_
            if isinstance(argument, prototype):
                if (grace_notes is None or
                    (grace_notes is True and
                    abjad.inspect(argument).is_grace_note()) or
                    (grace_notes is False and
                    not abjad.inspect(argument).is_grace_note())):
                    yield argument
            if grace_notes is not False and after_grace_container:
                for component in after_grace_container:
                    for component_ in abjad.iterate(component).components(
                        prototype,
                        grace_notes=grace_notes,
                        reverse=reverse,
                        ):
                        yield component_
            if isinstance(argument, collections.Iterable):
                for item in argument:
                    for component in abjad.iterate(item).components(
                        prototype,
                        grace_notes=grace_notes,
                        reverse=reverse,
                        ):
                        yield component
        else:
            if grace_notes is not False and after_grace_container:
                for component in reversed(after_grace_container):
                    for component_ in abjad.iterate(component).components(
                        prototype,
                        grace_notes=grace_notes,
                        reverse=reverse,
                        ):
                        yield component_
            if isinstance(argument, prototype):
                if (grace_notes is None or
                    (grace_notes is True and
                    abjad.inspect(argument).is_grace_note()) or
                    (grace_notes is False and
                    not abjad.inspect(argument).is_grace_note())):
                    yield argument
            if grace_notes is not False and grace_container:
                for component in reversed(grace_container):
                    for component_ in abjad.iterate(component).components(
                        prototype,
                        grace_notes=grace_notes,
                        reverse=reverse,
                        ):
                        yield component_
            if isinstance(argument, collections.Iterable):
                for item in reversed(argument):
                    for component in abjad.iterate(item).components(
                        prototype,
                        grace_notes=grace_notes,
                        reverse=reverse,
                        ):
                        yield component

    def leaf_pairs(self):
        r"""
        Iterates leaf pairs.

        ..  container:: example

            Iterates leaf pairs:

            ..  container:: example

                >>> score = abjad.Score()
                >>> score.append(abjad.Staff("c'8 d'8 e'8 f'8 g'4"))
                >>> score.append(abjad.Staff("c4 a,4 g,4"))
                >>> abjad.attach(abjad.Clef('bass'), score[1][0])
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            c'8
                            d'8
                            e'8
                            f'8
                            g'4
                        }
                        \new Staff
                        {
                            \clef "bass"
                            c4
                            a,4
                            g,4
                        }
                    >>

            ..  container:: example

                >>> for leaf_pair in abjad.iterate(score).leaf_pairs():
                ...     leaf_pair
                ...
                Selection([Note("c'8"), Note('c4')])
                Selection([Note("c'8"), Note("d'8")])
                Selection([Note('c4'), Note("d'8")])
                Selection([Note("d'8"), Note("e'8")])
                Selection([Note("d'8"), Note('a,4')])
                Selection([Note('c4'), Note("e'8")])
                Selection([Note('c4'), Note('a,4')])
                Selection([Note("e'8"), Note('a,4')])
                Selection([Note("e'8"), Note("f'8")])
                Selection([Note('a,4'), Note("f'8")])
                Selection([Note("f'8"), Note("g'4")])
                Selection([Note("f'8"), Note('g,4')])
                Selection([Note('a,4'), Note("g'4")])
                Selection([Note('a,4'), Note('g,4')])
                Selection([Note("g'4"), Note('g,4')])

        Iterates leaf pairs left-to-right and top-to-bottom.

        Returns generator.
        """
        import abjad
        vertical_moments = self.vertical_moments()
        for moment_1, moment_2 in abjad.sequence(vertical_moments).nwise():
            enumerator = abjad.Enumerator(moment_1.start_leaves)
            for pair in enumerator.yield_pairs():
                yield abjad.select(pair)
            sequences = [moment_1.leaves, moment_2.start_leaves]
            enumerator = abjad.Enumerator(sequences)
            for pair in enumerator.yield_outer_product():
                yield abjad.select(pair)
        else:
            enumerator = abjad.Enumerator(moment_2.start_leaves)
            for pair in enumerator.yield_pairs():
                yield abjad.select(pair)

    def leaves(
        self,
        prototype=None,
        grace_notes=None,
        pitched=None,
        reverse=False,
        ):
        r"""
        Iterates leaves.

        ..  container:: example

            Iterates leaves:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
                >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        {   % measure
                            \time 2/8
                            <c' bf'>8
                            <g' a'>8
                        }   % measure
                        {   % measure
                            af'8
                            r8
                        }   % measure
                        {   % measure
                            r8
                            gf'8
                        }   % measure
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(staff).leaves():
                ...     leaf
                ...
                Chord("<c' bf'>8")
                Chord("<g' a'>8")
                Note("af'8")
                Rest('r8')
                Rest('r8')
                Note("gf'8")

        ..  container:: example

            Iterates grace notes and nongrace notes:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
                        \grace {
                            cf''16
                            bf'16
                        }
                        \afterGrace
                        d'8
                        {
                            af'16
                            gf'16
                        }
                        e'8
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(voice).leaves():
                ...     leaf
                ...
                Note("c'8")
                Note("cf''16")
                Note("bf'16")
                Note("d'8")
                Note("af'16")
                Note("gf'16")
                Note("e'8")
                Note("f'8")

        ..  container:: example

            Iterates grace notes only:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
                        \grace {
                            cf''16
                            bf'16
                        }
                        \afterGrace
                        d'8
                        {
                            af'16
                            gf'16
                        }
                        e'8
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(voice).leaves(grace_notes=True):
                ...     leaf
                ...
                Note("cf''16")
                Note("bf'16")
                Note("af'16")
                Note("gf'16")

        ..  container:: example

            Iterates nongrace notes only:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
                        \grace {
                            cf''16
                            bf'16
                        }
                        \afterGrace
                        d'8
                        {
                            af'16
                            gf'16
                        }
                        e'8
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(voice).leaves(grace_notes=False):
                ...     leaf
                ...
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Note("f'8")

        ..  container:: example

            Iterates pitched leaves only:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
                >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        {   % measure
                            \time 2/8
                            <c' bf'>8
                            <g' a'>8
                        }   % measure
                        {   % measure
                            af'8
                            r8
                        }   % measure
                        {   % measure
                            r8
                            gf'8
                        }   % measure
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(staff).leaves(pitched=True):
                ...     leaf
                ...
                Chord("<c' bf'>8")
                Chord("<g' a'>8")
                Note("af'8")
                Note("gf'8")

        ..  container:: example

            Iterates nonpitched leaves only:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
                >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        {   % measure
                            \time 2/8
                            <c' bf'>8
                            <g' a'>8
                        }   % measure
                        {   % measure
                            af'8
                            r8
                        }   % measure
                        {   % measure
                            r8
                            gf'8
                        }   % measure
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(staff).leaves(pitched=False):
                ...     leaf
                ...
                Rest('r8')
                Rest('r8')

        ..  container:: example

            Iterates leaves in reverse:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
                >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        {   % measure
                            \time 2/8
                            <c' bf'>8
                            <g' a'>8
                        }   % measure
                        {   % measure
                            af'8
                            r8
                        }   % measure
                        {   % measure
                            r8
                            gf'8
                        }   % measure
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(staff).leaves(reverse=True):
                ...     leaf
                ...
                Note("gf'8")
                Rest('r8')
                Rest('r8')
                Note("af'8")
                Chord("<g' a'>8")
                Chord("<c' bf'>8")

        Returns generator.
        """
        import abjad
        prototype = prototype or abjad.Leaf
        if pitched is True:
            prototype = (abjad.Chord, abjad.Note)
        elif pitched is False:
            prototype = (abjad.MultimeasureRest, abjad.Rest, abjad.Skip)
        return self.components(
            prototype=prototype,
            grace_notes=grace_notes,
            reverse=reverse,
            )

    def logical_ties(
        self,
        grace_notes=None,
        nontrivial=None,
        pitched=None,
        reverse=False,
        ):
        r"""
        Iterates logical ties.

        ..  container:: example

            Iterates logical ties:

            ..  container:: example

                >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                >>> staff = abjad.Staff(string)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4
                        ~
                        \times 2/3 {
                            c'16
                            d'8
                        }
                        e'8
                        f'4
                        ~
                        f'16
                    }

            ..  container:: example

                >>> for logical_tie in abjad.iterate(staff).logical_ties():
                ...     logical_tie
                ...
                LogicalTie([Note("c'4"), Note("c'16")])
                LogicalTie([Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'4"), Note("f'16")])

        ..  container:: example

            Iterates pitched logical ties:

            ..  container:: example

                >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                >>> staff = abjad.Staff(string)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4
                        ~
                        \times 2/3 {
                            c'16
                            d'8
                        }
                        e'8
                        f'4
                        ~
                        f'16
                    }

            ..  container:: example

                >>> for logical_tie in abjad.iterate(staff).logical_ties(
                ...     pitched=True,
                ...     ):
                ...     logical_tie
                ...
                LogicalTie([Note("c'4"), Note("c'16")])
                LogicalTie([Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'4"), Note("f'16")])

        ..  container:: example

            Iterates nontrivial logical ties:

            ..  container:: example

                >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                >>> staff = abjad.Staff(string)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4
                        ~
                        \times 2/3 {
                            c'16
                            d'8
                        }
                        e'8
                        f'4
                        ~
                        f'16
                    }

            ..  container:: example

                >>> for logical_tie in abjad.iterate(staff).logical_ties(
                ...     nontrivial=True,
                ...     ):
                ...     logical_tie
                ...
                LogicalTie([Note("c'4"), Note("c'16")])
                LogicalTie([Note("f'4"), Note("f'16")])

        ..  container:: example

            Iterates trivial logical ties:

            ..  container:: example

                >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                >>> staff = abjad.Staff(string)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4
                        ~
                        \times 2/3 {
                            c'16
                            d'8
                        }
                        e'8
                        f'4
                        ~
                        f'16
                    }

            ..  container:: example

                >>> for logical_tie in abjad.iterate(staff).logical_ties(
                ...     nontrivial=False,
                ...     ):
                ...     logical_tie
                ...
                LogicalTie([Note("d'8")])
                LogicalTie([Note("e'8")])

        ..  container:: example

            Iterates logical ties together with grace notes and after grace
            notes:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
                        \grace {
                            cf''16
                            bf'16
                        }
                        \afterGrace
                        d'8
                        {
                            af'16
                            gf'16
                        }
                        e'8
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for item in abjad.iterate(voice).logical_ties():
                ...     item
                ...
                LogicalTie([Note("c'8")])
                LogicalTie([Note("cf''16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Note("d'8")])
                LogicalTie([Note("af'16")])
                LogicalTie([Note("gf'16")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'8")])

        ..  container:: example

            Iterates logical ties in reverse:

            ..  container:: example

                >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                >>> staff = abjad.Staff(string)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4
                        ~
                        \times 2/3 {
                            c'16
                            d'8
                        }
                        e'8
                        f'4
                        ~
                        f'16
                    }

            ..  container:: example

                >>> for logical_tie in abjad.iterate(staff).logical_ties(
                ...     reverse=True,
                ...     ):
                ...     logical_tie
                ...
                LogicalTie([Note("f'4"), Note("f'16")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("d'8")])
                LogicalTie([Note("c'4"), Note("c'16")])

        ..  container:: example

            REGRESSION: yields logical tie even when leaves are missing in
            input:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ ~ c' ~ c' d' ]")
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        ~
                        [
                        c'8
                        ~
                        c'8
                        d'8
                        ]
                    }

            ..  container:: example

                >>> selection = voice[:2]
                >>> for logical_tie in abjad.iterate(selection).logical_ties():
                ...     logical_tie
                ...
                LogicalTie([Note("c'8"), Note("c'8"), Note("c'8")])

        Returns generator.
        """
        import abjad
        yielded_logical_ties = set()
        for leaf in self.leaves(
            pitched=pitched,
            grace_notes=grace_notes,
            reverse=reverse,
            ):
            logical_tie = abjad.inspect(leaf).logical_tie()
            if leaf is not logical_tie.head:
                continue
            if (nontrivial is None or
                (nontrivial is True and not logical_tie.is_trivial) or
                (nontrivial is False and logical_tie.is_trivial)):
                if logical_tie not in yielded_logical_ties:
                    yielded_logical_ties.add(logical_tie)
                    yield logical_tie

    def out_of_range(self):
        r"""
        Iterates out-of-range notes and chords.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 r8 <d fs>8 r8")
            >>> violin = abjad.Violin()
            >>> abjad.attach(violin, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    r8
                    <d fs>8
                    r8
                }

            >>> for leaf in abjad.iterate(staff).out_of_range():
            ...     leaf
            ...
            Chord('<d fs>8')

        Returns generator.
        """
        import abjad
        for leaf in abjad.iterate(self.client).leaves(pitched=True):
            instrument = abjad.inspect(leaf).effective(abjad.Instrument)
            if instrument is None:
                message = 'no instrument found.'
                raise ValueError(message)
            if leaf not in instrument.pitch_range:
                yield leaf

    def pitch_pairs(self):
        r"""
        Iterates pitch pairs.

        ..  container:: example

            Iterates note pitch pairs:

            ..  container:: example

                >>> score = abjad.Score()
                >>> score.append(abjad.Staff("c'8 d' e' f' g'4"))
                >>> score.append(abjad.Staff("c4 a, g,"))
                >>> abjad.attach(abjad.Clef('bass'), score[1][0])
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            c'8
                            d'8
                            e'8
                            f'8
                            g'4
                        }
                        \new Staff
                        {
                            \clef "bass"
                            c4
                            a,4
                            g,4
                        }
                    >>

            ..  container:: example

                >>> for pair in abjad.iterate(score).pitch_pairs():
                ...     pair
                ...
                PitchSegment("c' c")
                PitchSegment("c' d'")
                PitchSegment("c d'")
                PitchSegment("d' e'")
                PitchSegment("d' a,")
                PitchSegment("c e'")
                PitchSegment("c a,")
                PitchSegment("e' a,")
                PitchSegment("e' f'")
                PitchSegment("a, f'")
                PitchSegment("f' g'")
                PitchSegment("f' g,")
                PitchSegment("a, g'")
                PitchSegment("a, g,")
                PitchSegment("g' g,")

        ..  container:: example

            Iterates chord pitch pairs:

            ..  container:: example

                >>> staff = abjad.Staff("<c' d' e'>4 <f'' g''>4")

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        <c' d' e'>4
                        <f'' g''>4
                    }

            ..  container:: example

                >>> for pair in abjad.iterate(staff).pitch_pairs():
                ...     pair
                ...
                PitchSegment("c' d'")
                PitchSegment("c' e'")
                PitchSegment("d' e'")
                PitchSegment("c' f''")
                PitchSegment("c' g''")
                PitchSegment("d' f''")
                PitchSegment("d' g''")
                PitchSegment("e' f''")
                PitchSegment("e' g''")
                PitchSegment("f'' g''")

        Returns generator.
        """
        import abjad
        for leaf_pair in self.leaf_pairs():
            pitches = sorted(abjad.iterate(leaf_pair[0]).pitches())
            enumerator = abjad.Enumerator(pitches)
            for pair in enumerator.yield_pairs():
                yield abjad.PitchSegment(pair)
            if isinstance(leaf_pair, set):
                pitches = sorted(abjad.iterate(leaf_pair).pitches())
                enumerator = abjad.Enumerator(pitches)
                for pair in enumerator.yield_pairs():
                    yield abjad.PitchSegment(pair)
            else:
                pitches_1 = sorted(abjad.iterate(leaf_pair[0]).pitches())
                pitches_2 = sorted(abjad.iterate(leaf_pair[1]).pitches())
                sequences = [pitches_1, pitches_2]
                enumerator = abjad.Enumerator(sequences)
                for pair in enumerator.yield_outer_product():
                    yield abjad.PitchSegment(pair)
            pitches = sorted(abjad.iterate(leaf_pair[1]).pitches())
            enumerator = abjad.Enumerator(pitches)
            for pair in enumerator.yield_pairs():
                yield abjad.PitchSegment(pair)

    def pitches(self):
        r"""
        Iterates pitches.

        ..  container:: example

            Iterates pitches in container:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> beam = abjad.Beam()
                >>> abjad.attach(beam, staff[:])
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

            ..  container:: example

                >>> for pitch in abjad.iterate(staff).pitches():
                ...     pitch
                ...
                NamedPitch("c'")
                NamedPitch("d'")
                NamedPitch("e'")
                NamedPitch("f'")

        ..  container:: example

            Iterates pitches in spanner:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> beam = abjad.Beam()
                >>> abjad.attach(beam, staff[:])
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

            ..  container:: example

                >>> for pitch in abjad.iterate(beam).pitches():
                ...     pitch
                ...
                NamedPitch("c'")
                NamedPitch("d'")
                NamedPitch("e'")
                NamedPitch("f'")

        ..  container:: example

            Iterates pitches in pitch set:

            ..  container:: example

                >>> pitch_set = abjad.PitchSet([0, 2, 4, 5])

            ..  container:: example

                >>> for pitch in abjad.iterate(pitch_set).pitches():
                ...     pitch
                ...
                NumberedPitch(0)
                NumberedPitch(2)
                NumberedPitch(4)
                NumberedPitch(5)

        ..  container:: example

            Iterates different types of object in tuple:

            ..  container:: example

                >>> pitches = (
                ...     abjad.NamedPitch("c'"),
                ...     abjad.Note("d'4"),
                ...     abjad.Chord("<e' fs' g>4"),
                ...     )

            ..  container:: example

                >>> for pitch in abjad.iterate(pitches).pitches():
                ...     pitch
                ...
                NamedPitch("c'")
                NamedPitch("d'")
                NamedPitch('g')
                NamedPitch("e'")
                NamedPitch("fs'")

        Returns generator.
        """
        import abjad
        if isinstance(self.client, abjad.Pitch):
            pitch = abjad.NamedPitch(self.client)
            yield pitch
        result = []
        try:
            result.extend(self.client.pitches)
        except AttributeError:
            pass
        if isinstance(self.client, abjad.Chord):
            result.extend(self.client.written_pitches)
        elif isinstance(self.client, abjad.Spanner):
            for leaf in self.client.leaves:
                try:
                    result.append(leaf.written_pitch)
                except AttributeError:
                    pass
                try:
                    result.extedn(leaf.written_pitches)
                except AttributeError:
                    pass
        elif isinstance(self.client, abjad.PitchSet):
            result.extend(sorted(list(self.client)))
        elif isinstance(self.client, (list, tuple, set)):
            for item in self.client:
                for pitch_ in abjad.iterate(item).pitches():
                    result.append(pitch_)
        else:
            for leaf in abjad.iterate(self.client).leaves():
                try:
                    result.append(leaf.written_pitch)
                except AttributeError:
                    pass
                try:
                    result.extedn(leaf.written_pitches)
                except AttributeError:
                    pass
        for pitch in result:
            yield pitch

    def spanners(self, prototype=None, reverse=False):
        r"""
        Iterates spanners.

        ..  container:: example

            Iterates spanners:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 f'8 b'8 c''8")
                >>> abjad.attach(abjad.Slur(), staff[:4])
                >>> abjad.attach(abjad.Slur(), staff[4:])
                >>> abjad.attach(abjad.Beam(), staff[:])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'8
                        [
                        (
                        d'8
                        e'8
                        f'8
                        )
                        g'8
                        (
                        a'8
                        f'8
                        b'8
                        c''8
                        ]
                        )
                    }

            ..  container:: example

                >>> for spanner in abjad.iterate(staff).spanners():
                ...     spanner
                ...
                Beam("c'8, d'8, ... [5] ..., b'8, c''8", durations=(), span_beam_count=1)
                Slur("c'8, d'8, e'8, f'8")
                Slur("g'8, a'8, f'8, b'8, c''8")

        ..  container:: example

            Iterates spanners in reverse:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 f'8 b'8 c''8")
                >>> abjad.attach(abjad.Slur(), staff[:4])
                >>> abjad.attach(abjad.Slur(), staff[4:])
                >>> abjad.attach(abjad.Beam(), staff[:])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'8
                        [
                        (
                        d'8
                        e'8
                        f'8
                        )
                        g'8
                        (
                        a'8
                        f'8
                        b'8
                        c''8
                        ]
                        )
                    }

            ..  container:: example

                >>> for spanner in abjad.iterate(staff).spanners(reverse=True):
                ...     spanner
                ...
                Beam("c'8, d'8, ... [5] ..., b'8, c''8", durations=(), span_beam_count=1)
                Slur("g'8, a'8, f'8, b'8, c''8")
                Slur("c'8, d'8, e'8, f'8")

        Returns generator.
        """
        import abjad
        visited_spanners = set()
        for component in self.components(reverse=reverse):
            spanners = abjad.inspect(component).spanners(
                prototype=prototype,
                )
            spanners = sorted(spanners,
                key=lambda x: (
                    type(x).__name__,
                    abjad.inspect(x).timespan(),
                    ),
                )
            for spanner in spanners:
                if spanner in visited_spanners:
                    continue
                visited_spanners.add(spanner)
                yield spanner

    def timeline(self, prototype=None, reverse=False):
        r"""
        Iterates timeline.

        ..  container:: example

            Timeline-iterates leaves:

            ..  container:: example

                >>> score = abjad.Score()
                >>> score.append(abjad.Staff("c'4 d'4 e'4 f'4"))
                >>> score.append(abjad.Staff("g'8 a'8 b'8 c''8"))
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                        \new Staff
                        {
                            g'8
                            a'8
                            b'8
                            c''8
                        }
                    >>

            ..  container:: example

                >>> for leaf in abjad.iterate(score).timeline():
                ...     leaf
                ...
                Note("c'4")
                Note("g'8")
                Note("a'8")
                Note("d'4")
                Note("b'8")
                Note("c''8")
                Note("e'4")
                Note("f'4")

        ..  container:: example

            Timeline-iterates leaves in reverse:

            ..  container:: example

                >>> score = abjad.Score()
                >>> score.append(abjad.Staff("c'4 d'4 e'4 f'4"))
                >>> score.append(abjad.Staff("g'8 a'8 b'8 c''8"))
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                        \new Staff
                        {
                            g'8
                            a'8
                            b'8
                            c''8
                        }
                    >>

            ..  container:: example

                >>> for leaf in abjad.iterate(score).timeline(reverse=True):
                ...     leaf
                ...
                Note("f'4")
                Note("e'4")
                Note("d'4")
                Note("c''8")
                Note("b'8")
                Note("c'4")
                Note("a'8")
                Note("g'8")

        ..  container:: example

            Timeline-iterates leaves together grace notes:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
                        \grace {
                            cf''16
                            bf'16
                        }
                        d'8
                        e'8
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for component in abjad.iterate(voice).timeline():
                ...     component
                ...
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Note("f'8")

                ..  todo:: Incorrect because grace notes are not included.

        Iterates leaves when ``prototype`` is none.
        """
        import abjad
        prototype = prototype or abjad.Leaf
        if isinstance(self.client, abjad.Component):
            components = [self.client]
        else:
            components = list(self.client)
        if not reverse:
            while components:
                current_start_offset = min(
                    abjad.inspect(_).timespan().start_offset
                    for _ in components
                    )
                components.sort(
                    key=lambda x: abjad.inspect(x).parentage(
                        grace_notes=True).score_index,
                    reverse=True,
                    )
                components_to_process = components[:]
                components = []
                while components_to_process:
                    component = components_to_process.pop()
                    start_offset = abjad.inspect(component).timespan().start_offset
                    #print('    COMPONENT:', component)
                    if current_start_offset < start_offset:
                        components.append(component)
                        #print('        TOO EARLY')
                        continue
                    if isinstance(component, prototype):
                        #print('        YIELDING', component)
                        yield component
                    sibling = component._get_sibling(1)
                    if sibling is not None:
                        #print('        SIBLING:', sibling)
                        components.append(sibling)
                    if not isinstance(component, abjad.Container):
                        continue
                    if not len(component):
                        continue
                    if not component.is_simultaneous:
                        components_to_process.append(component[0])
                    else:
                        components_to_process.extend(reversed(component))
        else:
            while components:
                #print('STEP')
                #print()
                current_stop_offset = max(
                    abjad.inspect(_).timespan().stop_offset
                    for _ in components
                    )
                components.sort(
                    key=lambda x: abjad.inspect(x).parentage(
                        grace_notes=True).score_index,
                    reverse=True,
                    )
                components_to_process = components[:]
                components = []
                while components_to_process:
                    component = components_to_process.pop()
                    stop_offset = abjad.inspect(component).timespan().stop_offset
                    #print('\tCOMPONENT:', component)
                    if stop_offset < current_stop_offset:
                        components.insert(0, component)
                        continue
                    if isinstance(component, prototype):
                        yield component
                    sibling = component._get_sibling(-1)
                    if sibling is not None:
                        components.insert(0, sibling)
                    if not isinstance(component, abjad.Container):
                        continue
                    if not len(component):
                        continue
                    if not component.is_simultaneous:
                        components_to_process.append(component[-1])
                    else:
                        components_to_process.extend(reversed(component))

    def vertical_moments(self, reverse=False):
        r'''Iterates vertical moments.

        ..  container:: example

            Iterates vertical moments:

            ..  container:: example

                >>> score = abjad.Score([])
                >>> staff = abjad.Staff(r"\times 4/3 { d''8 c''8 b'8 }")
                >>> score.append(staff)
                >>> staff_group = abjad.StaffGroup([])
                >>> staff_group.lilypond_type = 'PianoStaff'
                >>> staff_group.append(abjad.Staff("a'4 g'4"))
                >>> staff_group.append(abjad.Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
                >>> score.append(staff_group)
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 4/3 {
                                d''8
                                c''8
                                b'8
                            }
                        }
                        \new PianoStaff
                        <<
                            \new Staff
                            {
                                a'4
                                g'4
                            }
                            \new Staff
                            {
                                \clef "bass"
                                f'8
                                e'8
                                d'8
                                c'8
                            }
                        >>
                    >>

            ..  container:: example

                >>> for vertical_moment in abjad.iterate(score).vertical_moments():
                ...     vertical_moment.leaves
                ...
                Selection([Note("d''8"), Note("a'4"), Note("f'8")])
                Selection([Note("d''8"), Note("a'4"), Note("e'8")])
                Selection([Note("c''8"), Note("a'4"), Note("e'8")])
                Selection([Note("c''8"), Note("g'4"), Note("d'8")])
                Selection([Note("b'8"), Note("g'4"), Note("d'8")])
                Selection([Note("b'8"), Note("g'4"), Note("c'8")])

                >>> for vertical_moment in abjad.iterate(staff_group).vertical_moments():
                ...     vertical_moment.leaves
                ...
                Selection([Note("a'4"), Note("f'8")])
                Selection([Note("a'4"), Note("e'8")])
                Selection([Note("g'4"), Note("d'8")])
                Selection([Note("g'4"), Note("c'8")])

        ..  container:: example

            Iterates vertical moments in reverse:

            ..  container:: example

                >>> score = abjad.Score([])
                >>> staff = abjad.Staff(r"\times 4/3 { d''8 c''8 b'8 }")
                >>> score.append(staff)
                >>> staff_group = abjad.StaffGroup([])
                >>> staff_group.lilypond_type = 'PianoStaff'
                >>> staff_group.append(abjad.Staff("a'4 g'4"))
                >>> staff_group.append(abjad.Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
                >>> score.append(staff_group)
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 4/3 {
                                d''8
                                c''8
                                b'8
                            }
                        }
                        \new PianoStaff
                        <<
                            \new Staff
                            {
                                a'4
                                g'4
                            }
                            \new Staff
                            {
                                \clef "bass"
                                f'8
                                e'8
                                d'8
                                c'8
                            }
                        >>
                    >>

            ..  container:: example

                >>> agent = abjad.iterate(score)
                >>> for vertical_moment in agent.vertical_moments(
                ...     reverse=True,
                ...     ):
                ...     vertical_moment.leaves
                ...
                Selection([Note("b'8"), Note("g'4"), Note("c'8")])
                Selection([Note("b'8"), Note("g'4"), Note("d'8")])
                Selection([Note("c''8"), Note("g'4"), Note("d'8")])
                Selection([Note("c''8"), Note("a'4"), Note("e'8")])
                Selection([Note("d''8"), Note("a'4"), Note("e'8")])
                Selection([Note("d''8"), Note("a'4"), Note("f'8")])

                >>> agent = abjad.iterate(staff_group)
                >>> for vertical_moment in agent.vertical_moments(
                ...     reverse=True,
                ...     ):
                ...     vertical_moment.leaves
                ...
                Selection([Note("g'4"), Note("c'8")])
                Selection([Note("g'4"), Note("d'8")])
                Selection([Note("a'4"), Note("e'8")])
                Selection([Note("a'4"), Note("f'8")])

        Returns generator.
        '''
        import abjad
        def _buffer_components_starting_with(component, buffer, stop_offsets):
            buffer.append(component)
            stop_offset = abjad.inspect(component).timespan().stop_offset
            stop_offsets.append(stop_offset)
            if isinstance(component, abjad.Container):
                if component.is_simultaneous:
                    for component_ in component:
                        _buffer_components_starting_with(
                            component_,
                            buffer,
                            stop_offsets,
                            )
                elif component:
                    _buffer_components_starting_with(
                        component[0],
                        buffer,
                        stop_offsets,
                        )
        def _iterate_vertical_moments(argument):
            governors = (argument,)
            current_offset, stop_offsets, buffer = abjad.Offset(0), [], []
            _buffer_components_starting_with(argument, buffer, stop_offsets)
            while buffer:
                vertical_moment = abjad.VerticalMoment()
                offset = abjad.Offset(current_offset)
                components = list(buffer)
                components.sort(
                    key=lambda _: abjad.inspect(_).parentage().score_index
                    )
                vertical_moment._offset = offset
                vertical_moment._governors = governors
                vertical_moment._components = components
                yield vertical_moment
                current_offset, stop_offsets = min(stop_offsets), []
                _update_buffer(current_offset, buffer, stop_offsets)
        def _next_in_parent(component):
            assert isinstance(component, abjad.Component), repr(component)
            selection = abjad.select(component)
            result = selection._get_parent_and_start_stop_indices()
            parent, start, stop = result
            assert start == stop
            if parent is None:
                raise StopIteration
            if parent.is_simultaneous:
                raise StopIteration
            try:
                return parent[start + 1]
            except IndexError:
                raise StopIteration
        def _update_buffer(current_offset, buffer, stop_offsets):
            for component in buffer[:]:
                offset = abjad.inspect(component).timespan().stop_offset
                if offset <= current_offset:
                    buffer.remove(component)
                    try:
                        next_component = _next_in_parent(component)
                        _buffer_components_starting_with(
                            next_component,
                            buffer,
                            stop_offsets,
                            )
                    except StopIteration:
                        pass
                else:
                    stop_offsets.append(offset)
        if not reverse:
            for x in _iterate_vertical_moments(self.client):
                yield x
        else:
            moments_in_governor = []
            for component in self.components():
                offset = abjad.inspect(component).timespan().start_offset
                if offset not in moments_in_governor:
                    moments_in_governor.append(offset)
            moments_in_governor.sort()
            for moment_in_governor in reversed(moments_in_governor):
                yield self.client._get_vertical_moment_at(moment_in_governor)
