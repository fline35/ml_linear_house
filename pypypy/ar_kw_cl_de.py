from dataclasses import dataclass
from functools import wraps
from contextlib import contextmanager

def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)

        return wrapper
    return decorator


@repeat(3)
def hello():
    print('hello')

hello()

def log(func):
    def wrapper(*args, **kwargs):
        print(f'function name: {func.__name__}')

        print(f'args: {args}')
        print(f'kwargs {kwargs}')

        result = func(*args, **kwargs)
        print(f'result: {result}')

        return result
    return wrapper

@log
def add(a, b):
    return a + b

add(20, 30)



#Чтобы сохранить метаданные оригинальной функции, используют:
def ftool(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper



# Пример собственного контекстного менеджера
@contextmanager
def managed_resource():
    print("-> Вход в контекст (выделение ресурсов)")
    try:
        yield "ресурс"
    finally:
        print("<- Выход из контекста (освобождение ресурсов)")

# Декоратор, использующий контекстный менеджер
def my_decorator(func):
    @wraps(func)  # Сохраняет имя, документацию и аннотации исходной функции
    def wrapper(*args, **kwargs):
        with managed_resource() as resource:
            print(f"Контекст активен, передан: {resource}")
            # Вызываем исходную функцию
            result = func(*args, **kwargs)
            return result
    return wrapper

# Проверка работы
@my_decorator
def example_function(text):
    print(f"Вызвана функция с аргументом: {text}")
    return "Готово"

# Запуск
res = example_function("Привет!")
print(f"Результат функции: {res}")
################

class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email


    def method(self):
        pass

    @classmethod
    def class_method(cls):
        pass

    @staticmethod
    def static_method():
        pass
    



user = User(1, 'John Doe', 'john.doe@example.com')

print(user)

class Animal:

    def __init__(self, name):
        self.name = name

class Dog(Animal):

    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
    
    def speak(self):
        print(f"{self.name} says Woof!")

'''
Dog.__init__
    ↓
super().__init__
    ↓
Animal.__init__
    ↓
self.name = "Bob"
    ↓
возвращаемся в Dog
    ↓
self.breed = "Corgi"
'''

def make_sound(animal):
    animal.speak()

dog = Dog("Bob", "Corgi")
make_sound(dog)

'''
                    object
                       │
                       ↓
                    User()
                       │
             ┌─────────┴─────────┐
             │                   │
        атрибуты               методы
             │                   │
       name, age             say_hello()
             │                   │
             ↓                   ↓
         self.name           self → объект




             Animal
             /    \
            /      \
         Dog       Cat
          │         │
          │         │
       bark()    meow()
          │         │
          └────┬────┘
               ↓
          полиморфизм
'''


from abc import ABC, abstractmethod


class Animal(ABC):

    count = 0

    def __init__(self, name):
        self._name = name
        Animal.count += 1

    @property
    def name(self):
        return self._name

    @abstractmethod
    def speak(self):
        pass

    def __str__(self):
        return f"Animal: {self.name}"

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name!r})"

    @classmethod
    def how_many(cls):
        return cls.count

    @staticmethod
    def is_animal(obj):
        return isinstance(obj, Animal)


class Dog(Animal):

    def speak(self):
        return "Гав!"

dog = Dog("Bob")

#__str__
print(dog)

#__repr__
print(repr(dog))

#@property
print(dog.name)

#использует переопределённый метод Dog.
print(dog.speak())

#@classmethod
print(Dog.how_many())

#@staticmethod
Animal.is_animal(dog)


@dataclass
class Point:
    x: float
    y: float

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __repr__(self):
        return f"Point(x={self.x!r}, y={self.y!r})"

class Bank:
    def __init__(self, balance):
        self.balance = balance


    @property
    def interest_rate(self):
        return 0.05

    @interest_rate.setter
    def interest_rate(self, value):
        if value < 0:
            raise ValueError("Interest rate cannot be negative.")
        self._interest_rate = value


    