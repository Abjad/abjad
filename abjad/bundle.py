import dataclasses

from . import tag as _tag


@dataclasses.dataclass(slots=True)
class SlotContributions:
    """
    Slot contributions.
    """

    articulations: list[str] = dataclasses.field(default_factory=list)
    commands: list[str] = dataclasses.field(default_factory=list)
    comments: list[str] = dataclasses.field(default_factory=list)
    indicators: list[str] = dataclasses.field(default_factory=list)
    leaks: list[str] = dataclasses.field(default_factory=list)
    markup: list[str] = dataclasses.field(default_factory=list)
    spanners: list[str] = dataclasses.field(default_factory=list)
    spanner_starts: list[str] = dataclasses.field(default_factory=list)
    spanner_stops: list[str] = dataclasses.field(default_factory=list)
    stem_tremolos: list[str] = dataclasses.field(default_factory=list)
    trill_spanner_starts: list[str] = dataclasses.field(default_factory=list)

    __documentation_section__ = "LilyPond formatting"

    def tag(self, tag, deactivate=None):
        """
        Tags contributions.
        """
        self.articulations = _tag.double_tag(self.articulations, tag, deactivate)
        self.commands = _tag.double_tag(self.commands, tag, deactivate)
        self.comments = _tag.double_tag(self.comments, tag, deactivate)
        self.indicators = _tag.double_tag(self.indicators, tag, deactivate)
        self.leaks = _tag.double_tag(self.leaks, tag, deactivate)
        self.markup = _tag.double_tag(self.markup, tag, deactivate)
        self.spanners = _tag.double_tag(self.spanners, tag, deactivate)
        strings = []
        # make sure each line of multiline markup is tagged
        for string in self.spanner_starts:
            strings.extend(string.split("\n"))
        self.spanner_starts = _tag.double_tag(strings, tag, deactivate)
        self.spanner_stops = _tag.double_tag(self.spanner_stops, tag, deactivate)
        self.stem_tremolos = _tag.double_tag(self.stem_tremolos, tag, deactivate)

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


@dataclasses.dataclass(slots=True)
class LilyPondFormatBundle:
    """
    LilyPond format bundle.

    Transient class created to hold the collection of all format contributions generated
    on behalf of a single component.
    """

    absolute_after: SlotContributions = dataclasses.field(
        default_factory=SlotContributions
    )
    absolute_before: SlotContributions = dataclasses.field(
        default_factory=SlotContributions
    )
    before: SlotContributions = dataclasses.field(default_factory=SlotContributions)
    after: SlotContributions = dataclasses.field(default_factory=SlotContributions)
    opening: SlotContributions = dataclasses.field(default_factory=SlotContributions)
    closing: SlotContributions = dataclasses.field(default_factory=SlotContributions)
    context_settings: list = dataclasses.field(default_factory=list)
    grob_overrides: list = dataclasses.field(default_factory=list)
    grob_reverts: list = dataclasses.field(default_factory=list)

    __documentation_section__ = "LilyPond formatting"

    def sort_overrides(self):
        """
        Makes each slot immutable.
        """
        self.context_settings = tuple(sorted(set(self.context_settings)))
        self.grob_overrides = tuple(sorted(set(self.grob_overrides)))
        self.grob_reverts = tuple(sorted(set(self.grob_reverts)))

    def tag_format_contributions(self, tag, deactivate=None):
        """
        Tags format contributions with string ``tag``.
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

    def update(self, bundle):
        """
        Updates format bundle with all format contributions in ``bundle``.
        """
        assert isinstance(bundle, type(self))
        self.absolute_before.update(bundle.absolute_before)
        self.absolute_after.update(bundle.absolute_after)
        self.before.update(bundle.before)
        self.after.update(bundle.after)
        self.opening.update(bundle.opening)
        self.closing.update(bundle.closing)
        self.context_settings.extend(bundle.context_settings)
        self.grob_overrides.extend(bundle.grob_overrides)
        self.grob_reverts.extend(bundle.grob_reverts)
