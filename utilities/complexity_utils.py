"""Shared helpers for Lecture 03 notebook materials.

The goal is consistency, not abstraction for its own sake. These helpers keep
the visual narrative aligned across notebooks:

- wide, projection-friendly figure sizes
- restrained academic colors
- readable fonts, labels, and line weights
- lightweight timing utilities for complexity experiments
- consistent markdown boxes for takeaways and discussion prompts
"""

from __future__ import annotations

import html
import textwrap
from time import perf_counter
from typing import Any, Callable, Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import HTML, display
from matplotlib.patches import FancyArrowPatch, Rectangle

COLORS = {
    "navy": "#1f3b5c",
    "teal": "#2f6f77",
    "rust": "#b45f36",
    "gold": "#c7a252",
    "gray": "#5c6770",
    "light_gray": "#d9dde1",
}

FIGURE_SIZES = {
    "wide": (11.0, 6.0),
    "tall": (8.5, 7.0),
    "square": (7.0, 7.0),
}


def setup_lecture_style() -> None:
    """Apply a consistent matplotlib style for Lecture 03 notebooks."""
    plt.rcParams.update(
        {
            "figure.figsize": FIGURE_SIZES["wide"],
            "figure.dpi": 120,
            "axes.titlesize": 18,
            "axes.titleweight": "semibold",
            "axes.labelsize": 13,
            "axes.labelcolor": COLORS["navy"],
            "axes.edgecolor": COLORS["gray"],
            "axes.linewidth": 1.1,
            "axes.grid": True,
            "axes.axisbelow": True,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.prop_cycle": plt.cycler(
                color=[
                    COLORS["navy"],
                    COLORS["teal"],
                    COLORS["rust"],
                    COLORS["gold"],
                    COLORS["gray"],
                ]
            ),
            "grid.color": COLORS["light_gray"],
            "grid.linewidth": 0.8,
            "grid.alpha": 0.8,
            "legend.frameon": False,
            "legend.fontsize": 11,
            "lines.linewidth": 2.6,
            "lines.markersize": 7,
            "font.size": 12,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
        }
    )


def lecture_figure(
    kind: str = "wide",
    *,
    nrows: int = 1,
    ncols: int = 1,
    sharex: bool = False,
    sharey: bool = False,
):
    """Create a figure with the lecture defaults and constrained layout."""
    figsize = FIGURE_SIZES.get(kind, FIGURE_SIZES["wide"])
    return plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=figsize,
        sharex=sharex,
        sharey=sharey,
        constrained_layout=True,
    )


def _draw_labeled_array(
    ax,
    values: Iterable[Any],
    *,
    facecolors: list[str] | None = None,
    title: str = "",
    value_prefix: str = "value",
    index_prefix: str = "index",
    extra_labels: list[str] | None = None,
) -> None:
    """Draw a one-row array with index, value, and optional extra labels."""
    values = list(values)
    if facecolors is None:
        facecolors = ["white"] * len(values)
    if extra_labels is None:
        extra_labels = [""] * len(values)

    for position, value in enumerate(values):
        box = Rectangle(
            (position, 0),
            1.0,
            1.0,
            facecolor=facecolors[position],
            edgecolor=COLORS["gray"],
            linewidth=1.4,
        )
        ax.add_patch(box)
        ax.text(position + 0.5, 0.58, str(value), ha="center", va="center", fontsize=12)
        ax.text(
            position + 0.5,
            1.15,
            f"{index_prefix}={position}",
            ha="center",
            va="bottom",
            fontsize=10,
        )
        ax.text(
            position + 0.5,
            -0.18,
            f"{value_prefix}={value}",
            ha="center",
            va="top",
            fontsize=10,
        )
        if extra_labels[position]:
            ax.text(position + 0.5, -0.52, extra_labels[position], ha="center", va="top", fontsize=10)

    ax.set_xlim(0, len(values))
    ax.set_ylim(-0.9, 1.9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(title, loc="left", pad=12, fontsize=15, color=COLORS["navy"])


def _add_pointer(ax, x: int, text: str, *, color: str, y: float = 1.42) -> None:
    """Add a pointer label above one array position."""
    ax.annotate(
        text,
        xy=(x + 0.5, 1.02),
        xytext=(x + 0.5, y),
        ha="center",
        va="bottom",
        color=color,
        fontsize=11,
        arrowprops={"arrowstyle": "->", "color": color, "linewidth": 1.6},
    )


def plot_linear_search_demo(
    values: Iterable[Any],
    target: Any,
    *,
    ax=None,
    title: str = "Linear search: one moving index",
):
    """Visualize linear search on one concrete example."""
    values = list(values)
    try:
        found_index = values.index(target)
    except ValueError:
        found_index = len(values) - 1

    if ax is None:
        _, ax = plt.subplots(figsize=FIGURE_SIZES["wide"], constrained_layout=True)

    facecolors = [COLORS["light_gray"]] * len(values)
    for seen in range(found_index + 1):
        facecolors[seen] = "#f2ddd3"
    if 0 <= found_index < len(values):
        facecolors[found_index] = "#f6c6b1"

    extra_labels = [
        "checked" if position < found_index else "match" if position == found_index else ""
        for position in range(len(values))
    ]
    _draw_labeled_array(ax, values, facecolors=facecolors, title=title, extra_labels=extra_labels)
    if 0 <= found_index < len(values):
        _add_pointer(ax, found_index, "index", color=COLORS["rust"])
    ax.text(
        0.15,
        1.72,
        f"target = {target}, comparisons = {found_index + 1}",
        ha="left",
        va="center",
        fontsize=11,
        color=COLORS["rust"],
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9, "pad": 1.5},
    )
    return ax


def plot_binary_search_demo(
    values: Iterable[Any],
    target: Any,
    *,
    ax=None,
    title: str = "Binary search: left, mid, right shrink the interval",
):
    """Visualize the final active interval of binary search before it finds target."""
    values = list(values)
    left = 0
    right = len(values) - 1
    comparisons = 0
    snapshot = None

    while left <= right:
        mid = (left + right) // 2
        comparisons += 1
        snapshot = (left, right, mid, comparisons)
        if values[mid] == target:
            break
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    if snapshot is None:
        raise ValueError("Cannot visualize binary search on an empty sequence.")

    left, right, mid, comparisons = snapshot

    if ax is None:
        _, ax = plt.subplots(figsize=FIGURE_SIZES["wide"], constrained_layout=True)

    facecolors = [COLORS["light_gray"]] * len(values)
    for position in range(left, right + 1):
        facecolors[position] = "#d9e8ea"
    facecolors[mid] = "#a9d0d5"

    extra_labels = []
    for position in range(len(values)):
        if position < left or position > right:
            extra_labels.append("discarded")
        elif position == left:
            extra_labels.append("left")
        elif position == mid:
            extra_labels.append("mid")
        elif position == right:
            extra_labels.append("right")
        else:
            extra_labels.append("active")

    _draw_labeled_array(ax, values, facecolors=facecolors, title=title, extra_labels=extra_labels)
    _add_pointer(ax, left, "left", color=COLORS["teal"])
    _add_pointer(ax, mid, "mid", color=COLORS["navy"], y=1.48)
    _add_pointer(ax, right, "right", color=COLORS["gold"])
    ax.text(
        0.15,
        1.72,
        f"target = {target}, comparisons so far = {comparisons}",
        ha="left",
        va="center",
        fontsize=11,
        color=COLORS["navy"],
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9, "pad": 1.5},
    )
    return ax


