import dataclasses
import enum

from . import tag as _tag


class Sites(enum.Enum):
    """
    Contribution sites.
    """

    ABSOLUTE_BEFORE = enum.auto()
    BEFORE = enum.auto()
    OPEN_BRACKETS = enum.auto()
    OPENING = enum.auto()
    CONTENTS = enum.auto()
    CLOSING = enum.auto()
    CLOSE_BRACKETS = enum.auto()
    AFTER = enum.auto()
    ABSOLUTE_AFTER = enum.auto()


class Types(enum.Enum):
    """
    Contribution types.
    """

    ARTICULATIONS = enum.auto()
    COMMANDS = enum.auto()
    CONTEXT_SETTINGS = enum.auto()
    GROB_OVERRIDES = enum.auto()
    GROB_REVERTS = enum.auto()
    LEAK = enum.auto()
    LEAKS = enum.auto()
    MARKUP = enum.auto()
    PITCHED_TRILL = enum.auto()
    SPANNER_STARTS = enum.auto()
    SPANNER_STOPS = enum.auto()
    START_BEAM = enum.auto()
    STEM_TREMOLOS = enum.auto()
    STOP_BEAM = enum.auto()
    TRILL_SPANNER_STARTS = enum.auto()
    VOICE_NUMBER = enum.auto()


@dataclasses.dataclass(slots=True)
class _ContributionsByType:
    articulations: list[str] = dataclasses.field(default_factory=list)
    commands: list[str] = dataclasses.field(default_factory=list)
    leak: list[str] = dataclasses.field(default_factory=list)
    leaks: list[str] = dataclasses.field(default_factory=list)
    markup: list[str] = dataclasses.field(default_factory=list)
    pitched_trill: list[str] = dataclasses.field(default_factory=list)
    spanner_starts: list[str] = dataclasses.field(default_factory=list)
    spanner_stops: list[str] = dataclasses.field(default_factory=list)
    start_beam: list[str] = dataclasses.field(default_factory=list)
    stem_tremolos: list[str] = dataclasses.field(default_factory=list)
    stop_beam: list[str] = dataclasses.field(default_factory=list)
    trill_spanner_starts: list[str] = dataclasses.field(default_factory=list)
    voice_number: list[str] = dataclasses.field(default_factory=list)

    def __iter__(self):
        for type_ in (
            self.articulations,
            self.commands,
            self.leak,
            self.leaks,
            self.markup,
            self.pitched_trill,
            self.spanner_starts,
            self.spanner_stops,
            self.start_beam,
            self.stem_tremolos,
            self.stop_beam,
            self.trill_spanner_starts,
            self.voice_number,
        ):
            yield type_

    def tag(self, tag, deactivate=None):
        """
        Tags contributions.
        """
        self.articulations = _tag.double_tag(self.articulations, tag, deactivate)
        self.commands = _tag.double_tag(self.commands, tag, deactivate)
        self.leak = _tag.double_tag(self.leak, tag, deactivate)
        self.leaks = _tag.double_tag(self.leaks, tag, deactivate)
        self.markup = _tag.double_tag(self.markup, tag, deactivate)
        self.pitched_trill = _tag.double_tag(self.pitched_trill, tag, deactivate)
        self.spanner_starts = _tag.double_tag(self.spanner_starts, tag, deactivate)
        self.spanner_stops = _tag.double_tag(self.spanner_stops, tag, deactivate)
        self.start_beam = _tag.double_tag(self.start_beam, tag, deactivate)
        self.stem_tremolos = _tag.double_tag(self.stem_tremolos, tag, deactivate)
        self.stop_beam = _tag.double_tag(self.stop_beam, tag, deactivate)
        self.trill_spanner_starts = _tag.double_tag(
            self.trill_spanner_starts, tag, deactivate
        )
        self.voice_number = _tag.double_tag(self.voice_number, tag, deactivate)

    def update(self, contributions):
        """
        Updates contributions with ``contributions``.
        """
        assert isinstance(contributions, type(self))
        if contributions.articulations:
            self.articulations.append(contributions.articulations)
        if contributions.commands:
            self.commands.append(contributions.commands)
        if contributions.leak:
            self.leak.append(contributions.leak)
        if contributions.leaks:
            self.leaks.append(contributions.leaks)
        if contributions.markup:
            self.markup.append(contributions.markup)
        if contributions.pitched_trill:
            self.pitched_trill.append(contributions.pitched_trill)
        if contributions.spanner_starts:
            self.spanner_starts.append(contributions.spanner_starts)
        if contributions.spanner_stops:
            self.spanner_stops.append(contributions.spanner_stops)
        if contributions.start_beam:
            self.start_beam.append(contributions.start_beam)
        if contributions.stem_tremolos:
            self.stem_tremolos.append(contributions.stem_tremolos)
        if contributions.stop_beam:
            self.stop_beam.append(contributions.stop_beam)
        if contributions.trill_spanner_starts:
            self.trill_spanner_starts.append(contributions.trill_spanner_starts)
        if contributions.voice_number:
            self.voice_number.append(contributions.voice_number)


