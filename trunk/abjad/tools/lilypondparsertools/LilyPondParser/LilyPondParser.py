import itertools
import logging
import os

from ply import lex, yacc
from ply.lex import LexToken

from abjad import *
from abjad.tools.componenttools._Component import _Component
from abjad.tools.contexttools._Context import _Context
from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools.lilypondparsertools._GuileProxy._GuileProxy import _GuileProxy
from abjad.tools.lilypondparsertools._LilyPondDuration._LilyPondDuration import _LilyPondDuration
from abjad.tools.lilypondparsertools._LilyPondEvent._LilyPondEvent import _LilyPondEvent
from abjad.tools.lilypondparsertools._LilyPondFraction._LilyPondFraction import _LilyPondFraction
from abjad.tools.lilypondparsertools._LilyPondLexicalDefinition._LilyPondLexicalDefinition import _LilyPondLexicalDefinition
from abjad.tools.lilypondparsertools._LilyPondSyntacticalDefinition._LilyPondSyntacticalDefinition import _LilyPondSyntacticalDefinition
from abjad.tools.lilypondparsertools._NullHandler._NullHandler import _NullHandler
from abjad.tools.lilypondparsertools._SyntaxNode._SyntaxNode import _SyntaxNode as Node
from abjad.tools.lilypondparsertools._parse import _parse
from abjad.tools.lilypondparsertools._parse_debug import _parse_debug
from abjad.tools.sequencetools import iterate_sequence_pairwise_wrapped


# apply monkey patch
yacc.LRParser._monkey_patch_parse = _parse
yacc.LRParser._monkey_patch_parse_debug = _parse_debug


