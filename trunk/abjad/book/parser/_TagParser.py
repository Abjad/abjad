class _TagParser(object):

    def __init__(self, lines):
        self._close_tag = None
        self._open_tag = None
        self._target_open_tag = None
        self._target_close_tag = None
        self._input = lines
        self.output = [ ]

    def process(self):
        pass

    def _parse(self):
        pass

    def _verify_tag(self):
        '''Check for nested or incomplete tags.'''
        in_block = False
        error = SyntaxError('Mismatching %s %s tags found.' % (self._open_tag, self._close_tag))
        for line in self._input:
            if in_block:
                if self._open_tag in line:
                    raise error
                elif self._close_tag in line:
                    in_block = False
            else:
                if self._open_tag in line:
                    in_block = True
                elif self._close_tag in line:
                    raise error