@dataclasses.dataclass(slots=True)
class ContributionsBySite:
    """
    LilyPond format contributions.
    """

    absolute_after: _ContributionsByType = dataclasses.field(
        default_factory=_ContributionsByType
    )
    absolute_before: _ContributionsByType = dataclasses.field(
        default_factory=_ContributionsByType
    )
    before: _ContributionsByType = dataclasses.field(
        default_factory=_ContributionsByType
    )
    after: _ContributionsByType = dataclasses.field(
        default_factory=_ContributionsByType
    )
    opening: _ContributionsByType = dataclasses.field(
        default_factory=_ContributionsByType
    )
    closing: _ContributionsByType = dataclasses.field(
        default_factory=_ContributionsByType
    )
    context_settings: list = dataclasses.field(default_factory=list)
    grob_overrides: list = dataclasses.field(default_factory=list)
    grob_reverts: list = dataclasses.field(default_factory=list)

    def __iter__(self):
        for site in (
            self.absolute_before,
            self.absolute_after,
            self.before,
            self.after,
            self.opening,
            self.closing,
            self.context_settings,
            self.grob_overrides,
            self.grob_reverts,
        ):
            yield site

    @staticmethod
    def alphabetize(lists):
        assert isinstance(lists, list)
        for item in lists:
            assert isinstance(item, list), repr(item)

        def key(list_):
            list_ = [_ for _ in list_ if not _.lstrip().startswith("%! ")]
            list_ = [_.removeprefix("%@% ") for _ in list_]
            return list_

        lists_ = lists[:]
        lists_.sort(key=key)
        strings = []
        for list_ in lists_:
            strings.extend(list_)
        return strings

    # TODO: rename or remove?
    def freeze_overrides(self):
        """
        Sorts each site.
        """
        self.context_settings = list(sorted(set(self.context_settings)))
        self.grob_overrides = list(sorted(set(self.grob_overrides)))
        self.grob_reverts = list(sorted(set(self.grob_reverts)))

    def get_contribution_lists(self):
        lists = []
        for site in self:
            for list_ in site:
                if list_:
                    lists.append(list_)
        return lists

    def tag_contributions(self, tag, deactivate=None):
        """
        Tags contributions with ``tag``.
        """
        self.absolute_before.tag(tag, deactivate)
        self.absolute_after.tag(tag, deactivate)
        self.before.tag(tag, deactivate)
        self.after.tag(tag, deactivate)
        self.opening.tag(tag, deactivate)
        self.closing.tag(tag, deactivate)
        self.context_settings = _tag.double_tag(self.context_settings, tag, deactivate)
        self.grob_overrides = _tag.double_tag(self.grob_overrides, tag, deactivate)
        self.grob_reverts = _tag.double_tag(self.grob_reverts, tag, deactivate)

    def update(self, contributions):
        """
        Updates contributions with ``contributions``.
        """
        assert isinstance(contributions, type(self)), repr(contributions)
        self.absolute_before.update(contributions.absolute_before)
        self.absolute_after.update(contributions.absolute_after)
        self.before.update(contributions.before)
        self.after.update(contributions.after)
        self.opening.update(contributions.opening)
        self.closing.update(contributions.closing)
        self.context_settings.extend(contributions.context_settings)
        self.grob_overrides.extend(contributions.grob_overrides)
        self.grob_reverts.extend(contributions.grob_reverts)
