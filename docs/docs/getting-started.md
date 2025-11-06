# Getting Started

## Prerequisites

- [Node.js](https://nodejs.org/) 20+
- [pnpm](https://pnpm.io/) 9+

## Installation

```bash
pnpm install
```

This installs shared dependencies and links each app workspace.

## Local Development

```bash
pnpm dev:hub
```

Swap `hub` for `vsion`, `nora`, `analyst`, or `nexus` to boot a specific engine.

## Building Static Assets

```bash
pnpm build
```

The command compiles every app with Vite. Each module emits a single-page bundle under `apps/<name>/dist/index.html` ready for embedding.

## Deploying to Netlify

1. Connect the repository to Netlify.
2. Build command: `pnpm i && pnpm build`
3. Publish directory: `apps/hub/dist`
4. Netlify reads redirects from `netlify.toml`, enabling `/vsion`, `/nora`, `/analyst`, and `/nexus` shortcuts.

## Deploying to GitHub Pages

1. Ensure GitHub Pages is enabled for the repository.
2. The workflow `.github/workflows/pages.yml` produces the hub distribution and pushes it to the `gh-pages` branch.
3. Set Pages to serve from `gh-pages`.

## MkDocs Documentation

```bash
cd docs
mkdocs serve
```

The documentation is optional but recommended for sharing research notes and embed recipes.
