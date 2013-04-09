from scftools.selectors.Selector import Selector
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
        for name in os.listdir(self.editors_package_path_name):
            if name.endswith('SpecifierEditor'):
                if not name in forbidden_names:
                    result.append(name)
        return result
