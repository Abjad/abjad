from collections import OrderedDict


class AttributeNameEnumeration(OrderedDict):

    ### CLASS ATTIRBUTES ###

    attribute_names = (
        'articulations',
        'divisions', 
        'pitch_classes',
        'rhythm',
        'time_signatures',
        )

    ### INITIALIZER ###

    def __init__(self):
        OrderedDict.__init__(self)
        for i, attribute_name in enumerate(sorted(self.attribute_names)):
            self[attribute_name] = i