def insertion_sort_trace(values: Iterable[Any]) -> list[dict[str, Any]]:
    """Return the before/after state of each insertion-sort pass."""
    data = list(values)
    trace = [
        {
            "label": "Initially",
            "before": data.copy(),
            "after": data.copy(),
            "source_index": None,
            "target_index": None,
        }
    ]

    ordinal_names = {
        1: "First Pass",
        2: "Second Pass",
        3: "Third Pass",
        4: "Fourth Pass",
        5: "Fifth Pass",
        6: "Sixth Pass",
        7: "Seventh Pass",
        8: "Eighth Pass",
    }

    for i in range(1, len(data)):
        before = data.copy()
        key = data[i]
        j = i - 1

        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            j -= 1

        target_index = j + 1
        data[target_index] = key
        trace.append(
            {
                "label": ordinal_names.get(i, f"Pass {i}"),
                "before": before,
                "after": data.copy(),
                "source_index": i,
                "target_index": target_index,
            }
        )

    return trace


def plot_insertion_sort_passes(
    values: Iterable[Any],
    *,
    ax=None,
    title: str = "Insertion sort: all passes for one concrete array",
):
    """Plot insertion-sort passes in a step-by-step classroom-friendly layout."""
    trace = insertion_sort_trace(values)
    values = list(values)
    n = len(values)

    if ax is None:
        _, ax = plt.subplots(figsize=(11.5, max(4.5, 1.35 * len(trace))), constrained_layout=True)

    label_x = 0.0
    label_w = 2.25
    before_x = 2.7
    arrow_x = before_x + n + 0.55
    after_x = before_x + n + 1.45
    cell_h = 0.8
    row_gap = 1.15
    top_y = row_gap * (len(trace) - 1)

    def draw_row(x0: float, y0: float, row_values: list[Any], *, highlight=None, sorted_prefix: int = 0):
        for idx, value in enumerate(row_values):
            facecolor = "white"
            if sorted_prefix and idx < sorted_prefix:
                facecolor = "#eef4eb"
            if highlight is not None and idx == highlight:
                facecolor = "#f6e3b3"

            rect = Rectangle(
                (x0 + idx, y0),
                1.0,
                cell_h,
                facecolor=facecolor,
                edgecolor=COLORS["gray"],
                linewidth=1.2,
            )
            ax.add_patch(rect)
            ax.text(x0 + idx + 0.5, y0 + cell_h / 2, str(value), ha="center", va="center", fontsize=15)

    for row_index, row in enumerate(trace):
        y = top_y - row_index * row_gap

        label_rect = Rectangle(
            (label_x, y + 0.05),
            label_w,
            0.7,
            facecolor="#b8bfce",
            edgecolor=COLORS["gray"],
            linewidth=1.2,
        )
        ax.add_patch(label_rect)
        ax.text(label_x + label_w / 2, y + 0.4, row["label"], ha="center", va="center", fontsize=14)

        highlight = row["source_index"]
        sorted_prefix = row["target_index"] + 1 if row["target_index"] is not None else 0

        draw_row(before_x, y, row["before"], highlight=highlight)
        ax.text(arrow_x, y + cell_h / 2, "→", ha="center", va="center", fontsize=28, color="black")
        draw_row(after_x, y, row["after"], sorted_prefix=sorted_prefix)

        if row["source_index"] is not None:
            source_x = before_x + row["source_index"] + 0.5
            target_x = after_x + row["target_index"] + 0.5
            arrow = FancyArrowPatch(
                (source_x, y - 0.06),
                (target_x, y - 0.06),
                connectionstyle="arc3,rad=-0.55",
                arrowstyle="->",
                mutation_scale=14,
                linewidth=1.4,
                color="black",
            )
            ax.add_patch(arrow)

    ax.set_xlim(-0.15, after_x + n + 0.2)
    ax.set_ylim(-0.7, top_y + 1.25)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(title, loc="left")
    return ax


def merge_sort_trace(values: Iterable[Any]) -> dict[str, Any]:
    """Return a recursive trace of merge sort with both divide and merge states."""
    data = list(values)
    if len(data) <= 1:
        return {"input": data, "output": data, "left": None, "right": None}

    middle = len(data) // 2
    left = merge_sort_trace(data[:middle])
    right = merge_sort_trace(data[middle:])

    merged = []
    i = 0
    j = 0
    while i < len(left["output"]) and j < len(right["output"]):
        if left["output"][i] <= right["output"][j]:
            merged.append(left["output"][i])
            i += 1
        else:
            merged.append(right["output"][j])
            j += 1
    merged.extend(left["output"][i:])
    merged.extend(right["output"][j:])

    return {"input": data, "output": merged, "left": left, "right": right}


