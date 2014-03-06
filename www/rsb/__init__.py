from johnny.cache import enable

# We need to enable Johnny Cache manually so it works in management commands
# and Celery. See https://pythonhosted.org/johnny-cache/queryset_cache.html#using-with-scripts-management-commands-asynchronous-workers-and-the-shell
enable()
