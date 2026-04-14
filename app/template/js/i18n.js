const i18n = {
	en: {
		title: 'Freelancer Dependency Graph',

		search_placeholder: 'search dll...',
		reset: 'reset',
		api_only: 'api only',
		labels: 'labels',
		node_info: 'Node info',
		click_node: 'Click a node.',

		degree: 'degree',
		clean_exports: 'clean exports',
		raw_exports: 'raw exports',
		api: 'api',
		imports_from: 'imports from',
		imports_to: 'imports to',

		actions: 'Actions',
		load_exports: 'load exports',
		copy_json: 'copy .json',
		copy_txt: 'copy .txt',

		exports: 'Exports',
		not_loaded: 'Exports not loaded yet.',
		no_clean: 'No clean exports.',
		load_error: 'Failed to load',
		loading: 'loading',

		undecorated: 'undecorated',
		ordinal: 'ordinal',
		address: 'address',

		ordinal_only: '(ordinal only)',

		yes: 'yes',
		no: 'no',

		clipboard_failed: 'clipboard failed',
		json_failed: 'json failed',
		txt_failed: 'txt failed',
		copied: 'copied',

		filter_all: 'all',
		filter_reverse: 'reverse',
		filter_clean: 'clean',
		filter_raw: 'raw',
		empty: 'empty',

		dll: 'dll',
		undec_short: 'undec',
		no_results: 'no results',
		search_global: 'search exports...',

		close: 'close',
		language: 'language',

		footer_created_by: 'Created by',
		footer_github: 'BinNexus on GitHub',

		runtime: 'runtime',
		static: 'static',
	},
	ru: {
		title: 'Граф зависимостей Freelancer',

		search_placeholder: 'поиск dll...',
		reset: 'сброс',
		api_only: 'только api',
		labels: 'лейблы',
		node_info: 'Информация',
		click_node: 'Нажми на ноду.',

		degree: 'степень',
		clean_exports: 'чистые экспорты',
		raw_exports: 'сырые экспорты',
		api: 'api',
		imports_from: 'входящие',
		imports_to: 'исходящие',

		actions: 'Действия',
		load_exports: 'загрузить экспорты',
		copy_json: 'копировать .json',
		copy_txt: 'копировать .txt',

		exports: 'Экспорты',
		not_loaded: 'Экспорты ещё не загружены.',
		no_clean: 'Чистых экспортов нет.',
		load_error: 'Ошибка загрузки',
		loading: 'загрузка',

		undecorated: 'деманглированное имя',
		ordinal: 'ординал',
		address: 'адрес',

		ordinal_only: '(только ординал)',

		yes: 'да',
		no: 'нет',

		clipboard_failed: 'ошибка буфера',
		json_failed: 'ошибка json',
		txt_failed: 'ошибка txt',
		copied: 'скопировано',

		filter_all: 'все',
		filter_reverse: 'требуют реверса',
		filter_clean: 'чистые',
		filter_raw: 'сырые',
		empty: 'пусто',

		dll: 'библиотека',
		undec_short: 'демангл',
		no_results: 'ничего не найдено',
		search_global: 'поиск экспортов...',

		close: 'закрыть',
		language: 'язык',

		footer_created_by: 'Создано',
		footer_github: 'BinNexus на GitHub',

		runtime: 'рантайм',
		static: 'статик',
	},
}

let currentLang = 'en'

function t(key) {
	return i18n[currentLang][key] || key
}
