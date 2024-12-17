bl_info = {
    "name": "Link Materials to Data or Object",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (4, 3, 1),
    "location": "Ctrl+L > Link/Transfer Data",
    "description": "Link materials of selected objects to data or object",
    "category": "Object",
}

import bpy


class OBJECT_OT_link_materials_data_or_object(bpy.types.Operator):
    """Link Materials to Data or Object"""
    bl_idname = "object.link_materials_data_or_object"
    bl_label = "Link Materials to Data or Object"
    bl_options = {'REGISTER', 'UNDO'}
    
    link_to: bpy.props.EnumProperty(
        name="Link To",
        description="Link materials to",
        items=[
            ('DATA', "Data", "Useful for keeping instances in sync"),
            ('OBJECT', "Object", "Useful for making instances unique"),
        ],
        default='DATA'
    )
    
    @classmethod
    def poll(cls, context):
        return context.active_object
    
    def execute(self, context):
        initial_active_object = bpy.context.active_object  # Store active object
        for obj in bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = obj  # Iterate through selected objects
            for mat_slot in obj.material_slots:
                mat = mat_slot.material
                mat_slot.link = self.link_to
                mat_slot.material = mat
        bpy.context.view_layer.objects.active = initial_active_object  # Restore active object
        
        self.report({'INFO'}, "Completed.")        
        return {'FINISHED'}


# Add the operator to the Link/Transfer Data menu (Ctrl+L)
def link_transfer_menu_func(self, context):
    self.layout.operator(OBJECT_OT_link_materials_data_or_object.bl_idname, text="Link Materials to Data/Object")


_classes = (
    OBJECT_OT_link_materials_data_or_object,
)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)
    
    # Append to Link/Transfer Data menu
    bpy.types.VIEW3D_MT_make_links.append(link_transfer_menu_func)


def unregister():
    # Remove from Link/Transfer Data menu
    bpy.types.VIEW3D_MT_make_links.remove(link_transfer_menu_func)
    
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()