import pytest
from heap_sort import (
    heap_sort,
    SORT_ENTER, BUILD_HEAP_DONE, HEAPIFY_ENTER, HEAPIFY_SWAP,
    EXTRACT_SWAP, SORT_EXIT,
)


def _simplify(trace):
    result = []
    for cp, meta in trace:
        if cp == HEAPIFY_ENTER:
            result.append((cp, (meta["node"], meta["heap_size"])))
        elif cp == HEAPIFY_SWAP:
            result.append((cp, (meta["swap_from"], meta["swap_to"])))
        elif cp == EXTRACT_SWAP:
            result.append((cp, (meta["swap_index"],)))
        else:
            result.append((cp, ()))
    return result


def _cp(name, *args):
    return (name, tuple(args))


REF_EMPTY = [
    _cp(SORT_ENTER),
    _cp(BUILD_HEAP_DONE),
    _cp(SORT_EXIT),
]

REF_SINGLE = [
    _cp(SORT_ENTER),
    _cp(BUILD_HEAP_DONE),
    _cp(SORT_EXIT),
]

REF_ALL_EQUAL = [
    _cp(SORT_ENTER),
    _cp(HEAPIFY_ENTER, 0, 3),
    _cp(BUILD_HEAP_DONE),
    _cp(EXTRACT_SWAP, 2),
    _cp(HEAPIFY_ENTER, 0, 2),
    _cp(EXTRACT_SWAP, 1),
    _cp(HEAPIFY_ENTER, 0, 1),
    _cp(SORT_EXIT),
]

REF_ROOT_MAX = [
    _cp(SORT_ENTER),
    _cp(HEAPIFY_ENTER, 0, 3),
    _cp(BUILD_HEAP_DONE),
    _cp(EXTRACT_SWAP, 2),
    _cp(HEAPIFY_ENTER, 0, 2),
    _cp(EXTRACT_SWAP, 1),
    _cp(HEAPIFY_ENTER, 0, 1),
    _cp(SORT_EXIT),
]

REF_REVERSE = [
    _cp(SORT_ENTER),
    _cp(HEAPIFY_ENTER, 1, 5),
    _cp(HEAPIFY_ENTER, 0, 5),
    _cp(BUILD_HEAP_DONE),
    _cp(EXTRACT_SWAP, 4),
    _cp(HEAPIFY_ENTER, 0, 4), _cp(HEAPIFY_SWAP, 0, 1),
    _cp(HEAPIFY_ENTER, 1, 4), _cp(HEAPIFY_SWAP, 1, 3),
    _cp(HEAPIFY_ENTER, 3, 4),
    _cp(EXTRACT_SWAP, 3),
    _cp(HEAPIFY_ENTER, 0, 3), _cp(HEAPIFY_SWAP, 0, 2),
    _cp(HEAPIFY_ENTER, 2, 3),
    _cp(EXTRACT_SWAP, 2),
    _cp(HEAPIFY_ENTER, 0, 2), _cp(HEAPIFY_SWAP, 0, 1),
    _cp(HEAPIFY_ENTER, 1, 2),
    _cp(EXTRACT_SWAP, 1),
    _cp(HEAPIFY_ENTER, 0, 1),
    _cp(SORT_EXIT),
]

REF_MULTILEVEL = [
    _cp(SORT_ENTER),
    _cp(HEAPIFY_ENTER, 1, 5),
    _cp(HEAPIFY_ENTER, 0, 5), _cp(HEAPIFY_SWAP, 0, 1),
    _cp(HEAPIFY_ENTER, 1, 5), _cp(HEAPIFY_SWAP, 1, 3),
    _cp(HEAPIFY_ENTER, 3, 5),
    _cp(BUILD_HEAP_DONE),
    _cp(EXTRACT_SWAP, 4),
    _cp(HEAPIFY_ENTER, 0, 4), _cp(HEAPIFY_SWAP, 0, 1),
    _cp(HEAPIFY_ENTER, 1, 4), _cp(HEAPIFY_SWAP, 1, 3),
    _cp(HEAPIFY_ENTER, 3, 4),
    _cp(EXTRACT_SWAP, 3),
    _cp(HEAPIFY_ENTER, 0, 3), _cp(HEAPIFY_SWAP, 0, 1),
    _cp(HEAPIFY_ENTER, 1, 3),
    _cp(EXTRACT_SWAP, 2),
    _cp(HEAPIFY_ENTER, 0, 2),
    _cp(EXTRACT_SWAP, 1),
    _cp(HEAPIFY_ENTER, 0, 1),
    _cp(SORT_EXIT),
]


class TestHeapSortEmpty:

    def test_result_is_sorted(self):
        result, _ = heap_sort([])
        assert result == []

    def test_trace_matches_reference(self):
        _, trace = heap_sort([])
        assert _simplify(trace) == REF_EMPTY


class TestHeapSortSingleElement:

    def test_result_is_sorted(self):
        result, _ = heap_sort([1])
        assert result == [1]

    def test_trace_matches_reference(self):
        _, trace = heap_sort([1])
        assert _simplify(trace) == REF_SINGLE


class TestHeapSortAllEqual:

    def test_result_is_sorted(self):
        result, _ = heap_sort([2, 2, 2])
        assert result == [2, 2, 2]

    def test_trace_matches_reference(self):
        _, trace = heap_sort([2, 2, 2])
        assert _simplify(trace) == REF_ALL_EQUAL

    def test_no_heapify_swap_fires(self):
        _, trace = heap_sort([2, 2, 2])
        cp_names = [cp for cp, _ in trace]
        assert HEAPIFY_SWAP not in cp_names


