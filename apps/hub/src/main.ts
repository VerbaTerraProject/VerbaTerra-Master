import './styles.css';

type EngineCard = {
  title: string;
  description: string;
  href: string;
  ariaLabel: string;
};

const cards: EngineCard[] = [
  {
    title: 'vSION',
    description: 'Civilisation simulation exploring ritual, trade, symbolism, and hierarchy.',
    href: '/vsion',
    ariaLabel: 'Open the vSION simulation'
  },
  {
    title: 'NΦRA',
    description: 'Symbolic grammar interpreter that evolves lexicons under cultural pressure.',
    href: '/nora',
    ariaLabel: 'Open the NORA engine'
  },
  {
    title: 'Analyst',
    description: 'Upload CSV data, compute NLIS/CRM metrics, and visualise insights with charts.',
    href: '/analyst',
    ariaLabel: 'Open the Analyst engine'
  },
  {
    title: 'Nexus',
    description: 'Educator and researcher cockpit with guides, presets, and embed generator.',
    href: '/nexus',
    ariaLabel: 'Open the Nexus interface'
  }
];

const embedUrls = [
  'https://YOUR-SITE.netlify.app/apps/vsion/dist/index.html',
  'https://YOUR-SITE.netlify.app/apps/nora/dist/index.html',
  'https://YOUR-SITE.netlify.app/apps/analyst/dist/index.html',
  'https://YOUR-SITE.netlify.app/apps/nexus/dist/index.html'
];

function createCard(card: EngineCard): HTMLElement {
  const element = document.createElement('article');
  element.className = 'card';

  const title = document.createElement('h2');
  title.textContent = card.title;
  element.appendChild(title);

  const description = document.createElement('p');
  description.textContent = card.description;
  element.appendChild(description);

  const link = document.createElement('a');
  link.href = card.href;
  link.textContent = 'Launch';
  link.setAttribute('aria-label', card.ariaLabel);
  element.appendChild(link);

  return element;
}

function createEmbedSnippet(url: string): HTMLElement {
  const wrapper = document.createElement('div');
  wrapper.className = 'snippet';

  const button = document.createElement('button');
  button.className = 'copy';
  button.type = 'button';
  button.textContent = 'Copy';
  button.setAttribute('aria-label', `Copy embed snippet for ${url}`);

  const iframeCode = `<iframe src="${url}" style="width:100%;height:700px;border:0;border-radius:12px" loading="lazy"></iframe>`;

  const pre = document.createElement('pre');
  pre.textContent = iframeCode;

  button.addEventListener('click', async () => {
    try {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(iframeCode);
      } else {
        const textarea = document.createElement('textarea');
        textarea.value = iframeCode;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
      }
      button.textContent = 'Copied!';
      setTimeout(() => (button.textContent = 'Copy'), 2000);
    } catch (error) {
      console.error('Failed to copy embed code', error);
      button.textContent = 'Failed';
      setTimeout(() => (button.textContent = 'Copy'), 2500);
    }
  });

  wrapper.appendChild(button);
  wrapper.appendChild(pre);
  return wrapper;
}

function bootstrap(): void {
  const app = document.getElementById('app');
  if (!app) return;

  const header = document.createElement('header');
  const title = document.createElement('h1');
  title.textContent = 'VerbaTerra Lab';
  const subtitle = document.createElement('p');
  subtitle.textContent = 'A static laboratory for civilisational imagination, linguistic evolution, and classroom-ready storytelling.';
  header.appendChild(title);
  header.appendChild(subtitle);

  const grid = document.createElement('section');
  grid.className = 'grid';
  cards.map(createCard).forEach((card) => grid.appendChild(card));

  const snippetSection = document.createElement('section');
  snippetSection.className = 'section';
  const heading = document.createElement('h2');
  heading.textContent = 'Embed Snippets';
  const instructions = document.createElement('p');
  instructions.textContent = 'Use these iframe snippets to embed engines into Google Sites or other static hosts.';

  snippetSection.appendChild(heading);
  snippetSection.appendChild(instructions);
  embedUrls.map(createEmbedSnippet).forEach((snippet) => snippetSection.appendChild(snippet));

  app.appendChild(header);
  app.appendChild(grid);
  app.appendChild(snippetSection);
}

bootstrap();
