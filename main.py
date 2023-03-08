from util import *
import mem
import cache
import sys

def print_status(vaddr, paddr):
    backing_store.seek(256*vaddr.num)
    page = backing_store.read(256)

    chunk = "".join(["%02X" % x for x in page])
    refb = page[vaddr.offset]
    if refb > 256/2:
        refb = -1 * (256-refb)

    print(f"{vaddr.val}, {refb}, {paddr}, {chunk}")

def simulate(INPUT, verbose=False, debug=False):
    global backing_store 
    backing_store = open("BACKING_STORE.bin", 'rb')

    mem.PHYSICAL_FRAME_COUNT = INPUT.frames
    vaddrs = INPUT.vaddrs
    algorithm_name = INPUT.algorithm
    if algorithm_name == "FIFO":
        algorithm = cache.FIFOCache(INPUT.frames)
    elif algorithm_name == "LRU":
        algorithm = cache.LRUCache(INPUT.frames)
    elif algorithm_name == "OPT":
        algorithm = cache.OPTCache(INPUT.frames)
    elif algorithm_name == "BAD":
        algorithm = cache.BADCache(INPUT.frames)


    OUTPUT = Output(len(vaddrs))

    vaddrs = iter(vaddrs)
    vaddr = next(vaddrs, None)
    while vaddr is not None:
        if debug:
            print(f"TLB: {mem.tlb}", end="\t")

        # case: hit
        paddr = mem.check_tlb(vaddr, algorithm)
        if paddr is not None:
            OUTPUT.hits += 1
            if debug:
                print(f"[miss <- {vaddr.num}]")
            if verbose:
                print_status(vaddr, paddr)
            vaddr = next(vaddrs, None)
            continue

        # case: miss -> cache vaddr
        paddr = mem.check_page_table(vaddr, algorithm)
        if paddr is not None:
            OUTPUT.misses += 1
            if debug:
                print(f"[miss <- {vaddr.num}]")
            if verbose:
                print_status(vaddr, paddr)
            mem.cache(vaddr)
            vaddr = next(vaddrs, None)
            continue

        # case: fault -> assign paddr
        OUTPUT.faults += 1
        if debug:
            print(f"[fault <- {vaddr.num}]")

        paddr = mem.assign_paddr(vaddr, algorithm)
        
        #if verbose:
        #    print_status(vaddr, paddr)

    if verbose or debug:
        print(OUTPUT)
    if debug:
        print(f"(FRAMES = {INPUT.frames})")
        print(f"(ALGORITHM = {algorithm_name})")
    return OUTPUT

# sys.argv
x = Input(sys.argv)
simulate(x, debug=True)


