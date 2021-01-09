# Actions

Action contains business logic and isolate dependencies between endpoints and DB operations.

## Class naming

Class names should reflect the domain knowledge.

# Method naming

For methods that involve querying from other services (e.g. DB), we should use reserved verbs as prefix to indicate 
their query logic.

* `create_` - create resource
* `get_` - find existing resource, exception should be raised if nothing is yielded
* `find_` - find resource, it is okay to return `None` if resource does not exist
* `update_` - update an existing resource
* `delete_` - delete an existing resource
