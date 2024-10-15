'''
原理：重复遍历要排序的数列，一次比较两个元素，如果它们的顺序错误就把它们交换过来。遍历数列的工作是重复地进行直到没有再需要交换，也就是说该数列已经排序完成。
时间复杂度：平均和最坏情况下为O(n^2)，最好情况下（已排序）为O(n)。
空间复杂度：O(1)。
'''
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
    
def bubble_sort_recursive(arr, n):
    # 基准情况：如果数组只剩一个或没有元素，那么它自然就是排序好的
    if n == 1:
        return
    # 内层循环实现一次冒泡过程，将最大值移动到末尾
    for i in range(n-1):
        if arr[i] > arr[i+1]:
            arr[i], arr[i+1] = arr[i+1], arr[i]  # 交换元素
    # 递归调用，n减一因为每次最大的元素已经到位，下一次不需要考虑它了
    bubble_sort_recursive(arr, n-1)

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        # 提前退出冒泡循环的标志位
        swapped = False
        # 最后i个元素已排序好，无需再次比较
        for j in range(0, n-i-1):
            # 遍历数组，比较相邻元素，如果逆序就交换
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        # 如果在本轮遍历中没有发生交换，说明数组已经是有序的，可以提前结束
        if not swapped:
            break
    return arr
    
'''
快速排序是一种非常高效的排序算法，采用分而治之的策略，其基本步骤为：选择一个基准元素，
通过一趟排序将待排序的记录分割成独立的两部分，其中一部分的所有数据都比另外一部分的所有数据要小，然后再按此方法对这两部分数据分别进行快速排序'''
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]  # 选择第一个元素作为基准
        less_than_pivot = [x for x in arr[1:] if x <= pivot]  # 所有小于等于基准的元素
        greater_than_pivot = [x for x in arr[1:] if x > pivot]  # 所有大于基准的元素
        return quick_sort(less_than_pivot) + [pivot] + quick_sort(greater_than_pivot)
