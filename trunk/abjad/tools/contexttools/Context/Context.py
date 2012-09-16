import abc
from abjad.tools import componenttools
from abjad.tools import formattools
from abjad.tools.containertools.Container import Container
import copy


class Context(Container):
    '''.. versionadded:: 1.0

    Abjad model of a horizontal layer of music.

        >>> context = contexttools.Context(
        ... name='MeterVoice', context_name='TimeSignatureContext')

    ::

        >>> context
        TimeSignatureContext-"MeterVoice"{}

    ::

        >>> f(context)
        \context TimeSignatureContext = "MeterVoice" {
        }

    Return context object.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta 
    __slots__ = ('_context_name', '_engraver_consists', '_engraver_removals',
        '_is_nonsemantic', '_name', )

    ### INITIALIZER ###

    def __init__(self, music=None, context_name='Context', name=None):
        Container.__init__(self, music=music)
        self.context_name = context_name
        self._engraver_consists = []
        self._engraver_removals = []
        self._name = None
        self.name = name
        self.is_nonsemantic = False

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        new = Container.__copy__(self, *args)
        new._engraver_consists = copy.copy(self.engraver_consists)
        new._engraver_removals = copy.copy(self.engraver_removals)
        new.name = copy.copy(self.name)
        new.is_nonsemantic = copy.copy(self.is_nonsemantic)
        return new

    def __repr__(self):
        '''.. versionchanged:: 2.0

        Named contexts now print name at the interpreter.
        '''
        if 0 < len(self):
            summary = str(len(self))
        else:
            summary = ''
        if self.is_parallel:
            open_bracket_string, close_bracket_string = '<<', '>>'
        else:
            open_bracket_string, close_bracket_string = '{', '}'
        name = self.name
        if name is not None:
            name = '-"%s"' % name
        else:
            name = ''
        return '%s%s%s%s%s' % (self.context_name, name, open_bracket_string, summary, close_bracket_string)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        return self._format_component(pieces=True)

    ### PRIVATE METHODS ###

    def _format_engraver_consists(self):
        result = []
        for engraver in sorted(self.engraver_consists):
            result.append(r'\consists %s' % engraver)
        return result

    def _format_engraver_removals(self):
        result = []
        for engraver in sorted(self.engraver_removals):
            result.append(r'\remove %s' % engraver)
        return result

    def _format_invocation(self):
        if self.name is not None:
            return r'\context %s = "%s"' % (self.context_name, self.name)
        else:
            return r'\new %s' % self.context_name

    def _format_open_brackets_slot(context, format_contributions):
        result = []
        if context.is_parallel:
            brackets_open = ['<<']
        else:
            brackets_open = ['{']
        engraver_removals = context._format_engraver_removals()
        engraver_consists = context._format_engraver_consists()
        overrides = format_contributions.get('grob overrides', [])
        #overrides = formattools.get_grob_override_format_contributions(context)
        #overrides = overrides[1]
        settings = format_contributions.get('context settings', [])
        #settings = formattools.get_context_setting_format_contributions(context)
        #settings = settings[1]
        if engraver_removals or engraver_consists or overrides or settings:
            contributions = [context._format_invocation() + r' \with {']
            result.append([('context_brackets', 'open'), contributions])
            contributions = ['\t' + x for x in engraver_removals]
            result.append([('engraver removals', 'engraver_removals'), contributions])
            contributions = ['\t' + x for x in engraver_consists]
            result.append([('engraver consists', 'engraver_consists'), contributions])
            contributions = ['\t' + x for x in overrides]
            result.append([('overrides', 'overrides'), contributions])
            contributions = ['\t' + x for x in settings]
            result.append([('settings', 'settings'), contributions])
            contributions = ['} %s' % brackets_open[0]]
            result.append([('context_brackets', 'open'), contributions])
        else:
            contributions = [context._format_invocation() + ' %s' % brackets_open[0]]
            result.append([('context_brackets', 'open'), contributions])
        return tuple(result)

    def _format_opening_slot(context, format_contributions):
        result = []
        result.append(['comments', format_contributions.get('opening', {}).get('comments', [])])
        result.append(['context marks', format_contributions.get('opening', {}).get('context marks', [])])
        result.append(['lilypond command marks', format_contributions.get('opening', {}).get('lilypond command marks', [])])
        #result.append(formattools.get_comment_format_contributions_for_slot(context, 'opening'))
        #result.append(formattools.get_context_mark_format_contributions_for_slot(context, 'opening'))
        #result.append(formattools.get_lilypond_command_mark_format_contributions_for_slot(context, 'opening'))
        return context._format_slot_contributions_with_indent(result)

    def _format_closing_slot(context, format_contributions):
        result = []
        result.append(['context marks', format_contributions.get('closing', {}).get('context marks', [])])
        result.append(['lilypond command marks', format_contributions.get('closing', {}).get('lilypond command marks', [])])
        result.append(['comments', format_contributions.get('closing', {}).get('comments', [])])
        #result.append(formattools.get_context_mark_format_contributions_for_slot(context, 'closing'))
        #result.append(formattools.get_lilypond_command_mark_format_contributions_for_slot(context, 'closing'))
        #result.append(formattools.get_comment_format_contributions_for_slot(context, 'closing'))
        return context._format_slot_contributions_with_indent(result)

    def _initialize_keyword_values(self, **kwargs):
        if 'context_name' in kwargs:
            self.context_name = kwargs['context_name']
            del(kwargs['context_name'])
        if 'name' in kwargs:
            self.name = kwargs['name']
            del(kwargs['name'])
        Container._initialize_keyword_values(self, **kwargs)

    ### PUBLIC PROPERTIES ###

    @apply
    def context_name():
        def fget(self):
            '''Read / write name of context as a string.'''
            return self._context_name
        def fset(self, arg):
            assert isinstance(arg, str)
            self._context_name = arg
        return property(**locals())

    @property
    def engraver_consists(self):
        r'''.. versionadded:: 2.0

        Unordered set of LilyPond engravers to include in context definition.

        Manage with add, update, other standard set commands. ::

            >>> staff = Staff([])
            >>> staff.engraver_consists.append('Horizontal_bracket_engraver')
            >>> f(staff)
            \new Staff \with {
                \consists Horizontal_bracket_engraver
            } {
            }

        '''
        return self._engraver_consists

    @property
    def engraver_removals(self):
        r'''.. versionadded:: 2.0

        Unordered set of LilyPond engravers to remove from context.

        Manage with add, update, other standard set commands. ::

            >>> staff = Staff([])
            >>> staff.engraver_removals.append('Time_signature_engraver')
            >>> f(staff)
            \new Staff \with {
                \remove Time_signature_engraver
            } {
            }

        '''
        return self._engraver_removals

    @property
    def lilypond_format(self):
        self._update_marks_of_entire_score_tree_if_necessary()
        return self._format_component()

    @apply
    def is_nonsemantic():
        def fget(self):
            r'''Set indicator of nonsemantic voice::

                >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(
                ...     [(1, 8), (5, 16), (5, 16)])
                >>> voice = Voice(measures)
                >>> voice.name = 'HiddenTimeSignatureVoice'

            ::

                >>> voice.is_nonsemantic = True

            ::

                >>> f(voice)
                \context Voice = "HiddenTimeSignatureVoice" {
                    {
                        \time 1/8
                        s1 * 1/8
                    }
                    {
                        \time 5/16
                        s1 * 5/16
                    }
                    {
                        s1 * 5/16
                    }
                }

            ::

                >>> voice.is_nonsemantic
                True

            Get indicator of nonsemantic voice::

                >>> voice = Voice([])

            ::

                >>> voice.is_nonsemantic
                False

            Return boolean.

            The intent of this read / write attribute is to allow composers to tag invisible
            voices used to house time signatures indications, bar number directives or other
            pieces of score-global non-musical information. Such nonsemantic voices can then
            be omitted from voice interation and other functions.
            '''
            return self._is_nonsemantic
        def fset(self, arg):
            if not isinstance(arg, bool):
                raise TypeError
            self._is_nonsemantic = arg
        return property(**locals())

    @property
    def is_semantic(self):
        return not self.is_nonsemantic

    @apply
    def name():
        def fget(self):
            '''Read-write name of context. Must be string or none.
            '''
            return self._name
        def fset(self, arg):
            assert isinstance(arg, (str, type(None)))
            parentage = componenttools.get_proper_parentage_of_component(self)
            old_name = self._name
            for parent in parentage:
                named_children = parent._named_children
                if old_name is not None:
                    named_children[old_name].remove(self)
                    if not named_children[old_name]:
                        del named_children[old_name]
                if arg is not None:
                    if arg not in named_children:
                        named_children[arg] = [self]
                    else:
                        named_children[arg].append(self)
            self._name = arg
        return property(**locals())
