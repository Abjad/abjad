# -*- encoding: utf-8 -*-
import abc
import copy
from abjad.tools import systemtools
from abjad.tools.scoretools.Container import Container


class Context(Container):
    '''A horizontal layer of music.

    ::

        >>> context = scoretools.Context(
        ...     name='MeterVoice', 
        ...     context_name='TimeSignatureContext',
        ...     )

    ::

        >>> context
        TimeSignatureContext-"MeterVoice"{}

    ..  doctest::

        >>> print format(context)
        \context TimeSignatureContext = "MeterVoice" {
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context_name',
        '_engraver_consists',
        '_engraver_removals',
        '_is_nonsemantic',
        '_name',
        )

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

    def __repr__(self):
        r'''Interpreter representation of context.

        ::

            >>> context
            TimeSignatureContext-"MeterVoice"{}

        Returns string.
        '''
        if 0 < len(self):
            summary = str(len(self))
        else:
            summary = ''
        if self.is_simultaneous:
            open_bracket_string, close_bracket_string = '<<', '>>'
        else:
            open_bracket_string, close_bracket_string = '{', '}'
        name = self.name
        if name is not None:
            name = '-"{}"'.format(name)
        else:
            name = ''
        result = '{}{}{}{}{}'
        result = result.format(
            self.context_name,
            name,
            open_bracket_string,
            summary,
            close_bracket_string,
            )
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        return self._format_component(pieces=True)

    @property
    def _lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

    ### PRIVATE METHODS ###

    def _copy_with_indicators_but_without_children_or_spanners(self):
        new = Container._copy_with_indicators_but_without_children_or_spanners(self)
        new._engraver_consists = copy.copy(self.engraver_consists)
        new._engraver_removals = copy.copy(self.engraver_removals)
        new.name = copy.copy(self.name)
        new.is_nonsemantic = copy.copy(self.is_nonsemantic)
        return new
        return new

    def _format_closing_slot(context, bundle):
        result = []
        result.append(('indicators', bundle.closing.indicators))
        result.append(('commands', bundle.closing.commands))
        result.append(('comments', bundle.closing.comments))
        return context._format_slot_contributions_with_indent(result)

    def _format_engraver_consists(self):
        result = []
        for engraver in self.engraver_consists:
            string = r'\consists {}'.format(engraver)
            result.append(string)
        return result

    def _format_engraver_removals(self):
        result = []
        for engraver in self.engraver_removals:
            string = r'\remove {}'.format(engraver)
            result.append(string)
        return result

    def _format_invocation(self):
        if self.name is not None:
            string = r'\context {} = "{}"'
            string = string.format(self.context_name, self.name)
        else:
            string = r'\new {}'
            string = string.format(self.context_name)
        return string

    def _format_open_brackets_slot(context, bundle):
        result = []
        if context.is_simultaneous:
            brackets_open = ['<<']
        else:
            brackets_open = ['{']
        engraver_removals = context._format_engraver_removals()
        engraver_consists = context._format_engraver_consists()
        overrides = bundle.grob_overrides
        settings = bundle.context_settings
        if engraver_removals or engraver_consists or overrides or settings:
            contributions = [context._format_invocation() + r' \with {']
            contributions = tuple(contributions)
            identifier_pair = ('context_brackets', 'open')
            result.append((identifier_pair, contributions))
            contributions = ['\t' + x for x in engraver_removals]
            contributions = tuple(contributions)
            identifier_pair = ('engraver removals', 'engraver_removals')
            result.append((identifier_pair, contributions))
            contributions = ['\t' + x for x in engraver_consists]
            contributions = tuple(contributions)
            identifier_pair = ('engraver consists', 'engraver_consists')
            result.append((identifier_pair, contributions))
            contributions = ['\t' + x for x in overrides]
            contributions = tuple(contributions)
            identifier_pair = ('overrides', 'overrides')
            result.append((identifier_pair, contributions))
            contributions = ['\t' + x for x in settings]
            contributions = tuple(contributions)
            identifier_pair = ('settings', 'settings')
            result.append((identifier_pair, contributions))
            contributions = ['}} {}'.format(brackets_open[0])]
            contributions = tuple(contributions)
            identifier_pair = ('context_brackets', 'open')
            result.append((identifier_pair, contributions))
        else:
            contribution = context._format_invocation() 
            contribution += ' {}'.format(brackets_open[0])
            contributions = [contribution]
            contributions = tuple(contributions)
            identifier_pair = ('context_brackets', 'open')
            result.append((identifier_pair, contributions))
        return tuple(result)

    def _format_opening_slot(context, bundle):
        result = []
        result.append(('comments', bundle.opening.comments))
        result.append(('indicators', bundle.opening.indicators))
        result.append(('commands', bundle.opening.commands))
        return context._format_slot_contributions_with_indent(result)

    ### PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        r'''Gets and sets context name of context.

        Returns string.
        '''
        return self._context_name

    @context_name.setter
    def context_name(self, arg):
        assert isinstance(arg, str)
        self._context_name = arg

    @property
    def engraver_consists(self):
        r'''Unordered set of LilyPond engravers to include 
        in context definition.

        Manage with add, update, other standard set commands:

        ::

            >>> staff = Staff([])
            >>> staff.engraver_consists.append('Horizontal_bracket_engraver')
            >>> print format(staff)
            \new Staff \with {
                \consists Horizontal_bracket_engraver
            } {
            }

        '''
        return self._engraver_consists

    @property
    def engraver_removals(self):
        r'''Unordered set of LilyPond engravers to remove from context.

        Manage with add, update, other standard set commands:

        ::

            >>> staff = Staff([])
            >>> staff.engraver_removals.append('Time_signature_engraver')
            >>> print format(staff)
            \new Staff \with {
                \remove Time_signature_engraver
            } {
            }

        '''
        return self._engraver_removals

    @property
    def is_nonsemantic(self):
        r'''Gets and sets nonsemantic voice flag.

        ::

            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     [(1, 8), (5, 16), (5, 16)])
            >>> voice = Voice(measures)
            >>> voice.name = 'HiddenTimeSignatureVoice'

        ::

            >>> voice.is_nonsemantic = True

        ..  doctest::

            >>> print format(voice)
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

        Gets nonsemantic voice voice:

        ::

            >>> voice = Voice([])

        ::

            >>> voice.is_nonsemantic
            False

        Returns boolean.

        The intent of this read / write attribute is to allow composers
        to tag invisible voices used to house time signatures indications,
        bar number directives or other pieces of score-global non-musical
        information. Such nonsemantic voices can then be omitted from
        voice interation and other functions.
        '''
        return self._is_nonsemantic

    @is_nonsemantic.setter
    def is_nonsemantic(self, arg):
        if not isinstance(arg, bool):
            raise TypeError
        self._is_nonsemantic = arg

    @property
    def is_semantic(self):
        r'''True when context is semantic. Otherwise false.

        Returns boolean.
        '''
        return not self.is_nonsemantic

    @property
    def name(self):
        r'''Gets and sets name of context.

        Returns string or none.
        '''
        return self._name

    @name.setter
    def name(self, arg):
        assert isinstance(arg, (str, type(None)))
        old_name = self._name
        for parent in self._get_parentage(include_self=False):
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
