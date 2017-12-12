import copy
from abjad.tools import systemtools
from .Container import Container


class Context(Container):
    '''LilyPond context.

    ..  container:: example

        >>> context = abjad.Context(
        ...     name='MeterVoice',
        ...     context_name='GlobalContext',
        ...     )

        >>> context
        Context(context_name='GlobalContext', name='MeterVoice')

        ..  docs::

            >>> abjad.f(context)
            \context GlobalContext = "MeterVoice" {
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Contexts'

    __slots__ = (
        '_context_name',
        '_consists_commands',
        '_remove_commands',
        )

    _default_context_name = 'Voice'

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        context_name='Context',
        is_simultaneous=None,
        name=None,
        ):
        Container.__init__(
            self,
            is_simultaneous=is_simultaneous,
            components=components,
            name=name,
            )
        self.context_name = context_name
        self._consists_commands = []
        self._remove_commands = []

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of context.

        >>> context = abjad.Context(
        ...     name='MeterVoice',
        ...     context_name='GlobalContext',
        ...     )
        >>> repr(context)
        "Context(context_name='GlobalContext', name='MeterVoice')"

        Returns string.
        '''
        if self[:].are_leaves():
            return Container.__repr__(self)
        return self._get_abbreviated_string_format()

    ### PRIVATE METHODS ###

    def _copy_with_indicators_but_without_children_or_spanners(self):
        new = Container._copy_with_indicators_but_without_children_or_spanners(self)
        new._consists_commands = copy.copy(self.consists_commands)
        new._remove_commands = copy.copy(self.remove_commands)
        new.context_name = copy.copy(self.context_name)
        new.name = copy.copy(self.name)
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

    def _get_lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

    def _get_repr_kwargs_names(self):
        if self.context_name == type(self).__name__:
            return ['is_simultaneous', 'name']
        else:
            return ['is_simultaneous', 'context_name', 'name']

    ### PUBLIC PROPERTIES ###

    @property
    def consists_commands(self):
        r'''Unordered set of LilyPond engravers to include
        in context definition.

        Manage with add, update, other standard set commands:

        >>> staff = abjad.Staff([])
        >>> staff.consists_commands.append('Horizontal_bracket_engraver')
        >>> abjad.f(staff)
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
    def context_name(self, argument):
        if argument is None:
            argument = type(self).__name__
        else:
            argument = str(argument)
        self._context_name = argument

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

        >>> staff = abjad.Staff([])
        >>> staff.remove_commands.append('Time_signature_engraver')
        >>> abjad.f(staff)
        \new Staff \with {
            \remove Time_signature_engraver
        } {
        }

        '''
        return self._remove_commands
