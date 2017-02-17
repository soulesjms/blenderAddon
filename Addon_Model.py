import bpy
import pdb

scene = bpy.context.scene
scene.render.engine = 'CYCLES'

def create_stone_material():
    #create a material with a name
    if bpy.data.materials.find('Stone Material') == -1:
        material = bpy.data.materials.new(name="Stone Material")
    else:
        material = bpy.data.materials["Stone Material"]
    
    #start using nodes
    material.use_nodes = True
    stone_nodes = material.node_tree.nodes

	#clear nodes
    for node in stone_nodes:
        stone_nodes.remove(node)

    #create nodes
    texture_coord = stone_nodes.new(type='ShaderNodeTexCoord')
    musgrave_texture = stone_nodes.new(type='ShaderNodeTexMusgrave')
    wave_texture = stone_nodes.new(type='ShaderNodeTexWave')
    diffuse = stone_nodes.new(type='ShaderNodeBsdfDiffuse')
    multiply = stone_nodes.new(type='ShaderNodeMath')
    node_output = stone_nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = 400,0
    
    #change node default values
    musgrave_texture.inputs[1].default_value = 2.256
    wave_texture.inputs[1].default_value = 0.208
    wave_texture.inputs[3].default_value =4.654
    wave_texture.inputs[4].default_value =4.048
    wave_texture.wave_profile = 'SAW'
    diffuse.inputs[1].default_value = 0.278
    multiply.operation = 'MULTIPLY'
    multiply.inputs[1].default_value = 5
    

    #link nodes
    links = material.node_tree.links
    links.new(texture_coord.outputs[0], wave_texture.inputs[0])
    links.new(texture_coord.outputs[3], musgrave_texture.inputs[0])
    links.new(musgrave_texture.outputs[1], wave_texture.inputs[2])
    links.new(wave_texture.outputs[0], diffuse.inputs[0])
    links.new(diffuse.outputs[0], node_output.inputs[0])
    links.new(wave_texture.outputs[1], multiply.inputs[0])
    links.new(multiply.outputs[0], node_output.inputs[2])

    bpy.context.scene.objects.active.active_material = material
    

