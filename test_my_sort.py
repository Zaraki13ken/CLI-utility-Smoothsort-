"""Тесты для модуля my_sort"""

import unittest

import my_sort  # pylint: disable=E0401

TEST_NUMBER_38 = [
    27, 14, 35, 3, 19, 42, 8, 23, 1, 31, 16, 45, 10, 29, 5, 38, 
    12, 21, 47, 7, 33, 18, 2, 40, 25, 11, 36, 4, 22, 49, 15, 30, 
    6, 44, 20, 9, 37, 26
]

TEST_NUMBER = [
    [],
    [1],
    [1, 2, 3, 4, 5],
    [0, 0, 0, 55, 55, 60],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    [8, 0, 42, 3, 4, 8, 0, 45, 50, 9999, 7],
    [-5, 0, 9, -999, 874, 35, -4, -5, 0],
    [1, 1, 1],
]


TEST_STR = [
    [],
    ['a'],
    ['a', 'b', 'c', 'd', 'e'],
    ['aa', 'aa', 'aa', 'ab', 'ac', 'b'],
    ['e', 'd', 'c', 'b', 'a'],
    ['abc', 'a', 'foo', 'bar', 'booz', 'baz', 'spam', 'love'],
    ['abc', 'abc', 'abc'],
    [''],
]


class TestSort(unittest.TestCase):
    """Тест-кейс модуля my_sort"""
    def test_sort_38_increase(self):
        """Тест сортировки 38 элементов по возрастанию (выявляет ошибку индекса)."""
        self.assertEqual(my_sort.my_sort(TEST_NUMBER_38), sorted(TEST_NUMBER_38))

    def test_sort_38_decrease(self):
        """Тест сортировки 38 элементов по убыванию."""
        self.assertEqual(
            my_sort.my_sort(TEST_NUMBER_38, reverse=True),
            sorted(TEST_NUMBER_38, reverse=True)
        )
        
    def test_sort_number_increase(self):
        """Тест функции сортировки числовых данных по возрастанию"""
        for data in TEST_NUMBER:
            with self.subTest():
                self.assertEqual(my_sort.my_sort(data), sorted(data))

    def test_sort_number_decrease(self):
        """Тест функции сортировки числовых данных по невозрастанию"""
        for data in TEST_NUMBER:
            with self.subTest():
                self.assertEqual(
                    my_sort.my_sort(data, reverse=True),
                    sorted(data, reverse=True)
                )

    def test_sort_str_increase(self):
        """Тест функции сортировки строковых данных по возрастанию"""
        for data in TEST_STR:
            with self.subTest():
                self.assertEqual(my_sort.my_sort(data), sorted(data))

    def test_sort_str_decrease(self):
        """Тест функции сортировки строковых данных по невозрастанию"""
        for data in TEST_STR:
            with self.subTest():
                self.assertEqual(
                    my_sort.my_sort(data, reverse=True),
                    sorted(data, reverse=True)
                )
