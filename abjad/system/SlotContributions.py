import typing
from abjad.system.AbjadObject import AbjadObject


class SlotContributions(AbjadObject):
    """
    Slot contributions.
    """

    __documentation_section__ = 'LilyPond formatting'

    __slots__ = (
        '_articulations',
        '_commands',
        '_comments',
        '_indicators',
        '_leaks',
        '_markup',
        '_spanners',
        '_spanner_starts',
        '_spanner_stops',
        '_stem_tremolos',
        '_trill_spanner_starts',
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

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        names = [
            'articulations',
            'commands',
            'comments',
            'indicators',
            'markup',
            'spanners',
            'spanner_starts',
            'spanner_stops',
            'stem_tremolos',
            'trill_spanner_starts',
            ]
        names = [_ for _ in names if getattr(self, _)]
        return abjad.FormatSpecification(
            client=self,
            storage_format_kwargs_names=names,
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
            'articulations',
            'commands',
            'comments',
            'indicators',
            'leaks',
            'markup',
            'spanners',
            'spanner_starts',
            'spanner_stops',
            'stem_tremolos',
            'trill_spanner_starts',
            )
        return any(getattr(self, contribution_category)
            for contribution_category in contribution_categories)

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
        import abjad
        self._articulations = abjad.LilyPondFormatManager.tag(
            self.articulations,
            tag,
            deactivate,
            )
        self._commands = abjad.LilyPondFormatManager.tag(
            self.commands,
            tag,
            deactivate,
            )
        self._comments = abjad.LilyPondFormatManager.tag(
            self.comments,
            tag,
            deactivate,
            )
        self._indicators = abjad.LilyPondFormatManager.tag(
            self.indicators,
            tag,
            deactivate,
            )
        self._leaks = abjad.LilyPondFormatManager.tag(
            self.leaks,
            tag,
            deactivate,
            )
        self._markup = abjad.LilyPondFormatManager.tag(
            self.markup,
            tag,
            deactivate,
            )
        self._spanners = abjad.LilyPondFormatManager.tag(
            self.spanners,
            tag,
            deactivate,
            )
        strings = []
        # make sure each line of multiline markup is tagged
        for string in self.spanner_starts:
            strings.extend(string.split('\n'))
        self._spanner_starts = abjad.LilyPondFormatManager.tag(
            strings,
            tag,
            deactivate,
            )
        self._spanner_stops = abjad.LilyPondFormatManager.tag(
            self.spanner_stops,
            tag,
            deactivate,
            )
        self._stem_tremolos = abjad.LilyPondFormatManager.tag(
            self.stem_tremolos,
            tag,
            deactivate,
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
        self.trill_spanner_starts.extend(
            slot_contributions.trill_spanner_starts
            )