def create_metal_material():
    #create material if it doesn't exist 
    if bpy.data.materials.find('Metal Material') == -1:
        material = bpy.data.materials.new(name="Metal Material")
    else:
        material = bpy.data.materials["Metal Material"]
    
    #create node group and name it and check if it's already made
    if bpy.data.node_groups.find('metalGroup') == -1:
        metal_group = bpy.data.node_groups.new(name='metalGroup', type='ShaderNodeTree')
    else:
        metal_group = bpy.data.node_groups['metalGroup']
    
    #use nodes
    material.use_nodes = True
    
	#set variables for nodes. gNodes for group nodes, nodes for material nodes
    gNodes = metal_group.nodes
    nodes = material.node_tree.nodes
    
    #clear all nodes if there are any for a clean slate
    for node in gNodes:
        gNodes.remove(node)
    for node in nodes:
        nodes.remove(node)
	
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
    #create material if it doesn't exist 
    if bpy.data.materials.find('Car Material') == -1:
        material = bpy.data.materials.new(name="Car Material")
    else:
        material = bpy.data.materials["Car Material"]
    
    #create node group if it doesn't exist
    if bpy.data.node_groups.find('carNodeGroup') == -1:
        car_node_group = bpy.data.node_groups.new(name='carNodeGroup', type='ShaderNodeTree')
    else:
        car_node_group = bpy.data.node_groups['carNodeGroup']
    
    #use nodes
    material.use_nodes = True
    
    #set variables for nodes. gNodes for group nodes, nodes for material nodes
    gNodes = car_node_group.nodes
    nodes = material.node_tree.nodes
    
    #clear all nodes if there are any for a clean slate
    for node in gNodes:
        gNodes.remove(node)
    for node in nodes:
        nodes.remove(node)
    
    #create input node
    car_node_group.inputs.clear()
    car_node_group.inputs.new('NodeSocketColor', "Car Color")
    car_node_group.inputs['Car Color'].default_value = (0.5, 0, 0, 1)

    group_input = car_node_group.nodes.new("NodeGroupInput")
    group_input.outputs.new('RGBA', "Color")
    group_input.location = (-500, 0)    
    
	#create output node for the group
    car_node_group.outputs.clear()
    car_node_group.outputs.new("NodeSocketShader", "Out")
        
    group_output = car_node_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
        
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = car_node_group
        
    #create nodes
    glossy_node = gNodes.new(type='ShaderNodeBsdfGlossy')    
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')    
    layer_weight = gNodes.new(type='ShaderNodeLayerWeight')
    RGB_mix_node = gNodes.new(type='ShaderNodeMixRGB')
    mix_shader = gNodes.new(type='ShaderNodeMixShader')
    material_output = nodes.new(type='ShaderNodeOutputMaterial')

    #modify node default values
    glossy_node.inputs[1].default_value = 0.010
    glossy_node.distribution = 'BECKMANN'
    diffuse_node.inputs[1].default_value = 0.584
    layer_weight.inputs[0].default_value = 0.7
    RGB_mix_node.inputs[0].default_value = 0.150
    
    #create links between nodes
    gLinks = car_node_group.links
    links = material.node_tree.links
    gLinks.new(layer_weight.outputs[0], mix_shader.inputs[0])
    gLinks.new(diffuse_node.outputs[0], mix_shader.inputs[1])
    gLinks.new(glossy_node.outputs[0], mix_shader.inputs[2])
    gLinks.new(RGB_mix_node.outputs[0], glossy_node.inputs[0])
    gLinks.new(group_input.outputs[0], RGB_mix_node.inputs[1])
    gLinks.new(group_input.outputs[0], diffuse_node.inputs[0])
    gLinks.new(mix_shader.outputs[0], group_output.inputs[0])
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
    #create material if it doesn't exist 
    if bpy.data.materials.find('Sand Material') == -1:
        material = bpy.data.materials.new(name="Sand Material")
    else:
        material = bpy.data.materials["Sand Material"]
    
    #create node group and name it and check if it's already made
    if bpy.data.node_groups.find('sandGroup') == -1:
        sand_group = bpy.data.node_groups.new(name='sandGroup', type='ShaderNodeTree')
    else:
        sand_group = bpy.data.node_groups['sandGroup']
    
    #use nodes
    material.use_nodes = True
    
	#set variables for nodes. gNodes for group nodes, nodes for material nodes
    gNodes = sand_group.nodes
    nodes = material.node_tree.nodes
    
    #clear all nodes if there are any for a clean slate
    for node in gNodes:
        gNodes.remove(node)
    for node in nodes:
        nodes.remove(node)
        
    #create input node for group, and its inputs and their default values
    sand_group.inputs.clear()
    sand_group.inputs.new("NodeSocketFloat", "Scale")
    sand_group.inputs['Scale'].default_value = 15.100
    sand_group.inputs.new("NodeSocketFloat", "Detail")
    sand_group.inputs['Detail'].default_value = 11.400
    sand_group.inputs.new("NodeSocketFloat", "Distortion")
    sand_group.inputs['Distortion'].default_value = 5.000
    sand_group.inputs.new("NodeSocketFloat", "Circular/Stripe")
    sand_group.inputs['Circular/Stripe'].default_value = 0.500
    sand_group.inputs.new("NodeSocketColor", "Sand Color")
    sand_group.inputs['Sand Color'].default_value = (0.561, 0.439, 0.261, 1)
    sand_group.inputs.new("NodeSocketFloat", "Depth")
    sand_group.inputs['Depth'].default_value = 6.250
    group_input = sand_group.nodes.new("NodeGroupInput")
    
    #create the output Node for the group
    group_output = sand_group.nodes.new("NodeGroupOutput")
    group_output.location = (200, 0)
    sand_group.outputs.clear()
    sand_group.outputs.new("NodeSocketShader", "Shader")
    sand_group.outputs.new("NodeSocketFloat", "Bump")
    
    tree = material.node_tree
    group_node = tree.nodes.new("ShaderNodeGroup")
    group_node.node_tree = sand_group
    
    #create nodes
    texture_coord = gNodes.new(type='ShaderNodeTexCoord')
    normal_node = gNodes.new(type='ShaderNodeNormal')
    mix_node = gNodes.new(type='ShaderNodeMixRGB')
    noise_node = gNodes.new(type='ShaderNodeTexNoise')
    diffuse_node = gNodes.new(type='ShaderNodeBsdfDiffuse')
    multiply_node = gNodes.new(type='ShaderNodeMath')
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    
    #modify node default values
    multiply_node.operation = 'MULTIPLY'
    diffuse_node.inputs[1].default_value = 0
    normal_node.outputs[0].default_value = (0.220, 0.110, 0.969)
    
    #create link between nodes
    gLinks = sand_group.links
    links = material.node_tree.links
    gLinks.new(group_input.outputs[0], noise_node.inputs[1])
    gLinks.new(group_input.outputs[1], noise_node.inputs[2])
    gLinks.new(group_input.outputs[2], noise_node.inputs[3])
    gLinks.new(group_input.outputs[3], mix_node.inputs[0])
    gLinks.new(group_input.outputs[4], diffuse_node.inputs[0])
    gLinks.new(group_input.outputs[5], multiply_node.inputs[1])
    gLinks.new(texture_coord.outputs[0], normal_node.inputs[0])
    gLinks.new(texture_coord.outputs[0], mix_node.inputs[2])
    gLinks.new(normal_node.outputs[1], mix_node.inputs[1])
    gLinks.new(mix_node.outputs[0], noise_node.inputs[0])
    gLinks.new(noise_node.outputs[0], multiply_node.inputs[0])
    gLinks.new(multiply_node.outputs[0], group_output.inputs[1])
    gLinks.new(diffuse_node.outputs[0], group_output.inputs[0])
    links.new(nodes['Group'].outputs[0], material_output.inputs[0])
    links.new(nodes['Group'].outputs[1], material_output.inputs[2])
    
    bpy.context.scene.objects.active.active_material = material
    
#def add_icon(layout):
#    layout.operator(addmaterial.glass.bl_idname, icon='UGLYPACKAGE')
    
    
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
    
##########################################################
# BEGIN MAIN
##########################################################
#create_car_material()
#create_metal_material()
#create_stone_material()
#create_skin_material()
#create_glass_material()
#create_image_material()
#create_sand_material()
#create_rubber_material()
#create_snow_material()
