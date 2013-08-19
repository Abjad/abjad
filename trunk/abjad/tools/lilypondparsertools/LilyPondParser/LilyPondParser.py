# -*- encoding: utf-8 -*-
import itertools
import ply
from abjad.tools import abctools
from abjad.tools import chordtools
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import lilypondfiletools
from abjad.tools import marktools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools import stafftools
from abjad.tools import voicetools
from abjad.tools.lilypondparsertools._parse import _parse
from abjad.tools.lilypondparsertools._parse_debug import _parse_debug


# apply monkey patch
ply.yacc.LRParser._lilypond_patch_parse = _parse
ply.yacc.LRParser._lilypond_patch_parse_debug = _parse_debug


class LilyPondParser(abctools.Parser):
    r'''Parses a subset of LilyPond input syntax:

    ::

        >>> parser = lilypondparsertools.LilyPondParser()
        >>> input = r"\new Staff { c'4 ( d'8 e' fs'2) \fermata }"
        >>> result = parser(input)
        >>> f(result)
        \new Staff {
            c'4 (
            d'8
            e'8
            fs'2 -\fermata )
        }

    LilyPondParser defaults to English note names, but any of the other
    languages supported by LilyPond may be used:

    ::

        >>> parser = lilypondparsertools.LilyPondParser('nederlands')
        >>> input = '{ c des e fis }'
        >>> result = parser(input)
        >>> f(result)
        {
            c4
            df4
            e4
            fs4
        }

    Briefly, LilyPondParser understands theses aspects of LilyPond syntax:

    - Notes, chords, rests, skips and multi-measure rests
    - Durations, dots, and multipliers
    - All pitchnames, and octave ticks
    - Simple markup (i.e. ``c'4 ^ "hello!"``)
    - Most articulations
    - Most spanners, including beams, slurs, phrasing slurs, ties, and glissandi
    - Most context types via ``\new`` and ``\context``,
      as well as context ids (i.e. ``\new Staff = "foo" { }``)
    - Variable assignment (i.e. ``global = { \time 3/4 } \new Staff { \global }``)
    - Many music functions:
        - ``\acciaccatura``
        - ``\appoggiatura``
        - ``\bar``
        - ``\breathe``
        - ``\clef``
        - ``\grace``
        - ``\key``
        - ``\transpose``
        - ``\language``
        - ``\makeClusters``
        - ``\mark``
        - ``\oneVoice``
        - ``\relative``
        - ``\skip``
        - ``\slashedGrace``
        - ``\time``
        - ``\times``
        - ``\transpose``
        - ``\voiceOne``, ``\voiceTwo``, ``\voiceThree``, ``\voiceFour``

    LilyPondParser currently **DOES NOT** understand many other aspects of LilyPond syntax:

    - ``\markup``
    - ``\book``, ``\bookpart``, ``\header``, ``\layout``, ``\midi`` and ``\paper``
    - ``\repeat`` and ``\alternative``
    - Lyrics
    - ``\chordmode``, ``\drummode`` or ``\figuremode``
    - Property operations, such as ``\override``,
      ``\revert``, ``\set``, ``\unset``, and ``\once``
    - Music functions which generate or extensively mutate musical structures
    - Embedded Scheme statements (anything beginning with ``#``)

    Returns LilyPondParser instance.
    '''

    def __init__(self, default_language='english', debug=False):

        from abjad.tools import lilypondparsertools

        from abjad.ly.current_module import current_module
        from abjad.ly.language_pitch_names import language_pitch_names
        from abjad.ly.markup_functions import markup_functions
        from abjad.ly.markup_functions import markup_list_functions

        # LilyPond emulation data
        self._guile = lilypondparsertools.GuileProxy(self)
        self._current_module = current_module
        self._language_pitch_names = language_pitch_names
        self._markup_functions = markup_functions
        self._markup_list_functions = markup_list_functions
        self.default_language = default_language

        # attach parser and lexer rules
        self._lexdef = lilypondparsertools.LilyPondLexicalDefinition(self)
        self._syndef = lilypondparsertools.LilyPondSyntacticalDefinition(self)

        # build PLY parser and lexer
        abctools.Parser.__init__(self, debug=debug)

        self._reset_parser_variables()

    ### SPECIAL METHODS ###

    def __call__(self, input_string):

        self._reset_parser_variables()

        if self._debug:
            result = self._parser._lilypond_patch_parse_debug(
                input_string,
                lexer=self._lexer,
                debug=self._logger)
        else:
            result = self._parser._lilypond_patch_parse(
                input_string,
                lexer=self._lexer)

        if isinstance(result, containertools.Container):
            self._apply_spanners(result)
        elif isinstance(result, lilypondfiletools.LilyPondFile):
            for x in result:
                if isinstance(x, containertools.Container):
                    self._apply_spanners(x)
                elif isinstance(x, lilypondfiletools.ScoreBlock):
                    for y in x:
                        self._apply_spanners(y)

        return result


    ### PUBLIC PROPERTIES ###

    @property
    def available_languages(self):
        r'''Tuple of pitch-name languages supported by LilyPondParser:

        ::

            >>> parser = lilypondparsertools.LilyPondParser()
            >>> for language in parser.available_languages:
            ...     print language
            catalan
            deutsch
            english
            espanol
            español
            français
            italiano
            nederlands
            norsk
            portugues
            suomi
            svenska
            vlaams

        Return tuple.
        '''
        return tuple(sorted(self._language_pitch_names.keys()))

    @property
    def lexer_rules_object(self):
        return self._lexdef

    @property
    def parser_rules_object(self):
        return self._syndef

    ### PUBLIC PROPERTIES ###

    @apply
    def default_language():
        def fget(self):
            r'''Read/write attribute to set parser's default pitch-name language:

            ::

                >>> parser = lilypondparsertools.LilyPondParser()

            ::

                >>> parser.default_language
                'english'

            ::

                >>> parser('{ c df e fs }')
                {c4, df4, e4, fs4}

            ::

                >>> parser.default_language = 'nederlands'
                >>> parser.default_language
                'nederlands'

            ::

                >>> parser('{ c des e fis }')
                {c4, df4, e4, fs4}

            Return string.
            '''
            return self._default_language
        def fset(self, arg):
            assert arg in self.available_languages
            self._default_language = arg
        return property(**locals())

    ### PRIVATE METHODS ###

    def _apply_spanners(self, music):

        # get local reference to methods
        _get_span_events = self._get_span_events
        _span_event_name_to_spanner_class = self._span_event_name_to_spanner_class

        # dictionary of spanner classes and instances
        all_spanners = { }

        # traverse all leaves
        leaves = music.select_leaves(allow_discontiguous_leaves=True)
        first_leaf = None
        if leaves:
            first_leaf = leaves[0]
        for leaf, next_leaf in sequencetools.iterate_sequence_pairwise_wrapped(leaves):

            span_events = _get_span_events(leaf)
            directed_events = { }

            # sort span events into directed and undirected groups
            for span_event in span_events:
                spanner_class = _span_event_name_to_spanner_class(span_event.name)

                # group directed span events by their Abjad spanner class
                if hasattr(span_event, 'span_direction'):
                    if spanner_class not in directed_events:
                        directed_events[spanner_class] = [span_event]
                    else:
                        directed_events[spanner_class].append(span_event)
                    if spanner_class not in all_spanners:
                        all_spanners[spanner_class] = []

                # or apply undirected event immediately (i.e. ties, glisses)
                elif next_leaf is not first_leaf: # so long as we are not wrapping yet
                    previous_spanners = [
                        x for x in leaf._get_spanners() 
                        if isinstance(x, spanner_class)
                        ]
                    if previous_spanners:
                        previous_spanners[0].append(next_leaf)
                    else:
                        if hasattr(span_event, 'direction') and \
                            hasattr(spanner_class, 'direction'):
                            spanner_class(
                                [leaf, next_leaf], 
                                direction=span_event.direction
                                )
                        else:
                            spanner_class([leaf, next_leaf])

                # otherwise throw an error
                else:
                    raise Exception('Unterminated %s at %s.' % (spanner_class.__name__, leaf))

            # check for DynamicMarks, and terminate any hairpin
            dynamics = leaf._get_marks(contexttools.DynamicMark)
            if dynamics and spannertools.HairpinSpanner in all_spanners and \
                all_spanners[spannertools.HairpinSpanner]:
                all_spanners[spannertools.HairpinSpanner][0].append(leaf)
                all_spanners[spannertools.HairpinSpanner].pop()

            # loop through directed events, handling each as necessary
            for spanner_class, events in directed_events.iteritems():

                starting_events, stopping_events = [], []
                for x in events:
                    if x.span_direction == 'start':
                        starting_events.append(x)
                    else:
                        stopping_events.append(x)

                if spanner_class is spannertools.BeamSpanner:
                    # A beam may begin and end on the same leaf
                    # but only one beam spanner may cover any given leaf,
                    # and starting events are processed before ending ones
                    for event in starting_events:
                        if all_spanners[spanner_class]:
                            raise Exception('Already have beam.')
                        if hasattr(event, 'direction'):
                            all_spanners[spanner_class].append(spanner_class(direction=event.direction))
                        else:
                            all_spanners[spanner_class].append(spanner_class())
                    for _ in stopping_events:
                        if all_spanners[spanner_class]:
                            all_spanners[spanner_class][0].append(leaf)
                            all_spanners[spanner_class].pop()

                elif spanner_class is spannertools.HairpinSpanner:
                    # Dynamic events can be ended many times,
                    # but only one may start on a given leaf,
                    # and the event must start and end on separate leaves.
                    # If a hairpin already exists and another starts,
                    # the pre-existant spanner is ended.
                    for _ in stopping_events:
                        if all_spanners[spanner_class]:
                            all_spanners[spanner_class][0].append(leaf)
                            all_spanners[spanner_class].pop()
                    if 1 == len(starting_events):
                        if all_spanners[spanner_class]:
                            all_spanners[spanner_class][0].append(leaf)
                            all_spanners[spanner_class].pop()
                        shape = '<'
                        event = starting_events[0]
                        if event.name == 'DecrescendoEvent':
                            shape = '>'
                        if hasattr(event, 'direction'):
                            all_spanners[spanner_class].append(spanner_class([], shape, direction=event.direction))
                        else:
                            all_spanners[spanner_class].append(spanner_class([], shape))
                    elif 1 < len(starting_events):
                        raise Exception('Simultaneous dynamic-span events.')

                elif spanner_class in [spannertools.SlurSpanner, spannertools.PhrasingSlurSpanner,
                    spannertools.TextSpanner, spannertools.TrillSpanner]:
                    # These engravers process stop events before start events,
                    # they must contain more than one leaf,
                    # however, they can stop on a leaf and start on the same leaf.
                    for _ in stopping_events:
                        if all_spanners[spanner_class]:
                            all_spanners[spanner_class][0].append(leaf)
                            all_spanners[spanner_class].pop()
                        else:
                            raise Exception('Cannot end %s.' % spanner_class.__name__)
                    for event in starting_events:
                        if not all_spanners[spanner_class]:
                            if hasattr(event, 'direction') and hasattr(spanner_class, 'direction'):
                                all_spanners[spanner_class].append(spanner_class(direction=event.direction))
                            else:
                                all_spanners[spanner_class].append(spanner_class())
                        else:
                            raise Exception('Already have %s.' % spanner_class.__name__)

                elif spanner_class is spannertools.HorizontalBracketSpanner:
                    # Brackets can nest, meaning
                    # multiple brackets can begin or end on a leaf
                    # but cannot both begin and end on the same leaf
                    # and therefore a bracket cannot cover a single leaf
                    has_starting_events = bool(len(starting_events))
                    for _ in starting_events:
                        all_spanners[spanner_class].append(spanner_class())
                    if stopping_events:
                        if not has_starting_events:
                            for _ in stopping_events:
                                if all_spanners[spanner_class]:
                                    all_spanners[spanner_class][-1].append(leaf)
                                    all_spanners[spanner_class].pop()
                                else:
                                    raise Exception('Do not have that many brackets.')
                        else:
                            raise Exception('Conflicting note group events.')

            # append leaf to all tracked spanners,
            for spanner_class, instances in all_spanners.iteritems():
                for instance in instances:
                    instance.append(leaf)

        # check for unterminated spanners
        for spanner_class, instances in all_spanners.iteritems():
            if instances:
                raise Exception('Unterminated %s.' % spanner_class.__name__)

    def _assign_variable(self, identifier, value):
        self._scope_stack[-1][identifier] = value

    def _backup_token(self, token_type, token_value):
        if self._debug:
            self._logger.info('Extra  : Backing up')

        # push the current lookahead back onto the lookaheadstack
        self._push_extra_token(self._parser.lookahead)

        # create the backup token, set as new lookahead
        backup = ply.lex.LexToken()
        backup.type = 'BACKUP'
        backup.value = '(backed-up?)'
        backup.lexpos = 0
        backup.lineno = 0
        self._parser.lookahead = backup

        if token_type:
            token = ply.lex.LexToken()
            token.type = token_type
            token.value = token_value
            token.lexpos = 0
            token.lineno = 0
            self._push_extra_token(token)

    def _construct_context_specced_music(self, context, optional_id, optional_context_mod, music):
        known_contexts = {
            'ChoirStaff': scoretools.StaffGroup,
            'GrandStaff': scoretools.GrandStaff,
            'PianoStaff': scoretools.PianoStaff,
            'Score': scoretools.Score,
            'Staff': stafftools.Staff,
            'StaffGroup': scoretools.StaffGroup,
            'Voice': voicetools.Voice,
        }
        if context in known_contexts:
            context = known_contexts[context]([])
        else:
            raise Exception('Context type %s not supported.' % context)

        if optional_id is not None:
            context.name = optional_id

        if optional_context_mod is not None:
            for x in optional_context_mod:
                print x
            pass # TODO: Implement context mods on contexts. #

        context.is_simultaneous = music.is_simultaneous

        # add children
        while len(music):
            component = music.pop(0)
            context.append(component)

        marks = music._start_marks
        for mark in marks:
            mark(context)

        return context

    def _construct_sequential_music(self, music):
        # mark sorting could be rewritten into a single list, using tuplets,
        # with t[0] being 'forward' or 'backward' and t[1] being the mark, as
        # this better preserves attachment order.  Not clear if we need it.

        container = containertools.Container()
        previous_leaf = None
        apply_forward = []
        apply_backward = []

        # sort events into forward or backwards attaching, and attach them to
        # the proper leaf
        for x in music:
            if isinstance(x, componenttools.Component) \
                and not isinstance(x, leaftools.GraceContainer):
                for mark in apply_forward:
                    if hasattr(mark, 'attach'):
                        mark(x)
                if previous_leaf:
                    for mark in apply_backward:
                        if hasattr(mark, 'attach'):
                            mark(previous_leaf)
                else:
                    for mark in apply_backward:
                        if hasattr(mark, 'attach'):
                            mark.format_slot = 'before'
                            mark(x)
                apply_forward = []
                apply_backward = []
                previous_leaf = x
                container.append(x)
            else:
                if isinstance(x, marktools.BarLine):
                    apply_backward.append(x)
                elif isinstance(x, marktools.LilyPondCommandMark) and \
                    x.command_name in ['breathe']:
                        apply_backward.append(x)
                else:
                    apply_forward.append(x)

        # attach remaining events to last leaf, or to the container itself if
        # there were no leaves
        if previous_leaf:
            for mark in apply_forward:
                if hasattr(mark, 'attach'):
                    mark.format_slot = 'after'
                    mark(previous_leaf)
            for mark in apply_backward:
                if hasattr(mark, 'attach'):
                    mark(previous_leaf)
        else:
            for mark in apply_forward:
                if hasattr(mark, 'attach'):
                    mark.format_slot = 'opening'
                    mark(container)
            for mark in apply_backward:
                if hasattr(mark, 'attach'):
                    mark.format_slot = 'opening'
                    mark(container)

        return container

    def _construct_simultaneous_music(self, music):
        from abjad.tools import lilypondparsertools
        def is_separator(x):
            if isinstance(x, lilypondparsertools.LilyPondEvent):
                if x.name == 'VoiceSeparator':
                    return True
            return False

        container = containertools.Container()
        container.is_simultaneous = True

        # check for voice separators
        groups = []
        for value, group in itertools.groupby(music, is_separator):
            if not value:
                groups.append(list(group))

        # without voice separators
        if 1 == len(groups):
            assert all(isinstance(x, contexttools.Context) for x in groups[0])
            container.extend(groups[0])
        # with voice separators
        else:
            for group in groups:
                container.append(Voice(self._construct_sequential_music(group)[:]))

        return container

    @classmethod
    def _get_scheme_predicates(cls):
        return {
            'boolean?':           lambda x: isinstance(x, bool),
            'cheap-list?':        lambda x: isinstance(x, (list, tuple)),
            'cheap-markup?':      lambda x: isinstance(x, markuptools.MarkupCommand),
            'fraction?':          lambda x: isinstance(x, lilypondparsertools.LilyPondFraction),
            'integer?':           lambda x: isinstance(x, int),
            'list?':              lambda x: isinstance(x, (list, tuple)),
            'ly:duration?':       lambda x: isinstance(x, lilypondparsertools.LilyPondDuration),
            'ly:music?':          lambda x: isinstance(x, (componenttools.Component, marktools.Mark)),
            'ly:pitch?':          lambda x: isinstance(x, pitchtools.NamedPitch),
            'markup?':            lambda x: isinstance(x, markuptools.MarkupCommand),
            'number-list?':       lambda x: isinstance(x, (list, tuple)) and \
                                            all(isinstance(y, (int, float)) for y in x),
            'number?':            lambda x: isinstance(x, (int, float)),
            'real?':              lambda x: isinstance(x, (int, float)),
            'string?':            lambda x: isinstance(x, (str, unicode)),
            'void?':              lambda x: isinstance(x, type(None)),
            # the following predicates have not yet been implemented in Abjad
            'hash-table?':        lambda x: True,
            'list-or-symbol?':    lambda x: True,
            'ly:dir?':            lambda x: True,
            'ly:moment?':         lambda x: True,
            'number-or-string?':  lambda x: True,
            'number-pair?':       lambda x: True,
            'optional?':          lambda x: True,
            'pair?':              lambda x: True,
            'procedure?':         lambda x: True,
            'scheme?':            lambda x: True,
            'string-or-pair?':    lambda x: True,
            'symbol-or-boolean?': lambda x: True,
            'symbol?':            lambda x: True,
        }

    def _get_span_events(self, leaf):
        annotations = leaf.select().detach_marks(marktools.Annotation)
        if annotations:
            spanners_annotations = [x for x in annotations if x.name == 'spanners']
            if 1 == len(spanners_annotations):
                return spanners_annotations[0].value
            elif 1 < len(spanners_annotations):
                raise Exception('Multiple span events lists attached to %s' % leaf)
        return []

    def _pop_variable_scope(self):
        if self._scope_stack:
            self._scope_stack.pop()

    def _process_post_events(self, leaf, post_events):
        for post_event in post_events:
            if hasattr(post_event, '__call__'):
                post_event(leaf)
            else:
                annotation = [
                    x for x in leaf._get_marks(marktools.Annotation)
                    if x.name == 'spanners'
                    ]
                if not annotation:
                    annotation = marktools.Annotation('spanners', [])(leaf)
                else:
                    annotation = annotation[0]
                annotation.value.append(post_event)

    def _push_extra_token(self, token):
        self._parser.lookaheadstack.append(token)

    def _push_variable_scope(self):
        self._scope_stack.append({})

    def _relex_lookahead(self):
        if not str(self._parser.lookahead) == '$end':
            difference = self._parser.lookahead.lexpos - self._lexer.lexpos
            self._lexer.skip(difference)
            self._parser.lookahead = None

    def _reparse_token(self, predicate, token_type, token_value):
        if self._debug:
            self._logger.info('Extra  : Reparsing')

        # push the current lookahead back onto the lookaheadstack
        self._push_extra_token(self._parser.lookahead)

        token = ply.lex.LexToken()
        token.type = token_type
        token.value = token_value
        token.lexpos = 0
        token.lineno = 0
        self._push_extra_token(token)

        reparse = ply.lex.LexToken()
        reparse.type = 'REPARSE'
        reparse.value = predicate
        reparse.lineno = 0
        reparse.lexpos = 0
        self._parser.lookahead = reparse

    def _reset_parser_variables(self):
        from abjad.tools import lilypondparsertools
        try:
            self._parser.restart()
        except:
            pass
        self._scope_stack = [{}]
        self._chord_pitch_orders = {}
        self._lexer.push_state('notes')
        self._default_duration = lilypondparsertools.LilyPondDuration(durationtools.Duration(1, 4), None)
        self._last_chord = None
        # self._last_chord = chordtools.Chord(['c', 'g', "c'"], (1, 4)) # LilyPond's default!
        self._pitch_names = self._language_pitch_names[self.default_language]
        self._repeated_chords = {}

    def _resolve_event_identifier(self, identifier):
        from abjad.tools import lilypondparsertools
        lookup = self._current_module[identifier] # without any leading slash
        name = lookup['name']
        if name == 'ArticulationEvent':
            return marktools.Articulation(lookup['articulation-type'])
        elif name == 'AbsoluteDynamicEvent':
            return contexttools.DynamicMark(lookup['text'])
        elif name == 'LaissezVibrerEvent':
            return marktools.LilyPondCommandMark('laissezVibrer', 'after')
        event = lilypondparsertools.LilyPondEvent(name)
        if 'span-direction' in lookup:
            if lookup['span-direction'] == -1:
                event.span_direction = 'start'
            else:
                event.span_direction = 'stop'
        return event

    def _resolve_identifier(self, identifier):
        for scope in reversed(self._scope_stack):
            if identifier in scope:
                return scope[identifier]
        return None

    def _span_event_name_to_spanner_class(self, name):
        spanners = {
            'BeamEvent': spannertools.BeamSpanner,
            'CrescendoEvent': spannertools.HairpinSpanner,
            'DecrescendoEvent': spannertools.HairpinSpanner,
            'GlissandoEvent': spannertools.GlissandoSpanner,
            'NoteGroupingEvent': spannertools.HorizontalBracketSpanner,
            'PhrasingSlurEvent': spannertools.PhrasingSlurSpanner,
            'SlurEvent': spannertools.SlurSpanner,
            'TextSpanEvent': spannertools.TextSpanner,
            'TieEvent': spannertools.TieSpanner,
            'TrillSpanEvent': spannertools.TrillSpanner,
        }
        if name in spanners:
            return spanners[name]
        raise Exception('Abjad cannot associate a spanner class with %s' % name)

    def _test_scheme_predicate(self, predicate, value):
        from abjad.tools import lilypondparsertools
        predicates = self._get_scheme_predicates()
        if predicate in predicates:
            return predicates[predicate](value)
        return True

    @staticmethod
    def _transpose_enharmonically(pitch_a, pitch_b, pitch_c):
        r'''Transpose `pitch_c` by the distance between `pitch_b` and `pitch_a`.

        This function was reverse-engineered from LilyPond's source code.

        Return NamedPitch.
        '''
        if not isinstance(pitch_a, pitchtools.NamedPitch):
            pitch_a = pitchtools.NamedPitch(pitch_a)
        if not isinstance(pitch_b, pitchtools.NamedPitch):
            pitch_b = pitchtools.NamedPitch(pitch_b)
        if not isinstance(pitch_c, pitchtools.NamedPitch):
            pitch_c = pitchtools.NamedPitch(pitch_c)
        scale = [0., 2., 4., 5., 7., 9., 11.]
        def normalize_alteration(step, alteration):
            while 2. < alteration:
                alteration -= step_size(step)
                step += 1.
            while alteration < -2.:
                step -= 1.
                alteration += step_size(step)
            return step, alteration
        def normalize_octave(octave, step):
            normalized_step = step % len(scale)
            octave += (step - normalized_step) / len(scale)
            return octave, normalized_step
        def step_size(step):
            normalized_step = step % len(scale)
            if normalized_step == 6:
                return 1. # b to c
            return scale[normalized_step + 1] - scale[normalized_step]
        a_oct, a_step, a_alt = pitch_a.octave_number, \
            pitch_a.diatonic_pitch_class_number, pitch_a._accidental.semitones
        b_oct, b_step, b_alt = pitch_b.octave_number, \
            pitch_b.diatonic_pitch_class_number, pitch_b._accidental.semitones
        c_oct, c_step, c_alt = pitch_c.octave_number, \
            pitch_c.diatonic_pitch_class_number, pitch_c._accidental.semitones
        d_oct, d_step, d_alt, d_tones = b_oct - a_oct, b_step - a_step, \
            b_alt - a_alt, float(pitch_b) - float(pitch_a)
        tmp_alt = float(pitch_c) + d_tones
        # print 'TMP_ALT: %f' % tmp_alt
        new_oct = c_oct + d_oct
        new_step = c_step + d_step
        new_alt = c_alt
        # print 'NEW:', new_oct, new_step, new_alt
        new_step, new_alt = normalize_alteration(new_step, new_alt)
        new_oct, new_step = normalize_octave(new_oct, new_step)
        # print 'NEW(norm):', new_oct, new_step, new_alt
        octave_ticks = pitchtools.octave_number_to_octave_tick_string(new_oct)
        pitch_class_name = \
            pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_name(
                new_step)
        #pitch_class_name = str(pitchtools.NamedDiatonicPitchClass(
        #    int(new_step)))
        accidental = str(pitchtools.Accidental(new_alt))
        tmp_pitch = pitchtools.NamedPitch(
            pitch_class_name + accidental + octave_ticks)
        # print 'TMP(pitch): %r' % tmp_pitch
        new_alt += tmp_alt - float(tmp_pitch)
        # print 'NEW(alt): %f' % new_alt
        new_step, new_alt = normalize_alteration(new_step, new_alt)
        new_oct, new_step = normalize_octave(new_oct, new_step)
        # print 'NEW(norm):', new_oct, new_step, new_alt
        octave_ticks = pitchtools.octave_number_to_octave_tick_string(new_oct)
        #pitch_class_name = str(pitchtools.NamedDiatonicPitchClass(
        #    int(new_step)))
        pitch_class_name = \
            pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_name(
                new_step)
        accidental = str(pitchtools.Accidental(new_alt))
        return pitchtools.NamedPitch(
            pitch_class_name + accidental + octave_ticks)

    ### PUBLIC METHODS ###

    @staticmethod
    def list_known_contexts():
        r'''List all LilyPond contexts recognized by ``LilyPondParser``:

        ::

            >>> for x in lilypondparsertools.LilyPondParser.list_known_contexts():
            ...     print x
            ...
            ChoirStaff
            ChordNames
            CueVoice
            Devnull
            DrumStaff
            DrumVoice
            Dynamics
            FiguredBass
            FretBoards
            Global
            GrandStaff
            GregorianTranscriptionStaff
            GregorianTranscriptionVoice
            KievanStaff
            KievanVoice
            Lyrics
            MensuralStaff
            MensuralVoice
            NoteNames
            PetrucciStaff
            PetrucciVoice
            PianoStaff
            RhythmicStaff
            Score
            Staff
            StaffGroup
            TabStaff
            TabVoice
            VaticanaStaff
            VaticanaVoice
            Voice

        Return list.
        '''
        from abjad.ly import contexts
        return sorted(contexts.keys())
        
    @staticmethod
    def list_known_grobs():
        r'''List all LilyPond grobs recognized by ``LilyPondParser``:

        ::

            >>> for x in lilypondparsertools.LilyPondParser.list_known_grobs():
            ...     print x
            ...
            Accidental
            AccidentalCautionary
            AccidentalPlacement
            AccidentalSuggestion
            Ambitus
            AmbitusAccidental
            AmbitusLine
            AmbitusNoteHead
            Arpeggio
            BalloonTextItem
            BarLine
            BarNumber
            BassFigure
            BassFigureAlignment
            BassFigureAlignmentPositioning
            BassFigureBracket
            BassFigureContinuation
            BassFigureLine
            Beam
            BendAfter
            BreakAlignGroup
            BreakAlignment
            BreathingSign
            ChordName
            Clef
            ClusterSpanner
            ClusterSpannerBeacon
            CombineTextScript
            CueClef
            CueEndClef
            Custos
            DotColumn
            Dots
            DoublePercentRepeat
            DoublePercentRepeatCounter
            DoubleRepeatSlash
            DynamicLineSpanner
            DynamicText
            DynamicTextSpanner
            Episema
            Fingering
            FingeringColumn
            Flag
            FootnoteItem
            FootnoteSpanner
            FretBoard
            Glissando
            GraceSpacing
            GridLine
            GridPoint
            Hairpin
            HorizontalBracket
            InstrumentName
            InstrumentSwitch
            KeyCancellation
            KeySignature
            LaissezVibrerTie
            LaissezVibrerTieColumn
            LedgerLineSpanner
            LeftEdge
            LigatureBracket
            LyricExtender
            LyricHyphen
            LyricSpace
            LyricText
            MeasureCounter
            MeasureGrouping
            MelodyItem
            MensuralLigature
            MetronomeMark
            MultiMeasureRest
            MultiMeasureRestNumber
            MultiMeasureRestText
            NonMusicalPaperColumn
            NoteCollision
            NoteColumn
            NoteHead
            NoteName
            NoteSpacing
            OctavateEight
            OttavaBracket
            PaperColumn
            ParenthesesItem
            PercentRepeat
            PercentRepeatCounter
            PhrasingSlur
            PianoPedalBracket
            RehearsalMark
            RepeatSlash
            RepeatTie
            RepeatTieColumn
            Rest
            RestCollision
            Script
            ScriptColumn
            ScriptRow
            Slur
            SostenutoPedal
            SostenutoPedalLineSpanner
            SpacingSpanner
            SpanBar
            SpanBarStub
            StaffGrouper
            StaffSpacing
            StaffSymbol
            StanzaNumber
            Stem
            StemStub
            StemTremolo
            StringNumber
            StrokeFinger
            SustainPedal
            SustainPedalLineSpanner
            System
            SystemStartBar
            SystemStartBrace
            SystemStartBracket
            SystemStartSquare
            TabNoteHead
            TextScript
            TextSpanner
            Tie
            TieColumn
            TimeSignature
            TrillPitchAccidental
            TrillPitchGroup
            TrillPitchHead
            TrillSpanner
            TupletBracket
            TupletNumber
            UnaCordaPedal
            UnaCordaPedalLineSpanner
            VaticanaLigature
            VerticalAlignment
            VerticalAxisGroup
            VoiceFollower
            VoltaBracket
            VoltaBracketSpanner

        Return tuple.
        '''
        from abjad.ly import grob_interfaces
        return sorted(grob_interfaces.keys())

    @staticmethod
    def list_known_languages():
        r'''List all note-input languages recognized by ``LilyPondParser``:

        ::

            >>> for x in lilypondparsertools.LilyPondParser.list_known_languages():
            ...     print x
            ...
            catalan
            deutsch
            english
            espanol
            español
            français
            italiano
            nederlands
            norsk
            portugues
            suomi
            svenska
            vlaams

        Return list.
        '''
        from abjad.ly import language_pitch_names
        return sorted(language_pitch_names.keys())

    @staticmethod
    def list_known_markup_functions():
        r'''List all markup functions recognized by ``LilyPondParser``:

        ::

            >>> for x in lilypondparsertools.LilyPondParser.list_known_markup_functions():
            ...     print x
            ...
            abs-fontsize
            arrow-head
            auto-footnote
            backslashed-digit
            beam
            bold
            box
            bracket
            caps
            center-align
            center-column
            char
            circle
            column
            column-lines
            combine
            concat
            customTabClef
            dir-column
            doubleflat
            doublesharp
            draw-circle
            draw-hline
            draw-line
            dynamic
            epsfile
            eyeglasses
            fill-line
            fill-with-pattern
            filled-box
            finger
            flat
            fontCaps
            fontsize
            footnote
            fraction
            fret-diagram
            fret-diagram-terse
            fret-diagram-verbose
            fromproperty
            general-align
            halign
            harp-pedal
            hbracket
            hcenter-in
            hspace
            huge
            italic
            justified-lines
            justify
            justify-field
            justify-string
            large
            larger
            left-align
            left-brace
            left-column
            line
            lookup
            lower
            magnify
            markalphabet
            markletter
            medium
            musicglyph
            natural
            normal-size-sub
            normal-size-super
            normal-text
            normalsize
            note
            note-by-number
            null
            number
            on-the-fly
            override
            override-lines
            pad
            pad-around
            pad-to-box
            pad-x
            page-link
            page-ref
            parenthesize
            path
            pattern
            postscript
            property-recursive
            put-adjacent
            raise
            replace
            rest
            rest-by-number
            right-align
            right-brace
            right-column
            roman
            rotate
            rounded-box
            sans
            scale
            score
            semiflat
            semisharp
            sesquiflat
            sesquisharp
            sharp
            simple
            slashed-digit
            small
            smallCaps
            smaller
            stencil
            strut
            sub
            super
            table-of-contents
            teeny
            text
            tied-lyric
            tiny
            translate
            translate-scaled
            transparent
            triangle
            typewriter
            underline
            upright
            vcenter
            verbatim-file
            vspace
            whiteout
            with-color
            with-dimensions
            with-link
            with-url
            woodwind-diagram
            wordwrap
            wordwrap-field
            wordwrap-internal
            wordwrap-lines
            wordwrap-string
            wordwrap-string-internal

        Return list.
        '''
        from abjad.ly import markup_functions
        from abjad.ly import markup_list_functions
        return sorted(markup_functions.keys() + markup_list_functions.keys())

    @staticmethod
    def list_known_music_functions():
        r'''List all music functions recognized by ``LilyPondParser``:

        ::

            >>> for x in lilypondparsertools.LilyPondParser.list_known_music_functions():
            ...     print x
            ...
            acciaccatura
            appoggiatura
            bar
            breathe
            clef
            grace
            key
            language
            makeClusters
            mark
            relative
            skip
            time
            times
            transpose

        Return list.
        '''
        from abjad.ly import current_module
        from abjad.tools import lilypondparsertools
        music_functions = []
        for name in current_module:
            if not isinstance(current_module[name], dict):
                continue
            if not 'type' in current_module[name]:
                continue
            if not current_module[name]['type'] == 'ly:music-function?':
                continue
            if not hasattr(lilypondparsertools.GuileProxy, name):
                continue
            music_functions.append(name)
        return sorted(music_functions)

    @classmethod
    def register_markup_function(cls, name, signature):
        r'''Register a custom markup function globally with LilyPondParser:

        ::

            >>> name = 'my-custom-markup-function'
            >>> signature = ['markup?']
            >>> lilypondparsertools.LilyPondParser.register_markup_function(name, signature)

        ::

            >>> parser = lilypondparsertools.LilyPondParser()
            >>> string = r"\markup { \my-custom-markup-function { foo bar baz } }"
            >>> parser(string)
            Markup((MarkupCommand('my-custom-markup-function', ['foo', 'bar', 'baz']),))

        `signature` should be a sequence of zero or more type-predicate names, as
        understood by LilyPond.  Consult LilyPond's documentation for a complete
        list of all understood type-predicates.

        Return None
        '''

        from abjad.ly.markup_functions import markup_functions

        assert isinstance(name, str)
        assert all(not x.isspace() for x in name)
        assert isinstance(signature, (list, tuple))
        for predicate in signature:
            assert isinstance(predicate, str)
            assert all(not x.isspace() for x in predicate)
            assert predicate.endswith('?')

        markup_functions[name] = tuple(signature)
