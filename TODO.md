# TODO

## Tasks

-   [x] convert prints to logging
-   [x] conversation api (reset messages/increment conversation id/ etc)
-   [x] preserve conversations as sqllite
-   [ ] load/save state from sqllite
-   [ ] fix typing hell with pandera schemas/etc
    -   [ ] convert pandera to object-based api
-   [ ] use same model for multiple experts, (maintain separate message histories)
-   [ ] feedback api, for refining results via deterministic functions
-   [ ] improve timesheet generation speed
-   [ ] add pre-commit + format everything
-   [ ] token/context limit monitoring
-   [x] suppress sqllite logs
-   [ ] ability to prune/preserve history for repeated dataframe calls
-   [ ] split out llm/sqlite class from polarsllm

## Experiment With

-   [x] tools - Completed: added basic api for defining tools (parsing docstring is a bit cheesy tho)
-   [ ] json as llm generated format (llms are potentially better are structuring json?)
