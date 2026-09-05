# Configuration Registries

Exactly nine top-level *.yaml files are run-level configuration registries:

1. evidence_policy
2. deny_list
3. narrative_library
4. format_profiles
5. category_profiles
6. creative_taxonomy
7. experiment_variables
8. diversity_targets
9. tool_capability

A tenth top-level registry is not permitted.

During Phase 3B these files are placeholders with:
status: PLACEHOLDER_NOT_AUTHORISED

A run must refuse to start while a required registry remains unauthorised.

config/styles/ contains registry entities and is not a tenth run-level registry.
