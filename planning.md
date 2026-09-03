# RPG Box development plan

## Goal and scope

Build a small, replayable party-based fantasy adventure in the spirit of the
classic Gold Box games: create a party, explore a keyed area on a tactical grid,
make text/menu choices, enter turn-based encounters, return to camp/town, and
save the adventure. The first release should be one polished short adventure,
not a general-purpose RPG engine or content editor.

The guiding rule is: prove one complete play loop before expanding the world.
Every feature should be judged by whether it makes that loop more playable,
testable, or authorable.

## Current state (2026-09-03)

- [x] Cover, intro/demo, main menu, party assignment, deletion, character sheet
- [x] Character creation flow: race, alignment, class, stats, adjustments, HP
- [x] Shared UI styling and reusable bottom action bar
- [x] Initial equipment/inventory model and equipment rules
- [x] Foundational ability, encumbrance, combat, saving throw, and leveling rules
- [x] Rules/UI separation is started; model and rules do not depend on Panda3D
- [x] 42 automated tests pass
- [~] Matte story screen accepts scene-shaped data, but is still a presentation
      stub and does not yet drive game state
- [~] Type/lint hygiene needs a pass (Ruff: 6 errors; type checker: 19 diagnostics)
- [ ] Persistent character/game saves
- [ ] Runtime world/area state, map transitions, encounters, and exploration view

## Near-term milestone: one playable dungeon room

This is the next meaningful milestone. It should be possible to create or use
a party, enter one small dungeon, move on a grid, inspect a feature, trigger a
simple encounter, resolve it, and return to the dungeon with state preserved.

### Stabilize the seam before building the viewport

- [ ] Replace the `MasterFSM`'s scene-choice `pass` with an explicit application
      command/result boundary.
- [ ] Introduce a small `GameSession` (or `AdventureState`) containing party,
      current area, position, facing, time, flags, and active encounter.
- [ ] Keep UI pages as views/controllers: they send commands and render state;
      they should not own world rules or mutate map data directly.
- [ ] Add tests for session transitions and movement without starting Panda3D.
- [ ] Clean up the six Ruff errors and either fix or consciously scope the type
      checker diagnostics. Do not let static-analysis work become a rewrite.

### Build the smallest area exploration slice

- [ ] Define an area as a stable ID, display name, dimensions, cells, start
      position, exits, and keyed points of interest.
- [ ] Define cell properties separately from runtime state: blocked/open,
      terrain, elevation, wall/door edges, and optional art/description IDs.
- [ ] Define runtime state separately: party position/facing, opened doors,
      searched features, defeated encounters, and area flags.
- [ ] Implement grid movement, collision, facing/turning, and a simple action
      log first; add 3D floor/wall presentation after these rules are tested.
- [ ] Build a deliberately plain 3D grid-walker viewport for one room. Keep
      party/status/action UI in the existing 2D DirectGUI layer.
- [ ] Add inspect/search/open actions and one deterministic transition to a
      text encounter.

### Add the first encounter, not the whole combat system

- [ ] Create an encounter interface with `can_trigger`, `start`, available
      actions, `resolve`, and an outcome applied to `GameSession`.
- [ ] Implement one non-combat scene and one very small combat: one enemy type,
      attack/defend, damage, victory/defeat, and return to exploration.
- [ ] Route encounter outcomes through rules/services, not UI callbacks.
- [ ] Add tests for movement, trigger conditions, combat outcome, and persistence
      of a defeated encounter.

## Content and data architecture

Use stable IDs and typed Python domain objects at runtime. Keep three things
distinct:

1. Content definitions: areas, cells, actors, items, encounters, scenes, and
   transitions authored by the developer.
2. Runtime state: current location, party condition, inventory, flags, time,
   opened/defeated content, and completed objectives.
3. Presentation: Panda3D nodes, DirectGUI widgets, textures, and input mapping.

SQLite is reasonable for a future editor and for larger authored content, but
it should sit behind repositories rather than become the game's domain model.
Start with a tiny in-memory repository (and optionally JSON fixtures) so the
dungeon slice remains easy to test. Move to SQLite when there are enough
entities to benefit from querying or when the editor has a concrete workflow.
At that point, use migrations, stable string IDs, a schema version, and an
import/export path; do not store Panda3D objects or arbitrary Python code in
the database.

Likely initial repository interfaces:

- `AreaRepository.get(area_id)`
- `EncounterRepository.get(encounter_id)`
- `SceneRepository.get(scene_id)`
- `GameSaveRepository.save/load(slot)`

## After the dungeon slice

- [ ] Complete equipment/wealth/shop flow, armor presentation, languages,
      race/class abilities, and leveling beyond level 1 as needed by playtests
- [ ] Generalize encounter types: combat, story, shop, treasure, travel, and
      skill/check outcomes
- [ ] Add save/load for `GameSession`; then add campaign/world progression
- [ ] Add a country/wilderness map using the same area/transition contracts
- [ ] Add town/camp screens and travel procedures
- [ ] Improve UI abstraction where repetition is demonstrated by real screens;
      avoid building a UI framework in advance
- [ ] Build an editor only after authoring the first adventure exposes the
      actual editing pain points

## Explicitly deferred

- Physics-based dice simulation
- Character-sheet export
- A generalized visual editor
- Full multiclass/leveling coverage before the first playable encounter
- Large-scale procedural generation
- Broad art production before the interaction loop is fun

## Definition of “ready” for area exploration

The project is ready now for a narrow exploration prototype, provided it is
kept to one test area. It is not ready for a full world architecture or editor
because runtime state, persistence, encounter contracts, and map transitions
have not yet been exercised. The next success criterion is a 10–15 minute
vertical slice, not a finished 3D engine.
