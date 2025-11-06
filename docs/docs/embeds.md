# Google Sites Embeds

Embedding VerbaTerra Lab engines inside Google Sites only requires the published URLs from Netlify or GitHub Pages.

## Steps

1. Publish the repository to Netlify or GitHub Pages.
2. Copy the URL for the engine you want to embed.
3. In Google Sites choose **Insert → Embed → By URL** and paste the link.
4. Resize the iframe (recommended height: 800px).

## Snippets

```html
<!-- Replace YOUR_DOMAIN with the deployed host -->
<iframe src="https://YOUR_DOMAIN/apps/vsion/dist/index.html"
        style="width:100%;height:800px;border:0;border-radius:12px" loading="lazy"></iframe>

<iframe src="https://YOUR_DOMAIN/apps/nora/dist/index.html"
        style="width:100%;height:800px;border:0;border-radius:12px" loading="lazy"></iframe>

<iframe src="https://YOUR_DOMAIN/apps/analyst/dist/index.html"
        style="width:100%;height:800px;border:0;border-radius:12px" loading="lazy"></iframe>

<iframe src="https://YOUR_DOMAIN/apps/nexus/dist/index.html"
        style="width:100%;height:800px;border:0;border-radius:12px" loading="lazy"></iframe>
```

## Accessibility Tips

- Keep contrast high inside each embed.
- Provide descriptive captions around the iframe in Google Sites so readers understand the context.
- Encourage keyboard navigation by highlighting focusable elements in your Google Site.