def plot_merge_sort_decomposition(
    values: Iterable[Any],
    *,
    ax=None,
    title: str = "Merge sort: divide, then conquer and merge",
):
    """Plot a merge-sort decomposition in separate divide and merge zones."""
    tree = merge_sort_trace(values)

    leaf_gap = 1.9
    cell_w = 0.72
    cell_h = 0.62
    divide_top = 5.8
    divide_gap = 1.05
    merge_base = 0.9
    merge_gap = 1.05

    def assign_layout(node: dict[str, Any], depth: int, cursor: list[int]) -> None:
        node["depth"] = depth
        if node["left"] is None:
            node["x"] = cursor[0] * leaf_gap
            node["height"] = 0
            cursor[0] += 1
            return

        assign_layout(node["left"], depth + 1, cursor)
        assign_layout(node["right"], depth + 1, cursor)
        node["x"] = 0.5 * (node["left"]["x"] + node["right"]["x"])
        node["height"] = 1 + max(node["left"]["height"], node["right"]["height"])

    assign_layout(tree, 0, [0])
    max_depth = max(
        node["depth"]
        for node in [tree]
        + [tree["left"], tree["right"]]
        if node is not None
    )

    def walk(node: dict[str, Any]):
        yield node
        if node["left"] is not None:
            yield from walk(node["left"])
            yield from walk(node["right"])

    all_nodes = list(walk(tree))
    max_depth = max(node["depth"] for node in all_nodes)
    max_height = max(node["height"] for node in all_nodes)

    if ax is None:
        _, ax = plt.subplots(figsize=(11.8, 7.2), constrained_layout=True)

    def node_width(row_values: list[Any]) -> float:
        return cell_w * len(row_values)

    def draw_array_node(
        x: float,
        y: float,
        row_values: list[Any],
        *,
        color: str = "white",
        text_color: str = "black",
    ) -> tuple[float, float]:
        width = node_width(row_values)
        left = x - width / 2
        for index, value in enumerate(row_values):
            rect = Rectangle(
                (left + cell_w * index, y - cell_h / 2),
                cell_w,
                cell_h,
                facecolor=color,
                edgecolor=COLORS["gray"],
                linewidth=1.2,
            )
            ax.add_patch(rect)
            ax.text(
                left + cell_w * index + cell_w / 2,
                y,
                str(value),
                ha="center",
                va="center",
                fontsize=14,
                color=text_color,
            )
        return left, width

    input_anchor: dict[int, tuple[float, float]] = {}
    output_anchor: dict[int, tuple[float, float]] = {}

    # Draw divide-phase nodes from top to bottom.
    for node in sorted(all_nodes, key=lambda item: item["depth"]):
        y = divide_top - divide_gap * node["depth"]
        _, width = draw_array_node(node["x"], y, node["input"], color="white")
        input_anchor[id(node)] = (node["x"], y, width)

    # Draw merge outputs from bottom to top for internal nodes only.
    internal_nodes = [node for node in all_nodes if node["left"] is not None]
    for node in sorted(internal_nodes, key=lambda item: item["height"]):
        y = merge_base + merge_gap * (max_height - node["height"])
        color = "#37a354" if node is tree else "#dff0d8"
        text_color = "white" if node is tree else "black"
        _, width = draw_array_node(node["x"], y, node["output"], color=color, text_color=text_color)
        output_anchor[id(node)] = (node["x"], y, width)

    def connect(start: tuple[float, float], end: tuple[float, float]) -> None:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=11,
                linewidth=1.4,
                color="black",
                shrinkA=0,
                shrinkB=0,
            )
        )

    def draw_edges(node: dict[str, Any]) -> None:
        if node["left"] is None:
            return

        parent_x, parent_y, _ = input_anchor[id(node)]
        left_x, left_y, _ = input_anchor[id(node["left"])]
        right_x, right_y, _ = input_anchor[id(node["right"])]
        connect((parent_x, parent_y - cell_h / 2), (left_x, left_y + cell_h / 2))
        connect((parent_x, parent_y - cell_h / 2), (right_x, right_y + cell_h / 2))

        left_merge = output_anchor.get(id(node["left"]))
        right_merge = output_anchor.get(id(node["right"]))
        parent_merge = output_anchor[id(node)]

        left_start = (left_merge[0], left_merge[1] - cell_h / 2) if left_merge else (left_x, left_y - cell_h / 2)
        right_start = (right_merge[0], right_merge[1] - cell_h / 2) if right_merge else (right_x, right_y - cell_h / 2)
        connect(left_start, (parent_merge[0], parent_merge[1] + cell_h / 2))
        connect(right_start, (parent_merge[0], parent_merge[1] + cell_h / 2))

        draw_edges(node["left"])
        draw_edges(node["right"])

    draw_edges(tree)

    root_input_x, root_input_y, root_input_w = input_anchor[id(tree)]
    root_output_x, root_output_y, root_output_w = output_anchor[id(tree)]
    ax.text(root_input_x - root_input_w / 2 - 0.15, root_input_y, "Unsorted Array:", ha="right", va="center", fontsize=15)
    ax.text(root_output_x - root_output_w / 2 - 0.15, root_output_y, "Sorted Array:", ha="right", va="center", fontsize=15)

    x_bracket = max(node["x"] + node_width(node["input"]) / 2 for node in all_nodes) + 1.0
    divide_top_y = divide_top + 0.35
    divide_bottom_y = divide_top - divide_gap * max_depth - 0.35
    ax.plot([x_bracket, x_bracket], [divide_top_y, divide_bottom_y], linestyle=(0, (2, 2)), color="black", linewidth=1.2)
    ax.plot([x_bracket - 0.42, x_bracket], [divide_top_y, divide_top_y], linestyle=(0, (2, 2)), color="black", linewidth=1.2)
    ax.plot([x_bracket - 0.42, x_bracket], [divide_bottom_y, divide_bottom_y], linestyle=(0, (2, 2)), color="black", linewidth=1.2)
    ax.text(x_bracket + 0.22, 0.5 * (divide_top_y + divide_bottom_y), "Divide", fontsize=16, va="center")

    merge_top_y = max(y for _, y, _ in output_anchor.values()) + 0.35
    merge_bottom_y = root_output_y - 0.35
    ax.plot([x_bracket, x_bracket], [merge_top_y, merge_bottom_y], linestyle=(0, (2, 2)), color="black", linewidth=1.2)
    ax.plot([x_bracket - 0.42, x_bracket], [merge_top_y, merge_top_y], linestyle=(0, (2, 2)), color="black", linewidth=1.2)
    ax.plot([x_bracket - 0.42, x_bracket], [merge_bottom_y, merge_bottom_y], linestyle=(0, (2, 2)), color="black", linewidth=1.2)
    ax.text(x_bracket + 0.22, 0.5 * (merge_top_y + merge_bottom_y), "Conquer\n& Merge", fontsize=16, va="center")

    min_x = min(node["x"] - node_width(node["input"]) / 2 for node in all_nodes) - 1.2
    max_x = x_bracket + 1.8
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(root_output_y - 0.8, divide_top + 0.9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(title, loc="left", pad=10)
    return ax


def plot_preprocessing_workflow(
    system_n: int,
    *,
    ax=None,
    title: str = "Two workflows: repeated linear search vs preprocessing then binary search",
):
    """Plot the end-to-end workflow comparison used in the preprocessing section."""
    if ax is None:
        _, ax = plt.subplots(figsize=FIGURE_SIZES["wide"], constrained_layout=True)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    def workflow_box(x: float, y: float, text: str, color: str) -> None:
        rect = Rectangle(
            (x, y),
            2.2,
            0.8,
            facecolor=color,
            edgecolor=COLORS["gray"],
            linewidth=1.4,
        )
        ax.add_patch(rect)
        ax.text(x + 1.1, y + 0.4, text, ha="center", va="center", fontsize=11)

    workflow_box(0.4, 3.2, f"system_data\n(length = {system_n})", "#e8eef5")
    workflow_box(3.3, 3.2, "linear_search(system_data, target)", "#f2ddd3")
    workflow_box(6.3, 3.2, "repeat query_count times", "#f2ddd3")

    workflow_box(0.4, 1.2, f"system_data\n(length = {system_n})", "#e8eef5")
    workflow_box(3.0, 1.2, "prepared = sorted(system_data)", "#d9e8ea")
    workflow_box(6.3, 1.2, "binary_search(prepared, target)", "#f6e3b3")

    ax.annotate("", xy=(3.3, 3.6), xytext=(2.6, 3.6), arrowprops={"arrowstyle": "->", "linewidth": 1.8, "color": COLORS["gray"]})
    ax.annotate("", xy=(6.3, 3.6), xytext=(5.5, 3.6), arrowprops={"arrowstyle": "->", "linewidth": 1.8, "color": COLORS["gray"]})
    ax.annotate("", xy=(3.0, 1.6), xytext=(2.6, 1.6), arrowprops={"arrowstyle": "->", "linewidth": 1.8, "color": COLORS["gray"]})
    ax.annotate("", xy=(6.3, 1.6), xytext=(5.2, 1.6), arrowprops={"arrowstyle": "->", "linewidth": 1.8, "color": COLORS["gray"]})

    ax.text(8.9, 3.6, "cost paid\nevery query", ha="center", va="center", fontsize=11, color=COLORS["rust"])
    ax.text(8.9, 1.6, "one-time sort\nthen cheap queries", ha="center", va="center", fontsize=11, color=COLORS["navy"])
    ax.set_title(title, loc="left")
    return ax


def adjacency_matrix_from_list(
    adj_list: dict[Any, list[Any]],
    node_order: list[Any] | None = None,
) -> tuple[np.ndarray, list[Any]]:
    """Convert an adjacency-list graph into a dense 0/1 adjacency matrix."""
    if node_order is None:
        node_order = list(adj_list.keys())

    index = {node: position for position, node in enumerate(node_order)}
    matrix = np.zeros((len(node_order), len(node_order)), dtype=int)
    for source, neighbors in adj_list.items():
        i = index[source]
        for target in neighbors:
            j = index[target]
            matrix[i, j] = 1
    return matrix, node_order


def _draw_small_graph(
    ax,
    adj_list: dict[Any, list[Any]],
    positions: dict[Any, tuple[float, float]],
    *,
    title: str = "",
    parent: dict[Any, Any] | None = None,
    order: list[Any] | None = None,
    subtitle: str | None = None,
) -> None:
    """Draw a small stable-layout graph with optional traversal highlights."""
    seen_edges: set[tuple[Any, Any]] = set()
    parent_edges = set()
    if parent is not None:
        parent_edges = {
            tuple(sorted((node, predecessor)))
            for node, predecessor in parent.items()
            if predecessor is not None
        }

    for source, neighbors in adj_list.items():
        x0, y0 = positions[source]
        for target in neighbors:
            edge = tuple(sorted((source, target)))
            if edge in seen_edges:
                continue
            seen_edges.add(edge)
            x1, y1 = positions[target]
            color = COLORS["light_gray"]
            linewidth = 2.0
            zorder = 1
            if edge in parent_edges:
                color = COLORS["navy"]
                linewidth = 3.0
                zorder = 2
            ax.plot([x0, x1], [y0, y1], color=color, linewidth=linewidth, zorder=zorder)

    order_map = {node: idx + 1 for idx, node in enumerate(order)} if order is not None else {}
    for node, (x, y) in positions.items():
        facecolor = "#eef4eb" if node in order_map else "white"
        circle = plt.Circle((x, y), 0.17, facecolor=facecolor, edgecolor=COLORS["gray"], linewidth=1.4, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, str(node), ha="center", va="center", fontsize=13, zorder=4)
        if node in order_map:
            badge = plt.Circle((x, y + 0.28), 0.11, facecolor=COLORS["navy"], edgecolor="white", linewidth=1.0, zorder=5)
            ax.add_patch(badge)
            ax.text(x, y + 0.28, str(order_map[node]), ha="center", va="center", fontsize=10, color="white", zorder=6)

    if subtitle:
        ax.text(0.0, 1.02, subtitle, transform=ax.transAxes, ha="left", va="bottom", fontsize=11, color=COLORS["gray"])

    ax.set_title(title, loc="left")
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)


