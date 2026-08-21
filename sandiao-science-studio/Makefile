PYTHON ?= python3
STORY ?= stories/ac-16c.json

.PHONY: install validate build test clean
install:
	$(PYTHON) -m pip install -e .
validate:
	PYTHONPATH=src $(PYTHON) -m sandiao_studio validate $(STORY)
build:
	PYTHONPATH=src $(PYTHON) -m sandiao_studio build $(STORY)
test:
	PYTHONPATH=src $(PYTHON) -m pytest -q
clean:
	rm -rf build/audio output/*.wav output/*.mp4
