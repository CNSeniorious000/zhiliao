<script lang="ts">
	import { LightSwitch } from '@skeletonlabs/skeleton';
	import { fly } from 'svelte/transition';
	import type { PageData } from './$types';

	export let data: PageData;
	const { records } = data;
</script>

<main class="mt-10 flex flex-col gap-5 w-fit self-center mx-auto">
	<div class="flex flex-row justify-between items-center">
		<a href="/" class="btn variant-soft w-fit btn-sm">&lt; 返回</a>
		<LightSwitch />
	</div>
	<div class="rounded-2xl backdrop-blur-md bg-white/80 dark:bg-surface-900/60 p-5 sm:p-7 md:p-10 gap-3 grid grid-cols-7 sm:grid-cols-8 md:grid-cols-9 lg:grid-cols-10 xl:grid-cols-11 2xl:grid-cols-12">
		{#each records as recordId, index}
			<a href="/records/{recordId}" in:fly|global={{ delay: index * 30, duration: 300 + index * 30, y: 5 }} class="btn btn-sm variant-soft hover:variant-filled">{recordId}</a>
		{/each}
	</div>
</main>
