from collections import OrderedDict
from abjad.tools.abctools.AbjadObject import AbjadObject


# TODO: do not inherit from OrderedDict; use custom class attributes instead
class ContextProxy(AbjadObject, OrderedDict):

    ### INITIALIZER ###

    # TODO: add public rhythm_region_products timespan inventory
    def __init__(self):
        from experimental.tools import settingtools
        OrderedDict.__init__(self)
        self._division_region_commands = settingtools.RegionCommandInventory()
        self._division_region_products = settingtools.RegionCommandInventory()
        self._rhythm_region_commands = settingtools.RegionCommandInventory()
        self._rhythm_region_products = settingtools.RegionCommandInventory()
        self._voice_division_list = None

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

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def division_region_commands(self):
        '''Context proxy division region commands.

        Return region command inventory.
        '''
        return self._division_region_commands

    @property
    def division_region_products(self):
        '''Context proxy division region products.

        Return region product inventory.
        '''
        return self._division_region_products

    @property
    def rhythm_region_commands(self):
        '''Context proxy rhythm region commands.

        Return region command inventory.
        '''
        return self._rhythm_region_commands

    @property
    def rhythm_region_products(self):
        '''Context proxy rhythm region products.

        Return region product inventory.
        '''
        return self._rhythm_region_products

    @property
    def voice_division_list(self):
        '''Context proxy voice divisionlist.

        Return voice division list.
        '''
        return self._voice_division_list

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
