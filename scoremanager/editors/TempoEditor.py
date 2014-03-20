# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import durationtools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class TempoEditor(Editor):
    r'''Tempo editor.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from scoremanager.editors import TargetManifest
        return TargetManifest(
            indicatortools.Tempo,
            ('duration', 'd', getters.get_duration),
            ('units_per_minute', 'pm', getters.get_integer),
            )
