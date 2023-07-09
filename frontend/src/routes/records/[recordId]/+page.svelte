<script lang="ts">
	import { fly } from 'svelte/transition';
	import { LightSwitch } from '@skeletonlabs/skeleton';
	import type { PageData } from './$types';

	export let data: PageData;
	const { messages } = data;
</script>

<main class="mt-10 flex flex-col gap-5">
	<div class="flex flex-row justify-between items-center">
		<a href="/records" class="select-none btn variant-soft w-fit btn-sm">&lt; 返回</a>
		<LightSwitch />
	</div>
	<div class="rounded-2xl backdrop-blur-md bg-white/80 dark:bg-surface-900/60 p-5 sm:p-7 md:p-10 gap-3 flex flex-col">
		{#each messages as { role, content }, index}
			<div in:fly|global={{ delay: index * 100, duration: 300 + 30 * index, y: 5 }} class="flex gap-3 flex-row" class:flex-row-reverse={role === 'user'}>
				<div class="rounded-full select-none scale-80 w-12 h-12 shrink-0 variant-soft grid place-items-center uppercase font-bold text-surface-500/50" class:!variant-soft-secondary={role === 'user'}>{role[0]}</div>
				<div class="card p-3 px-4 variant-soft transition-colors hover:variant-filled space-y-2" class:rounded-tl-lg={role !== 'user'} class:rounded-tr-lg={role === 'user'} class:!variant-soft-secondary={role === 'user'} class:hover:!variant-filled-secondary={role === 'user'}>
					{content}
				</div>
			</div>
		{/each}
	</div>
</main>

<style>
	main {
		width: min(90ch, 100% - 5rem);
		margin-inline: auto;
	}
</style>
