from dataclasses import dataclass
from time import perf_counter_ns
from typing import cast

from src.engine.ecs import ECS, Component, Entity


@dataclass
class Position(Component):
    x: float
    y: float


@dataclass
class Velocity(Component):
    dx: float
    dy: float


@dataclass
class Acceleration(Component):
    dx: float
    dy: float


if __name__ == "__main__":
    ecs = ECS()
    samples: list[float] = []
    entities: list[Entity] = []

    n = 100_000
    steps = 100

    print(f"Bench entity spawn ({n}):", end=" ")
    for _ in range(n):
        t0 = perf_counter_ns()
        entity = ecs.spawn()
        samples.append(perf_counter_ns() - t0)
        entities.append(entity)
    print(f"avg {sum(samples) / n} ns/call")

    samples = []
    print(f"Bench set components ({n}):", end=" ")
    for entity in entities:
        components = cast(
            list[Component],
            [
                Position(x=0, y=0),
                Velocity(dx=1, dy=1),
                Acceleration(dx=1, dy=1),
            ],
        )
        t0 = perf_counter_ns()
        ecs.set_components(entity, components)
        samples.append(perf_counter_ns() - t0)
    print(f"avg {sum(samples) / n} ns/call")

    samples = []
    print(f"Bench query ({steps}):", end=" ")
    for _ in range(steps):
        t0 = perf_counter_ns()
        _ = ecs.query([Position, Velocity])
        samples.append(perf_counter_ns() - t0)
    print(f"avg {sum(samples) / steps} ns/call")

    samples = []
    print(f"Bench entity remove ({n}):", end=" ")
    for entity in entities:
        t0 = perf_counter_ns()
        ecs.remove(entity)
        samples.append(perf_counter_ns() - t0)
    print(f"avg {sum(samples) / n} ns/call")
