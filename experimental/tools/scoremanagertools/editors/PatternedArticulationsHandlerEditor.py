# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class PatternedArticulationsHandlerEditor(InteractiveEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return TargetManifest(
            handlertools.PatternedArticulationsHandler,
            ('articulation_lists', None, 'al', getters.get_lists, False),
            ('minimum_duration', None, 'nd', getters.get_duration, False),
            ('maximum_duration', None, 'xd', getters.get_duration, False),
            ('minimum_written_pitch', None, 'np', 
                getters.get_named_pitch, False),
            ('maximum_written_pitch', None, 'xp', 
                getters.get_named_pitch, False),
            )
