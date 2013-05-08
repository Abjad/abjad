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
        for name in os.listdir(self.configuration.system_editors_directory_path):
            if name.endswith('SpecifierEditor'):
                if not name in forbidden_directory_entries:
                    result.append(name)
        return result
