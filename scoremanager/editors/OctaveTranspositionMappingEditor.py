# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from scoremanager import getters
from scoremanager.editors.ListEditor import ListEditor


class OctaveTranspositionMappingEditor(ListEditor):
    r'''OctaveTranspositionMapping editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        superclass = super(OctaveTranspositionMappingEditor, self)
        superclass.__init__(session=session, target=target)
        # TODO: derive from self._tagte_manifest?
        self._item_class = pitchtools.OctaveTranspositionMappingComponent
        # TODO: derive from self._item_class
        self._item_identifier = 'octave transposition mapping component'

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from abjad.tools import systemtools
        return systemtools.AttributeManifest(
            pitchtools.OctaveTranspositionMapping,
            target_name_attribute='name',
            )