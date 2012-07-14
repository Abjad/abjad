from experimental.specificationtools.exceptions import *
from abjad.tools.abctools.AbjadObject import AbjadObject
from collections import OrderedDict


class ContextProxy(AbjadObject, OrderedDict):

    ### INITIALIZER ###

    def __init__(self):
        OrderedDict.__init__(self)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return OrderedDict.__repr__(self)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _mandatory_argument_values(self):
        return self.items()

    ### PUBLIC METHODS ###

    def get_setting(self, attribute=None):
        settings = self.get_settings(attribute=attribute)
        if not settings:
            raise MissingContextSettingError('no settings for {!r} found.'.format(attribute))
        elif 1 < len(settings):
            raise ExtraContextSettingError('multiple settings for {!r} found.'.format(attribute))
        assert len(settings) == 1
        return settings[0]

    def get_settings(self, attribute=None):
        result = []
        for key, value in self.iteritems():
            if attribute is None or key == attribute:
                # CURRENT: toggle between these two values while implementing count ratio selectors
                #          First line is for last known good behavior.
                #          Second line is for newly improved behavior.
                result.append(value)
                #result.extend(value)
        return result
