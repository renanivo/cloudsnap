def filter_backups_by_tags(backup_list, tags_equal=None, tags_not_equal=None):
    if tags_equal is None:
        tags_equal = {}

    if tags_not_equal is None:
        tags_not_equal = {}

    def equals_filter(item):
        for k, v in tags_equal.items():
            return k in item.tags and item.tags[k] == v
        return True

    def not_equals_filter(item):
        for k, v in tags_not_equal.items():
            return k not in item.tags or item.tags[k] != v
        return True

    backup_list = filter(equals_filter, backup_list)
    backup_list = filter(not_equals_filter, backup_list)

    return backup_list
