from experimental.tools.scoremanagertools.selectors.Selector import Selector
import os


class ParameterEditorClassNameSelector(Selector):

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        forbidden_directory_content_names = (
            'MusicSpecifierEditor',
            'MusicContributionSpecifierEditor',
            'ParameterSpecifierEditor',
            )
        for name in os.listdir(self.configuration.editors_directory_path):
            if name.endswith('SpecifierEditor'):
                if not name in forbidden_directory_content_names:
                    result.append(name)
        return result
