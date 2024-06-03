month = "2024-05"  # note: to find attendance data folder for current month

# map centre here
# note: update if there are new centers
jkt_1 = ["PP", "SDC", "KG"]
jkt_2 = ["GC", "LW", "BSD", "TBS", "CP"]
jkt_3 = ["KK", "CBB", "SMB"]
bdg = ["DG"]
sby = ["PKW"]
centers = jkt_1 + jkt_2 + jkt_3 + bdg + sby

map_areas = {
    "JKT 1": jkt_1,
    "JKT 2": jkt_2,
    "JKT 3": jkt_3,
    "BDG": bdg,
    "SBY": sby,
    "Other": ["HO", "Street Talk"],
    "Corporate": ["Corporate"],
    "Online Center": ["Online Center"],
}
