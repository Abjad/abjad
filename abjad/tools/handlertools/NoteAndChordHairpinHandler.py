# -*- encoding: utf-8 -*-
import collections
from abjad.tools import datastructuretools
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from abjad.tools.handlertools.DynamicHandler import DynamicHandler


class NoteAndChordHairpinHandler(DynamicHandler):
    r'''Note and chord hairpin handler.

    ..  container:: example
        
        **Example 1.** Spans contiguous notes and chords:

        ::

            >>> handler = handlertools.NoteAndChordHairpinHandler(
            ...     hairpin_token='ppp < p',
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

            >>> handler = handlertools.NoteAndChordHairpinHandler(
            ...     hairpin_token='ppp < p',
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
        
        **Example 3.** Spans individual notes and chords grouped in repeating
        patterns of 3 and 4:

        ::

            >>> handler = handlertools.NoteAndChordHairpinHandler(
            ...     hairpin_token='p < f',
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

    ..  container:: example
        
        **Example 4.** Spans individual notes and chords grouped in repeating
        patterns of 3 and 4 with alternating crescendi and decrescendi:

        ::

            >>> handler = handlertools.NoteAndChordHairpinHandler(
            ...     hairpin_token=['p < f', 'f > p'],
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
                e'16 \> \f
                c'16
                d'16 ~
                d'16 \p
                e'16 \< \p
                c'16
                d'16 ~ \f
                d'16 \> \f
                e'16
                c'8
                e'8 \p
            }
            
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_hairpin_token',
        '_patterns',
        '_span',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        hairpin_token=None, 
        minimum_duration=None,
        patterns=None,
        span='contiguous notes and chords',
        ):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        if hairpin_token is None:
            hairpin_token = []
        elif isinstance(hairpin_token, str):
            hairpin_token = tuple(hairpin_token.split())
            assert spannertools.Hairpin._is_hairpin_token(hairpin_token)
        elif isinstance(hairpin_token, list):
            tokens = []
            for element in hairpin_token:
                if isinstance(element, str):
                    element = tuple(element.split())
                    if not spannertools.Hairpin._is_hairpin_token(element):
                        message = 'must be valid hairpin token: {!r}.'
                        message = message.format(element)
                        raise Exception(message)
                tokens.append(element)
            hairpin_token = tokens
        if isinstance(hairpin_token, list):
            hairpin_token = datastructuretools.CyclicTuple(hairpin_token)
        elif isinstance(hairpin_token, tuple):
            hairpin_token = datastructuretools.CyclicTuple([hairpin_token])
        else:
            raise TypeError(hairpin_token)
        self._hairpin_token = hairpin_token
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

    def __call__(self, logical_ties, timespan=None, offset=0):
        r'''Calls note and chord hairpin handler on `logical_ties` 
        with `offset`.

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
        for group_index, group in enumerate(groups):
            notes = []
            for logical_tie in group:
                for note in logical_tie:
                    notes.append(note)
            if len(notes) <= 1:
                continue
            total_notes = len(notes)
            notes_to_span = []
            for note_index, note in enumerate(notes):
                if self._index_matches_patterns(note_index, total_notes):
                    notes_to_span.append(note)
            if not notes_to_span:
                continue
            hairpin_token = self.hairpin_token[group_index]
            descriptor = ' '.join([_ for _ in hairpin_token if _])
            hairpin = spannertools.Hairpin(
                descriptor=descriptor,
                include_rests=False,
                )
            attach(hairpin, notes_to_span)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from ide import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='hairpin_token',
                command='ht',
                editor=idetools.getters.get_hairpin_token,
                ),
            systemtools.AttributeDetail(
                name='minimum_duration',
                command='md',
                editor=idetools.getters.get_duration,
                ),
            )

    ### PRIVATE METHODS ###

    def _index_matches_patterns(self, index, total):
        if not self.patterns:
            return True
        for pattern in self.patterns:
            if pattern.matches_index(index, total):
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def hairpin_token(self):
        r'''Gets hairpin token of handler.

        Like ``('f', '>', 'p')``.

        Set to triple, string, list of triples, list of strings or none.

        Returns cyclic tuple.
        '''
        return self._hairpin_token

    @property
    def patterns(self):
        r'''Gets patterns of handler.

        Set to boolean patterns or none.
        '''
        return self._patterns

    @property
    def span(self):
        r'''Controls what is spanned.

        Defaults to ``'contiguous notes and chords'``.

        Set to ``'contiguous notes and chords'`` or ``'nontrivial ties'`` or to
        an iterable of positive integers.

        Returns one of the values listed above.
        '''
        return self._span