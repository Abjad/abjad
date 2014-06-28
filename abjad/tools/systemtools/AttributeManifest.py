# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class AttributeManifest(AbjadObject):
    r'''Target manifest.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_attribute_details',
        )

    ### INITIALIZER ###

    def __init__(self, *attribute_details):
        from abjad.tools import systemtools
        self._attribute_details = []
        for attribute_detail in attribute_details:
            if not isinstance(attribute_detail, systemtools.AttributeDetail):
                attribute_detail = systemtools.AttributeDetail(
                    *attribute_detail)
            self.attribute_details.append(attribute_detail)

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        r'''Gets attribute detail from attribute manifest.

        Returns attribute detail.
        '''
        return self.attribute_details.__getitem__(expr)

    def __repr__(self):
        r'''Gets interpreter representation of target manifest.

        Returns string.
        '''
        parts = ', '.join([str(x) for x in self.attribute_details])
        result = '{}({})'
        result = result.format(type(self).__name__, parts)
        return result

    ### PRIVATE METHODS ###

    def _command_to_attribute_detail(self, command):
        for attribute_detail in self.attribute_details:
            if attribute_detail.command == command:
                return attribute_detail

    def _command_to_attribute_name(self, command):
        attribute_detail = self._command_to_attribute_detail(command)
        if attribute_detail:
            return attribute_detail.name

    def _command_to_prepopulated_value(self, command):
        attribute_name = self._command_to_attribute_name(command)
        return getattr(self.target, attribute_name, None)

    def _to_initializer_argument_names(self, retrievable_attribute_name):
        for attribute_detail in self.attribute_details:
            if attribute_detail.name == retrievable_attribute_name:
                return attribute_detail.name
        raise ValueError

    def _to_retrievable_attribute_name(self, initializer_argument_name):
        for attribute_detail in self.attribute_details:
            if attribute_detail.name == initializer_argument_name:
                return attribute_detail.name
        raise ValueError

    ### PUBLIC PROPERTIES ###

    @property
    def attribute_details(self):
        r'''Gets attribute details of target manifest.

        Returns list.
        '''
        return self._attribute_details