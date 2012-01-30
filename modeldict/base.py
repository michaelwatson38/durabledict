class PersistedDict(object):
    """
    Dictionary that calls out to its persistant data store when items are
    created or deleted.  Caches data in process for a set time period before
    refreshing from the persistant data store.
    """

    def __init__(self):
        self.__dict = dict()
        self.last_synced = 0
        self.__sync_with_persistent_storage()

    @property
    def cache_expired(self):
        persistance_last_updated = self.last_updated()

        if not self.last_synced or persistance_last_updated > self.last_synced:
            return persistance_last_updated

    def __setitem__(self, key, val):
        self.persist(key, val)
        self.__sync_with_persistent_storage()

    def __delitem__(self, key):
        self.depersist(key)
        self.__sync_with_persistent_storage()

    def __getattr__(self, name):
        self.__sync_with_persistent_storage()
        return getattr(self.__dict, name)

    def __getitem__(self, key):
        self.__sync_with_persistent_storage()
        return self.__dict.__getitem__(key)

    def __len__(self):
        self.__sync_with_persistent_storage()
        return self.__dict.__len__()

    def __cmp__(self, other):
        self.__sync_with_persistent_storage()
        return self.__dict.__cmp__(other)

    def __repr__(self):
        return self.__dict.__repr__()

    def __sync_with_persistent_storage(self, force=False):
        cache_expired_at = self.cache_expired

        if cache_expired_at:
            self.__dict = self.persistants()
            self.last_synced = cache_expired_at

    def persist(self, key, val):
        raise NotImplementedError

    def depersist(self, key):
        raise NotImplementedError

    def persistants(self):
        raise NotImplementedError

    def last_updated(self):
        raise NotImplementedError
