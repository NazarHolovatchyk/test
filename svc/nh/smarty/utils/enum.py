
def enum(**enums):
    """
    A helper function for creating enum classes that are iterable
    Usage:
    MY_ENUM = enum(VALUE0 = 0, VALUE1 = 1, VALUE2 = 2)
    print MY_ENUM.VALUE0
    >> 0
    print 2 in MY_ENUM
    >> True
    print 3 in MY_ENUM
    >> False
    """

    cls = type('EnumClass', (), {})
    
    def __iter__(self):
        for _attr, val in enums.items():
            yield val

    cls.__iter__ = __iter__
    
    enum_object = cls()
    
    for attr, value in enums.items():
        setattr(enum_object, attr, value)
    return enum_object
