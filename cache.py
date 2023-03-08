#class LRUCache:
#    def __init__(self, capacity):
#        self.cache = []
#        self.capacity = capacity

# PROBLEM: LRU cache changes on `get`

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []
        self.hash_map = {}

    #def get(self, key):
    #    if key in self.hash_map:
    #        val = self.hash_map[key]
    #        self.cache.remove(key)
    #        self.cache.append(key)
    #        return val
    #    return -1

    def put(self, new_vnum, page_table, tlb_evict):
    #def put(self, key, value):
        if key in self.hash_map:
            self.cache.remove(key)
        elif len(self.cache) >= self.capacity:
            lru_key = self.cache.pop(0)
            del self.hash_map[lru_key]
        self.cache.append(key)
        self.hash_map[key] = value


class FIFOCache:
    def __init__(self, capacity):
        self.cache = []
        self.capacity = capacity
        self.pnum_assigner = 0

    def put(self, new_vnum, page_table, tlb_evict):
        new_pnum = None
        
        if len(self.cache) >= self.capacity:
            evict_vnum = self.cache.pop()
            evict_pnum = page_table[evict_vnum]
            page_table[evict_vnum] = None
            tlb_evict(evict_vnum)
            new_pnum = evict_pnum
        else:
            new_pnum = self.pnum_assigner
            self.pnum_assigner += 1

        self.cache.insert(0, new_vnum)
        page_table[new_vnum] = new_pnum
        return new_pnum


