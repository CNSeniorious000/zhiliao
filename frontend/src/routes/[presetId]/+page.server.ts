import type { PageServerLoad } from './$types';
import { error, redirect } from '@sveltejs/kit';

export const load = (async ({ params, parent, fetch }) => {
	const { presetId } = params;
	if (presetId === 'new') {
		const res = await fetch(`${process.env.BASEURL}/presets`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ title: '', messages: [] })
		});
		if (res.status !== 201) throw error(404);
		const newPresetId = await res.text();
		throw redirect(307, `/${newPresetId}`);
	}

	const presets = await parent();

	if (!(presetId in presets)) throw error(404, `${presetId} not found`);

	return { presetId, preset: presets[presetId] };
}) satisfies PageServerLoad;
