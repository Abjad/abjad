from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.specificationtools.AttributeNameEnumeration import AttributeNameEnumeration
from experimental.settingtools.SingleContextSetting import SingleContextSetting


class ContextSettingInventory(ObjectInventory):
    r'''.. versionadded:: 1.0

    Context setting inventory.
    '''

    ### CLASS ATTRIBUTES ###

    attributes = AttributeNameEnumeration()

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _item_callable(self):
        return SingleContextSetting

    ### PUBLIC METHODS ###

    def get_setting(self, 
        attribute=None, context_name=None, persistent=None, timespan=None, segment_name=None):
        settings = self.get_settings(attribute=attribute, 
            context_name=context_name, persistent=persistent, timespan=timespan, segment_name=segment_name)
        if not settings:
            raise Exception(
                'no settings for {!r} found in segment {!r}.'.format(attribute, segment_name))
        elif 1 < len(settings):
            raise Exception(
                'multiple settings for {!r} found in segment {!r}.'.format(attribute, segment_name))
        assert len(settings) == 1
        return settings[0]

    def get_settings(self, attribute=None, context_name=None, persistent=None, timespan=None, target=None):
        assert attribute in self.attributes, repr(attribute)
        settings = []
        for setting in self:
            if (
                (attribute is None or setting.attribute == attribute) and
                (target is None or setting.target == target) and
                (context_name is None or setting.target.context_name == context_name) and
                (timespan is None or setting.target.timespan == timespan) and
                (persistent is None or setting.persistent == persistent)
                ):
                settings.append(setting)
        return settings
