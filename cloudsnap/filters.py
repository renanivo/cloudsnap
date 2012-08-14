def filter_backups_by_tags(backup_list, tags_equal={}, tags_not_equal={}):
    def callback(item):
        for k, v in tags_equal.items():
            return k in item.tags and item.tags[k] == v

        for k, v in tags_not_equal.items():
            return k not in item.tags or item.tags[k] != v

    return filter(callback, backup_list)
