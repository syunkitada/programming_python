from pkg.utils import calc


def sum(nums):
    try:
        result = 0
        for num in nums:
            result = calc.add_num(result, num)
        return result
    except Exception:
        return -1
