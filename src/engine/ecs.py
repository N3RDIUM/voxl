from collections.abc import Collection, Generator
from dataclasses import dataclass
from typing import Generic, TypeVar, cast

type EntityID = int
type RowIndex = int


@dataclass
class Component: ...


C = TypeVar("C", bound=Component)


@dataclass(frozen=True)
class Entity:
    id: EntityID


type Archetype = int


class ComponentLookup(Generic[C]):
    _data: dict[type[Component], list[Component]]
    _row: int

    def __init__(self, data: dict[type[Component], list[Component]], row: int):
        self._data = data
        self._row = row

    def __getitem__(self, key: type[C]) -> C:
        return cast(C, self._data[key][self._row])


class ECS:  # TODO document
    _next_entity_id: EntityID
    _next_archetype: Archetype

    entities: dict[Entity, tuple[Archetype, RowIndex]]
    entity_rows: dict[Archetype, dict[RowIndex, Entity]]
    components: dict[Archetype, dict[type[Component], list[Component]]]
    archetypes: dict[frozenset[type[Component]], Archetype]
    archetypes_reverse: dict[Archetype, frozenset[type[Component]]]

    def __init__(self):
        self._next_entity_id = 0
        self._next_archetype = 0

        self.entities = {}
        self.entity_rows = {}
        self.components = {}
        self.archetypes = {}
        self.archetypes_reverse = {}

    def spawn(self) -> Entity:
        empty_archetype = self.determine_archetype(frozenset())
        row: RowIndex = len(self.entity_rows[empty_archetype])

        entity = Entity(id=self._next_entity_id)
        self._next_entity_id += 1

        self.entities[entity] = (empty_archetype, row)
        self.entity_rows[empty_archetype][row] = entity

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

        self.archetypes[component_types] = self._next_archetype
        self.archetypes_reverse[self._next_archetype] = component_types
        archetype = self._next_archetype
        self._next_archetype += 1

        self.components[archetype] = {t: [] for t in component_types}
        self.entity_rows[archetype] = {}

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
            self.entity_rows[empty_archetype][row] = entity
            return

        types = self.component_types(components)
        archetype = self.determine_archetype(types)
        self._remove_components(entity)

        first_type: type[Component] = type(components[0])
        for component in components:
            self.components[archetype][type(component)].append(component)

        row: RowIndex = len(self.components[archetype][first_type]) - 1
        self.entities[entity] = (archetype, row)
        self.entity_rows[archetype][row] = entity

    def _remove_components(self, entity: Entity) -> None:
        archetype, row = self.entities[entity]
        component_types = self.archetypes_reverse[archetype]

        if not component_types:
            last_row = len(self.entity_rows[archetype]) - 1

            if row == last_row:
                del self.entity_rows[archetype][last_row]
                return

            last_entity = self.entity_rows[archetype][last_row]
            del self.entity_rows[archetype][last_row]

            self.entity_rows[archetype][row] = last_entity
            self.entities[last_entity] = (archetype, row)
            return

        first_type = next(iter(component_types))
        last_row = len(self.components[archetype][first_type]) - 1

        if row == last_row:
            for component_type in self.components[archetype]:
                _ = self.components[archetype][component_type].pop()
            del self.entity_rows[archetype][last_row]
            return

        last_components: dict[type[Component], Component] = {}
        for component_type in self.components[archetype]:
            last_components[component_type] = self.components[archetype][
                component_type
            ].pop()

        last_entity = self.entity_rows[archetype][last_row]
        del self.entity_rows[archetype][last_row]

        self.entity_rows[archetype][row] = last_entity
        self.entities[last_entity] = (archetype, row)
        for component_type, component in last_components.items():
            self.components[archetype][component_type][row] = component

    def query(
        self, component_types: Collection[type[C]]
    ) -> Generator[tuple[Entity, ComponentLookup[C]], None, None]:
        required_types = frozenset(component_types)

        for archetype_set, archetype in self.archetypes.items():
            if not archetype_set.issuperset(required_types):
                continue
            for row, entity in self.entity_rows[archetype].items():
                yield (
                    entity,
                    ComponentLookup(self.components[archetype], row),
                )
