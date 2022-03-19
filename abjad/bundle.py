import dataclasses

from . import tag as _tag


@dataclasses.dataclass(slots=True)
class _ContributionsByType:

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

    def update(self, contributions):
        """
        Updates contributions.
        """
        assert isinstance(contributions, type(self))
        self.articulations.extend(contributions.articulations)
        self.commands.extend(contributions.commands)
        self.comments.extend(contributions.comments)
        self.indicators.extend(contributions.indicators)
        self.leaks.extend(contributions.leaks)
        self.markup.extend(contributions.markup)
        self.spanners.extend(contributions.spanners)
        self.spanner_starts.extend(contributions.spanner_starts)
        self.spanner_stops.extend(contributions.spanner_stops)
        self.stem_tremolos.extend(contributions.stem_tremolos)
        self.trill_spanner_starts.extend(contributions.trill_spanner_starts)


@dataclasses.dataclass(slots=True)
class LilyPondFormatBundle:
    """
    LilyPond format bundle.
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

    __documentation_section__ = "LilyPond formatting"

    def freeze_overrides(self):
        """
        Makes each site immutable.
        """
        self.context_settings = tuple(sorted(set(self.context_settings)))
        self.grob_overrides = tuple(sorted(set(self.grob_overrides)))
        self.grob_reverts = tuple(sorted(set(self.grob_reverts)))

    def tag_contributions(self, tag, deactivate=None):
        """
        Tags contributions with string ``tag``.
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
        Updates format bundle with contributions in ``bundle``.
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
