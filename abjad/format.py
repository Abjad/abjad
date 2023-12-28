from . import _indentlib
from . import contributions as _contributions
from . import enums as _enums
from . import indicators as _indicators
from . import overrides as _overrides


def _get_context_setting_contributions(component, contributions):
    result = []
    if hasattr(component, "_lilypond_type"):
        strings = _overrides.setting(component)._format_in_with_block()
        result.extend(strings)
    else:
        strings = _overrides.setting(component)._format_inline()
        result.extend(strings)
    contributions.context_settings.extend(result)
    contributions.context_settings.sort()


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
    contributions.grob_overrides.sort()


def _get_grob_revert_contributions(component, contributions):
    if not hasattr(component, "_written_duration"):
        contributions_ = _overrides.override(component)._list_contributions("revert")
        contributions.grob_reverts.extend(contributions_)
    contributions.grob_reverts.sort()


def _get_indicator_contributions(component, contributions):
    wrappers = []
    for parent in component._get_parentage():
        wrappers_ = parent._get_indicators(unwrap=False)
        wrappers.extend(wrappers_)
    up_markup_wrappers = []
    down_markup_wrappers = []
    neutral_markup_wrappers = []
    context_wrappers = []
    noncontext_wrappers = []
    for wrapper in wrappers:
        if wrapper.annotation:
            continue
        elif not hasattr(wrapper.get_item(), "_get_contributions"):
            continue
        elif (
            wrapper.context is None
            and hasattr(wrapper.get_item(), "format_leaf_children")
            and not getattr(wrapper.get_item(), "format_leaf_children")
            and wrapper.component is not component
        ):
            continue
        elif isinstance(wrapper.unbundle_indicator(), _indicators.Markup):
            if wrapper.direction is _enums.UP:
                up_markup_wrappers.append(wrapper)
            elif wrapper.direction is _enums.DOWN:
                down_markup_wrappers.append(wrapper)
            elif wrapper.direction in (_enums.CENTER, None):
                neutral_markup_wrappers.append(wrapper)
        elif wrapper.context is not None:
            if wrapper.component is component:
                context_wrappers.append(wrapper)
        else:
            noncontext_wrappers.append(wrapper)
    context_wrappers.sort(key=lambda _: type(_.unbundle_indicator()).__name__)
    noncontext_wrappers.sort(key=lambda _: type(_.unbundle_indicator()).__name__)
    for wrappers in (
        up_markup_wrappers,
        down_markup_wrappers,
        neutral_markup_wrappers,
        context_wrappers,
        noncontext_wrappers,
    ):
        for wrapper in wrappers:
            item = wrapper.get_item()
            contributions_ = None
            try:
                contributions_ = item._get_contributions(wrapper=wrapper)
            except TypeError:
                pass
            if contributions_ is None:
                try:
                    contributions_ = item._get_contributions(
                        component=wrapper.component
                    )
                except TypeError:
                    pass
            if contributions_ is None:
                contributions_ = item._get_contributions()
            contributions_.tag_contributions(wrapper.tag, deactivate=wrapper.deactivate)
            if getattr(item, "check_effective_context", False) is True:
                if wrapper._get_effective_context() is None:
                    for list_ in contributions_.get_contribution_lists():
                        list_[:] = [rf"%%% {_} %%%" for _ in list_]
            contributions.update(contributions_)


def _get_contributions_by_site(component) -> _contributions.ContributionsBySite:
    contributions = _contributions.ContributionsBySite()
    _get_indicator_contributions(component, contributions)
    _get_context_setting_contributions(component, contributions)
    _get_grob_override_contributions(component, contributions)
    _get_grob_revert_contributions(component, contributions)
    contributions.freeze_overrides()
    return contributions


def format_component(component) -> str:
    """
    Formats ``component``.
    """
    strings = []
    contributions = _get_contributions_by_site(component)
    strings_ = component._format_absolute_before_site(contributions)
    if strings_:
        strings.append(f"% {_contributions.Sites.ABSOLUTE_BEFORE.name}:")
        strings.extend(strings_)
    strings_ = component._format_before_site(contributions)
    if strings_:
        strings.append(f"% {_contributions.Sites.BEFORE.name}:")
        strings.extend(strings_)
    if hasattr(component, "_format_open_brackets_site"):
        strings_ = component._format_open_brackets_site(contributions)
        if strings_:
            strings.append(f"% {_contributions.Sites.OPEN_BRACKETS.name}:")
            strings.extend(strings_)
    strings_ = component._format_opening_site(contributions)
    if strings_:
        strings.append(f"% {_contributions.Sites.OPENING.name}:")
        strings.extend(strings_)
    strings_ = component._format_contents()
    if strings_:
        strings.extend(strings_)
    strings_ = component._format_closing_site(contributions)
    if strings_:
        strings.append(_indentlib.INDENT + f"% {_contributions.Sites.CLOSING.name}:")
        strings.extend(strings_)
    if hasattr(component, "_format_close_brackets"):
        strings_ = component._format_close_brackets()
        if strings_:
            strings.append(f"% {_contributions.Sites.CLOSE_BRACKETS.name}:")
            strings.extend(strings_)
    strings_ = component._format_after_site(contributions)
    if strings_:
        strings.append(f"% {_contributions.Sites.AFTER.name}:")
        strings.extend(strings_)
    strings_ = component._format_absolute_after_site(contributions)
    if strings_:
        strings.append(f"% {_contributions.Sites.ABSOLUTE_AFTER.name}:")
        strings.extend(strings_)
    assert all(isinstance(_, str) for _ in strings), repr(strings)
    strings = ["" if _.isspace() else _ for _ in strings]
    string = "\n".join(strings)
    return string


def remove_site_comments(string: str) -> str:
    """
    Removes site comments from ``string``.
    """
    site_comments = []
    for site in _contributions.Sites:
        site_comments.append(f"% {site.name}:")
    for type_ in _contributions.Types:
        site_comments.append(f"% {type_.name}:")
    lines = [_ for _ in string.split("\n") if _.strip() not in site_comments]
    string = "\n".join(lines)
    return string
