from abjad.demos.presentation.presentation import *

def test_Presentation_01( ):
    '''
    A presentation must take at least three arguments:
    title, abstract and a list of statements.
    '''
    s = Statement('Hello', 'x = 3')
    t = Presentation('Title', 'Abstract', [s])