def _annotated_heatmap(
    ax,
    matrix: np.ndarray,
    labels: list[Any],
    *,
    title: str,
    cmap: str = "Greens",
    annotate: bool = True,
) -> None:
    """Draw a readable 0/1 heatmap with optional cell annotations."""
    ax.imshow(matrix, cmap=cmap, vmin=0, vmax=max(1, int(np.max(matrix))), aspect="equal")
    ax.set_title(title, loc="left")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.tick_params(axis="x", rotation=0)
    ax.grid(False)
    if annotate and matrix.shape[0] <= 12:
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                value = matrix[i, j]
                ax.text(j, i, str(int(value)), ha="center", va="center", fontsize=10, color="black")


def plot_representation_views(
    adj_list: dict[Any, list[Any]],
    positions: dict[Any, tuple[float, float]],
    *,
    node_order: list[Any] | None = None,
    title: str = "Two ways to store the same graph",
):
    """Show one graph as a node-link diagram, adjacency list, and adjacency matrix."""
    matrix, labels = adjacency_matrix_from_list(adj_list, node_order=node_order)
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 5.2), constrained_layout=True, gridspec_kw={"width_ratios": [1.1, 0.95, 1.2]})

    _draw_small_graph(axes[0], adj_list, positions, title="Same graph as a node-link picture")
    axes[0].set_xlim(min(x for x, _ in positions.values()) - 0.45, max(x for x, _ in positions.values()) + 0.45)
    axes[0].set_ylim(min(y for _, y in positions.values()) - 0.45, max(y for _, y in positions.values()) + 0.5)

    axes[1].set_title("Adjacency list", loc="left")
    axes[1].axis("off")
    list_lines = [f"{node}: {adj_list[node]}" for node in labels]
    axes[1].text(
        0.0,
        1.0,
        "\n".join(list_lines),
        ha="left",
        va="top",
        fontsize=13,
        family="monospace",
        transform=axes[1].transAxes,
    )

    _annotated_heatmap(axes[2], matrix, labels, title="Adjacency matrix")
    fig.suptitle(title, x=0.06, ha="left", fontsize=18, fontweight="semibold")
    return fig, axes


def plot_sparsity_heatmaps(
    sparse_matrix: np.ndarray,
    dense_matrix: np.ndarray,
    *,
    sparse_title: str = "Sparse graph occupancy",
    dense_title: str = "Dense graph occupancy",
    title: str = "Sparse vs dense graphs",
):
    """Compare sparse and dense adjacency matrices side by side."""
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2), constrained_layout=True)
    labels = list(range(sparse_matrix.shape[0]))
    _annotated_heatmap(axes[0], sparse_matrix, labels, title=sparse_title, annotate=False)
    _annotated_heatmap(axes[1], dense_matrix, labels, title=dense_title, annotate=False)

    sparse_fill = float(np.count_nonzero(sparse_matrix) / sparse_matrix.size)
    dense_fill = float(np.count_nonzero(dense_matrix) / dense_matrix.size)
    axes[0].text(0.0, 1.02, f"occupied cells = {sparse_fill:.1%}", transform=axes[0].transAxes, ha="left", va="bottom", fontsize=11, color=COLORS["gray"])
    axes[1].text(0.0, 1.02, f"occupied cells = {dense_fill:.1%}", transform=axes[1].transAxes, ha="left", va="bottom", fontsize=11, color=COLORS["gray"])
    fig.suptitle(title, x=0.06, ha="left", fontsize=18, fontweight="semibold")
    return fig, axes


def plot_traversal_graph(
    adj_list: dict[Any, list[Any]],
    positions: dict[Any, tuple[float, float]],
    order: list[Any],
    parent: dict[Any, Any],
    *,
    title: str,
    subtitle: str | None = None,
):
    """Show BFS/DFS order on a small stable-layout graph."""
    fig, ax = plt.subplots(figsize=(7.8, 5.2), constrained_layout=True)
    _draw_small_graph(ax, adj_list, positions, title=title, parent=parent, order=order, subtitle=subtitle)
    ax.set_xlim(min(x for x, _ in positions.values()) - 0.45, max(x for x, _ in positions.values()) + 0.45)
    ax.set_ylim(min(y for _, y in positions.values()) - 0.45, max(y for _, y in positions.values()) + 0.55)
    return fig, ax


def plot_grouped_bars(
    categories: list[Any],
    series: dict[str, Iterable[float]],
    *,
    title: str,
    ylabel: str,
):
    """Plot a grouped bar chart for a small set of comparison series."""
    categories = list(categories)
    series = {name: list(values) for name, values in series.items()}
    fig, ax = plt.subplots(figsize=FIGURE_SIZES["wide"], constrained_layout=True)
    x = np.arange(len(categories), dtype=float)
    width = 0.8 / max(len(series), 1)

    for offset, (name, values) in enumerate(series.items()):
        positions = x - 0.4 + width / 2 + offset * width
        ax.bar(positions, values, width=width, label=name)

    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel(ylabel)
    ax.set_title(title, loc="left")
    ax.legend(loc="upper left")
    return fig, ax


def plot_cost_tradeoff_summary(
    summary_df: pd.DataFrame,
    *,
    category_col: str = "scenario",
    memory_col: str = "memory_units",
    traversal_col: str = "edge_checks",
    title: str = "What costs dominate depends on graph structure and representation",
):
    """Plot memory cost and traversal work side by side for a small scenario table."""
    categories = summary_df[category_col].tolist()
    memory_values = summary_df[memory_col].tolist()
    traversal_values = summary_df[traversal_col].tolist()

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.2), constrained_layout=True)
    x = np.arange(len(categories))

    axes[0].bar(x, memory_values, color=COLORS["navy"])
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(categories, rotation=15, ha="right")
    axes[0].set_title("Estimated memory footprint", loc="left")
    axes[0].set_ylabel("Storage units")

    axes[1].bar(x, traversal_values, color=COLORS["teal"])
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(categories, rotation=15, ha="right")
    axes[1].set_title("Traversal work in BFS", loc="left")
    axes[1].set_ylabel("Neighbor / cell checks")

    fig.suptitle(title, x=0.06, ha="left", fontsize=18, fontweight="semibold")
    return fig, axes


def plot_growth_story(
    n_values: Iterable[float],
    series: dict[str, Iterable[float]],
    *,
    title: str = "Some growth laws stay manageable, others explode",
):
    """Show the same growth curves on linear and log scales."""
    n_values = np.asarray(list(n_values), dtype=float)
    series = {label: np.asarray(list(values), dtype=float) for label, values in series.items()}

    fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.3), constrained_layout=True)
    for label, values in series.items():
        axes[0].plot(n_values, values, marker="o", label=label)
        axes[1].plot(n_values, values, marker="o", label=label)

    axes[0].set_title("Linear scale", loc="left")
    axes[0].set_xlabel("Input size n")
    axes[0].set_ylabel("Relative work")

    axes[1].set_title("Log y-scale", loc="left")
    axes[1].set_xlabel("Input size n")
    axes[1].set_ylabel("Relative work")
    axes[1].set_yscale("log")

    for ax in axes:
        ax.legend(loc="upper left")

    fig.suptitle(title, x=0.06, ha="left", fontsize=18, fontweight="semibold")
    return fig, axes


