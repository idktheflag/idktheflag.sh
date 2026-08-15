import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = (await getCollection('blog', ({ data }) => !data.draft)).sort(
    (a, b) => b.data.date.valueOf() - a.data.date.valueOf(),
  );

  return rss({
    title: 'idktheflag — CTF Team Blog',
    description: 'Writeups, recaps, and notes from the idktheflag CTF team.',
    site: context.site ?? 'https://idktheflag.sh',
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.date,
      description: post.data.description,
      categories: [post.data.category, ...(post.data.tags || [])],
      author: post.data.author,
      link: `/blog/${post.id}/`,
    })),
  });
}
