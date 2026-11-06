
#для отсортированного массива
def two_pointers(arr, target) -> list:
    left = 0
    right = len(arr) - 1
    choice = 0

    while left < right:
        choice = arr[left] + arr[right]
        if choice == target:
            return arr[left], arr[right]

        elif choice < target:
            left += 1

        else:
            right -= 1

    return 0
#print(two_pointers([1, 2, 3, 4, 5, 6, 7, 8], 10))

#для неотсортированного массива
def two_pointers_unsorted(arr, target) -> list:
    arr.sort()
    left = 0
    right = len(arr) - 1
    choice = 0

    while left < right:
        choice = arr[left] + arr[right]
        if choice == target:
            return arr[left], arr[right]

        elif choice < target:
            left += 1

        else:
            right -= 1

    return 0

# print(two_pointers_unsorted([3, 4, 5, 4, 5, 6, 7, 8], 10))

#слияние массивов
def merge_sorted_arrays(arr1, arr2) -> list:
    merged = []
    i = 0
    j = 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            merged.append(arr1[i])
            i += 1
        else:
            merged.append(arr2[j])
            j += 1

    while i < len(arr1):
        merged.append(arr1[i])
        i += 1

    while j < len(arr2):
        merged.append(arr2[j])
        j += 1

    return merged


def two_pointers_sort(arr1) -> list:
    write = 1
    read = 1
    for read in range(1, len(arr1)):
        if arr1[read] != arr1[read - 1]:
            arr1[write] = arr1[read]
            write += 1

    return arr1[:write]

print(two_pointers_sort([1, 1, 2, 2, 3, 4, 4, 5, 6, 7, 7, 8]))







