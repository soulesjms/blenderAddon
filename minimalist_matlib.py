# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Materials Minimalist Library",
    "author": "Mark Soules",
    "version": (1,0),
    "blender": (2, 77, 0),
    "location": "View3D > Tools > Material Library",
    "description": "Create materials from a pre-defined list. Unused materials will disappear from materials properties menu",
    "warning": "", # used for warning icon and text in addons panel
    "category": "Material"}

import bpy

class myMaterial:
    def __init__(self, mat_name):
        self.group = mat_name + "_group"
        
        #create material if it doesn't exist 
        if bpy.data.materials.find(mat_name + " Material") == -1: 
            self.material = bpy.data.materials.new(name=mat_name + " Material")
        else:
            self.material = bpy.data.materials[mat_name + " Material"]
        
        #create node group and name it and check if it's already made
        if bpy.data.node_groups.find(self.group) == -1:
            self.mat_group = bpy.data.node_groups.new(name=self.group, type='ShaderNodeTree')
        else:
            self.mat_group = bpy.data.node_groups[self.group]
        
        #use nodes
        self.material.use_nodes = True
        
    	#set variables for nodes. gNodes for group nodes, nodes for material nodes
        self.gNodes = self.mat_group.nodes
        self.nodes = self.material.node_tree.nodes
        
        #clear all nodes if there are any for a clean slate
        for node in self.gNodes:
            self.gNodes.remove(node)
        for node in self.nodes:
            self.nodes.remove(node)

def create_stone_material():
    stone_material = myMaterial("Stone")
    
    nodes = stone_material.nodes
    gNodes = stone_material.gNodes
    stone_group = stone_material.mat_group
    material = stone_material.material

    #create input Node for the group, and its inputs, and their default values
    stone_group.inputs.clear()
    stone_group.inputs.new("NodeSocketVector", "Vector")
    stone_group.inputs.new("NodeSocketFloat", "Scale")
    stone_group.inputs.new("NodeSocketColor", "Color 1")
    stone_group.inputs.new("NodeSocketColor", "Color 2")
    stone_group.inputs['Scale'].default_value = 1
    stone_group.inputs['Color 1'].default_value = (0.181, 0.178, 0.216, 1)
    stone_group.inputs['Color 2'].default_value = (0.451, 0.479, 0.571, 1)
    group_input = stone_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = stone_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    stone_group.outputs.clear()
    stone_group.outputs.new("NodeSocketShader", "Shader")
        
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = stone_group
    
    #create nodes
    add_shader = gNodes.new(type='ShaderNodeAddShader')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    mix_shader = gNodes.new(type='ShaderNodeMixShader')
    glossy_node = gNodes.new(type='ShaderNodeBsdfGlossy')
    color_ramp_main1 = gNodes.new(type='ShaderNodeValToRGB')
    color_ramp_main2 = gNodes.new(type='ShaderNodeValToRGB')
    color_ramp_main3 = gNodes.new(type='ShaderNodeValToRGB')
    color_ramp_main4 = gNodes.new(type='ShaderNodeValToRGB')
    color_ramp_main5 = gNodes.new(type='ShaderNodeValToRGB')
    bump_node = gNodes.new(type='ShaderNodeBump')
    noise_node_main1 = gNodes.new(type='ShaderNodeTexNoise')
    noise_node_main2 = gNodes.new(type='ShaderNodeTexNoise')
    multiply_node1 = gNodes.new(type='ShaderNodeMath')
    multiply_node2 = gNodes.new(type='ShaderNodeMath')
    multiply_node3 = gNodes.new(type='ShaderNodeMath')
    multiply_node4 = gNodes.new(type='ShaderNodeMath')
    multiply_node5 = gNodes.new(type='ShaderNodeMath')
    overlay_node1 = gNodes.new(type='ShaderNodeMixRGB')
    overlay_node2 = gNodes.new(type='ShaderNodeMixRGB')
    mix_node = gNodes.new(type='ShaderNodeMixRGB')
    geometry_node = gNodes.new(type='ShaderNodeNewGeometry')
    add_node1 = gNodes.new(type='ShaderNodeMixRGB')
    add_node2 = gNodes.new(type='ShaderNodeMixRGB')
    add_node3 = gNodes.new(type='ShaderNodeMixRGB')
    multiply_rgb = gNodes.new(type='ShaderNodeMixRGB')
    color_ramp1 = gNodes.new(type='ShaderNodeValToRGB')
    color_ramp2 = gNodes.new(type='ShaderNodeValToRGB')
    color_ramp3 = gNodes.new(type='ShaderNodeValToRGB')
    musgrave_node = gNodes.new(type='ShaderNodeTexMusgrave')
    noise_node1 = gNodes.new(type='ShaderNodeTexNoise')
    noise_node2 = gNodes.new(type='ShaderNodeTexNoise')
    noise_node3 = gNodes.new(type='ShaderNodeTexNoise')
    mapping_node = gNodes.new(type='ShaderNodeMapping')
    texture_coord = nodes.new(type='ShaderNodeTexCoord')
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    material_output.location = 400,0
    
    #change node default values
    multiply_node1.operation = 'MULTIPLY'
    multiply_node2.operation = 'MULTIPLY'
    multiply_node3.operation = 'MULTIPLY'
    multiply_node4.operation = 'MULTIPLY'
    multiply_node5.operation = 'MULTIPLY'
    add_node1.blend_type = 'ADD'
    add_node2.blend_type = 'ADD'
    add_node3.blend_type = 'ADD'
    overlay_node1.blend_type = 'OVERLAY'
    overlay_node2.blend_type = 'OVERLAY'
    multiply_rgb.blend_type = 'MULTIPLY'
    mix_shader.inputs[0].default_value = 0.1
    bump_node.inputs[0].default_value = 0.5
    color_ramp_main1.color_ramp.elements[0].position = 0.627
    color_ramp_main1.color_ramp.elements[1].position = 0.636
    color_ramp_main3.color_ramp.elements[0].position = 0.491
    color_ramp_main3.color_ramp.elements[1].position = 0.609
    color_ramp_main5.color_ramp.elements[0].position = 0.605
    noise_node_main1.inputs[2].default_value = 16
    noise_node_main2.inputs[2].default_value = 16
    multiply_node1.inputs[1].default_value = 6
    multiply_node2.inputs[1].default_value = 3
    multiply_node3.inputs[1].default_value = 0.5
    multiply_node4.inputs[1].default_value = 2
    multiply_node5.inputs[1].default_value = 3
    overlay_node2.inputs[0].default_value = 1
    overlay_node2.use_clamp = True
    add_node1.inputs[0].default_value = 1
    add_node2.inputs[0].default_value = 1
    add_node3.inputs[0].default_value = 1
    multiply_rgb.inputs[0].default_value = 1
    musgrave_node.inputs[2].default_value = 16
    musgrave_node.inputs[3].default_value = 0
    musgrave_node.inputs[4].default_value = 1.5
    color_ramp1.color_ramp.elements[0].position = 0.605
    color_ramp2.color_ramp.elements[0].position = 0.605
    color_ramp3.color_ramp.elements[0].position = 0.605
    color_ramp1.color_ramp.interpolation = 'B_SPLINE'
    color_ramp2.color_ramp.interpolation = 'B_SPLINE'
    color_ramp3.color_ramp.interpolation = 'B_SPLINE'
    color_ramp_main5.color_ramp.interpolation = 'B_SPLINE'
    noise_node1.inputs[2].default_value = 16
    noise_node2.inputs[2].default_value = 16
    noise_node3.inputs[2].default_value = 16
    mapping_node.rotation[1] = 0.0174533
    mapping_node.rotation[2] = 3.01942

    #link nodes
    gLinks = stone_group.links
    links = material.node_tree.links
    gLinks.new(group_input.outputs[0],      mapping_node.inputs[0])
    gLinks.new(group_input.outputs[0],      noise_node1.inputs[0])
    gLinks.new(group_input.outputs[0],      noise_node2.inputs[0])
    gLinks.new(group_input.outputs[0],      noise_node3.inputs[0])
    gLinks.new(group_input.outputs[0],      noise_node_main1.inputs[0])
    gLinks.new(group_input.outputs[0],      noise_node_main2.inputs[0])
    gLinks.new(group_input.outputs[1],      noise_node1.inputs[1])
    gLinks.new(group_input.outputs[1],      multiply_node5.inputs[0])
    gLinks.new(group_input.outputs[1],      multiply_node3.inputs[0])
    gLinks.new(group_input.outputs[2],      mix_node.inputs[1])
    gLinks.new(group_input.outputs[3],      mix_node.inputs[2])
    gLinks.new(multiply_node5.outputs[0],   noise_node2.inputs[1])
    gLinks.new(multiply_node5.outputs[0],   multiply_node4.inputs[0])
    gLinks.new(multiply_node4.outputs[0],   noise_node3.inputs[1])
    gLinks.new(multiply_node4.outputs[0],   multiply_node2.inputs[0])
    gLinks.new(multiply_node4.outputs[0],   multiply_node2.inputs[1])
    gLinks.new(multiply_node3.outputs[0],   musgrave_node.inputs[1])
    gLinks.new(multiply_node2.outputs[0],   noise_node_main2.inputs[1])
    gLinks.new(multiply_node2.outputs[0],   multiply_node1.inputs[0])
    gLinks.new(noise_node3.outputs[1],      color_ramp3.inputs[0])
    gLinks.new(noise_node2.outputs[1],      color_ramp2.inputs[0])
    gLinks.new(noise_node1.outputs[1],      color_ramp1.inputs[0])
    gLinks.new(mapping_node.outputs[0],     musgrave_node.inputs[0])
    gLinks.new(color_ramp1.outputs[0],      add_node2.inputs[1])
    gLinks.new(color_ramp1.outputs[0],      add_node3.inputs[1])
    gLinks.new(color_ramp2.outputs[0],      add_node2.inputs[2])
    gLinks.new(color_ramp3.outputs[0],      add_node3.inputs[2])
    gLinks.new(noise_node_main2.outputs[1], color_ramp_main5.inputs[0])
    gLinks.new(add_node3.outputs[0],        multiply_rgb.inputs[2])
    gLinks.new(add_node2.outputs[0],        multiply_rgb.inputs[1])
    gLinks.new(multiply_rgb.outputs[0],     add_node1.inputs[1])
    gLinks.new(color_ramp_main5.outputs[0], add_node1.inputs[2])
    gLinks.new(musgrave_node.outputs[1],    color_ramp_main4.inputs[0])
    gLinks.new(color_ramp_main4.outputs[0], overlay_node2.inputs[2])
    gLinks.new(add_node1.outputs[0],        overlay_node2.inputs[1])
    gLinks.new(overlay_node2.outputs[0],    mix_node.inputs[0])
    gLinks.new(geometry_node.outputs[7],    color_ramp_main3.inputs[0])
    gLinks.new(color_ramp_main3.outputs[0], overlay_node1.inputs[2])
    gLinks.new(mix_node.outputs[0],         overlay_node1.inputs[1])
    gLinks.new(multiply_node1.outputs[0],   noise_node_main1.inputs[1])
    gLinks.new(noise_node_main1.outputs[0], color_ramp_main1.inputs[0])
    gLinks.new(color_ramp_main2.outputs[0], bump_node.inputs[2])
    gLinks.new(bump_node.outputs[0],        glossy_node.inputs[2])
    gLinks.new(overlay_node1.outputs[0],    diffuse_node.inputs[0])
    gLinks.new(overlay_node1.outputs[0],    color_ramp_main2.inputs[0])
    gLinks.new(bump_node.outputs[0],        diffuse_node.inputs[2])
    gLinks.new(color_ramp_main1.outputs[0], glossy_node.inputs[0])
    gLinks.new(glossy_node.outputs[0],      mix_shader.inputs[2])
    gLinks.new(mix_shader.outputs[0],       add_shader.inputs[1])
    gLinks.new(diffuse_node.outputs[0],     add_shader.inputs[0])
    gLinks.new(add_shader.outputs[0],       group_output.inputs[0])
    links.new(texture_coord.outputs[3],     nodes['Group'].inputs[0])
    links.new(nodes['Group'].outputs[0],    material_output.inputs[0])

    bpy.context.scene.objects.active.active_material = material
    

