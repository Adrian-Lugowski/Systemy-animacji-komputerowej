import bpy
import math
import os
import random

TYPY_ROSLIN = {
    "drzewo": {
        "wysokosc": (3.0, 5.0),  # zakres (min, max) dla random.uniform()
        "liczba_lisci": (4, 6),
        "promien_lisci": (0.4, 0.7),
        "liczba_korzeni": (4, 6),
        "kolor_lodygi": (0.15, 0.08, 0.02, 1),  # ciemny brąz
        "kolor_lisci": (0.05, 0.35, 0.1, 1),  # ciemna zieleń
    },
    "krzew": {
        "wysokosc": (0.8, 1.8),
        "liczba_lisci": (5, 8),
        "promien_lisci": (0.5, 0.9),
        "liczba_korzeni": (2, 4),
        "kolor_lodygi": (0.25, 0.15, 0.05, 1),  # jasny brąz
        "kolor_lisci": (0.1, 0.5, 0.05, 1),  # żywa zieleń
    },
    "paproc": {
        "wysokosc": (0.5, 1.2),
        "liczba_lisci": (6, 10),
        "promien_lisci": (0.6, 1.0),
        "liczba_korzeni": (2, 3),
        "kolor_lodygi": (0.2, 0.3, 0.1, 1),  # oliwkowy
        "kolor_lisci": (0.0, 0.6, 0.15, 1),  # soczysty zielony
    },
}


def wyczysc_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    for collection in bpy.data.collections:
        if collection.name.startswith("Las"):
            bpy.data.collections.remove(collection)


def utworz_materialy(typy):
    mat_lodyga = bpy.data.materials.new(name="Lodyga")
    mat_lodyga.use_nodes = True
    bsdf_lodyga = mat_lodyga.node_tree.nodes["Principled BSDF"]
    bsdf_lodyga.inputs["Base Color"].default_value = typy["kolor_lodygi"]
    bsdf_lodyga.inputs["Metallic"].default_value = 0.8
    bsdf_lodyga.inputs["Roughness"].default_value = 0.3

    mat_lisc = bpy.data.materials.new(name="Lisc")
    mat_lisc.use_nodes = True
    bsdf_lisc = mat_lisc.node_tree.nodes["Principled BSDF"]
    bsdf_lisc.inputs["Base Color"].default_value = typy["kolor_lisci"]
    bsdf_lisc.inputs["Metallic"].default_value = 0.6
    bsdf_lisc.inputs["Roughness"].default_value = 0.2

    return mat_lodyga, mat_lisc


def stworz_rosline(wysokosc=2.0, liczba_lisci=3, promien_lisci=0.3, liczba_korzeni=4, przesuniecie_x=0.0,
                   przesuniecie_y=0.0, typy=TYPY_ROSLIN["drzewo"]):
    mat_lodyga, mat_lisc = utworz_materialy(typy)
    obiekty = []

    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.1,
        depth=1.0,
        location=(przesuniecie_x, przesuniecie_y, wysokosc / 2)
    )
    lodyga = bpy.context.active_object
    lodyga.scale.z = wysokosc
    lodyga.name = "Lodyga"
    lodyga.data.materials.append(mat_lodyga)
    obiekty.append(lodyga)

    wysokosc_lisci = wysokosc * 0.9
    for i in range(liczba_lisci):
        kat = (i / liczba_lisci) * 2 * math.pi
        odleglosc = 0.15
        x = przesuniecie_x + math.cos(kat) * odleglosc
        y = przesuniecie_y + math.sin(kat) * odleglosc

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, wysokosc_lisci))
        lisc = bpy.context.active_object
        lisc.name = f"Lisc_{i}"
        lisc.scale = (promien_lisci, promien_lisci / 2, 0.05)
        lisc.rotation_euler = (0, math.radians(40), kat)
        lisc.data.materials.append(mat_lisc)
        obiekty.append(lisc)

    for i in range(liczba_korzeni):
        kat = (i / liczba_korzeni) * 2 * math.pi
        odleglosc = 0.12
        x = przesuniecie_x + math.cos(kat) * odleglosc
        y = przesuniecie_y + math.sin(kat) * odleglosc

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, 0.1))
        korzen = bpy.context.active_object
        korzen.name = f"Korzen_{i}"
        korzen.scale = (0.3, 0.1, 0.1)
        korzen.rotation_euler = (0, math.radians(-30), kat)
        korzen.data.materials.append(mat_lodyga)
        obiekty.append(korzen)

    return obiekty


