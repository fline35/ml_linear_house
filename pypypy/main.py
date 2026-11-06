"""
def fun(*args, **kwargs):
    num = 0
    for arg in args:
        num += arg
    print(f"Sum of args: {num}")

    print("Hello, PyPyPy!") 

    for key, value in kwargs.items():
        print(f"{key}: {value}")


fun(1, 2, 3, 4, 5, name='John', age=30, city='New York')
"""
"""
def modify_dict(old_dict : dict, **kwargs) -> tuple[dict, bool]:
    new_dict = old_dict.copy()
    for key, value in kwargs.items():
        if key not in new_dict:
            print(f"Key '{key}' has been added with value: {value}")
        elif old_dict[key] != value:
            print(f"Key '{key}' has been modified from {new_dict[key]} to {value}")
        new_dict[key] = value
    is_modified = new_dict != old_dict
    

    return new_dict, is_modified

old_dict = {'a': 1, 'b': 2, 'c': 3}
new_dict, modified = modify_dict(old_dict, b=20, d=4, e=5)
print("New Dictionary:", new_dict)
print("Was the dictionary modified?", modified)
"""
"""
def mod_dict(old_dict : dict, **kwargs) -> tuple[dict, bool]:
    new_dict = old_dict.copy()

    for key, value in kwargs.items():
        if key not in new_dict:
            print(f'New item is {key} and his value is {value}')
        elif old_dict[key] != value:
            print(f'Modified key is {key}, and his value is {value}')
        new_dict[key] = value

    is_modified = new_dict != old_dict
    return new_dict, is_modified



old_dict = {'a':23, 'b':24, 'c':25}
new_dict, modified = mod_dict(old_dict, b=13, c=15, f=55)
print(f'New dicts is {new_dict}')
print(f'Modified dicts is {modified}')
"""
'''
def new_mod(old_dict : dict, **kwargs) -> tuple[dict, bool]:
    new_dict = old_dict.copy()

    for key, value in kwargs.items():
        if key not in new_dict:
            print(f'Added new {key} and his value is {value}')
        elif old_dict[key] != value:
            print(f'In key {key} values been modified for {value}')

        new_dict[key] = value
    is_modified = new_dict != old_dict

    return new_dict, is_modified

old_dict = {'a':15, 'b':16, 'c':18}
new_dict, modified = new_mod(old_dict, a = 16, d = 45)

print(f'new dicts is {new_dict}')
print(f'modified dicts is {modified}')

'''

#list comprehension
#dict comprehension
#set comprehension

new_list = [x**2 for x in range(10) if x % 2 == 0]

new_dict = {x: x**2 for x in range(10) if x % 2 == 0}

new_set = {x**2 for x in range(10) if x % 2 == 0}

print(new_list)
print(new_dict)
print(new_set)

#lambda функция


list_samp = [1, 2, 3, 4, 5]
new = list(map(lambda x: x**2, list_samp))

print(new)

#фильтр
numbers = [1, 2, 3, 4, 5, 6]

result = filter(lambda x: x % 2 == 0, numbers)

people = [
    {'name': 'Alice', 'age': 30},
    {'name': 'Bob', 'age': 25},
    {'name': 'Charlie', 'age': 35}
]

def sort_people(people):
    return sorted(people, key=lambda x: x['age'])

sorted_people = sort_people(people)
print(sorted_people)