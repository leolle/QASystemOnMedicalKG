import itertools
numbers = [1, 2, 3, 7, 7, 9, 10]
result = [seq for i in range(len(numbers), 0, -1) for seq in itertools.combinations(numbers, i) if sum(seq) == 10]
print(result)


def subset_sum(numbers, target, partial=[], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(numbers):
        remaining = numbers[i + 1:]
        yield from subset_sum(remaining, target, partial + [n], partial_sum + n)
ls_input = [124, 74]
total = 500
list(subset_sum(ls_input, total))