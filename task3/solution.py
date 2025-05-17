from __future__ import annotations

def process_interval(
    interval: list[int], lesson_start: int, lesson_end: int
) -> list[tuple[int, int]]:
    processed = []
    for index in range(0, len(interval), 2):
        start, end = max(interval[index], lesson_start), min(
            interval[index + 1], lesson_end
        )
        if start < end:
            processed.append((start, end))
    processed = sorted(processed)

    merged = [processed[0]]
    for current in processed[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)
    return merged


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals["lesson"]
    pupil, tutor = (
        process_interval(
            interval=intervals["pupil"],
            lesson_start=lesson_start,
            lesson_end=lesson_end,
        ),
        process_interval(
            interval=intervals["tutor"],
            lesson_start=lesson_start,
            lesson_end=lesson_end,
        ),
    )

    total = 0
    i = j = 0
    while i < len(pupil) and j < len(tutor):
        p_start, p_end = pupil[i]
        t_start, t_end = tutor[j]

        start, end = max(p_start, t_start), min(p_end, t_end)
        if start < end:
            total += end - start

        if p_end < t_end:
            i += 1
        else:
            j += 1

    return total
