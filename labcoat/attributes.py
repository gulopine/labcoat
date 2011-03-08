class AttributeTester(object):
    def __init__(self, specimen):
        self.__dict__['specimen'] = specimen
        self.__dict__['instance'] = specimen.instance
        self.__dict__['results'] = specimen.results

    def __getattr__(self, name):
        self.__dict__['name'] = name
        result = self.test(self.__dict__['instance'], name)
        self.__dict__['results'].append((result, self.test.output, self.__dict__))


class S(AttributeTester):
    def __getattr__(self, name):
        self.__dict__['name'] = name
        return AttributeComparison(self, name)

    def __setattr__(self, name, value):
        self.__dict__['name'] = name
        setattr(self.instance, name, value)


class AttributeComparison:
    def __init__(self, specimen, name):
        self.instance = specimen.instance
        self.results = specimen.results
        self.name = name

    def test(self, func, other, display):
        value = getattr(self.instance, self.name)
        success = func(value, other)
        data = dict(self.__dict__, value=other)
        return (success, display, data)

    def __le__(self, other):
        self.results.append(self.test(lambda a, b: a <= b, other, '%s is at most %r'))

    def __lt__(self, other):
        self.results.append(self.test(lambda a, b: a < b, other, '%s is less than %r'))

    def __eq__(self, other):
        self.results.append(self.test(lambda a, b: a == b, other, '%s is equal to %r'))

    def __ne__(self, other):
        self.results.append(self.test(lambda a, b: a != b, other, '%s is different from %r'))

    def __gt__(self, other):
        self.results.append(self.test(lambda a, b: a > b, other, '%s is greater than %r'))

    def __ge__(self, other):
        self.results.append(self.test(lambda a, b: a >= b, other, '%s is at least %r'))


class Has(AttributeTester):
    def test(self, instance, name):
        # Passing requires that the attribute exist and evaluate to True
        return hasattr(instance, name) and bool(getattr(instance, name))
    test.output = 'has %(name)s'

    def __call__(self, num):
        return HasNum(self.specimen, num)


class HasNum(AttributeTester):
    def __init__(self, specimen, num, **kwargs):
        super(HasNum, self).__init__(specimen, **kwargs)
        self.__dict__['num'] = num

    def test(self, instance, name):
        # Passing requires that the attribute exist and evaluate to True
        return hasattr(instance, name) and len(getattr(instance, name)) == self.__dict__['num']
    test.output = 'has %(num)s %(name)s'

    @property
    def or_less(self):
        return HasNumOrLess(self.specimen, self.num)

    @property
    def or_more(self):
        return HasNumOrMore(self.specimen, self.num)


class HasNumOrMore(HasNum):
    def test(self, instance, name):
        return hasattr(instance, name) and len(getattr(instance, name)) >= self.num
    test.output = 'has %(num)s or more %(name)s'


class HasNumOrLess(HasNum):
    def test(self, instance, name):
        return hasattr(instance, name) and len(getattr(instance, name)) <= self.num
    test.output = 'has %(num)s or less %(name)s'


class Lacks(AttributeTester):
    def test(self, instance, name):
        # Passing requires that the attribute evaluate to False or not exist
        return not (hasattr(instance, name) and bool(getattr(instance, name)))
    test.output = 'lacks %(name)s'

    def __call__(self, num):
        return LacksNum(self.specimen, num)


class LacksNum(Lacks):
    def __init__(self, specimen, num, **kwargs):
        super(LacksNum, self).__init__(specimen, **kwargs)
        self.__dict__['num'] = num

    def test(self, instance, name):
        return not hasattr(instance, name) or len(getattr(instance, name)) != self.num
    test.output = 'lacks %(num)s %(name)s'

    @property
    def or_less(self):
        return LacksNumOrLess(self.specimen, self.num)

    @property
    def or_more(self):
        return LacksNumOrMore(self.specimen, self.num)


class LacksNumOrMore(LacksNum):
    def test(self, instance, name):
        return hasattr(instance, name) and len(getattr(instance, name)) < self.num
    test.output = 'lacks %(num)s or more %(name)s'


class LacksNumOrLess(LacksNum):
    def test(self, instance, name):
        return hasattr(instance, name) and len(getattr(instance, name)) > self.num
    test.output = 'lacks %(num)s or less %(name)s'


