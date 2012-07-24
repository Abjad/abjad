from experimental.quantizationtools.QTarget import QTarget
from experimental.quantizationtools.QTargetBeat import QTargetBeat


class BeatwiseQTarget(QTarget): 

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def beats(self):
        return tuple(self.items)
    
    @property
    def item_klass(self):
        return QTargetBeat

