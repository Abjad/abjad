from . import contributions as _contributions
from . import enums as _enums
from . import overrides as _overrides
from . import tag as _tag


def _collect_indicators(component):
    wrappers = []
    for parent in component._get_parentage():
        wrappers_ = parent._get_indicators(unwrap=False)
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
            indicator, "_get_contributions"
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
            # if wrapper.indicator.direction is _enums.UP:
            if wrapper.direction is _enums.UP:
                up_markup_wrappers.append(wrapper)
            # elif wrapper.indicator.direction is _enums.DOWN:
            elif wrapper.direction is _enums.DOWN:
                down_markup_wrappers.append(wrapper)
            # elif wrapper.indicator.direction in (_enums.CENTER, None):
            elif wrapper.direction in (_enums.CENTER, None):
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


def _get_context_setting_contributions(component, contributions):
    result = []
    if hasattr(component, "_lilypond_type"):
        strings = _overrides.setting(component)._format_in_with_block()
        result.extend(strings)
    else:
        strings = _overrides.setting(component)._format_inline()
        result.extend(strings)
    result.sort()
    contributions.context_settings.extend(result)


def _get_context_wrapper_contributions(component, contributions, context_wrappers):
    for wrapper in context_wrappers:
        format_pieces = wrapper._get_format_pieces()
        if isinstance(format_pieces, type(contributions)):
            contributions.update(format_pieces)
        else:
            site = wrapper.indicator._site
            getattr(contributions, site).indicators.extend(format_pieces)


def _get_grob_override_contributions(component, contributions):
    result = []
    once = hasattr(component, "_written_duration")
    grob = _overrides.override(component)
    contributions_ = grob._list_contributions("override", once=once)
    for string in result[:]:
        if "NoteHead" in string and "pitch" in string:
            contributions_.remove(string)
    try:
        written_pitch = component.written_pitch
        arrow = written_pitch.arrow
    except AttributeError:
        arrow = None
    if arrow in (_enums.UP, _enums.DOWN):
        contributions__ = written_pitch._list_contributions()
        contributions_.extend(contributions__)
    contributions.grob_overrides.extend(contributions_)


def _get_grob_revert_contributions(component, contributions):
    if not hasattr(component, "_written_duration"):
        contributions_ = _overrides.override(component)._list_contributions("revert")
        contributions.grob_reverts.extend(contributions_)


def _get_indicator_contributions(component, contributions):
    (
        up_markup_wrappers,
        down_markup_wrappers,
        neutral_markup_wrappers,
        context_wrappers,
        noncontext_wrappers,
    ) = _collect_indicators(component)
    _get_markup_contributions(
        component,
        contributions,
        up_markup_wrappers,
        down_markup_wrappers,
        neutral_markup_wrappers,
    )
    _get_context_wrapper_contributions(component, contributions, context_wrappers)
    _get_noncontext_wrapper_contributions(component, contributions, noncontext_wrappers)


def _get_markup_contributions(
    component,
    contributions,
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
            markup = wrapper.indicator
            format_pieces = markup._get_format_pieces(wrapper=wrapper)
            format_pieces = _tag.double_tag(
                format_pieces, wrapper.tag, deactivate=wrapper.deactivate
            )
            contributions.after.markup.extend(format_pieces)


def _get_noncontext_wrapper_contributions(
    component, contributions, noncontext_wrappers
):
    for wrapper in noncontext_wrappers:
        indicator = wrapper.indicator
        try:
            contributions_ = indicator._get_contributions(wrapper=wrapper)
        except TypeError:
            contributions_ = indicator._get_contributions()
        if wrapper.tag:
            contributions_.tag_contributions(wrapper.tag, deactivate=wrapper.deactivate)
        contributions.update(contributions_)


def get_contributions_by_site(component) -> _contributions.ContributionsBySite:
    """
    Gets contributions by site for ``component``.
    """
    contributions = _contributions.ContributionsBySite()
    _get_indicator_contributions(component, contributions)
    _get_context_setting_contributions(component, contributions)
    _get_grob_override_contributions(component, contributions)
    _get_grob_revert_contributions(component, contributions)
    contributions.freeze_overrides()
    return contributions