def plot_search_space_growth(
    sizes: Iterable[Any],
    counts: Iterable[float],
    *,
    title: str = "Brute force means paying for every candidate",
    ylabel: str = "Number of candidates",
):
    """Plot brute-force search space growth on a log scale."""
    sizes = list(sizes)
    counts = np.asarray(list(counts), dtype=float)
    fig, ax = plt.subplots(figsize=FIGURE_SIZES["wide"], constrained_layout=True)
    x = np.arange(len(sizes))
    ax.bar(x, counts, color=COLORS["rust"])
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.set_yscale("log")
    ax.set_xlabel("Problem size")
    ax.set_ylabel(ylabel)
    ax.set_title(title, loc="left")

    for position, value in zip(x, counts):
        ax.text(
            position,
            value * 1.08,
            f"{int(value):,}",
            ha="center",
            va="bottom",
            fontsize=10,
            color=COLORS["gray"],
        )
    return fig, ax


def plot_subset_sum_workflow(
    numbers: Iterable[int],
    candidate_mask: Iterable[int],
    target: int,
    *,
    ax=None,
    title: str = "Finding a subset and checking a subset are very different jobs",
):
    """Compare exhaustive search with verification for one subset-sum example."""
    numbers = list(numbers)
    candidate_mask = [bool(flag) for flag in candidate_mask]
    selected_numbers = [value for value, keep in zip(numbers, candidate_mask) if keep]
    candidate_sum = sum(selected_numbers)

    if ax is None:
        _, ax = plt.subplots(figsize=(12.6, 5.8), constrained_layout=True)

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    def box(x: float, y: float, w: float, h: float, text: str, *, color: str) -> None:
        rect = Rectangle((x, y), w, h, facecolor=color, edgecolor=COLORS["gray"], linewidth=1.3)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=12)

    ax.text(0.4, 4.55, "Solve", fontsize=16, color=COLORS["rust"], fontweight="semibold")
    box(0.4, 3.25, 2.4, 0.82, f"numbers = {numbers}", color="#f3ece8")
    box(3.35, 3.25, 2.2, 0.82, f"enumerate all\n{2 ** len(numbers):,} subsets", color="#f6d9cc")
    box(6.05, 3.25, 2.35, 0.82, "compute each sum", color="#f6d9cc")
    box(8.95, 3.25, 2.25, 0.82, f"stop when sum = {target}", color="#f6c6b1")

    ax.text(0.4, 1.95, "Verify", fontsize=16, color=COLORS["navy"], fontweight="semibold")
    box(0.4, 0.72, 2.4, 0.82, f"candidate mask\n= {candidate_mask}", color="#e7eef6")
    box(3.35, 0.72, 2.45, 0.82, f"selected = {selected_numbers}", color="#d9e8ea")
    box(6.35, 0.72, 2.0, 0.82, f"sum = {candidate_sum}", color="#d9e8ea")
    box(8.95, 0.72, 2.25, 0.82, f"compare with {target}", color="#cfe0e9")

    for y in (3.66, 1.13):
        ax.annotate("", xy=(3.35, y), xytext=(2.8, y), arrowprops={"arrowstyle": "->", "linewidth": 1.7, "color": COLORS["gray"]})
        ax.annotate("", xy=(6.05 if y > 2 else 6.35, y), xytext=(5.55 if y > 2 else 5.8, y), arrowprops={"arrowstyle": "->", "linewidth": 1.7, "color": COLORS["gray"]})
        ax.annotate("", xy=(8.95, y), xytext=(8.4 if y > 2 else 8.35, y), arrowprops={"arrowstyle": "->", "linewidth": 1.7, "color": COLORS["gray"]})

    ax.text(10.1, 4.47, "many candidates", ha="center", va="center", fontsize=11, color=COLORS["rust"])
    ax.text(10.1, 2.17, "one candidate", ha="center", va="center", fontsize=11, color=COLORS["navy"])
    ax.set_title(title, loc="left")
    return ax


def plot_problem_class_map(
    *,
    title: str = "Problem classes are a map, not a magic ladder",
):
    """Draw a clean card-based map for P, NP, NP-hard, and NP-complete."""
    fig, ax = plt.subplots(figsize=(13.0, 6.2), constrained_layout=True)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    cards = [
        (
            0.45,
            3.9,
            3.2,
            2.2,
            "#e7eef6",
            "P",
            "Polynomial-time solvable\nProblems with algorithms\nthat scale reasonably well",
        ),
        (
            4.0,
            3.9,
            3.35,
            2.2,
            "#d9e8ea",
            "NP",
            "Nondeterministic polynomial-time\nProblems where a proposed\nsolution can be checked quickly",
        ),
        (
            7.75,
            3.9,
            3.75,
            2.2,
            "#f6d9cc",
            "NP-hard",
            "Non-deterministic polynomial-time hard\nAt least as hard as the\nhardest problems in NP",
        ),
        (
            4.55,
            0.9,
            3.55,
            2.15,
            "#f6e3b3",
            "NP-complete",
            "Non-deterministic polynomial-time complete\nProblems inside NP that are\nalso NP-hard",
        ),
    ]

    for x, y, w, h, color, label, body in cards:
        rect = Rectangle((x, y), w, h, facecolor=color, edgecolor=COLORS["gray"], linewidth=1.4)
        ax.add_patch(rect)
        ax.text(x + 0.25, y + h - 0.35, label, ha="left", va="top", fontsize=15, color=COLORS["navy"], fontweight="semibold")
        ax.text(x + 0.25, y + h - 0.82, body, ha="left", va="top", fontsize=10.5)

    ax.annotate("", xy=(4.0, 5.0), xytext=(3.5, 5.0), arrowprops={"arrowstyle": "->", "linewidth": 1.7, "color": COLORS["gray"]})
    ax.annotate("", xy=(7.7, 5.0), xytext=(7.2, 5.0), arrowprops={"arrowstyle": "->", "linewidth": 1.7, "color": COLORS["gray"]})
    ax.annotate("", xy=(6.3, 3.9), xytext=(6.3, 3.15), arrowprops={"arrowstyle": "->", "linewidth": 1.7, "color": COLORS["gray"]})

    ax.text(6.0, 6.5, "Moving right means stronger hardness claims, not guaranteed efficient algorithms.", ha="center", va="center", fontsize=11, color=COLORS["gray"])
    ax.text(
        6.35,
        0.38,
        "NP-complete is the overlap: efficiently checkable, but as hard as any problem in NP.",
        ha="center",
        va="center",
        fontsize=10.5,
        color=COLORS["gray"],
    )
    ax.set_title(title, loc="left")
    return fig, ax


def plot_bounded_error_amplification(
    repeats: Iterable[int],
    error_series: dict[str, Iterable[float]],
    *,
    title: str = "Bounded-error algorithms can often be amplified",
):
    """Plot how repeating an imperfect procedure can reduce error."""
    repeats = np.asarray(list(repeats), dtype=int)
    error_series = {label: np.asarray(list(values), dtype=float) for label, values in error_series.items()}

    fig, ax = plt.subplots(figsize=FIGURE_SIZES["wide"], constrained_layout=True)
    for label, values in error_series.items():
        ax.plot(repeats, values, marker="o", label=label)

    ax.set_xlabel("Odd number of repeated runs")
    ax.set_ylabel("Probability majority vote is wrong")
    ax.set_title(title, loc="left")
    ax.legend(loc="upper right")
    return fig, ax


