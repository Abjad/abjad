import typing

from . import enums
from .lilypondnames.LilyPondGrobNameManager import override
from .lilypondnames.LilyPondSettingNameManager import setting
from .new import new
from .scheme import Scheme, SchemePair
from .storage import FormatSpecification, StorageFormatManager
from .utilities.String import String


class LilyPondFormatBundle(object):
    """
    LilyPond format bundle.

    Transient class created to hold the collection of all
    format contributions generated on behalf of a single component.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "LilyPond formatting"

    __slots__ = (
        "_absolute_after",
        "_absolute_before",
        "_after",
        "_before",
        "_closing",
        "_context_settings",
        "_grob_overrides",
        "_grob_reverts",
        "_opening",
    )

    ### INITIALIZER ###

    def __init__(self):
        self._absolute_after = SlotContributions()
        self._absolute_before = SlotContributions()
        self._before = SlotContributions()
        self._after = SlotContributions()
        self._opening = SlotContributions()
        self._closing = SlotContributions()
        self._context_settings = []
        self._grob_overrides = []
        self._grob_reverts = []

    ### SPECIAL METHODS ###

    def __format__(self, format_specification="") -> str:
        """
        Formats object.
        """
        return StorageFormatManager(self).get_storage_format()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        slot_contribution_names = (
            "absolute_before",
            "absolute_after",
            "before",
            "after",
            "opening",
            "closing",
        )
        grob_contribution_names = (
            "context_settings",
            "grob_overrides",
            "grob_reverts",
        )
        names = [
            _ for _ in slot_contribution_names if getattr(self, _).has_contributions
        ]
        names.extend(_ for _ in grob_contribution_names if getattr(self, _))
        return FormatSpecification(client=self, storage_format_kwargs_names=names)

    ### PUBLIC METHODS ###

    def get(self, identifier):
        """
        Gets ``identifier``.

        Returns format contributions object or list.
        """
        return getattr(self, identifier)

    def sort_overrides(self):
        """
        Makes each slot immutable.

        Returns none.
        """
        self._context_settings = tuple(sorted(set(self.context_settings)))
        self._grob_overrides = tuple(sorted(set(self.grob_overrides)))
        self._grob_reverts = tuple(sorted(set(self.grob_reverts)))

    def tag_format_contributions(self, tag, deactivate=None):
        """
        Tags format contributions with string ``tag``.

        Returns none.
        """
        self.absolute_before.tag(tag, deactivate)
        self.absolute_after.tag(tag, deactivate)
        self.before.tag(tag, deactivate)
        self.after.tag(tag, deactivate)
        self.opening.tag(tag, deactivate)
        self.closing.tag(tag, deactivate)
        self._context_settings = LilyPondFormatManager.tag(
            self.context_settings, tag, deactivate
        )
        self._grob_overrides = LilyPondFormatManager.tag(
            self.grob_overrides, tag, deactivate
        )
        self._grob_reverts = LilyPondFormatManager.tag(
            self.grob_reverts, tag, deactivate
        )

    def update(self, format_bundle):
        """
        Updates format bundle with all format contributions in
        ``format_bundle``.

        Returns none.
        """
        if hasattr(format_bundle, "_get_lilypond_format_bundle"):
            format_bundle = format_bundle._get_lilypond_format_bundle()
        assert isinstance(format_bundle, type(self))
        self.absolute_before.update(format_bundle.absolute_before)
        self.absolute_after.update(format_bundle.absolute_after)
        self.before.update(format_bundle.before)
        self.after.update(format_bundle.after)
        self.opening.update(format_bundle.opening)
        self.closing.update(format_bundle.closing)
        self.context_settings.extend(format_bundle.context_settings)
        self.grob_overrides.extend(format_bundle.grob_overrides)
        self.grob_reverts.extend(format_bundle.grob_reverts)

    ### PUBLIC PROPERTIES ###

    @property
    def absolute_after(self):
        """
        Aboslute after slot contributions.

        Returns slot contributions object.
        """
        return self._absolute_after

    @property
    def absolute_before(self):
        """
        Absolute before slot contributions.

        Returns slot contributions object.
        """
        return self._absolute_before

    @property
    def after(self):
        """
        After slot contributions.

        Returns slot contributions object.
        """
        return self._after

    @property
    def before(self):
        """
        Before slot contributions.

        Returns slot contributions object.
        """
        return self._before

    @property
    def closing(self):
        """
        Closing slot contributions.

        Returns slot contributions object.
        """
        return self._closing

    @property
    def context_settings(self):
        """
        Context setting format contributions.

        Returns list.
        """
        return self._context_settings

    @property
    def grob_overrides(self):
        """
        Grob override format contributions.

        Returns list.
        """
        return self._grob_overrides

    @property
    def grob_reverts(self):
        """
        Grob revert format contributions.

        Returns list.
        """
        return self._grob_reverts

    @property
    def opening(self):
        """
        Opening slot contributions.

        Returns slot contributions object.
        """
        return self._opening


class LilyPondFormatManager(object):
    """
    Manages LilyPond formatting logic.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "LilyPond formatting"

    __slots__ = ()

    indent = 4 * " "

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _collect_indicators(component):
        from .core.Component import inspect

        wrappers = []
        for parent in inspect(component).parentage():
            wrappers_ = inspect(parent).wrappers()
            wrappers.extend(wrappers_)
        up_markup_wrappers = []
        down_markup_wrappers = []
        neutral_markup_wrappers = []
        context_wrappers = []
        noncontext_wrappers = []
        # classify wrappers attached to component
        for wrapper in wrappers:
            # skip nonprinting indicators like annotation
            indicator = wrapper.indicator
            if not hasattr(indicator, "_get_lilypond_format") and not hasattr(
                indicator, "_get_lilypond_format_bundle"
            ):
                continue
            elif wrapper.annotation is not None:
                continue
            # skip comments and commands unless attached directly to us
            elif (
                wrapper.context is None
                and hasattr(wrapper.indicator, "_format_leaf_children")
                and not getattr(wrapper.indicator, "_format_leaf_children")
                and wrapper.component is not component
            ):
                continue
            # store markup wrappers
            elif wrapper.indicator.__class__.__name__ == "Markup":
                if wrapper.indicator.direction is enums.Up:
                    up_markup_wrappers.append(wrapper)
                elif wrapper.indicator.direction is enums.Down:
                    down_markup_wrappers.append(wrapper)
                elif wrapper.indicator.direction in (enums.Center, None):
                    neutral_markup_wrappers.append(wrapper)
            # store context wrappers
            elif wrapper.context is not None:
                if wrapper.annotation is None and wrapper.component is component:
                    context_wrappers.append(wrapper)
            # store noncontext wrappers
            else:
                noncontext_wrappers.append(wrapper)
        indicators = (
            up_markup_wrappers,
            down_markup_wrappers,
            neutral_markup_wrappers,
            context_wrappers,
            noncontext_wrappers,
        )
        return indicators

    @staticmethod
    def _populate_context_setting_format_contributions(component, bundle):
        result = []
        manager = LilyPondFormatManager
        if hasattr(component, "_lilypond_type"):
            for name, value in vars(setting(component)).items():
                string = manager.format_lilypond_context_setting_in_with_block(
                    name, value
                )
                result.append(string)
        else:
            contextualizer = setting(component)
            variables = vars(contextualizer)
            for name, value in variables.items():
                # if we've found a leaf context namespace
                if name.startswith("_"):
                    for x, y in vars(value).items():
                        if not x.startswith("_"):
                            string = manager.format_lilypond_context_setting_inline(
                                x, y, name
                            )
                            result.append(string)
                # otherwise we've found a default leaf context setting
                else:
                    # parse default context setting
                    string = manager.format_lilypond_context_setting_inline(name, value)
                    result.append(string)
        result.sort()
        bundle.context_settings.extend(result)

    @staticmethod
    def _populate_context_wrapper_format_contributions(
        component, bundle, context_wrappers
    ):
        for wrapper in context_wrappers:
            format_pieces = wrapper._get_format_pieces()
            if isinstance(format_pieces, type(bundle)):
                bundle.update(format_pieces)
            else:
                format_slot = wrapper.indicator._format_slot
                bundle.get(format_slot).indicators.extend(format_pieces)

    @staticmethod
    def _populate_grob_override_format_contributions(component, bundle):
        result = []
        once = hasattr(component, "_written_duration")
        grob = override(component)
        contributions = grob._list_format_contributions("override", once=once)
        for string in result[:]:
            if "NoteHead" in string and "pitch" in string:
                contributions.remove(string)
        try:
            written_pitch = component.written_pitch
            arrow = written_pitch.arrow
        except AttributeError:
            arrow = None
        if arrow in (enums.Up, enums.Down):
            contributions_ = written_pitch._list_format_contributions()
            contributions.extend(contributions_)
        bundle.grob_overrides.extend(contributions)

    @staticmethod
    def _populate_grob_revert_format_contributions(component, bundle):
        if not hasattr(component, "_written_duration"):
            manager = override(component)
            contributions = manager._list_format_contributions("revert")
            bundle.grob_reverts.extend(contributions)

    @staticmethod
    def _populate_indicator_format_contributions(component, bundle):
        manager = LilyPondFormatManager
        (
            up_markup_wrappers,
            down_markup_wrappers,
            neutral_markup_wrappers,
            context_wrappers,
            noncontext_wrappers,
        ) = LilyPondFormatManager._collect_indicators(component)
        manager._populate_markup_format_contributions(
            component,
            bundle,
            up_markup_wrappers,
            down_markup_wrappers,
            neutral_markup_wrappers,
        )
        manager._populate_context_wrapper_format_contributions(
            component, bundle, context_wrappers
        )
        manager._populate_noncontext_wrapper_format_contributions(
            component, bundle, noncontext_wrappers
        )

    @staticmethod
    def _populate_markup_format_contributions(
        component,
        bundle,
        up_markup_wrappers,
        down_markup_wrappers,
        neutral_markup_wrappers,
    ):
        for wrappers in (
            up_markup_wrappers,
            down_markup_wrappers,
            neutral_markup_wrappers,
        ):
            for wrapper in wrappers:
                if wrapper.indicator.direction is None:
                    markup = new(wrapper.indicator, direction="-")
                else:
                    markup = wrapper.indicator
                format_pieces = markup._get_format_pieces()
                format_pieces = LilyPondFormatManager.tag(
                    format_pieces, wrapper.tag, deactivate=wrapper.deactivate
                )
                bundle.after.markup.extend(format_pieces)

    @staticmethod
    def _populate_noncontext_wrapper_format_contributions(
        component, bundle, noncontext_wrappers
    ):
        for wrapper in noncontext_wrappers:
            indicator = wrapper.indicator
            if hasattr(indicator, "_get_lilypond_format_bundle"):
                bundle_ = indicator._get_lilypond_format_bundle()
                if wrapper.tag:
                    bundle_.tag_format_contributions(
                        wrapper.tag, deactivate=wrapper.deactivate
                    )
                if bundle_ is not None:
                    bundle.update(bundle_)

    @staticmethod
    def _populate_spanner_format_contributions(component, bundle):
        from .core.Component import inspect

        if not hasattr(component, "_spanners"):
            return
        pairs = []
        for spanner in inspect(component).spanners():
            spanner_bundle = spanner._get_lilypond_format_bundle(component)
            spanner_bundle.tag_format_contributions(
                spanner._tag, deactivate=spanner._deactivate
            )
            pair = (spanner, spanner_bundle)
            pairs.append(pair)
        pairs.sort(key=lambda _: type(_[0]).__name__)
        for spanner, spanner_bundle in pairs:
            bundle.update(spanner_bundle)

    ### PUBLIC METHODS ###

    @staticmethod
    def align_tags(string: str, n: int) -> str:
        """
        Line-breaks ``string`` and aligns tags starting a column ``n``.
        """
        if not isinstance(n, int):
            raise Exception(f"must be integer:\n    {repr(n)}")
        lines = []
        for line in string.split("\n"):
            if "%!" not in line:
                lines.append(line)
                continue
            location = line.find("%!")
            left = line[:location].rstrip()
            right = line[location:]
            pad = n - len(left)
            if pad < 1:
                pad = 1
            line = left + pad * " " + right
            lines.append(line)
        string = "\n".join(lines)
        return string

    @staticmethod
    def bundle_format_contributions(component) -> "LilyPondFormatBundle":
        """
        Gets all format contributions for ``component``.
        """
        manager = LilyPondFormatManager
        bundle = LilyPondFormatBundle()
        manager._populate_indicator_format_contributions(component, bundle)
        manager._populate_spanner_format_contributions(component, bundle)
        manager._populate_context_setting_format_contributions(component, bundle)
        manager._populate_grob_override_format_contributions(component, bundle)
        manager._populate_grob_revert_format_contributions(component, bundle)
        bundle.sort_overrides()
        return bundle

    @staticmethod
    def format_lilypond_attribute(attribute) -> str:
        """
        Formats LilyPond attribute according to Scheme formatting conventions.
        """
        assert isinstance(attribute, str), repr(attribute)
        attribute = attribute.replace("__", ".")
        result = attribute.replace("_", "-")
        return result

    @staticmethod
    def format_lilypond_context_setting_in_with_block(name, value) -> str:
        """
        Formats LilyPond context setting ``name`` with ``value`` in LilyPond
        with-block.
        """
        assert isinstance(name, str), repr(name)
        name = name.split("_")
        first = name[0:1]
        rest = name[1:]
        rest = [x.title() for x in rest]
        name = first + rest
        name = "".join(name)
        value = LilyPondFormatManager.format_lilypond_value(value)
        value_parts = value.split("\n")
        result = rf"{name!s} = {value_parts[0]!s}"
        pieces = [result]
        for part in value_parts[1:]:
            pieces.append(LilyPondFormatManager.indent + part)
        return "\n".join(pieces)

    @staticmethod
    def format_lilypond_context_setting_inline(name, value, context=None) -> str:
        """
        Formats LilyPond context setting ``name`` with ``value`` in
        ``context``.
        """
        name = name.split("_")
        first = name[0:1]
        rest = name[1:]
        rest = [x.title() for x in rest]
        name = first + rest
        name = "".join(name)
        value = LilyPondFormatManager.format_lilypond_value(value)
        if context is not None:
            context_string = context[1:]
            context_string = context_string.split("_")
            context_string = [x.title() for x in context_string]
            context_string = "".join(context_string)
            context_string += "."
        else:
            context_string = ""
        result = rf"\set {context_string}{name} = {value}"
        return result

    @staticmethod
    def format_lilypond_value(argument) -> str:
        """
        Formats LilyPond ``argument`` according to Scheme formatting
        conventions.
        """
        if "_get_lilypond_format" in dir(argument) and not isinstance(argument, str):
            pass
        elif argument in (True, False):
            argument = Scheme(argument)
        elif argument in (enums.Up, enums.Down, enums.Left, enums.Right, enums.Center,):
            argument = Scheme(repr(argument).lower())
        elif isinstance(argument, int) or isinstance(argument, float):
            argument = Scheme(argument)
        elif argument in Scheme.lilypond_color_constants:
            argument = Scheme(argument)
        elif isinstance(argument, str) and argument.startswith("#"):
            # argument = Scheme(argument)
            return argument
        elif isinstance(argument, str) and "::" in argument:
            argument = Scheme(argument)
        elif isinstance(argument, tuple) and len(argument) == 2:
            argument = SchemePair(argument)
        elif isinstance(argument, str) and " " not in argument:
            argument = Scheme(argument, quoting="'")
        elif isinstance(argument, str) and " " in argument:
            argument = Scheme(argument)
        else:
            argument = Scheme(argument, quoting="'")
        return format(argument, "lilypond")

    @staticmethod
    def left_shift_tags(text, realign=None) -> str:
        """
        Left shifts tags in ``strings`` and realigns to column ``realign``.
        """
        strings = text.split("\n")
        strings_ = []
        for string in strings:
            if "%@% " not in string or "%!" not in string:
                strings_.append(string)
                continue
            if not string.startswith(4 * " "):
                strings_.append(string)
                continue
            string_ = string[4:]
            tag_start = string_.find("%!")
            string_ = list(string_)
            string_[tag_start:tag_start] = 4 * " "
            string_ = "".join(string_)
            strings_.append(string_)
        text = "\n".join(strings_)
        if realign is not None:
            text = LilyPondFormatManager.align_tags(text, n=realign)
        return text

    @staticmethod
    def make_lilypond_override_string(
        grob, attribute, value, context=None, once=False
    ) -> str:
        """
        Makes Lilypond override string.
        """
        grob = String(grob).to_upper_camel_case()
        attribute = LilyPondFormatManager.format_lilypond_attribute(attribute)
        value = LilyPondFormatManager.format_lilypond_value(value)
        if context is not None:
            context = String(context).capitalize_start() + "."
        else:
            context = ""
        if once is True:
            once = r"\once "
        else:
            once = ""
        result = rf"{once}\override {context}{grob}.{attribute} = {value}"
        return result

    @staticmethod
    def make_lilypond_revert_string(grob, attribute, context=None) -> str:
        r"""
        Makes LilyPond revert string.

        ..  container:: example

            >>> abjad.LilyPondFormatManager.make_lilypond_revert_string(
            ...     'glissando',
            ...     'bound_details__right__arrow',
            ...     )
            '\\revert Glissando.bound-details.right.arrow'

        """
        grob = String(grob).to_upper_camel_case()
        dotted = LilyPondFormatManager.format_lilypond_attribute(attribute)
        if context is not None:
            context = String(context).to_upper_camel_case()
            context += "."
        else:
            context = ""
        result = rf"\revert {context}{grob}.{dotted}"
        return result

    @staticmethod
    def make_lilypond_tweak_string(
        attribute, value, *, directed=True, grob=None, literal=None
    ) -> str:
        r"""
        Makes Lilypond \tweak string.
        """
        if grob is not None:
            grob = String(grob).to_upper_camel_case()
            grob += "."
        else:
            grob = ""
        attribute = LilyPondFormatManager.format_lilypond_attribute(attribute)
        if not literal:
            value = LilyPondFormatManager.format_lilypond_value(value)
        string = rf"\tweak {grob}{attribute} {value}"
        if directed:
            string = "- " + string
        return string

    @staticmethod
    def tag(strings, tag, deactivate=None) -> typing.List[str]:
        """
        Tags ``strings`` with ``tag``.
        """
        if not tag:
            return strings
        if not strings:
            return strings
        if deactivate is not None:
            assert isinstance(deactivate, type(True)), repr(deactivate)
        length = max([len(_) for _ in strings])
        strings_ = []
        for string in strings:
            if "%!" in string and r"\tweak" in string:
                strings_.append(string)
                continue
            if "%!" not in string:
                pad = length - len(string)
            else:
                pad = 0
            tag_ = pad * " " + " " + "%!" + " " + str(tag)
            string = string + tag_
            strings_.append(string)
        if deactivate is True:
            strings_ = ["%@% " + _ for _ in strings_]
        return strings_


