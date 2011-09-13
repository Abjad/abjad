from abjad.tools.containertools.Container._ContainerFormatterSlotsInterface import _ContainerFormatterSlotsInterface


class _ContextFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

    def __init__(self, client):
        _ContainerFormatterSlotsInterface.__init__(self, client)

    ### PUBLIC ATTRIBUTES ###

    @property
    def slot_2(self):
        from abjad.core.LilyPondGrobOverrideComponentPlugIn._get_grob_override_format_contributions import _get_grob_override_format_contributions
        from abjad.tools.contexttools._get_context_setting_format_contributions import _get_context_setting_format_contributions
        result = []
        formatter = self.formatter
        context = formatter.context
        if self._client._client.is_parallel:
            brackets_open = ['<<']
        else:
            brackets_open = ['{']
        engraver_removals = formatter._formatted_engraver_removals
        engraver_consists = formatter._formatted_engraver_consists
        overrides = _get_grob_override_format_contributions(self._client._client)
        overrides = overrides[1]
        settings = _get_context_setting_format_contributions(self._client._client)
        settings = settings[1]
        if engraver_removals or engraver_consists or overrides or settings:
            contributions = [formatter._invocation + r' \with {']
            result.append([('context_brackets', 'open'), contributions])
            contributions = ['\t' + x for x in engraver_removals]
            result.append([(formatter, 'engraver_removals'), contributions])
            contributions = ['\t' + x for x in engraver_consists]
            result.append([(formatter, 'engraver_consists'), contributions])
            contributions = ['\t' + x for x in overrides]
            result.append([('overrides', 'overrides'), contributions])
            contributions = ['\t' + x for x in settings]
            result.append([('settings', 'settings'), contributions])
            contributions = ['} %s' % brackets_open[0]]
            result.append([('context_brackets', 'open'), contributions])
        else:
            contributions = [formatter._invocation + ' %s' % brackets_open[0]]
            result.append([('context_brackets', 'open'), contributions])
        return tuple(result)

    @property
    def slot_3(self):
        from abjad.tools.marktools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
        from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot
        from abjad.tools.contexttools._get_context_mark_format_contributions_for_slot import _get_context_mark_format_contributions_for_slot
        result = []
        context = self.formatter.context
        result.append(_get_comment_format_contributions_for_slot(context, 'opening'))
        result.append(_get_context_mark_format_contributions_for_slot(context, 'opening'))
        result.append(_get_lilypond_command_mark_format_contributions_for_slot(context, 'opening'))
        self._indent_slot_contributions(result)
        return tuple(result)

    @property
    def slot_5(self):
        from abjad.tools.marktools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
        from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot
        from abjad.tools.contexttools._get_context_mark_format_contributions_for_slot import _get_context_mark_format_contributions_for_slot
        result = []
        context = self.formatter.context
        result.append(_get_context_mark_format_contributions_for_slot(context, 'closing'))
        result.append(_get_lilypond_command_mark_format_contributions_for_slot(context, 'closing'))
        result.append(_get_comment_format_contributions_for_slot(context, 'closing'))
        self._indent_slot_contributions(result)
        return tuple(result)
