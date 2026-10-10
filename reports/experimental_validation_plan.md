# Experimental validation plan

## Purpose

Validate any candidate factor-response relationship with authorized equipment, approved wafers, and an agreed metrology plan. The synthetic DOE module in this repository does not provide a recipe or validation evidence.

## Before running an experiment

1. Define the product, film stack, etch endpoint, equipment/chamber identity, approved safety controls, and response specifications.
2. Confirm chamber conditioning, wafer sampling, measurement locations, measurement-system capability, randomization, blocking, and replication with the process owner.
3. Freeze the factor ranges only after an engineering safety and hardware review. Do not use the illustrative ranges in this repository as operating instructions.

## Design and execution

1. Start with a screening DOE that includes center points and independent replicates.
2. Randomize run order within operational constraints and record unavoidable blocks, maintenance, lot changes, and metrology timestamps.
3. Capture raw metrology, tool logs, recipe revision, and exceptions. Preserve the immutable raw export.
4. Predefine response metrics, exclusion rules, acceptance criteria, and follow-up confirmation runs.

## Analysis and release discipline

1. Check residuals, influential observations, measurement repeatability, and lack-of-fit before interpreting factor effects.
2. Confirm any predicted optimum with independent runs. Report uncertainty intervals, not only point estimates.
3. Establish control limits only after demonstrating an appropriate stable baseline. Do not calculate Cp/Cpk without approved specifications and a suitable stability assessment.
4. Require cross-functional review before any recipe or control-plan change.
