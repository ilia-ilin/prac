LOCALES_DIR = mood/server/locales
DOMAIN = messages
DOCS_SOURCE = mood/docs/source
DOCS_BUILD = mood/docs/build/html
SOURCES = mood/server/*.py
BABEL_CFG = mood/server/babel.cfg
TEST_DIR = .

.PHONY: all i18n html test clean clean_i18n clean_docs clean_pyc

all: html

i18n: i18n_extract i18n_init i18n_update i18n_compile

i18n_extract:
	pybabel extract -F $(BABEL_CFG) -o $(LOCALES_DIR)/$(DOMAIN).pot $(SOURCES)

i18n_init:
	pybabel init -i $(LOCALES_DIR)/$(DOMAIN).pot -d $(LOCALES_DIR) -l ru

i18n_update:
	pybabel update -i $(LOCALES_DIR)/$(DOMAIN).pot -d $(LOCALES_DIR)

i18n_compile:
	pybabel compile -d $(LOCALES_DIR) -D $(DOMAIN)

html:
	sphinx-build -b html $(DOCS_SOURCE) $(DOCS_BUILD)

test: i18n
	pytest $(TEST_DIR) -v

clean: clean_i18n clean_docs clean_pyc

clean_i18n:
	rm -f $(LOCALES_DIR)/*.pot
	rm -f $(LOCALES_DIR)/ru/LC_MESSAGES/*.mo

clean_docs:
	rm -rf $(DOCS_BUILD)

clean_pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.pytest_cache' -exec rm -rf {} +

help:
	@echo "Доступные цели:"
	@echo "  i18n        - Генерация переводов"
	@echo "  html        - Сборка HTML-документации"
	@echo "  test        - Запуск тестов"
	@echo "  clean       - Очистка всех артефактов"
	@echo "  clean_i18n  - Удаление файлов переводов"
	@echo "  clean_docs  - Удаление сгенерированной документации"
	@echo "  clean_pyc   - Удаление .pyc файлов и кэшей"