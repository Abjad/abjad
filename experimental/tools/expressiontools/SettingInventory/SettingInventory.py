from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.tools.expressiontools.AttributeNameEnumeration import AttributeNameEnumeration


class SettingInventory(ObjectInventory):
    r'''Single inventory.
    '''

    ### CLASS ATTRIBUTES ###

    attributes = AttributeNameEnumeration()

    ### PUBLIC METHODS ###

    def get_setting(self, attribute=None, context_name=None, persist=None, timespan=None, segment_name=None):
        settings = self.get_settings(attribute=attribute, 
            context_name=context_name, persist=persist, timespan=timespan, segment_name=segment_name)
        if not settings:
            error ='no settings for {!r} found in segment {!r}.'.format(attribute, segment_name)
            raise Exception(error)
        elif 1 < len(settings):
            error = 'multiple settings for {!r} found in segment {!r}.'.format(attribute, segment_name)
            raise Exception(error)
        assert len(settings) == 1
        return settings[0]

    def get_settings(self, attribute=None, context_name=None, persist=None, timespan=None, target=None):
        assert attribute in self.attributes, repr(attribute)
        settings = []
        for setting in self:
            if (
                (attribute is None or setting.attribute == attribute) and
                (target is None or setting.target == target) and
                (context_name is None or setting.target.context_name == context_name) and
                (timespan is None or setting.target.timespan == timespan) and
                (persist is None or setting.persist == persist)
                ):
                settings.append(setting)
        return settings
