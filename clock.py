#!/bin/python3
import arrow
import datetime
import math
import os
import json

def tdfmt(td):
    return f"{math.floor(td.seconds/3600)}h {math.floor(td.seconds/60)%60}m"

fn="clock.json"

cdict={}
cdict["cin"]=""
cdict["clunchout"]=""
cdict["clunchin"]=""

# if file !exists or !modified today
if (not os.path.isfile(fn) or os.path.getmtime(fn) < arrow.get(arrow.get().format("MM-DD-YY"), "MM-DD-YY").timestamp()):
    # create new dict
    pass
# else load file
else:
    with open(fn) as f:
        cdict = json.load(f)
        for key in cdict.keys():
            try:
                a = arrow.get(cdict[key])
                cdict[key] = a 
            except (TypeError, arrow.parser.ParserError):
                pass


# get user input
if (cdict["cin"] == ""):
    cdict["cin"] = arrow.get(arrow.now().format("Z MM-DD-YY ") + input("in: "), "Z MM-DD-YY HmmA")
if (cdict["clunchout"] == ""):
    cdict["clunchout"] = input("lunch out (enter for none): ")
if (cdict["clunchin"] == ""):
    cdict["clunchin"] = input("lunch in (enter for none): ")

# process user input
if (type(cdict["clunchout"]) != arrow.Arrow and cdict["clunchout"] != ""):
    cdict["clunchout"] = arrow.get(arrow.now().format("Z MM-DD-YY ") + cdict["clunchout"], "Z MM-DD-YY HmmA")
    cdict["clunchin"] = arrow.get(arrow.now().format("Z MM-DD-YY ") + cdict["clunchin"], "Z MM-DD-YY HmmA")
if (type(cdict["clunchout"]) != arrow.Arrow and "clunchout" not in cdict.keys() or cdict["clunchout"] != ""):
    cdict["cout"] = cdict["clunchin"]+(datetime.timedelta(seconds=8*60*60)-(cdict["clunchout"]-cdict["cin"]))
else:
    cdict["cout"] = cdict["cin"]+(datetime.timedelta(seconds=8*60*60))

if (cdict["clunchout"]!=""):
    cluncht = cdict["clunchin"]-cdict["clunchout"]
    p1 = cdict["clunchout"]-cdict["cin"]
    p2 = cdict["cout"]-cdict["clunchin"]

# display
#    print(f"clunchin    {cdict['clunchin'].format('h:mm A')}")
#    print(f"clunchout   {cdict['clunchout'].format('h:mm A')}")
#    print(f"p1          {tdfmt(p1)}")
#    print(f"cluncht     {tdfmt(cluncht)}")
#    print(f"p2          {tdfmt(p2)}")

print(f"Clock out at {cdict['cout'].format('h:mm A')} (in {tdfmt(cdict['cout']-arrow.get())})")
if (cdict["clunchout"] == ""):
    print(f"With 30m lunch: {(cdict['cout']+datetime.timedelta(minutes=30)).format('h:mm A')} (in {tdfmt(cdict['cout']-arrow.get()+datetime.timedelta(minutes=30))})")

# save file
with open(fn, 'w') as f:
    for key in cdict.keys():
        if type(cdict[key]) is arrow.Arrow:
            iso = cdict[key].isoformat()
            cdict[key] = iso
    json.dump(cdict, f)
