# SEDS519 Petition Producer

Petition management system for `SEDS519 HW1`, implemented in Python with the required design patterns.

## Project Summary

This project is a desktop petition application built with `Flet`.

The system provides `6` built-in petition templates:

- `3` academic templates
- `3` administrative templates

The user can:

1. choose a built-in template
2. create a blank academic or administrative petition from scratch
3. edit petition fields such as `title`, `body`, `petitioner`, `receiver`, and `created_by`
4. save the current editor state as a reusable custom template
5. upload one or more attachments
6. save the petition as `draft`
7. register the petition
8. view saved petitions and filter them by type or status

Saved petitions are persisted as JSON files in `data/petitions/`.
User-defined templates are persisted separately in `data/templates/`.

## Implemented Design Patterns

### Factory Method

Used to create different petition types through dedicated factories:

- [petition_factory.py](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/src/factories/petition_factory.py)
- [academic_factory.py](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/src/factories/academic_factory.py)
- [administrative_factory.py](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/src/factories/administrative_factory.py)

### Singleton

Used for the shared petition registry:

- [petition_registry.py](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/src/registry/petition_registry.py)

### Iterator

Used to traverse petitions and apply type/status filtering:

- [petition_iterator.py](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/src/iterators/petition_iterator.py)

### Prototype

Used to clone an existing petition/template before editing:

- [petition.py](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/src/models/petition.py)

## Current Features

- built-in template catalog with `6` templates
- user-defined template creation from scratch
- reusable custom templates saved separately from petitions
- academic and administrative petition subclasses
- JSON-based petition persistence
- draft and registered petition states
- GUI for:
  - selecting templates
  - creating petitions from scratch
  - editing petitions
  - saving custom templates
  - uploading attachments
  - saving/registering petitions
  - viewing saved petitions
  - filtering saved petitions by type and status
- basic validation for:
  - empty body
  - missing attachments when `attachment_required=True`
- UML sources for both:
  - a detailed class diagram
  - a simplified class diagram

## Project Structure

```text
SEDS519-PetitionProducer/
├── data/
│   ├── petitions/
│   └── templates/
├── docs/
│   ├── SEDS519_HW1.pdf
│   └── uml/
│       ├── class_diagram.puml
│       └── class_diagram_simple.puml
├── src/
│   ├── main.py
│   ├── models/
│   │   ├── petition.py
│   │   ├── academic_petition.py
│   │   └── administrative_petition.py
│   ├── factories/
│   │   ├── petition_factory.py
│   │   ├── academic_factory.py
│   │   └── administrative_factory.py
│   ├── registry/
│   │   └── petition_registry.py
│   ├── iterators/
│   │   └── petition_iterator.py
│   ├── templates/
│   │   └── petition_templates.py
│   ├── gui/
│   │   ├── app.py
│   │   └── forms.py
│   └── utils/
│       └── validators.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Important Files

- [main.py](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/src/main.py)
  Entry point that launches the GUI.

- [petition.py](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/src/models/petition.py)
  Base petition model, `clone()` support, and JSON serialization.

- [petition_templates.py](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/src/templates/petition_templates.py)
  Built-in academic and administrative petition templates.

- [app.py](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/src/gui/app.py)
  Main Flet application and petition editor flow.

- [forms.py](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/src/gui/forms.py)
  Reusable GUI sections for template and petition display.

- [validators.py](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/src/utils/validators.py)
  Petition validation rules.

- [class_diagram.puml](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/docs/uml/class_diagram.puml)
  Detailed UML class diagram source.

- [class_diagram_simple.puml](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/docs/uml/class_diagram_simple.puml)
  Simpler UML class diagram source.

## Built-in Templates

### Academic

- Make-Up Exam Request
- Course Exemption Request
- Internship Approval Request

### Administrative

- Student ID Renewal Request
- Official Document Request
- Dormitory Issue Request

## Persistence

Petitions are stored in:

```text
data/petitions/
```

Each saved petition is written as a separate JSON file.

User-defined templates are stored in:

```text
data/templates/
```

## Local Setup

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

Run the app:

```bash
python src/main.py
```

Leave the virtual environment:

```bash
deactivate
```

## Dependency Note

`flet` is pinned to `0.28.2` in [requirements.txt](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/requirements.txt).

Reason:

- `0.28.3` had a macOS `FilePicker` issue during this project
- the attachment upload flow worked correctly with `0.28.2` in the current setup

## UML

UML sources are in:

- [class_diagram.puml](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/docs/uml/class_diagram.puml)
- [class_diagram_simple.puml](/Users/cankoc/Desktop/masters/SEDS519-DesignPatterns/SEDS519-PetitionProducer/docs/uml/class_diagram_simple.puml)

If `plantuml` is installed on your machine, render them with:

```bash
plantuml docs/uml/class_diagram.puml
plantuml docs/uml/class_diagram_simple.puml
```

## Remaining Work

- strengthen the validation story by marking some templates as attachment-required
- optionally store copied attachment files in a dedicated app folder instead of only storing selected paths
