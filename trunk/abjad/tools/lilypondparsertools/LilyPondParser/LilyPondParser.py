import itertools
import logging
import os

from ply import lex, yacc
from ply.lex import LexToken

from abjad import *
from abjad.tools.componenttools._Component import _Component
from abjad.tools.contexttools._Context import _Context
from abjad.tools.leaftools._Leaf import _Leaf
from abjad.ly.py.current_module import current_module
from abjad.ly.py.language_pitch_names import language_pitch_names
from abjad.ly.py.markup_functions import markup_functions
from abjad.ly.py.markup_functions import markup_list_functions
from abjad.tools.lilypondparsertools._GuileProxy._GuileProxy import _GuileProxy
from abjad.tools.lilypondparsertools._LilyPondDuration._LilyPondDuration import _LilyPondDuration
from abjad.tools.lilypondparsertools._LilyPondEvent._LilyPondEvent import _LilyPondEvent
from abjad.tools.lilypondparsertools._LilyPondLexicalDefinition._LilyPondLexicalDefinition import _LilyPondLexicalDefinition
from abjad.tools.lilypondparsertools._LilyPondSyntacticalDefinition._LilyPondSyntacticalDefinition import _LilyPondSyntacticalDefinition
from abjad.tools.lilypondparsertools._SyntaxNode._SyntaxNode import _SyntaxNode as Node
from abjad.tools.lilypondparsertools._parse import _parse
from abjad.tools.lilypondparsertools._parse_debug import _parse_debug


# apply monkey patch
yacc.LRParser._monkey_patch_parse = _parse
yacc.LRParser._monkey_patch_parse_debug = _parse_debug


class LilyPondParser(object):


    def __init__(self, default_language='english', debug=False):

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
            self._logger.addHandler(logging.NullHandler())

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

        self._apply_spanners(result)

        return result


    ### PUBLIC ATTRIBUTES ###

    
    @apply
    def default_language():
        def fset(self, arg):
            assert arg in self._language_pitch_names.keys( )
            self._default_language = arg
        def fget(self):
            return self._default_language
        return property(**locals( ))


    ### PRIVATE METHODS ###


    def _apply_spanners(self, music):

        # get local reference to methods
        _get_span_events = self._get_span_events
        _spanner_class_can_nest = self._spanner_class_can_nest
        _span_event_name_to_spanner_class = self._span_event_name_to_spanner_class

        # dictionary of spanner classes and instances
        spanners = { }

        # traverse all leaves
        for leaf in music.leaves:

            span_events = _get_span_events(leaf)
            starting_events = filter(lambda x: x.span_direction is 'start', span_events)
            stopping_events = filter(lambda x: x.span_direction is 'stop', span_events)

            # open spanners
            for span_event in starting_events:
                klass = _span_event_name_to_spanner_class(span_event.name)
                if klass not in spanners:
                    spanners[klass] = [ ]
                can_nest = _spanner_class_can_nest(klass)
                if can_nest:
                    spanners[klass].append(klass( ))
                elif 0 == len(spanners[klass]):
                    spanners[klass].append(klass( ))
                else:
                    raise Exception('%s is already covered by a %s.' % (leaf, klass.__name__))
                            
            # append leaf to all open spanners
            for instances in spanners.itervalues( ):
                for instance in instances:
                    instance.append(leaf)                    

            # close spanners 
            for span_event in stopping_events:
                klass = _span_event_name_to_spanner_class(span_event.name)
                if klass not in spanners or not len(spanners[klass]):
                    raise Exception('Trying to end unbegun %s at %s' % (klass.__name__, leaf))
                spanners[klass].pop( )

        # check for unterminated spanners
        for klass, instances in spanners.iteritems( ):
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
            pass # TODO
        context.is_parallel = music.is_parallel

        while len(music):
            component = music.pop(0)
            context.append(component)

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
            spanners_annotations = filter(lambda x: x.name is 'spanners', annotations)
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
                annotation = filter(lambda x: x.name is 'spanners',
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
        if name is 'BeamEvent':
            return spannertools.BeamSpanner
        elif name is 'GlissandoEvent':
            return spannertools.GlissandoSpanner
        elif name is 'NoteGroupingEvent':
            return spannertools.HorizontalBracketSpanner
        elif name is 'SlurEvent':
            return spannertools.SlurSpanner
        elif name is 'TieEvent':
            return spannertools.TieSpanner
        elif name is 'TrillSpanEvent':
            return spannertools.TrillSpanner
        raise Exception('Abjad cannot associate a spanner class with %s' % name)


    def _spanner_class_can_nest(self, spanner_class):
        if spanner_class is spannertools.HorizontalBracketSpanner:
            return True
        return False


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
