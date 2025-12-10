We will build an interrogator module that essentially implements the first part of the agent architecture stated in the ADJACENT.md document.

The worlds/ project essentially enumerated what a world could look like, so that we can capture the fullness of it. And we explored a few instantiations of it in book/.

This was only a beginning to capture the immediate environment of a world for a given actor.

Given the importance of path dependence, and for privacy reasons, we will capture it in a private memoir/ repo that is outside of this schema/ repo. But something we still structure so that the schema can work upon the memoir repo(set in .env file). Maintain submodule as needed.

The memoir probe will capture scenes of the world as it is experienced by the actor, similar to what we captured in WORLDS.md but it will attempt to capture the fullness of it. Use anthropological, sociological, phenomenological techniques to capture some qualititative information. And structure the life worlds in such a way that it can be visualized in a graph with nodes and edges, and can also represent intersectional worlds schematically so that they can be programmatically worked upon. 

Capture the detailed pipeline and schema for the input/output in a different file(while the instances being captured in the memoir repo). This file will remain the high level intent, and you shouldn't need to modify it.

## Implementation

See the following files for the implementation:

- **[SCHEMA.md](SCHEMA.md)**: Complete schema definition for memoir scenes, including phenomenological, structural, and systemic dimensions, plus graph representation.
- **[PIPELINE.md](PIPELINE.md)**: Detailed pipeline documentation, usage instructions, and data flow.
- **[interrogator.py](interrogator.py)**: Interactive interview module that guides the user through scene capture.
- **[memoir_manager.py](memoir_manager.py)**: Repository manager for the private memoir repo (with privacy validation).
- **[graph.py](graph.py)**: Graph data structures and operations for representing scenes and their relationships.