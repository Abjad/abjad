# -*- coding: utf-8 -*-
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
        Context()

    ..  doctest::

        >>> print(format(context))
        \context TimeSignatureContext = "MeterVoice" {
        }


    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Contexts'

    __slots__ = (
        '_context_name',
        '_consists_commands',
        '_remove_commands',
        '_is_nonsemantic',
        )

    _default_context_name = 'Voice'

    ### INITIALIZER ###

    def __init__(
        self,
        music=None,
        context_name='Context',
        is_simultaneous=None,
        name=None,
        ):
        Container.__init__(
            self,
            is_simultaneous=is_simultaneous,
            music=music,
            name=name,
            )
        self.context_name = context_name
        self._consists_commands = []
        self._remove_commands = []
        self.is_nonsemantic = False

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of context.

        ::

            >>> context = scoretools.Context(
            ...     name='MeterVoice',
            ...     context_name='TimeSignatureContext',
            ...     )
            >>> repr(context)
            'Context()'

        Returns string.
        '''
        from abjad.tools import scoretools
        if all(isinstance(x, scoretools.Leaf) for x in self):
            return Container.__repr__(self)
        return self._get_abbreviated_string_format()

    ### PRIVATE METHODS ###

    def _copy_with_indicators_but_without_children_or_spanners(self):
        new = Container._copy_with_indicators_but_without_children_or_spanners(self)
        new._consists_commands = copy.copy(self.consists_commands)
        new._remove_commands = copy.copy(self.remove_commands)
        new.context_name = copy.copy(self.context_name)
        new.name = copy.copy(self.name)
        new.is_nonsemantic = copy.copy(self.is_nonsemantic)
        return new

    def _format_closing_slot(context, bundle):
        result = []
        result.append(('indicators', bundle.closing.indicators))
        result.append(('commands', bundle.closing.commands))
        result.append(('comments', bundle.closing.comments))
        return context._format_slot_contributions_with_indent(result)

    def _format_consists_commands(self):
        result = []
        for engraver in self.consists_commands:
            string = r'\consists {}'.format(engraver)
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
        indent = systemtools.LilyPondFormatManager.indent
        result = []
        if context.is_simultaneous:
            brackets_open = ['<<']
        else:
            brackets_open = ['{']
        remove_commands = context._format_remove_commands()
        consists_commands = context._format_consists_commands()
        overrides = bundle.grob_overrides
        settings = bundle.context_settings
        if remove_commands or consists_commands or overrides or settings:
            contributions = [context._format_invocation() + r' \with {']
            contributions = tuple(contributions)
            identifier_pair = ('context_brackets', 'open')
            result.append((identifier_pair, contributions))
            contributions = [indent + x for x in remove_commands]
            contributions = tuple(contributions)
            identifier_pair = ('engraver removals', 'remove_commands')
            result.append((identifier_pair, contributions))
            contributions = [indent + x for x in consists_commands]
            contributions = tuple(contributions)
            identifier_pair = ('engraver consists', 'consists_commands')
            result.append((identifier_pair, contributions))
            contributions = [indent + x for x in overrides]
            contributions = tuple(contributions)
            identifier_pair = ('overrides', 'overrides')
            result.append((identifier_pair, contributions))
            contributions = [indent + x for x in settings]
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

    def _format_remove_commands(self):
        result = []
        for engraver in self.remove_commands:
            string = r'\remove {}'.format(engraver)
            result.append(string)
        return result

    def _get_format_pieces(self):
        return self._format_component(pieces=True)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

    ### PUBLIC PROPERTIES ###

    @property
    def consists_commands(self):
        r'''Unordered set of LilyPond engravers to include
        in context definition.

        Manage with add, update, other standard set commands:

        ::

            >>> staff = Staff([])
            >>> staff.consists_commands.append('Horizontal_bracket_engraver')
            >>> print(format(staff))
            \new Staff \with {
                \consists Horizontal_bracket_engraver
            } {
            }

        '''
        return self._consists_commands

    @property
    def context_name(self):
        r'''Gets and sets context name of context.

        Returns string.
        '''
        return self._context_name

    @context_name.setter
    def context_name(self, expr):
        if expr is None:
            expr = type(self).__name__
        else:
            expr = str(expr)
        self._context_name = expr

    @property
    def is_nonsemantic(self):
        r'''Gets and sets nonsemantic voice flag.

        ::

            >>> pairs = [(1, 8), (5, 16), (5, 16)]
            >>> measures = scoretools.make_spacer_skip_measures(pairs)
            >>> voice = Voice(measures)
            >>> voice.name = 'HiddenTimeSignatureVoice'

        ::

            >>> voice.is_nonsemantic = True

        ..  doctest::

            >>> print(format(voice))
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

        Returns true or false.

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
        r'''Is true when context is semantic. Otherwise false.

        Returns true or false.
        '''
        return not self.is_nonsemantic

    @property
    def lilypond_context(self):
        r'''Gets `LilyPondContext` associated with context.

        Returns LilyPond context instance.
        '''
        from abjad.tools import lilypondnametools
        try:
            lilypond_context = lilypondnametools.LilyPondContext(
                name=self.context_name,
                )
        except AssertionError:
            lilypond_context = lilypondnametools.LilyPondContext(
                name=self._default_context_name,
                )
        return lilypond_context

    @property
    def remove_commands(self):
        r'''Unordered set of LilyPond engravers to remove from context.

        Manage with add, update, other standard set commands:

        ::

            >>> staff = Staff([])
            >>> staff.remove_commands.append('Time_signature_engraver')
            >>> print(format(staff))
            \new Staff \with {
                \remove Time_signature_engraver
            } {
            }

        '''
        return self._remove_commands
