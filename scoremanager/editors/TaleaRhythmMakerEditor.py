# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class TaleaRhythmMakerEditor(Editor):
    r'''TaleaRhythmMaker editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        return systemtools.AttributeManifest(
            type(self),
            systemtools.AttributeDetail(
                name='extra_counts_per_division', 
                menu_key='ad', 
                editor_callable=getters.get_integers, 
                is_positional=False,
                ),
            systemtools.AttributeDetail(
                name='split_divisions_by_counts', 
                menu_key='sd', 
                editor_callable=getters.get_integers, 
                is_positional=False,
                ),
            systemtools.AttributeDetail(
                name='talea', 
                menu_key='ta', 
                editor_callable=getters.get_nonzero_integers, 
                is_positional=False,
                ),
            )

    ### PRIVATE METHODS ###

    def _get_target_summary_lines(self):
        result = []
        if self.target:
            result.append(self.target.__class__.__name__)
            result.append('')
            result.extend(Editor._target_summary_lines.fget(self))
        return result