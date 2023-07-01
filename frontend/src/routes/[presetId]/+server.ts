import type { RequestHandler } from './$types';

export const PUT: RequestHandler = async ({ fetch, params, request }) => {
	const { presetId } = params;
	const body = await request.json();

	const res = await fetch(`${process.env.BASEURL}/presets/${presetId}`, {
		method: 'PUT',
		headers: request.headers,
		body: JSON.stringify(body)
	});

	return new Response(res.body, { status: res.status, headers: res.headers });
};

export const DELETE: RequestHandler = async ({ fetch, params }) => {
	const { presetId } = params;

	const res = await fetch(`${process.env.BASEURL}/presets/${presetId}`, { method: 'DELETE' });

	return new Response(res.body, { status: res.status });
};
