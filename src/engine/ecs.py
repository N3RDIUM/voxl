from collections.abc import Collection
from dataclasses import dataclass
from typing import TypeVar, cast

type Entity = int
type RowIndex = int
type Archetype = int


@dataclass
class Component: ...


C = TypeVar("C", bound=Component)


class ECS:
    _next_entity_id: Entity
    _next_archetype: Archetype

    entities: dict[Entity, tuple[Archetype, RowIndex]]
    entity_rows: dict[Archetype, list[Entity]]
    components: dict[Archetype, dict[type[Component], list[Component]]]

    archetypes: dict[frozenset[type[Component]], Archetype]
    archetypes_reverse: dict[Archetype, frozenset[type[Component]]]
    archetypes_by_component: dict[type[Component], set[Archetype]]

    def __init__(self):
        self._next_entity_id = 0
        self._next_archetype = 0

        self.entities = {}
        self.entity_rows = {}
        self.components = {}

        self.archetypes = {}
        self.archetypes_reverse = {}
        self.archetypes_by_component = {}

    def spawn(self) -> Entity:
        empty_archetype = self.determine_archetype(frozenset())
        row: RowIndex = len(self.entity_rows[empty_archetype])

        entity = self._next_entity_id
        self._next_entity_id += 1

        self.entities[entity] = (empty_archetype, row)
        self.entity_rows[empty_archetype].append(entity)

        return entity

    def remove(self, entity: Entity) -> None:
        self._remove_components(entity)
        del self.entities[entity]

    def determine_archetype(
        self, component_types: frozenset[type[Component]]
    ) -> Archetype:
        try:
            return self.archetypes[component_types]
        except KeyError:
            pass

        archetype = self._next_archetype
        self._next_archetype += 1

        self.archetypes[component_types] = archetype
        self.archetypes_reverse[archetype] = component_types

        for t in component_types:
            self.archetypes_by_component.setdefault(t, set()).add(archetype)

        self.components[archetype] = {t: [] for t in component_types}
        self.entity_rows[archetype] = []

        return archetype

    @staticmethod
    def component_types(
        components: list[Component],
    ) -> frozenset[type[Component]]:
        return frozenset(type(component) for component in components)

    def set_components(
        self, entity: Entity, components: list[Component]
    ) -> None:
        if not components:
            self._remove_components(entity)
            empty_archetype = self.determine_archetype(frozenset())
            row = len(self.entity_rows[empty_archetype])
            self.entities[entity] = (empty_archetype, row)
            self.entity_rows[empty_archetype].append(entity)
            return

        types = self.component_types(components)
        archetype = self.determine_archetype(types)

        self._remove_components(entity)

        for component in components:
            self.components[archetype][type(component)].append(component)

        first_type = type(components[0])
        row: RowIndex = len(self.components[archetype][first_type]) - 1

        self.entities[entity] = (archetype, row)
        self.entity_rows[archetype].append(entity)

    def _remove_components(self, entity: Entity) -> None:
        archetype, row = self.entities[entity]
        component_types = self.archetypes_reverse[archetype]

        if not component_types:
            last_row = len(self.entity_rows[archetype]) - 1

            if row == last_row:
                _ = self.entity_rows[archetype].pop()
                return

            last_entity = self.entity_rows[archetype].pop()
            self.entity_rows[archetype][row] = last_entity
            self.entities[last_entity] = (archetype, row)
            return

        first_type = next(iter(component_types))
        last_row = len(self.components[archetype][first_type]) - 1

        if row == last_row:
            for component_type in self.components[archetype]:
                _ = self.components[archetype][component_type].pop()
            _ = self.entity_rows[archetype].pop()
            return

        last_components: dict[type[Component], Component] = {}
        for component_type in self.components[archetype]:
            last_components[component_type] = self.components[archetype][
                component_type
            ].pop()

        last_entity = self.entity_rows[archetype].pop()

        self.entity_rows[archetype][row] = last_entity
        self.entities[last_entity] = (archetype, row)

        for component_type, component in last_components.items():
            self.components[archetype][component_type][row] = component

    def query(
        self, component_types: Collection[type[C]]
    ) -> tuple[list[Entity], dict[type[C], list[C]]]:
        required = list(component_types)
        if not required:
            return [], {}

        candidate_sets = [self.archetypes_by_component.get(t) for t in required]

        if not candidate_sets or any(s is None for s in candidate_sets):
            return [], {}

        first_set = candidate_sets[0]
        assert first_set is not None
        matching_archetypes = first_set.copy()
        for s in candidate_sets[1:]:
            assert s is not None
            matching_archetypes &= s

        if not matching_archetypes:
            return [], {}

        result_entities: list[Entity] = []
        result_components: dict[type[C], list[C]] = {t: [] for t in required}

        for archetype in matching_archetypes:
            entity_list = self.entity_rows[archetype]
            component_data = self.components[archetype]

            result_entities.extend(entity_list)

            for t in required:
                result_components[t].extend(cast(list[C], component_data[t]))

        return result_entities, result_components
