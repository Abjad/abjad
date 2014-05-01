import sys


class Statement(object):

    def __init__(self, text=None, code=[ ]):
        self.text = text or ' '
        self.code = code

    ### PUBLIC PROPERTIES ###

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, arg):
        if sys.version_info[0] == 2:
            prototype = basestring
        else:
            prototype = str
        if isinstance(arg, prototype):
            self._code = [arg]
        elif isinstance(arg, (list, tuple)):
            self._code = arg
        else:
            raise TypeError('must be a list or a tuple of executable strings: "%s".' % arg)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, arg):
        if sys.version_info[0] == 2:
            prototype = basestring
        else:
            prototype = str
        if not isinstance(arg, prototype):
            raise TypeError('must be string: "%s".' % arg)
        self._text = arg
