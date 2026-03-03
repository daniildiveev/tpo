from __future__ import annotations
from typing import Any

SORT_ENTER      = "CP1_SORT_ENTER"
BUILD_HEAP_DONE = "CP2_BUILD_HEAP_DONE"
HEAPIFY_ENTER   = "CP3_HEAPIFY_ENTER"
HEAPIFY_SWAP    = "CP4_HEAPIFY_SWAP"
EXTRACT_SWAP    = "CP5_EXTRACT_SWAP"
SORT_EXIT       = "CP6_SORT_EXIT"


def _heapify(arr: list, node: int, heap_size: int, trace: list) -> None:
    trace.append((HEAPIFY_ENTER, {"node": node, "heap_size": heap_size}))

    largest = node
    left    = 2 * node + 1
    right   = 2 * node + 2

    if left < heap_size and arr[left] > arr[largest]:
        largest = left
    if right < heap_size and arr[right] > arr[largest]:
        largest = right

    if largest != node:
        trace.append((HEAPIFY_SWAP, {"swap_from": node, "swap_to": largest,
                                      "value_from": arr[node], "value_to": arr[largest]}))
        arr[node], arr[largest] = arr[largest], arr[node]
        _heapify(arr, largest, heap_size, trace)


def _build_max_heap(arr: list, trace: list) -> None:
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, i, n, trace)


def heap_sort(arr: list) -> tuple[list, list[tuple[str, dict[str, Any]]]]:
    data  = list(arr)
    trace: list = []

    trace.append((SORT_ENTER, {"initial": list(data)}))

    _build_max_heap(data, trace)

    trace.append((BUILD_HEAP_DONE, {"heap": list(data)}))

    for i in range(len(data) - 1, 0, -1):
        data[0], data[i] = data[i], data[0]
        trace.append((EXTRACT_SWAP, {"swap_index": i, "extracted_value": data[i]}))
        _heapify(data, 0, i, trace)

    trace.append((SORT_EXIT, {"result": list(data)}))

    return data, trace
