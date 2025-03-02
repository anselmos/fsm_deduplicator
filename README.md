# FSM Deduplicator

- Connects to Postgres DB files table
- Searches for any duplicate files and directories
- Enables end user choose where such duplicates needs to be moved with web page list.
- Separate process: 
  - checks for any updated files with "to_be_deleted" and "new_path_after_deleted"
  - connects with GRPC to FSM_cleanup service that makes those file movement and sets files as "new_path_moved" = True