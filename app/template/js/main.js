// DOM refs
const sideBody = document.getElementById('sideBody')
const searchInput = document.getElementById('search')
const apiOnlyCheckbox = document.getElementById('apiOnly')
const showLabelsCheckbox = document.getElementById('showLabels')
const resetViewBtn = document.getElementById('resetView')
const input = document.getElementById('globalSearchInput')
const openBtn = document.getElementById('openGlobalSearch')

if (openBtn) {
	openBtn.addEventListener('click', () => {
		openSearch()
	})
}

input.placeholder = t('search_global')
input.addEventListener('input', () => {
	const q = input.value.trim()

	if (!q) return

	const results = searchExports(q)
	renderSearchResults(results)
})

document.getElementById('searchClose').onclick = closeSearch

// utils
function escapeHtml(str) {
	return String(str)
		.replaceAll('&', '&amp;')
		.replaceAll('<', '&lt;')
		.replaceAll('>', '&gt;')
		.replaceAll('"', '&quot;')
		.replaceAll("'", '&#039;')
}

async function fetchTextFile(path) {
	const res = await fetch(path)
	if (!res.ok) throw new Error(`HTTP ${res.status}`)
	return await res.text()
}

async function fetchJsonFile(path) {
	const res = await fetch(path)
	if (!res.ok) throw new Error(`HTTP ${res.status}`)
	return await res.json()
}

// global API (ВАЖНО)
window.showExports = function (encodedId) {
	const nodeId = decodeURIComponent(encodedId)
	loadExportsForNode(nodeId)
}

window.copyExportsJson = async function (encodedId) {
	const nodeId = decodeURIComponent(encodedId)
	const fileBase = getNodeFileBase(nodeId)
	const jsonPath = `exports/${fileBase}.json`

	try {
		const text = await fetchTextFile(jsonPath)
		await copyTextToClipboard(text, `${fileBase}.json ${t('copied')}`)
	} catch (err) {
		showToast(`${t('json_failed')}: ${err.message}`)
	}
}

window.copyExportsTxt = async function (encodedId) {
	const nodeId = decodeURIComponent(encodedId)
	const fileBase = getNodeFileBase(nodeId)
	const txtPath = `exports/${fileBase}.txt`

	try {
		const text = await fetchTextFile(txtPath)
		await copyTextToClipboard(text, `${fileBase}.txt ${t('copied')}`)
	} catch (err) {
		showToast(`${t('txt_failed')}: ${err.message}`)
	}
}

// UI logic
function clearFocus() {
	cy.elements().removeClass('faded')
	cy.nodes().removeClass('search-hit')
	cy.fit(undefined, 40)
}

function applySearch() {
	const val = searchInput.value.trim().toLowerCase()

	cy.nodes().removeClass('search-hit')

	if (!val) return

	cy.nodes().forEach(n => {
		if (n.id().toLowerCase().includes(val)) {
			n.addClass('search-hit')
		}
	})
}

function applyApiFilter() {
	const apiOnly = apiOnlyCheckbox.checked

	cy.nodes().removeClass('hidden-by-filter')
	cy.edges().removeClass('hidden-by-filter')

	if (!apiOnly) return

	cy.nodes().forEach(n => {
		if (!n.data('has_api')) {
			n.addClass('hidden-by-filter')
		}
	})

	cy.edges().forEach(e => {
		if (
			e.source().hasClass('hidden-by-filter') ||
			e.target().hasClass('hidden-by-filter')
		) {
			e.addClass('hidden-by-filter')
		}
	})
}

function applyLabelMode() {
	const show = showLabelsCheckbox.checked
	cy.style()
		.selector('node')
		.style('label', show ? 'data(label)' : '')
		.update()
}

// events
searchInput.addEventListener('input', applySearch)
apiOnlyCheckbox.addEventListener('change', applyApiFilter)
showLabelsCheckbox.addEventListener('change', applyLabelMode)

resetViewBtn.addEventListener('click', () => {
	searchInput.value = ''
	apiOnlyCheckbox.checked = false
	applyApiFilter()
	clearFocus()
	applyLabelMode()
	sideBody.textContent = t('click_node')
})

// init language
const browserLang = navigator.language.startsWith('ru') ? 'ru' : 'en'
const savedLang = localStorage.getItem('lang')

currentLang = savedLang || browserLang

const langSwitch = document.getElementById('langSwitch')
langSwitch.value = currentLang

langSwitch.addEventListener('change', () => {
	currentLang = langSwitch.value
	localStorage.setItem('lang', currentLang)
	applyTranslations()
})

// init
window.addEventListener('DOMContentLoaded', () => {
	applyTranslations()
	applySearch()
	applyApiFilter()
	applyLabelMode()
})
