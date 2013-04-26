from experimental.tools.scoremanagertools.selectors.Selector import Selector
import os


class ParameterEditorClassNameSelector(Selector):

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        forbidden_names = (
            'MusicSpecifierEditor',
            'MusicContributionSpecifierEditor',
            'ParameterSpecifierEditor',
            )
        for name in os.listdir(self.configuration.EDITORS_DIRECTORY_PATH):
            if name.endswith('SpecifierEditor'):
                if not name in forbidden_names:
                    result.append(name)
        return result
