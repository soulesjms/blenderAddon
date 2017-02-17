import bpy
import sys
sys.path.insert(0, r"C:\Users\Mark\Desktop\Blender\Senior_Project_files\Python_Files")
import Addon_Model

class addon_menu(bpy.types.Menu):
    bl_label = "Material Lib"
    bl_idname = "OBJECT_MT_custom_menu"
    
    def draw(self, context):
        layout = self.layout
        mats = bpy.data.materials
        
        layout.operator("addmaterial.glass")
        layout.operator("addmaterial.stone")
        layout.operator("addmaterial.skin")
        layout.operator("addmaterial.metal")
        layout.operator("addmaterial.car")
        layout.operator("addmaterial.sand")
        layout.operator("addmaterial.rubber")
        layout.operator("addmaterial.snow")
        layout.operator("addmaterial.image")
        Addon_Model.add_icon(layout)

class PanelOne(bpy.types.Panel):
    bl_label = "Materials Library"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Material Library"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.new")
        if (bpy.data.materials.values() != []):
            layout.menu(addon_menu.bl_idname, icon_value=layout.icon(context.object.active_material))
        else:
            layout.operator("addmaterial.default")
            
            
def register():
    bpy.utils.register_class(PanelOne)
def unregister():
    bpy.utils.register_class(PanelOne)
    

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
    bl_idname = "addmaterial.rubber"
    bl_label = "Rubber Material"

    def execute(self, context):
        Addon_Model.create_rubber_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.snow"
    bl_label = "Snow Material"

    def execute(self, context):
        Addon_Model.create_snow_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.image"
    bl_label = "Image Material"

    def execute(self, context):
        Addon_Model.create_image_material()
        #Addon_Model.add_icon(self.layout)
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.default"
    bl_label = "Start Using Addon"

    def execute(self, context):
        material = bpy.data.materials.new(name="Default Material")
        bpy.context.scene.objects.active.active_material = material
        return{'FINISHED'}
bpy.utils.register_module(__name__)
