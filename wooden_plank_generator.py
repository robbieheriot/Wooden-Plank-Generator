bl_info = {
    "name": "Wooden Plank Generator",
    "blender": (2, 80, 0),
    "category": "Mesh",
}

import bpy


#Make Texture
tex = bpy.data.textures.new("WoodTexture", 'CLOUDS')
tex.noise_scale = 1.25
tex.noise_depth = 8



# Create a new material
material_name = "Wood Materail"
material = bpy.data.materials.new(name=material_name)


# Clear default nodes
material.use_nodes = True
nodes = material.node_tree.nodes
for node in nodes:
    nodes.remove(node)

# Create Texture Coordinate node
tex_coord_node = nodes.new(type='ShaderNodeTexCoord')
tex_coord_node.location = (0, 0)

# Create Mapping node (first one)
mapping_node_1 = nodes.new(type='ShaderNodeMapping')
mapping_node_1.location = (200, 0)
material.node_tree.links.new(tex_coord_node.outputs["Object"], mapping_node_1.inputs[0])

# Create Mapping node (second one)
mapping_node_2 = nodes.new(type='ShaderNodeMapping')
mapping_node_2.location = (400, 0)

# Connect nodes
material.node_tree.links.new(mapping_node_1.outputs["Vector"], mapping_node_2.inputs[0])

# Set scale using the input socket
mapping_node_2.inputs["Scale"].default_value = (1, 0.350, 0.45)

# Create Noise Texture node
noise_texture_node = nodes.new(type='ShaderNodeTexNoise')
noise_texture_node.location = (600, 0)
noise_texture_node.inputs["Scale"].default_value = 3
noise_texture_node.inputs["Detail"].default_value = 15
noise_texture_node.inputs["Roughness"].default_value = 0.6
noise_texture_node.inputs["Distortion"].default_value = 0.9

# Connect nodes
material.node_tree.links.new(mapping_node_2.outputs["Vector"], noise_texture_node.inputs["Vector"])

# Create Magic Texture node
magic_texture_node = nodes.new(type='ShaderNodeTexMagic')
magic_texture_node.turbulence_depth = (10)
magic_texture_node.location = (800, 0)

# Connect nodes
material.node_tree.links.new(noise_texture_node.outputs["Color"], magic_texture_node.inputs["Vector"])

# Create Color Ramp node
color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
color_ramp_node.location = (1000, 0)
color_ramp_node.color_ramp.interpolation = 'LINEAR'

color_ramp_node.color_ramp.elements[0].color = (0.0512781, 0.0295555, 0.0168062, 1)
color_ramp_node.color_ramp.elements[0].position = (0.582)

color_ramp_node.color_ramp.elements[1].color = (0.412612, 0.212221, 0.127429, 1)
color_ramp_node.color_ramp.elements[1].position = (0.818)

    

# Connect nodes
material.node_tree.links.new(magic_texture_node.outputs["Fac"], color_ramp_node.inputs["Fac"])

# Create Principled BSDF node
principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
principled_node.location = (2000, 0)

# Connect nodes
material.node_tree.links.new(color_ramp_node.outputs["Color"], principled_node.inputs["Base Color"])

# Create Material Output node
material_output_node = nodes.new(type='ShaderNodeOutputMaterial')
material_output_node.location = (2400, 0)

# Connect nodes
material.node_tree.links.new(principled_node.outputs["BSDF"], material_output_node.inputs["Surface"])


# Create Second Noise Texture node
noise_texture_node1 = nodes.new(type='ShaderNodeTexNoise')
noise_texture_node1.location = (600,-600)
noise_texture_node1.inputs["Scale"].default_value = 1.6
noise_texture_node1.inputs["Detail"].default_value = 15
noise_texture_node1.inputs["Roughness"].default_value = 0.6
noise_texture_node1.inputs["Lacunarity"].default_value = 60
noise_texture_node1.inputs["Distortion"].default_value = 13

# Connect nodes
material.node_tree.links.new(mapping_node_2.outputs["Vector"], noise_texture_node1.inputs["Vector"])


#create bump
bump_node=nodes.new(type="ShaderNodeBump")
bump_node.location = (800,-600)
bump_node.inputs["Strength"].default_value = 0.36
bump_node.inputs["Distance"].default_value = 1

# Connect nodes
material.node_tree.links.new(noise_texture_node1.outputs["Fac"],bump_node.inputs["Height"])


#create second bump
bump_node2=nodes.new(type="ShaderNodeBump")
bump_node2.location = (1400,-600)
bump_node2.inputs["Strength"].default_value = 0.4
bump_node2.inputs["Distance"].default_value = 1

# Connect nodes
material.node_tree.links.new(bump_node.outputs["Normal"],bump_node2.inputs["Normal"])
material.node_tree.links.new(color_ramp_node.outputs["Color"],bump_node2.inputs["Height"])
material.node_tree.links.new(bump_node2.outputs["Normal"],principled_node.inputs["Normal"])


# Create second Color Ramp node
color_ramp_node2 = nodes.new(type='ShaderNodeValToRGB')
color_ramp_node2.location = (1400, -300)
color_ramp_node2.color_ramp.interpolation = 'LINEAR'

color_ramp_node2.color_ramp.elements[0].color = (0.317, 0.317, 0.317, 1)
color_ramp_node2.color_ramp.elements[0].position = (0)

color_ramp_node2.color_ramp.elements[1].color = (1, 1, 1, 1)
color_ramp_node2.color_ramp.elements[1].position = (1)

# Connect nodes
material.node_tree.links.new(color_ramp_node.outputs["Color"],color_ramp_node2.inputs["Fac"])
material.node_tree.links.new(color_ramp_node2.outputs["Color"], principled_node.inputs["Roughness"])



class OBJECT_OT_add_wooden_plank(bpy.types.Operator):
    bl_idname = "mesh.primitive_wooden_plank_add"
    bl_label = "Wooden Plank"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
        wooden_plank = bpy.context.active_object
        wooden_plank.name = "Wooden Plank"
        wooden_plank.dimensions = (0.25, 1.25, 0.05)
        bpy.context.object.data.materials.append(material)
        bpy.context.view_layer.objects.active.material_slots[0].material = material
        
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(scale=True)

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.bevel(offset=0.00734234, offset_pct=0, affect='EDGES')


        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].levels = 4



        # Link the texture to the Displace modifiers
        displace_modifier_name = "MyDisplaceModifier"
        displace_modifier = bpy.context.active_object.modifiers.new(name=displace_modifier_name, type='DISPLACE')
        displace_modifier.strength = 1  # Adjust strength as needed
        displace_modifier.direction = 'Y'
        displace_modifier.texture = bpy.data.textures['WoodTexture']

        # Link the texture to the Displace modifiers
        displace_modifier_name = "MyDisplaceModifier2"
        displace_modifier = bpy.context.active_object.modifiers.new(name=displace_modifier_name, type='DISPLACE')
        displace_modifier.strength = 0.1 # Adjust strength as needed
        displace_modifier.direction = 'X'
        displace_modifier.texture = bpy.data.textures['WoodTexture']


        bpy.ops.object.shade_smooth()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_add_wooden_plank.bl_idname, icon='MESH_CUBE')


def register():
    bpy.utils.register_class(OBJECT_OT_add_wooden_plank)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_wooden_plank)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()