class LilyPondParser(object):
    r'''Parses a subset of LilyPond input syntax:

    ::

        abjad> from abjad.tools.lilypondparsertools import LilyPondParser
        abjad> parser = LilyPondParser( )
        abjad> input = r"\new Staff { c'4 ( d'8 e' fs'2) \fermata }"
        abjad> result = parser(input)
        abjad> f(result)
        \new Staff {
            c'4 (
            d'8
            e'8
            fs'2 -\fermata )
        }

    LilyPondParser defaults to English note names, but any of the other
    languages supported by LilyPond may be used:

    ::

        abjad> parser = LilyPondParser('nederlands')
        abjad> input = '{ c des e fis }'
        abjad> result = parser(input)
        abjad> f(result)
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
    - Most context types via ``\new`` and ``\context``, as well as context ids (i.e. ``\new Staff = "foo" { }``)
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
    - Property operations, such as ``\override``, ``\revert``, ``\set``, ``\unset``, and ``\once``
    - Music functions which generate or extensively mutate musical structures
    - Embedded Scheme statements (anything beginning with ``#``)

    Returns LilyPondParser instance.
    '''

    def __init__(self, default_language='english', debug=False):

        from abjad.ly.py.current_module import current_module
        from abjad.ly.py.language_pitch_names import language_pitch_names
        from abjad.ly.py.markup_functions import markup_functions
        from abjad.ly.py.markup_functions import markup_list_functions

        # LilyPond emulation data
        self._guile = _GuileProxy(self)
        self._current_module = current_module
        self._language_pitch_names = language_pitch_names
        self._markup_functions = markup_functions
        self._markup_list_functions = markup_list_functions

        self.default_language = default_language
        self._debug = bool(debug)

        # parser and lexer rules
        self._lexdef = _LilyPondLexicalDefinition(self)
        self._syndef = _LilyPondSyntacticalDefinition(self)

        # output paths
        self._output_path = os.path.dirname(__file__)
        self._pickle_path = os.path.join(self._output_path, '_parsetab.pkl')
        self._logger_path = os.path.join(self._output_path, 'parselog.txt')

        # setup a logging
        if self._debug:
            logging.basicConfig(
                level = logging.DEBUG,
                filename = self._logger_path,
                filemode = 'w',
                format = '%(filename)10s:%(lineno)8d:%(message)s'
            )
            self._logger = logging.getLogger()
        else:
            self._logger = logging.getLogger()
            self._logger.addHandler(_NullHandler()) # use custom NullHandler for 2.6 compatibility

        # setup PLY objects
        self._lexer = lex.lex(
            debug=True,
            debuglog=self._logger,
            object=self._lexdef,
        )
        self._parser = yacc.yacc(
            debug=True,
            debuglog=self._logger,
            module=self._syndef,
            outputdir=self._output_path,
            picklefile=self._pickle_path,
        )

        self._reset_parser_variables()


    ### OVERRIDES ###


    def __call__(self, input_string):
        if os.path.exists(self._logger_path):
            os.remove(self._logger_path)

        self._reset_parser_variables()

        if self._debug:
            result = self._parser._monkey_patch_parse_debug(
                input_string, 
                lexer=self._lexer,
                debug=self._logger)
        else:
            result = self._parser._monkey_patch_parse(
                input_string,
                lexer=self._lexer)

        if isinstance(result, Container):
            self._apply_spanners(result)
        else:
            for x in result:
                if isinstance(x, Container):
                    self._apply_spanners(x)
                elif isinstance(x, lilypondfiletools.ScoreBlock):
                    for y in x:
                        self._apply_spanners(y)

        return result


    ### PUBLIC ATTRIBUTES ###


    @property
    def available_languages(self):
        '''Tuple of pitch-name languages supported by LilyPondParser:

        ::

            abjad> from abjad.tools.lilypondparsertools import LilyPondParser
            abjad> parser = LilyPondParser( )
            abjad> parser.available_languages
            ('catalan', 'deutsch', 'english', 'espanol', 'italiano', 'nederlands', 'norsk', 'portugues', 'suomi', 'svenska', 'vlaams')

        Return tuple.
        '''
        return tuple(sorted(self._language_pitch_names.keys( )))

    
    @apply
    def default_language():
        def fget(self):
            '''Read/write attribute to set parser's default pitch-name language:

            ::

                abjad> from abjad.tools.lilypondparsertools import LilyPondParser
                abjad> parser = LilyPondParser( )
                abjad> parser.default_language
                'english'
                abjad> parser('{ c df e fs }')
                {c4, df4, e4, fs4}
                abjad> parser.default_language = 'nederlands'
                abjad> parser.default_language
                'nederlands'
                abjad> parser('{ c des e fis }')
                {c4, df4, e4, fs4}

            '''
            return self._default_language
        def fset(self, arg):
            assert arg in self.available_languages
            self._default_language = arg
        return property(**locals( ))


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
        for leaf, next_leaf in iterate_sequence_pairwise_wrapped(leaves):

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
                        all_spanners[klass] = [ ]

                # or apply undirected event immediately (i.e. ties, glisses)
                elif next_leaf is not first_leaf: # so long as we are not wrapping yet
                    previous_spanners = filter(lambda x: isinstance(x, klass), leaf.spanners)
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
                all_spanners[spannertools.HairpinSpanner].pop( )

            # loop through directed events, handling each as necessary
            for klass, events in directed_events.iteritems( ):

                starting_events = filter(lambda x: x.span_direction == 'start', events)
                stopping_events = filter(lambda x: x.span_direction == 'stop', events)

                if klass is spannertools.BeamSpanner:
                    # A beam may begin and end on the same leaf
                    # but only one beam spanner may cover any given leaf,
                    # and starting events are processed before ending ones
                    for event in starting_events:
                        if all_spanners[klass]:
                            raise Exception('Already have beam.')
                        if hasattr(event, 'direction'):
                            all_spanners[klass].append(klass(direction=event.direction))
                        else:
                            all_spanners[klass].append(klass( ))
                    for _ in stopping_events:
                        if all_spanners[klass]:
                            all_spanners[klass][0].append(leaf)
                            all_spanners[klass].pop( )

                elif klass is spannertools.HairpinSpanner:
                    # Dynamic events can be ended many times,
                    # but only one may start on a given leaf,
                    # and the event must start and end on separate leaves.
                    # If a hairpin already exists and another starts,
                    # the pre-existant spanner is ended.
                    for _ in stopping_events:
                        if all_spanners[klass]:
                            all_spanners[klass][0].append(leaf)
                            all_spanners[klass].pop( )
                    if 1 == len(starting_events):
                        if all_spanners[klass]:
                            all_spanners[klass][0].append(leaf)
                            all_spanners[klass].pop( )
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
                            all_spanners[klass].pop( )
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
                        all_spanners[klass].append(klass( ))
                    if stopping_events:
                        if not has_starting_events:
                            for _ in stopping_events:
                                if all_spanners[klass]:
                                    all_spanners[klass][-1].append(leaf)
                                    all_spanners[klass].pop( )
                                else:
                                    raise Exception('Do not have that many brackets.')
                        else:
                            raise Exception('Conflicting note group events.')

            # append leaf to all tracked spanners,
            for klass, instances in all_spanners.iteritems( ):
                for instance in instances:
                    instance.append(leaf)

        # check for unterminated spanners
        for klass, instances in all_spanners.iteritems( ):
            if instances:
                raise Exception('Unterminated %s.' % klass.__name__)


    def _backup_token(self, token_type, token_value):
        if self._debug:
            self._logger.info('Extra  : Backing up')

        # push the current lookahead back onto the lookaheadstack
        self._push_extra_token(self._parser.lookahead)

        # create the backup token, set as new lookahead
        backup = LexToken( )
        backup.type = 'BACKUP'
        backup.value = '(backed-up?)'
        backup.lexpos = 0
        backup.lineno = 0
        self._parser.lookahead = backup

        if token_type:
            token = LexToken( )
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
            'Score': Score,
            'Staff': Staff,
            'StaffGroup': scoretools.StaffGroup,
            'Voice': Voice,
        }
        if context in known_contexts:
            context = known_contexts[context]([ ])
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

        marks = music.marks
        for mark in marks:
            mark(context)

        return context


    def _construct_sequential_music(self, music):
        # mark sorting could be rewritten into a single list, using tuplets,
        # with t[0] being 'forward' or 'backward' and t[1] being the mark, as
        # this better preserves attachment order.  Not clear if we need it.

        container = Container()
        previous_leaf = None
        apply_forward = [ ]
        apply_backward = [ ]

        # sort events into forward or backwards attaching, and attach them to
        # the proper leaf
        for x in music:
            if isinstance(x, _Component):
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
                apply_forward = [ ]
                apply_backward = [ ]
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
        def is_separator(x):
            if isinstance(x, _LilyPondEvent):
                if x.name == 'VoiceSeparator':
                    return True
            return False
        
        container = Container()
        container.is_parallel = True

        # check for voice separators     
        groups = [ ]
        for value, group in itertools.groupby(music, is_separator):
            if not value:
                groups.append(list(group))

        # without voice separators
        if 1 == len(groups):
            assert all([isinstance(x, _Context) for x in groups[0]])
            container.extend(groups[0])
        # with voice separators
        else:
            for group in groups:
                container.append(Voice(self._construct_sequential_music(group)[:]))

        return container


    def _get_span_events(self, leaf):
        annotations = marktools.get_annotations_attached_to_component(leaf)
        if annotations:
            spanners_annotations = filter(lambda x: x.name == 'spanners', annotations)
            if 1 == len(spanners_annotations):
                return spanners_annotations[0].value
            elif 1 < len(spanners_annotations):
                raise Exception('Multiple span events lists attached to %s' % leaf)
        return [ ]


    def _process_post_events(self, leaf, post_events):
        for post_event in post_events:
            if hasattr(post_event, '__call__'):
                post_event(leaf)
            else:
                annotation = filter(lambda x: x.name == 'spanners',
                    marktools.get_annotations_attached_to_component(leaf))
                if not annotation:
                    annotation = marktools.Annotation('spanners', [ ])(leaf)
                else:
                    annotation = annotation[0]
                annotation.value.append(post_event)


    def _push_extra_token(self, token):
        self._parser.lookaheadstack.append(token)


    def _reparse_token(self, predicate, token_type, token_value):
        if self._debug:
            self._logger.info('Extra  : Reparsing')

        # push the current lookahead back onto the lookaheadstack
        self._push_extra_token(self._parser.lookahead)

        token = LexToken( )
        token.type = token_type
        token.value = token_value
        token.lexpos = 0
        token.lineno = 0
        self._push_extra_token(token)

        reparse = LexToken( )
        reparse.type = 'REPARSE'
        reparse.value = predicate
        reparse.lineno = 0
        reparse.lexpos = 0
        self._parser.lookahead = reparse


    def _reset_parser_variables(self):
        try:
            self._parser.restart( )
        except:
            pass
        self._assignments = { }
        self._chord_pitch_orders = { }
        self._lexer.push_state('notes')
        self._default_duration = _LilyPondDuration(Duration(1, 4), None)
        self._last_chord = Chord("<c g c'>4") # LilyPond's default!
        self._pitch_names = self._language_pitch_names[self.default_language]
        self._repeated_chords = { }


    def _resolve_event_identifier(self, identifier):
        lookup = self._current_module[identifier] # without any leading slash
        name = lookup['name']
        if name == 'ArticulationEvent':
            return marktools.Articulation(lookup['articulation-type'])
        elif name == 'AbsoluteDynamicEvent':
            return contexttools.DynamicMark(lookup['text'])
        event = _LilyPondEvent(name)
        if 'span-direction' in lookup:
            if lookup['span-direction'] == -1:
                event.span_direction = 'start'
            else:
                event.span_direction = 'stop'
        return event


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
            'TieEvent': tietools.TieSpanner,
            'TrillSpanEvent': spannertools.TrillSpanner,
        }
        if name in spanners:
            return spanners[name]
        raise Exception('Abjad cannot associate a spanner class with %s' % name)


    def _test_scheme_predicate(self, predicate, value):
        predicates = {
            'boolean?':           lambda x: isinstance(x, bool),
            'cheap-list?':        lambda x: isinstance(x, (list, tuple)),
            #'cheap-markup?':      lambda x: True,,
            'fraction?':          lambda x: isinstance(x, _LilyPondFraction),
            #'hash-table?':        lambda x: True,
            'integer?':           lambda x: isinstance(x, int),
            #'list-or-symbol?':    lambda x: True,
            'list?':              lambda x: isinstance(x, (list, tuple)),
            #'ly:dir?':            lambda x: True,
            'ly:duration?':       lambda x: isinstance(x, _LilyPondDuration),
            #'ly:moment?':         lambda x: True,
            'ly:music?':          lambda x: isinstance(x, (_Component, marktools.Mark)),
            'ly:pitch?':          lambda x: isinstance(x, pitchtools.NamedChromaticPitch),
            'number-list?':       lambda x: isinstance(x, (list, tuple)) and \
                                            all([isinstance(y, (int, float)) for y in x]),
            #'number-or-string?':  lambda x: True,
            #'number-pair?':       lambda x: True,
            #'number?':            lambda x: True,
            #'optional?':          lambda x: True,
            #'pair?':              lambda x: True,
            #'procedure?':         lambda x: True,
            'real?':              lambda x: isinstance(x, (int, float)),
            'scheme?':            lambda x: True,
            #'string-or-pair?':    lambda x: True,
            'string?':            lambda x: isinstance(x, (str, unicode)),
            #'symbol-or-boolean?': lambda x: True,
            #'symbol?':            lambda x: True,
            'void?':              lambda x: isinstance(x, type(None)),
        }
        if predicate in predicates:
            return predicates[predicate](value)
        return True
