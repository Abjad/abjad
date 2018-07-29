import abjad


def test_TypedOrderedDict_01():
    """
    Implements __contains__().
    """

    dictionary = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert 'soprano' in dictionary
    assert 'treble' not in dictionary
    assert [_ for _ in dictionary] == ['soprano', 'alto', 'tenor', 'bass']


def test_TypedOrderedDict_02():
    """
    Implements __delitem__().
    """

    dictionary_1 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'
    del(dictionary_1['soprano'])

    dictionary_2 = abjad.OrderedDict(item_class=abjad.Clef)
    assert dictionary_1 == dictionary_2


def test_TypedOrderedDict_03():
    """
    Implements __eq__().
    """

    dictionary_1 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'

    dictionary_2 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_2['soprano'] = 'treble'

    dictionary_3 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_3['bass'] = 'bass'

    assert dictionary_1 == dictionary_1
    assert dictionary_1 == dictionary_2
    assert not dictionary_1 == dictionary_3
    assert dictionary_2 == dictionary_1
    assert dictionary_2 == dictionary_2
    assert not dictionary_2 == dictionary_3
    assert not dictionary_3 == dictionary_1
    assert not dictionary_3 == dictionary_2
    assert dictionary_3 == dictionary_3


def test_TypedOrderedDict_04():
    """
    Implements __format__().
    """

    dictionary_1 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'
    dictionary_1['tenor'] = 'tenor'
    dictionary_1['bass'] = 'bass'

    assert format(dictionary_1) == abjad.String.normalize(
        """
        abjad.OrderedDict(
            [
                (
                    'soprano',
                    abjad.Clef('treble'),
                    ),
                (
                    'alto',
                    abjad.Clef('alto'),
                    ),
                (
                    'tenor',
                    abjad.Clef('tenor'),
                    ),
                (
                    'bass',
                    abjad.Clef('bass'),
                    ),
                ],
            item_class=abjad.Clef,
            )
        """
        )

    globs = abjad.__dict__.copy()
    globs['abjad'] = abjad
    dictionary_2 = eval(format(dictionary_1), globs)
    assert dictionary_1 == dictionary_2


def test_TypedOrderedDict_05():
    """
    Initializes from dictionary items.
    """

    items = [
        ('soprano', abjad.Clef('treble')),
        ('alto', abjad.Clef('alto')),
        ('tenor', abjad.Clef('tenor')),
        ('bass', abjad.Clef('bass')),
        ]
    dictionary_1 = abjad.OrderedDict(
        item_class=abjad.Clef,
        items=items,
        )

    dictionary_2 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_2['soprano'] = 'treble'
    dictionary_2['alto'] = 'alto'
    dictionary_2['tenor'] = 'tenor'
    dictionary_2['bass'] = 'bass'

    assert dictionary_1 == dictionary_2


def test_TypedOrderedDict_06():
    """
    Implements __len__().
    """

    dictionary = abjad.OrderedDict(item_class=abjad.Clef)
    assert len(dictionary) == 0

    dictionary = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary['soprano'] = 'treble'
    assert len(dictionary) == 1


def test_TypedOrderedDict_07():

    dictionary_1 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'

    dictionary_2 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_2['soprano'] = 'treble'

    dictionary_3 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_3['bass'] = 'bass'

    assert not dictionary_1 != dictionary_1
    assert not dictionary_1 != dictionary_2
    assert dictionary_1 != dictionary_3
    assert not dictionary_2 != dictionary_1
    assert not dictionary_2 != dictionary_2
    assert dictionary_2 != dictionary_3
    assert dictionary_3 != dictionary_1
    assert dictionary_3 != dictionary_2
    assert not dictionary_3 != dictionary_3


def test_TypedOrderedDict_08():
    """
    Implements __reversed__().
    """

    dictionary = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    generator = reversed(dictionary)
    assert [_ for _ in generator] == ['bass', 'tenor', 'alto', 'soprano']


def test_TypedOrderedDict_09():
    """
    Implements clear().
    """

    dictionary_1 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'
    dictionary_1['tenor'] = 'tenor'
    dictionary_1['bass'] = 'bass'
    dictionary_1.clear()

    dictionary_2 = abjad.OrderedDict(item_class=abjad.Clef)
    assert dictionary_1 == dictionary_2


def test_TypedOrderedDict_10():
    """
    Implements copy().
    """

    dictionary_1 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'
    dictionary_1['tenor'] = 'tenor'
    dictionary_1['bass'] = 'bass'

    dictionary_2 = dictionary_1.copy()
    assert dictionary_1 == dictionary_2


def test_TypedOrderedDict_11():
    """
    Implements get().
    """

    dictionary = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert dictionary.get('soprano') == abjad.Clef('treble')
    assert dictionary.get('foo') is None
    assert dictionary.get('foo', 'bar') == 'bar'


def test_TypedOrderedDict_12():
    """
    Implements has_key().
    """

    dictionary = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert dictionary.has_key('soprano')
    assert not dictionary.has_key('treble')
    assert not dictionary.has_key('foo')


def test_TypedOrderedDict_13():
    """
    Implements items().
    """

    dictionary = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert list(dictionary.items()) == [
        ('soprano', abjad.Clef('treble')),
        ('alto', abjad.Clef('alto')),
        ('tenor', abjad.Clef('tenor')),
        ('bass', abjad.Clef('bass')),
        ]


def test_TypedOrderedDict_14():
    """
    Implements keys().
    """

    dictionary = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert list(dictionary.keys()) == ['soprano', 'alto', 'tenor', 'bass']


def test_TypedOrderedDict_15():
    """
    Implements pop().
    """

    dictionary_1 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'
    dictionary_1['tenor'] = 'tenor'
    dictionary_1['bass'] = 'bass'

    dictionary_2 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_2['alto'] = 'alto'
    dictionary_2['tenor'] = 'tenor'
    dictionary_2['bass'] = 'bass'

    assert dictionary_1.pop('soprano') == abjad.Clef('treble')
    assert dictionary_1 == dictionary_2


#def test_TypedOrderedDict_16():
#    """
#    Implements popitem().
#    """
#
#    dictionary_1 = abjad.OrderedDict(item_class=Clef)
#    dictionary_1['soprano'] = 'treble'
#    dictionary_1['alto'] = 'alto'
#    dictionary_1['tenor'] = 'tenor'
#    dictionary_1['bass'] = 'bass'
#
#    dictionary_2 = abjad.OrderedDict(item_class=Clef)
#    dictionary_2['alto'] = 'alto'
#    dictionary_2['tenor'] = 'tenor'
#    dictionary_2['bass'] = 'bass'
#
#    item = dictionary_1.popitem('soprano')
#    assert item == ('soprano', abjad.Clef('treble'))
#    assert dictionary_1 == dictionary_2


def test_TypedOrderedDict_17():
    """
    Implements update().
    """

    dictionary_1 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'

    dictionary_2 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_2['tenor'] = 'tenor'
    dictionary_2['bass'] = 'bass'

    dictionary_3 = abjad.OrderedDict(item_class=abjad.Clef)
    dictionary_3['soprano'] = 'treble'
    dictionary_3['alto'] = 'alto'
    dictionary_3['tenor'] = 'tenor'
    dictionary_3['bass'] = 'bass'

    dictionary_1.update(dictionary_2)
    assert dictionary_1 == dictionary_3
