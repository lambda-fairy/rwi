class MessageError(ValueError):
    """An exception raised while trying to parse an invalid message.

    **Note**: this is only raised while *parsing* messages, not
    serializing them. When you receive an invalid message, it's okay to
    ignore it and keep going. But if you try to *send* an invalid
    message, that's different -- it means there's a bug in your program.
    So in the former case we use MessageError, and in the latter we
    simply rethrow whatever comes up.
    """
    pass
