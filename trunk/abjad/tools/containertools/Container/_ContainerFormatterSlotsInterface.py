from abjad.tools.componenttools._Component._ComponentFormatterSlotsInterface import _ComponentFormatterSlotsInterface


class _ContainerFormatterSlotsInterface(_ComponentFormatterSlotsInterface):

    def __init__(self, client):
        _ComponentFormatterSlotsInterface.__init__(self, client)

    ### PRIVATE METHODS ###

    def _indent_slot_contributions(self, slot):
        for contributor, contributions in slot:
            if contributions:
                for i, contribution in enumerate(contributions):
                    contributions[i] = '\t' + contribution

    ### PUBLIC ATTRIBUTES ###

    @property
    def slot_1(self):
        from abjad.tools.marktools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
        from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot
        result = []
        container = self.formatter.container
        result.append(_get_comment_format_contributions_for_slot(container, 'before'))
        result.append(_get_lilypond_command_mark_format_contributions_for_slot(container, 'before'))
        return tuple(result)

    @property
    def slot_2(self):
        result = []
        if self._client._client.is_parallel:
            brackets_open = ['<<']
        else:
            brackets_open = ['{']
        result.append([('open brackets', ''), brackets_open])
        return tuple(result)

    @property
    def slot_3(self):
        from abjad.tools.marktools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
        from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot
        from abjad.core.LilyPondGrobOverrideComponentPlugIn._get_grob_override_format_contributions import _get_grob_override_format_contributions
        from abjad.tools.contexttools._get_context_setting_format_contributions import _get_context_setting_format_contributions
        result = []
        container = self.formatter.container
        result.append(_get_comment_format_contributions_for_slot(container, 'opening'))
        result.append(_get_lilypond_command_mark_format_contributions_for_slot(container, 'opening'))
        result.append(_get_grob_override_format_contributions(container))
        result.append(_get_context_setting_format_contributions(container))
        self._indent_slot_contributions(result)
        return tuple(result)

    @property
    def slot_4(self):
        result = []
        result.append(self.wrap(self.formatter, '_contents'))
        return tuple(result)

    @property
    def slot_5(self):
        from abjad.tools.marktools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
        from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot
        from abjad.core.LilyPondGrobOverrideComponentPlugIn._get_grob_revert_format_contributions import _get_grob_revert_format_contributions
        result = []
        container = self.formatter.container
        result.append(_get_grob_revert_format_contributions(container))
        result.append(_get_lilypond_command_mark_format_contributions_for_slot(container, 'closing'))
        result.append(_get_comment_format_contributions_for_slot(container, 'closing'))
        self._indent_slot_contributions(result)
        return tuple(result)

    @property
    def slot_6(self):
        result = []
        if self._client._client.is_parallel:
            brackets_close = ['>>']
        else:
            brackets_close = ['}']
        result.append([('close brackets', ''), brackets_close])
        return tuple(result)

    @property
    def slot_7(self):
        from abjad.tools.marktools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
        from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot
        result = []
        container = self.formatter.container
        result.append(_get_lilypond_command_mark_format_contributions_for_slot(container, 'after'))
        result.append(_get_comment_format_contributions_for_slot(container, 'after'))
        return tuple(result)
