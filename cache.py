class OPTCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []
        self.pnum_assigner = 0

class OptimalCache:
    def __init__(self, capacity): #, reference_string):
        self.capacity = capacity
        #self.reference_string = reference_string
        self.cache = []
    def register_get(self, vnum):
        pass

    #def put(self, new_vnum, page_table, tlb_evict):
    def put(self, new_vnum):
        #for i in range(len(self.reference_string)):
            #if self.reference_string[i] not in self.cache:
        if len(self.cache) == self.capacity:
            # Find the page that won't be used for the longest period of time in the future
            # go through the pages in physical memory, evict the one
            # the longest ways away from now
            future_accesses = {}
            for tmp_vnum in self.cache:
                future_accesses[tmp_vnum] = float('inf')
                for j in range(i, len(self.reference_string)):
                    if self.reference_string[j] == tmp_vnum:
                        future_accesses[tmp_vnum] = j
                        break
            # PROBLEM: we need the index of the current vaddr, 
            #          and the next future use of it
            
            # evict the page with the highest in this list
            evict_vnum = max(future_accesses, key=future_accesses.get)
            self.cache.remove(evict_vnum)

        self.cache.append(new_vnum)
        #self.page_faults += 1


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []
        self.pnum_assigner = 0

    def register_get(self, vnum):
        try: 
            self.cache.remove(vnum)
            self.cache.append(vnum)
        except ValueError:
            pass

    def put(self, new_vnum, page_table, tlb_evict):
        if len(self.cache) >= self.capacity:
            evict_vnum = self.cache.pop(0)
            evict_pnum = page_table[evict_vnum]
            page_table[evict_vnum] = None
            tlb_evict(evict_vnum)
            new_pnum = evict_pnum
        else:
            new_pnum = self.pnum_assigner
            self.pnum_assigner += 1
        self.cache.append(new_vnum)
        page_table[new_vnum] = new_pnum


class FIFOCache:
    def __init__(self, capacity):
        self.cache = []
        self.capacity = capacity
        self.pnum_assigner = 0

    def register_get(self, vnum):
        pass

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

# Not Recently Used
# -> evicts the most recently used page
# XXX maybe do something more creative than this
class BADCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []
        self.pnum_assigner = 0

    def register_get(self, vnum):
        try: 
            self.cache.remove(vnum)
            self.cache.append(vnum)
        except ValueError:
            pass

    def put(self, new_vnum, page_table, tlb_evict):
        if len(self.cache) >= self.capacity:
            evict_vnum = self.cache.pop()
            evict_pnum = page_table[evict_vnum]
            page_table[evict_vnum] = None
            tlb_evict(evict_vnum)
            new_pnum = evict_pnum
        else:
            new_pnum = self.pnum_assigner
            self.pnum_assigner += 1
        self.cache.append(new_vnum)
        page_table[new_vnum] = new_pnum