def create_metal_material():
    metal_material = myMaterial("Metal")
    
    nodes = metal_material.nodes
    gNodes = metal_material.gNodes
    metal_group = metal_material.mat_group
    material = metal_material.material
	
    #create input Node for the group, and its inputs, and their default values
    metal_group.inputs.clear()
    metal_group.inputs.new("NodeSocketColor", "Metal Color")
    metal_group.inputs.new("NodeSocketVector", "Brush Coords")
    metal_group.inputs.new("NodeSocketFloat", "Brush Scale")
    metal_group.inputs.new("NodeSocketFloat", "Brush Detail")
    metal_group.inputs.new("NodeSocketFloat", "Brush Strength")
    metal_group.inputs.new("NodeSocketFloat", "Brush Opacity")
    metal_group.inputs.new("NodeSocketColor", "Base Diffusion")
    metal_group.inputs.new("NodeSocketFloat", "Diffusion Opacity")
    metal_group.inputs['Metal Color'].default_value = (0.868, 0.866, 0.900, 1)
    metal_group.inputs['Brush Scale'].default_value = 25
    metal_group.inputs['Brush Detail'].default_value = 2
    metal_group.inputs['Brush Strength'].default_value =4
    metal_group.inputs['Brush Opacity'].default_value = 1
    metal_group.inputs['Base Diffusion'].default_value = (0.8, 0.8, 0.8, 1)
    group_input = metal_group.nodes.new("NodeGroupInput")
	
    #create the output Node for the group
    group_output = metal_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    metal_group.outputs.clear()
    metal_group.outputs.new("NodeSocketShader", "Shader")
    metal_group.outputs.new("NodeSocketFloat", "Bump")
        
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = metal_group
	
	#create nodes
    mapping_node = gNodes.new(type='ShaderNodeMapping')
    subtract_node = gNodes.new(type='ShaderNodeMath')
    multiply_node = gNodes.new(type='ShaderNodeMath')
    glossy_node = gNodes.new(type='ShaderNodeBsdfGlossy')
    noise_texture = gNodes.new(type='ShaderNodeTexNoise')
    velvet_node = gNodes.new(type='ShaderNodeBsdfVelvet')
    add_shader = gNodes.new(type='ShaderNodeAddShader')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    mix_shader = gNodes.new(type='ShaderNodeMixShader')
    texture_coord = nodes.new(type='ShaderNodeTexCoord')
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    
    #modify node default values
    subtract_node.operation = 'SUBTRACT'
    multiply_node.operation = 'MULTIPLY'
    subtract_node.inputs[1].default_value = 1
    mapping_node.scale[0] = 100
    mapping_node.scale[1] = 0
    mapping_node.scale[2] = 0
    
    
	#create links between nodes
    gLinks = metal_group.links
    links = material.node_tree.links
    gLinks.new( mapping_node.outputs[0], noise_texture.inputs[0])
    gLinks.new(subtract_node.outputs[0],   glossy_node.inputs[1])
    gLinks.new(  velvet_node.outputs[0],    add_shader.inputs[1])
    gLinks.new(  glossy_node.outputs[0],    add_shader.inputs[0])
    gLinks.new(   add_shader.outputs[0],    mix_shader.inputs[1])
    gLinks.new( diffuse_node.outputs[0],    mix_shader.inputs[2])
    gLinks.new(   mix_shader.outputs[0],  group_output.inputs[0])
    gLinks.new(noise_texture.outputs[1], multiply_node.inputs[0])
    gLinks.new(multiply_node.outputs[0],  group_output.inputs[1])
    gLinks.new(  group_input.outputs[0],   glossy_node.inputs[0])
    gLinks.new(  group_input.outputs[0],   velvet_node.inputs[0])
    gLinks.new(  group_input.outputs[1],  mapping_node.inputs[0])
    gLinks.new(  group_input.outputs[2], noise_texture.inputs[1])
    gLinks.new(  group_input.outputs[3], noise_texture.inputs[2])
    gLinks.new(  group_input.outputs[4], multiply_node.inputs[1])
    gLinks.new(  group_input.outputs[5], subtract_node.inputs[0])
    gLinks.new(  group_input.outputs[5],   velvet_node.inputs[1])
    gLinks.new(  group_input.outputs[6],  diffuse_node.inputs[0])
    gLinks.new(  group_input.outputs[7],    mix_shader.inputs[0])
    
    links.new( texture_coord.outputs[0],  nodes['Group'].inputs[1])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])
    links.new(nodes['Group'].outputs[1], material_output.inputs[2])
	
    bpy.context.scene.objects.active.active_material = material
	
def create_car_material():
    car_material = myMaterial("Car")
    
    nodes = car_material.nodes
    gNodes = car_material.gNodes
    car_group = car_material.mat_group
    material = car_material.material
    
    #create input node for group, and its inputs and their default values
    car_group.inputs.clear()
    car_group.inputs.new("NodeSocketColor", "Diffuse Color")
    car_group.inputs.new("NodeSocketColor", "Reflection Color")
    car_group.inputs.new("NodeSocketFloatFactor", "Roughness")
    car_group.inputs.new("NodeSocketFloatFactor", "Reflection")
    car_group.inputs.new("NodeSocketVector", "Normal")
    car_group.inputs['Diffuse Color'].default_value = (1, 0, 0, 1)
    car_group.inputs['Reflection Color'].default_value = (1, 1, 1, 1)
    car_group.inputs['Roughness'].default_value = 0
    car_group.inputs['Reflection'].default_value = 0.3
    group_input = car_group.nodes.new("NodeGroupInput")
    group_input.location = (-200, 0)
    
    #create the output Node for the group
    group_output = car_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    car_group.outputs.clear()
    car_group.outputs.new("NodeSocketShader", "Shader")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = car_group
    
    #create nodes
    power_node1 = gNodes.new(type='ShaderNodeMath')
    power_node2 = gNodes.new(type='ShaderNodeMath')
    fresnel_node = gNodes.new(type='ShaderNodeFresnel')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    glossy_node = gNodes.new(type='ShaderNodeBsdfGlossy')
    mix_node = gNodes.new(type='ShaderNodeMixRGB')
    mix_shader = gNodes.new(type='ShaderNodeMixShader')
    material_output = nodes.new('ShaderNodeOutputMaterial')
    geometry_node = gNodes.new(type='ShaderNodeNewGeometry')
    mix_node2 = gNodes.new(type='ShaderNodeMixRGB')
    bump_node = gNodes.new(type='ShaderNodeBump')
    
    
    #modify values
    power_node1.inputs[1].default_value = 2
    power_node2.inputs[1].default_value = 2
    power_node1.operation = 'POWER'
    power_node2.operation = 'POWER'
    mix_node.inputs[2].default_value = (1, 1, 1, 1)
    car_group.inputs[2].min_value = 0
    car_group.inputs[3].min_value = 0
    car_group.inputs[2].max_value = 1
    car_group.inputs[3].max_value = 1
    
    
    #create Links
    gLinks = car_group.links
    links = material.node_tree.links
    gLinks.new(group_input.outputs[0], diffuse_node.inputs[0])
    gLinks.new(group_input.outputs[1], glossy_node.inputs[0])
    gLinks.new(group_input.outputs[2], power_node1.inputs[0])
    gLinks.new(group_input.outputs[3], power_node2.inputs[0])
    gLinks.new(group_input.outputs[4], bump_node.inputs[3])
    gLinks.new(group_input.outputs[4], diffuse_node.inputs[2])
    gLinks.new(group_input.outputs[4], glossy_node.inputs[2])
    gLinks.new(power_node1.outputs[0], mix_node2.inputs[0])
    gLinks.new(power_node1.outputs[0], glossy_node.inputs[1])
    gLinks.new(power_node1.outputs[0], diffuse_node.inputs[1])
    gLinks.new(power_node2.outputs[0], mix_node.inputs[1])
    gLinks.new(fresnel_node.outputs[0], mix_node.inputs[0])
    gLinks.new(diffuse_node.outputs[0], mix_shader.inputs[1])
    gLinks.new(glossy_node.outputs[0], mix_shader.inputs[2])
    gLinks.new(mix_node.outputs[0], mix_shader.inputs[0])
    gLinks.new(mix_shader.outputs[0], group_output.inputs[0])
    gLinks.new(mix_node2.outputs[0], fresnel_node.inputs[1])
    gLinks.new(bump_node.outputs[0], mix_node2.inputs[1])
    gLinks.new(geometry_node.outputs[0], mix_node2.inputs[2])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])
    
    bpy.context.scene.objects.active.active_material = material
    
