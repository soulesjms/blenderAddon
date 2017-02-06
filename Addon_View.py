import bpy
import sys
sys.path.insert(0, r"C:\Users\Mark\Desktop\Blender\CS 499 - Senior Project_files\Python_Files")
import Addon_Model

class View3DPanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Materials Addon'

    @classmethod
    def poll(cls, context):
        return (context.object is not None)


class PanelOne(View3DPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_test_1"
    bl_label = "Panel One"
    #either DEFAULT_CLOSED to be collapsed upon creation, or HIDE_HEADER to hide header upon creation
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        layout = self.layout

        layout.label("Add Materials")
        layout.operator("addmaterial.glass")
        layout.operator("addmaterial.stone")
        layout.operator("addmaterial.skin")
        layout.operator("addmaterial.metal")
        layout.operator("addmaterial.car")
        layout.operator("addmaterial.sand")
        layout.operator("addmaterial.image")


def register():
    bpy.utils.register_class(PanelOne)
def unregister():
    bpy.utils.register_class(PanelOne)
        
#def unregister():
#    bpy.utils.unregister_class(PanelOne)

class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.glass"
    bl_label = "Glass Material"

    def execute(self, context):
        Addon_Model.create_glass_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.stone"
    bl_label = "Stone Material"

    def execute(self, context):
        Addon_Model.create_stone_material()
        return{'FINISHED'}
    def draw(self, context):
        layout = self.layout
        layout.prop(text='test')
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.skin"
    bl_label = "Skin Material"

    def execute(self, context):
        Addon_Model.create_skin_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.car"
    bl_label = "Car Material"

    def execute(self, context):
        Addon_Model.create_car_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.metal"
    bl_label = "Metal Material"

    def execute(self, context):
        Addon_Model.create_metal_material()
        return{'FINISHED'}    
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.sand"
    bl_label = "Sand Material"

    def execute(self, context):
        Addon_Model.create_sand_material()
        return{'FINISHED'}    
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.image"
    bl_label = "Image Material"

    def execute(self, context):
        Addon_Model.create_image_material()
        return{'FINISHED'}
bpy.utils.register_module(__name__)
