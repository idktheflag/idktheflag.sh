import type { CollectionEntry } from 'astro:content';

export type DocEntry = CollectionEntry<'docs'>;

export interface DocCategory {
  slug: string;
  title: string;
  docs: DocEntry[];
}

const titleFromSlug = (slug: string) =>
  slug
    .split('-')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');

export const getDocCategory = (doc: DocEntry) => doc.id.split('/')[0] ?? 'general';

export const sortDocs = (docs: DocEntry[]) =>
  [...docs].sort((a, b) => {
    const categoryCompare = getDocCategory(a).localeCompare(getDocCategory(b));
    if (categoryCompare !== 0) return categoryCompare;
    return a.data.order - b.data.order || a.data.title.localeCompare(b.data.title);
  });

export const groupDocs = (docs: DocEntry[]): DocCategory[] => {
  const categories = new Map<string, DocEntry[]>();

  for (const doc of sortDocs(docs)) {
    const category = getDocCategory(doc);
    categories.set(category, [...(categories.get(category) ?? []), doc]);
  }

  return [...categories].map(([slug, entries]) => ({
    slug,
    title: titleFromSlug(slug),
    docs: entries,
  }));
};
