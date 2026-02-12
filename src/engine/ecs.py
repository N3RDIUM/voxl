from collections.abc import Generator
from dataclasses import dataclass

type EntityID = int


@dataclass
class Component: ...


@dataclass(frozen=True)
class Entity:
    id: EntityID


type Archetype = int
type ComponentTable = dict[Entity, dict[type[Component], Component]]


class ECS:
    _next_entity_id: EntityID
    _next_archetype: Archetype
    entities: dict[Entity, Archetype]
    components: ComponentTable
    archetypes: dict[frozenset[type[Component]], Archetype]
    archetype_table: dict[Archetype, list[Entity]]

    def __init__(self):
        self._next_entity_id = 0
        self._next_archetype = 1

        self.entities = {}
        self.components = {}
        self.archetypes = {frozenset([]): 0}
        self.archetype_table = {}

    def spawn(self) -> Entity:  # TODO? arg components: list[Component] = []
        entity = Entity(id=self._next_entity_id)
        self._next_entity_id += 1

        archetype = self.determine_archetype(frozenset([]))
        self.entities[entity] = archetype
        self.components[entity] = {}

        if self.archetype_table.get(archetype) is None:
            self.archetype_table[archetype] = []
        self.archetype_table[archetype].append(entity)

        return entity

    # TODO remove entity

    # TODO get components associated with entity

    def determine_archetype(
        self, component_types: frozenset[type[Component]]
    ) -> Archetype:
        try:
            return self.archetypes[component_types]
        except ValueError:
            pass

        self.archetypes[component_types] = self._next_archetype
        self._next_archetype += 1
        return self._next_archetype - 1

    @staticmethod
    def component_types(components: list[Component]) -> list[type[Component]]:
        return [type(component) for component in components]

    def insert_components(self, entity: Entity, components: list[Component]):
        types = self.component_types(components)
        archetype = self.determine_archetype(frozenset(types))
        current_archetype = self.entities[entity]

        self.archetype_table[current_archetype].remove(entity)
        self.archetype_table[archetype].append(entity)

        self.entities[entity] = archetype

        component_dict = {}
        assert len(types) == len(components)
        for i in range(len(types)):
            component_dict[types[i]] = components[i]

        self.components[entity] = component_dict

    # TODO remove_components

    def query(
        self, component_types: list[type[Component]]
    ) -> Generator[tuple[Entity, dict[type[Component], Component]]]:
        archetype_sets: list[frozenset[type[Component]]] = list(
            self.archetypes.keys()
        )
        matching_archetype_sets = filter(
            lambda x: x.issuperset(component_types), archetype_sets
        )
        matching_archetypes = [
            self.archetypes[archetype_set]
            for archetype_set in matching_archetype_sets
        ]

        entities: list[Entity] = []
        for archetype in matching_archetypes:
            if self.archetype_table.get(archetype) is None:
                continue
            entities.extend(self.archetype_table[archetype])

        for entity in entities:
            yield entity, self.components[entity]
