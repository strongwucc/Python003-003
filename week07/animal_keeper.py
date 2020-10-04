from abc import ABCMeta, abstractmethod

'''
动物类
'''


class Animal(metaclass=ABCMeta):

    def __init__(self, category, shape, character):
        self.category = category
        self.shape = shape
        self.character = character

    @property
    def is_ferocious(self):
        return (self.shape == '中型' or self.shape == '大型') and self.category == '食肉' and self.character == '凶猛'

    @property
    @abstractmethod
    def as_pets(self):
        pass


'''
猫类
'''


class Cat(Animal):

    # 叫声
    call = ''

    def __init__(self, name, category, shape, character):
        self.name = name
        super().__init__(category, shape, character)

    @property
    def as_pets(self):
        return not self.is_ferocious


'''
狗类
'''


class Dog(Animal):

    # 叫声
    call = ''

    def __init__(self, name, category, shape, character):
        self.name = name
        super().__init__(category, shape, character)

    @property
    def as_pets(self):
        return not self.is_ferocious


'''
动物园类
'''


class Zoo(object):

    animals = {}

    def __init__(self, name):
        self.name = name

    # 添加动物
    @classmethod
    def add_animal(cls, animal):
        if animal not in cls.animals:
            cls.animals[animal] = animal
        if animal.__class__ == Cat:
            cls.cat = True


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小型', '温顺')
    dog1 = Dog('大花狗 1', '食肉', '中型', '凶猛')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    z.add_animal(dog1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'cat')
    print(have_cat)
