import bpy
import math
import os

SCIEZKA_LAB07 = r"C:\Users\Ampio\Desktop\SAK\lab7\lab_07.blend"
NAZWA_KOLEKCJI = "Roslina_Hero"

KLATKA_START = 1
KLATKA_KONIEC = 125
FPS = 25


def wyczysc_animacje(obj):
    if obj.animation_data and obj.animation_data.action:
        obj.animation_data.action = None


def importuj_rosline(sciezka_blend, nazwa_kolekcji):
    sciezka_kolekcji = os.path.join(sciezka_blend, "Collection", nazwa_kolekcji)
    bpy.ops.wm.append(
        filepath=sciezka_kolekcji,
        directory=os.path.join(sciezka_blend, "Collection"),
        filename=nazwa_kolekcji,
    )


def animuj_lisc(obj, faza, czestosc=0.05, amplituda=0.3, klatka_start=1, klatka_koniec=125):
    wyczysc_animacje(obj)
    rotacja_bazowa_y = obj.rotation_euler[1]

    for klatka in range(klatka_start, klatka_koniec + 1):
        kat = rotacja_bazowa_y + amplituda * math.sin(klatka * czestosc + faza)
        obj.rotation_euler[1] = kat
        obj.keyframe_insert(data_path="rotation_euler", frame=klatka, index=1)


def animuj_wszystkie_liscie(prefix_nazwy="RoslinaLisc"):
    liscie = [obj for obj in bpy.data.objects if obj.name.startswith(prefix_nazwy)]

    for i, lisc in enumerate(liscie):
        faza_lisc = i * (2 * math.pi / max(len(liscie), 1))
        animuj_lisc(lisc, faza=faza_lisc, klatka_start=KLATKA_START, klatka_koniec=KLATKA_KONIEC)


def animuj_pak(nazwa_obj="Roslina_Pak", klatka_start=30, klatka_koniec=90):
    obj = bpy.data.objects.get(nazwa_obj)

    wyczysc_animacje(obj)

    skala_max = 0.2
    skala_min = 0.02

    obj.scale = (skala_min, skala_min, skala_min)
    obj.keyframe_insert(data_path="scale", frame=KLATKA_START)
    obj.keyframe_insert(data_path="scale", frame=klatka_start)

    obj.scale = (skala_max, skala_max, skala_max)
    obj.keyframe_insert(data_path="scale", frame=klatka_koniec)
    obj.keyframe_insert(data_path="scale", frame=KLATKA_KONIEC)


def ustaw_scene():
    bpy.context.scene.frame_start = KLATKA_START
    bpy.context.scene.frame_end = KLATKA_KONIEC
    bpy.context.scene.render.fps = FPS


if __name__ == "__main__" or True:
    ustaw_scene()

    if NAZWA_KOLEKCJI not in bpy.data.collections:
        try:
            importuj_rosline(SCIEZKA_LAB07, NAZWA_KOLEKCJI)
            print("Zaimportowano kolekcję rośliny.")
        except Exception as e:
            print(f"Błąd importu")

    animuj_wszystkie_liscie(prefix_nazwy="RoslinaLisc")
    animuj_pak()