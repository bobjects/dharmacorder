# noinspection PyPep8Naming
class classproperty(property):
    # noinspection PyMethodOverriding
    def __get__(self, obj, type_):
        return self.fget.__get__(None, type_)()
