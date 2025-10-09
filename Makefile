.PHONY: run 

run:
	@uv run flet src/main.py -w

test:
	@uv run pytest .