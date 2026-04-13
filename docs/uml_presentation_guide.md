# How to Present the UML Diagram

This guide is only about how to explain the UML diagram during your presentation.

The main rule is:

**Present the UML as a map of responsibilities, not as a picture full of boxes.**

Do not try to explain every arrow, every attribute, or every small notation detail.
Instead, use the diagram to answer these questions:

- what are the main parts of the system?
- how are they related?
- where are the design patterns?

## The Best Way to Present It

When you show the UML, explain it in this order:

1. `Petition` hierarchy
2. `Factory` hierarchy
3. `Registry` classes
4. `Iterator`
5. `PetitionApp`

This is the best order because it matches how the system works:

- first define the objects
- then create them
- then store them
- then traverse them
- then connect everything in the GUI

---

## 1. Start from the Center

Begin with the domain model:

- `Petition`
- `AcademicPetition`
- `AdministrativePetition`

What to say:

> At the center of the system is the `Petition` base class.  
> `AcademicPetition` and `AdministrativePetition` inherit from it and define different petition types with different defaults, such as petition type and receiver.

Why start here:

- this is the heart of the application
- the audience first needs to understand what the system is built around

---

## 2. Then Explain Creation

Move to the factory side:

- `PetitionFactory`
- `AcademicPetitionFactory`
- `AdministrativePetitionFactory`

What to say:

> This part of the UML shows the Factory Method pattern.  
> `PetitionFactory` is the abstract base factory, and the concrete factories create different petition subtypes.

Then add:

> This is useful because the GUI does not need to construct academic and administrative petitions directly.  
> The factories handle creation and can also set creation-time rules like default receiver or attachment requirement.

You can mention the concrete example:

> For example, the internship approval template is created with `attachment_required=True`.

---

## 3. Then Explain Prototype

Now point back to `Petition` and mention:

- `clone()`

What to say:

> The Prototype pattern appears in the `clone()` method of `Petition`.  
> When a user selects a template, the system does not edit the original template directly. It clones it and edits the copy.

Why this matters:

- the original template remains unchanged
- the same template can be reused many times

---

## 4. Then Explain Storage

Move to:

- `PetitionRegistry`
- `TemplateRegistry`

What to say:

> These classes handle storage and persistence.  
> `PetitionRegistry` is the main registry for saved petitions, while `TemplateRegistry` stores reusable user-defined templates.

Then explain the Singleton part:

> `PetitionRegistry` is the Singleton in the project.  
> It has one shared instance that the whole application uses when saving and retrieving petitions.

Important clarification:

- `PetitionRegistry` is Singleton
- `TemplateRegistry` is a normal registry class, not the Singleton required by the homework

That distinction is worth saying if your instructor cares about patterns precisely.

---

## 5. Then Explain Traversal

Move to:

- `PetitionIterator`

What to say:

> This class implements the Iterator pattern.  
> It traverses saved petitions and can filter them by petition type or status.

Then add:

> This keeps the filtering and traversal logic out of the GUI and makes the petition list easier to manage.

---

## 6. Finally Explain the GUI Coordinator

Point to:

- `PetitionApp`

What to say:

> `PetitionApp` is the class that coordinates the user flow.  
> It connects the GUI to the factories, registries, iterator, and petition objects.

Then say:

> In other words, the GUI does not contain all the logic itself. It delegates to the appropriate classes.

This is a good final step because it ties the whole UML together.

---

## The Best Simple Words to Use

When explaining the UML, use simple verbs like:

- `inherits from`
- `creates`
- `stores`
- `uses`
- `traverses`
- `clones`

Examples:

- `AcademicPetition` inherits from `Petition`
- `AcademicPetitionFactory` creates `AcademicPetition`
- `PetitionRegistry` stores many `Petition` objects
- `PetitionIterator` traverses petitions
- `PetitionApp` uses the factories and registries

This is much better than spending time on detailed UML terminology.

---

## A Good Full UML Explanation Script

You can present the diagram almost exactly like this:

> This UML diagram shows the main structure of the system.  
> At the center is the `Petition` base class, and `AcademicPetition` and `AdministrativePetition` extend it.  
> On the creation side, `PetitionFactory` is the abstract factory and the two concrete factories create different petition types.  
> The Prototype pattern appears in the `clone()` method of `Petition`, which is used when templates are copied for editing.  
> For storage, `PetitionRegistry` manages saved petitions and is implemented as a Singleton, while `TemplateRegistry` stores reusable user-defined templates separately.  
> `PetitionIterator` is responsible for traversing and filtering petitions by type and status.  
> Finally, `PetitionApp` connects the GUI to all these components and coordinates the overall user flow.

That is already a strong UML explanation for a short presentation.

---

## How to Visually Point at the Diagram

If you are presenting live, point at the diagram in regions:

- first the model classes
- then the factory classes
- then the registry classes
- then the iterator
- then the GUI

Do not jump randomly around the diagram.

If possible:

- zoom in slightly
- point to groups of classes
- avoid showing the whole diagram and talking too fast

---

## What Not to Do

Avoid these mistakes:

- do not read all class attributes one by one
- do not explain every line or arrow type in UML notation
- do not focus on Python syntax like `list[str]`, `bool`, or `None`
- do not spend too long on one small part of the diagram
- do not make the UML explanation longer than necessary

The UML is there to support architecture understanding, not to become the entire talk.

---

## Best Short Summary Sentence

If you need one clean sentence:

> The UML diagram shows how the petition models, factories, registries, iterator, and GUI cooperate to implement the required design patterns.

---

## Best Final Advice

When presenting the UML, always connect each part to one purpose:

- model classes -> represent petition data
- factories -> create petition objects
- registries -> store and persist them
- iterator -> traverse and filter them
- app -> coordinate the flow

If you do that, your UML explanation will sound clear and organized instead of mechanical.

