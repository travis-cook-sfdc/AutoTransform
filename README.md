# **Overview**

## Installing

> **⚠ WARNING:** AutoTransform requires Python 3.10

 - **Latest Release** `pip install AutoTransform`
 - **Bleeding Edge** `pip install git+git://github.com/nathro/AutoTransform.git`
   - Windows users may need to replace `git://` with `https://`
   - If you do not have git use: `pip install https://github.com/nathro/AutoTransform/archive/master.zip`
## **Summary**

AutoTransform is an opensource framework for large-scale code modification. It enables a schema-based system of defining codemods that can then be run using AutoTransform, with options for automatic scheduling as well as change management. AutoTransform leverages a component-based model that allows adopters to quickly and easily get whatever behavior they need through the creation of new, custom components. Additionally, custom components can readily be added to the component library of AutoTransform to be shared more widely with others using the framework.

## **Goal**

The goal of AutoTransform is to make codebase maintenance simple, easy, and automatic. By providing a clear structure for definition, all types of modifications can be automated. Some examples include:

* Library upgrades
* API changes
* Performance improvements
* Lint or style fixes
* Dead code
* One-off refactors
* Any other programmatically definable modification

## **Philosophies**
### **Component Based**

AutoTransform heavily uses a component based model for functionality. This allows easy customization through the creation of new plug-and-play components. Core logic is about funneling information between components, while the components themselves contain business logic. While AutoTransform provides an ever-growing library of components for ease of adoption, bespoke components will always be needed for some use cases.

### **Language Agnostic**

AutoTransform, though written in Python, is a language agnostic framework. Our component model allows AutoTransform to treat each component as a black-box that can leverage whatever tooling or language makes sense for the goal of the component. This is most heavily needed for the components which actually make code changes where leveraging tools for Abstract(or Concrete) Syntax Trees(AST/CST) is often done in the language being modified.

### **Minimal Developer Involvement**

Managing large scale changes can be extremely time consuming, AutoTransform puts automation first with the goal of automating as much of the process as possible. Developer time is incredibly valuable and should be saved for things that actually require it. If a computer can do it, a computer should do it.

## **Example - Typing**

As an example of how AutoTransform might be used, let’s go through the case of typing a legacy codebase. This is a notoriously difficult and time consuming process.

### **Static Inference**

A codemod can be written that statically infers types from the types around whatever needs types. Hooking this up to scheduled runs would mean that as people type your code, other types can later be inferred. Additionally, as the codemod types code, that can reveal further types that can be statically inferred. This would allow typing to slowly build up over time automatically as the codemod runs and developers introduce more types themselves, significantly speeding up the process of typing a legacy codebase.

### **Run Time Logging**

In addition to static typing, a codemod could instrument untyped functions or other code to log types at run time. These logs could then be fed into the codemod to add types to code that can’t be inferred but can be determined at run time. This codemod could additionally be written to only instrument a small part of the codebase at a given time, preventing excessive resource utilization.

### **The Whole Versus the Sum of the Parts**

Each codemod that can change code can benefit from all other codemods. As run time logging adds types, static inference can make better changes. Dead code removal can clean up untyped code. The layered passes, and building on top of the changes of each codemod, can produce significantly greater wins.

# **Core Functionality**

## **Schema**

