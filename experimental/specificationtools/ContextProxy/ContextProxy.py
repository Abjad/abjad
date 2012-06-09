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

    def get_setting(self, attribute_name=None, scope=None):
        settings = self.get_settings(attribute_name=attribute_name, scope=scope)
        if not settings:
            raise MissingSettingError('no settings for {!r} found.'.format(attribute_name))
        elif 1 < len(settings):
            raise ExtraSettingError('multiple settings for {!r} found.'.format(attribute_name))
        assert len(settings) == 1
        return settings[0]

    def get_settings(self, attribute_name=None, scope=None):
        settings = []
        for key, setting in self.iteritems():
            if ((attribute_name is None or key == attribute_name) and
                (scope is None or setting.scope == scope)
                ):
                settings.append(setting)
        return settings
