let SEARCH_INDEX = []

fetch('search_index.json')
	.then(r => r.json())
	.then(data => {
		SEARCH_INDEX = data
	})

function openSearch() {
	document.getElementById('globalSearch').classList.remove('hidden')
	document.getElementById('searchBackdrop').classList.remove('hidden')

	const input = document.getElementById('globalSearchInput')
	setTimeout(() => {
		input.focus()
		input.select()
	}, 0)
}

function closeSearch() {
	document.getElementById('globalSearch').classList.add('hidden')
	document.getElementById('searchBackdrop').classList.add('hidden')

	const input = document.getElementById('globalSearchInput')
	const results = document.getElementById('globalSearchResults')

	input.value = ''
	results.innerHTML = ''
	results.classList.remove('has-results')
}

function searchExports(query) {
	query = query.toLowerCase()

	return SEARCH_INDEX.filter(e => {
		return (
			e.symbol?.toLowerCase().includes(query) ||
			e.undec?.toLowerCase().includes(query) ||
			e.address?.includes(query)
		)
	}).slice(0, 50)
}

function renderSearchResults(list) {
	const box = document.getElementById('globalSearchResults')

	if (!list || list.length === 0) {
		box.classList.remove('has-results')
		box.innerHTML = `<div class="mono-box">${t('no_results')}</div>`
		return
	}

	box.classList.add('has-results') // 💥 ВАЖНО

	box.innerHTML = list
		.map(
			item => `
		<div class="export-item">
			<div class="sym copyable" data-copy="${escapeHtml(item.symbol)}">
				${escapeHtml(item.symbol)}
			</div>

			<div class="export-row">
				<span class="k">${t('dll')}</span>
				<span class="value">${escapeHtml(item.dll)}</span>
			</div>

			<div class="export-row">
				<span class="k">${t('address')}</span>
				<span class="value copyable" data-copy="${escapeHtml(item.address)}">
					${escapeHtml(item.address)}
				</span>
			</div>

			${
				item.undec
					? `
				<div class="export-row">
					<span class="k">${t('undec_short')}</span>
					<span class="value copyable" data-copy="${escapeHtml(item.undec)}">
						${escapeHtml(item.undec)}
					</span>
				</div>
			`
					: ''
			}
		</div>
	`,
		)
		.join('')
}
