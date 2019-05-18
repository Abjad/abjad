class LilyPondEvent(object):
    """
    Model of an arbitrary event in LilyPond.

    Not composer-safe.

    Used internally by LilyPondParser.
    """

    ### INITIALIZER ###

    def __init__(self, name=None, **keywords):
        self.name = name
        for k, v in keywords.items():
            if k != "name":
                setattr(self, k, v)

    ### SPECIAL METHODS ###

    def __str__(self):
        """
        Gets string representation of LilyPond event.

        Returns string.
        """
        result = repr(self.name)
        for key in self.__dict__:
            if key == "name":
                continue
            result += f", {key} = {getattr(self, key)!r}"
        return result

    def __repr__(self):
        """
        Gets interpreter representation of LilyPond event.

        Returns string.
        """
        name = type(self).__name__
        return f"{name}({str(self)})"
