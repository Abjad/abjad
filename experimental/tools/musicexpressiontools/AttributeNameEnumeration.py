# -*- encoding: utf-8 -*-
import collections


class AttributeNameEnumeration(collections.OrderedDict):
    r'''Attribute name enumeration.

    The allowable attribute names known to the ``musicexpressiontools``
    classes:

    ::

        >>> attributes = musicexpressiontools.AttributeNameEnumeration()

    ::

        >>> for key, value in attributes.iteritems(): key, value
        ...
        ('articulations', 0)
        ('divisions', 1)
        ('pitch_classes', 2)
        ('registration', 3)
        ('rhythm', 4)
        ('time_signatures', 5)

    Attribute names are alphabetized.

    The integer constants serve only to fit the attribute names into
    dictionary form.

    The class will grow as more attributes are added to the system.
    '''

    ### CLASS ATTIRBUTES ###

    attributes = (
        'articulations',
        'divisions',
        'pitch_classes',
        'registration',
        'rhythm',
        'time_signatures',
        )

    ### INITIALIZER ###

    def __init__(self):
        collections.OrderedDict.__init__(self)
        for i, attribute in enumerate(sorted(self.attributes)):
            self[attribute] = i