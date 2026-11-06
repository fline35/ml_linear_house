from math import log

#бинарный поиск
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    count = 0

    while low <= high:
        count += 1
        mid = (low + high) // 2
        guess = arr[mid]

        if guess == target:
            return mid, count

        elif guess > target:
            high = mid - 1

        else:
             low = mid + 1

    return None

arr1 = [1,2,3,4,5,6,7,8,9]

print(binary_search(arr1, 6))

#общ время O(log n)

#задание 1
print(log(128, 2))

#2. каждое удвоение увеличивает на n+1



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


from functools import wraps

#Чтобы сохранить метаданные оригинальной функции, используют:
def ftool(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

