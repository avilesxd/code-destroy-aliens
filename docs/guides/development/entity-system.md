# 🎮 Entity System

## Overview

This guide covers the Entity Component System (ECS) implementation for Alien Invasion, including entities, components, and systems.

## Core Concepts

### 1. Entity

```python
class Entity:
    def __init__(self, entity_id: int):
        self.id = entity_id
        self.components = {}
        self.active = True

    def add_component(self, component: Component) -> None:
        self.components[type(component)] = component

    def get_component(self, component_type: Type[Component]) -> Optional[Component]:
        return self.components.get(component_type)

    def has_component(self, component_type: Type[Component]) -> bool:
        return component_type in self.components

    def remove_component(self, component_type: Type[Component]) -> None:
        if component_type in self.components:
            del self.components[component_type]
```

### 2. Component

```python
class Component:
    def __init__(self):
        self.entity = None

    def attach_to_entity(self, entity: Entity) -> None:
        self.entity = entity

    def detach_from_entity(self) -> None:
        self.entity = None
```

### 3. System

```python
class System:
    def __init__(self):
        self.entities = set()
        self.required_components = set()

    def add_entity(self, entity: Entity) -> None:
        if self._entity_has_required_components(entity):
            self.entities.add(entity)

    def remove_entity(self, entity: Entity) -> None:
        if entity in self.entities:
            self.entities.remove(entity)

    def _entity_has_required_components(self, entity: Entity) -> bool:
        return all(entity.has_component(comp) for comp in self.required_components)

    def update(self, delta_time: float) -> None:
        for entity in self.entities:
            self.process_entity(entity, delta_time)

    def process_entity(self, entity: Entity, delta_time: float) -> None:
        raise NotImplementedError
```

## Core Components

### 1. Position

```python
class Position(Component):
    def __init__(self, x: float = 0.0, y: float = 0.0):
        super().__init__()
        self.x = x
        self.y = y
```

### 2. Velocity

```python
class Velocity(Component):
    def __init__(self, x: float = 0.0, y: float = 0.0):
        super().__init__()
        self.x = x
        self.y = y
```

### 3. Sprite

```python
class Sprite(Component):
    def __init__(self, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
```

## Game-Specific Components

### 1. Health

```python
class Health(Component):
    def __init__(self, max_health: int):
        super().__init__()
        self.max_health = max_health
        self.current_health = max_health

    def take_damage(self, amount: int) -> None:
        self.current_health = max(0, self.current_health - amount)

    def is_dead(self) -> bool:
        return self.current_health <= 0
```

### 2. Weapon

```python
class Weapon(Component):
    def __init__(self, damage: int, cooldown: float):
        super().__init__()
        self.damage = damage
        self.cooldown = cooldown
        self.last_shot = 0.0

    def can_shoot(self, current_time: float) -> bool:
        return current_time - self.last_shot >= self.cooldown

    def shoot(self, current_time: float) -> None:
        self.last_shot = current_time
```

## Core Systems

### 1. Movement System

```python
class MovementSystem(System):
    def __init__(self):
        super().__init__()
        self.required_components = {Position, Velocity}

    def process_entity(self, entity: Entity, delta_time: float) -> None:
        position = entity.get_component(Position)
        velocity = entity.get_component(Velocity)
        
        position.x += velocity.x * delta_time
        position.y += velocity.y * delta_time
```

### 2. Rendering System

```python
class RenderingSystem(System):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.required_components = {Position, Sprite}
        self.screen = screen

    def process_entity(self, entity: Entity, delta_time: float) -> None:
        position = entity.get_component(Position)
        sprite = entity.get_component(Sprite)
        
        sprite.rect.x = position.x
        sprite.rect.y = position.y
        self.screen.blit(sprite.image, sprite.rect)
```

## Entity Manager

```python
class EntityManager:
    def __init__(self):
        self.entities = {}
        self.next_entity_id = 0
        self.systems = []

    def create_entity(self) -> Entity:
        entity = Entity(self.next_entity_id)
        self.entities[self.next_entity_id] = entity
        self.next_entity_id += 1
        return entity

    def add_system(self, system: System) -> None:
        self.systems.append(system)
        # Add existing entities to the new system
        for entity in self.entities.values():
            system.add_entity(entity)

    def update(self, delta_time: float) -> None:
        for system in self.systems:
            system.update(delta_time)
```

## Best Practices

### 1. Component Design

- Keep components small and focused
- Use composition over inheritance
- Make components data-oriented
- Avoid component dependencies

### 2. System Design

- Systems should be stateless
- Process entities in batches when possible
- Use appropriate update frequencies
- Handle entity creation/destruction efficiently

### 3. Performance

- Minimize component lookups
- Use spatial partitioning for collision detection
- Implement entity pooling for frequently created/destroyed entities
- Profile system performance regularly

## Tools

### 1. Debugging

- Entity visualization
- Component inspection
- System profiling
- Memory usage monitoring

### 2. Development

- Entity editor
- Component editor
- System configuration
- Performance analysis

## Next Steps

- Read the [Asset Management Guide](assets.md)
- Check out the [Audio System Guide](audio-system.md)
- Learn about [Performance Optimization](performance.md)