The core of AutoTransform is the [schema](https://github.com/nathro/AutoTransform/blob/master/autotransform/schema/schema.py). A schema is a collection of components and configurations required to actually execute a change.

* **[Config](https://github.com/nathro/AutoTransform/blob/master/autotransform/schema/config.py)**
    * **Name** - A unique name to identify the change in PRs and scheduling
    * **Owner** - An owner to notify about actions taken by the schema
    * **Allowed Validation Level** - The level of validation errors allowed by the schema (none vs warning vs error)
* **[Input](https://github.com/nathro/AutoTransform/blob/master/autotransform/input/base.py)** - The input component returns a list of inputs that are potential targets of the change (i.e. code files)
* **[Filters](https://github.com/nathro/AutoTransform/blob/master/autotransform/filter/base.py)** - Filters take a set of inputs and apply criteria to the inputs that were not applied by the input, such as checking file extensions.
* **[Batcher](https://github.com/nathro/AutoTransform/blob/master/autotransform/batcher/base.py)** - A batcher takes a set of filtered inputs and breaks it into groups that can be executed independently. This component also generates metadata for this grouping used for things like the body of a pull request.
* **[Transformer](https://github.com/nathro/AutoTransform/blob/master/autotransform/transformer/base.py)** - The core of any change, takes a batch and actually makes changes to files based on the batch provided.
* **[Validators](https://github.com/nathro/AutoTransform/blob/master/autotransform/validator/base.py)** - Validators are run after transformation to check the health of a codebase after the transformation and ensure no issues are present. Things like typing, testing, etc...
* **[Commands](https://github.com/nathro/AutoTransform/blob/master/autotransform/command/base.py)** - Post run processes that need to be executed. Could involve updating databases, generating code, etc...
* **[Repo](https://github.com/nathro/AutoTransform/blob/master/autotransform/repo/base.py)** - An abstraction for the repository being modified. Allows functionality like commits or submitting changes for review.

## **Other Components**

### **[Config Fetcher](https://github.com/nathro/AutoTransform/blob/master/autotransform/config/fetcher.py)**

The config fetcher allows for configuration of AutoTransform as a whole. This includes things like specifying custom component imports as well as providing credentials, such as a github token. There are three config fetchers provided as part of AutoTransform that can be selected based on the AUTO_TRANSFORM_CONFIG environment variable:

* **[Default](https://github.com/nathro/AutoTransform/blob/master/autotransform/config/default.py)** - Pulls configuration from data/config.ini, a[ sample_config.ini](https://github.com/nathro/AutoTransform/blob/master/autotransform/data/sample_config.ini) file provides an example. This is the easiest choice for local use cases on a developers machine.
* **[Console](https://github.com/nathro/AutoTransform/blob/master/autotransform/config/console.py)** - Prompts the user to input configuration values when they are needed via console input. This is occasionally useful for CLI use cases.
* **[Environment Variable](https://github.com/nathro/AutoTransform/blob/master/autotransform/config/envvar.py)** - Pulls configuration from environment variables, using names that match the pattern: AUTO_TRANSFORM_&lt;SECTION>_&lt;SETTING> where section and setting represent the section and setting that would be used in a config.ini file, such as AUTO_TRANSFORM_CREDENTIALS_GITHUB_TOKEN. This is the preferred option for production use cases.

### **Worker**

**[Workers](https://github.com/nathro/AutoTransform/blob/master/autotransform/worker/base.py)** actually execute a schema. They allow integration with an organization’s CI infrastructure for distributed runs or local runs using the[ LocalWorker](https://github.com/nathro/AutoTransform/blob/master/autotransform/worker/local.py). Other options can be created to leverage things like queue based systems for batches with workers pulling batches off a common queue.

### **Remote**

**[Remote](https://github.com/nathro/AutoTransform/blob/master/autotransform/remote/base.py)** components are used to trigger a run on an organization’s CI infrastructure or other job queue system. This allows developers to run their transformations on remote machines rather than locally. Additionally, they are used by the scheduling logic of AutoTransform to handle scheduled runs.

### **Data Store**

**[DataStore](https://github.com/nathro/AutoTransform/blob/master/autotransform/common/datastore.py)** provides a unique dictionary that can map inputs to extra data that may be needed for some transformations. Examples could include when removing experiments, information on the current state of the experiment. This information should be populated by the Input component and can be accessed by any component in the chain.

## **Data Flow**

### **Schema**

**[A visual representation](https://lucid.app/lucidchart/eca43a3d-175f-416f-bb4f-4363d56f951b/edit?invitationId=inv_f44ed708-8c4a-4998-96f2-8b860aba8ebc)**

The input component of the schema will get a list of strings representing inputs, these are then passed through the filters where only those that pass the is_valid check make it through. This filtered set of inputs is then passed to a batcher which breaks the input into groups called batches. Batches will be executed sequentially as independent changes going through a multi-step process. First, the batch goes to a transformer which makes the actual changes to the codebase. Next, validators are invoked which check to ensure the codebase is still healthy. After this, commands are run which perform post-change processing, such as code generation. Finally, the repo object will check for changes, commit them if present and submit them (i.e. as a Pull Request). Once this is done, the repo object will return the repository to a clean state in preparation for the next batch.

### **Worker**

Workers are handled using a[ Coordinator](https://github.com/nathro/AutoTransform/blob/master/autotransform/worker/coordinator.py) class that spawns, runs, and manages workers. When started, a coordinator will run a schema's get_batches() function to get each batch for the schema. It will then spawn workers from these batches based on the WorkerType supplied to the coordinator. A script run will check the is_finished() state of the coordinator before eventually killing the jobs if a timeout is passed.

# **Upcoming Milestones**

## **Milestone 1 - Beta 0.2.0 - ETA 5/29/2022**

An early beta with all core functionality, including scheduling and change management available with an initial set of core components. This represents a mostly locked down version of the code, APIs, etc. Breaking changes may still happen after this release, but they will be weighted heavily against potential existing adoption. Before this release, breaking changes will be far more likely.

## **Milestone 2 - Release 1.0.0 - 7/29/2022**

This will include changes made as part of easing initial deployments. At this point AutoTransform will have been deployed to a production environment and the components will be considered production ready. Breaking changes after this release will be very unlikely and will coincide with new major versions of AutoTransform.

# **Security Best Practices**

The nature of AutoTransform creates the potential for significant security implications when deployed at an organization. Because of this, there is a set of best practices that are strongly encouraged to ensure security is maintained. These are less important for individual work that doesn’t get deployed to a production environment (i.e. updating personal projects).

## **AutoTransform User**

Create a separate user in whatever code review/management system (i.e. Github) you use that will be the actor for all changes/management and supply their credentials via secrets/environment variables. Try to minimize access to these credentials using things like Github repo secrets. The number of people capable of creating bot credentials should be as small a set as possible.

## **Reviewed Components**

All custom components used should be required to pull from a repo/package that goes through a code review process or is otherwise from a trusted open source provider (i.e. AutoTransform’s core components). Components will be able to access credentials and make changes to the codebase and thus must be reviewed.

## **Checked In Schemas**

All schemas that are run through scheduling must be checked into the codebase. This prevents people from stitching together components in unexpected ways that can present security or codebase health concerns. By ensuring all schemas are checked in you additionally ensure that schemas are all reviewed.

## **Thorough Review**

Schemas and components should be thoroughly reviewed and tested by people familiar with what they are trying to accomplish. Automated changes are readily accepted by developers and it is crucial that the schemas that produce these changes can be trusted. By putting in the upfront time to review the schemas, the review of the changes can be made much easier (or even unnecessary).

# **Schema Best Practices**

## **Batch Correctly**

The batching method chosen is very important. The more thorough reviewers need to be, the smaller the batches should be. If a schema can be guaranteed correct, one batch is fine. If review of each change is needed, the changes should be made in to small batches.

## **No Mixing Of Safety Categories**

Some schemas produce guaranteed safe changes, some schemas produce mostly safe, but potentially incorrect changes. Separate schemas should be created for each of these types of changes. Mixing these types of changes in one schema will lead to complacency in review that can let errors slip through.

## **Test Test Test**

Every component and schema should be thoroughly tested for each different possible case. AutoTransform is a scaling system that requires an upfront investment in exchange for automating all future work. By thoroughly testing your components and schemas you support all future changes.

## **Mind Developer Time**

Just because something can be automated to be made better, doesn’t mean it should be. Developer time is important and wasting it by submitting numerous of changes for review that don’t really do much to improve things is a bad practice that can eliminate the benefits of AutoTransform. Try to minimize review required for changes where possible, and if review is required, ensure that it is worth the time of the reviewer to get the changes in.

## **Create A Council**

As developers in your organization learn about AutoTransform, they will inevitably want to use it. Growth of usage will likely be organic and rapid, including many people without a lot of experience using these types of tools. Be prepared to have a council or other group these developers can go to for support.