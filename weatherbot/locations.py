# List of all location codes. Must be lowercase.
locations      = ["ubc", "porteau", "macmillan", "kobau", "merritt", "mitchell", "boundary"]

# Reference of location to coordinates
location_ref   = {"ubc"       : (49.2653645, -123.2520194),
                  "porteau"   : (49.5571242, 123.2384998),
                  "macmillan" : (49.2763368, 123.1450727),
                  "merritt"   : (49.9308074, 120.6356903),
                  "kobau"     : (49.1865648, 119.569987),
                  "mitchell"  : (44.5701282, 120.1627358),
                  "boundary"  : (49.0039561, 123.0423283)}

# Reference of short names to location codes. Every item in `locations` must also have a reference to itself.
location_short = {"ubc"  : "ubc", "porteau" : "porteau", "macmillan" : "macmillan", "van" : "ubc", "vancouver" : "ubc",
                  "kobau" : "kobau", "merritt" : "merritt", "meritt" : "merritt", "mitchell" : "mitchell",
                  "oliver" : "kobau", "aspen": "merritt", "boundary" : "boundary", "merit" : "merritt"}