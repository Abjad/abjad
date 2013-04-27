from experimental.tools.scoremanagertools.selectors.Selector import Selector
import os


class ParameterSpecifierClassNameSelector(Selector):

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        forbidden_directory_content_names = (
            'MusicSpecifier',
            'MusicContributionSpecifier',
            'ParameterSpecifier',
            'Specifier',
            )
        for name in os.listdir(self.configuration.SPECIFIER_CLASSES_DIRECTORY_PATH):
            if name.endswith('Specifier'):
                if not name in forbidden_directory_content_names:
                    result.append(name)
        return result
