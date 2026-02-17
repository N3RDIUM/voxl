import unittest
from dataclasses import dataclass
from typing import cast

from src.engine.ecs import ECS, Component


@dataclass
class Position(Component):
    x: float = 0.0
    y: float = 0.0


@dataclass
class Velocity(Component):
    dx: float = 0.0
    dy: float = 0.0


@dataclass
class Tag(Component):
    name: str = ""


class TestECS(unittest.TestCase):
    def test_spawn_increments_entity_ids(self):
        ecs = ECS()

        e1 = ecs.spawn()
        e2 = ecs.spawn()
        e3 = ecs.spawn()

        self.assertEqual(e1, 0)
        self.assertEqual(e2, 1)
        self.assertEqual(e3, 2)

        self.assertEqual(len(ecs.entities), 3)

    def test_spawn_creates_empty_archetype(self):
        ecs = ECS()

        entity = ecs.spawn()

        self.assertIn(entity, ecs.entities)
        archetype, row = ecs.entities[entity]
        self.assertEqual(archetype, 0)
        self.assertEqual(row, 0)

    def test_determine_archetype_same_type_returns_same_index(self):
        ecs = ECS()

        a1 = ecs.determine_archetype(frozenset({Position, Velocity}))
        a2 = ecs.determine_archetype(frozenset({Position, Velocity}))

        self.assertEqual(a1, a2)

    def test_set_components_adds_entity(self):
        ecs = ECS()
        entity = ecs.spawn()

        ecs.set_components(entity, [Position(x=1.0, y=2.0)])

        self.assertIn(entity, ecs.entities)
        archetype, _ = ecs.entities[entity]
        self.assertEqual(len(ecs.components[archetype][Position]), 1)

    def test_set_components_updates_existing_entity(self):
        ecs = ECS()
        entity = ecs.spawn()

        ecs.set_components(entity, [Position(x=1.0, y=2.0)])
        ecs.set_components(
            entity, [Position(x=3.0, y=4.0), Velocity(dx=0.1, dy=0.2)]
        )

        archetype, _ = ecs.entities[entity]
        self.assertEqual(len(ecs.components[archetype][Position]), 1)
        self.assertEqual(len(ecs.components[archetype][Velocity]), 1)

    def test_set_components_empty_removes_to_empty_archetype(self):
        ecs = ECS()
        entity = ecs.spawn()

        ecs.set_components(entity, [Position(x=1.0, y=2.0)])
        ecs.set_components(entity, [])

        archetype, _ = ecs.entities[entity]
        self.assertEqual(archetype, 0)

    def test_remove_deletes_entity(self):
        ecs = ECS()
        entity = ecs.spawn()
        ecs.set_components(entity, [Position(x=1.0, y=2.0)])

        ecs.remove(entity)

        self.assertNotIn(entity, ecs.entities)

    def test_remove_compacts_rows(self):
        ecs = ECS()
        e1 = ecs.spawn()
        e2 = ecs.spawn()
        e3 = ecs.spawn()

        ecs.set_components(e1, [Position(x=1.0, y=1.0)])
        ecs.set_components(e2, [Position(x=2.0, y=2.0)])
        ecs.set_components(e3, [Position(x=3.0, y=3.0)])

        ecs.remove(e2)

        self.assertIn(e1, ecs.entities)
        self.assertIn(e3, ecs.entities)
        self.assertNotIn(e2, ecs.entities)

    def test_remove_from_empty_archetype(self):
        ecs = ECS()
        entity = ecs.spawn()

        ecs.remove(entity)

        self.assertNotIn(entity, ecs.entities)

    def test_query_returns_matching_entities(self):
        ecs = ECS()
        e1 = ecs.spawn()
        e2 = ecs.spawn()
        e3 = ecs.spawn()

        ecs.set_components(
            e1, [Position(x=1.0, y=1.0), Velocity(dx=0.1, dy=0.1)]
        )
        ecs.set_components(e2, [Position(x=2.0, y=2.0)])
        ecs.set_components(
            e3, [Position(x=3.0, y=3.0), Velocity(dx=0.3, dy=0.3)]
        )

        results, _ = ecs.query([Position])
        self.assertEqual(len(results), 3)

    def test_query_filters_by_component_types(self):
        ecs = ECS()
        e1 = ecs.spawn()
        e2 = ecs.spawn()
        e3 = ecs.spawn()

        ecs.set_components(
            e1, [Position(x=1.0, y=1.0), Velocity(dx=0.1, dy=0.1)]
        )
        ecs.set_components(e2, [Position(x=2.0, y=2.0)])
        ecs.set_components(e3, [Velocity(dx=0.3, dy=0.3)])

        results, _ = ecs.query([Position, Velocity])

        self.assertEqual(len(results), 1)
        entity = results[0]
        self.assertEqual(entity, e1)

    def test_query_returns_component_lookup(self):
        ecs = ECS()
        entity = ecs.spawn()
        ecs.set_components(
            entity, [Position(x=1.5, y=2.5), Velocity(dx=0.1, dy=0.2)]
        )

        _, components = ecs.query([Position, Velocity])
        lookup: dict[type[Component], Component] = {
            Position: components[Position][0],
            Velocity: components[Velocity][0],
        }
        pos = cast(Position, lookup[Position])
        vel = cast(Velocity, lookup[Velocity])
        self.assertEqual(pos.x, 1.5)
        self.assertEqual(pos.y, 2.5)
        self.assertEqual(vel.dx, 0.1)
        self.assertEqual(vel.dy, 0.2)

    def test_query_empty_when_no_matches(self):
        ecs = ECS()
        e1 = ecs.spawn()
        ecs.set_components(e1, [Position(x=1.0, y=1.0)])

        results, _ = ecs.query([Velocity])
        self.assertEqual(len(results), 0)

    def test_query_with_tag_component(self):
        ecs = ECS()
        e1 = ecs.spawn()
        e2 = ecs.spawn()

        ecs.set_components(e1, [Position(x=1.0, y=1.0), Tag(name="player")])
        ecs.set_components(e2, [Position(x=2.0, y=2.0), Tag(name="enemy")])

        results = list(ecs.query([Tag]))

        self.assertEqual(len(results), 2)

    def test_component_types_static_method(self):
        components: list[Component] = [
            Position(x=1.0, y=2.0),
            Velocity(dx=0.1, dy=0.2),
        ]

        types = ECS.component_types(components)

        self.assertEqual(types, frozenset({Position, Velocity}))

    def test_multiple_entities_same_archetype(self):
        ecs = ECS()

        e1 = ecs.spawn()
        e2 = ecs.spawn()
        e3 = ecs.spawn()

        ecs.set_components(e1, [Position(x=1.0, y=1.0)])
        ecs.set_components(e2, [Position(x=2.0, y=2.0)])
        ecs.set_components(e3, [Position(x=3.0, y=3.0)])

        archetype1, _ = ecs.entities[e1]
        archetype2, _ = ecs.entities[e2]
        archetype3, _ = ecs.entities[e3]

        self.assertEqual(archetype1, archetype2)
        self.assertEqual(archetype2, archetype3)

    def test_remove_last_entity_in_archetype(self):
        ecs = ECS()
        entity = ecs.spawn()
        ecs.set_components(entity, [Position(x=1.0, y=2.0)])

        archetype = ecs.determine_archetype(frozenset({Position}))
        ecs.remove(entity)

        self.assertNotIn(entity, ecs.entities)
        self.assertEqual(len(ecs.components[archetype][Position]), 0)
        self.assertEqual(len(ecs.entity_rows[archetype]), 0)

    def test_entity_rows_consistency(self):
        ecs = ECS()
        e1 = ecs.spawn()
        e2 = ecs.spawn()

        ecs.set_components(e1, [Position(x=1.0, y=1.0)])
        ecs.set_components(e2, [Position(x=2.0, y=2.0)])

        archetype, _ = ecs.entities[e1]

        self.assertEqual(ecs.entity_rows[archetype][0], e1)
        self.assertEqual(ecs.entity_rows[archetype][1], e2)
