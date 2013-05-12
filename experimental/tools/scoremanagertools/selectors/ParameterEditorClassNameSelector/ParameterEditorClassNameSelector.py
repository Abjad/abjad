import os
from experimental.tools.scoremanagertools.selectors.Selector import Selector


class ParameterEditorClassNameSelector(Selector):

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        forbidden_directory_entries = (
            'MusicSpecifierEditor',
            'MusicContributionSpecifierEditor',
            'ParameterSpecifierEditor',
            )
        for directory_entry in os.listdir(self.configuration.built_in_editors_directory_path):
            if directory_entry.endswith('SpecifierEditor'):
                if not directory_entry in forbidden_directory_entries:
                    result.append(directory_entry)
        return result
