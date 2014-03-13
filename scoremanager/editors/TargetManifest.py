# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class TargetManifest(AbjadObject):
    r'''Target manifest.
    '''

    ### INITIALIZER ###

    def __init__(self, _target_class, *attribute_details, **kwargs):
        from scoremanager import editors
        self._target_class = _target_class
        self._attribute_details = []
        for attribute_detail in attribute_details:
            attribute_detail = editors.AttributeDetail(*attribute_detail)
            self.attribute_details.append(attribute_detail)
        self.target_name_attribute = kwargs.get('target_name_attribute')

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of target manifest.

        Returns string.
        '''
        parts = ', '.join([str(x) for x in self.attribute_details])
        return '{}({}, {})'.format(
            type(self).__name__, self._target_class.__name__, parts)

    ### PRIVATE METHODS ###

    def _menu_key_to_attribute_detail(self, menu_key):
        for attribute_detail in self.attribute_details:
            if attribute_detail.menu_key == menu_key:
                return attribute_detail

    def _menu_key_to_attribute_name(self, menu_key):
        attribute_detail = self._menu_key_to_attribute_detail(menu_key)
        if attribute_detail:
            return attribute_detail.name

    def _menu_key_to_editor(
        self, 
        menu_key, 
        prepopulated_value, 
        session=None, 
        **kwargs
        ):
        space_delimited_attribute_name = \
            self._menu_key_to_space_delimited_lowercase_attribute_name(menu_key)
        attribute_detail = self._menu_key_to_attribute_detail(menu_key)
        editor = attribute_detail._get_editor(
            space_delimited_attribute_name, 
            prepopulated_value, 
            session=session, 
            **kwargs
            )
        return editor

    def _menu_key_to_prepopulated_value(self, menu_key):
        attribute_name = self._menu_key_to_attribute_name(menu_key)
        return getattr(self.target, attribute_name, None)

    def _menu_key_to_space_delimited_lowercase_attribute_name(self, menu_key):
        attribute_detail = self._menu_key_to_attribute_detail(menu_key)
        if attribute_detail:
            return attribute_detail._space_delimited_lowercase_name

    def _to_retrievable_attribute_name(
        self, initializer_argument_name):
        for attribute_detail in self.attribute_details:
            if attribute_detail.name == initializer_argument_name:
                return attribute_detail.retrievable_name
        raise ValueError

    def _to_initializer_argument_names(
        self, retrievable_attribute_name):
        for attribute_detail in self.attribute_details:
            if attribute_detail.retrievable_name == retrievable_attribute_name:
                return attribute_detail.name
        raise ValueError

    ### PUBLIC PROPERTIES ###

    @property
    def attribute_details(self):
        r'''Gets attribute details of target manifest.

        Returns list.
        '''
        return self._attribute_details

    @property
    def attribute_menu_keys(self):
        r'''Gets attribute menu keys of target manifest.

        Returns list.
        '''
        result = []
        for attribute_detail in self.attribute_details:
            result.append(attribute_detail.menu_key)
        return result

    @property
    def attribute_names(self):
        r'''Gets attribute names of target manifest.

        Returns list.
        '''
        result = []
        for attribute_detail in self.attribute_details:
            result.append(attribute_detail.name)
        return result

    @property
    def format_pieces(self):
        r'''Gets format pieces of target manifest.

        Returns list.
        '''
        result = []
        result.append('{}({},'.format(
            type(self).__name__, self._target_class.__name__))
        for attribute_detail in self.attribute_details:
            result.append('\t{!r},'.format(attribute_detail))
        result.append('\t)')
        return result

    @property
    def keyword_attribute_names(self):
        r'''Gets keyword attribute names of target manifest.

        Returns list.
        '''
        result = []
        for attribute_detail in self.attribute_details:
            if not attribute_detail.is_positional:
                result.append(attribute_detail.name)
        return result

    @property
    def positional_initializer_argument_names(self):
        r'''Gets positional initializer argument names of target manifest.

        Returns list.
        '''
        result = []
        for attribute_detail in self.attribute_details:
            if attribute_detail.is_positional:
                result.append(attribute_detail.name)
        return result

    @property
    def positional_initializer_retrievable_attribute_names(self):
        r'''Gest positional initializer retrievable attribute names.

        Returns list.
        '''
        result = []
        for attribute_detail in self.attribute_details:
            if attribute_detail.is_positional:
                result.append(attribute_detail.retrievable_name)
        return result

    @property
    def space_delimited_lowercase_attribute_names(self):
        r'''Gets space delimited lowercase attribute names of target manifest.

        Returns list.
        '''
        result = []
        for attribute_detail in self.attribute_details:
            result.append(attribute_detail._space_delimited_lowercase_name)
        return result
