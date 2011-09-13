from abjad import *
from abjad.tools.contexttools._Context import _Context
import py.test


def test_Context___cmp___01():
    '''Compare context to itself.
    '''

    context = _Context([])

    assert context == context
    assert not context != context

    comparison_string = 'context <  context'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'context <= context'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'context >  context'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'context >= context'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Context___cmp___02():
    '''Compare contexts.
    '''

    context_1 = _Context([])
    context_2 = _Context([])

    assert not context_1 == context_2
    assert      context_1 != context_2

    comparison_string = 'context_1 <  context_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'context_1 <= context_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'context_1 >  context_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'context_1 >= context_2'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Context___cmp___03():
    '''Compare context to foreign type.
    '''

    context = _Context([])

    assert not context == 'foo'
    assert      context != 'foo'

    comparison_string = "context <  'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "context <= 'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "context >  'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "context >= 'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
