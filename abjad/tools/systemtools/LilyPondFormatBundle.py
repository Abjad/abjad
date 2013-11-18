# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LilyPondFormatBundle(AbjadObject):
    r'''LilyPond format bundle.

    Transient class created to hold the collection of all
    format contributions generated on behalf of a single component.
    '''

    ### CLASS VARIABLES ###

#    __slots__ = (
#        
#        )
    
    ### INITIALIZER ###

    def __init__(self):
        self._before = {}
        self._after = {}
        self._opening = {}
        self._closing = {}
        self._right = {}
        self._context_settings = []
        self._grob_overrides = []
        self._grob_reverts = []

    ### PUBLIC PROPERTIES ###

    @property
    def before(self):
        return self._before

    @property
    def after(self):
        return self._after

    @property
    def opening(self):
        return self._opening

    @property
    def closing(self):
        return self._closing

    @property
    def right(self):
        return self._right

    @property
    def grob_overrides(self):
        return self._grob_overrides

    @property
    def grob_reverts(self):
        return self._grob_reverts

    @property
    def context_settings(self):
        return self._context_settings
