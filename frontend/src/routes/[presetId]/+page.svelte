<script lang="ts">
	import { Accordion, AccordionItem, LightSwitch, SlideToggle } from '@skeletonlabs/skeleton';
	import { goto, invalidateAll } from '$app/navigation';
	import type { PageData } from './$types';

	type Role = 'user' | 'assistant' | 'system';
	type Message = { role: Role; content: string; name?: string | null };

	export let data: PageData;

	let {
		presetId,
		preset: { title, messages, examples, hideContext }
	}: {
		presetId: string;
		preset: { title: string; messages: Message[]; examples: string[]; hideContext: boolean };
	} = data;

	messages ?? (messages = []);
	examples ?? (examples = []);

	async function sync() {
		await fetch(presetId, {
			method: 'PUT',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ title, messages, examples, hideContext })
		});
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
		return sync();
	}

	function remove(position: number) {
		messages = messages.filter((_, i) => i !== position);
		return sync();
	}

	function changeRole(position: number) {
		messages[position].role = { user: 'assistant', assistant: 'system', system: 'user' }[messages[position].role] as Role;
		return sync();
	}

	async function suicide() {
		fetch(presetId, { method: 'DELETE' });
		await goto('/');
		await invalidateAll();
	}
</script>

<main class="flex flex-col mx-auto max-w-[50em] p-8 gap-3 relative">
	<div class="flex flex-row justify-between items-center">
		<div class="flex flex-row gap-2">
			<a href="/" class="text-lg btn btn-icon variant-soft" on:click={() => sync().then(invalidateAll)}> &lt; </a>
			<button class="text-lg btn btn-icon variant-soft-error" on:click={suicide}> - </button>
		</div>
		<LightSwitch />
	</div>
	<div class="h-10 grid absolute self-center place-items-center">
		<h2 class="select-none h3"># {presetId} {title}</h2>
	</div>

	<div class="grid-cols-[auto_1fr_auto] input-group variant-form-material">
		<div class="input-group-shim select-none">课堂名称</div>
		<input bind:value={title} on:blur={sync} class="font-bold input variant-form-material !rounded-tl-none placeholder:text-current placeholder:opacity-20" type="text" placeholder="追问消息" />
	</div>

	<hr class="!border-dashed" />

	<Accordion>
		<AccordionItem open={true}>
			<svelte:fragment slot="summary">
				<span class="tracking-wide"> 预设上下文 </span>
			</svelte:fragment>

			<svelte:fragment slot="content">
				<div class="flex flex-row justify-between">
					<span>在消息列表中隐藏预设上下文</span>
					<SlideToggle size="sm" name="hideContext" bind:checked={hideContext} on:change={sync} />
				</div>
				{#each messages as { role, content }, i}
					<div class="flex flex-row gap-10 overflow-scroll hide-scrollbar select-none">
						<button class="tracking-widest btn variant-filled uppercase" on:click={() => changeRole(i)}>
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
				{:else}
					<div class="text-center opacity-40 select-none">点击加号来给预设上下文添加消息</div>
				{/each}
				<button class="w-full btn variant-soft" on:click={() => insert(messages.length)}>+</button>
			</svelte:fragment>
		</AccordionItem>
		<AccordionItem open={true}>
			<svelte:fragment slot="summary">
				<span class="tracking-wide"> 预设追问选项 </span>
			</svelte:fragment>
			<svelte:fragment slot="content">
				{#each examples as msg, i}
					<div class="grid-cols-[auto_1fr_auto] input-group variant-form-material">
						<div class="input-group-shim select-none">{i + 1}</div>
						<input bind:value={msg} on:blur={sync} class="font-bold input variant-form-material !rounded-tl-none placeholder:text-current placeholder:opacity-20" type="text" placeholder="标题" />
					</div>
				{:else}
					<div class="text-center opacity-40 select-none">点击加号来添加预设追问选项</div>
				{/each}
				<div class="flex flex-row gap-2">
					<button class="w-full btn variant-soft" on:click={() => ((examples = [...examples, '']), sync())}>+</button>
					<button class="w-full btn variant-soft-error" on:click={() => ((examples = examples.slice(0, -1)), sync())}>-</button>
				</div>
			</svelte:fragment>
		</AccordionItem>
	</Accordion>
</main>

<style lang="postcss">
	button,
	a,
	span {
		@apply select-none;
	}
</style>
