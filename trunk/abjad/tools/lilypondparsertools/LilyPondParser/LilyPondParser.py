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
from abjad.tools.lilypondparsertools._LilyPondLexicalDefinition._LilyPondLexicalDefinition \
    import _LilyPondLexicalDefinition
from abjad.tools.lilypondparsertools._LilyPondSyntacticalDefinition._LilyPondSyntacticalDefinition \
    import _LilyPondSyntacticalDefinition
from abjad.tools.lilypondparsertools._LilyPondEvent._LilyPondEvent \
    import _LilyPondEvent as Event
from abjad.tools.lilypondparsertools._SyntaxNode._SyntaxNode \
    import _SyntaxNode as Node
from abjad.tools.lilypondparsertools._parse import _parse


# apply monkey patch
yacc.LRParser.parse_monkey_patch = _parse


class LilyPondParser(object):


    def __init__(self):
        self._lexdef = _LilyPondLexicalDefinition(self)
        self._syndef = _LilyPondSyntacticalDefinition(self)
        self._output_path = os.path.dirname(__file__)
        self._pickle_path = os.path.join(self._output_path, '_parsetab.pkl')

        logging.basicConfig(
            level = logging.DEBUG,
            filename = "parselog.txt",
            filemode = "w",
            format = "%(filename)10s:%(lineno)4d:%(message)s"
        )
        self._logger = logging.getLogger()

        self._lexer = lex.lex(object=self._lexdef)
        self._parser = yacc.yacc(
            debug=self._logger,
            module=self._syndef,
            outputdir=self._output_path,
            picklefile=self._pickle_path
        )

        self._guile = _GuileProxy(self)
        self._current_module = current_module
        self._language_pitch_names = language_pitch_names
        self._markup_functions = markup_functions
        self._markup_list_functions = markup_list_functions

        self._reset_parser_variables()


    ### OVERRIDES ###


    def __call__(self, input_string):
        self._reset_parser_variables()

        # use the monkeypatched function
        result = self._parser.parse_monkey_patch(
            input_string,
            lexer=self._lexer,
            debug=self._logger,
        )

        # clean up
        if self._leaf_attachments:
            self._construct_spanners(result)
        for annotation in self._annotations:
            annotation.detach( )

        return result


    ### PRIVATE METHODS ###


    def _backup_token(self, token_type, token_value):
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
            'GrandStaff': scoretools.GrandStaff,
            'PianoStaff': scoretools.PianoStaff,
            'Score': Score,
            'Staff': Staff,
            'Voice': Voice,
        }
        if context in known_contexts:
            context = known_contexts[context]()
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
        return Container(filter(lambda x: isinstance(x, _Component), music))


    def _construct_simultaneous_music(self, music):
        def is_separator(x):
            if isinstance(x, Event):
                if x.name == 'VoiceSeparator':
                    return True
            return False
        
        con = Container()
        con.is_parallel = True
     
        groups = [ ]
        for value, group in itertools.groupby(music, is_separator):
            if not value:
                groups.append(filter(lambda x: isinstance(x, _Component), list(group)))

        if 1 == len(groups):
            print 'NUMBER ONE'
            for x in groups[0]:
                if isinstance(x, _Leaf):
                    con.append(Voice[x])
                elif not isinstance(x, _Context):
                    con.append(Voice(x[:]))
                else:
                    con.append(x)

        else:
            for group in groups:
                if 1 < len(group):
                    con.append(Voice(group))
                elif not isinstance(group[0], _Context):
                    con.append(Voice(group[0][:]))
                else:
                    con.append(group[0])

        return con


    def _construct_spanners(self, result):
        return result


    def _get_leaf_attachments(self, leaf, kind = None):
        if leaf not in self._leaf_attachments:
            return [ ]
        events = self._leaf_attachments[leaf]
        spanners = filter(lambda x: x.name.endswith('SpanEvent', 'TieEvent'), events)
        if kind:
            spanners = filter(lambda x: x.name == kind)
        return spanners            


    def _process_post_events(self, leaf, post_events):
        for post_event in post_events:
            if hasattr(post_event, '__call__'):
                post_event(leaf)
            else:
                if leaf not in self._leaf_attachments:
                    self._leaf_attachments[leaf] = [ ]
                self._leaf_attachments[leaf].append(post_event)


    def _push_extra_token(self, token):
        self._parser.lookaheadstack.append(token)


    def _reparse_token(self, predicate, token_type, token_value):
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
        self._annotations = [ ]
        self._assignments = { }
        self._chord_pitch_orders = { }
        self._leaf_attachments = { }
        self._lexer.push_state('notes')
        self._parser_variables = {
            'default_duration': Node('multiplied_duration', [Duration(1, 4)]),
            'language': 'english',
            'last_chord': Chord("<c g c'>4"), # LilyPond's default!
        }
        self._repeated_chords = { }


    def _resolve_event_identifier(self, identifier):
        lookup = self._resolve_identifier(identifier)
        name = lookup['name']
        if name == 'ArticulationEvent':
            return marktools.Articulation(lookup['articulation-type'])
        elif name == 'AbsoluteDynamicEvent':
            return contexttools.DynamicMark(lookup['text'])
        event = Event(name)
        if 'span-direction' in lookup:
            if lookup['span-direction'] == -1:
                event.span_direction = 'start'
            else:
                event.span_direction = 'stop'
        return event


    def _resolve_identifier(self, identifier):
        name = identifier
        if name.startswith('\\'):
            name = name[1:]
        if name in self._assignments:
            return self._assignments[name]
        else:
            return self._current_module[name]
        raise Exception('Unknown identifer: %s' % identifier)
        if name in self._assignments:
            return self._assignments[name]
        else:
            return self._current_module[name]
        raise Exception('Unknown identifer: %s' % identifier)


    def _test_scheme_predicate(self, predicate, value):
        predicates = {
            'boolean?':           lambda x: isinstance(x, bool),
            'cheap-list?':        lambda x: isinstance(x, (list, tuple)),
            #'cheap-markup?':      lambda x: True,,
            'fraction?':          lambda x: isinstance(x, Fraction),
            #'hash-table?':        lambda x: True,
            'integer?':           lambda x: isinstance(x, int),
            #'list-or-symbol?':    lambda x: True,
            'list?':              lambda x: isinstance(x, (list, tuple)),
            #'ly:dir?':            lambda x: True,
            'ly:duration?':       lambda x: True,
            #'ly:moment?':         lambda x: True,
            'ly:music?':          lambda x: True,
            'ly:pitch?':          lambda x: True,
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
            'string?':            lambda x: isinstance(x, str),
            #'symbol-or-boolean?': lambda x: True,
            #'symbol?':            lambda x: True,
            'void?':              lambda x: isinstance(x, type(None)),
        }
        if predicate in predicates:
            return predicates[predicate](value)
        return True
