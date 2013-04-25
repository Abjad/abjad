from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.tools.scoremanagertools.editors.InteractiveEditor import InteractiveEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagertools import getters


class TempoMarkEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(contexttools.TempoMark,
        ('duration', 'd', getters.get_duration),
        ('units_per_minute', 'm', getters.get_integer),
        )
