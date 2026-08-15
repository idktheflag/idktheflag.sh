import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const title = args[0] || 'My CTF Writeup';
const ctfName = args[1] || 'CTF Event';
const category = args[2] || 'Web';
const author = args[3] || 'qu1ck';

const slug = title
  .toLowerCase()
  .replace(/[^a-z0-9]+/g, '-')
  .replace(/(^-|-$)/g, '');

const dateStr = new Date().toISOString().split('T')[0];

const content = `---
title: "${title}"
description: "Writeup for ${title} from ${ctfName}"
date: ${dateStr}
author: "${author}"
category: "${category}"
tags: ["${category.toLowerCase()}", "writeup"]
draft: false
---

# ${title}

**CTF**: ${ctfName}  
**Category**: ${category}  
**Author**: ${author}  

## Challenge Description

> Add challenge description or prompt here...

## Solution Approach

Describe your step-by-step solver approach and analysis here.

\`\`\`python
# Solver script example
import pwn

print("[+] Flag solved!")
\`\`\`

## Flag

\`\`\`text
idktheflag{example_flag_here}
\`\`\`
`;

const targetDir = path.join(process.cwd(), 'src', 'blog');
fs.mkdirSync(targetDir, { recursive: true });
const targetFile = path.join(targetDir, `${slug}.mdx`);

if (fs.existsSync(targetFile)) {
  console.error(`Error: File ${targetFile} already exists.`);
  process.exit(1);
}

fs.writeFileSync(targetFile, content, 'utf-8');
console.log(`✅ Created new writeup template at src/blog/${slug}.mdx`);
