import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

export const load = (async ({ params, fetch }) => {
	const { recordId } = params;
	const res = await fetch(`${process.env.BASEURL}/records/${recordId}`);
	if (res.status !== 200) throw error(404);
	const messages = await res.json();
	return { messages };
}) satisfies PageServerLoad;
