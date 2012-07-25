from collections import OrderedDict


class AttributeNameEnumeration(OrderedDict):
    r'''.. versionadded:: 1.0

    The allowable attribute names known to the ``specificationtools`` classes::

        >>> from experimental import specificationtools

    ::

        >>> attributes = helpertools.AttributeNameEnumeration()

    ::

        >>> for key, value in attributes.iteritems(): key, value
        ... 
        ('articulations', 0)
        ('divisions', 1)
        ('pitch_classes', 2)
        ('rhythm', 3)
        ('time_signatures', 4)

    Attribute names are alphabetized.

    The integer constants serve only to fit the attribute names into dictionary form.

    The class will grow as more attributes are added to the system.
    '''

    ### CLASS ATTIRBUTES ###

    attributes = (
        'articulations',
        'divisions', 
        'pitch_classes',
        'rhythm',
        'time_signatures',
        )

    ### INITIALIZER ###

    def __init__(self):
        OrderedDict.__init__(self)
        for i, attribute in enumerate(sorted(self.attributes)):
            self[attribute] = i
