# VerbaTerra Simulation Lab

Welcome to the VerbaTerra technical documentation. This site captures the
project vision, methodology, and API needed to reproduce the cultural–
linguistic simulations that power the toolkit.

- Start with the [Overview](overview.md) for a conceptual tour of the research
  program.
- Explore the [Methods](methods/index.md) section to learn how ICLHF and CALR
  connect rituals, trade, symbolism, and hierarchy with linguistic resilience.
- Dive into the [Engines](engines/vsion.md) pages for implementation details of
  the simulators and analytical modules.
- Consult the [API Reference](api/index.md) when integrating VerbaTerra into
  your own experiments.

The documentation is authored in Markdown and built with MkDocs. To serve it
locally run:

```bash
python -m pip install -e .[docs]
mkdocs serve
```

For release automation, see the repository README and GitHub Actions workflow.
