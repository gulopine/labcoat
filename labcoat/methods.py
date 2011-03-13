from labcoat.attributes import AttributeTester


class Please(AttributeTester):
    def __getattr__(self, name):
        self.__dict__['name'] = name
        def func(*args, **kwargs):
            getattr(self.instance, name)(*args, **kwargs)
        return func


class MethodTester(AttributeTester):
    def __getattr__(self, name):
        self.__dict__['name'] = name
        def func(*args, **kwargs):
            from labcoat.specimen import Context
            args = tuple(arg.instance if isinstance(arg, Context) else arg for arg in args)
            kwargs = dict((kw, arg.instance if isinstance(arg, SpecimenContext) else arg) for (kw, arg) in kwargs.items())
            success = self.test(self.instance, name, args, kwargs)
            self.results.append((success, self.test.output, self.__dict__))
        return func


class Can(MethodTester):
    def test(self, instance, name, args, kwargs):
        if not hasattr(instance, name):
            return False

        try:
            getattr(instance, name)(*args, **kwargs)
        except Exception as e:
            self.exception = e
            return False

        return True
    test.output = 'can %(name)s'


class Cannot(MethodTester):
    def __getattr__(self, name):
        self.__dict__['name'] = name
        inner_func = super(Cannot, self).__getattr__(name)
        def func(*args, **kwargs):
            self.__dict__['result'] = None
            self.__dict__['exception'] = None

            inner_func(*args, **kwargs)

            return CannotResult(self.specimen, self.__dict__['result'], self.__dict__['exception'])
        return func

    def test(self, instance, name, args, kwargs):
        # Passing requires that the attribute exist and evaluate to True
        if not hasattr(instance, name):
            return True

        try:
            self.__dict__['result'] = getattr(instance, name)(*args, **kwargs)
        except Exception as e:
            self.__dict__['exception'] = e
            return True

        return False
    test.output = 'can not %(name)s'


class CannotResult:
    def __init__(self, specimen, result, exception):
        self.results = specimen.results
        self.result = result
        self.exception = exception

    def because(self, exception_type):
        self.__dict__['exception_type'] = exception_type
        self.__dict__['exception_name'] = exception_type.__name__
        success = self.test(self.exception, exception_type)
        self.results.append((success, self.test.output, self.__dict__))

    def test(self, exception, exception_type):
        return isinstance(exception, exception_type)
    test.output = 'because of %(exception_name)s'


