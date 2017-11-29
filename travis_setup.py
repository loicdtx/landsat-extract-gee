#!/usr/bin/env python

# THis script is used to write the GEE API key (available as GEE_API_KEY environment variable
# in the travis machine via the travis variable encription mechanism) to a file
import os

# Get key
key = os.environ['GEE_API_KEY']

# Build line
line = '{"refresh_token": "%s"}' % key

# Create directory 
os.makedirs('.config/earthengine/')

# Write line to file
with open('.config/earthengine/credentials', 'w') as dst:
   dst.write(line)

