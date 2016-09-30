# List of all location codes. Must be lowercase.
locations      = ["ubc", "porteau", "macmillan", "kobau", "merritt", "mitchell", "boundary"]

# Reference of location to coordinates
location_ref   = {"ubc"       : (49.2653645, -123.2520194),  # id=6173331
                  "porteau"   : (49.5822613, -123.2239489),  # id=5909028
                  "macmillan" : (49.2763368, -123.1450727),  # id=6173331
                  "merritt"   : (49.9302902, -120.6471635),  # id=6072350
                  "kobau"     : (49.1809335, -119.5571474),  # id=6093514
                  "mitchell"  : (44.5785998, -120.1671435),  # id=5721611
                  "boundary"  : (49.0039561, -123.0423283)}  # id=5807107

# Reference of short names to location codes. Every item in `locations` must also have a reference to itself.
location_short = {"ubc"  : "ubc", "porteau" : "porteau", "macmillan" : "macmillan", "van" : "ubc", "vancouver" : "ubc",
                  "kobau" : "kobau", "merritt" : "merritt", "meritt" : "merritt", "mitchell" : "mitchell",
                  "oliver" : "kobau", "aspen": "merritt", "boundary" : "boundary", "merit" : "merritt"}