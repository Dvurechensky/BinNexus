function applyTranslations() {
	translateDOM()
	translateAttrs()

	document.title = t('title')

	searchInput.placeholder = t('search_placeholder')
	resetViewBtn.textContent = t('reset')

	document.getElementById('sideHeader').textContent = t('node_info')

	if (!sideBody.dataset.activeNode) {
		sideBody.textContent = t('click_node')
	}
}

function translateDOM() {
	document.querySelectorAll('[data-i18n]').forEach(el => {
		const key = el.getAttribute('data-i18n')
		el.textContent = t(key)
	})
}

function translateAttrs() {
	document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
		const key = el.getAttribute('data-i18n-placeholder')
		el.placeholder = t(key)
	})
}

function showToast(text) {
	let toast = document.getElementById('toast')
	if (!toast) {
		toast = document.createElement('div')
		toast.id = 'toast'
		Object.assign(toast.style, {
			position: 'fixed',
			right: '20px',
			bottom: '20px',
			background: '#252526',
			color: '#fff',
			border: '1px solid #3c3c3c',
			borderRadius: '10px',
			padding: '10px 14px',
			fontSize: '12px',
			zIndex: '9999',
			boxShadow: '0 10px 30px rgba(0,0,0,0.35)',
			opacity: '0',
			transition: 'opacity 0.15s ease',
		})
		document.body.appendChild(toast)
	}

	toast.textContent = text
	toast.style.opacity = '1'

	clearTimeout(showToast._timer)
	showToast._timer = setTimeout(() => {
		toast.style.opacity = '0'
	}, 1400)
}

async function copyTextToClipboard(text, label = 'copied') {
	try {
		await navigator.clipboard.writeText(text)
		showToast(label)
	} catch {
		showToast(t('clipboard_failed'))
	}
}

document.addEventListener('click', async e => {
	const el = e.target.closest('.copyable')
	if (!el) return

	const text = el.dataset.copy
	if (!text) return

	try {
		await navigator.clipboard.writeText(text)

		el.classList.add('copied')
		setTimeout(() => el.classList.remove('copied'), 400)
	} catch (err) {
		console.error(err)
	}
})

document.addEventListener('keydown', e => {
	if (e.ctrlKey && e.key.toLowerCase() === 'p') {
		e.preventDefault()
		e.stopPropagation()

		const overlay = document.getElementById('globalSearch')

		if (overlay.classList.contains('hidden')) {
			openSearch()
		} else {
			closeSearch()
		}
	}
})

document.addEventListener('keydown', e => {
	if (e.key === 'Escape') {
		closeSearch()
	}
})

document.addEventListener('mousedown', e => {
	const overlay = document.getElementById('globalSearch')

	if (!overlay || overlay.classList.contains('hidden')) return

	if (!overlay.contains(e.target)) {
		closeSearch()
	}
})
