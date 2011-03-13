import threading

from labcoat import attributes, methods


store = threading.local()

class Specimen:
    def __init__(self, cls, *args, **kwargs):
        self.__dict__['class'] = cls
        self.__dict__['args'] = args
        self.__dict__['kwargs'] = kwargs
        self.__dict__['steps'] = []
        self.__dict__['instance'] = cls(*args, **kwargs)

    def __getattr__(self, name):
        def method(*args, **kwargs):
            func = lambda obj: getattr(obj, name)(*args, **kwargs)
            self.__dict__['steps'].append(func)
            func(self.__dict__['instance'])
        return method

    def __setattr__(self, name, value):
        func = lambda obj: setattr(obj, name, value)
        self.__dict__['steps'].append(func)
        func(self.__dict__['instance'])

    def __setitem__(self, name, value):
        func = lambda obj: obj.__setitem__(name, value)
        self.__dict__['steps'].append(func)
        func(self.__dict__['instance'])

    def __enter__(self):
        store.results = []
        return Context(self)

    def __exit__(self, type, value, traceback):
        for success, display, data in store.results:
            print('%s %s' % (success and '.' or 'F', display % data))


class Context:
    def __init__(self, specimen):
        instance = specimen.__dict__['class'](*specimen.__dict__['args'],
                                              **specimen.__dict__['kwargs'])
        # Initialize the specimen
        for func in specimen.__dict__['steps']:
            func(instance)

        self.specimen = specimen
        self.instance = instance
        self.results = store.results

    # Attribute tests

    @property
    def s(self):
        return attributes.S(self)

    @property
    def has(self):
        return attributes.Has(self)

    @property
    def lacks(self):
        return attributes.Lacks(self)

    # Method tests

    @property
    def please(self):
        return methods.Please(self)

    @property
    def can(self):
        return methods.Can(self)

    @property
    def cannot(self):
        return methods.Cannot(self)

