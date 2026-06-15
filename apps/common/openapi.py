"""drf-spectacular hooks."""


def exclude_api_root(endpoints):
    """Drop DRF DefaultRouter ``APIRootView`` entries from the schema.

    They are navigational HTML helpers, not real API operations, and otherwise
    show up under a stray path-derived tag (e.g. "v1").
    """
    result = []
    for path, path_regex, method, callback in endpoints:
        cls = getattr(callback, "cls", None)
        if cls is not None and cls.__name__ == "APIRootView":
            continue
        result.append((path, path_regex, method, callback))
    return result