def create_skin_material():
    #create material if it doesn't exist 
    if bpy.data.materials.find('Skin Material') == -1:
        material = bpy.data.materials.new(name="Skin Material")
    else:
        material = bpy.data.materials["Skin Material"]
    
    #create node group and name it and check if it's already made
    if bpy.data.node_groups.find('skinGroup') == -1:
        skin_group = bpy.data.node_groups.new(name='skinGroup', type='ShaderNodeTree')
    else:
        skin_group = bpy.data.node_groups['skinGroup']
    
    #use nodes
    material.use_nodes = True
    
	#set variables for nodes. gNodes for group nodes, nodes for material nodes
    gNodes = skin_group.nodes
    nodes = material.node_tree.nodes
    
    #clear all nodes if there are any for a clean slate
    for node in gNodes:
        gNodes.remove(node)
    for node in nodes:
        nodes.remove(node)
        
    #create input node for group, and its inputs and their default values
    skin_group.inputs.clear()
    skin_group.inputs.new("NodeSocketColor", "Skin Color")
    skin_group.inputs['Skin Color'].default_value = (0.800, 0.545, 0.461, 1)
    skin_group.inputs.new("NodeSocketFloat", "Color Multiply")
    skin_group.inputs['Color Multiply'].default_value = 1.2
    group_input = skin_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = skin_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    skin_group.outputs.clear()
    skin_group.outputs.new("NodeSocketShader", "Shader")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = skin_group
    
    #create nodes
    multiply_node = gNodes.new(type='ShaderNodeMixRGB')
    subsurf_scatter = gNodes.new(type='ShaderNodeSubsurfaceScattering')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    glossy_node = gNodes.new(type='ShaderNodeBsdfGlossy')
    mix_shader1 = gNodes.new(type='ShaderNodeMixShader')
    mix_shader2 = gNodes.new(type='ShaderNodeMixShader')
    RGB_node = gNodes.new(type='ShaderNodeRGB')
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    
    #modify node default values
    multiply_node.blend_type = 'MULTIPLY'
    subsurf_scatter.falloff = 'CUBIC'
    RGB_node.outputs[0].default_value = (0.318, 0.171, 0.089, 1)
    diffuse_node.inputs[0].default_value = (0.800, 0.693, 0.465, 1)
    mix_shader1.inputs[0].default_value = 0.300
    mix_shader2.inputs[0].default_value = 0.300
    
    #create link between nodes
    gLinks = skin_group.links
    links = material.node_tree.links
    gLinks.new(group_input.outputs[0], subsurf_scatter.inputs[0])
    gLinks.new(group_input.outputs[1], multiply_node.inputs[2])
    gLinks.new(multiply_node.outputs[0], subsurf_scatter.inputs[2])
    gLinks.new(diffuse_node.outputs[0], mix_shader1.inputs[1])
    gLinks.new(glossy_node.outputs[0], mix_shader1.inputs[2])
    gLinks.new(subsurf_scatter.outputs[0], mix_shader2.inputs[1])
    gLinks.new(mix_shader1.outputs[0], mix_shader2.inputs[2])
    gLinks.new(mix_shader2.outputs[0], group_output.inputs[0])
    gLinks.new(RGB_node.outputs[0], multiply_node.inputs[1])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])

    bpy.context.scene.objects.active.active_material = material
    
def create_glass_material():
    #create material if it doesn't exist 
    if bpy.data.materials.find('Glass Material') == -1:
        material = bpy.data.materials.new(name="Glass Material")
    else:
        material = bpy.data.materials["Glass Material"]
    
    #use nodes
    material.use_nodes = True
    
    #set variables for nodes. gNodes for group nodes, nodes for material nodes
    nodes = material.node_tree.nodes
    
    #clear all nodes if there are any for a clean slate
    for node in nodes:
        nodes.remove(node)
        
    material_output = nodes.new('ShaderNodeOutputMaterial')
    glossy_node = nodes.new('ShaderNodeBsdfGlass')
    
    links = material.node_tree.links
    links.new(glossy_node.outputs[0], material_output.inputs[0])
    
    bpy.context.scene.objects.active.active_material = material


def create_image_material():
    #create material if it doesn't exist 
    if bpy.data.materials.find('Image Material') == -1:
        material = bpy.data.materials.new(name="Image Material")
    else:
        material = bpy.data.materials["Image Material"]
    
    #use nodes
    material.use_nodes = True
    
    #set variables for nodes. gNodes for group nodes, nodes for material nodes
    nodes = material.node_tree.nodes
    
    #clear all nodes if there are any for a clean slate
    for node in nodes:
        nodes.remove(node)
        
    material_output = nodes.new('ShaderNodeOutputMaterial')
    diffuse_node = nodes.new('ShaderNodeBsdfDiffuse')
    image_node = nodes.new('ShaderNodeTexImage')
    
    links = material.node_tree.links
    links.new(image_node.outputs[0], diffuse_node.inputs[0])
    links.new(image_node.outputs[0], material_output.inputs[2])
    links.new(diffuse_node.outputs[0], material_output.inputs[0])
    
    bpy.context.scene.objects.active.active_material = material


def create_sand_material():
    sand_material = myMaterial("Sand")
    
    nodes = sand_material.nodes
    gNodes = sand_material.gNodes
    sand_group = sand_material.mat_group
    material = sand_material.material
        
    #create input node for group, and its inputs and their default values
    sand_group.inputs.clear()
    sand_group.inputs.new("NodeSocketColor", "Sand Color1")
    sand_group.inputs.new("NodeSocketColor", "Sand Color2")
    sand_group.inputs.new("NodeSocketFloat", "Displacement Height")
    sand_group.inputs.new("NodeSocketFloat", "Waves Scale")
    sand_group.inputs.new("NodeSocketFloat", "Smooth Scale")
    sand_group.inputs.new("NodeSocketFloat", "Small Waves Scale")
    sand_group.inputs['Sand Color1'].default_value = (0.8, 0.659, 0.504, 1)
    sand_group.inputs['Sand Color2'].default_value = (0.521, 0.513, 0.335, 1)
    sand_group.inputs['Displacement Height'].default_value = 0.350
    sand_group.inputs['Waves Scale'].default_value = 3
    sand_group.inputs['Smooth Scale'].default_value = 5
    sand_group.inputs['Small Waves Scale'].default_value = 25
    group_input = sand_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = sand_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    sand_group.outputs.clear()
    sand_group.outputs.new("NodeSocketShader", "Shader")
    sand_group.outputs.new("NodeSocketColor", "Color")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = sand_group
    
    #create nodes
    hue_saturation1 = gNodes.new(type='ShaderNodeHueSaturation')
    hue_saturation2 = gNodes.new(type='ShaderNodeHueSaturation')
    hue_saturation3 = gNodes.new(type='ShaderNodeHueSaturation')
    mix_shader = gNodes.new(type='ShaderNodeMixShader')
    mix_node1 = gNodes.new(type='ShaderNodeMixRGB')
    mix_node2 = gNodes.new(type='ShaderNodeMixRGB')
    diffuse_node1 = gNodes.new(type='ShaderNodeBsdfDiffuse')
    diffuse_node2 = gNodes.new(type='ShaderNodeBsdfDiffuse')
    noise_node1 = gNodes.new(type='ShaderNodeTexNoise')
    noise_node2 = gNodes.new(type='ShaderNodeTexNoise')
    noise_node3 = gNodes.new(type='ShaderNodeTexNoise')
    wave_node1 = gNodes.new(type='ShaderNodeTexWave')
    wave_node2 = gNodes.new(type='ShaderNodeTexWave')
    bright_contrast = gNodes.new(type='ShaderNodeBrightContrast')
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    
    #modify node default values
    hue_saturation1.inputs[1].default_value = 0
    noise_node1.inputs[2].default_value = 5
    noise_node2.inputs[2].default_value = 10
    bright_contrast.inputs[1].default_value = -0.250
    bright_contrast.inputs[2].default_value = 1
    hue_saturation2.inputs[2].default_value = 0.1
    hue_saturation3.inputs[2].default_value = 10
    noise_node3.inputs[2].default_value = 10
    noise_node3.inputs[3].default_value = 0.5
    wave_node1.inputs[2].default_value = 25
    wave_node1.inputs[3].default_value = 10
    wave_node1.inputs[4].default_value = 1
    wave_node2.inputs[2].default_value = 15
    wave_node2.inputs[3].default_value = 1
    wave_node2.inputs[4].default_value = 5
    
    #create link between nodes
    gLinks = sand_group.links
    links = material.node_tree.links
    gLinks.new(mix_shader.outputs[0], group_output.inputs[0])
    gLinks.new(hue_saturation1.outputs[0], group_output.inputs[1])
    gLinks.new(noise_node1.outputs[1], mix_shader.inputs[0])
    gLinks.new(diffuse_node1.outputs[0], mix_shader.inputs[1])
    gLinks.new(diffuse_node2.outputs[0], mix_shader.inputs[2])
    gLinks.new(group_input.outputs[2], hue_saturation1.inputs[2])
    gLinks.new(mix_node1.outputs[0], hue_saturation1.inputs[4])
    gLinks.new(group_input.outputs[0], diffuse_node1.inputs[0])
    gLinks.new(group_input.outputs[1], diffuse_node2.inputs[0])
    gLinks.new(bright_contrast.outputs[0], mix_node1.inputs[0])
    gLinks.new(mix_node2.outputs[0], mix_node1.inputs[1])
    gLinks.new(hue_saturation2.outputs[0], mix_node1.inputs[2])
    gLinks.new(noise_node2.outputs[1], bright_contrast.inputs[0])
    gLinks.new(wave_node1.outputs[1], mix_node2.inputs[1])
    gLinks.new(hue_saturation3.outputs[0], mix_node2.inputs[2])
    gLinks.new(wave_node2.outputs[1], hue_saturation2.inputs[4])
    gLinks.new(group_input.outputs[3], wave_node1.inputs[1])
    gLinks.new(noise_node3.outputs[1], hue_saturation3.inputs[4])
    gLinks.new(group_input.outputs[4], noise_node3.inputs[1])
    gLinks.new(group_input.outputs[5], wave_node2.inputs[1])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])
    links.new(nodes['Group'].outputs[1], material_output.inputs[2])
    
    bpy.context.scene.objects.active.active_material = material
    
    
def create_rubber_material():
    #create material if it doesn't exist 
    if bpy.data.materials.find('Rubber Material') == -1:
        material = bpy.data.materials.new(name="Rubber Material")
    else:
        material = bpy.data.materials["Rubber Material"]
    
    #create node group and name it and check if it's already made
    if bpy.data.node_groups.find('rubberGroup') == -1:
        rubber_group = bpy.data.node_groups.new(name='rubberGroup', type='ShaderNodeTree')
    else:
        rubber_group = bpy.data.node_groups['rubberGroup']
    
    #use nodes
    material.use_nodes = True
    
	#set variables for nodes. gNodes for group nodes, nodes for material nodes
    gNodes = rubber_group.nodes
    nodes = material.node_tree.nodes
    
    #clear all nodes if there are any for a clean slate
    for node in gNodes:
        gNodes.remove(node)
    for node in nodes:
        nodes.remove(node)
        
    #create input node for group, and its inputs and their default values
    rubber_group.inputs.clear()
    rubber_group.inputs.new("NodeSocketColor", "Rubber Color")
    rubber_group.inputs['Rubber Color'].default_value = (0.011, 0.011, 0.011, 1)
    group_input = rubber_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = rubber_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    rubber_group.outputs.clear()
    rubber_group.outputs.new("NodeSocketShader", "Shader")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = rubber_group
    
    #create nodes
    add_shader = gNodes.new(type='ShaderNodeAddShader')
    mix_node = gNodes.new(type='ShaderNodeMixRGB')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    translucent_node = gNodes.new(type='ShaderNodeBsdfTranslucent')
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    
    #modify node default values
    diffuse_node.inputs[1].default_value = 0
    
    #create link between nodes
    gLinks = rubber_group.links
    links = material.node_tree.links
    gLinks.new(group_input.outputs[0], mix_node.inputs[1])
    gLinks.new(group_input.outputs[0], diffuse_node.inputs[0])
    gLinks.new(mix_node.outputs[0], translucent_node.inputs[0])
    gLinks.new(translucent_node.outputs[0], add_shader.inputs[1])
    gLinks.new(diffuse_node.outputs[0], add_shader.inputs[0])
    gLinks.new(add_shader.outputs[0], group_output.inputs[0])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])
    
    bpy.context.scene.objects.active.active_material = material
    
