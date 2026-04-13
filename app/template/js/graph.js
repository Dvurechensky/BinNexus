let currentExports = []
let currentFilter = 'all'

function getNodeFileBase(nodeId) {
	return nodeId.replace(/\.(dll|exe)$/i, '')
}

function escapeHtml(str) {
	return String(str)
		.replaceAll('&', '&amp;')
		.replaceAll('<', '&lt;')
		.replaceAll('>', '&gt;')
		.replaceAll('"', '&quot;')
		.replaceAll("'", '&#039;')
}

const cy = cytoscape({
	container: document.getElementById('cy'),

	elements: [
		...data.nodes.map(n => ({
			data: {
				id: n.id,
				degree: n.degree ?? 0,
				export_count: n.export_count ?? 0,
				export_raw_count: n.export_raw_count ?? 0,
				has_api: !!n.has_api,
				color: n.color || AppConfig.defaultNodeColor,
				label: n.label || `${n.id}\n${n.export_count ?? 0} exp`,
			},
		})),
		...data.edges.map(e => ({
			data: {
				source: e.source,
				target: e.target,
			},
		})),
	],

	style: [
		{
			selector: 'node',
			style: {
				'background-color': 'data(color)',
				label: 'data(label)',
				'font-size': 7,
				color: '#fff',
				'text-wrap': 'wrap',
				'text-max-width': 90,
				'text-valign': 'center',
				'text-halign': 'center',
				'border-width': 1,
				'border-color': '#222',
				width: ele => 16 + Math.min(ele.data('degree') * 1.8, 60),
				height: ele => 16 + Math.min(ele.data('degree') * 1.8, 60),
			},
		},
		{
			selector: 'edge',
			style: {
				width: 1.2,
				'line-color': '#777',
				'target-arrow-shape': 'triangle',
				'target-arrow-color': '#777',
				'curve-style': 'bezier',
				'arrow-scale': 0.7,
				opacity: 0.65,
			},
		},
		{
			selector: '.search-hit',
			style: {
				'background-color': AppConfig.searchHitColor,
				'border-width': 2,
				'border-color': '#fff',
			},
		},
		{
			selector: '.faded',
			style: {
				opacity: 0.08,
			},
		},
		{
			selector: '.hidden-by-filter',
			style: {
				display: 'none',
			},
		},
	],

	layout: {
		name: 'cose',
		animate: true,
		fit: true,
		padding: 30,
		nodeRepulsion: 500000,
		idealEdgeLength: 90,
	},
})

function initExportFilters() {
	document.querySelectorAll('.exports-filter button').forEach(btn => {
		btn.onclick = () => {
			document
				.querySelectorAll('.exports-filter button')
				.forEach(b => b.classList.remove('active'))

			btn.classList.add('active')
			currentFilter = btn.dataset.filter

			document
				.querySelectorAll('.exports-filter button')
				.forEach(b => b.classList.remove('active'))

			btn.classList.add('active')

			renderExports()
		}
	})
}

function applyActiveFilterUI() {
	document.querySelectorAll('.exports-filter button').forEach(btn => {
		btn.classList.toggle('active', btn.dataset.filter === currentFilter)
	})
}

cy.on('tap', 'node', function (evt) {
	const node = evt.target

	currentFilter = 'all'

	cy.elements().addClass('faded')

	node.removeClass('faded')
	node.connectedEdges().removeClass('faded')
	node.connectedEdges().sources().removeClass('faded')
	node.connectedEdges().targets().removeClass('faded')

	renderNodeInfo(node)
	loadExportsForNode(node.data('id'))
	setTimeout(() => {
		initExportFilters()
		applyActiveFilterUI()
	}, 0)
})

cy.on('tap', function (evt) {
	if (evt.target === cy) {
		cy.elements().removeClass('faded')
		sideBody.textContent = t('click_node')
	}
})

