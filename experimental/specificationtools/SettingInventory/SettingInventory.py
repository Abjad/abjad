from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.specificationtools.AttributeNameEnumeration import AttributeNameEnumeration
from experimental.specificationtools.Setting import Setting


class SettingInventory(ObjectInventory):

    ### CLASS ATTRIBUTES ###

    attribute_names = AttributeNameEnumeration()

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _item_callable(self):
        return Setting

    ### PUBLIC METHODS ###

    def get_setting(self, 
        attribute_name=None, context_name=None, persistent=None, scope=None, segment_name=None):
        settings = self.get_settings(attribute_name=attribute_name, 
            context_name=context_name, persistent=persistent, scope=scope, segment_name=segment_name)
        if not settings:
            raise Exception(
                'no settings for {!r} found in segment {!r}.'.format(attribute_name, segment_name))
        elif 1 < len(settings):
            raise Exception(
                'multiple settings for {!r} found in segment {!r}.'.format(attribute_name, segment_name))
        assert len(settings) == 1
        return settings[0]

    def get_settings(self, attribute_name=None, context_name=None, persistent=None, scope=None, target=None):
        assert attribute_name in self.attribute_names, repr(attribute_name)
        settings = []
        for setting in self:
            if (
                (attribute_name is None or setting.attribute_name == attribute_name) and
                (target is None or setting.target == target) and
                (context_name is None or setting.target.context_name == context_name) and
                (scope is None or setting.target.scope == scope) and
                (persistent is None or setting.persistent == persistent)
                ):
                settings.append(setting)
        return settings
