#!/usr/bin/env python
# encoding: utf-8
"""
usingFuzz.py

Created by Aaron Erlich on 2012-08-12.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

fuzz.ratio("this is a tést", "this is a tést")

if __name__ == "__main__":
	sys.exit(main())
