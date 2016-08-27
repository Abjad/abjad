# -*- coding: utf-8 -*-
import abjad
from abjad.tools.datastructuretools import TypedOrderedDict


def test_datastructuretools_TypedOrderedDict_01():
    r'''Implements __contains__().
    '''

    dictionary = TypedOrderedDict(item_class=abjad.Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert 'soprano' in dictionary
    assert 'treble' not in dictionary
    assert [_ for _ in dictionary] == ['soprano', 'alto', 'tenor', 'bass']


def test_datastructuretools_TypedOrderedDict_02():
    r'''Implements __delitem__().
    '''

    dictionary_1 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'
    del(dictionary_1['soprano'])

    dictionary_2 = TypedOrderedDict(item_class=abjad.Clef)
    assert dictionary_1 == dictionary_2


def test_datastructuretools_TypedOrderedDict_03():
    r'''Implements __eq__().
    '''

    dictionary_1 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'

    dictionary_2 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_2['soprano'] = 'treble'

    dictionary_3 = TypedOrderedDict(item_class=abjad.Clef)
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


def test_datastructuretools_TypedOrderedDict_04():
    r'''Implements __format__().
    '''

    dictionary_1 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'
    dictionary_1['tenor'] = 'tenor'
    dictionary_1['bass'] = 'bass'

    assert format(dictionary_1) == abjad.stringtools.normalize(
        r'''
        abjad.datastructuretools.TypedOrderedDict(
            [
                (
                    'soprano',
                    indicatortools.Clef(
                        name='treble',
                        ),
                    ),
                (
                    'alto',
                    indicatortools.Clef(
                        name='alto',
                        ),
                    ),
                (
                    'tenor',
                    indicatortools.Clef(
                        name='tenor',
                        ),
                    ),
                (
                    'bass',
                    indicatortools.Clef(
                        name='bass',
                        ),
                    ),
                ],
            item_class=indicatortools.Clef,
            )
        '''
        )

    globs = abjad.__dict__.copy()
    globs['abjad'] = abjad
    dictionary_2 = eval(format(dictionary_1), globs)
    assert dictionary_1 == dictionary_2


def test_datastructuretools_TypedOrderedDict_05():
    r'''Initializes from dictionary items.
    '''

    items = [
        ('soprano', abjad.Clef('treble')),
        ('alto', abjad.Clef('alto')),
        ('tenor', abjad.Clef('tenor')),
        ('bass', abjad.Clef('bass')),
        ]
    dictionary_1 = TypedOrderedDict(
        item_class=abjad.Clef,
        items=items,
        )

    dictionary_2 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_2['soprano'] = 'treble'
    dictionary_2['alto'] = 'alto'
    dictionary_2['tenor'] = 'tenor'
    dictionary_2['bass'] = 'bass'

    assert dictionary_1 == dictionary_2


def test_datastructuretools_TypedOrderedDict_06():
    r'''Implements __len__().
    '''

    dictionary = TypedOrderedDict(item_class=abjad.Clef)
    assert len(dictionary) == 0

    dictionary = TypedOrderedDict(item_class=abjad.Clef)
    dictionary['soprano'] = 'treble'
    assert len(dictionary) == 1


def test_TypedOrderedDict_07():
    r'''Implements __ne__().
    '''

    dictionary_1 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'

    dictionary_2 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_2['soprano'] = 'treble'

    dictionary_3 = TypedOrderedDict(item_class=abjad.Clef)
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


def test_datastructuretools_TypedOrderedDict_08():
    r'''Implements __reversed__().
    '''

    dictionary = TypedOrderedDict(item_class=abjad.Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    generator = reversed(dictionary)
    assert [_ for _ in generator] == ['bass', 'tenor', 'alto', 'soprano']


def test_TypedOrderedDict_09():
    r'''Implements clear().
    '''

    dictionary_1 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'
    dictionary_1['tenor'] = 'tenor'
    dictionary_1['bass'] = 'bass'
    dictionary_1.clear()

    dictionary_2 = TypedOrderedDict(item_class=abjad.Clef)
    assert dictionary_1 == dictionary_2


def test_TypedOrderedDict_10():
    r'''Implements copy().
    '''

    dictionary_1 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'
    dictionary_1['tenor'] = 'tenor'
    dictionary_1['bass'] = 'bass'

    dictionary_2 = dictionary_1.copy()
    assert dictionary_1 == dictionary_2


def test_TypedOrderedDict_11():
    r'''Implements get().
    '''

    dictionary = TypedOrderedDict(item_class=abjad.Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert dictionary.get('soprano') == abjad.Clef('treble')
    assert dictionary.get('foo') is None
    assert dictionary.get('foo', 'bar') == 'bar'


def test_TypedOrderedDict_12():
    r'''Implements has_key().
    '''

    dictionary = TypedOrderedDict(item_class=abjad.Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert dictionary.has_key('soprano')
    assert not dictionary.has_key('treble')
    assert not dictionary.has_key('foo')


def test_TypedOrderedDict_13():
    r'''Implements items().
    '''

    dictionary = TypedOrderedDict(item_class=abjad.Clef)
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
    r'''Implements keys().
    '''

    dictionary = TypedOrderedDict(item_class=abjad.Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert list(dictionary.keys()) == ['soprano', 'alto', 'tenor', 'bass']


def test_TypedOrderedDict_15():
    r'''Implements pop().
    '''

    dictionary_1 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'
    dictionary_1['tenor'] = 'tenor'
    dictionary_1['bass'] = 'bass'

    dictionary_2 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_2['alto'] = 'alto'
    dictionary_2['tenor'] = 'tenor'
    dictionary_2['bass'] = 'bass'

    assert dictionary_1.pop('soprano') == abjad.Clef('treble')
    assert dictionary_1 == dictionary_2


#def test_TypedOrderedDict_16():
#    r'''Implements popitem().
#    '''
#
#    dictionary_1 = TypedOrderedDict(item_class=Clef)
#    dictionary_1['soprano'] = 'treble'
#    dictionary_1['alto'] = 'alto'
#    dictionary_1['tenor'] = 'tenor'
#    dictionary_1['bass'] = 'bass'
#
#    dictionary_2 = TypedOrderedDict(item_class=Clef)
#    dictionary_2['alto'] = 'alto'
#    dictionary_2['tenor'] = 'tenor'
#    dictionary_2['bass'] = 'bass'
#
#    item = dictionary_1.popitem('soprano')
#    assert item == ('soprano', Clef('treble'))
#    assert dictionary_1 == dictionary_2


def test_TypedOrderedDict_17():
    r'''Implements update().
    '''

    dictionary_1 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'

    dictionary_2 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_2['tenor'] = 'tenor'
    dictionary_2['bass'] = 'bass'

    dictionary_3 = TypedOrderedDict(item_class=abjad.Clef)
    dictionary_3['soprano'] = 'treble'
    dictionary_3['alto'] = 'alto'
    dictionary_3['tenor'] = 'tenor'
    dictionary_3['bass'] = 'bass'

    dictionary_1.update(dictionary_2)
    assert dictionary_1 == dictionary_3
