from collections import OrderedDict
from abjad.tools.abctools.AbjadObject import AbjadObject


# TODO: Change to *have a* settings OrderedDict rather than *being an* OrderedDict.
#       This will mean adding a 'settings' property.
class ContextProxy(AbjadObject, OrderedDict):

    ### INITIALIZER ###

    def __init__(self):
        from experimental.tools import expressiontools
        OrderedDict.__init__(self)
        self._division_payload_expressions = \
            expressiontools.TimespanScopedSingleContextSettingInventory()
        self._rhythm_payload_expressions = \
            expressiontools.TimespanScopedSingleContextSettingInventory()
        self._timespan_scoped_single_context_division_settings = \
            expressiontools.TimespanScopedSingleContextSettingInventory()
        self._timespan_scoped_single_context_rhythm_settings = \
            expressiontools.TimespanScopedSingleContextSettingInventory()
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
    def division_payload_expressions(self):
        '''Context proxy division payload expressions.

        Return inventory.
        '''
        return self._division_payload_expressions

    @property
    def rhythm_payload_expressions(self):
        '''Context proxy rhythm payload expressions.

        Return inventory.
        '''
        return self._rhythm_payload_expressions

    @property
    def timespan_scoped_single_context_division_settings(self):
        '''Context proxy timespan-scoped
        single-context division settings.

        Return inventory.
        '''
        return self._timespan_scoped_single_context_division_settings

    @property
    def timespan_scoped_single_context_rhythm_settings(self):
        '''Context proxy timespan-scoped
        single-context rhythm settings.

        Return inventory.
        '''
        return self._timespan_scoped_single_context_rhythm_settings

    @property
    def voice_division_list(self):
        '''Context proxy voice division list.

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

    def get_settings(self, attribute=None):
        result = []
        for key, value in self.iteritems():
            if attribute is None or key == attribute:
                result.extend(value)
        return result
