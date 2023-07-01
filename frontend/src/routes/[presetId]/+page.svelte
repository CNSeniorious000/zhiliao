<script lang="ts">
	import { Accordion, AccordionItem, LightSwitch } from '@skeletonlabs/skeleton';
	import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';

	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

	import type { PageData } from './$types';
	import { goto, invalidateAll } from '$app/navigation';

	type Role = 'user' | 'assistant' | 'system';
	type Message = { role: Role; content: string; name?: string | null };

	export let data: PageData;

	let {
		presetId,
		preset: { title, messages }
	}: {
		presetId: string;
		preset: { title: string; messages: Message[] };
	} = data;

	async function sync() {
		await fetch(presetId, {
			method: 'PUT',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ title, messages })
		});
		await invalidateAll();
		console.log('updated', { title, messages });
	}

	function insert(position: number) {
		messages = [
			...messages.slice(0, position),
			{
				role: messages[Math.max(0, position - 1)]?.role === 'user' ? 'assistant' : 'user',
				content: ''
			},
			...messages.slice(position)
		];
		sync();
	}

	function remove(position: number) {
		messages = messages.filter((_, i) => i !== position);
		sync();
	}

	function changeRole(role: Role) {
		return { user: 'assistant', assistant: 'system', system: 'user' }[role] as Role;
	}

	async function suicide() {
		fetch(presetId, { method: 'DELETE' });
		await invalidateAll();
		await goto('/');
	}
</script>

<main class="flex flex-col mx-auto max-w-[50em] p-8 gap-3 relative">
	<div class="flex flex-row justify-between items-center">
		<div class="flex flex-row gap-2">
			<a href="/" class="text-lg btn btn-icon variant-soft"> &lt; </a>
			<button class="text-lg btn btn-icon variant-soft-error" on:click={suicide}> - </button>
		</div>
		<LightSwitch />
	</div>
	<div class="h-10 grid absolute self-center place-items-center">
		<h2 class="select-none h3"># {presetId} {title}</h2>
	</div>

	<div class="grid-cols-[auto_1fr_auto] input-group variant-form-material">
		<div class="input-group-shim select-none">课堂名称</div>
		<input bind:value={title} on:blur={sync} class="font-bold input variant-form-material" type="text" placeholder="标题" />
	</div>

	<hr class="!border-dashed" />

	<span>上下文预设</span>

	<Accordion>
		{#each messages as { role, content }, i}
			<AccordionItem open={true}>
				<svelte:fragment slot="summary">
					<span class="tracking-widest uppercase">
						{i} - {role}
					</span>
				</svelte:fragment>
				<svelte:fragment slot="content">
					<div class="flex flex-row gap-10 overflow-scroll hide-scrollbar select-none">
						<button class="tracking-wide btn variant-filled capitalize" on:click={() => (messages[i].role = changeRole(role))}>
							{role}
						</button>

						<div class="flex flex-row w-full gap-2 justify-end">
							<button type="button" class="text-sm btn variant-soft btn-sm" on:click={() => insert(i)}> 在上方添加 </button>
							<button type="button" class="btn btn-sm variant-soft" on:click={() => remove(i)}> 删除本条 </button>
							<button type="button" class="text-sm btn variant-soft btn-sm" on:click={() => insert(i + 1)}> 在下方添加 </button>
						</div>
					</div>

					<label class="label">
						<span>消息内容</span>
						<textarea class="textarea variant-form-material" on:blur={sync} bind:value={content} />
					</label>
				</svelte:fragment>
			</AccordionItem>
		{/each}
	</Accordion>
	<button class="w-full btn variant-soft" on:click={() => insert(messages.length)}>+</button>
</main>

<style lang="postcss">
	button,
	a,
	span {
		@apply select-none;
	}
</style>
