
class Statement(object):

    def __init__(self, text=None, code=[ ]):
        self.text = text or ' '
        self.code = code

    ### PUBLIC ATTRIBUTES ###

    @apply
    def text( ):
        def fget(self):
            return self._text
        def fset(self, arg):
            if not isinstance(arg, basestring):
                raise TypeError('must be string: "%s".' % arg)
            self._text = arg
        return property(**locals( ))

    @apply
    def code( ):
        def fget(self):
            return self._code
        def fset(self, arg):
            if isinstance(arg, basestring):
                self._code = [arg]
            elif isinstance(arg, (list, tuple)):
                self._code = arg
            else:
                raise TypeError('must be a list or a tuple of executable strings: "%s".' % arg)
        return property(**locals( ))
