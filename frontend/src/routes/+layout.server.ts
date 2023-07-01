import type { LayoutServerLoad } from './$types';
import 'dotenv/config';

export const load = (async ({ fetch }) => {
	const res = await fetch(`${process.env.BASEURL}/presets`);
	const data = await res.json();
	return data;
}) satisfies LayoutServerLoad;
