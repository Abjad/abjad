from . import bundle as _bundle
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


def _bundle_context_setting_contributions(component, bundle):
    result = []
    if hasattr(component, "_lilypond_type"):
        strings = _overrides.setting(component)._format_in_with_block()
        result.extend(strings)
    else:
        strings = _overrides.setting(component)._format_inline()
        result.extend(strings)
    result.sort()
    bundle.context_settings.extend(result)


def _bundle_context_wrapper_contributions(component, bundle, context_wrappers):
    for wrapper in context_wrappers:
        format_pieces = wrapper._get_format_pieces()
        if isinstance(format_pieces, type(bundle)):
            bundle.update(format_pieces)
        else:
            site = wrapper.indicator._site
            getattr(bundle, site).indicators.extend(format_pieces)


def _bundle_grob_override_contributions(component, bundle):
    result = []
    once = hasattr(component, "_written_duration")
    grob = _overrides.override(component)
    contributions = grob._list_contributions("override", once=once)
    for string in result[:]:
        if "NoteHead" in string and "pitch" in string:
            contributions.remove(string)
    try:
        written_pitch = component.written_pitch
        arrow = written_pitch.arrow
    except AttributeError:
        arrow = None
    if arrow in (_enums.UP, _enums.DOWN):
        contributions_ = written_pitch._list_contributions()
        contributions.extend(contributions_)
    bundle.grob_overrides.extend(contributions)


def _bundle_grob_revert_contributions(component, bundle):
    if not hasattr(component, "_written_duration"):
        contributions = _overrides.override(component)._list_contributions("revert")
        bundle.grob_reverts.extend(contributions)


def _bundle_indicator_contributions(component, bundle):
    (
        up_markup_wrappers,
        down_markup_wrappers,
        neutral_markup_wrappers,
        context_wrappers,
        noncontext_wrappers,
    ) = _collect_indicators(component)
    _bundle_markup_contributions(
        component,
        bundle,
        up_markup_wrappers,
        down_markup_wrappers,
        neutral_markup_wrappers,
    )
    _bundle_context_wrapper_contributions(component, bundle, context_wrappers)
    _bundle_noncontext_wrapper_contributions(component, bundle, noncontext_wrappers)


def _bundle_markup_contributions(
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
            markup = wrapper.indicator
            format_pieces = markup._get_format_pieces(wrapper=wrapper)
            format_pieces = _tag.double_tag(
                format_pieces, wrapper.tag, deactivate=wrapper.deactivate
            )
            bundle.after.markup.extend(format_pieces)


def _bundle_noncontext_wrapper_contributions(component, bundle, noncontext_wrappers):
    for wrapper in noncontext_wrappers:
        indicator = wrapper.indicator
        try:
            bundle_ = indicator._get_lilypond_format_bundle(wrapper=wrapper)
        except TypeError:
            bundle_ = indicator._get_lilypond_format_bundle()
        if wrapper.tag:
            bundle_.tag_contributions(wrapper.tag, deactivate=wrapper.deactivate)
        bundle.update(bundle_)


def bundle_contributions(component) -> _bundle.LilyPondFormatBundle:
    """
    Bundles contributions for ``component``.
    """
    bundle = _bundle.LilyPondFormatBundle()
    _bundle_indicator_contributions(component, bundle)
    _bundle_context_setting_contributions(component, bundle)
    _bundle_grob_override_contributions(component, bundle)
    _bundle_grob_revert_contributions(component, bundle)
    bundle.freeze_overrides()
    return bundle
