import bpy
import math
import os


def wyczysc_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


def utworz_materialy():
    mat_lodyga = bpy.data.materials.new(name="Lodyga")
    mat_lodyga.use_nodes = True
    bsdf_lodyga = mat_lodyga.node_tree.nodes["Principled BSDF"]
    bsdf_lodyga.inputs["Base Color"].default_value = (0.4, 0.25, 0.1, 1.0)
    bsdf_lodyga.inputs["Metallic"].default_value = 0.8
    bsdf_lodyga.inputs["Roughness"].default_value = 0.3

    mat_lisc = bpy.data.materials.new(name="Lisc")
    mat_lisc.use_nodes = True
    bsdf_lisc = mat_lisc.node_tree.nodes["Principled BSDF"]
    bsdf_lisc.inputs["Base Color"].default_value = (0.0, 0.8, 0.5, 1.0)
    bsdf_lisc.inputs["Metallic"].default_value = 0.6
    bsdf_lisc.inputs["Roughness"].default_value = 0.2
    bsdf_lisc.inputs["Emission Color"].default_value = (0.0, 1.0, 0.5, 1.0)
    bsdf_lisc.inputs["Emission Strength"].default_value = 1.5

    return mat_lodyga, mat_lisc


def stworz_rosline(wysokosc=2.0, liczba_lisci=3, promien_lisci=0.3, liczba_korzeni=4, przesuniecie_x=0.0):
    mat_lodyga, mat_lisc = utworz_materialy()

    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.1,
        depth=1.0,
        location=(przesuniecie_x, 0, wysokosc / 2)
    )
    lodyga = bpy.context.active_object
    lodyga.scale.z = wysokosc
    lodyga.name = "Lodyga"
    lodyga.data.materials.append(mat_lodyga)

    wysokosc_lisci = wysokosc * 0.9
    for i in range(liczba_lisci):
        kat = (i / liczba_lisci) * 2 * math.pi
        odleglosc = 0.15
        x = przesuniecie_x + math.cos(kat) * odleglosc
        y = math.sin(kat) * odleglosc

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, wysokosc_lisci))
        lisc = bpy.context.active_object
        lisc.name = f"Lisc_{i}"

        lisc.scale = (promien_lisci, promien_lisci / 2, 0.05)

        lisc.rotation_euler = (0, math.radians(40), kat)
        lisc.data.materials.append(mat_lisc)

    for i in range(liczba_korzeni):
        kat = (i / liczba_korzeni) * 2 * math.pi
        odleglosc = 0.12
        x = przesuniecie_x + math.cos(kat) * odleglosc
        y = math.sin(kat) * odleglosc

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, 0.1))
        korzen = bpy.context.active_object
        korzen.name = f"Korzen_{i}"

        korzen.scale = (0.3, 0.1, 0.1)
        korzen.rotation_euler = (0, math.radians(-30), kat)
        korzen.data.materials.append(mat_lodyga)


wyczysc_scene()

stworz_rosline(wysokosc=1.5, liczba_lisci=3, promien_lisci=0.4, liczba_korzeni=4, przesuniecie_x=-3.0)
stworz_rosline(wysokosc=2.5, liczba_lisci=5, promien_lisci=0.6, liczba_korzeni=6, przesuniecie_x=0.0)
stworz_rosline(wysokosc=3.5, liczba_lisci=4, promien_lisci=0.8, liczba_korzeni=8, przesuniecie_x=3.0)

bpy.ops.mesh.primitive_plane_add(size=12.0, location=(0, 0, 0))

bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
slonce = bpy.context.active_object
slonce.rotation_euler = (math.radians(60), 0, math.radians(45))
slonce.data.energy = 3.0

bpy.ops.object.camera_add(location=(0, -10, 3))
kamera = bpy.context.active_object
kamera.rotation_euler = (math.radians(80), 0, 0)
bpy.context.scene.camera = kamera

scene = bpy.context.scene
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()

output_path = os.path.join(script_dir, "//lab_04.png")

scene.render.filepath = output_path
scene.render.image_settings.file_format = 'PNG'
scene.render.resolution_x = 800
scene.render.resolution_y = 600

bpy.ops.render.render(write_still=True)
print(f"Render zapisany pod ścieżką: {output_path}")