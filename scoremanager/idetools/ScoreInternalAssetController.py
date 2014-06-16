# -*- encoding: utf-8 -*-
from scoremanager.idetools.AssetController import AssetController


class ScoreInternalAssetController(AssetController):
    r'''Score-internal asset controller.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_method(self):
        superclass = super(ScoreInternalAssetController, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            '<<': self.go_to_previous_score,
            '>>': self.go_to_next_score,
            #
            'd': self.go_to_distribution_files,
            'g': self.go_to_segments,
            'k': self.go_to_maker_files,
            'm': self.go_to_materials,
            'u': self.go_to_build_files,
            'y': self.go_to_stylesheets,
            #
            'sse': self.edit_score_stylesheet,
            })
        return result