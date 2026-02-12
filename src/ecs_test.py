from dataclasses import dataclass
from typing import cast

from src.engine.ecs import ECS, Component

# --- Define concrete components ---


@dataclass
class Position(Component):
    x: float
    y: float


@dataclass
class Velocity(Component):
    dx: float
    dy: float


@dataclass
class Health(Component):
    value: int


# --- Example systems ---


def movement_system(ecs: ECS):
    """Update Position using Velocity."""
    for _, comps in ecs.query([Position, Velocity]):
        pos = cast(Position, comps[Position])
        vel = cast(Velocity, comps[Velocity])

        pos.x += vel.dx
        pos.y += vel.dy


def damage_system(ecs: ECS, amount: int):
    """Reduce Health for all entities that have it."""
    for _, comps in ecs.query([Health]):
        health = comps[Health]
        health.value -= amount


# --- Main demo ---


def main():
    ecs = ECS()

    # Spawn entities
    player = ecs.spawn()
    enemy = ecs.spawn()
    projectile = ecs.spawn()

    # Assign components
    ecs.set_components(
        player,
        [
            Position(0, 0),
            Velocity(1, 1),
            Health(100),
        ],
    )

    ecs.set_components(
        enemy,
        [
            Position(10, 5),
            Health(50),
        ],
    )

    ecs.set_components(
        projectile,
        [
            Position(2, 2),
            Velocity(5, 0),
        ],
    )

    print("== Initial State ==")
    for entity, comps in ecs.query([Position]):
        print(entity, comps)

    # Run systems
    movement_system(ecs)
    damage_system(ecs, amount=10)

    print("\n== After 1 Tick ==")
    for entity, comps in ecs.query([Position]):
        print(f"{entity} -> Position: {comps[Position]}")

    for entity, comps in ecs.query([Health]):
        print(f"{entity} -> Health: {comps[Health].value}")

    # Remove an entity
    print("\n== Removing projectile ==")
    ecs.remove(projectile)

    print("\n== Final State (Position query) ==")
    for entity, comps in ecs.query([Position]):
        print(f"{entity} -> {comps[Position]}")


if __name__ == "__main__":
    main()