def plot_claim_checklist(
    claims: Iterable[dict[str, str]],
    *,
    title: str = "Misconceptions to avoid",
):
    """Display misconception claims and their corrections as large readable cards."""
    claims = list(claims)
    fig, ax = plt.subplots(figsize=(14.5, max(5.8, 2.0 * len(claims))), constrained_layout=True)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 2.05 * len(claims) + 0.7)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    top_y = 1.8 * len(claims)
    for index, row in enumerate(claims):
        y = top_y - 1.8 * index
        left = Rectangle((0.45, y), 5.25, 1.28, facecolor="#f6d9cc", edgecolor=COLORS["gray"], linewidth=1.3)
        right = Rectangle((6.2, y), 6.55, 1.28, facecolor="#e7eef6", edgecolor=COLORS["gray"], linewidth=1.3)
        ax.add_patch(left)
        ax.add_patch(right)
        claim_text = textwrap.fill(row["claim"], width=34, break_long_words=False, break_on_hyphens=False)
        correction_text = textwrap.fill(row["correction"], width=46, break_long_words=False, break_on_hyphens=False)

        ax.text(0.62, y + 0.98, "Misleading claim", ha="left", va="center", fontsize=11, color=COLORS["rust"], fontweight="semibold")
        ax.text(6.5, y + 0.98, "Safer framing", ha="left", va="center", fontsize=11, color=COLORS["navy"], fontweight="semibold")

        claim_artist = ax.text(
            0.62,
            y + 0.72,
            claim_text,
            ha="left",
            va="top",
            fontsize=10.8,
            linespacing=1.2,
            clip_on=True,
        )
        claim_artist.set_clip_path(left)

        correction_artist = ax.text(
            6.5,
            y + 0.72,
            correction_text,
            ha="left",
            va="top",
            fontsize=10.8,
            linespacing=1.2,
            clip_on=True,
        )
        correction_artist.set_clip_path(right)

    ax.set_title(title, loc="left")
    return fig, ax


def plot_abstraction_gap(
    *,
    title: str = "A quantum algorithm on a slide is only one layer of the real workflow",
):
    """Contrast an abstract circuit view with a fuller execution pipeline view."""
    fig, ax = plt.subplots(figsize=(13.2, 5.4), constrained_layout=True)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    def box(x: float, y: float, w: float, h: float, text: str, color: str, *, fontsize: float = 11.5):
        rect = Rectangle((x, y), w, h, facecolor=color, edgecolor=COLORS["gray"], linewidth=1.3)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize)

    ax.text(1.8, 5.35, "Abstract view", fontsize=15, color=COLORS["navy"], fontweight="semibold")
    box(0.55, 3.2, 3.3, 1.2, "problem -> ideal circuit -> complexity claim", "#e7eef6")
    box(1.1, 1.35, 2.2, 0.9, "good for theory", "#d9e8ea")

    ax.text(8.9, 5.35, "Execution view", fontsize=15, color=COLORS["rust"], fontweight="semibold")
    stages = [
        (5.25, 4.0, "encoding"),
        (7.15, 4.0, "logical circuit"),
        (9.05, 4.0, "mapping"),
        (10.95, 4.0, "execution"),
        (6.2, 2.3, "routing / device constraints"),
        (9.15, 2.3, "shots + post-processing"),
    ]
    for x, y, label in stages:
        box(x, y, 1.65, 0.9, label, "#f6e3b3" if "logical" in label else "#f6d9cc", fontsize=10.8)

    arrows = [
        ((3.95, 3.8), (5.25, 4.45)),
        ((6.9, 4.45), (7.15, 4.45)),
        ((8.8, 4.45), (9.05, 4.45)),
        ((10.7, 4.45), (10.95, 4.45)),
        ((7.95, 3.95), (7.0, 3.2)),
        ((9.9, 3.95), (9.95, 3.2)),
    ]
    for start, end in arrows:
        ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "linewidth": 1.7, "color": COLORS["gray"]})

    ax.text(8.85, 1.05, "Useful systems question:\nwhat remains of the advantage after full-stack cost is included?", ha="center", va="center", fontsize=11, color=COLORS["gray"])
    ax.set_title(title, loc="left")
    return fig, ax


