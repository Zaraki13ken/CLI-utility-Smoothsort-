"""Единая точка входа консольной утилиты плавной сортировки."""

import argparse
import sys
from typing import List, Optional

from my_sort import my_sort


def _parse_data(raw: str, numeric: bool) -> List:
    """Разбирает строку с данными в список."""
    cleaned = raw.strip().strip("[]")
    for sep in (",", ";"):
        cleaned = cleaned.replace(sep, " ")
    tokens = cleaned.split()
    if numeric:
        return [int(tok) for tok in tokens]
    return tokens


def _load_data_from_file(path: str, numeric: bool) -> List:
    """Читает данные из файла (по одному значению на строку)."""
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if numeric:
        return [int(x) for x in lines]
    return lines


def _get_data(args: argparse.Namespace) -> List:
    """Возвращает данные согласно приоритету флагов."""
    if args.data is not None:
        return _parse_data(args.data, args.numeric)
    if args.input is not None:
        return _load_data_from_file(args.input, args.numeric)
    raise ValueError("Не заданы данные: укажите --input или --data")


def _save_result(result: List, output_path: str) -> None:
    """Записывает результат в файл (по одному элементу на строку)."""
    with open(output_path, "w", encoding="utf-8") as f:
        for item in result:
            f.write(f"{item}\n")
    print(f"Результат сохранён в файл: {output_path}")


def _run_graphical_visualization(
        data: List,
        reverse: bool = False,
        interval: int = 1000,
        output_path: Optional[str] = None) -> None:
    """Графическая визуализация с настройкой скорости."""
    try:
        from visualize import smoothsort_with_frames, animate  # pylint: disable=import-outside-toplevel
    except ImportError as exc:
        print(
            "Графическая визуализация недоступна: не установлен matplotlib.\n"
            "Установите зависимости: pip install matplotlib\n"
            f"Подробности: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)

    print("Исходный массив:", data)

    frames = smoothsort_with_frames(data, reverse=reverse)

    animate(frames, interval=interval)

    result = my_sort(data, reverse=reverse)
    print("Отсортированный массив:", result)

    if output_path:
        _save_result(result, output_path)


def _run_sort(args: argparse.Namespace) -> None:
    """Обычная сортировка: вывод в консоль и (опционально) в файл."""
    data = _get_data(args)
    result = my_sort(data, reverse=args.reverse)

    for item in result:
        print(item)

    if args.output:
        _save_result(result, args.output)


def main() -> None:
    """Точка входа программы."""
    parser = argparse.ArgumentParser(
        description="Плавная сортировка (smoothsort).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Примеры:\n"
            "  python main.py --visualize --data \"2 -3 5 0 5\" --numeric\n"
            "  python main.py --visualize --data \"2 -3 5 0 5\" --numeric --interval 1000\n"
            "  python main.py --input nums.txt --numeric --reverse\n"
        ),
    )
    parser.add_argument("--input", help="входной файл")
    parser.add_argument("--output", help="выходной файл")
    parser.add_argument("--data", help="данные в командной строке")
    parser.add_argument("--reverse", action="store_true", help="по невозрастанию")
    parser.add_argument("--numeric", action="store_true", help="числовые данные")
    parser.add_argument("--visualize", action="store_true", help="графическая визуализация")
    parser.add_argument("--interval", type=int, default=500,
                        help="задержка между кадрами анимации в мс "
                             "(больше = медленнее, по умолчанию 500)")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    if args.visualize:
        try:
            data = _get_data(args)
        except ValueError as exc:
            print(f"Ошибка: {exc}", file=sys.stderr)
            sys.exit(1)

        if not args.numeric:
            print("Ошибка: графическая визуализация доступна только для чисел. "
                  "Добавьте флаг --numeric.", file=sys.stderr)
            sys.exit(1)

        _run_graphical_visualization(data, args.reverse, args.interval, args.output)
        return

    try:
        _run_sort(args)
    except ValueError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
