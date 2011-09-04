from abjad.tools import durationtools
from abjad.tools.containertools.Container._ContainerFormatterSlotsInterface import _ContainerFormatterSlotsInterface


class _TupletFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

    def __init__(self, _client):
        _ContainerFormatterSlotsInterface.__init__(self, _client)

    ### PUBLIC ATTRIBUTES ###

    @property
    def slot_1(self):
        from abjad.tools.marktools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
        from abjad.core.LilyPondGrobOverrideComponentPlugIn._get_grob_override_format_contributions import _get_grob_override_format_contributions
        from abjad.core.LilyPondGrobOverrideComponentPlugIn._get_grob_revert_format_contributions import _get_grob_revert_format_contributions
        from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot
        result = []
        tuplet = self.formatter.tuplet
        result.append(_get_comment_format_contributions_for_slot(tuplet, 'before'))
        result.append(_get_lilypond_command_mark_format_contributions_for_slot(tuplet, 'before'))
        result.append(_get_grob_override_format_contributions(self._client._client))
        return tuple(result)

    @property
    def slot_2(self):
        result = []
        formatter = self.formatter
        tuplet = formatter.tuplet
        if tuplet.multiplier:
            if tuplet.is_invisible:
                multiplier = tuplet.multiplier
                n, d = multiplier.numerator, multiplier.denominator
                contributor = (tuplet, 'is_invisible')
                contributions = [r"\scaleDurations #'(%s . %s) {" % (n, d)]
                result.append([contributor, contributions])
            else:
                contributor = ('tuplet_brackets', 'open')
                if tuplet.multiplier != 1:
                    contributions = [r'%s\times %s %s' % (
                        formatter._fraction,
                        tuplet._multiplier_fraction_string,
                        '{'
                        )]
                else:
                    contributions = ['{']
                result.append([contributor, contributions])
        return tuple(result)

    @property
    def slot_3(self):
        '''Read-only tuple of format contributions to appear immediately after tuplet opening.
        '''
        from abjad.tools.marktools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
        from abjad.core.LilyPondGrobOverrideComponentPlugIn._get_grob_override_format_contributions import _get_grob_override_format_contributions
        from abjad.core.LilyPondGrobOverrideComponentPlugIn._get_grob_revert_format_contributions import _get_grob_revert_format_contributions
        from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot
        result = []
        tuplet = self.formatter.tuplet
        result.append(_get_comment_format_contributions_for_slot(tuplet, 'opening'))
        result.append(_get_lilypond_command_mark_format_contributions_for_slot(tuplet, 'opening'))
        self._indent_slot_contributions(result)
        return tuple(result)

    @property
    def slot_5(self):
        '''Read-only tuple of format contributions to appear immediately before tuplet closing.
        '''
        from abjad.tools.marktools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
        from abjad.core.LilyPondGrobOverrideComponentPlugIn._get_grob_override_format_contributions import _get_grob_override_format_contributions
        from abjad.core.LilyPondGrobOverrideComponentPlugIn._get_grob_revert_format_contributions import _get_grob_revert_format_contributions
        from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot
        result = []
        tuplet = self.formatter.tuplet
        result.append(_get_lilypond_command_mark_format_contributions_for_slot(tuplet, 'closing'))
        result.append(_get_comment_format_contributions_for_slot(tuplet, 'closing'))
        self._indent_slot_contributions(result)
        return tuple(result)

    @property
    def slot_6(self):
        '''Read-only tuplet of format contributions used to generate tuplet closing.
        '''
        result = []
        tuplet = self.formatter.tuplet
        if tuplet.multiplier:
            result.append([('tuplet_brackets', 'close'), '}'])
        return tuple(result)

    @property
    def slot_7(self):
        '''Read-only tuple of format contributions to appear immediately after tuplet closing.
        '''
        from abjad.tools.marktools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
        from abjad.core.LilyPondGrobOverrideComponentPlugIn._get_grob_override_format_contributions import _get_grob_override_format_contributions
        from abjad.core.LilyPondGrobOverrideComponentPlugIn._get_grob_revert_format_contributions import _get_grob_revert_format_contributions
        from abjad.tools.marktools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot
        result = []
        tuplet = self.formatter.tuplet
        result.append(_get_lilypond_command_mark_format_contributions_for_slot(tuplet, 'after'))
        result.append(_get_grob_revert_format_contributions(self._client._client))
        result.append(_get_comment_format_contributions_for_slot(tuplet, 'after'))
        return tuple(result)
