# -*- encoding: utf-8 -*-
import collections
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.topleveltools import iterate


class IterationAgent(object):
    r'''A wrapper around the Abjad score iterators.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client):
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self):
        '''Interpreter representation of score iteration agent.

        ..  container:: example

            ::

                >>> staff = Staff("c'4 e'4 d'4 f'4")
                >>> iterate(staff[2:])
                IterationAgent(SliceSelection(Note("d'4"), Note("f'4")))

        Returns string.
        '''
        return '{}({})'.format(
            type(self).__name__,
            self._client,
            )

    ### PUBLIC METHODS ###

    def by_class(
        self,
        component_classes=None,
        reverse=False,
        start=0,
        stop=None,
        ):
        r'''Iterate components forward in `expr`.

        ::

            >>> staff = Staff()
            >>> staff.append(Measure((2, 8), "c'8 d'8"))
            >>> staff.append(Measure((2, 8), "e'8 f'8"))
            >>> staff.append(Measure((2, 8), "g'8 a'8"))

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/8
                    c'8
                    d'8
                }
                {
                    e'8
                    f'8
                }
                {
                    g'8
                    a'8
                }
            }

        ::

            >>> for note in iterate(staff).by_class(Note):
            ...     note
            ...
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Note("g'8")
            Note("a'8")

        Use optional `start` and `stop` keyword parameters to control
        start and stop indices of iteration:

        ::

            >>> for note in iterate(staff).by_class(
            ...     Note, start=0, stop=3):
            ...     note
            ...
            Note("c'8")
            Note("d'8")
            Note("e'8")

        ::

            >>> for note in iterate(staff).by_class(
            ...     Note, start=2, stop=4):
            ...     note
            ...
            Note("e'8")
            Note("f'8")

        Yield right-to-left notes in `expr`:

        ::

            >>> staff = Staff()
            >>> staff.append(Measure((2, 8), "c'8 d'8"))
            >>> staff.append(Measure((2, 8), "e'8 f'8"))
            >>> staff.append(Measure((2, 8), "g'8 a'8"))

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/8
                    c'8
                    d'8
                }
                {
                    e'8
                    f'8
                }
                {
                    g'8
                    a'8
                }
            }

        ::

            >>> for note in iterate(staff).by_class(
            ...     Note, reverse=True):
            ...     note
            ...
            Note("a'8")
            Note("g'8")
            Note("f'8")
            Note("e'8")
            Note("d'8")
            Note("c'8")

        Use optional `start` and `stop` keyword parameters to control
        indices of iteration:

        ::

            >>> for note in iterate(staff).by_class(
            ...     Note, reverse=True, start=3):
            ...     note
            ...
            Note("e'8")
            Note("d'8")
            Note("c'8")

        ::

            >>> for note in iterate(staff).by_class(
            ...     Note, reverse=True, start=0, stop=3):
            ...     note
            ...
            Note("a'8")
            Note("g'8")
            Note("f'8")

        ::

            >>> for note in iterate(staff).by_class(
            ...     Note, reverse=True, start=2, stop=4):
            ...     note
            ...
            Note("f'8")
            Note("e'8")

        Iterates across different logical voices.

        Returns generator.
        '''
        component_classes = component_classes or scoretools.Component
        def component_iterator(expr, component_class, reverse=False):
            if isinstance(expr, component_class):
                yield expr
            if isinstance(expr, (list, tuple, spannertools.Spanner)) or \
                hasattr(expr, '_music'):
                if hasattr(expr, '_music'):
                    expr = expr._music
                if reverse:
                    expr = reversed(expr)
                for m in expr:
                    for x in component_iterator(
                        m, component_class, reverse=reverse):
                        yield x

        def subrange(iter, start=0, stop=None):
            # if start<0, then 'stop-start' gives a funny result
            # don not have to check stop>=start
            # because xrange(stop-start) already handles that
            assert 0 <= start

            try:
                # skip the first few elements, up to 'start' of them:
                for i in xrange(start):
                    # no yield to swallow the results
                    iter.next()

                # now generate (stop-start) elements
                # (or all elements if stop is none)
                if stop is None:
                    for x in iter:
                        yield x
                else:
                    for i in xrange(stop - start):
                        yield iter.next()
            except StopIteration:
                # this happens if we exhaust the list before
                # we generate a total of 'stop' elements
                pass

        return subrange(
            component_iterator(
                self._client,
                component_classes,
                reverse=reverse),
            start,
            stop,
            )

    def by_components_and_grace_containers(self, component_classes=None):
        r'''Iterate components of `component_class` forward in `expr`:

        ::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> beam = spannertools.Beam()
            >>> attach(beam, voice[:])

        ::

            >>> grace_notes = [Note("c'16"), Note("d'16")]
            >>> grace = scoretools.GraceContainer(
            ...     grace_notes,
            ...     kind='grace',
            ...     )
            >>> attach(grace, voice[1])
            Note("d'8")

        ::

            >>> after_grace_notes = [Note("e'16"), Note("f'16")]
            >>> after_grace = scoretools.GraceContainer(
            ...     after_grace_notes,
            ...     kind='after')
            >>> attach(after_grace, voice[1])
            Note("d'8")

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'8 [
                \grace {
                    c'16
                    d'16
                }
                \afterGrace
                d'8
                {
                    e'16
                    f'16
                }
                e'8
                f'8 ]
            }

        ::

            >>> x = iterate(voice).by_components_and_grace_containers(Note)
            >>> for note in x:
            ...     note
            ...
            Note("c'8")
            Note("c'16")
            Note("d'16")
            Note("d'8")
            Note("e'16")
            Note("f'16")
            Note("e'8")
            Note("f'8")

        Include grace leaves before main leaves.

        Include grace leaves after main leaves.
        '''
        component_classes = component_classes or scoretools.Leaf
        if hasattr(self._client, '_grace'):
            for m in self._client.grace:
                for x in iterate(m).by_components_and_grace_containers(
                    component_classes,
                    ):
                    yield x
            if isinstance(self._client, component_classes):
                yield self._client
        if hasattr(self._client, '_after_grace'):
            for m in self._client.after_grace:
                for x in iterate(m).by_components_and_grace_containers(
                    component_classes,
                    ):
                    yield x
        elif isinstance(self._client, component_classes):
            yield self._client
        if isinstance(self._client, (list, tuple)):
            for m in self._client:
                for x in iterate(m).by_components_and_grace_containers(
                    component_classes,
                    ):
                    yield x
        if hasattr(self._client, '_music'):
            for m in self._client._music:
                for x in iterate(m).by_components_and_grace_containers(
                    component_classes,
                    ):
                    yield x

    def by_leaf_pairs(self):
        r'''Iterate leaf pairs forward in `expr`:

        ::

            >>> score = Score([])
            >>> notes = [Note("c'8"), Note("d'8"), Note("e'8"),
            ...     Note("f'8"), Note("g'4")]
            >>> score.append(Staff(notes))
            >>> notes = [Note(x, (1, 4)) for x in [-12, -15, -17]]
            >>> score.append(Staff(notes))
            >>> clef = Clef('bass')
            >>> attach(clef, score[1])
            Clef('bass')(Staff{3})
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> f(score)
            \new Score <<
                \new Staff {
                    c'8
                    d'8
                    e'8
                    f'8
                    g'4
                }
                \new Staff {
                    \clef "bass"
                    c4
                    a,4
                    g,4
                }
            >>

        ::

            >>> for pair in iterate(score).by_leaf_pairs():
            ...        pair
            (Note("c'8"), Note('c4'))
            (Note("c'8"), Note("d'8"))
            (Note('c4'), Note("d'8"))
            (Note("d'8"), Note("e'8"))
            (Note("d'8"), Note('a,4'))
            (Note('c4'), Note("e'8"))
            (Note('c4'), Note('a,4'))
            (Note("e'8"), Note('a,4'))
            (Note("e'8"), Note("f'8"))
            (Note('a,4'), Note("f'8"))
            (Note("f'8"), Note("g'4"))
            (Note("f'8"), Note('g,4'))
            (Note('a,4'), Note("g'4"))
            (Note('a,4'), Note('g,4'))
            (Note("g'4"), Note('g,4'))

        Iterate leaf pairs left-to-right and top-to-bottom.

        Returns generator.
        '''
        from abjad.tools import iterationtools
        vertical_moments = self.by_vertical_moment()
        for moment_1, moment_2 in \
            sequencetools.iterate_sequence_pairwise_strict(vertical_moments):
            for pair in sequencetools.yield_all_unordered_pairs_of_sequence(
                moment_1.start_leaves):
                yield pair
            pairs = sequencetools.yield_all_pairs_between_sequences(
                moment_1.leaves, moment_2.start_leaves)
            for pair in pairs:
                yield pair
        else:
            for pair in sequencetools.yield_all_unordered_pairs_of_sequence(
                moment_2.start_leaves):
                yield pair

    def by_runs(self, classes):
        r'''Iterate runs in expression.

        ..  container:: example

            **Example 1.** Iterate runs of notes and chords at only the
            top level of score:

            ::

                >>> staff = Staff(r"\times 2/3 { c'8 d'8 r8 }")
                >>> staff.append(r"\times 2/3 { r8 <e' g'>8 <f' a'>8 }")
                >>> staff.extend("g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \times 2/3 {
                        c'8
                        d'8
                        r8
                    }
                    \times 2/3 {
                        r8
                        <e' g'>8
                        <f' a'>8
                    }
                    g'8
                    a'8
                    r8
                    r8
                    <b' d''>8
                    <c'' e''>8
                }

            ::

                >>> for group in iterate(staff[:]).by_runs((Note, Chord)):
                ...     group
                ...
                (Note("g'8"), Note("a'8"))
                (Chord("<b' d''>8"), Chord("<c'' e''>8"))

        ..  container:: example

            **Example 2.** Iterate runs of notes and chords at all levels of
            score:

            ::

                >>> leaves = iterate(staff).by_class(scoretools.Leaf)

            ::

                >>> for group in iterate(leaves).by_runs((Note, Chord)):
                ...     group
                ...
                (Note("c'8"), Note("d'8"))
                (Chord("<e' g'>8"), Chord("<f' a'>8"), Note("g'8"), Note("a'8"))
                (Chord("<b' d''>8"), Chord("<c'' e''>8"))

        Returns generator.
        '''
        from abjad.tools import selectiontools
        sequence = selectiontools.SliceSelection(self._client)
        current_group = ()
        for group in sequence.group_by(type):
            if type(group[0]) in classes:
                current_group = current_group + group
            elif current_group:
                yield current_group
                current_group = ()
        if current_group:
            yield current_group

    def by_semantic_voices(
        self,
        reverse=False,
        start=0,
        stop=None,
        ):
        r'''Iterate semantic voices forward in `expr`:

        ::

            >>> measures = scoretools.make_measures_with_full_measure_spacer_skips(
            ...     [(3, 8), (5, 16), (5, 16)])
            >>> time_signature_voice = Voice(measures)
            >>> time_signature_voice.name = 'TimeSignatuerVoice'
            >>> time_signature_voice.is_nonsemantic = True
            >>> music_voice = Voice("c'4. d'4 e'16 f'4 g'16")
            >>> music_voice.name = 'MusicVoice'
            >>> staff = Staff([time_signature_voice, music_voice])
            >>> staff.is_simultaneous = True

        ..  doctest::

            >>> f(staff)
            \new Staff <<
                \context Voice = "TimeSignatuerVoice" {
                    {
                        \time 3/8
                        s1 * 3/8
                    }
                    {
                        \time 5/16
                        s1 * 5/16
                    }
                    {
                        s1 * 5/16
                    }
                }
                \context Voice = "MusicVoice" {
                    c'4.
                    d'4
                    e'16
                    f'4
                    g'16
                }
            >>

            >>> for voice in iterate(staff).by_semantic_voices():
            ...   voice
            ...
            Voice-"MusicVoice"{5}

        Iterate semantic voices backward in `expr`:

        ::

            >>> for voice in iterate(staff).by_semantic_voices(reverse=True):
            ...   voice
            ...
            Voice-"MusicVoice"{5}

        Returns generator.
        '''
        for voice in self.by_class(
            scoretools.Voice,
            reverse=reverse,
            start=start,
            stop=stop,
            ):
            if not voice.is_nonsemantic:
                yield voice

    def by_tie_chain(
        self,
        nontrivial=False,
        pitched=False,
        reverse=False,
        ):
        r'''Iterate tie chains forward in `expr`:

        ::

            >>> staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4 ~
                \times 2/3 {
                    c'16
                    d'8
                }
                e'8
                f'4 ~
                f'16
            }

        ::

            >>> for x in iterate(staff).by_tie_chain():
            ...     x
            ...
            TieChain(Note("c'4"), Note("c'16"))
            TieChain(Note("d'8"),)
            TieChain(Note("e'8"),)
            TieChain(Note("f'4"), Note("f'16"))

        Iterate tie chains backward in `expr`:

        ::

            >>> for x in iterate(staff).by_tie_chain(reverse=True):
            ...     x
            ...
            TieChain(Note("f'4"), Note("f'16"))
            TieChain(Note("e'8"),)
            TieChain(Note("d'8"),)
            TieChain(Note("c'4"), Note("c'16"))

        Iterate pitched tie chains in `expr`:

        ::

            >>> for x in iterate(staff).by_tie_chain(pitched=True):
            ...     x
            ...
            TieChain(Note("c'4"), Note("c'16"))
            TieChain(Note("d'8"),)
            TieChain(Note("e'8"),)
            TieChain(Note("f'4"), Note("f'16"))

        Iterate nontrivial tie chains in `expr`:

        ::

            >>> for x in iterate(staff).by_tie_chain(nontrivial=True):
            ...     x
            ...
            TieChain(Note("c'4"), Note("c'16"))
            TieChain(Note("f'4"), Note("f'16"))

        Returns generator.
        '''
        spanner_classes = (spannertools.Tie,)
        nontrivial = bool(nontrivial)
        component_classes = scoretools.Leaf
        if pitched:
            component_classes = (scoretools.Chord, scoretools.Note)
        if not reverse:
            for leaf in self.by_class(component_classes):
                tie_spanners = leaf._get_spanners(spanner_classes)
                if not tie_spanners or \
                    tuple(tie_spanners)[0]._is_my_last_leaf(leaf):
                    tie_chain = leaf._get_tie_chain()
                    if not nontrivial or not tie_chain.is_trivial:
                        yield tie_chain
        else:
            for leaf in self.by_class(component_classes, reverse=True):
                tie_spanners = leaf._get_spanners(spanner_classes)
                if not(tie_spanners) or \
                    tuple(tie_spanners)[0]._is_my_first_leaf(leaf):
                    tie_chain = leaf._get_tie_chain()
                    if not nontrivial or not tie_chain.is_trivial:
                        yield tie_chain

    def by_topmost_tie_chains_and_components(self):
        r'''Iterate topmost tie chains and components forward in `expr`:

        ::

            >>> string = r"c'8 ~ c'32 d'8 ~ d'32 \times 2/3 { e'8 f'8 g'8 } "
            >>> string += "a'8 ~ a'32 b'8 ~ b'32"
            >>> staff = Staff(string)

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'8 ~
                c'32
                d'8 ~
                d'32
                \times 2/3 {
                    e'8
                    f'8
                    g'8
                }
                a'8 ~
                a'32
                b'8 ~
                b'32
            }

        ::

            >>> for x in iterate(staff).by_topmost_tie_chains_and_components():
            ...     x
            ...
            TieChain(Note("c'8"), Note("c'32"))
            TieChain(Note("d'8"), Note("d'32"))
            Tuplet(2/3, [e'8, f'8, g'8])
            TieChain(Note("a'8"), Note("a'32"))
            TieChain(Note("b'8"), Note("b'32"))

        Raise tie chain error on overlapping tie chains.

        Returns generator.
        '''
        from abjad.tools import selectiontools
        spanner_classes = (spannertools.Tie,)
        if isinstance(self._client, scoretools.Leaf):
            tie_chain = self._client._get_tie_chain()
            if len(tie_chain) == 1:
                yield tie_chain
            else:
                message = 'can not have only one leaf in tie chain.'
                raise TieChainError(message)
        elif isinstance(
            self._client, (
                collections.Sequence,
                scoretools.Container,
                selectiontools.SliceSelection,
                )):
            for component in self._client:
                if isinstance(component, scoretools.Leaf):
                    tie_spanners = component._get_spanners(spanner_classes)
                    if not tie_spanners or \
                        tuple(tie_spanners)[0]._is_my_last_leaf(component):
                        yield component._get_tie_chain()
                elif isinstance(component, scoretools.Container):
                    yield component
        else:
            message = 'input must be iterable: {!r}.'.format(self._client)
            raise ValueError(message)

    def by_vertical_moment(
        self,
        reverse=False,
        ):
        r'''Iterate vertical moments forward in `expr`:

        ::

            >>> score = Score([])
            >>> staff = Staff(r"\times 4/3 { d''8 c''8 b'8 }")
            >>> score.append(staff)

        ::

            >>> piano_staff = scoretools.PianoStaff([])
            >>> piano_staff.append(Staff("a'4 g'4"))
            >>> piano_staff.append(Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
            >>> score.append(piano_staff)

        ..  doctest::

            >>> f(score)
            \new Score <<
                \new Staff {
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 4/3 {
                        d''8
                        c''8
                        b'8
                    }
                }
                \new PianoStaff <<
                    \new Staff {
                        a'4
                        g'4
                    }
                    \new Staff {
                        \clef "bass"
                        f'8
                        e'8
                        d'8
                        c'8
                    }
                >>
            >>

        ::

            >>> for x in iterate(score).by_vertical_moment():
            ...     x.leaves
            ...
            (Note("d''8"), Note("a'4"), Note("f'8"))
            (Note("d''8"), Note("a'4"), Note("e'8"))
            (Note("c''8"), Note("a'4"), Note("e'8"))
            (Note("c''8"), Note("g'4"), Note("d'8"))
            (Note("b'8"), Note("g'4"), Note("d'8"))
            (Note("b'8"), Note("g'4"), Note("c'8"))

        ::

            >>> for x in iterate(piano_staff).by_vertical_moment():
            ...     x.leaves
            ...
            (Note("a'4"), Note("f'8"))
            (Note("a'4"), Note("e'8"))
            (Note("g'4"), Note("d'8"))
            (Note("g'4"), Note("c'8"))

        Iterate vertical moments backward in `expr`:

        ::

        ::

            >>> for x in iterate(score).by_vertical_moment(reverse=True):
            ...     x.leaves
            ...
            (Note("b'8"), Note("g'4"), Note("c'8"))
            (Note("b'8"), Note("g'4"), Note("d'8"))
            (Note("c''8"), Note("g'4"), Note("d'8"))
            (Note("c''8"), Note("a'4"), Note("e'8"))
            (Note("d''8"), Note("a'4"), Note("e'8"))
            (Note("d''8"), Note("a'4"), Note("f'8"))

        ::

            >>> for x in iterate(piano_staff).by_vertical_moment(
            ...     reverse=True):
            ...     x.leaves
            ...
            (Note("g'4"), Note("c'8"))
            (Note("g'4"), Note("d'8"))
            (Note("a'4"), Note("e'8"))
            (Note("a'4"), Note("f'8"))

        Returns generator.
        '''
        from abjad.tools import selectiontools

        def _buffer_components_starting_with(component, buffer, stop_offsets):
            #if not isinstance(component, scoretools.Component):
            #    raise TypeError
            buffer.append(component)
            stop_offsets.append(component._get_timespan().stop_offset)
            if isinstance(component, scoretools.Container):
                if component.is_simultaneous:
                    for x in component:
                        _buffer_components_starting_with(
                            x, buffer, stop_offsets)
                else:
                    if component:
                        _buffer_components_starting_with(
                            component[0], buffer, stop_offsets)

        def _iterate_vertical_moments_forward_in_expr(expr):
            #if not isinstance(expr, scoretools.Component):
            #    raise TypeError
            governors = (expr,)
            current_offset, stop_offsets, buffer = \
                durationtools.Offset(0), [], []
            _buffer_components_starting_with(expr, buffer, stop_offsets)
            while buffer:
                vertical_moment = selectiontools.VerticalMoment()
                offset = durationtools.Offset(current_offset)
                components = list(buffer)
                components.sort(key=lambda x: x._get_parentage().score_index)
                vertical_moment._offset = offset
                vertical_moment._governors = governors
                vertical_moment._components = components
                yield vertical_moment
                current_offset, stop_offsets = min(stop_offsets), []
                _update_buffer(current_offset, buffer, stop_offsets)

        def _next_in_parent(component):
            from abjad.tools import selectiontools
            if not isinstance(component, scoretools.Component):
                raise TypeError
            selection = selectiontools.SliceSelection(component)
            parent, start, stop = \
                selection._get_parent_and_start_stop_indices()
            assert start == stop
            if parent is None:
                raise StopIteration
            # can not advance within simultaneous parent
            if parent.is_simultaneous:
                raise StopIteration
            try:
                return parent[start + 1]
            except IndexError:
                raise StopIteration

        def _update_buffer(current_offset, buffer, stop_offsets):
            #print 'At %s with %s ...' % (current_offset, buffer)
            for component in buffer[:]:
                if component._get_timespan().stop_offset <= current_offset:
                    buffer.remove(component)
                    try:
                        next_component = _next_in_parent(component)
                        _buffer_components_starting_with(
                            next_component, buffer, stop_offsets)
                    except StopIteration:
                        pass
                else:
                    stop_offsets.append(component._get_timespan().stop_offset)

        if not reverse:
            for x in _iterate_vertical_moments_forward_in_expr(self._client):
                yield x
        else:
            moments_in_governor = []
            for component in self.by_class():
                offset = component._get_timespan().start_offset
                if offset not in moments_in_governor:
                    moments_in_governor.append(offset)
            moments_in_governor.sort()
            for moment_in_governor in reversed(moments_in_governor):
                yield self._client._get_vertical_moment_at(moment_in_governor)

    def depth_first(
        self,
        capped=True,
        direction=Left,
        forbid=None,
        unique=True,
        ):
        '''Iterate components depth-first from `component`.

        .. todo:: Add usage examples.
        '''

        def _next_node_depth_first(component, total):
            r'''If client has unvisited music, return next unvisited node in
            client's music.

            If client has no univisited music and has a parent, return client's
            parent.

            If client has no univisited music and no parent, return None.
            '''

            client = component
            if hasattr(client, '_music') and \
                0 < len(client) and \
                total < len(client):
                return client[total], 0
            else:
                parent = client._parent
                if parent is not None:
                    return parent, parent.index(client) + 1
                else:
                    return None, None

        def _previous_node_depth_first(component, total=0):
            r'''If client has unvisited music, return prev unvisited node in
            client's music.

            If client has no univisited music and has a parent, return client's
            parent.

            If client has no univisited music and no parent, return None.
            '''

            client = component
            if hasattr(client, '_music') and \
                0 < len(client) and \
                total < len(client):
                return client[len(client) - 1 - total], 0
            else:
                parent = client._parent
                if parent is not None:
                    return parent, len(parent) - parent.index(client)
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
            # TODO: remove 'left'
            if direction in ('left', Left):
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
            if hasattr(node, '_music'):
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

        assert isinstance(self._client, scoretools.Component)
        component = self._client
        client_parent, node, rank = component._parent, component, 0
        queue = collections.deque([])
        while node is not None and not (capped and node is client_parent):
            result = _find_yield(node, rank, queue, unique)
            if result is not None:
                yield result
            if _is_node_forbidden(node, forbid):
                node, rank = _handle_forbidden_node(node, queue)
            else:
                node, rank = _advance_node_depth_first(node, rank, direction)
        queue.clear()