def create_snow_material():
     #create material if it doesn't exist 
    if bpy.data.materials.find('Snow Material') == -1:
        material = bpy.data.materials.new(name="Snow Material")
    else:
        material = bpy.data.materials["Snow Material"]
    
    #create node group and name it and check if it's already made
    if bpy.data.node_groups.find('snowGroup') == -1:
        snow_group = bpy.data.node_groups.new(name='snowGroup', type='ShaderNodeTree')
    else:
        snow_group = bpy.data.node_groups['snowGroup']
    
    #use nodes
    material.use_nodes = True
    
	#set variables for nodes. gNodes for group nodes, nodes for material nodes
    gNodes = snow_group.nodes
    nodes = material.node_tree.nodes
    
    #clear all nodes if there are any for a clean slate
    for node in gNodes:
        gNodes.remove(node)
    for node in nodes:
        nodes.remove(node)
        
    #create input node for group, and its inputs and their default values
    snow_group.inputs.clear()
    snow_group.inputs.new("NodeSocketColor", "Snow Color")
    snow_group.inputs['Snow Color'].default_value = (1, 1, 1, 1)
    snow_group.inputs.new("NodeSocketColor", "Reflection Color")
    snow_group.inputs['Reflection Color'].default_value = (0.75, 0.75, 0.75, 1)
    snow_group.inputs.new("NodeSocketFloat", "Scale")
    snow_group.inputs['Scale'].default_value = 25.000
    snow_group.inputs.new("NodeSocketFloat", "Detail")
    snow_group.inputs['Detail'].default_value = 6.000
    snow_group.inputs.new("NodeSocketFloat", "Distortion")
    snow_group.inputs['Distortion'].default_value = 0.500
    group_input = snow_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = snow_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    snow_group.outputs.clear()
    snow_group.outputs.new("NodeSocketShader", "Shader")
    snow_group.outputs.new("NodeSocketFloat", "Value")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = snow_group
    
    #create nodes
    noise_texture = gNodes.new(type='ShaderNodeTexNoise')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    mix_node = gNodes.new(type='ShaderNodeMixShader')
    subtract_node = gNodes.new(type='ShaderNodeMath')
    glossy_node = gNodes.new(type='ShaderNodeBsdfGlossy')
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    
    #modify node default values
    subtract_node.operation = 'SUBTRACT'
    glossy_node.inputs[1].default_value = 0.5
    diffuse_node.inputs[1].default_value = 1
    subtract_node.inputs[0].default_value = 1
    mix_node.inputs[0].default_value = 0.3
    
    #create links
    gLinks = snow_group.links
    links = material.node_tree.links
    gLinks.new(group_input.outputs[0], glossy_node.inputs[0])
    gLinks.new(group_input.outputs[1], diffuse_node.inputs[0])
    gLinks.new(group_input.outputs[1], glossy_node.inputs[0])
    gLinks.new(group_input.outputs[2], noise_texture.inputs[1])
    gLinks.new(group_input.outputs[3], noise_texture.inputs[2])
    gLinks.new(group_input.outputs[4], noise_texture.inputs[3])
    gLinks.new(noise_texture.outputs[1], subtract_node.inputs[1])
    gLinks.new(diffuse_node.outputs[0], mix_node.inputs[1])
    gLinks.new(glossy_node.outputs[0], mix_node.inputs[2])
    gLinks.new(mix_node.outputs[0], group_output.inputs[0])
    gLinks.new(subtract_node.outputs[0], group_output.inputs[1])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])
    links.new(nodes['Group'].outputs[1], material_output.inputs[2])
    
    bpy.context.scene.objects.active.active_material = material
    
    
def create_hair_material():
    #create material if it doesn't exist 
    if bpy.data.materials.find('Hair Material') == -1:
        material = bpy.data.materials.new(name="Hair Material")
    else:
        material = bpy.data.materials["Hair Material"]
    
    #create node group and name it and check if it's already made
    if bpy.data.node_groups.find('hairGroup') == -1:
        hair_group = bpy.data.node_groups.new(name='hairGroup', type='ShaderNodeTree')
    else:
        hair_group = bpy.data.node_groups['hairGroup']
    
    #use nodes
    material.use_nodes = True
    
	#set variables for nodes. gNodes for group nodes, nodes for material nodes
    gNodes = hair_group.nodes
    nodes = material.node_tree.nodes
    
    #clear all nodes if there are any for a clean slate
    for node in gNodes:
        gNodes.remove(node)
    for node in nodes:
        nodes.remove(node)
        
    #create input node for group, and its inputs and their default values
    hair_group.inputs.clear()
    hair_group.inputs.new("NodeSocketColor", "hair Color")
    hair_group.inputs.new("NodeSocketColor", "hair highlight")
    hair_group.inputs['hair Color'].default_value = (0.402, 0.266, 0.093, 1)
    hair_group.inputs['hair highlight'].default_value = (0.266, 0.266, 0.266, 1)
    group_input = hair_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = hair_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    hair_group.outputs.clear()
    hair_group.outputs.new("NodeSocketShader", "Shader")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = hair_group
    
    #create nodes
    add_node = gNodes.new('ShaderNodeMixRGB')
    hair_node = gNodes.new('ShaderNodeBsdfHair')
    glossy_node = gNodes.new('ShaderNodeBsdfGlossy')
    mix_node = gNodes.new('ShaderNodeMixShader')
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    
    #modify node default values
    add_node.blend_type = 'ADD'
    mix_node.inputs[0].default_value = 0.05
    
    #create links
    gLinks = hair_group.links
    links = material.node_tree.links
    gLinks.new(group_input.outputs[0], add_node.inputs[1])
    gLinks.new(group_input.outputs[1], add_node.inputs[2])
    gLinks.new(hair_node.outputs[0], mix_node.inputs[1])
    gLinks.new(glossy_node.outputs[0], mix_node.inputs[2])
    gLinks.new(mix_node.outputs[0], group_output.inputs[0])
    gLinks.new(add_node.outputs[0], hair_node.inputs[0])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])
    
    bpy.context.scene.objects.active.active_material = material
    
    
def create_wood_material():
    wood_material = myMaterial("Wood")
    
    nodes = wood_material.nodes
    gNodes = wood_material.gNodes
    wood_group = wood_material.mat_group
    material = wood_material.material
        
    #create input node for group, and its inputs and their default values
    wood_group.inputs.clear()
    wood_group.inputs.new("NodeSocketVector", "Vector")
    wood_group.inputs.new("NodeSocketColor", "wood Color")
    wood_group.inputs.new("NodeSocketColor", "wood bands color")
    wood_group.inputs.new("NodeSocketFloat", "wood scale")
    wood_group.inputs.new("NodeSocketFloat", "Bump Factor")
    wood_group.inputs['wood Color'].default_value = (0.022, 0.018, 0.012, 1)
    wood_group.inputs['wood bands color'].default_value = (0.070, 0.032, 0.014, 1)
    wood_group.inputs['wood scale'].default_value = -0.6
    group_input = wood_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = wood_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    wood_group.outputs.clear()
    wood_group.outputs.new("NodeSocketShader", "Shader")
    wood_group.outputs.new("NodeSocketFloat", "Wood Bump")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = wood_group
    
    #create nodes
    texture_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping_node = gNodes.new(type='ShaderNodeMapping')
    wave_node = gNodes.new(type='ShaderNodeTexWave')
    color_ramp = gNodes.new(type='ShaderNodeValToRGB')
    greater_than = gNodes.new(type='ShaderNodeMath')
    color_mix = gNodes.new(type='ShaderNodeMixRGB')
    color_mix2 = gNodes.new(type='ShaderNodeMixRGB')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    glossy_node = gNodes.new(type='ShaderNodeBsdfGlossy')
    mix_node = gNodes.new(type='ShaderNodeMixShader')
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    voronoi_node = gNodes.new(type='ShaderNodeTexVoronoi')
    multiply_node = gNodes.new(type='ShaderNodeMath')
    
    #modify values
    color_ramp.color_ramp.elements.new(0.425)
    color_ramp.color_ramp.elements.new(0.540)
    color_ramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1)
    color_ramp.color_ramp.elements[1].color = (0, 0, 0, 1)
    color_ramp.color_ramp.elements[2].color = (0, 0, 0, 1)
    glossy_node.inputs[1].default_value = 0.167
    multiply_node.operation = 'MULTIPLY'
    #multiply_node.inputs[1].default_value = 0.3
    greater_than.operation = 'GREATER_THAN'
    color_mix.blend_type = 'MIX'
    color_mix2.blend_type = 'MIX'
    color_mix2.inputs[0].default_value = 0.418
    mix_node.inputs[0].default_value = 0.05
    mapping_node.scale[0] = 3.6
    mapping_node.scale[1] = 12
    mapping_node.scale[2] = 12
    mapping_node.translation[0] = -5.6
    wave_node.inputs[2].default_value = 15
    wave_node.inputs[3].default_value = 2
    wave_node.inputs[4].default_value = 1
    greater_than.inputs[1].default_value = 0.1
    voronoi_node.inputs[1].default_value = 18.5
    
    #create Links
    gLinks = wood_group.links
    links = material.node_tree.links
    links.new(texture_coord.outputs[3], nodes['Group'].inputs[3])
    gLinks.new(mapping_node.outputs[0], wave_node.inputs[0])
    gLinks.new(wave_node.outputs[0], color_mix2.inputs[1])
    gLinks.new(voronoi_node.outputs[0], color_mix2.inputs[2])
    gLinks.new(color_mix2.outputs[0], color_ramp.inputs[0])
    gLinks.new(color_ramp.outputs[0], greater_than.inputs[0])
    gLinks.new(greater_than.outputs[0], color_mix.inputs[0])
    gLinks.new(color_mix.outputs[0], diffuse_node.inputs[0])
    gLinks.new(glossy_node.outputs[0], mix_node.inputs[2])
    gLinks.new(diffuse_node.outputs[0], mix_node.inputs[1])
    gLinks.new(mix_node.outputs[0], group_output.inputs[0])
    gLinks.new(group_input.outputs[0], mapping_node.inputs[0])
    gLinks.new(group_input.outputs[1], color_mix.inputs[1])
    gLinks.new(group_input.outputs[2], color_mix.inputs[2])
    gLinks.new(group_input.outputs[3], wave_node.inputs[1])
    gLinks.new(group_input.outputs[4], multiply_node.inputs[1])
    gLinks.new(color_mix.outputs[0], multiply_node.inputs[0])
    gLinks.new(wave_node.outputs[0], color_mix2.inputs[1])
    gLinks.new(multiply_node.outputs[0], group_output.inputs[1])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])
    links.new(nodes['Group'].outputs[1], material_output.inputs[2])
    
    bpy.context.scene.objects.active.active_material = material
    
    
