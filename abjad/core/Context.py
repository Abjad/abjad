import copy
import typing

from abjad.instruments import Instrument
from abjad.lilypondnames.LilyPondContext import LilyPondContext
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.system.Tag import Tag
from abjad.system.Wrapper import Wrapper
from abjad.top.inspect import inspect

from .Container import Container


class Context(Container):
    r"""
    LilyPond context.

    ..  container:: example

        >>> context = abjad.Context(
        ...     lilypond_type='GlobalContext',
        ...     name='Meter_Voice',
        ...     )

        >>> context
        Context(lilypond_type='GlobalContext', name='Meter_Voice')

        ..  docs::

            >>> abjad.f(context)
            \context GlobalContext = "Meter_Voice"
            {
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Contexts"

    __slots__ = (
        "_lilypond_type",
        "_consists_commands",
        "_dependent_wrappers",
        "_remove_commands",
    )

    _default_lilypond_type = "Voice"

    lilypond_types = (
        "Score",
        "StaffGroup",
        "ChoirStaff",
        "GrandStaff",
        "PianoStaff",
        "Staff",
        "RhythmicStaff",
        "TabStaff",
        "DrumStaff",
        "VaticanaStaff",
        "MensuralStaff",
        "Voice",
        "VaticanaVoice",
        "MensuralVoice",
        "Lyrics",
        "DrumVoice",
        "FiguredBass",
        "TabVoice",
        "CueVoice",
        "ChordNames",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        lilypond_type: str = "Context",
        simultaneous: bool = None,
        name: str = None,
        tag: Tag = None,
    ) -> None:
        self._consists_commands: typing.List[str] = []
        self._dependent_wrappers: typing.List[Wrapper] = []
        self._remove_commands: typing.List[str] = []
        self.lilypond_type = lilypond_type
        Container.__init__(
            self, simultaneous=simultaneous, components=components, name=name, tag=tag,
        )

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Shallow copies context.

        Copies indicators.

        Does not copy children.

        Returns new component.
        """
        new_context = Container.__copy__(self)
        new_context._consists_commands = copy.copy(self.consists_commands)
        new_context._remove_commands = copy.copy(self.remove_commands)
        return new_context

    def __getnewargs__(self):
        """
        Gets new container arguments.

        Returns tuple.
        """
        return [], self.lilypond_type, self.simultaneous, self.name

    def __repr__(self):
        """
        Gets interpreter representation of context.

        ..  container:: example

            >>> context = abjad.Context(
            ...     lilypond_type='GlobalContext',
            ...     name='Meter_Voice',
            ...     )
            >>> repr(context)
            "Context(lilypond_type='GlobalContext', name='Meter_Voice')"

        Returns string.
        """
        if self[:].are_leaves():
            return Container.__repr__(self)
        return self._get_abbreviated_string_format()

    ### PRIVATE METHODS ###

    def _format_closing_slot(self, bundle):
        result = []
        result.append(("indicators", bundle.closing.indicators))
        result.append(("commands", bundle.closing.commands))
        result.append(("comments", bundle.closing.comments))
        return self._format_slot_contributions_with_indent(result)

    def _format_consists_commands(self):
        result = []
        for engraver in self.consists_commands:
            string = rf"\consists {engraver}"
            result.append(string)
        return result

    def _format_invocation(self):
        if self.name is not None:
            string = rf'\context {self.lilypond_type} = "{self.name}"'
        else:
            string = rf"\new {self.lilypond_type}"
        return string

    def _format_open_brackets_slot(self, bundle):
        indent = LilyPondFormatManager.indent
        result = []
        if self.simultaneous:
            if self.identifier:
                open_bracket = f"<<  {self.identifier}"
            else:
                open_bracket = "<<"
        else:
            if self.identifier:
                open_bracket = f"{{   {self.identifier}"
            else:
                open_bracket = "{"
        brackets_open = [open_bracket]
        remove_commands = self._format_remove_commands()
        consists_commands = self._format_consists_commands()
        overrides = bundle.grob_overrides
        settings = bundle.context_settings
        if remove_commands or consists_commands or overrides or settings:
            contributions = [self._format_invocation(), r"\with", "{"]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("context_brackets", "open")
            result.append((identifier_pair, contributions))
            contributions = [indent + _ for _ in remove_commands]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("engraver removals", "remove_commands")
            result.append((identifier_pair, contributions))
            contributions = [indent + _ for _ in consists_commands]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("engraver consists", "consists_commands")
            result.append((identifier_pair, contributions))
            contributions = [indent + _ for _ in overrides]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("overrides", "overrides")
            result.append((identifier_pair, contributions))
            contributions = [indent + _ for _ in settings]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("settings", "settings")
            result.append((identifier_pair, contributions))
            contributions = [f"}} {brackets_open[0]}"]
            contributions = ["}", open_bracket]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("context_brackets", "open")
            result.append((identifier_pair, contributions))
        else:
            contribution = self._format_invocation()
            contribution += f" {brackets_open[0]}"
            contributions = [contribution]
            contributions = [self._format_invocation(), open_bracket]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("context_brackets", "open")
            result.append((identifier_pair, contributions))
        return tuple(result)

    def _format_opening_slot(self, bundle):
        result = []
        result.append(("comments", bundle.opening.comments))
        result.append(("indicators", bundle.opening.indicators))
        result.append(("commands", bundle.opening.commands))
        return self._format_slot_contributions_with_indent(result)

    def _format_remove_commands(self):
        result = []
        for engraver in self.remove_commands:
            string = rf"\remove {engraver}"
            result.append(string)
        return result

    def _get_format_pieces(self):
        return self._format_component(pieces=True)

    def _get_lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

    @staticmethod
    def _get_persistent_wrappers(*, dependent_wrappers=None, omit_with_indicator=None):
        wrappers = {}
        for wrapper in dependent_wrappers:
            if wrapper.annotation:
                continue
            indicator = wrapper.indicator
            if not getattr(indicator, "persistent", False):
                continue
            assert isinstance(indicator.persistent, bool)
            should_omit = False
            if omit_with_indicator is not None:
                parentage = inspect(wrapper.component).parentage()
                for component in parentage:
                    if inspect(component).has_indicator(omit_with_indicator):
                        should_omit = True
                        continue
            if should_omit:
                continue
            if hasattr(indicator, "parameter"):
                key = indicator.parameter
            elif isinstance(indicator, Instrument):
                key = "Instrument"
            else:
                key = str(type(indicator))
            if (
                key not in wrappers
                or wrappers[key].start_offset <= wrapper.start_offset
            ):
                wrappers[key] = wrapper
        return wrappers

    def _get_repr_kwargs_names(self):
        if self.lilypond_type == type(self).__name__:
            return ["simultaneous", "name"]
        else:
            return ["simultaneous", "lilypond_type", "name"]

    ### PUBLIC PROPERTIES ###

    @property
    def consists_commands(self):
        r"""
        Unordered set of LilyPond engravers to include
        in context definition.

        ..  container:: example

            Manage with add, update, other standard set commands:

            >>> staff = abjad.Staff([])
            >>> staff.consists_commands.append('Horizontal_bracket_engraver')
            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \consists Horizontal_bracket_engraver
            }
            {
            }

        """
        return self._consists_commands

    @property
    def lilypond_type(self):
        """
        Gets lilypond type.

        ..  container:: example

            >>> context = abjad.Context(
            ...     lilypond_type='ViolinStaff',
            ...     name='MyViolinStaff',
            ...     )
            >>> context.lilypond_type
            'ViolinStaff'

        Gets and sets lilypond type of context.

        Returns string.
        """
        return self._lilypond_type

    @lilypond_type.setter
    def lilypond_type(self, argument):
        if argument is None:
            argument = type(self).__name__
        else:
            argument = str(argument)
        self._lilypond_type = argument

    @property
    def lilypond_context(self):
        """
        Gets ``LilyPondContext`` associated with context.

        Returns LilyPond context instance.
        """
        try:
            lilypond_context = LilyPondContext(name=self.lilypond_type)
        except AssertionError:
            lilypond_context = LilyPondContext(name=self._default_lilypond_type)
        return lilypond_context

    @property
    def remove_commands(self):
        r"""
        Unordered set of LilyPond engravers to remove from context.

        ..  container:: example

            Manage with add, update, other standard set commands:

            >>> staff = abjad.Staff([])
            >>> staff.remove_commands.append('Time_signature_engraver')
            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \remove Time_signature_engraver
            }
            {
            }

        """
        return self._remove_commands

    @property
    def tag(self) -> typing.Optional[Tag]:
        r"""
        Gets tag.

        ..  container:: example

            >>> context = abjad.Context(
            ...     "c'4 d' e' f'",
            ...     lilypond_type='CustomContext',
            ...     tag=abjad.Tag('RED'),
            ...     )
            >>> abjad.show(context) # doctest: +SKIP

            >>> abjad.f(context, strict=20)
            \new CustomContext  %! RED
            {                   %! RED
                c'4
                d'4
                e'4
                f'4
            }                   %! RED

        """
        return super().tag
