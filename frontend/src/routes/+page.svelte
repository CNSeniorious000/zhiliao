<script lang="ts">
	import { LightSwitch } from '@skeletonlabs/skeleton';
	import { invalidateAll } from '$app/navigation';
	export let data;
</script>

<div class="container h-full mx-auto grid place-items-center select-none">
	<div class="rounded-2xl space-y-5 p-8">
		<LightSwitch />
		<h2 class="text-lg tracking-[0.5em] uppercase">zhiliao</h2>
		<h1 class="tracking-widest text-5xl">知了同行</h1>
		<hr class="!border-dashed" />
		<a href="/new" on:click={() => invalidateAll()} class="text-lg w-full p-[0.25pt] btn variant-soft">+</a>
		<ul class="flex flex-col items-start">
			{#each Object.entries(data) as [presetId, { title, messages }]}
				<a href="/{presetId}" class="group py-1 w-full transition-opacity">
					<li class="flex flex-row text-lg gap-2 items-center justify-between transition-all group-hover:translate-x-1 border-l-[2.5pt] border-transparent group-hover:border-primary-600 -ml-2.5 pl-2.5">
						<div class="flex flex-row gap-2 items-center group-hover:-translate-x-0.5 transition-transform">
							<code class="code">{presetId}</code>
							{title}
						</div>
						<span class="opacity-0 group-hover:opacity-100 transition-all group-hover:-translate-x-0.5">&gt;</span>
					</li>
				</a>
			{/each}
		</ul>
	</div>
</div>

<style lang="postcss">
	ul:has(:hover) a:not(a:hover) {
		@apply opacity-30;
	}
</style>
