import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/blog', generateId: ({ entry }) => entry.replace(/\.mdx?$/, '').replace(/\\/g, '/') }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    author: z.string(),
    category: z.string().default('General'),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const team = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/team', generateId: ({ entry }) => entry.replace(/\.mdx?$/, '').replace(/\\/g, '/') }),
  schema: z.object({
    handle: z.string(),
    role: z.string(),
    categories: z
      .array(z.string().nullable())
      .transform((categories) => categories.filter((c): c is string => Boolean(c && c.trim()))),
    bio: z.string(),
    avatar: z.string(),
    order: z.number().default(999),
    github: z.string().optional(),
    twitter: z.string().optional(),
    discord: z.string().optional(),
    ctftime: z.string().optional(),
  }),
});

const docs = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/docs', generateId: ({ entry }) => entry.replace(/\.mdx?$/, '').replace(/\\/g, '/') }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    order: z.number().default(999),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog, team, docs };
