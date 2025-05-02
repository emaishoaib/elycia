# Makefile

note:
	poetry run python scripts/add_note.py

obfuscate:
	poetry run python scripts/add_obfuscation_entry.py

index:
	poetry run python scripts/index_notes.py

query:
	poetry run python scripts/query_brain.py