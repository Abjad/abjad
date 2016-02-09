# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.handlertools.Handler import Handler


class HairpinHandler(Handler):
    r'''Hairpin handler.

    ..  container:: example

        **Example 1.** Attaches hairpins to nontrivial ties:

        ::

            >>> handler = handlertools.HairpinHandler(
            ...     hairpin_tokens=['f > niente', 'niente < f'],
            ...     span='nontrivial ties',
            ...     )
            >>> string = "c'4 ~ c' ~ c' r4 d'4 ~ d' ~ d' r4"
            >>> staff = Staff(string)
            >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
            >>> logical_ties = list(logical_ties)
            >>> handler(logical_ties)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                \once \override Hairpin #'circled-tip = ##t
                c'4 ~ \> \f
                c'4 ~
                c'4 \!
                r4
                \once \override Hairpin #'circled-tip = ##t
                d'4 ~ \<
                d'4 ~
                d'4 \f
                r4
            }

    ..  container:: example

        **Example 2.** Gets storage format of handler:

        ::

            >>> print(format(handler))
            handlertools.HairpinHandler(
                attach_start_dynamic_to_lone_notes=True,
                hairpin_tokens=datastructuretools.CyclicTuple(
                    [
                        ('f', '>', 'niente'),
                        ('niente', '<', 'f'),
                        ]
                    ),
                span='nontrivial ties',
                )

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_attach_start_dynamic_to_lone_notes',
        '_enchain_hairpins',
        '_hairpin_tokens',
        '_include_following_rests',
        '_minimum_duration',
        '_patterns',
        '_span',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        attach_start_dynamic_to_lone_notes=True,
        enchain_hairpins=None,
        hairpin_tokens=None,
        include_following_rests=None,
        minimum_duration=None,
        patterns=None,
        span='contiguous notes and chords',
        ):
        self._attach_start_dynamic_to_lone_notes = bool(
            attach_start_dynamic_to_lone_notes)
        if enchain_hairpins is not None:
            enchain_hairpins = bool(enchain_hairpins)
        self._enchain_hairpins = enchain_hairpins
        hairpin_tokens = hairpin_tokens or []
        assert isinstance(hairpin_tokens, list), repr(hairpin_tokens)
        tokens = []
        for element in hairpin_tokens:
            if isinstance(element, str):
                element = tuple(element.split())
                if not spannertools.Hairpin._is_hairpin_token(element):
                    message = 'must be valid hairpin token: {!r}.'
                    message = message.format(element)
                    raise Exception(message)
            tokens.append(element)
        hairpin_tokens = tokens
        hairpin_tokens = datastructuretools.CyclicTuple(hairpin_tokens)
        self._hairpin_tokens = hairpin_tokens
        if include_following_rests is not None:
            include_following_rests = bool(include_following_rests)
        self._include_following_rests = include_following_rests
        if minimum_duration is not None:
            minimum_duration = durationtools.Duration(minimum_duration)
        self._minimum_duration = minimum_duration
        if patterns is not None:
            assert isinstance(patterns, (list, tuple)), repr(patterns)
        self._patterns = patterns
        strings = (
            'contiguous notes and chords',
            'nontrivial ties',
            )
        if span not in strings:
            assert isinstance(span, (tuple, list)), repr(span)
        self._span = span

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        r'''Calls hairpin handler on `logical_ties`.

        Returns none.
        '''
        if (self.span == 'contiguous notes and chords'
            or isinstance(self.span, (tuple, list))):
            groups = self._group_contiguous_logical_ties(logical_ties)
        elif self.span == 'nontrivial ties':
            groups = [[_] for _ in logical_ties]
        else:
            raise ValueError(self.span)
        if isinstance(self.span, (tuple, list)):
            if not self.enchain_hairpins:
                groups = self._partition_groups(groups)
            else:
                groups = self._partition_enchained_groups(groups)
        for group_index, group in enumerate(groups):
            notes = []
            for logical_tie in group:
                for note in logical_tie:
                    notes.append(note)
            if len(notes) == 0:
                continue
            total_notes = len(notes)
            notes_to_span = []
            for note_index, note in enumerate(notes):
                if self._index_matches_patterns(note_index, total_notes):
                    notes_to_span.append(note)
            if not notes_to_span:
                continue
            if self.include_following_rests:
                last_note = notes_to_span[-1]
                next_leaf = inspect_(last_note).get_leaf(1)
                if isinstance(next_leaf, scoretools.Rest):
                    notes_to_span.append(next_leaf)
            if (len(notes_to_span) == 1 and
                not self.attach_start_dynamic_to_lone_notes):
                continue
            if (len(notes_to_span) == 1 and
                self.attach_start_dynamic_to_lone_notes):
                hairpin_token = self.hairpin_tokens[group_index]
                start_dynamic = hairpin_token[0]
                dynamic = indicatortools.Dynamic(start_dynamic)
                attach(dynamic, notes[0])
                continue
            hairpin_token = self.hairpin_tokens[group_index]
            descriptor = ' '.join([_ for _ in hairpin_token if _])
            include_rests = bool(self.include_following_rests)
            hairpin = spannertools.Hairpin(
                descriptor=descriptor,
                include_rests=include_rests,
                )
            attach(hairpin, notes_to_span)

    ### PRIVATE METHODS ###

    def _group_contiguous_logical_ties(self, logical_ties):
        result = []
        current_group = [logical_ties[0]]
        for logical_tie in logical_ties[1:]:
            last_timespan = current_group[-1].get_timespan()
            current_timespan = logical_tie.get_timespan()
            if last_timespan.stops_when_timespan_starts(current_timespan):
                current_group.append(logical_tie)
            else:
                result.append(current_group)
                current_group = [logical_tie]
        if current_group:
            result.append(current_group)
        return result

    def _index_matches_patterns(self, index, total):
        if not self.patterns:
            return True
        for pattern in self.patterns:
            if pattern.matches_index(index, total):
                return True
        return False

    def _partition_by_enchained_counts(self, leaves, counts):
        assert isinstance(leaves, list), repr(leaves)
        counts = datastructuretools.CyclicTuple(counts)
        shards = []
        shard_index = 0
        leaf_start_index = 0
        total_leaves = len(leaves)
        while True:
            current_count = counts[shard_index]
            leaf_stop_index = leaf_start_index + current_count
            shard = leaves[leaf_start_index:leaf_stop_index]
            shards.append(shard)
            shard_index += 1
            leaf_start_index = leaf_stop_index - 1
            if total_leaves <= leaf_start_index:
                break
        return shards

    def _partition_enchained_groups(self, groups):
        new_groups = []
        for group in groups:
            leaves = iterate(group).by_class(scoretools.Leaf)
            leaves = list(leaves)
            shards = self._partition_by_enchained_counts(
                leaves,
                counts=self.span,
                )
            new_groups.extend(shards)
        groups = new_groups
        groups = [[_] for _ in groups]
        return groups

    def _partition_groups(self, groups):
        new_groups = []
        for group in groups:
            leaves = iterate(group).by_class(scoretools.Leaf)
            leaves = list(leaves)
            shards = sequencetools.partition_sequence_by_counts(
                leaves,
                counts=self.span,
                cyclic=True,
                )
            new_groups.extend(shards)
        groups = new_groups
        groups = [[_] for _ in groups]
        return groups

    ### PUBLIC PROPERTIES ###

    @property
    def attach_start_dynamic_to_lone_notes(self):
        r'''Is true when start dynamic of hairpin should be attached to lone
        notes. Otherwise false.

        ..  container:: example

            **Example 1.** Attaches start dynamic to lone notes:

            ::

                >>> handler = handlertools.HairpinHandler(
                ...     attach_start_dynamic_to_lone_notes=True,
                ...     hairpin_tokens=['ppp < p'],
                ...     span='nontrivial ties',
                ...     )
                >>> staff = Staff("c'4 ~ c'8 d'8 ~ d'4 r4 e'4 g'4 fs'4 ~ fs'4")
                >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> handler(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'4 ~ \< \ppp
                    c'8 \p
                    d'8 ~ \< \ppp
                    d'4 \p
                    r4
                    e'4 \ppp
                    g'4 \ppp
                    fs'4 ~ \< \ppp
                    fs'4 \p
                }

        ..  container:: example

            **Example 2.** Does not attach start dynamic to lone notes:

            ::

                >>> handler = handlertools.HairpinHandler(
                ...     attach_start_dynamic_to_lone_notes=False,
                ...     hairpin_tokens=['ppp < p'],
                ...     span='nontrivial ties',
                ...     )
                >>> staff = Staff("c'4 ~ c'8 d'8 ~ d'4 r4 e'4 g'4 fs'4 ~ fs'4")
                >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> handler(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'4 ~ \< \ppp
                    c'8 \p
                    d'8 ~ \< \ppp
                    d'4 \p
                    r4
                    e'4
                    g'4
                    fs'4 ~ \< \ppp
                    fs'4 \p
                }


        Defaults to true.

        Set to true or false.

        Returns true or false
        '''
        return self._attach_start_dynamic_to_lone_notes

    @property
    def enchain_hairpins(self):
        r'''Is true when hairpins should enchain. Otherwise false.

        ..  container:: example

            **Example 1.** Spans groups of notes and chords:

            ::

                >>> handler = handlertools.HairpinHandler(
                ...     hairpin_tokens=['p < f', 'f > p'],
                ...     span=[3, 2],
                ...     )
                >>> string = "c'8 ~ c' ~ c' ~ c' ~ c' ~ c' ~ c' ~ c'"
                >>> staff = Staff(string)
                >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> handler(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8 ~ \< \p
                    c'8 ~
                    c'8 ~ \f
                    c'8 ~ \> \f
                    c'8 ~ \p
                    c'8 ~ \< \p
                    c'8 ~
                    c'8 \f
                }

        ..  container:: example

            **Example 2.** Spans enchained groups of notes and chords:

            ::

                >>> handler = handlertools.HairpinHandler(
                ...     enchain_hairpins=True,
                ...     hairpin_tokens=['p < f', 'f > p'],
                ...     span=[3, 2],
                ...     )
                >>> string = "c'8 ~ c' ~ c' ~ c' ~ c' ~ c' ~ c' ~ c'"
                >>> staff = Staff(string)
                >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> handler(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8 ~ \< \p
                    c'8 ~
                    c'8 ~ \f \> \f
                    c'8 ~ \p \< \p
                    c'8 ~
                    c'8 ~ \f \> \f
                    c'8 ~ \p \< \p
                    c'8 \f
                }

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._enchain_hairpins

    @property
    def hairpin_tokens(self):
        r'''Gets hairpin tokens of handler.

        Tuple like ``('f', '>', 'p')`` or string like ``'f > p'``.

        Set to triple, string, list of triples, list of strings or none.

        Returns cyclic tuple.
        '''
        return self._hairpin_tokens

    @property
    def include_following_rests(self):
        r'''Is true if every hairpin should extend to include rests
        following the last note or chord in each hairpin. Otherwise false.

        ..  container:: example

            **Example 1.** Does not include following rests:

            ::

                >>> handler = handlertools.HairpinHandler(
                ...     enchain_hairpins=True,
                ...     hairpin_tokens=['p < f', 'f > niente'],
                ...     span=[2, 3],
                ...     )
                >>> string = "c'4 ~ c' ~ c' r"
                >>> staff = Staff(string)
                >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> handler(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'4 ~ \< \p
                    \once \override Hairpin #'circled-tip = ##t
                    c'4 ~ \f \> \f
                    c'4 \!
                    r4
                }

        ..  container:: example

            **Example 2.** Includes following rests:

            ::

                >>> handler = handlertools.HairpinHandler(
                ...     enchain_hairpins=True,
                ...     hairpin_tokens=['p < f', 'f > niente'],
                ...     include_following_rests=True,
                ...     span=[2, 3],
                ...     )
                >>> string = "c'4 ~ c' ~ c' r"
                >>> staff = Staff(string)
                >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> handler(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'4 ~ \< \p
                    \once \override Hairpin #'circled-tip = ##t
                    c'4 ~ \f \> \f
                    c'4
                    r4 \!
                }

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._include_following_rests

    @property
    def minimum_duration(self):
        r'''Gets minimum duration of handler.

        Returns duration or none.
        '''
        return self._minimum_duration

    @property
    def patterns(self):
        r'''Gets patterns of handler.

        Set to patterns or none.
        '''
        return self._patterns

    @property
    def span(self):
        r'''Gets span of handler.
        
        ..  container:: example

            **Example 1.** Spans contiguous notes and chords:

            ::

                >>> handler = handlertools.HairpinHandler(
                ...     hairpin_tokens=['ppp < p'],
                ...     span='contiguous notes and chords',
                ...     )
                >>> staff = Staff("c'4 ~ c'8 d'8 ~ d'4 r4 e'4 g'4 fs'4 ~ fs'4")
                >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> handler(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'4 ~ \< \ppp
                    c'8
                    d'8 ~
                    d'4 \p
                    r4
                    e'4 \< \ppp
                    g'4
                    fs'4 ~
                    fs'4 \p
                }

        ..  container:: example

            **Example 2.** Spans nontrivial ties:

            ::

                >>> handler = handlertools.HairpinHandler(
                ...     attach_start_dynamic_to_lone_notes=False,
                ...     hairpin_tokens=['ppp < p'],
                ...     span='nontrivial ties',
                ...     )
                >>> staff = Staff("c'4 ~ c'8 d'8 ~ d'4 r4 e'4 g'4 fs'4 ~ fs'4")
                >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> handler(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'4 ~ \< \ppp
                    c'8 \p
                    d'8 ~ \< \ppp
                    d'4 \p
                    r4
                    e'4
                    g'4
                    fs'4 ~ \< \ppp
                    fs'4 \p
                }

        ..  container:: example

            **Example 3.** Spans notes and chords grouped in repeating patterns
            of 3 and 4:

            ::

                >>> handler = handlertools.HairpinHandler(
                ...     hairpin_tokens=['p < f'],
                ...     span=[3, 4],
                ...     )
                >>> string = "c'16 d' ~ d' e' c' d' ~ d' e' c' d' ~ d' e' c'8 e'8"
                >>> staff = Staff(string)
                >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> handler(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'16 \< \p
                    d'16 ~
                    d'16 \f
                    e'16 \< \p
                    c'16
                    d'16 ~
                    d'16 \f
                    e'16 \< \p
                    c'16
                    d'16 ~ \f
                    d'16 \< \p
                    e'16
                    c'8
                    e'8 \f
                }

        Defaults to ``'contiguous notes and chords'``.

        Set to ``'contiguous notes and chords'``, ``'nontrivial ties'`` or
        an iterable of positive integers.

        Returns ``'contiguous notes and chords'``, ``'nontrivial ties'`` or
        an iterable of positive integers.
        '''
        return self._span