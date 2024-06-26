import numpy as np
import laspy

# Read the LAS file and convert it into a numpy array
las_file = laspy.read(...)

point_cloud = np.vstack((las_file.x, las_file.y, las_file.z)).transpose()

# Write to file

with open(..., 'w') as file:
    for i in point_cloud:
        for j in range(len(i)):
            if (j < len(i)-1):
                file.write(str(i[j]))
                file.write(',')
            else:
                file.write(str(i[j]))
                file.write('\n')