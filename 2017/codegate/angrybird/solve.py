import angr

main = 0x4007DA
find = 0x404FC1
avoid = [0x404f97]

p = angr.Project('./angrybird_patch', load_options={'auto_load_libs':False})
init = p.factory.blank_state(addr=main)
pg = p.factory.path_group(init, threads=8)
ex = pg.explore(find=find, avoid=avoid)

final = ex.found[0].state

print("Flag: {0}".format(final.posix.dumps(1)))
