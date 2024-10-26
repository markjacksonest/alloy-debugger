export:
	conda env export --from-history > environment-from-history.yml
	conda env export --no-builds > environment-no-builds.yml
	conda env export > environment.yml
	pip list --format=freeze > requirements.txt
