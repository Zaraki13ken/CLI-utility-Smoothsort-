"""Визуализация плавной сортировки с помощью matplotlib."""
# pylint: disable=import-error, consider-using-from-import

from typing import List, Optional

import matplotlib.pyplot as plt
import matplotlib.animation as animation


def _leonardo_numbers(hi: int) -> List[int]:
    """Числа Леонардо, не превышающие ``hi``."""
    a, b = 1, 1
    nums = []
    while a <= hi:
        nums.append(a)
        a, b = b, a + b + 1
    return nums


def _get_child_trees(i: int, k: int, leo_nums: List[int]):
    """Индексы и порядки двух поддеревьев кучи порядка ``k``."""
    t_r, k_r = i - 1, k - 2
    t_l, k_l = t_r - leo_nums[k_r], k - 1
    return t_r, k_r, t_l, k_l


def smoothsort_with_frames(data: List[int], reverse: bool = False) -> List[dict]: # pylint: disable=too-many-locals, too-many-statements
    """Плавная сортировка, возвращающая кадры для визуализации."""
    arr = list(data)
    n = len(arr)
    frames: List[dict] = []
    leo_nums = _leonardo_numbers(n)
    heap: List[int] = []
    gt = (lambda a, b: a < b) if reverse else (lambda a, b: a > b)

    def add_frame(active: Optional[int], stage: str) -> None:
        roots = set()
        pos = 0
        for k in heap:
            pos += leo_nums[k]
            roots.add(pos - 1)
        frames.append({
            "array": arr.copy(),
            "roots": roots,
            "active": active,
            "stage": stage,
        })

    def restore_heap(i: int, heap_ref: List[int]) -> None:
        current = len(heap_ref) - 1
        k = heap_ref[current]
        while current > 0:
            j = i - leo_nums[k]
            if gt(arr[j], arr[i]) and (
                    k < 2 or (gt(arr[j], arr[i - 1]) and gt(arr[j], arr[i - 2]))):
                add_frame(i, "trinkle: swap")
                arr[i], arr[j] = arr[j], arr[i]
                i = j
                current -= 1
                k = heap_ref[current]
            else:
                break
        while k >= 2:
            t_r, k_r, t_l, k_l = _get_child_trees(i, k, leo_nums)
            if gt(arr[t_r], arr[i]) or gt(arr[t_l], arr[i]):
                if gt(arr[t_r], arr[t_l]):
                    add_frame(i, "sift: swap right")
                    arr[i], arr[t_r] = arr[t_r], arr[i]
                    i, k = t_r, k_r
                else:
                    add_frame(i, "sift: swap left")
                    arr[i], arr[t_l] = arr[t_l], arr[i]
                    i, k = t_l, k_l
            else:
                break

    # Фаза 1
    for i in range(n):
        if len(heap) >= 2 and heap[-2] == heap[-1] + 1:
            heap.pop()
            heap[-1] += 1
        else:
            if len(heap) >= 1 and heap[-1] == 1:
                heap.append(0)
            else:
                heap.append(1)
        add_frame(i, "build: add")
        restore_heap(i, heap)

    # Фаза 2
    for i in reversed(range(n)):
        if heap[-1] < 2:
            heap.pop()
            add_frame(i, "extract: remove root")
        else:
            k = heap.pop()
            t_r, k_r, t_l, k_l = _get_child_trees(i, k, leo_nums)
            heap.append(k_l)
            restore_heap(t_l, heap)
            heap.append(k_r)
            restore_heap(t_r, heap)
            add_frame(i, "extract: split")

    return frames

def animate(frames: List[dict], interval: int = 1000) -> None:
    """Запускает анимацию."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")


    all_vals = [val for frame in frames for val in frame["array"]]
    if not all_vals:
        all_vals = [0, 1]
    g_min = min(all_vals)
    g_max = max(all_vals)

    y_margin = max(abs(g_max), abs(g_min)) * 0.2 if g_max != g_min else 1
    y_min = g_min - y_margin if g_min < 0 else 0
    y_max = g_max + y_margin

    def draw(frame_idx: int) -> None:
        ax.clear()
        frame = frames[frame_idx]
        arr = frame["array"]
        roots = frame["roots"]
        active = frame["active"]

        colors = []
        for idx in range(len(arr)):
            if idx == active:
                colors.append("#ff0000") # Красный
            else:
                colors.append("#cccccc") # Серый

        x = list(range(len(arr)))

        ax.bar(x, arr, color=colors, edgecolor="none", width=0.85, zorder=3)

        for idx in roots:
            ax.plot(idx, arr[idx], marker="s", markersize=6,
                    color="black", zorder=5)

        for i, val in enumerate(arr):
            ax.text(i, y_min + (y_max - y_min) * 0.02, str(val),
                    ha='center', va='bottom', color='black', fontsize=10, zorder=6)

        if g_min < 0:
            ax.axhline(0, color='black', linewidth=0.8, zorder=2)

        ax.set_xlim(-0.5, len(arr) - 0.5)
        ax.set_ylim(y_min, y_max)
        ax.set_title(f"Шаг {frame_idx + 1}/{len(frames)} — {frame['stage']}")

        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    animation.FuncAnimation(
        fig, draw, frames=len(frames), interval=interval, repeat=False
    )
    plt.show()
