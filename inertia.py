from pprint import pprint
import sys

# local files
from inc.inertia import *


infile = sys.argv[1]
I = Inertia(infile)

It = I.GetInertiaTensor()
pprint(It)
