# VerbaTerra Lab

VerbaTerra Lab is a client-only exploration space for cultural, linguistic, and educational scenarios. The monorepo contains four interactive engines and a shared hub that can be deployed as static assets on Netlify, GitHub Pages, or embedded inside Google Sites.

## Repository Layout

```
verbaterra-lab/
  LICENSE
  README.md
  netlify.toml
  package.json
  pnpm-lock.yaml
  apps/
    hub/
    vsion/
    nora/
    analyst/
    nexus/
  data/
  docs/
    mkdocs.yml
    docs/
  .github/workflows/
```

### Engines

| Module | Description |
| --- | --- |
| **Hub** | Central landing portal with navigation cards, embed snippets, and launchers for each engine. |
| **vSION** | Agent-based civilization simulation that lets you tune ritual, trade, symbolism, and hierarchy while visualising outcomes. |
| **NΦRA** | Symbolic grammar playground that transforms seed lexicons using cultural weightings and exports CSV snapshots. |
| **Analyst** | Metrics explorer that ingests CSV data, infers schema, and computes demonstrative NLIS and CRM indicators with charts. |
| **Nexus** | Educator and researcher control panel with guidance, preset launch links, and an embed generator. |

### Quick Start

1. Install dependencies:
   ```bash
   pnpm install
   ```
2. Run an individual app during development, for example the hub:
   ```bash
   pnpm dev:hub
   ```
   Each engine has a matching `dev:<name>` command.
3. Build every app for static deployment:
   ```bash
   pnpm build
   ```
4. Run unit tests:
   ```bash
   pnpm test
   ```

### Deployment

#### Netlify

1. Connect the repository to Netlify.
2. Use build command `pnpm i && pnpm build`.
3. Set publish directory to `apps/hub/dist`.
4. The provided `netlify.toml` configures friendly redirects to each engine distribution folder.

#### GitHub Pages

The GitHub workflow `.github/workflows/pages.yml` builds the project and publishes the hub distribution to the `gh-pages` branch automatically. Enable GitHub Pages for the repository and point it to the `gh-pages` branch.

### Google Sites Embedding

1. Build the project and deploy to Netlify or GitHub Pages.
2. In Google Sites, choose **Insert → Embed → By URL**.
3. Paste one of the engine URLs:
   * `https://YOUR_DOMAIN/apps/vsion/dist/index.html`
   * `https://YOUR_DOMAIN/apps/nora/dist/index.html`
   * `https://YOUR_DOMAIN/apps/analyst/dist/index.html`
   * `https://YOUR_DOMAIN/apps/nexus/dist/index.html`
4. Adjust iframe size (recommended width 100%, height 700–800px).

### Documentation

MkDocs documentation lives in `docs/` and includes engine overviews, metrics references, and embed guidance. Serve locally with:

```bash
cd docs
mkdocs serve
```

### License

Released under the [MIT License](LICENSE).