def stworz_rosline_typ(x, z, typ_nazwy):
    typ = TYPY_ROSLIN[typ_nazwy]

    wysokosc_typ = random.uniform(*typ["wysokosc"])
    liczba_typ = random.randint(*typ["liczba_lisci"])
    promien_typ = random.uniform(*typ["promien_lisci"])
    korzenie_typ = random.randint(*typ["liczba_korzeni"])

    return stworz_rosline(
        wysokosc=wysokosc_typ,
        liczba_lisci=liczba_typ,
        promien_lisci=promien_typ,
        liczba_korzeni=korzenie_typ,
        przesuniecie_x=x,
        przesuniecie_y=z,
        typy=typ
    )


def wybierz_typ_biomu(x, z, rozmiar_pola):
    max_promien = rozmiar_pola / 2.0
    odleglosc = max(abs(x), abs(z))

    if odleglosc < 0.3 * max_promien:
        return "drzewo"
    elif odleglosc <= 0.7 * max_promien:
        if random.random() < 0.7:
            return "krzew"
        else:
            return "drzewo"
    else:
        if random.random() < 0.5:
            return "paproc"
        else:
            return "krzew"


def generuj_las(liczba_roslin=18, rozmiar_pola=10.0, seed=42):
    wyczysc_scene()
    random.seed(seed)

    kolekcja_glowna = bpy.data.collections.new("Las")
    bpy.context.scene.collection.children.link(kolekcja_glowna)

    podkolekcje = {}
    for nazwa_typu in TYPY_ROSLIN.keys():
        podkolekcja = bpy.data.collections.new(f"Las/{nazwa_typu.capitalize()}")
        kolekcja_glowna.children.link(podkolekcja)
        podkolekcje[nazwa_typu] = podkolekcja

    for i in range(liczba_roslin):
        x = random.uniform(-rozmiar_pola / 2, rozmiar_pola / 2)
        z = random.uniform(-rozmiar_pola / 2, rozmiar_pola / 2)

        typ = wybierz_typ_biomu(x, z, rozmiar_pola)
        obiekty_rosliny = stworz_rosline_typ(x, z, typ)

        for obj in obiekty_rosliny:
            for col in obj.users_collection:
                col.objects.unlink(obj)
            podkolekcje[typ].objects.link(obj)


generuj_las(liczba_roslin=30, rozmiar_pola=12.0, seed=37)

bpy.ops.mesh.primitive_plane_add(size=14.0, location=(0, 0, 0))
podloze = bpy.context.active_object
mat_podloze = bpy.data.materials.new(name="Mat_Ziemia")
mat_podloze.use_nodes = True
mat_podloze.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.08, 0.02, 1)
podloze.data.materials.append(mat_podloze)

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=20)
bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.modifier_add(type='DISPLACE')
mod_displace = podloze.modifiers["Displace"]
tex_podloze = bpy.data.textures.new("Tex_Ziemia", type='CLOUDS')
tex_podloze.noise_scale = 3.0
mod_displace.texture = tex_podloze
mod_displace.strength = 0.3

bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
slonce = bpy.context.active_object
slonce.rotation_euler = (math.radians(60), 0, math.radians(45))
slonce.data.energy = 3.0

bpy.ops.object.camera_add(location=(0, -18, 7))
kamera = bpy.context.active_object
kamera.rotation_euler = (math.radians(70), 0, 0)
bpy.context.scene.camera = kamera

scene = bpy.context.scene
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()

output_path = os.path.join(script_dir, "//las_05.png")

scene.render.filepath = output_path
scene.render.image_settings.file_format = 'PNG'
scene.render.resolution_x = 1200
scene.render.resolution_y = 800

bpy.ops.render.render(write_still=True)