from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.tools import helpertools


class SingleContextSettingInventory(ObjectInventory):
    r'''

    Single-context setting inventory.
    '''

    ### CLASS ATTRIBUTES ###

    attributes = helpertools.AttributeNameEnumeration()

    ### PUBLIC METHODS ###

    def get_setting(self, 
        attribute=None, context_name=None, persist=None, timespan=None, segment_name=None):
        settings = self.get_settings(attribute=attribute, 
            context_name=context_name, persist=persist, timespan=timespan, segment_name=segment_name)
        if not settings:
            raise Exception(
                'no settings for {!r} found in segment {!r}.'.format(attribute, segment_name))
        elif 1 < len(settings):
            raise Exception(
                'multiple settings for {!r} found in segment {!r}.'.format(attribute, segment_name))
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