class TestHeapSortRootAlreadyMax:

    def test_result_is_sorted(self):
        result, _ = heap_sort([3, 1, 2])
        assert result == [1, 2, 3]

    def test_trace_matches_reference(self):
        _, trace = heap_sort([3, 1, 2])
        assert _simplify(trace) == REF_ROOT_MAX

    def test_no_heapify_swap_in_build(self):
        _, trace = heap_sort([3, 1, 2])
        cp_names = [cp for cp, _ in trace]
        idx_build_done = cp_names.index(BUILD_HEAP_DONE)
        assert HEAPIFY_SWAP not in cp_names[:idx_build_done]


class TestHeapSortReverseSorted:

    def test_result_is_sorted(self):
        result, _ = heap_sort([5, 4, 3, 2, 1])
        assert result == [1, 2, 3, 4, 5]

    def test_trace_matches_reference(self):
        _, trace = heap_sort([5, 4, 3, 2, 1])
        assert _simplify(trace) == REF_REVERSE

    def test_no_swap_during_build(self):
        _, trace = heap_sort([5, 4, 3, 2, 1])
        cp_names = [cp for cp, _ in trace]
        idx_build_done = cp_names.index(BUILD_HEAP_DONE)
        assert HEAPIFY_SWAP not in cp_names[:idx_build_done]

    def test_extract_swap_fires_four_times(self):
        _, trace = heap_sort([5, 4, 3, 2, 1])
        count = sum(1 for cp, _ in trace if cp == EXTRACT_SWAP)
        assert count == 4


class TestHeapSortMultilevel:

    def test_result_is_sorted(self):
        result, _ = heap_sort([4, 10, 3, 5, 1])
        assert result == [1, 3, 4, 5, 10]

    def test_trace_matches_reference(self):
        _, trace = heap_sort([4, 10, 3, 5, 1])
        assert _simplify(trace) == REF_MULTILEVEL

    def test_swaps_during_build(self):
        _, trace = heap_sort([4, 10, 3, 5, 1])
        cp_names = [cp for cp, _ in trace]
        idx_build_done = cp_names.index(BUILD_HEAP_DONE)
        assert HEAPIFY_SWAP in cp_names[:idx_build_done]

    def test_extract_swap_fires_four_times(self):
        _, trace = heap_sort([4, 10, 3, 5, 1])
        count = sum(1 for cp, _ in trace if cp == EXTRACT_SWAP)
        assert count == 4


class TestStructuralInvariants:

    @pytest.mark.parametrize("arr", [
        [], [1], [2, 2, 2], [3, 1, 2], [5, 4, 3, 2, 1], [4, 10, 3, 5, 1],
    ])
    def test_trace_starts_with_sort_enter(self, arr):
        _, trace = heap_sort(arr)
        assert trace[0][0] == SORT_ENTER

    @pytest.mark.parametrize("arr", [
        [], [1], [2, 2, 2], [3, 1, 2], [5, 4, 3, 2, 1], [4, 10, 3, 5, 1],
    ])
    def test_trace_ends_with_sort_exit(self, arr):
        _, trace = heap_sort(arr)
        assert trace[-1][0] == SORT_EXIT

    @pytest.mark.parametrize("arr", [
        [], [1], [2, 2, 2], [3, 1, 2], [5, 4, 3, 2, 1], [4, 10, 3, 5, 1],
    ])
    def test_build_heap_done_appears_once(self, arr):
        _, trace = heap_sort(arr)
        count = sum(1 for cp, _ in trace if cp == BUILD_HEAP_DONE)
        assert count == 1

    @pytest.mark.parametrize("arr", [
        [], [1], [2, 2, 2], [3, 1, 2], [5, 4, 3, 2, 1], [4, 10, 3, 5, 1],
    ])
    def test_build_heap_done_before_first_extract_swap(self, arr):
        _, trace = heap_sort(arr)
        cp_names = [cp for cp, _ in trace]
        idx_build = cp_names.index(BUILD_HEAP_DONE)
        extract_indices = [i for i, cp in enumerate(cp_names) if cp == EXTRACT_SWAP]
        for ei in extract_indices:
            assert idx_build < ei

    @pytest.mark.parametrize("arr", [
        [], [1], [2, 2, 2], [3, 1, 2], [5, 4, 3, 2, 1], [4, 10, 3, 5, 1],
    ])
    def test_heapify_swap_always_preceded_by_heapify_enter(self, arr):
        _, trace = heap_sort(arr)
        for i, (cp, _) in enumerate(trace):
            if cp == HEAPIFY_SWAP:
                assert i > 0 and trace[i - 1][0] == HEAPIFY_ENTER

    @pytest.mark.parametrize("arr", [
        [], [1], [2, 2, 2], [3, 1, 2], [5, 4, 3, 2, 1], [4, 10, 3, 5, 1],
    ])
    def test_extract_swap_count_equals_n_minus_1(self, arr):
        _, trace = heap_sort(arr)
        count = sum(1 for cp, _ in trace if cp == EXTRACT_SWAP)
        assert count == max(0, len(arr) - 1)

    @pytest.mark.parametrize("arr", [
        [], [1], [2, 2, 2], [3, 1, 2], [5, 4, 3, 2, 1], [4, 10, 3, 5, 1],
    ])
    def test_original_not_mutated(self, arr):
        original = list(arr)
        heap_sort(arr)
        assert arr == original