def create_sky_material():
    sky_material = myMaterial("Sky")
    
    nodes = sky_material.nodes
    gNodes = sky_material.gNodes
    sky_group = sky_material.mat_group
    material = sky_material.material
    
    #create input node for group, and its inputs and their default values
    sky_group.inputs.clear()
    sky_group.inputs.new("NodeSocketFloat", "sky scale")
    sky_group.inputs['sky scale'].default_value = 10
    group_input = sky_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = sky_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    sky_group.outputs.clear()
    sky_group.outputs.new("NodeSocketShader", "Shader")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = sky_group
    
    #create nodes
    noise_node = gNodes.new(type='ShaderNodeTexNoise')
    color_ramp = gNodes.new(type='ShaderNodeValToRGB')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    
    #modify values
    color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[1].color = (0, 0.108, 0.5, 1)
    diffuse_node.inputs[1].default_value = 0.2
    
    #create Links
    gLinks = sky_group.links
    links = material.node_tree.links
    gLinks.new(noise_node.outputs[0], color_ramp.inputs[0])
    gLinks.new(color_ramp.outputs[0], diffuse_node.inputs[0])
    gLinks.new(diffuse_node.outputs[0], group_output.inputs[0])
    gLinks.new(group_input.outputs[0], noise_node.inputs[1])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])
    
    bpy.context.scene.objects.active.active_material = material
    
    
def create_fire_material():
    fire_material = myMaterial("Fire")
    
    nodes = fire_material.nodes
    gNodes = fire_material.gNodes
    fire_group = fire_material.mat_group
    material = fire_material.material
    
    #create input node for group, and its inputs and their default values
    fire_group.inputs.clear()
    fire_group.inputs.new("NodeSocketFloat", "Smoke Density")
    fire_group.inputs.new("NodeSocketFloat", "Flame Density")
    fire_group.inputs.new("NodeSocketFloat", "Temperature")
    fire_group.inputs['Smoke Density'].default_value = 7.500
    fire_group.inputs['Flame Density'].default_value = 5.000
    fire_group.inputs['Temperature'].default_value = 1750.000
    group_input = fire_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = fire_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    fire_group.outputs.clear()
    fire_group.outputs.new("NodeSocketShader", "Shader")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = fire_group
    
    #create nodes
    add_node1 = gNodes.new(type='ShaderNodeAddShader')
    add_node2 = gNodes.new(type='ShaderNodeAddShader')
    vol_absorption = gNodes.new(type='ShaderNodeVolumeAbsorption')
    vol_scatter = gNodes.new(type='ShaderNodeVolumeScatter')
    emit_shader = gNodes.new(type='ShaderNodeEmission')
    black_body = gNodes.new(type='ShaderNodeBlackbody')
    multiply_node1 = gNodes.new(type='ShaderNodeMath')
    multiply_node2 = gNodes.new(type='ShaderNodeMath')
    flame_node = gNodes.new(type='ShaderNodeAttribute')
    smoke_node = gNodes.new(type='ShaderNodeAttribute')
    material_output = nodes.new('ShaderNodeOutputMaterial')
    
    #modify values
    smoke_node.attribute_name = "density"
    flame_node.attribute_name = "flame"
    multiply_node1.operation = 'MULTIPLY'
    multiply_node2.operation = 'MULTIPLY'
    
    #create Links
    gLinks = fire_group.links
    links = material.node_tree.links
    gLinks.new(group_input.outputs[0], multiply_node1.inputs[1])
    gLinks.new(group_input.outputs[1], multiply_node2.inputs[1])
    gLinks.new(group_input.outputs[2], black_body.inputs[0])
    gLinks.new(smoke_node.outputs[2], multiply_node1.inputs[0])
    gLinks.new(flame_node.outputs[2], multiply_node2.inputs[0])
    gLinks.new(multiply_node1.outputs[0], vol_absorption.inputs[1])
    gLinks.new(multiply_node1.outputs[0], vol_scatter.inputs[1])
    gLinks.new(multiply_node2.outputs[0], emit_shader.inputs[1])
    gLinks.new(black_body.outputs[0], emit_shader.inputs[0])
    gLinks.new(vol_absorption.outputs[0], add_node1.inputs[0])
    gLinks.new(vol_scatter.outputs[0], add_node1.inputs[1])
    gLinks.new(black_body.outputs[0], emit_shader.inputs[0])
    gLinks.new(add_node1.outputs[0], add_node2.inputs[0])
    gLinks.new(add_node2.outputs[0], group_output.inputs[0])
    gLinks.new(emit_shader.outputs[0], add_node2.inputs[1])
    links.new(nodes['Group'].outputs[0], material_output.inputs[1])
    
    bpy.context.scene.objects.active.active_material = material
    
    
def create_silk_material(): 
    silk_material = myMaterial("Silk")
    
    nodes = silk_material.nodes
    gNodes = silk_material.gNodes
    silk_group = silk_material.mat_group
    material = silk_material.material
    
    #create input node for group, and its inputs and their default values
    silk_group.inputs.clear()
    silk_group.inputs.new("NodeSocketColor", "Color 1")
    silk_group.inputs.new("NodeSocketColor", "Color 2")
    silk_group.inputs.new("NodeSocketColor", "Sheen Color")
    silk_group.inputs.new("NodeSocketFloat", "Roughness")
    silk_group.inputs.new("NodeSocketFloat", "Sheen Factor")
    silk_group.inputs['Color 1'].default_value = (0.06, 0.5, 0.074, 1)
    silk_group.inputs['Color 2'].default_value = (0.037, 0.227, 0.044, 1)
    silk_group.inputs['Sheen Color'].default_value = (0.579, 0.8, 0.502, 1)
    silk_group.inputs['Roughness'].default_value = 0
    silk_group.inputs['Sheen Factor'].default_value = 0.7
    
    group_input = silk_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = silk_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    silk_group.outputs.clear()
    silk_group.outputs.new("NodeSocketShader", "Shader")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = silk_group
    
    #create nodes
    mix_node = gNodes.new(type='ShaderNodeMixShader')
    anisotropic_node = gNodes.new(type='ShaderNodeBsdfAnisotropic')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    rgb_mix_node = gNodes.new(type='ShaderNodeMixRGB')
    layer_weight = gNodes.new(type='ShaderNodeLayerWeight')
    material_output = nodes.new('ShaderNodeOutputMaterial')
    
    #modify values
    layer_weight.inputs[0].default_value = 0.4
    anisotropic_node.distribution = 'BECKMANN'
    
    #create Links
    gLinks = silk_group.links
    links = material.node_tree.links
    gLinks.new(group_input.outputs[0], rgb_mix_node.inputs[1])
    gLinks.new(group_input.outputs[1], rgb_mix_node.inputs[2])
    gLinks.new(group_input.outputs[3], diffuse_node.inputs[1])
    gLinks.new(group_input.outputs[2], anisotropic_node.inputs[0])
    gLinks.new(group_input.outputs[4], mix_node.inputs[0])
    gLinks.new(layer_weight.outputs[1], rgb_mix_node.inputs[0])
    gLinks.new(rgb_mix_node.outputs[0], diffuse_node.inputs[0])
    gLinks.new(anisotropic_node.outputs[0], mix_node.inputs[2])
    gLinks.new(diffuse_node.outputs[0], mix_node.inputs[1])
    gLinks.new(mix_node.outputs[0], group_output.inputs[0])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])
    
    bpy.context.scene.objects.active.active_material = material
    
    
def create_silk_material(): 
    silk_material = myMaterial("Silk")
    
    nodes = silk_material.nodes
    gNodes = silk_material.gNodes
    silk_group = silk_material.mat_group
    material = silk_material.material
    
    #create input node for group, and its inputs and their default values
    silk_group.inputs.clear()
    silk_group.inputs.new("NodeSocketColor", "Color 1")
    silk_group.inputs.new("NodeSocketColor", "Color 2")
    silk_group.inputs.new("NodeSocketColor", "Sheen Color")
    silk_group.inputs.new("NodeSocketFloat", "Roughness")
    silk_group.inputs.new("NodeSocketFloat", "Sheen Factor")
    silk_group.inputs['Color 1'].default_value = (0.06, 0.5, 0.074, 1)
    silk_group.inputs['Color 2'].default_value = (0.037, 0.227, 0.044, 1)
    silk_group.inputs['Sheen Color'].default_value = (0.579, 0.8, 0.502, 1)
    silk_group.inputs['Roughness'].default_value = 0
    silk_group.inputs['Sheen Factor'].default_value = 0.7
    
    group_input = silk_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = silk_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    silk_group.outputs.clear()
    silk_group.outputs.new("NodeSocketShader", "Shader")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = silk_group
    
    #create nodes
    mix_node = gNodes.new(type='ShaderNodeMixShader')
    anisotropic_node = gNodes.new(type='ShaderNodeBsdfAnisotropic')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    rgb_mix_node = gNodes.new(type='ShaderNodeMixRGB')
    layer_weight = gNodes.new(type='ShaderNodeLayerWeight')
    material_output = nodes.new('ShaderNodeOutputMaterial')
    
    #modify values
    layer_weight.inputs[0].default_value = 0.4
    anisotropic_node.distribution = 'BECKMANN'
    
    #create Links
    gLinks = silk_group.links
    links = material.node_tree.links
    gLinks.new(group_input.outputs[0], rgb_mix_node.inputs[1])
    gLinks.new(group_input.outputs[1], rgb_mix_node.inputs[2])
    gLinks.new(group_input.outputs[3], diffuse_node.inputs[1])
    gLinks.new(group_input.outputs[2], anisotropic_node.inputs[0])
    gLinks.new(group_input.outputs[4], mix_node.inputs[0])
    gLinks.new(layer_weight.outputs[1], rgb_mix_node.inputs[0])
    gLinks.new(rgb_mix_node.outputs[0], diffuse_node.inputs[0])
    gLinks.new(anisotropic_node.outputs[0], mix_node.inputs[2])
    gLinks.new(diffuse_node.outputs[0], mix_node.inputs[1])
    gLinks.new(mix_node.outputs[0], group_output.inputs[0])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])
    
    bpy.context.scene.objects.active.active_material = material
    
    
