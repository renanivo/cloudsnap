def filter_backups_by_tags(backup_list, filter_by):
    def callback(item):
        for k, v in filter_by.items():
            return k in item.tags and item.tags[k] == v

    return filter(callback, backup_list)
