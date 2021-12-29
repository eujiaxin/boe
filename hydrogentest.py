def median_result(stud_id, results):
    # lst = list(map(lambda x:x[2], filter(lambda x: x[1] == stud_id, results)))
    lst = []
    for x in results:
        if x[1] == stud_id:
            lst.append(x[2])
    lst.sort()
    n = len(lst)
    if n % 2 == 0:
        return (lst[n/2] + lst[n/2 - 1])/2
    return lst[n//2]

results = [
    ['', 101028, 65],
    ['', 101022, 80],
    ['', 201028, 61],
    ['', 201022, 59],
    ['', 310666, 45],
    ['', 101022, 85],
    ['', 101022, 71],
    ['', 493968, 67],
    ['', 523123, 75]
]

median_result(101022, results)
median_result(201022, results)


while len(lst) > 1:
    # let n be len(lst) before a and b is popped
    # lst[-1] is the maximum in original_lst[n-1:]
    a = lst.pop()
    b = lst.pop()
    if a > b:
        lst.append(a)
    else:
        lst.append(b)
    # lst[-1] is the maximum in original_lst[n-2:]

    # exit condition: len(lst) == 1
    # post condition: len(lst) == 1, lst[0] == lst[-1]
return lst[0]

def remove(lst, x):
    if lst:
        if lst[0] == x:
            return remove(lst[1:], x)
        else:
            return [lst[0]] + remove(lst[1:], x)
    return []

remove([2,3,4,1], 1)
remove([1,1,1,1,1], 1)
remove([0,0,0,0,0], 1)
remove([1], 1)