def create_dirt_material(): 
    dirt_material = myMaterial("Dirt")
    
    nodes = dirt_material.nodes
    gNodes = dirt_material.gNodes
    dirt_group = dirt_material.mat_group
    material = dirt_material.material
    
    #create input node for group, and its inputs and their default values
    dirt_group.inputs.clear()
    dirt_group.inputs.new("NodeSocketVector", "Vector")
    dirt_group.inputs.new("NodeSocketColor", "Color 1")
    dirt_group.inputs.new("NodeSocketColor", "Color 2")
    dirt_group.inputs['Color 1'].default_value = (0.137, 0.078, 0.049, 1)
    dirt_group.inputs['Color 2'].default_value = (0.035, 0.021, 0.014, 1)
    dirt_group.inputs.new("NodeSocketFloat", "Texture Scale")
    dirt_group.inputs['Texture Scale'].default_value = 7
    group_input = dirt_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = dirt_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    dirt_group.outputs.clear()
    dirt_group.outputs.new("NodeSocketFloat", "Bump")
    dirt_group.outputs.new("NodeSocketShader", "Shader")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = dirt_group
    
    #create nodes
    mix_node = gNodes.new(type='ShaderNodeMixShader')
    mix_node2 = gNodes.new(type='ShaderNodeMixShader')
    fresnel_node = gNodes.new(type='ShaderNodeFresnel')
    subsurf_scatter = gNodes.new(type='ShaderNodeSubsurfaceScattering')
    fresnel_node2 = gNodes.new(type='ShaderNodeFresnel')
    mix_node3 = gNodes.new(type='ShaderNodeMixShader')
    glossy_node = gNodes.new(type='ShaderNodeBsdfGlossy')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    diffuse_node2 = gNodes.new(type='ShaderNodeBsdfDiffuse')
    invert_node = gNodes.new(type='ShaderNodeInvert') 
    multiply_node = gNodes.new(type='ShaderNodeMath')
    bump_node = gNodes.new(type='ShaderNodeBump')
    musgrave_node = gNodes.new(type='ShaderNodeTexMusgrave')
    musgrave_node2 = gNodes.new(type='ShaderNodeTexMusgrave')
    subtract_node = gNodes.new(type='ShaderNodeMath')
    mapping_node = gNodes.new(type='ShaderNodeMapping')
    material_output = nodes.new('ShaderNodeOutputMaterial')
    texture_coord = nodes.new('ShaderNodeTexCoord')
    
    #modify values
    subtract_node.inputs[1].default_value = 2
    musgrave_node2.inputs[2].default_value = 14
    musgrave_node2.inputs[3].default_value = 0.1
    musgrave_node2.inputs[4].default_value = 4.5
    musgrave_node.inputs[2].default_value = 7
    musgrave_node.inputs[3].default_value = 1.2
    musgrave_node.inputs[4].default_value = 4.5
    bump_node.inputs[0].default_value = 0.3
    multiply_node.inputs[1].default_value = 4
    fresnel_node2.inputs[0].default_value = 1.200
    glossy_node.inputs[0].default_value = (0.704, 0.568, 0.398, 1)
    glossy_node.inputs[1].default_value = 0.4
    subsurf_scatter.inputs[0].default_value = (0.137, 0.078, 0.049, 1)
    subsurf_scatter.falloff = 'CUBIC'
    subtract_node.operation = 'SUBTRACT'
    multiply_node.operation = 'MULTIPLY'
    
    #create Links
    gLinks = dirt_group.links
    links = material.node_tree.links
    gLinks.new(group_input.outputs[0], mapping_node.inputs[0])
    gLinks.new(group_input.outputs[1], diffuse_node.inputs[0])
    gLinks.new(group_input.outputs[2], diffuse_node2.inputs[0])
    gLinks.new(group_input.outputs[3], subtract_node.inputs[0])
    gLinks.new(group_input.outputs[3], musgrave_node.inputs[1])
    gLinks.new(mapping_node.outputs[0], musgrave_node2.inputs[0])
    gLinks.new(mapping_node.outputs[0], musgrave_node.inputs[0])
    gLinks.new(subtract_node.outputs[0], musgrave_node2.inputs[1])
    gLinks.new(musgrave_node2.outputs[0], invert_node.inputs[1])
    gLinks.new(musgrave_node2.outputs[0], bump_node.inputs[2])
    gLinks.new(musgrave_node.outputs[0], multiply_node.inputs[0])
    gLinks.new(multiply_node.outputs[0], group_output.inputs[0])
    gLinks.new(bump_node.outputs[0], diffuse_node.inputs[2])
    gLinks.new(bump_node.outputs[0], diffuse_node2.inputs[2])
    gLinks.new(bump_node.outputs[0], glossy_node.inputs[2])
    gLinks.new(invert_node.outputs[0], mix_node3.inputs[0])
    gLinks.new(diffuse_node.outputs[0], mix_node3.inputs[2])
    gLinks.new(diffuse_node2.outputs[0], mix_node3.inputs[1])
    gLinks.new(mix_node3.outputs[0], mix_node2.inputs[1])
    #gLinks.new(group_input.outputs[1], subsurf_scatter.inputs[0])
    gLinks.new(fresnel_node2.outputs[0], mix_node2.inputs[0])
    gLinks.new(glossy_node.outputs[0], mix_node2.inputs[2])
    gLinks.new(mix_node2.outputs[0], mix_node.inputs[1])
    gLinks.new(subsurf_scatter.outputs[0], mix_node.inputs[2])
    gLinks.new(fresnel_node.outputs[0], mix_node.inputs[0])
    gLinks.new(mix_node.outputs[0], group_output.inputs[1])
    links.new(nodes['Group'].outputs[0], material_output.inputs[2])
    links.new(nodes['Group'].outputs[1], material_output.inputs[0])
    links.new(texture_coord.outputs[0], nodes['Group'].inputs[0])
    
    bpy.context.scene.objects.active.active_material = material
        
    
def create_leather_material(): 
    leather_material = myMaterial("Leather")
    
    nodes = leather_material.nodes
    gNodes = leather_material.gNodes
    leather_group = leather_material.mat_group
    material = leather_material.material
    
    #create input node for group, and its inputs and their default values
    leather_group.inputs.clear()
    leather_group.inputs.new("NodeSocketVector", "Vector")
    leather_group.inputs.new("NodeSocketFloat", "Glossy Roughness")
    leather_group.inputs.new("NodeSocketFloat", "Glossy Amount")
    leather_group.inputs.new("NodeSocketFloat", "Scale")
    leather_group.inputs.new("NodeSocketColor", "Color1")
    leather_group.inputs.new("NodeSocketColor", "Color2")
    leather_group.inputs.new("NodeSocketFloat", "Bump Strength")
    leather_group.inputs.new("NodeSocketFloat", "Wear & Tear Amount")
    leather_group.inputs.new("NodeSocketFloat", "Leather Pattern Color Amount")
    leather_group.inputs['Glossy Roughness'].default_value = 0.2
    leather_group.inputs['Glossy Amount'].default_value = 0.6
    leather_group.inputs['Scale'].default_value = 12
    leather_group.inputs['Color1'].default_value = (0.057, 0.038, 0.028, 1)
    leather_group.inputs['Color2'].default_value = (0.1, 0.067, 0.048, 1)
    leather_group.inputs['Bump Strength'].default_value = 0.13
    leather_group.inputs['Wear & Tear Amount'].default_value = 0.5
    leather_group.inputs['Leather Pattern Color Amount'].default_value = 0.3
    group_input = leather_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = leather_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    leather_group.outputs.clear()
    leather_group.outputs.new("NodeSocketShader", "Shader")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = leather_group
    
    #create nodes
    bump_node = gNodes.new(type='ShaderNodeBump')
    color_ramp = gNodes.new(type='ShaderNodeValToRGB')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    geometry_node = gNodes.new(type='ShaderNodeNewGeometry')
    glossy_node = gNodes.new(type='ShaderNodeBsdfGlossy')
    layer_weight = gNodes.new(type='ShaderNodeLayerWeight')
    light_path_node = gNodes.new(type='ShaderNodeLightPath')
    math_node1 = gNodes.new(type='ShaderNodeMath')
    math_node2 = gNodes.new(type='ShaderNodeMath')
    math_node3 = gNodes.new(type='ShaderNodeMath')
    math_node4 = gNodes.new(type='ShaderNodeMath')
    math_node5 = gNodes.new(type='ShaderNodeMath')
    math_node6 = gNodes.new(type='ShaderNodeMath')
    math_node7 = gNodes.new(type='ShaderNodeMath')
    math_node8 = gNodes.new(type='ShaderNodeMath')
    math_node9 = gNodes.new(type='ShaderNodeMath')
    rgb_mix_node1 = gNodes.new(type='ShaderNodeMixRGB')
    rgb_mix_node2 = gNodes.new(type='ShaderNodeMixRGB')
    rgb_mix_node3 = gNodes.new(type='ShaderNodeMixRGB')
    rgb_mix_node4 = gNodes.new(type='ShaderNodeMixRGB')
    rgb_mix_node5 = gNodes.new(type='ShaderNodeMixRGB')
    rgb_mix_node6 = gNodes.new(type='ShaderNodeMixRGB')
    rgb_mix_node7 = gNodes.new(type='ShaderNodeMixRGB')
    rgb_mix_node8 = gNodes.new(type='ShaderNodeMixRGB')
    mix_shader = gNodes.new(type='ShaderNodeMixShader')
    noise_node = gNodes.new(type='ShaderNodeTexNoise')
    voronoi_node1 = gNodes.new(type='ShaderNodeTexVoronoi')
    voronoi_node2 = gNodes.new(type='ShaderNodeTexVoronoi')
    voronoi_node3 = gNodes.new(type='ShaderNodeTexVoronoi')
    material_output = nodes.new('ShaderNodeOutputMaterial')
    texture_coord = nodes.new('ShaderNodeTexCoord')
    
    #modify values
    bump_node.invert = True
    math_node1.operation = 'MULTIPLY'
    math_node2.operation = 'MULTIPLY'
    math_node2.inputs[1].default_value = 10
    math_node3.operation = 'MULTIPLY'
    math_node4.operation = 'MULTIPLY'
    math_node4.inputs[1].default_value = 3
    math_node5.operation = 'MULTIPLY'
    math_node5.inputs[1].default_value = 1.5
    math_node6.operation = 'MULTIPLY'
    math_node6.inputs[1].default_value = 4
    math_node7.operation = 'MULTIPLY'
    math_node7.inputs[1].default_value = 2.5
    math_node8.operation = 'DIVIDE'
    math_node8.inputs[1].default_value = 3
    math_node9.operation = 'POWER'
    math_node9.inputs[1].default_value = 5
    rgb_mix_node1.inputs[1].default_value = (0.007, 0.007, 0.007, 1)
    rgb_mix_node1.inputs[2].default_value = (0.703, 0.703, 0.703, 1)
    rgb_mix_node2.inputs[1].default_value = (0.009, 0.009, 0.009, 1)
    rgb_mix_node2.inputs[2].default_value = (0.729, 0.708, 0.708, 1)
    rgb_mix_node3.inputs[1].default_value = (0, 0, 0, 1)
    rgb_mix_node4.inputs[0].default_value = 0.3
    rgb_mix_node6.blend_type = 'DODGE'
    rgb_mix_node7.blend_type = 'OVERLAY'
    rgb_mix_node8.blend_type = 'ADD'
    rgb_mix_node8.inputs[0].default_value = 1
    color_ramp.color_ramp.elements[0].position = 0.505
    color_ramp.color_ramp.elements[1].position = 0.664
    
    #create Links
    gLinks = leather_group.links
    links = material.node_tree.links
    gLinks.new(mix_shader.outputs[0], group_output.inputs[0])
    gLinks.new(math_node1.outputs[0], mix_shader.inputs[0])
    gLinks.new(diffuse_node.outputs[0], mix_shader.inputs[1])
    gLinks.new(glossy_node.outputs[0], mix_shader.inputs[2])
    gLinks.new(rgb_mix_node1.outputs[0], math_node1.inputs[0])
    gLinks.new(math_node2.outputs[0], math_node1.inputs[1])
    gLinks.new(rgb_mix_node7.outputs[0], diffuse_node.inputs[0])
    gLinks.new(bump_node.outputs[0], diffuse_node.inputs[2])
    gLinks.new(math_node3.outputs[0], glossy_node.inputs[1])
    gLinks.new(bump_node.outputs[0], glossy_node.inputs[2])
    gLinks.new(rgb_mix_node2.outputs[0], math_node3.inputs[0])
    gLinks.new(group_input.outputs[1], math_node3.inputs[1])
    gLinks.new(group_input.outputs[7], rgb_mix_node7.inputs[0])
    gLinks.new(rgb_mix_node6.outputs[0], rgb_mix_node7.inputs[1])
    gLinks.new(color_ramp.outputs[0], rgb_mix_node7.inputs[2])
    gLinks.new(group_input.outputs[2], math_node2.inputs[0])
    gLinks.new(math_node9.outputs[0], rgb_mix_node1.inputs[0])
    gLinks.new(layer_weight.outputs[1], rgb_mix_node2.inputs[0])
    gLinks.new(layer_weight.outputs[1], math_node9.inputs[0])
    gLinks.new(bump_node.outputs[0], layer_weight.inputs[1])
    gLinks.new(group_input.outputs[6], bump_node.inputs[0])
    gLinks.new(rgb_mix_node3.outputs[0], bump_node.inputs[2])
    gLinks.new(light_path_node.outputs[0], rgb_mix_node3.inputs[0])
    gLinks.new(rgb_mix_node8.outputs[0], rgb_mix_node3.inputs[2])
    gLinks.new(rgb_mix_node4.outputs[0], rgb_mix_node8.inputs[1])
    gLinks.new(math_node4.outputs[0], rgb_mix_node8.inputs[2])
    gLinks.new(voronoi_node1.outputs[0], math_node4.inputs[0])
    gLinks.new(rgb_mix_node4.outputs[0], rgb_mix_node6.inputs[2])
    gLinks.new(rgb_mix_node5.outputs[0], rgb_mix_node6.inputs[1])
    gLinks.new(group_input.outputs[8], rgb_mix_node6.inputs[0])
    gLinks.new(noise_node.outputs[1], rgb_mix_node5.inputs[0])
    gLinks.new(group_input.outputs[4], rgb_mix_node5.inputs[1])
    gLinks.new(group_input.outputs[5], rgb_mix_node5.inputs[2])
    gLinks.new(group_input.outputs[0], noise_node.inputs[0])
    gLinks.new(math_node5.outputs[0], noise_node.inputs[1])
    gLinks.new(group_input.outputs[3], math_node5.inputs[0])
    gLinks.new(geometry_node.outputs[7], color_ramp.inputs[0])
    gLinks.new(group_input.outputs[0], voronoi_node1.inputs[0])
    gLinks.new(group_input.outputs[0], voronoi_node2.inputs[0])
    gLinks.new(math_node7.outputs[0], voronoi_node2.inputs[1])
    gLinks.new(group_input.outputs[0], voronoi_node3.inputs[0])
    gLinks.new(math_node8.outputs[0], voronoi_node1.inputs[1])
    gLinks.new(voronoi_node2.outputs[0], rgb_mix_node4.inputs[2])
    gLinks.new(voronoi_node3.outputs[1], rgb_mix_node4.inputs[1])
    gLinks.new(group_input.outputs[3], math_node8.inputs[0])
    gLinks.new(math_node6.outputs[0], voronoi_node3.inputs[1])
    gLinks.new(math_node6.outputs[0], math_node7.inputs[0])
    gLinks.new(group_input.outputs[3], math_node6.inputs[0])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])
    links.new(texture_coord.outputs[3], nodes['Group'].inputs[0])
    
    bpy.context.scene.objects.active.active_material = material
    
