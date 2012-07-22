from experimental.interpretertools.UninterpretedDivisionToken import UninterpretedDivisionToken


class RegionDivisionToken(UninterpretedDivisionToken):
    r'''.. versionadded:: 1.0

    Durated period of time over which a division-maker will apply.

    How do region division tokens and (unqualified) division tokens differ?

    Region division tokens represent a more refined product of interpretation.

    (Unqualified) division tokens may or may not glue together to create region division tokens. 

    Region division tokens never glue together.

    Region division tokens represent an absolute command to create divisions over a given duration.
    '''

    pass
