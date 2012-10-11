import itertools
from ply import lex
from ply import yacc
from abjad.tools import abctools
from abjad.tools import beamtools
from abjad.tools import chordtools
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import gracetools
from abjad.tools import lilypondfiletools
from abjad.tools import marktools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools import stafftools
from abjad.tools import tietools
from abjad.tools import voicetools
from abjad.tools.lilypondparsertools._parse import _parse
from abjad.tools.lilypondparsertools._parse_debug import _parse_debug


# apply monkey patch
yacc.LRParser._lilypond_patch_parse = _parse
yacc.LRParser._lilypond_patch_parse_debug = _parse_debug


class LilyPondParser(abctools.Parser):
    r'''Parses a subset of LilyPond input syntax:

    ::

        >>> from abjad.tools.lilypondparsertools import LilyPondParser

    ::

        >>> parser = LilyPondParser()
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

        >>> parser = LilyPondParser('nederlands')
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

        from abjad.ly.py.current_module import current_module
        from abjad.ly.py.language_pitch_names import language_pitch_names
        from abjad.ly.py.markup_functions import markup_functions
        from abjad.ly.py.markup_functions import markup_list_functions

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


    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def available_languages(self):
        '''Tuple of pitch-name languages supported by LilyPondParser:

        ::

            >>> from abjad.tools.lilypondparsertools import LilyPondParser
            >>> parser = LilyPondParser()
            >>> parser.available_languages
            ('catalan', 'deutsch', 'english', 'espanol', 'italiano', 'nederlands', 
            'norsk', 'portugues', 'suomi', 'svenska', 'vlaams')

        Return tuple.
        '''
        return tuple(sorted(self._language_pitch_names.keys()))

    @property
    def lexer_rules_object(self):
        return self._lexdef

    @property
    def parser_rules_object(self):
        return self._syndef

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def default_language():
        def fget(self):
            '''Read/write attribute to set parser's default pitch-name language:

            ::

                >>> from abjad.tools.lilypondparsertools import LilyPondParser

            ::

                >>> parser = LilyPondParser()

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
        leaves = music.leaves
        first_leaf = None
        if leaves:
            first_leaf = leaves[0]
        for leaf, next_leaf in sequencetools.iterate_sequence_pairwise_wrapped(leaves):

            span_events = _get_span_events(leaf)
            directed_events = { }

            # sort span events into directed and undirected groups
            for span_event in span_events:
                klass = _span_event_name_to_spanner_class(span_event.name)

                # group directed span events by their Abjad spanner class
                if hasattr(span_event, 'span_direction'):
                    if klass not in directed_events:
                        directed_events[klass] = [span_event]
                    else:
                        directed_events[klass].append(span_event)
                    if klass not in all_spanners:
                        all_spanners[klass] = []

                # or apply undirected event immediately (i.e. ties, glisses)
                elif next_leaf is not first_leaf: # so long as we are not wrapping yet
                    previous_spanners = [x for x in leaf.spanners if isinstance(x, klass)]
                    if previous_spanners:
                        previous_spanners[0].append(next_leaf)
                    else:
                        if hasattr(span_event, 'direction') and hasattr(klass, 'direction'):
                            klass([leaf, next_leaf], direction=span_event.direction)
                        else:
                            klass([leaf, next_leaf])

                # otherwise throw an error
                else:
                    raise Exception('Unterminated %s at %s.' % (klass.__name__, leaf))

            # check for DynamicMarks, and terminate any hairpin
            dynamics = contexttools.get_dynamic_marks_attached_to_component(leaf)
            if dynamics and spannertools.HairpinSpanner in all_spanners and \
                all_spanners[spannertools.HairpinSpanner]:
                all_spanners[spannertools.HairpinSpanner][0].append(leaf)
                all_spanners[spannertools.HairpinSpanner].pop()

            # loop through directed events, handling each as necessary
            for klass, events in directed_events.iteritems():

                starting_events, stopping_events = [], []
                for x in events:
                    if x.span_direction == 'start':
                        starting_events.append(x)
                    else:
                        stopping_events.append(x)

                if klass is beamtools.BeamSpanner:
                    # A beam may begin and end on the same leaf
                    # but only one beam spanner may cover any given leaf,
                    # and starting events are processed before ending ones
                    for event in starting_events:
                        if all_spanners[klass]:
                            raise Exception('Already have beam.')
                        if hasattr(event, 'direction'):
                            all_spanners[klass].append(klass(direction=event.direction))
                        else:
                            all_spanners[klass].append(klass())
                    for _ in stopping_events:
                        if all_spanners[klass]:
                            all_spanners[klass][0].append(leaf)
                            all_spanners[klass].pop()

                elif klass is spannertools.HairpinSpanner:
                    # Dynamic events can be ended many times,
                    # but only one may start on a given leaf,
                    # and the event must start and end on separate leaves.
                    # If a hairpin already exists and another starts,
                    # the pre-existant spanner is ended.
                    for _ in stopping_events:
                        if all_spanners[klass]:
                            all_spanners[klass][0].append(leaf)
                            all_spanners[klass].pop()
                    if 1 == len(starting_events):
                        if all_spanners[klass]:
                            all_spanners[klass][0].append(leaf)
                            all_spanners[klass].pop()
                        shape = '<'
                        event = starting_events[0]
                        if event.name == 'DecrescendoEvent':
                            shape = '>'
                        if hasattr(event, 'direction'):
                            all_spanners[klass].append(klass([], shape, direction=event.direction))
                        else:
                            all_spanners[klass].append(klass([], shape))
                    elif 1 < len(starting_events):
                        raise Exception('Simultaneous dynamic-span events.')
                    
                elif klass in [spannertools.SlurSpanner, spannertools.PhrasingSlurSpanner,
                    spannertools.TextSpanner, spannertools.TrillSpanner]:
                    # These engravers process stop events before start events,
                    # they must contain more than one leaf,
                    # however, they can stop on a leaf and start on the same leaf.
                    for _ in stopping_events:                    
                        if all_spanners[klass]:
                            all_spanners[klass][0].append(leaf)
                            all_spanners[klass].pop()
                        else:
                            raise Exception('Cannot end %s.' % klass.__name__)
                    for event in starting_events:
                        if not all_spanners[klass]:
                            if hasattr(event, 'direction') and hasattr(klass, 'direction'):
                                all_spanners[klass].append(klass(direction=event.direction))
                            else:
                                all_spanners[klass].append(klass())
                        else:
                            raise Exception('Already have %s.' % klass.__name__)

                elif klass is spannertools.HorizontalBracketSpanner:
                    # Brackets can nest, meaning
                    # multiple brackets can begin or end on a leaf
                    # but cannot both begin and end on the same leaf
                    # and therefore a bracket cannot cover a single leaf
                    has_starting_events = bool(len(starting_events))
                    for _ in starting_events:
                        all_spanners[klass].append(klass())
                    if stopping_events:
                        if not has_starting_events:
                            for _ in stopping_events:
                                if all_spanners[klass]:
                                    all_spanners[klass][-1].append(leaf)
                                    all_spanners[klass].pop()
                                else:
                                    raise Exception('Do not have that many brackets.')
                        else:
                            raise Exception('Conflicting note group events.')

            # append leaf to all tracked spanners,
            for klass, instances in all_spanners.iteritems():
                for instance in instances:
                    instance.append(leaf)

        # check for unterminated spanners
        for klass, instances in all_spanners.iteritems():
            if instances:
                raise Exception('Unterminated %s.' % klass.__name__)

    def _assign_variable(self, identifier, value):
        self._scope_stack[-1][identifier] = value

    def _backup_token(self, token_type, token_value):
        if self._debug:
            self._logger.info('Extra  : Backing up')

        # push the current lookahead back onto the lookaheadstack
        self._push_extra_token(self._parser.lookahead)

        # create the backup token, set as new lookahead
        backup = lex.LexToken()
        backup.type = 'BACKUP'
        backup.value = '(backed-up?)'
        backup.lexpos = 0
        backup.lineno = 0
        self._parser.lookahead = backup

        if token_type:
            token = lex.LexToken()
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

        context.is_parallel = music.is_parallel

        # add children
        while len(music):
            component = music.pop(0)
            context.append(component)

        marks = music._marks_for_which_component_functions_as_start_component
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
            if isinstance(x, componenttools.Component) and not isinstance(x, gracetools.GraceContainer):
                for mark in apply_forward:
                    if hasattr(mark, '__call__'):
                        mark(x)
                if previous_leaf:
                    for mark in apply_backward:
                        if hasattr(mark, '__call__'):
                            mark(previous_leaf)
                else:
                    for mark in apply_backward:
                        if hasattr(mark, '__call__'):
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
                if hasattr(mark, '__call__'):
                    mark.format_slot = 'after'
                    mark(previous_leaf)
            for mark in apply_backward:
                if hasattr(mark, '__call__'):
                    mark(previous_leaf)
        else:
            for mark in apply_forward:
                if hasattr(mark, '__call__'):
                    mark.format_slot = 'opening'
                    mark(container)
            for mark in apply_backward:
                if hasattr(mark, '__call__'):
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
        container.is_parallel = True

        # check for voice separators     
        groups = []
        for value, group in itertools.groupby(music, is_separator):
            if not value:
                groups.append(list(group))

        # without voice separators
        if 1 == len(groups):
            assert all([isinstance(x, contexttools.Context) for x in groups[0]])
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
            'ly:pitch?':          lambda x: isinstance(x, pitchtools.NamedChromaticPitch),
            'markup?':            lambda x: isinstance(x, markuptools.MarkupCommand),
            'number-list?':       lambda x: isinstance(x, (list, tuple)) and \
                                            all([isinstance(y, (int, float)) for y in x]),
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
        annotations = marktools.get_annotations_attached_to_component(leaf)
        if annotations:
            spanners_annotations = [x for x in annotations if x.name == 'spanners']
            if 1 == len(spanners_annotations):
                return spanners_annotations[0].value
            elif 1 < len(spanners_annotations):
                raise Exception('Multiple span events lists attached to %s' % leaf)
        return []

    def _process_post_events(self, leaf, post_events):
        for post_event in post_events:
            if hasattr(post_event, '__call__'):
                post_event(leaf)
            else:
                annotation = [x for x in marktools.get_annotations_attached_to_component(leaf)
                    if x.name == 'spanners']
                if not annotation:
                    annotation = marktools.Annotation('spanners', [])(leaf)
                else:
                    annotation = annotation[0]
                annotation.value.append(post_event)

    def _push_variable_scope(self):
        self._scope_stack.append({})

    def _pop_variable_scope(self):
        if self._scope_stack:
            self._scope_stack.pop()

    def _push_extra_token(self, token):
        self._parser.lookaheadstack.append(token)

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

        token = lex.LexToken()
        token.type = token_type
        token.value = token_value
        token.lexpos = 0
        token.lineno = 0
        self._push_extra_token(token)

        reparse = lex.LexToken()
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
        self._last_chord = chordtools.Chord(['c', 'g', "c'"], (1, 4)) # LilyPond's default!
        self._pitch_names = self._language_pitch_names[self.default_language]
        self._repeated_chords = {}

    def _resolve_identifier(self, identifier):
        for scope in reversed(self._scope_stack):
            if identifier in scope:
                return scope[identifier]
        return None

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

    def _span_event_name_to_spanner_class(self, name):
        spanners = {
            'BeamEvent': beamtools.BeamSpanner,
            'CrescendoEvent': spannertools.HairpinSpanner,
            'DecrescendoEvent': spannertools.HairpinSpanner,
            'GlissandoEvent': spannertools.GlissandoSpanner,
            'NoteGroupingEvent': spannertools.HorizontalBracketSpanner,
            'PhrasingSlurEvent': spannertools.PhrasingSlurSpanner,
            'SlurEvent': spannertools.SlurSpanner,
            'TextSpanEvent': spannertools.TextSpanner,
            'TieEvent': tietools.TieSpanner,
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

    ### PUBLIC METHODS ###

    @classmethod
    def register_markup_function(cls, name, signature):
        r'''Register a custom markup function globally with LilyPondParser:

        ::

            >>> from abjad.tools.lilypondparsertools import LilyPondParser

        ::

            >>> name = 'my-custom-markup-function'
            >>> signature = ['markup?']
            >>> LilyPondParser.register_markup_function(name, signature)

        ::

            >>> parser = LilyPondParser()
            >>> string = r"\markup { \my-custom-markup-function { foo bar baz } }"
            >>> parser(string)
            Markup((MarkupCommand('my-custom-markup-function', ['foo', 'bar', 'baz']),))

        `signature` should be a sequence of zero or more type-predicate names, as
        understood by LilyPond.  Consult LilyPond's documentation for a complete
        list of all understood type-predicates.

        Return None
        '''

        from abjad.ly.py.markup_functions import markup_functions

        assert isinstance(name, str)
        assert all([not x.isspace() for x in name])
        assert isinstance(signature, (list, tuple))
        for predicate in signature:
            assert isinstance(predicate, str)
            assert all([not x.isspace() for x in predicate])
            assert predicate.endswith('?')

        markup_functions[name] = tuple(signature)
