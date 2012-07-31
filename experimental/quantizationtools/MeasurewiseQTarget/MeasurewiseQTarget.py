from experimental.quantizationtools.QTarget import QTarget
from experimental.quantizationtools.QTargetMeasure import QTargetMeasure


class MeasurewiseQTarget(QTarget):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def beats(self):
        return tuple([beat for beat in item.beats for item in self.items])

    @property
    def item_klass(self):
        return QTargetMeasure

    ### PRIVATE METHODS ###

    def _notate(self, grace_handler):
        pass
