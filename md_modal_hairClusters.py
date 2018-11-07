import bpy
import random
import pickle

###################################################
clusters_save_location = "E:/b_Bk@/MdHairX/scripts/data/clusters.gpickle"

hair_obj  = bpy.context.object.data
scalp_obj = "carla_head"
###################################################

class HairxClusters(bpy.types.Operator):
    """Hair Clusters operations"""
    bl_idname = "wm.md_hairx_clusters"
    bl_label = "Hair Clusters operations"
    bl_options = {'REGISTER', 'UNDO'}

    tgl = bpy.props.IntProperty(default=0)
    tgl_nested = bpy.props.IntProperty(default=0)

    clusters = []
    nested_clusters = []
    id_cluster = 0

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC', 'SPACE'}:
            self.limits = 0
            self.cancel(context)
            return {'FINISHED'}

        if (event.type == 'Z') and (event.value == 'RELEASE'):
            bpy.ops.curve.select_all(action='DESELECT')

            id = self.tgl_nested % len(self.nested_clusters[self.id_cluster])
            self.report({'INFO'}, "Strand #" + str(id))

            for s in self.nested_clusters[self.id_cluster][id]:
                for i in range(len(hair_obj.splines[s].points)):
                    hair_obj.splines[s].points[i].select = True
            self.tgl_nested += 1

        elif (event.type == 'A') and  (event.value == 'RELEASE'):
            bpy.ops.curve.select_all(action='DESELECT')

            self.tgl_nested = 0
            self.id_cluster = self.tgl % len(self.clusters)
            self.report({'INFO'}, "Cluster #" + str(self.id_cluster))

            for s in self.clusters[self.id_cluster]:
                for i in range(len(hair_obj.splines[s].points)):
                    hair_obj.splines[s].points[i].select = True
            self.tgl += 1

        return {'PASS_THROUGH'}

    def execute(self, context):

        (self.clusters, self.nested_clusters) = pickle.load(open(clusters_save_location, "rb"))

        bpy.ops.interaction_mode.edit()

        self.report({'INFO'}, "Number of clusters: " + str(len(self.clusters)))

        wm = context.window_manager
        #self._timer = wm.event_timer_add(time_step=1., window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        #wm.event_timer_remove(self._timer)


def register():
    bpy.utils.register_class(HairxClusters)


def unregister():
    bpy.utils.unregister_class(HairxClusters)

if __name__ == "__main__":
    register()
