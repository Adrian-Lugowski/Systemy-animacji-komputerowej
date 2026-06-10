import bpy
import random

NAZWA_MATERIALU = "Latarnia_Emission"
ZAKRES_KLATEK = 150
SILA_BAZOWA = 2.0
SILA_ROZBLYSKU = 35.0
CZESTOTLIWOSC = 3

def animuj_migotanie():
    mat = bpy.data.materials.get(NAZWA_MATERIALU)
    if not mat or not mat.use_nodes:
        print("Brak materiału.")
        return

    docelowy_wezel = None
    nazwa_wejscia = ""
    
    for node in mat.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            docelowy_wezel = node
            nazwa_wejscia = "Emission Strength"
            break
        elif node.type == 'EMISSION':
            docelowy_wezel = node
            nazwa_wejscia = "Strength"
            break
            
    if not docelowy_wezel:
        print("Błąd: Nie znaleziono odpowiedniego węzła dla emisji.")
        return

    if mat.node_tree.animation_data:
        mat.node_tree.animation_data_clear()

    for klatka in range(1, ZAKRES_KLATEK + 1, CZESTOTLIWOSC):
        sila = random.uniform(SILA_BAZOWA, SILA_ROZBLYSKU)
        
        docelowy_wezel.inputs[nazwa_wejscia].default_value = sila
        docelowy_wezel.inputs[nazwa_wejscia].keyframe_insert(data_path="default_value", frame=klatka)

animuj_migotanie()