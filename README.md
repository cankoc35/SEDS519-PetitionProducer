# SEDS519 Homework 1

Petition management system implemented in Python using design patterns.

## Project Goal

This project is a petition management system for the SEDS519 homework.

The main goal is not advanced petition writing. The important part is to show the required design patterns clearly and show how they interact with each other in one application.

The user will:

- choose a petition type
- enter petition information such as title and body
- optionally upload attachment files
- save the petition as draft or register it
- display stored petitions
- clone an existing petition as a template for a new one

## Main Notes From Lecture

- A web or desktop application is acceptable.
- We will use `Flet` for the GUI.
- File upload should be supported for attachments.
- A database is not mandatory.
- Petition storage can be folder-based or in-memory at first.
- Petition content quality is less important than correct design pattern usage.
- UML is important.
- The interactions between the patterns are important.

## Design Pattern Mapping

- `Factory Method`
  Used to create different petition types such as academic and administrative petitions.

- `Singleton`
  Used for `PetitionRegistry`, which will be the single shared petition storage/management object.

- `Iterator`
  Used to traverse petitions in a type-agnostic way and filter them by type or status.

- `Prototype`
  Used to clone an existing petition and reuse it as a template.

## Simple Roadmap

### Step 1: Complete the Core Petition Model

- finalize the shared fields in `Petition`
- make petition types meaningfully different
- add ownership information such as `created_by`

### Step 2: Complete Petition Creation Logic

- finish concrete petition factories
- make factories assign proper defaults
- support different rules for different petition types

### Step 3: Complete Registry Logic

- keep petitions in one shared singleton registry
- support draft and registered petitions
- add retrieval methods for stored petitions

### Step 4: Complete Traversal and Validation

- improve iterator to filter by type and status
- validate empty body
- validate missing required attachments

### Step 5: Complete Prototype Flow

- allow cloning an existing petition
- reuse cloned petitions as templates for new petitions

### Step 6: Build the Flet GUI

- create petition form screen
- add attachment upload
- display petitions
- filter petitions
- register petitions
- clone petitions from the interface

### Step 7: Prepare UML and Final Cleanup

- draw the UML class diagram
- show class interactions clearly
- review that each required pattern is visible in the code

## TODO

- [ ] Finalize the `Petition` model fields.
- [ ] Add meaningful differences between petition types.
- [ ] Complete the petition factories.
- [ ] Expand the singleton registry logic.
- [ ] Improve iterator filtering by type and status.
- [ ] Complete validation rules.
- [ ] Implement cloning/template flow.
- [ ] Build the GUI with `Flet`.
- [ ] Add attachment upload support.
- [ ] Prepare UML diagrams for submission.
