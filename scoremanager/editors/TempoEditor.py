# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import durationtools
from scoremanager import getters
from scoremanager.editors.InteractiveEditor \
    import InteractiveEditor


class TempoEditor(InteractiveEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            indicatortools.Tempo,
            ('duration', 'd', getters.get_duration),
            ('units_per_minute', 'm', getters.get_integer),
            )