function renderNodeInfo(node) {
	const d = node.data()

	sideBody.innerHTML = `
					<div class="panel-card">
						<div class="panel-title">${escapeHtml(d.id)}</div>

						<div class="meta-grid">
							<div class="meta-key">${t('degree')}</div>
							<div class="meta-value"><span class="badge">${d.degree}</span></div>

							<div class="meta-key">${t('clean_exports')}</div>
							<div class="meta-value"><span class="badge">${d.export_count}</span></div>

							<div class="meta-key">${t('raw_exports')}</div>
							<div class="meta-value"><span class="badge">${d.export_raw_count}</span></div>

							<div class="meta-key">${t('api')}</div>
							<div class="meta-value">
								<span class="badge ${d.has_api ? 'badge-yes' : ''}">
									${d.has_api ? t('yes') : t('no')}
								</span>
							</div>

							<div class="meta-key">${t('imports_from')}</div>
							<div class="meta-value"><span class="badge">${node.incomers('edge').length}</span></div>

							<div class="meta-key">${t('imports_to')}</div>
							<div class="meta-value"><span class="badge">${node.outgoers('edge').length}</span></div>
						</div>
					</div>

					<div class="panel-card">
						<div class="panel-title">${t('actions')}</div>
						<div class="actions">
							<button class="btn-primary" onclick="window.showExports('${encodeURIComponent(d.id)}')">
								${t('load_exports')}
							</button>
							<button class="btn-subtle" onclick="window.copyExportsJson('${encodeURIComponent(d.id)}')">
								${t('copy_json')}
							</button>
							<button class="btn-subtle" onclick="window.copyExportsTxt('${encodeURIComponent(d.id)}')">
								${t('copy_txt')}
							</button>
						</div>
						<div class="status-line" style="margin-top:10px;">
							JSON: exports/${escapeHtml(getNodeFileBase(d.id))}.json<br>
							TXT: exports/${escapeHtml(getNodeFileBase(d.id))}.txt
						</div>
					</div>

					<div class="panel-card">
						<div class="panel-title">${t('exports')}</div>
						<div class="exports-filter">
							<button data-filter="all" class="active">${t('filter_all')}</button>
							<button data-filter="reverse">${t('filter_reverse')}</button>
						</div>
						<div id="exportsBox" class="export-list">
							<div class="mono-box">${t('not_loaded')}</div>
						</div>
					</div>
				`
}

function renderExports() {
	const exportsBox = document.getElementById('exportsBox')
	if (!exportsBox) return

	const list = getFilteredExports()

	if (!list.length) {
		exportsBox.innerHTML = `<div class="mono-box">${t('empty')}</div>`
		return
	}

	exportsBox.innerHTML = list
		.map(item => {
			const symbol = item.symbol || t('ordinal_only')
			const clean = isClean(item)

			return `
			<div class="export-item ${clean ? 'clean' : 'raw'}">

				<span class="sym copyable" data-copy="${escapeHtml(symbol)}">
					${escapeHtml(symbol)}
				</span>

				<div class="export-row">
					<span class="k">${t('ordinal')}</span>
					<span class="value copyable" data-copy="${item.ordinal ?? ''}">
						${item.ordinal ?? ''}
					</span>
				</div>

				<div class="export-row export-address">
					<span class="k">${t('address')}</span>
					<span class="value copyable" data-copy="${escapeHtml(item.address ?? '')}">
						${escapeHtml(item.address ?? '')}
					</span>
				</div>

				${
					item.symbol_undecorated
						? `
					<div class="export-row export-undec">
						<span class="k">${t('undecorated')}</span>
						<span class="undec-text copyable" data-copy="${escapeHtml(item.symbol_undecorated)}">
							${escapeHtml(item.symbol_undecorated)}
						</span>
					</div>
					`
						: ''
				}

			</div>
		`
		})
		.join('')
}

async function loadExportsForNode(nodeId) {
	const exportsBox = document.getElementById('exportsBox')
	if (!exportsBox) return

	const fileBase = getNodeFileBase(nodeId)
	const jsonPath = `exports/${fileBase}.json`

	exportsBox.innerHTML = `
		<div class="mono-box">
			${t('loading')} ${escapeHtml(jsonPath)} ...
		</div>
	`

	try {
		const report = await fetchJsonFile(jsonPath)

		// СОХРАНЯЕМ ВСЕ
		currentExports = report.exports || []

		if (!currentExports.length) {
			exportsBox.innerHTML = `<div class="mono-box">empty</div>`
			return
		}

		renderExports()
	} catch (err) {
		exportsBox.innerHTML = `
			<div class="mono-box">
				${t('load_error')} ${escapeHtml(jsonPath)}
				${escapeHtml(err.message)}
			</div>
		`
	}
}

function hasUndecorated(exp) {
	return exp.symbol_undecorated && exp.symbol_undecorated.trim() !== ''
}

function isClean(exp) {
	const u = exp.symbol_undecorated
	const s = exp.symbol

	return u && u.trim() !== '' && u !== s
}

function getFilteredExports() {
	if (currentFilter === 'clean') {
		return currentExports.filter(isClean)
	}

	if (currentFilter === 'raw') {
		return currentExports.filter(e => !isClean(e))
	}

	if (currentFilter === 'reverse') {
		return currentExports.filter(e => {
			const u = e.symbol_undecorated
			return !u || u.trim() === ''
		})
	}

	return currentExports
}