def create_mirror_material():
    #create material if it doesn't exist 
    if bpy.data.materials.find('Mirror Material') == -1:
        material = bpy.data.materials.new(name="Mirror Material")
    else:
        material = bpy.data.materials["Mirror Material"]
    
    #use nodes
    material.use_nodes = True
    
    #set variables for nodes. gNodes for group nodes, nodes for material nodes
    nodes = material.node_tree.nodes
    
    #clear all nodes if there are any for a clean slate
    for node in nodes:
        nodes.remove(node)
        
    material_output = nodes.new('ShaderNodeOutputMaterial')
    glossy_node = nodes.new('ShaderNodeBsdfGlossy')
    
    glossy_node.inputs[1].default_value = 0
    
    links = material.node_tree.links
    links.new(glossy_node.outputs[0], material_output.inputs[0])
    
    bpy.context.scene.objects.active.active_material = material
    

def create_light_material():
    #create material if it doesn't exist 
    if bpy.data.materials.find('Light Material') == -1:
        material = bpy.data.materials.new(name="Light Material")
    else:
        material = bpy.data.materials["Light Material"]
    
    #use nodes
    material.use_nodes = True
    
    #set variables for nodes. gNodes for group nodes, nodes for material nodes
    nodes = material.node_tree.nodes
    
    #clear all nodes if there are any for a clean slate
    for node in nodes:
        nodes.remove(node)
        
    material_output = nodes.new('ShaderNodeOutputMaterial')
    emission_node = nodes.new('ShaderNodeEmission')
    
    links = material.node_tree.links
    links.new(emission_node.outputs[0], material_output.inputs[0])
    
    bpy.context.scene.objects.active.active_material = material
    
    
def create_concrete_material():
    concrete_material = myMaterial("Concrete")
    
    nodes = concrete_material.nodes
    gNodes = concrete_material.gNodes
    concrete_group = concrete_material.mat_group
    material = concrete_material.material
    
    concrete_group.inputs.clear()
    concrete_group.inputs.new("NodeSocketVector", "Vector")
    concrete_group.inputs.new("NodeSocketColor", "Concrete Color 1")
    concrete_group.inputs.new("NodeSocketColor", "Concrete Color 2")
    concrete_group.inputs.new("NodeSocketFloatFactor", "Texture Scale")
    concrete_group.inputs.new("NodeSocketFloatFactor", "Texture for Specular")
    concrete_group.inputs.new("NodeSocketFloatFactor", "Scratches Displacement Strength")
    concrete_group.inputs.new("NodeSocketFloatFactor", "Grunge Use Diffuse")
    concrete_group.inputs.new("NodeSocketColor", "Grunge Color 1")
    concrete_group.inputs.new("NodeSocketColor", "Grunge Color 2")
    concrete_group.inputs.new("NodeSocketFloatFactor", "Concrete Bump Strength")
    concrete_group.inputs['Concrete Color 1'].default_value = (0.292, 0.292, 0.292, 1)
    concrete_group.inputs['Concrete Color 2'].default_value = (0.657, 0.657, 0.657, 1)
    concrete_group.inputs['Texture Scale'].default_value = 4
    concrete_group.inputs['Texture for Specular'].default_value = 0.5
    concrete_group.inputs['Scratches Displacement Strength'].default_value = 1
    concrete_group.inputs['Grunge Use Diffuse'].default_value = 1
    concrete_group.inputs['Grunge Color 1'].default_value = (0.017, 0.021, 0.006, 1)
    concrete_group.inputs['Grunge Color 2'].default_value = (0.074, 0.056, 0.049, 1)
    concrete_group.inputs['Concrete Bump Strength'].default_value = 1
    group_input = concrete_group.nodes.new("NodeGroupInput")
    group_input.location = (-200, 0)
    
    #create the output Node for the group
    group_output = concrete_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    concrete_group.outputs.clear()
    concrete_group.outputs.new("NodeSocketShader", "Shader")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = concrete_group
    
    #create nodes
    mix_shader = gNodes.new(type='ShaderNodeMixShader')
    glossy_node = gNodes.new(type='ShaderNodeBsdfGlossy')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    bump_node = gNodes.new(type='ShaderNodeBump')
    color_ramp_main = gNodes.new(type='ShaderNodeValToRGB')
    color_ramp1 = gNodes.new(type='ShaderNodeValToRGB')
    color_ramp2 = gNodes.new(type='ShaderNodeValToRGB')
    color_ramp3 = gNodes.new(type='ShaderNodeValToRGB')
    layer_weight = gNodes.new(type='ShaderNodeLayerWeight')
    geometry_node = gNodes.new(type='ShaderNodeNewGeometry')
    mix_node1 = gNodes.new(type='ShaderNodeMixRGB')
    mix_node2 = gNodes.new(type='ShaderNodeMixRGB')
    mix_node3 = gNodes.new(type='ShaderNodeMixRGB')
    multiply_node1 = gNodes.new(type='ShaderNodeMath')
    multiply_node2 = gNodes.new(type='ShaderNodeMath')
    multiply_node3 = gNodes.new(type='ShaderNodeMath')
    multiply_rgb = gNodes.new(type='ShaderNodeMixRGB')
    noise_node1 = gNodes.new(type='ShaderNodeTexNoise')
    noise_node2 = gNodes.new(type='ShaderNodeTexNoise')
    noise_node3 = gNodes.new(type='ShaderNodeTexNoise')
    noise_node4 = gNodes.new(type='ShaderNodeTexNoise')
    overlay_node_main1 = gNodes.new(type='ShaderNodeMixRGB')
    overlay_node_main2 = gNodes.new(type='ShaderNodeMixRGB')
    overlay_node1 = gNodes.new(type='ShaderNodeMixRGB')
    overlay_node2 = gNodes.new(type='ShaderNodeMixRGB')
    bright_contrast = gNodes.new(type='ShaderNodeBrightContrast')
    texture_coord = nodes.new(type='ShaderNodeTexCoord')
    material_output = nodes.new('ShaderNodeOutputMaterial')
    
    #modify values
    multiply_rgb.blend_type = 'MULTIPLY'
    overlay_node_main1.blend_type = 'OVERLAY'
    overlay_node_main2.blend_type = 'OVERLAY'
    overlay_node1.blend_type = 'OVERLAY'
    overlay_node2.blend_type = 'OVERLAY'
    multiply_node1.operation = 'MULTIPLY'
    multiply_node2.operation = 'MULTIPLY'
    multiply_node3.operation = 'MULTIPLY'
    overlay_node_main1.inputs[0].default_value = 1
    overlay_node_main2.inputs[0].default_value = 1
    bright_contrast.inputs[2].default_value = -0.2
    noise_node4.inputs[2].default_value = 16
    noise_node4.inputs[3].default_value = 1
    noise_node3.inputs[2].default_value = 16
    noise_node2.inputs[2].default_value = 16
    multiply_node1.inputs[1].default_value = 1.7
    multiply_node2.inputs[1].default_value = 14
    multiply_node3.inputs[1].default_value = 70
    color_ramp3.color_ramp.elements[0].position = 0.486
    color_ramp3.color_ramp.elements[1].position = 0.509
    color_ramp2.color_ramp.elements[0].position = 0.355
    color_ramp2.color_ramp.elements[0].color = (0.072, 0.072, 0.072, 1)
    color_ramp2.color_ramp.elements[1].color = (0.013, 0.031, 0.031, 1)
    color_ramp1.color_ramp.elements[0].color = (0.065, 0.065, 0.065, 1)
    color_ramp1.color_ramp.elements[1].color = (0.200, 0.200, 0.200, 1)
    
    #create Links
    gLinks = concrete_group.links
    links = material.node_tree.links
    gLinks.new(mix_shader.outputs[0], group_output.inputs[0])
    gLinks.new(multiply_rgb.outputs[0], mix_shader.inputs[0])
    gLinks.new(glossy_node.outputs[0], mix_shader.inputs[2])
    gLinks.new(diffuse_node.outputs[0], mix_shader.inputs[1])
    gLinks.new(bump_node.outputs[0], diffuse_node.inputs[2])
    gLinks.new(bump_node.outputs[0], glossy_node.inputs[2])
    gLinks.new(mix_node1.outputs[0], diffuse_node.inputs[0])
    gLinks.new(overlay_node2.outputs[0], glossy_node.inputs[1])
    gLinks.new(color_ramp_main.outputs[0], bump_node.inputs[2])
    gLinks.new(overlay_node_main1.outputs[0], color_ramp_main.inputs[0])
    gLinks.new(group_input.outputs[9], bump_node.inputs[0])
    gLinks.new(mix_node2.outputs[0], mix_node1.inputs[1])
    gLinks.new(mix_node3.outputs[0], mix_node1.inputs[2])
    gLinks.new(multiply_node1.outputs[0], mix_node3.inputs[0])
    gLinks.new(group_input.outputs[1], mix_node3.inputs[2])
    gLinks.new(group_input.outputs[2], mix_node3.inputs[1])
    gLinks.new(overlay_node_main1.outputs[0], multiply_node1.inputs[0])
    gLinks.new(overlay_node_main1.outputs[0], overlay_node1.inputs[2])
    gLinks.new(overlay_node_main1.outputs[0], overlay_node2.inputs[2])
    gLinks.new(overlay_node_main2.outputs[0], overlay_node_main1.inputs[1])
    gLinks.new(noise_node2.outputs[1], overlay_node_main1.inputs[2])
    gLinks.new(group_input.outputs[0], noise_node2.inputs[0])
    gLinks.new(color_ramp3.outputs[0], multiply_rgb.inputs[2])
    gLinks.new(color_ramp3.outputs[0], mix_node1.inputs[0])
    gLinks.new(group_input.outputs[6], multiply_rgb.inputs[0])
    gLinks.new(overlay_node1.outputs[0], multiply_rgb.inputs[1])
    gLinks.new(color_ramp1.outputs[0], overlay_node1.inputs[1])
    gLinks.new(group_input.outputs[4], overlay_node1.inputs[0])
    gLinks.new(group_input.outputs[4], overlay_node2.inputs[0])
    gLinks.new(color_ramp2.outputs[0], overlay_node2.inputs[1])
    gLinks.new(layer_weight.outputs[1], color_ramp1.inputs[0])
    gLinks.new(layer_weight.outputs[1], color_ramp2.inputs[0])
    gLinks.new(geometry_node.outputs[7], color_ramp3.inputs[0])
    gLinks.new(noise_node1.outputs[0], mix_node2.inputs[0])
    gLinks.new(group_input.outputs[7], mix_node2.inputs[1])
    gLinks.new(group_input.outputs[8], mix_node2.inputs[2])
    gLinks.new(noise_node3.outputs[1], bright_contrast.inputs[0])
    gLinks.new(bright_contrast.outputs[0], overlay_node_main2.inputs[2])
    gLinks.new(group_input.outputs[0], noise_node3.inputs[0])
    gLinks.new(noise_node4.outputs[1], overlay_node_main2.inputs[1])
    gLinks.new(group_input.outputs[0], noise_node4.inputs[0])
    gLinks.new(group_input.outputs[3], noise_node4.inputs[1])
    gLinks.new(multiply_node3.outputs[0], noise_node1.inputs[1])
    gLinks.new(multiply_node3.outputs[0], noise_node2.inputs[1])
    gLinks.new(multiply_node2.outputs[0], noise_node3.inputs[1])
    gLinks.new(group_input.outputs[3], multiply_node3.inputs[0])
    gLinks.new(group_input.outputs[3], multiply_node2.inputs[0])
    links.new(texture_coord.outputs[3], nodes['Group'].inputs[0])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])

    bpy.context.scene.objects.active.active_material = material
    

