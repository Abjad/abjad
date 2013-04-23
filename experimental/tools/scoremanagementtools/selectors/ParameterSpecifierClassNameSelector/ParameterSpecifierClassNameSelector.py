from experimental.tools.scoremanagementtools.selectors.Selector import Selector
import os


class ParameterSpecifierClassNameSelector(Selector):

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        forbidden_names = (
            'MusicSpecifier',
            'MusicContributionSpecifier',
            'ParameterSpecifier',
            'Specifier',
            )
        for name in os.listdir(self.configuration.specifier_classes_package_path_name):
            if name.endswith('Specifier'):
                if not name in forbidden_names:
                    result.append(name)
        return result
