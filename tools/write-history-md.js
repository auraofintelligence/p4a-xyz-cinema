const fs = require('fs');
const path = require('path');

const chunks = [];
process.stdin.on('data', (chunk) => chunks.push(chunk));
process.stdin.on('end', () => {
  const raw = Buffer.concat(chunks).toString('utf8');
  const history = JSON.parse(raw);
  if (!history.sources) {
    const byUrl = new Map();
    for (const event of history.events || []) {
      for (const source of event.sources || []) {
        byUrl.set(source.url, source);
      }
    }
    history.sources = Array.from(byUrl.values());
  }
  if (!history.sortingNotes) {
    history.sortingNotes = [
      'sortYear is numeric so ancient, approximate and modern events can be sorted without parsing date labels.',
      'level basic is the plain public path. level advanced is for constitutional, electoral and institutional detail.',
      'themes allow the page controls and future agents to group history by topic.',
      'Every event should keep at least one source link.'
    ];
  }
  const outDir = path.join(process.cwd(), 'content', 'history');
  fs.mkdirSync(outDir, { recursive: true });
  const md = `# ${history.stateName} history

This markdown file powers the generated P4A history page for ${history.stateName}. Edit the JSON block, then rerun \`tools/build-state-sites.ps1\`.

\`\`\`json history-data
${JSON.stringify(history, null, 2)}
\`\`\`
`;
  fs.writeFileSync(path.join(outDir, `${history.slug}.md`), md, 'utf8');
  console.log(`Wrote content/history/${history.slug}.md`);
});
