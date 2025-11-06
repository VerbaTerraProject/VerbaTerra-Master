import './styles.css';
import guideContent from './guide.md?raw';

interface ModulePreset {
  id: string;
  name: string;
  description: string;
  url: string;
}

const MODULES: ModulePreset[] = [
  {
    id: 'vsion',
    name: 'vSION',
    description: 'Simulation with ritual/trade/symbolism/hierarchy sliders.',
    url: '/vsion#ritual=0.70&trade=0.45&symbolism=0.8&hierarchy=0.4'
  },
  {
    id: 'nora',
    name: 'NΦRA',
    description: 'Lexicon rule interpreter for symbolic evolution.',
    url: '/nora'
  },
  {
    id: 'analyst',
    name: 'Analyst',
    description: 'Metrics explorer for NLIS/CRM datasets.',
    url: '/analyst'
  },
  {
    id: 'nexus',
    name: 'Nexus',
    description: 'Educator and researcher coordination space.',
    url: '/nexus'
  }
];

function markdownToHtml(markdown: string): string {
  const lines = markdown.split('\n');
  let html = '';
  let listMode: 'ul' | 'ol' | null = null;

  const closeList = () => {
    if (listMode) {
      html += `</${listMode}>`;
      listMode = null;
    }
  };

  for (const line of lines) {
    if (line.startsWith('# ')) {
      closeList();
      html += `<h1>${line.slice(2)}</h1>`;
      continue;
    }
    if (line.startsWith('## ')) {
      closeList();
      html += `<h2>${line.slice(3)}</h2>`;
      continue;
    }
    if (line.startsWith('- ')) {
      if (listMode !== 'ul') {
        closeList();
        html += '<ul>';
        listMode = 'ul';
      }
      html += `<li>${line.slice(2)}</li>`;
      continue;
    }
    const orderedMatch = line.match(/^(\d+)\.\s+(.*)$/);
    if (orderedMatch) {
      if (listMode !== 'ol') {
        closeList();
        html += '<ol>';
        listMode = 'ol';
      }
      html += `<li>${orderedMatch[2]}</li>`;
      continue;
    }
    if (!line.trim()) {
      closeList();
      continue;
    }
    closeList();
    html += `<p>${line}</p>`;
  }

  closeList();
  return html;
}

function createEmbedCode(module: string, customPath = ''): string {
  const base = `https://YOUR_DOMAIN/apps/${module}/dist/index.html`;
  const url = customPath ? `${base}${customPath.startsWith('#') ? customPath : `#${customPath}`}` : base;
  return `<iframe src="${url}" style="width:100%;height:780px;border:0;border-radius:12px" loading="lazy"></iframe>`;
}

function main(): void {
  const app = document.getElementById('app');
  if (!app) return;
  app.innerHTML = '';

  const header = document.createElement('header');
  const title = document.createElement('h1');
  title.textContent = 'VerbaTerra Nexus';
  const subtitle = document.createElement('p');
  subtitle.textContent = 'Launch presets, review facilitation guides, and generate embed snippets for your learning network.';
  header.appendChild(title);
  header.appendChild(subtitle);

  const sections = document.createElement('section');
  sections.className = 'sections';

  const guidePanel = document.createElement('article');
  guidePanel.className = 'panel';
  const guideHeading = document.createElement('h2');
  guideHeading.textContent = 'Facilitation Guide';
  const guideBody = document.createElement('div');
  guideBody.innerHTML = markdownToHtml(guideContent);
  guidePanel.appendChild(guideHeading);
  guidePanel.appendChild(guideBody);

  const linksPanel = document.createElement('article');
  linksPanel.className = 'panel';
  const linkHeading = document.createElement('h2');
  linkHeading.textContent = 'Quick Launch';
  const linkList = document.createElement('div');
  linkList.className = 'links';
  MODULES.forEach((module) => {
    const link = document.createElement('a');
    link.href = module.url;
    link.textContent = module.name;
    link.title = module.description;
    linkList.appendChild(link);
  });
  linksPanel.appendChild(linkHeading);
  linksPanel.appendChild(linkList);

  const embedPanel = document.createElement('article');
  embedPanel.className = 'panel';
  const embedHeading = document.createElement('h2');
  embedHeading.textContent = 'Embed Generator';
  const form = document.createElement('form');
  form.addEventListener('submit', (event) => event.preventDefault());

  const select = document.createElement('select');
  select.setAttribute('aria-label', 'Choose module to embed');
  MODULES.forEach((module) => {
    const option = document.createElement('option');
    option.value = module.id;
    option.textContent = module.name;
    select.appendChild(option);
  });

  const customInput = document.createElement('input');
  customInput.type = 'text';
  customInput.placeholder = 'Optional hash params e.g. ritual=0.8&trade=0.3';
  customInput.setAttribute('aria-label', 'Optional hash parameters');

  const generateButton = document.createElement('button');
  generateButton.type = 'button';
  generateButton.textContent = 'Generate Embed';

  const copyButton = document.createElement('button');
  copyButton.type = 'button';
  copyButton.textContent = 'Copy';
  copyButton.style.marginLeft = '0.75rem';

  const embedOutput = document.createElement('textarea');
  embedOutput.className = 'embed-output';
  embedOutput.readOnly = true;
  embedOutput.setAttribute('aria-label', 'Generated embed code');

  const generate = () => {
    const code = createEmbedCode(select.value, customInput.value.trim());
    embedOutput.value = code;
  };

  generateButton.addEventListener('click', generate);
  copyButton.addEventListener('click', async () => {
    if (!embedOutput.value) generate();
    try {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(embedOutput.value);
        copyButton.textContent = 'Copied!';
        setTimeout(() => (copyButton.textContent = 'Copy'), 2000);
      }
    } catch (error) {
      console.warn('Clipboard unavailable', error);
    }
  });

  form.appendChild(select);
  form.appendChild(customInput);
  form.appendChild(generateButton);
  form.appendChild(copyButton);
  form.appendChild(embedOutput);

  embedPanel.appendChild(embedHeading);
  embedPanel.appendChild(form);

  sections.appendChild(guidePanel);
  sections.appendChild(linksPanel);
  sections.appendChild(embedPanel);

  app.appendChild(header);
  app.appendChild(sections);

  generate();
}

main();
