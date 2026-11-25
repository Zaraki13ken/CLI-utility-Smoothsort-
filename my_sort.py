"""Модуль плавной сортировки (smoothsort)."""

from typing import Callable, List, Optional


def _leonardo_numbers(hi: int) -> List[int]:
    """Генерирует числа Леонардо, не превышающие ``hi``."""
    a, b = 1, 1
    numbers: List[int] = []
    while a <= hi:
        numbers.append(a)
        a, b = b, a + b + 1
    return numbers


def _get_child_trees(i: int, k: int, leo_nums: List[int]):
    """Возвращает индексы и порядки двух поддеревьев кучи порядка ``k``."""
    t_r, k_r = i - 1, k - 2
    t_l, k_l = t_r - leo_nums[k_r], k - 1
    return t_r, k_r, t_l, k_l


def _restore_heap(lst: list, i: int, heap: List[int],
                  leo_nums: List[int], gt: Callable) -> None:
    """Восстанавливает свойства куч (trinkle + sift).

    :param lst: массив
    :param i: индекс корня текущей кучи
    :param heap: стек порядков куч
    :param leo_nums: числа Леонардо
    :param gt: функция строгого сравнения ``a > b``
    """
    # --- trinkle: поднимаем корень через предыдущие кучи ---
    current = len(heap) - 1
    k = heap[current]

    while current > 0:
        # j — корень предыдущей кучи (левый потомок текущей)
        j = i - leo_nums[k]
        
        # Если у текущей кучи есть потомки (k >= 2), 
        # проверяем, что корень предыдущей кучи (j) больше их обоих
        if k >= 2:
            t_r, k_r, t_l, k_l = _get_child_trees(i, k, leo_nums)
            check_children = gt(lst[j], lst[t_r]) and gt(lst[j], lst[t_l])
        else:
            check_children = True

        if gt(lst[j], lst[i]) and check_children:
            lst[i], lst[j] = lst[j], lst[i]
            i = j
            current -= 1
            k = heap[current]
        else:
            break

    # --- sift: просейка внутри текущего дерева ---
    while k >= 2:
        t_r, k_r, t_l, k_l = _get_child_trees(i, k, leo_nums)
        if gt(lst[t_r], lst[i]) or gt(lst[t_l], lst[i]):
            if gt(lst[t_r], lst[t_l]):
                lst[i], lst[t_r] = lst[t_r], lst[i]
                i, k = t_r, k_r
            else:
                lst[i], lst[t_l] = lst[t_l], lst[i]
                i, k = t_l, k_l
        else:
            break


def _smoothsort(data: list, gt: Callable) -> None:
    """Сортирует список на месте плавной сортировкой.

    :param data: сортируемый список
    :param gt: функция строгого сравнения ``a > b``
    """
    n = len(data)
    if n <= 1:
        return

    leo_nums = _leonardo_numbers(n)
    heap: List[int] = []

    # Фаза 1: построение куч
    for i in range(n):
        if len(heap) >= 2 and heap[-2] == heap[-1] + 1:
            heap.pop()
            heap[-1] += 1
        else:
            if len(heap) >= 1 and heap[-1] == 1:
                heap.append(0)
            else:
                heap.append(1)
        _restore_heap(data, i, heap, leo_nums, gt)

    # Фаза 2: разбор куч
    for i in reversed(range(n)):
        if heap[-1] < 2:
            heap.pop()
        else:
            k = heap.pop()
            t_r, k_r, t_l, k_l = _get_child_trees(i, k, leo_nums)
            heap.append(k_l)
            _restore_heap(data, t_l, heap, leo_nums, gt)
            heap.append(k_r)
            _restore_heap(data, t_r, heap, leo_nums, gt)


def _make_gt(cmp: Optional[Callable], reverse: bool) -> Callable:
    """Создаёт функцию строгого сравнения ``a > b``."""
    if cmp is not None:
        if reverse:
            return lambda a, b: cmp(a, b) < 0
        return lambda a, b: cmp(a, b) > 0
    if reverse:
        return lambda a, b: a < b
    return lambda a, b: a > b


def _make_key(key: Optional[Callable]) -> Callable:
    """Создаёт функцию ключа."""
    if key is not None:
        return key
    return lambda x: x


def my_sort(array: list, reverse: bool = False,
            key: Optional[Callable] = None,
            cmp: Optional[Callable] = None) -> list:
    """Сортирует список плавной сортировкой (smoothsort).

    :param array: сортируемый список
    :param reverse: если ``True`` — по невозрастанию, иначе по неубыванию
    :param key: функция, вычисляющая значение для сравнения
    :param cmp: функция сравнения двух аргументов
    :return: новый отсортированный список
    """
    data = list(array)
    if len(data) <= 1:
        return data

    get_key = _make_key(key)

    if key is not None:
        # pylint: disable=too-few-public-methods
        class _Keyed:
            """Обёртка элемента с ключом."""
            __slots__ = ("value", "k")

            def __init__(self, value, k):
                self.value = value
                self.k = k

        wrapped = [_Keyed(v, get_key(v)) for v in data]
        if cmp is not None:
            base_gt = _make_gt(cmp, reverse)

            def wrapped_gt(a, b):
                """Сравнение обёрнутых элементов по ключу."""
                return base_gt(a.k, b.k)
        else:
            wrapped_gt = (lambda a, b: a.k < b.k) if reverse else (
                lambda a, b: a.k > b.k)
        _smoothsort(wrapped, wrapped_gt)
        return [w.value for w in wrapped]

    gt = _make_gt(cmp, reverse)
    _smoothsort(data, gt)
    return data