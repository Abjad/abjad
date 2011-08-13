class _Interface(object):

    __slots__ = ('_client')

    def __init__(self, client):
        self._client = client

    ### OVERLOADS ###

    def __repr__(self):
        return '<%s>' % self.__class__.__name__
