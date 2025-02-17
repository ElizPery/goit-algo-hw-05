def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    num_of_iteration = 1
    upper_bound = arr[-1]
 
    while low <= high:
 
        mid = (high + low) // 2
 
        # if x is greater than the value in the middle of the list, ignore the left half
        if arr[mid] < x:
            low = mid + 1
            num_of_iteration += 1
 
        # if x is less than the value in the middle of the list, ignore the right half
        elif arr[mid] > x:
            upper_bound = mid
            high = mid - 1
            num_of_iteration += 1
 
        # return number of needed iterations and index of element
        else:
            return (num_of_iteration, mid)
 
    # if the item is not found return upper bound
    return (num_of_iteration, upper_bound)

arr = [2.2, 2.5, 3, 3.9, 4.7, 11, 13, 15, 40.5, 40.8, 40.9]
x = 2.3
print(binary_search(arr, x))