def create_plastic_material():
    plastic_material = myMaterial("Plastic")
    
    nodes = plastic_material.nodes
    gNodes = plastic_material.gNodes
    plastic_group = plastic_material.mat_group
    material = plastic_material.material
    
    #create input node for group, and its inputs and their default values
    plastic_group.inputs.clear()
    plastic_group.inputs.new("NodeSocketColor", "Diffuse Color")
    plastic_group.inputs.new("NodeSocketColor", "Reflection Color")
    plastic_group.inputs.new("NodeSocketFloatFactor", "Roughness")
    plastic_group.inputs.new("NodeSocketFloatFactor", "Reflection")
    plastic_group.inputs.new("NodeSocketVector", "Normal")
    plastic_group.inputs['Diffuse Color'].default_value = (0.3, 0.5, 0.7, 1)
    plastic_group.inputs['Reflection Color'].default_value = (1, 1, 1, 1)
    plastic_group.inputs['Roughness'].default_value = 0.227
    plastic_group.inputs['Reflection'].default_value = 0.227
    group_input = plastic_group.nodes.new("NodeGroupInput")
    group_input.location = (-200, 0)
    
    #create the output Node for the group
    group_output = plastic_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    plastic_group.outputs.clear()
    plastic_group.outputs.new("NodeSocketShader", "Shader")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = plastic_group
    
    #create nodes
    power_node1 = gNodes.new(type='ShaderNodeMath')
    power_node2 = gNodes.new(type='ShaderNodeMath')
    fresnel_node = gNodes.new(type='ShaderNodeFresnel')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    glossy_node = gNodes.new(type='ShaderNodeBsdfGlossy')
    mix_node = gNodes.new(type='ShaderNodeMixRGB')
    mix_shader = gNodes.new(type='ShaderNodeMixShader')
    material_output = nodes.new('ShaderNodeOutputMaterial')
    geometry_node = gNodes.new(type='ShaderNodeNewGeometry')
    mix_node2 = gNodes.new(type='ShaderNodeMixRGB')
    bump_node = gNodes.new(type='ShaderNodeBump')
    
    
    #modify values
    power_node1.inputs[1].default_value = 2
    power_node2.inputs[1].default_value = 2
    power_node1.operation = 'POWER'
    power_node2.operation = 'POWER'
    mix_node.inputs[2].default_value = (1, 1, 1, 1)
    plastic_group.inputs[2].min_value = 0
    plastic_group.inputs[3].min_value = 0
    plastic_group.inputs[2].max_value = 1
    plastic_group.inputs[3].max_value = 1
    
    
    #create Links
    gLinks = plastic_group.links
    links = material.node_tree.links
    gLinks.new(group_input.outputs[0], diffuse_node.inputs[0])
    gLinks.new(group_input.outputs[1], glossy_node.inputs[0])
    gLinks.new(group_input.outputs[2], power_node1.inputs[0])
    gLinks.new(group_input.outputs[3], power_node2.inputs[0])
    gLinks.new(group_input.outputs[4], bump_node.inputs[3])
    gLinks.new(group_input.outputs[4], diffuse_node.inputs[2])
    gLinks.new(group_input.outputs[4], glossy_node.inputs[2])
    gLinks.new(power_node1.outputs[0], mix_node2.inputs[0])
    gLinks.new(power_node1.outputs[0], glossy_node.inputs[1])
    gLinks.new(power_node1.outputs[0], diffuse_node.inputs[1])
    gLinks.new(power_node2.outputs[0], mix_node.inputs[1])
    gLinks.new(fresnel_node.outputs[0], mix_node.inputs[0])
    gLinks.new(diffuse_node.outputs[0], mix_shader.inputs[1])
    gLinks.new(glossy_node.outputs[0], mix_shader.inputs[2])
    gLinks.new(mix_node.outputs[0], mix_shader.inputs[0])
    gLinks.new(mix_shader.outputs[0], group_output.inputs[0])
    gLinks.new(mix_node2.outputs[0], fresnel_node.inputs[1])
    gLinks.new(bump_node.outputs[0], mix_node2.inputs[1])
    gLinks.new(geometry_node.outputs[0], mix_node2.inputs[2])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])
    
    bpy.context.scene.objects.active.active_material = material
    

class addon_menu(bpy.types.Menu):
    bl_label = "Material Lib"
    bl_idname = "OBJECT_MT_custom_menu"
    
    def draw(self, context):
        layout = self.layout
        mats = bpy.data.materials
        layout.label("Create Materials")
        layout.operator("addmaterial.car")
        layout.operator("addmaterial.concrete")
        layout.operator("addmaterial.dirt")
        layout.operator("addmaterial.fire")
        layout.operator("addmaterial.glass")
        layout.operator("addmaterial.hair")
        layout.operator("addmaterial.image")
        layout.operator("addmaterial.leather")
        layout.operator("addmaterial.light")
        layout.operator("addmaterial.metal")
        layout.operator("addmaterial.mirror")
        layout.operator("addmaterial.plastic")
        layout.operator("addmaterial.rubber")
        layout.operator("addmaterial.sand")
        layout.operator("addmaterial.silk")
        layout.operator("addmaterial.skin")
        layout.operator("addmaterial.sky")
        layout.operator("addmaterial.snow")
        layout.operator("addmaterial.stone")
        layout.operator("addmaterial.wood")

class PanelOne(bpy.types.Panel):
    bl_label = "Materials Library"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Material Library"
    
    def draw(self, context):
        layout = self.layout
        
        if (context.active_object.material_slots.values() == []):
            layout.operator("addmaterial.default")
        elif (bpy.context.scene.objects.active.active_material):
            layout.menu(addon_menu.bl_idname, icon_value=layout.icon(context.object.active_material))
        else:
            layout.operator("addmaterial.default")
    

class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.glass"
    bl_label = "Glass Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_glass_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.stone"
    bl_label = "Stone Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_stone_material()
        return{'FINISHED'}    
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.concrete"
    bl_label = "Concrete Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_concrete_material()
        return{'FINISHED'}    
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.plastic"
    bl_label = "Plastic Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_plastic_material()
        return{'FINISHED'}    
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.skin"
    bl_label = "Skin Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_skin_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.car"
    bl_label = "Car Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_car_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.metal"
    bl_label = "Metal Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_metal_material()
        return{'FINISHED'}    
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.sand"
    bl_label = "Sand Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_sand_material()
        return{'FINISHED'}    
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.rubber"
    bl_label = "Rubber Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_rubber_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.snow"
    bl_label = "Snow Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_snow_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.hair"
    bl_label = "Hair Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_hair_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.wood"
    bl_label = "Wood Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_wood_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.sky"
    bl_label = "Sky Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_sky_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.light"
    bl_label = "Light Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_light_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.fire"
    bl_label = "Fire Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_fire_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.silk"
    bl_label = "Silk Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_silk_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.leather"
    bl_label = "Leather Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_leather_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.mirror"
    bl_label = "Mirror Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_mirror_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.dirt"
    bl_label = "Dirt Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_dirt_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.image"
    bl_label = "Image Material"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        create_image_material()
        return{'FINISHED'}
class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "addmaterial.default"
    bl_label = "Select An Object"

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        if (bpy.data.materials.find("Material") == -1):
            material = bpy.data.materials.new(name="Material")
        else:
            material = bpy.data.materials["Material"]
        bpy.context.scene.objects.active.active_material = material
        return{'FINISHED'}
		
def register():
    bpy.utils.register_module(__name__)
def unregister():
    bpy.utils.unregister_module(__name__)
    
if __name__ == "__main__":
    register()
