import bpy
import numpy as np
import pickle
import os

os.system('cls')

if __name__ == "__main__":

    hair_obj  = bpy.context.object.data
    splines_save_location = "E:/b_Bk@/MdHairX/scripts/data/splines.gpickle"

    hair_strands = []
    for spline in hair_obj.splines:
        v = []
        for i in range(len(spline.points)):
            v.append(spline.points[i].co[:-1])
        hair_strands.append(np.array(v))

    print("Writing "+str(len(hair_strands))+" splines.")
    pickle.dump(hair_strands, open(splines_save_location, "wb"))

    print("\nEND")
