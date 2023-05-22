build:
	docker build -t scrapper-rp5 .
run:
	python ./app/main.py "$(min_date)" "$(max_date)"
test:
	python -m pytest -v
