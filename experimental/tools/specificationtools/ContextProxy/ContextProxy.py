from collections import OrderedDict
from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextProxy(AbjadObject, OrderedDict):

    ### INITIALIZER ###

    # TODO: add public division_region_commands timespan inventory
    # TODO: add public division_region_expressions timespan inventory
    # TODO: add public rhythm_region_expressions timespan inventory
    def __init__(self):
        OrderedDict.__init__(self)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return OrderedDict.__repr__(self)

    def __setitem__(self, key, value):
        assert isinstance(key, str)
        OrderedDict.__setitem__(self, key, value)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _positional_argument_values(self):
        return self.items()

    ### PUBLIC METHODS ###

    def get_setting(self, attribute=None):
        settings = self.get_settings(attribute=attribute)
        if not settings:
            raise Exception('no settings for {!r} found.'.format(attribute))
        elif 1 < len(settings):
            raise Exception('multiple settings for {!r} found.'.format(attribute))
        assert len(settings) == 1
        return settings[0]

    # the if-clause can be removed once context proxies always store multiple settings per attribute
    def get_settings(self, attribute=None):
        result = []
        for key, value in self.iteritems():
            if attribute is None or key == attribute:
                if isinstance(value, list):
                    result.extend(value)
                else:
                    result.append(value)
        return result