def plot_quantum_pipeline(
    stages: Iterable[str],
    *,
    title: str = "From classical problem to quantum workflow",
):
    """Draw a clear left-to-right execution pipeline."""
    stages = list(stages)
    fig, ax = plt.subplots(figsize=(14.5, 4.6), constrained_layout=True)
    ax.set_ylim(0, 3.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    x = 0.5
    positions = []
    for index, stage in enumerate(stages):
        width = 1.25 if len(stage) < 12 else 1.55
        rect = Rectangle(
            (x, 1.2),
            width,
            0.9,
            facecolor="#e7eef6" if index in (0, len(stages) - 1) else "#f6e3b3",
            edgecolor=COLORS["gray"],
            linewidth=1.3,
        )
        ax.add_patch(rect)
        ax.text(x + width / 2, 1.65, textwrap.fill(stage, width=14), ha="center", va="center", fontsize=10.8)
        positions.append((x, width))
        x += width + 0.38

    ax.set_xlim(0, x + 0.2)

    for (x0, w0), (x1, _) in zip(positions[:-1], positions[1:]):
        ax.annotate("", xy=(x1, 1.65), xytext=(x0 + w0, 1.65), arrowprops={"arrowstyle": "->", "linewidth": 1.7, "color": COLORS["gray"]})

    ax.text(positions[0][0] + positions[0][1] / 2, 0.7, "problem definition", ha="center", va="center", fontsize=10.5, color=COLORS["gray"])
    ax.text(positions[-1][0] + positions[-1][1] / 2, 0.7, "usable classical answer", ha="center", va="center", fontsize=10.5, color=COLORS["gray"])
    ax.set_title(title, loc="left")
    return fig, ax


def plot_component_tradeoff(
    x_values: Iterable[Any],
    series: dict[str, Iterable[float]],
    *,
    title: str,
    xlabel: str,
    ylabel: str,
):
    """Plot a small number of component-cost curves on one axis."""
    x_values = np.asarray(list(x_values))
    series = {label: np.asarray(list(values), dtype=float) for label, values in series.items()}
    fig, ax = plt.subplots(figsize=FIGURE_SIZES["wide"], constrained_layout=True)
    for label, values in series.items():
        ax.plot(x_values, values, marker="o", label=label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, loc="left")
    ax.legend(loc="upper left")
    return fig, ax


def _topology_edges(kind: str, num_qubits: int) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    if kind == "all_to_all":
        for i in range(num_qubits):
            for j in range(i + 1, num_qubits):
                edges.append((i, j))
    elif kind == "line":
        edges = [(i, i + 1) for i in range(num_qubits - 1)]
    elif kind == "ring":
        edges = [(i, i + 1) for i in range(num_qubits - 1)]
        if num_qubits > 2:
            edges.append((num_qubits - 1, 0))
    elif kind == "grid":
        cols = int(np.ceil(np.sqrt(num_qubits)))
        rows = int(np.ceil(num_qubits / cols))
        for r in range(rows):
            for c in range(cols):
                i = r * cols + c
                if i >= num_qubits:
                    continue
                if c + 1 < cols:
                    j = r * cols + c + 1
                    if j < num_qubits:
                        edges.append((i, j))
                if r + 1 < rows:
                    j = (r + 1) * cols + c
                    if j < num_qubits:
                        edges.append((i, j))
    else:
        raise ValueError(f"Unknown topology kind: {kind}")
    return edges


def _topology_positions(kind: str, num_qubits: int) -> dict[int, tuple[float, float]]:
    if kind == "line":
        return {i: (i, 0.0) for i in range(num_qubits)}
    if kind == "ring":
        angles = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, num_qubits, endpoint=False)
        return {i: (np.cos(angle), np.sin(angle)) for i, angle in enumerate(angles)}
    if kind == "all_to_all":
        angles = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, num_qubits, endpoint=False)
        return {i: (np.cos(angle), np.sin(angle)) for i, angle in enumerate(angles)}
    if kind == "grid":
        cols = int(np.ceil(np.sqrt(num_qubits)))
        return {i: (i % cols, -(i // cols)) for i in range(num_qubits)}
    raise ValueError(f"Unknown topology kind: {kind}")


def _draw_topology(
    ax,
    kind: str,
    num_qubits: int,
    *,
    title: str,
    highlight_edges: Iterable[tuple[int, int]] | None = None,
    overlay_edges: Iterable[tuple[int, int]] | None = None,
) -> None:
    positions = _topology_positions(kind, num_qubits)
    device_edges = {tuple(sorted(edge)) for edge in _topology_edges(kind, num_qubits)}
    highlight_edges = {tuple(sorted(edge)) for edge in (highlight_edges or [])}
    overlay_edges = {tuple(sorted(edge)) for edge in (overlay_edges or [])}

    for u, v in sorted(device_edges):
        x0, y0 = positions[u]
        x1, y1 = positions[v]
        color = COLORS["light_gray"]
        linewidth = 2.0
        if (u, v) in highlight_edges:
            color = COLORS["teal"]
            linewidth = 3.0
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=linewidth, zorder=1)

    for u, v in sorted(overlay_edges):
        if (u, v) in device_edges:
            continue
        x0, y0 = positions[u]
        x1, y1 = positions[v]
        arc = FancyArrowPatch(
            (x0, y0),
            (x1, y1),
            connectionstyle="arc3,rad=0.18",
            arrowstyle="-",
            linewidth=1.6,
            linestyle=(0, (4, 3)),
            color=COLORS["rust"],
            zorder=2,
        )
        ax.add_patch(arc)

    for node, (x, y) in positions.items():
        circle = plt.Circle((x, y), 0.12 if kind == "grid" else 0.14, facecolor="white", edgecolor=COLORS["gray"], linewidth=1.3, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, str(node), ha="center", va="center", fontsize=11, zorder=4)

    xs = [x for x, _ in positions.values()]
    ys = [y for _, y in positions.values()]
    ax.set_xlim(min(xs) - 0.5, max(xs) + 0.5)
    ax.set_ylim(min(ys) - 0.5, max(ys) + 0.55)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(title, loc="left")


def plot_logical_vs_physical(
    logical_edges: Iterable[tuple[int, int]],
    *,
    num_qubits: int,
    physical_kind: str = "line",
    title: str = "Logical interactions and physical device constraints are different objects",
):
    """Compare an ideal logical interaction graph with one constrained device topology."""
    logical_edges = {tuple(sorted(edge)) for edge in logical_edges}
    fig, axes = plt.subplots(1, 2, figsize=(13.4, 5.1), constrained_layout=True)
    _draw_topology(axes[0], "all_to_all", num_qubits, title="Ideal logical interaction picture", highlight_edges=logical_edges)
    _draw_topology(
        axes[1],
        physical_kind,
        num_qubits,
        title=f"Physical device topology: {physical_kind.replace('_', '-')} ",
        highlight_edges=logical_edges & {tuple(sorted(edge)) for edge in _topology_edges(physical_kind, num_qubits)},
        overlay_edges=logical_edges,
    )
    fig.suptitle(title, x=0.06, ha="left", fontsize=18, fontweight="semibold")
    return fig, axes


def plot_topology_gallery(
    kinds: Iterable[str],
    *,
    num_qubits: int,
    title: str = "Different hardware topologies make different interactions easy",
):
    """Show a small set of device topologies side by side."""
    kinds = list(kinds)
    fig, axes = plt.subplots(1, len(kinds), figsize=(4.5 * len(kinds), 4.5), constrained_layout=True)
    if len(kinds) == 1:
        axes = [axes]
    for ax, kind in zip(axes, kinds):
        label = kind.replace("_", "-")
        _draw_topology(ax, kind, num_qubits, title=label)
    fig.suptitle(title, x=0.06, ha="left", fontsize=18, fontweight="semibold")
    return fig, axes


def plot_stacked_cost_bars(
    categories: Iterable[str],
    components: dict[str, Iterable[float]],
    *,
    title: str,
    ylabel: str,
):
    """Plot stacked bars for a small number of cost components."""
    categories = list(categories)
    components = {label: np.asarray(list(values), dtype=float) for label, values in components.items()}
    fig, ax = plt.subplots(figsize=(12.4, 5.6), constrained_layout=True)
    x = np.arange(len(categories))
    bottom = np.zeros(len(categories), dtype=float)

    palette = [COLORS["navy"], COLORS["teal"], COLORS["gold"], COLORS["rust"], COLORS["gray"]]
    for color, (label, values) in zip(palette, components.items()):
        ax.bar(x, values, bottom=bottom, label=label, color=color)
        bottom += values

    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel(ylabel)
    ax.set_title(title, loc="left")
    ax.legend(loc="upper left")
    return fig, ax


def plot_evaluation_funnel(
    stages: Iterable[str],
    *,
    title: str = "A speedup claim becomes credible only after several checks",
):
    """Draw a vertical evaluation funnel for judging performance claims."""
    stages = list(stages)
    fig, ax = plt.subplots(figsize=(10.8, 6.6), constrained_layout=True)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, max(7.5, 1.1 * len(stages) + 1))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    widths = np.linspace(7.8, 4.2, len(stages))
    top = ax.get_ylim()[1] - 1.2
    for idx, (stage, width) in enumerate(zip(stages, widths)):
        y = top - idx * 1.05
        rect = Rectangle(
            ((10 - width) / 2, y),
            width,
            0.78,
            facecolor="#e7eef6" if idx == 0 else "#f6e3b3" if idx < len(stages) - 1 else "#d9e8ea",
            edgecolor=COLORS["gray"],
            linewidth=1.3,
        )
        ax.add_patch(rect)
        ax.text(5.0, y + 0.39, textwrap.fill(stage, width=30), ha="center", va="center", fontsize=11)
        if idx < len(stages) - 1:
            ax.annotate("", xy=(5.0, y - 0.02), xytext=(5.0, y - 0.25), arrowprops={"arrowstyle": "->", "linewidth": 1.6, "color": COLORS["gray"]})

    ax.text(5.0, 0.65, "The claim gets narrower and more credible as it survives more checks.", ha="center", va="center", fontsize=10.8, color=COLORS["gray"])
    ax.set_title(title, loc="left")
    return fig, ax


def plot_io_constraint_summary(
    *,
    title: str = "Input and output assumptions can dominate the story",
):
    """Show input-loading and measurement constraints around a quantum core."""
    fig, ax = plt.subplots(figsize=(12.8, 4.8), constrained_layout=True)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    def box(x: float, y: float, w: float, h: float, text: str, color: str):
        rect = Rectangle((x, y), w, h, facecolor=color, edgecolor=COLORS["gray"], linewidth=1.3)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, textwrap.fill(text, width=18), ha="center", va="center", fontsize=11)

    box(0.5, 2.2, 2.4, 0.95, "classical data", "#e7eef6")
    box(3.35, 2.2, 2.6, 0.95, "encoding / state preparation", "#f6d9cc")
    box(6.45, 2.2, 2.1, 0.95, "logical circuit", "#f6e3b3")
    box(9.0, 2.2, 2.1, 0.95, "measurement shots", "#f6d9cc")
    box(4.35, 0.65, 3.2, 0.95, "classical post-processing", "#d9e8ea")

    for start_x, end_x in [(2.9, 3.35), (5.95, 6.45), (8.55, 9.0)]:
        ax.annotate("", xy=(end_x, 2.68), xytext=(start_x, 2.68), arrowprops={"arrowstyle": "->", "linewidth": 1.6, "color": COLORS["gray"]})
    ax.annotate("", xy=(7.4, 1.6), xytext=(10.05, 2.2), arrowprops={"arrowstyle": "->", "linewidth": 1.6, "color": COLORS["gray"]})

    ax.text(2.0, 3.45, "input side", ha="center", va="center", fontsize=11, color=COLORS["navy"])
    ax.text(10.0, 3.45, "output side", ha="center", va="center", fontsize=11, color=COLORS["rust"])
    ax.set_title(title, loc="left")
    return fig, ax


