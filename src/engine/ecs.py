from collections.abc import Collection
from dataclasses import dataclass
from typing import TypeVar, cast

from bidict import bidict

# TODO move to types
type Entity = int
type RowIndex = int
type Archetype = int


@dataclass
class Component: ...


C = TypeVar("C", bound=Component)


# TODO impl that clever bitshifting thing for the archetypes
class ECS:
    _next_entity_id: Entity
    _next_type_id: int

    entities: dict[Entity, tuple[Archetype, RowIndex]]
    entity_rows: dict[Archetype, list[Entity]]
    components: dict[Archetype, dict[type[Component], list[Component]]]

    types: bidict[int, type[Component]]

    def __init__(self):
        self._next_entity_id = 0
        self._next_type_id = 0

        self.entities = {}
        self.entity_rows = {}
        self.components = {}

        self.types = bidict({})

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
        archetype: Archetype = 0
        for component_type in component_types:
            place: int = 0

            if component_type not in self.types.inverse:
                self.types[self._next_type_id] = component_type
                place = self._next_type_id
                self._next_type_id += 1
            else:
                place = self.types.inverse[component_type]

            archetype |= 1 << place

        if archetype not in self.entity_rows:
            self.entity_rows[archetype] = []
        if archetype not in self.components:
            self.components[archetype] = {t: [] for t in component_types}

        return archetype

    def determine_types(self, archetype: Archetype) -> set[type[Component]]:
        types: set[type[Component]] = set()

        if archetype == 0:
            return types

        # Loop and bitshift until it becomes zero. Won't that be more efficient?
        # In some cases*
        for type_id, component_type in self.types.items():
            if archetype & (1 << type_id):
                types.add(component_type)

        return types

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
        component_types = self.determine_types(archetype)

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

        required_mask: Archetype = self.determine_archetype(frozenset(required))
        matching_archetypes = (
            archetype
            for archetype in self.entity_rows.keys()
            if (archetype & required_mask) == required_mask
        )

        result_entities: list[Entity] = []
        result_components: dict[type[C], list[C]] = {t: [] for t in required}

        for archetype in matching_archetypes:
            entity_list = self.entity_rows[archetype]
            component_data = self.components[archetype]

            result_entities.extend(entity_list)

            for t in required:
                result_components[t].extend(cast(list[C], component_data[t]))

        return result_entities, result_components
