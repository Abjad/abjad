import typing

from . import storage
from . import tag as _tag


class LilyPondFormatBundle:
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

    indent = 4 * " "

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

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return storage.StorageFormatManager(self).get_repr_format()

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
        return storage.FormatSpecification(
            client=self, storage_format_keyword_names=names
        )

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
        self._context_settings = _tag.tag(self.context_settings, tag, deactivate)
        self._grob_overrides = _tag.tag(self.grob_overrides, tag, deactivate)
        self._grob_reverts = _tag.tag(self.grob_reverts, tag, deactivate)

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


class SlotContributions:
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
        return storage.StorageFormatManager(self).get_repr_format()

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
        return storage.FormatSpecification(
            client=self, storage_format_keyword_names=names
        )

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
        self._articulations = _tag.tag(self.articulations, tag, deactivate)
        self._commands = _tag.tag(self.commands, tag, deactivate)
        self._comments = _tag.tag(self.comments, tag, deactivate)
        self._indicators = _tag.tag(self.indicators, tag, deactivate)
        self._leaks = _tag.tag(self.leaks, tag, deactivate)
        self._markup = _tag.tag(self.markup, tag, deactivate)
        self._spanners = _tag.tag(self.spanners, tag, deactivate)
        strings = []
        # make sure each line of multiline markup is tagged
        for string in self.spanner_starts:
            strings.extend(string.split("\n"))
        self._spanner_starts = _tag.tag(strings, tag, deactivate)
        self._spanner_stops = _tag.tag(self.spanner_stops, tag, deactivate)
        self._stem_tremolos = _tag.tag(self.stem_tremolos, tag, deactivate)

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
