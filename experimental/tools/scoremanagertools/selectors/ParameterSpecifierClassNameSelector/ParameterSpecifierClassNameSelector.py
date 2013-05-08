from experimental.tools.scoremanagertools.selectors.Selector import Selector
import os


class ParameterSpecifierClassNameSelector(Selector):

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        forbidden_directory_entries = (
            'MusicSpecifier',
            'MusicContributionSpecifier',
            'ParameterSpecifier',
            'Specifier',
            )
        for name in os.listdir(self.configuration.system_specifier_classes_directory_path):
            if name.endswith('Specifier'):
                if not name in forbidden_directory_entries:
                    result.append(name)
        return result
