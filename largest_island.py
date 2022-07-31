import random
from dataclasses import dataclass


@dataclass(slots=True)
class Point:
    x: int
    y: int


@dataclass(slots=True)
class Island:
    points: list[Point]

    @property
    def size(self) -> int:
        return len(self.points)


def main() -> None:
    row_length = random.randrange(10, 51)
    matrix = [
        [random.choice([0, 1]) for _ in range(row_length)]
        for _ in range(random.randrange(10, 51))
    ]

    print("Matrix:")
    for row in matrix:
        print(*row)
    print()

    islands = get_islands(matrix)

    if not islands:
        print("Largest island size: 0.")
        print("Changing any point results in a new largest island of size 1")
        return

    print(f"Largest island size: {islands[-1].size}")
    new_islands = get_new_islands(matrix, islands)

    if not new_islands:
        print("No new islands can be created.")
        return

    print(
        f"Changing {new_islands[-1].points[-1]} results in "
        f"a new largest island of size {new_islands[-1].size}"
    )


def get_islands(matrix: list[str]) -> list[Island]:
    islands: list[Island] = []
    for point in (
        Point(x, y)
        for y in range(len(matrix))
        for x in range(len(matrix[0]))
        if matrix[y][x]
    ):
        connected_islands = _get_connected_islands(point, islands)
        if connected_islands:
            for c in connected_islands:
                islands.remove(c)
            islands.append(
                Island([*(p for c in connected_islands for p in c.points), point])
            )
        else:
            islands.append(Island([point]))
    return sorted(islands, key=lambda island: island.size)


def get_new_islands(matrix: list[str], islands: list[Island]) -> list[Island]:
    new_islands: list[Island] = []
    for empty_point in (
        Point(x, y)
        for y in range(len(matrix))
        for x in range(len(matrix[0]))
        if not matrix[y][x]
    ):
        connected_islands = _get_connected_islands(empty_point, islands)
        new_islands.append(
            Island([*(p for c in connected_islands for p in c.points), empty_point]),
        )
    return sorted(new_islands, key=lambda island: island.size)


def _get_connected_islands(point: Point, islands: list[Island]) -> list[Island]:
    return [
        island
        for island in islands
        if any(
            (
                (abs(point.x - ip.x), abs(point.y - ip.y))
                in [
                    (0, 1),
                    (1, 0),
                    # uncomment if diagonal cells count as connected
                    # (1, 1),
                ]
                for ip in island.points
            )
        )
    ]


if __name__ == "__main__":
    main()