def plot_baseline_comparison(
    *,
    title: str = "A weak classical baseline can make any new method look stronger",
):
    """Compare fair and unfair benchmarking logic."""
    fig, ax = plt.subplots(figsize=(13.0, 5.4), constrained_layout=True)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    def lane(x: float, title_text: str, color: str, rows: list[str]):
        ax.text(x + 1.75, 4.55, title_text, ha="center", va="center", fontsize=15, color=color, fontweight="semibold")
        for idx, row in enumerate(rows):
            rect = Rectangle((x, 3.5 - idx * 1.0), 3.5, 0.72, facecolor="#f6d9cc" if color == COLORS["rust"] else "#e7eef6", edgecolor=COLORS["gray"], linewidth=1.3)
            ax.add_patch(rect)
            ax.text(x + 1.75, 3.86 - idx * 1.0, textwrap.fill(row, width=24), ha="center", va="center", fontsize=10.8)

    lane(
        0.8,
        "Unfair comparison",
        COLORS["rust"],
        [
            "old or naive classical baseline",
            "ignore preprocessing or I/O cost",
            "highlight only best quantum-looking metric",
        ],
    )
    lane(
        5.0,
        "Fair comparison",
        COLORS["navy"],
        [
            "strong current classical baseline",
            "end-to-end cost counted on both sides",
            "same problem definition and output target",
        ],
    )
    ax.text(10.8, 2.3, "Credible quantum advantage claims require the fair lane, not the unfair one.", ha="center", va="center", fontsize=11, color=COLORS["gray"])
    ax.set_title(title, loc="left")
    return fig, ax


def plot_case_study_matrix(
    case_names: Iterable[str],
    columns: Iterable[str],
    ratings: list[list[str]],
    *,
    judgments: Iterable[str],
    title: str = "Case studies become clearer when judged against the same checklist",
):
    """Draw a color-coded checklist matrix with a final judgment column."""
    case_names = list(case_names)
    columns = list(columns)
    judgments = list(judgments)
    all_columns = columns + ["judgment"]

    color_map = {
        "promising": "#d9e8ea",
        "mixed": "#f6e3b3",
        "risky": "#f6d9cc",
        "plausible": "#d9e8ea",
        "unclear": "#f6e3b3",
        "hype-prone": "#f6d9cc",
    }

    fig, ax = plt.subplots(figsize=(13.8, max(4.8, 1.15 * len(case_names) + 2.0)), constrained_layout=True)
    ax.set_xlim(0, len(all_columns) + 1.8)
    ax.set_ylim(0, len(case_names) + 1.6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    for col_index, col_name in enumerate(["case"] + all_columns):
        if col_index == 0:
            ax.text(0.9, len(case_names) + 0.95, "case", ha="center", va="center", fontsize=10.5, color=COLORS["gray"], fontweight="semibold")
        else:
            ax.text(col_index + 0.4, len(case_names) + 0.95, textwrap.fill(col_name, width=12), ha="center", va="center", fontsize=10.2, color=COLORS["gray"], fontweight="semibold")

    for row_index, case_name in enumerate(case_names):
        y = len(case_names) - row_index - 0.2
        ax.text(0.9, y, textwrap.fill(case_name, width=18), ha="center", va="center", fontsize=10.8)
        row_values = ratings[row_index] + [judgments[row_index]]
        for col_index, value in enumerate(row_values, start=1):
            rect = Rectangle((col_index - 0.05, y - 0.35), 0.9, 0.7, facecolor=color_map.get(value, "white"), edgecolor=COLORS["gray"], linewidth=1.1)
            ax.add_patch(rect)
            ax.text(col_index + 0.4, y, textwrap.fill(value, width=10), ha="center", va="center", fontsize=9.8)

    ax.set_title(title, loc="left")
    return fig, ax


def plot_checklist_ladder(
    steps: Iterable[str],
    *,
    title: str = "A reusable mental framework for judging quantum advantage",
):
    """Draw a clean ladder-style checklist for lecture closing."""
    steps = list(steps)
    fig, ax = plt.subplots(figsize=(11.8, 5.8), constrained_layout=True)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, max(5.5, len(steps) + 1))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    for idx, step in enumerate(steps):
        y = len(steps) - idx + 0.1
        rect = Rectangle((1.0 + 0.45 * idx, y - 0.35), 7.8 - 0.45 * idx, 0.72, facecolor="#e7eef6" if idx < len(steps) - 1 else "#d9e8ea", edgecolor=COLORS["gray"], linewidth=1.3)
        ax.add_patch(rect)
        ax.text(1.25 + 0.45 * idx, y, textwrap.fill(step, width=38), ha="left", va="center", fontsize=10.8)

    ax.text(8.65, 1.0, "If several steps fail, the claim becomes weaker.\nIf the claim survives all steps, it becomes more plausible.", ha="center", va="center", fontsize=10.6, color=COLORS["gray"])
    ax.set_title(title, loc="left")
    return fig, ax


def timed_call(
    func: Callable[..., Any],
    *args: Any,
    repeat: int = 5,
    warmup: int = 1,
    **kwargs: Any,
) -> tuple[Any, dict[str, Any]]:
    """Run a callable repeatedly and return the last result plus timing stats."""
    for _ in range(max(warmup, 0)):
        func(*args, **kwargs)

    timings = []
    result = None
    for _ in range(max(repeat, 1)):
        start = perf_counter()
        result = func(*args, **kwargs)
        timings.append(perf_counter() - start)

    samples = np.asarray(timings, dtype=float)
    stats = {
        "times_s": samples,
        "mean_s": float(samples.mean()),
        "std_s": float(samples.std(ddof=0)),
        "min_s": float(samples.min()),
        "max_s": float(samples.max()),
        "repeat": int(len(samples)),
    }
    return result, stats


def time_size_series(
    func: Callable[[Any], Any],
    sizes: Iterable[Any],
    *,
    repeat: int = 5,
    warmup: int = 1,
) -> pd.DataFrame:
    """Measure runtime over a sequence of input sizes and return a tidy table."""
    rows = []
    for size in sizes:
        _, stats = timed_call(func, size, repeat=repeat, warmup=warmup)
        rows.append(
            {
                "size": size,
                "mean_s": stats["mean_s"],
                "std_s": stats["std_s"],
                "min_s": stats["min_s"],
                "max_s": stats["max_s"],
            }
        )
    return pd.DataFrame(rows)


def style_wrapped_df(
    df: pd.DataFrame | pd.Series,
    *,
    max_width: str = "280px",
) -> HTML:
    """Render a dataframe as lightweight HTML with wrapped text."""
    if isinstance(df, pd.Series):
        df = df.to_frame()

    html_table = df.to_html(classes="lecture-wrapped-df", escape=False)
    styles = f"""
<style>
.lecture-wrapped-df {{
  table-layout: fixed;
  width: 100%;
}}
.lecture-wrapped-df th,
.lecture-wrapped-df td {{
  text-align: left;
  white-space: normal !important;
  overflow-wrap: anywhere;
  word-break: break-word;
  max-width: {html.escape(max_width)};
  vertical-align: top;
}}
</style>
"""
    return HTML(styles + html_table)


def display_wrapped(
    obj: Any,
    *,
    max_width: str = "280px",
) -> None:
    """Display dataframes with wrapped text while passing other objects through."""
    if isinstance(obj, (pd.DataFrame, pd.Series)):
        display(style_wrapped_df(obj, max_width=max_width))
        return
    display(obj)


def markdown_box(text: str, *, title: str = "Takeaway") -> str:
    """Return a quoted markdown box for notebook recap cells."""
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    prefix = f"> **{title}:**"
    body = "\n".join(f"> {line}" for line in lines)
    return f"{prefix}\n{body}" if body else prefix


def instructor_prompt(text: str) -> str:
    """Return a consistent markdown block for live-discussion prompts."""
    return markdown_box(text, title="Instructor Prompt")
