import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

export const load = (async ({ fetch }) => {
	const res = await fetch(`${process.env.BASEURL}/records`);
	if (res.status !== 200) throw error(404);
	const records = await res.json();
	return { records };
}) satisfies PageServerLoad;
