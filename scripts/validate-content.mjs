import fs from 'node:fs';
import path from 'node:path';

function getFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  let files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files = files.concat(getFiles(fullPath));
    } else if (entry.name.endsWith('.md') || entry.name.endsWith('.mdx')) {
      files.push(fullPath);
    }
  }
  return files;
}

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return null;
  const yaml = match[1];
  const result = {};
  for (const line of yaml.split(/\r?\n/)) {
    const colonIdx = line.indexOf(':');
    if (colonIdx !== -1) {
      const key = line.slice(0, colonIdx).trim();
      let val = line.slice(colonIdx + 1).trim();
      if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
        val = val.slice(1, -1);
      }
      result[key] = val;
    }
  }
  return result;
}

function validateCollection(dir, requiredKeys, name) {
  const files = getFiles(dir);
  let errors = 0;
  console.log(`Checking ${name} collection (${files.length} files)...`);
  for (const file of files) {
    const content = fs.readFileSync(file, 'utf-8');
    const fm = parseFrontmatter(content);
    if (!fm) {
      console.error(`❌ Error in ${file}: Missing frontmatter delimiter ---`);
      errors++;
      continue;
    }
    for (const key of requiredKeys) {
      if (!(key in fm)) {
        console.error(`❌ Error in ${file}: Missing required key '${key}'`);
        errors++;
      }
    }
  }
  return errors;
}

const rootDir = process.cwd();
let totalErrors = 0;

totalErrors += validateCollection(path.join(rootDir, 'src', 'blog'), ['title', 'description', 'date', 'author'], 'Blog');
totalErrors += validateCollection(path.join(rootDir, 'src', 'team'), ['handle', 'role', 'bio', 'avatar'], 'Team');
totalErrors += validateCollection(path.join(rootDir, 'src', 'docs'), ['title'], 'Docs');

if (totalErrors > 0) {
  console.error(`\nValidation failed with ${totalErrors} error(s).`);
  process.exit(1);
} else {
  console.log('\n✅ All content collection frontmatter validated successfully!');
}
