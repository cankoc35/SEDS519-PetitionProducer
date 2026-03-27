# SEDS519 Homework 1

Petition management system implemented in Python using design patterns.

## Project Goal

This project is a template-based petition builder for the SEDS519 homework.

The app will provide `6` built-in petition templates:

- `3` academic templates
- `3` administrative templates

The user flow is planned as:

1. choose one of the built-in templates
2. optionally upload attachment files
3. enter their own name
4. edit fields such as `title`, `body`, `petitioner`, and `receiver`
5. save the petition as draft or register it
6. display previously saved petitions

The main focus of the homework is correct use of design patterns and the interaction between them, not advanced petition text generation.

## Current Status

The core backend logic is already implemented and working in console form:

- petition models for academic and administrative petitions
- factory layer for creating petition objects
- singleton registry
- iterator with type and status filtering
- prototype cloning with `clone()`
- basic validation
- JSON persistence in `data/petitions/`

Current limitation:

- the Flet GUI is still not implemented
- the built-in 6-template catalog is not implemented yet

## Design Pattern Mapping

- `Factory Method`
  Used to create different petition types such as academic and administrative petitions.

- `Singleton`
  Used for `PetitionRegistry`, which acts as the single shared storage and management object.

- `Iterator`
  Used to traverse petitions in a type-agnostic way and filter by petition type or status.

- `Prototype`
  Used to clone an existing petition so it can be reused as a template.

## Current Project Structure

```text
SEDS519-PetitionProducer/
├── data/
│   └── petitions/
├── docs/
│   ├── SEDS519_HW1.pdf
│   └── uml/
├── src/
│   ├── main.py
│   ├── models/
│   ├── factories/
│   ├── registry/
│   ├── iterators/
│   ├── gui/
│   └── utils/
├── .gitignore
├── LICENSE
└── README.md
```

## Important Files

- `src/models/petition.py`
  Base petition model, clone support, and JSON serialization.

- `src/models/academic_petition.py`
  Academic petition subtype.

- `src/models/administrative_petition.py`
  Administrative petition subtype.

- `src/factories/petition_factory.py`
  Abstract factory interface.

- `src/factories/academic_factory.py`
  Factory for academic petitions.

- `src/factories/administrative_factory.py`
  Factory for administrative petitions.

- `src/registry/petition_registry.py`
  Singleton registry plus JSON save/load behavior.

- `src/iterators/petition_iterator.py`
  Iterator for all petitions or filtered petition traversal.

- `src/utils/validators.py`
  Basic petition validation rules.

- `src/main.py`
  Current console demo for the implemented backend features.

## Persistence

Petitions are currently stored as JSON files in:

```text
data/petitions/
```

This acts as a simple folder-based database, which matches the lecture guidance that a full database is not required.

## Run Locally

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Note:

- `flet` is pinned to `0.28.2` because `0.28.3` has a macOS `FilePicker` issue that prevents the native file selection dialog from opening reliably in this project setup.

Check that the virtual environment Python is active:

```bash
which python
python --version
```

Run the current console demo:

```bash
python src/main.py
```

Leave the virtual environment when you are done:

```bash
deactivate
```

## Roadmap

### 1. Build the Template Catalog

- define `3` academic templates
- define `3` administrative templates
- make user-created petitions start from these built-in templates

### 2. Strengthen Prototype Usage

- clone a selected built-in template
- let the user edit the cloned petition instead of editing the original template

### 3. Build the Flet GUI

- show the available templates
- let the user choose one
- let the user edit petition fields
- let the user upload attachments
- let the user save draft or register

### 4. Connect GUI to Persistence

- load saved petitions into the interface
- display saved petitions from JSON storage
- allow filtering by type and status

### 5. Prepare UML

- draw the UML class diagram
- clearly show interactions between the patterns

## TODO

- [ ] Add the built-in `6` petition templates.
- [ ] Decide the exact titles and default bodies of those templates.
- [ ] Build the Flet GUI.
- [ ] Add file upload support for attachments in the GUI.
- [ ] Connect template selection to Prototype cloning.
- [ ] Display saved petitions in the GUI.
- [ ] Add filtering controls in the GUI.
- [ ] Prepare UML diagrams for submission.
