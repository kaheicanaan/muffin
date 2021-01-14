# Actions

Action contains business logic and isolate dependencies between endpoints and DB operations.

## Folder naming

Actions are grouped according to "who" will use those APIs. For example, developers will use actions without 
authentication information. Hence, these classes are grouped in `/internal` folder. Likewise, authentication is required 
for users before doing any action. Therefore, these classes are grouped in `/user` folder. You may expect that 
the function `get_authenticated_user` is nearly a must as a `Depends()` for all methods in actions under `/user` folder.

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
