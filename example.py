from labcoat import Specimen


# Some example objects

class Dog:
    legs = (('front', 'left'), ('front', 'right'), ('back', 'left'), ('back', 'right'))
    tail = True
    fur_color = 'black'

    def bark(self):
        return 'Woof!'

    def hump(self, obj):
        if isinstance(obj, Human):
            raise BadDog('Down boy!')


class Human:
    legs = ('left', 'right')

    def set_name(self, name):
        self.name = name


class Furniture:
    legs = ('a', 'b', 'c', 'd')


class BadDog(Exception):
    pass


def test():
    with Specimen(Dog) as rover:
        rover.has.tail
        rover.has(4).legs
        rover.can.bark()

    with Specimen(Furniture) as couch:
        couch.has(4).or_more.legs
        couch.lacks.tail
        couch.can_not.bark()
        rover.can.hump(couch)

    with Specimen(Human) as owner:
        owner.has(2).legs
        owner.lacks.tail
        rover.can_not.hump(owner).because(BadDog)


if __name__ == '__main__':
    test()

