from abjad import *
from abjad.tools.contexttools.Context import Context
import py.test


def test_Context___cmp___01():
    '''Compare context to itself.
    '''

    context = Context([])

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

    context_1 = Context([])
    context_2 = Context([])

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

    context = Context([])

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