class SlotContributions(object):
    """
    Slot contributions.
    """

    __documentation_section__ = "LilyPond formatting"

    __slots__ = (
        "_articulations",
        "_commands",
        "_comments",
        "_indicators",
        "_leaks",
        "_markup",
        "_spanners",
        "_spanner_starts",
        "_spanner_stops",
        "_stem_tremolos",
        "_trill_spanner_starts",
    )

    ### INITIALIZER ###

    def __init__(self) -> None:
        self._articulations: typing.List[str] = []
        self._commands: typing.List[str] = []
        self._comments: typing.List[str] = []
        self._indicators: typing.List[str] = []
        self._leaks: typing.List[str] = []
        self._markup: typing.List[str] = []
        self._spanners: typing.List[str] = []
        self._spanner_starts: typing.List[str] = []
        self._spanner_stops: typing.List[str] = []
        self._stem_tremolos: typing.List[str] = []
        self._trill_spanner_starts: typing.List[str] = []

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        names = [
            "articulations",
            "commands",
            "comments",
            "indicators",
            "markup",
            "spanners",
            "spanner_starts",
            "spanner_stops",
            "stem_tremolos",
            "trill_spanner_starts",
        ]
        names = [_ for _ in names if getattr(self, _)]
        return FormatSpecification(client=self, storage_format_kwargs_names=names)

    ### PUBLIC PROPERTIES ###

    @property
    def articulations(self) -> typing.List[str]:
        """
        Gets articulations.
        """
        return self._articulations

    @property
    def commands(self) -> typing.List[str]:
        """
        Gets commands.
        """
        return self._commands

    @property
    def comments(self) -> typing.List[str]:
        """
        Gets comments.
        """
        return self._comments

    @property
    def has_contributions(self) -> bool:
        """
        Is true when has contributions.
        """
        contribution_categories = (
            "articulations",
            "commands",
            "comments",
            "indicators",
            "leaks",
            "markup",
            "spanners",
            "spanner_starts",
            "spanner_stops",
            "stem_tremolos",
            "trill_spanner_starts",
        )
        return any(
            getattr(self, contribution_category)
            for contribution_category in contribution_categories
        )

    @property
    def indicators(self) -> typing.List[str]:
        """
        Gets indicators.
        """
        return self._indicators

    @property
    def leaks(self) -> typing.List[str]:
        """
        Gets leaks.
        """
        return self._leaks

    @property
    def markup(self) -> typing.List[str]:
        """
        Gets markup.
        """
        return self._markup

    @property
    def spanner_starts(self) -> typing.List[str]:
        """
        Gets spanner starts.
        """
        return self._spanner_starts

    @property
    def spanner_stops(self) -> typing.List[str]:
        """
        Gets spanner stops.
        """
        return self._spanner_stops

    @property
    def spanners(self) -> typing.List[str]:
        """
        Gets spanners.
        """
        return self._spanners

    @property
    def stem_tremolos(self) -> typing.List[str]:
        """
        Gets stem tremolos.
        """
        return self._stem_tremolos

    @property
    def trill_spanner_starts(self) -> typing.List[str]:
        """
        Gets trill spanner starts.
        """
        return self._trill_spanner_starts

    ### PUBLIC METHODS ###

    def get(self, identifier):
        """
        Gets ``identifier``.
        """
        return getattr(self, identifier)

    def tag(self, tag, deactivate=None):
        """
        Tags contributions.
        """
        self._articulations = LilyPondFormatManager.tag(
            self.articulations, tag, deactivate
        )
        self._commands = LilyPondFormatManager.tag(self.commands, tag, deactivate)
        self._comments = LilyPondFormatManager.tag(self.comments, tag, deactivate)
        self._indicators = LilyPondFormatManager.tag(self.indicators, tag, deactivate)
        self._leaks = LilyPondFormatManager.tag(self.leaks, tag, deactivate)
        self._markup = LilyPondFormatManager.tag(self.markup, tag, deactivate)
        self._spanners = LilyPondFormatManager.tag(self.spanners, tag, deactivate)
        strings = []
        # make sure each line of multiline markup is tagged
        for string in self.spanner_starts:
            strings.extend(string.split("\n"))
        self._spanner_starts = LilyPondFormatManager.tag(strings, tag, deactivate)
        self._spanner_stops = LilyPondFormatManager.tag(
            self.spanner_stops, tag, deactivate
        )
        self._stem_tremolos = LilyPondFormatManager.tag(
            self.stem_tremolos, tag, deactivate
        )

    def update(self, slot_contributions):
        """
        Updates contributions.
        """
        assert isinstance(slot_contributions, type(self))
        self.articulations.extend(slot_contributions.articulations)
        self.commands.extend(slot_contributions.commands)
        self.comments.extend(slot_contributions.comments)
        self.indicators.extend(slot_contributions.indicators)
        self.leaks.extend(slot_contributions.leaks)
        self.markup.extend(slot_contributions.markup)
        self.spanners.extend(slot_contributions.spanners)
        self.spanner_starts.extend(slot_contributions.spanner_starts)
        self.spanner_stops.extend(slot_contributions.spanner_stops)
        self.stem_tremolos.extend(slot_contributions.stem_tremolos)
        self.trill_spanner_starts.extend(slot_contributions.trill_spanner_starts)


### FUNCTIONS ###


def f(argument, strict=None):
    r"""
    Formats ``argument`` and prints result.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup('Allegro', direction=abjad.Up)
        >>> markup = markup.with_color('blue')
        >>> abjad.attach(markup, staff[0])
        >>> for leaf in staff:
        ...     abjad.attach(abjad.Articulation('.'), leaf)
        ...
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            - \staccato
            ^ \markup {
                \with-color
                    #blue
                    Allegro
                }
            d'4
            - \staccato
            e'4
            - \staccato
            f'4
            - \staccato
        }

        >>> abjad.show(staff) # doctest: +SKIP

    """
    if strict is not None:
        assert isinstance(strict, int), repr(strict)
    if hasattr(argument, "_publish_storage_format"):
        string = StorageFormatManager(argument).get_storage_format()
    else:
        string = format(argument, "lilypond")
    realign = None
    if isinstance(strict, int):
        string = LilyPondFormatManager.align_tags(string, strict)
        realign = strict
    string = LilyPondFormatManager.left_shift_tags(string, realign=realign)
    print(string)
