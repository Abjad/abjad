from experimental.tools.scoremanagementtools.editors.AttributeDetail import AttributeDetail


class TargetManifest(object):

    ### INITIALIZER ###

    def __init__(self, target_class, *attribute_details, **kwargs):
        self.target_class = target_class
        self._attribute_details = []
        for attribute_detail in attribute_details:
            self.attribute_details.append(AttributeDetail(*attribute_detail))
        self.is_keyed = kwargs.get('is_keyed', False)
        self.target_name_attribute = kwargs.get('target_name_attribute')

    ### SPECIAL METHODS ###

    def __repr__(self):
        parts = ', '.join([str(x) for x in self.attribute_details])
        return '{}({}, {})'.format(type(self).__name__, self.target_class.__name__, parts)

    ### READ-ONLY PROPERTIES ###

    @property
    def attribute_details(self):
        return self._attribute_details

    @property
    def attribute_human_readable_names(self):
        result = []
        for attribute_detail in self.attribute_details:
            result.append(attribute_detail.human_readable_name)
        return result

    @property
    def attribute_menu_keys(self):
        result = []
        for attribute_detail in self.attribute_details:
            result.append(attribute_detail.menu_key)
        return result

    @property
    def attribute_names(self):
        result = []
        for attribute_detail in self.attribute_details:
            result.append(attribute_detail.name)
        return result

    @property
    def format(self):
        return '\n'.join(self.format_pieces)

    @property
    def format_pieces(self):
        result = []
        result.append('{}({},'.format(type(self).__name__, self.target_class.__name__))
        for attribute_detail in self.attribute_details:
            result.append('\t{!r},'.format(attribute_detail))
        result.append('\t)')
        return result

    @property
    def keyword_attribute_names(self):
        result = []
        for attribute_detail in self.attribute_details:
            if not attribute_detail.is_positional:
                result.append(attribute_detail.name)
        return result

    # TODO: deprecate and use two more specifier labels instead
#    @property
#    def positional_attribute_names(self):
#        result = []
#        for attribute_detail in self.attribute_details:
#            if attribute_detail.is_positional:
#                result.append(attribute_detail.name)
#        return result

    @property
    def positional_initializer_argument_names(self):
        result = []
        for attribute_detail in self.attribute_details:
            if attribute_detail.is_positional:
                result.append(attribute_detail.name)
        return result

    @property
    def positional_initializer_retrievable_attribute_names(self):
        result = []
        for attribute_detail in self.attribute_details:
            if attribute_detail.is_positional:
                result.append(attribute_detail.retrievable_name)
        return result

    ### PUBLIC METHODS ###

    def change_initializer_argument_name_to_retrievable_attribute_name(self, initializer_argument_name):
        for attribute_detail in self.attribute_details:
            if attribute_detail.name == initializer_argument_name:
                return attribute_detail.retrievable_name
        raise ValueError

    def change_retrievable_attribute_name_to_initializer_argument_name(self, retrievable_attribute_name):
        for attribute_detail in self.attribute_details:
            if attribute_detail.retrievable_name == retrievable_attribute_name:
                return attribute_detail.name
        raise ValueError

    def menu_key_to_attribute_detail(self, menu_key):
        for attribute_detail in self.attribute_details:
            if attribute_detail.menu_key == menu_key:
                return attribute_detail

    def menu_key_to_attribute_name(self, menu_key):
        attribute_detail = self.menu_key_to_attribute_detail(menu_key)
        if attribute_detail:
            return attribute_detail.name

    def menu_key_to_editor(self, menu_key, existing_value, session=None, **kwargs):
        attribute_spaced_name = self.menu_key_to_human_readable_attribute_name(menu_key)
        attribute_detail = self.menu_key_to_attribute_detail(menu_key)
        return attribute_detail.get_editor(attribute_spaced_name, existing_value, session=session, **kwargs)

    def menu_key_to_existing_value(self, menu_key):
        attribute_name = self.menu_key_to_attribute_name(menu_key)
        return getattr(self.target, attribute_name, None)

    def menu_key_to_human_readable_attribute_name(self, menu_key):
        attribute_detail = self.menu_key_to_attribute_detail(menu_key)
        if attribute_detail:
            return attribute_detail.human_readable_name
