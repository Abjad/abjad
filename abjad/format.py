from . import bundle as _bundle
from . import enums, overrides, storage
from . import tag as _tag
from .new import new


def remove_tags(string) -> str:
    """
    Removes all tags from ``string``.
    """
    lines = []
    for line in string.split("\n"):
        if "%!" not in line:
            lines.append(line)
            continue
        tag_start = line.find("%!")
        line = line[:tag_start]
        line = line.rstrip()
        lines.append(line)
    string = "\n".join(lines)
    return string


class LilyPondFormatManager:
    """
    Manages LilyPond formatting logic.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "LilyPond formatting"

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return storage.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
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
        if hasattr(component, "_lilypond_type"):
            strings = overrides.setting(component)._format_in_with_block()
            result.extend(strings)
        else:
            strings = overrides.setting(component)._format_inline()
            result.extend(strings)
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
        grob = overrides.override(component)
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
            contributions = overrides.override(component)._list_format_contributions(
                "revert"
            )
            bundle.grob_reverts.extend(contributions)

    @staticmethod
    def _populate_indicator_format_contributions(component, bundle):
        (
            up_markup_wrappers,
            down_markup_wrappers,
            neutral_markup_wrappers,
            context_wrappers,
            noncontext_wrappers,
        ) = LilyPondFormatManager._collect_indicators(component)
        LilyPondFormatManager._populate_markup_format_contributions(
            component,
            bundle,
            up_markup_wrappers,
            down_markup_wrappers,
            neutral_markup_wrappers,
        )
        LilyPondFormatManager._populate_context_wrapper_format_contributions(
            component, bundle, context_wrappers
        )
        LilyPondFormatManager._populate_noncontext_wrapper_format_contributions(
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
                format_pieces = _tag.tag(
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
    def _report_leaf_format_contributions(leaf):
        bundle = LilyPondFormatManager.bundle_format_contributions(leaf)
        report = ""
        report += 'slot "absolute before":\n'
        packet = leaf._format_absolute_before_slot(bundle)
        report += leaf._process_contribution_packet(packet)
        report += 'slot "before":\n'
        packet = leaf._format_before_slot(bundle)
        report += leaf._process_contribution_packet(packet)
        report += 'slot "opening":\n'
        packet = leaf._format_opening_slot(bundle)
        report += leaf._process_contribution_packet(packet)
        report += 'slot "contents slot":\n'
        report += _bundle.LilyPondFormatBundle.indent + "leaf body:\n"
        string = leaf._format_contents_slot(bundle)[0][1][0]
        report += (2 * _bundle.LilyPondFormatBundle.indent) + string + "\n"
        report += 'slot "closing":\n'
        packet = leaf._format_closing_slot(bundle)
        report += leaf._process_contribution_packet(packet)
        report += 'slot "after":\n'
        packet = leaf._format_after_slot(bundle)
        report += leaf._process_contribution_packet(packet)
        report += 'slot "absolute after":\n'
        packet = leaf._format_absolute_after_slot(bundle)
        report += leaf._process_contribution_packet(packet)
        while report[-1] == "\n":
            report = report[:-1]
        return report

    ### PUBLIC METHODS ###

    # TODO: make top-level function
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
    def bundle_format_contributions(component) -> "_bundle.LilyPondFormatBundle":
        """
        Gets all format contributions for ``component``.
        """
        bundle = _bundle.LilyPondFormatBundle()
        LilyPondFormatManager._populate_indicator_format_contributions(
            component, bundle
        )
        LilyPondFormatManager._populate_context_setting_format_contributions(
            component, bundle
        )
        LilyPondFormatManager._populate_grob_override_format_contributions(
            component, bundle
        )
        LilyPondFormatManager._populate_grob_revert_format_contributions(
            component, bundle
        )
        bundle.sort_overrides()
        return bundle

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
            string_[tag_start:tag_start] = _bundle.LilyPondFormatBundle.indent
            string_ = "".join(string_)
            strings_.append(string_)
        text = "\n".join(strings_)
        if realign is not None:
            text = LilyPondFormatManager.align_tags(text, n=realign)
        return text
