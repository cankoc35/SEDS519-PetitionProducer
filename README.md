# SEDS519 Petition Producer

Desktop petition management system developed for `SEDS519 HW1` with `Python` and `Flet`.

## What The Project Does

- provides `6` built-in petition templates
- lets the user create academic and administrative petitions from scratch
- supports saving petitions as `draft` or `registered`
- stores petitions in `data/petitions/`
- stores user-created templates in `data/templates/`
- supports attachments
- lets users reopen saved drafts
- shows registered petitions in a formal `A4` document view
- exports registered petitions as `PDF`

## Design Patterns Used

- `Factory Method`: create academic and administrative petition objects
- `Singleton`: shared petition registry
- `Iterator`: filter and traverse saved petitions
- `Prototype`: clone templates and petitions before editing

## Main Files

- `src/gui/app.py`: main application flow
- `src/models/`: petition model classes
- `src/factories/`: factory method implementation
- `src/registry/`: petition and template registries
- `src/iterators/petition_iterator.py`: petition iterator
- `src/utils/pdf_export.py`: PDF export for registered petitions
- `docs/report.pdf`: project report
- `docs/uml/class_diagram.puml`: UML source

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## Notes

- `flet==0.28.2` is used in this project.
- Example saved data is included under `data/`.
