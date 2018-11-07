import bpy
#import math
#import mathutils
#from mathutils import Matrix, Vector
import random
import numpy as np
import os
import pickle
import time

###################################################
#sel_cluster_no =

clusters_save_location = "E:/b_Bk@/MdHairX/scripts/clusters.gpickle"

hair_obj  = bpy.context.object.data
scalp_obj = "carla_head"
###################################################

def main():


    clusters = pickle.load(open(clusters_save_location, "rb"))

    bpy.ops.interaction_mode.edit()

    i = 0
    while(i < len(clusters)):

        bpy.ops.curve.select_all(action='DESELECT')

        print(len(clusters))

        for s in clusters[i]:
            for i in range(len(hair_obj.splines[s].points)):
                hair_obj.splines[s].points[i].select = True

        time.sleep(2)
        i += 1


if __name__ == '__main__':
    main()
