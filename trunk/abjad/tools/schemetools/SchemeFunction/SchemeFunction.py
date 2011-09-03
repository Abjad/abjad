from abjad.core import _Immutable
from abjad.core import _StrictComparator


class SchemeFunction(_StrictComparator, _Immutable):
    '''Abjad model of Scheme function::

        abjad> schemetools.SchemeFunction('magstep', -3)
        SchemeFunction('magstep', -3)

    Scheme functions are immutable.
    '''

    def __new__(klass, *args):
        self = object.__new__(klass)
        object.__setattr__(self, 'name', args[0])
        if 1 < len(args):
            object.__setattr__(self, 'args', args[1:])
        else:
            object.__setattr__(self, 'args', [])
        return self

    def __getnewargs__(self):
        newargs = [self.name]
        newargs.extend(self.args)
        return tuple(newargs)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._repr_contents_string)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _repr_contents_string(self):
        result = []
        result.append('%r' % self.name)
        result.extend(self.args)
        result = ', '.join(str(x) for x in result)
        return result

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''LilyPond input format of Scheme function::

            abjad> scheme_function = schemetools.SchemeFunction('magstep', -3)
            abjad> scheme_function.format
            '#(magstep -3)'

        Return string.
        '''
        if len(self.args) == 0:
            body = self.name
        elif len(self.args) == 1:
            if isinstance(self.args[0], (int, float, long)):
                body = "(%s %s)" % (self.name, self.args[0])
            elif isinstance(self.args[0], str):
                body = "(%s '%s)" % (self.name, self.args[0])
            else:
                raise ValueError
        # TODO: Generalize for many arguments + parsing #
        else:
            raise NotImplementedError('multiple scheme arguments not yet implemented.')
        return '#' + body
