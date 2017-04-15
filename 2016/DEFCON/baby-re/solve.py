import angr

main = 0x4025E7
find = 0x40294b
avoid = 0x402941

p = angr.Project('./baby-re', load_options={'auto_load_libs':False})
init = p.factory.blank_state(addr=main)
pg = p.factory.path_group(init, threads=8)
ex = pg.explore(find=find, avoid=avoid)

final = ex.found[0].state

print("Flag: {0}".format(final.posix.dumps(1)))