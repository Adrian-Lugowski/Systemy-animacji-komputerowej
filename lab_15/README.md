# Projekt Końcowy — Miasto Nocą
**Przedmiot:** Systemy Animacji Komputerowej  
**Autor:** Adrian Ługowski  

## 1. Opis sceny
Animacja POV przedstawiająca nocny spacer przez deszczowe miasto. Celem było stworzenie mrocznego, neo-noirowego klimatu opartego na kontraście ciemnych ulic i jasnych neonów.

Kluczowe elementy projektu:
* **Mokra nawierzchnia:** Użycie materiałów PBR (mapy chropowatości i normalnych) do uzyskania realistycznych kałuż i odbić światła na asfalcie.
* **Ruch kamery:** Proceduralna symulacja ludzkiego chodu wygenerowana za pomocą modyfikatora *Noise*, bez użycia ręcznych klatek kluczowych.
* **Żywa ulica:** Dwa przejeżdżające samochody z fizycznymi światłami (*Spot*), które oświetlają drogę i przecinają padający deszcz.

## 2. Uruchomienie i renderowanie
1. Sklonuj repozytorium (wymagane zainstalowane rozszerzenie **Git LFS**).
2. Otwórz plik `assets/scena.blend`.
3. Skrypt sterujący znajduje się w `src/animacja.py`.
4. Renderowanie wideo: Ustaw silnik na **Cycles** (urządzenie: GPU Compute) i wciśnij `Ctrl + F12`. Plik zapisze się w ścieżce `renders/miasto_nocą.mp4`. Jeśli urządzenie nie ta rady to trzeba zmienić na **EEVEE**.

# 3. Skrypt Python (animacja.py)
Skrypt proceduralnie generuje efekt uszkodzonego, migoczącego neonu. Automatycznie modyfikuje parametry materiału i wstawia losowe klatki kluczowe na osi czasu.

Główne zmienne sterujące:
* `NAZWA_MATERIALU` – docelowy materiał przypisany do neonu.
* `ZAKRES_KLATEK` – czas trwania animacji.
* `SILA_BAZOWA` i `SILA_ROZBLYSKU` – minimalna i maksymalna moc emitowanego światła.
* `CZESTOTLIWOSC` – gęstość występowania rozbłysków.

## 4. Opcje zaawansowane
* **Motion Blur:** Rozmycie wektorowe tworzy smugi z padającego deszczu oraz świateł poruszających się aut.
* **Light Paths:** Zwiększone limity odbić, aby światło realistycznie i wielokrotnie odbijało się od kałuż i szyb.

## 5. Lista użytych assetów zewnętrznych
| Typ zasobu | Nazwa assetu | Źródło / Adres URL | Licencja |
| :--- | :--- | :--- | :--- |
| **Model 3D** | *New York City* (Geometria miasta) | [Sketchfab](https://skfb.ly/pIHYX) autor: golukumar | Creative Commons Attribution (CC BY 4.0) |
| **Model 3D** | *Bmw M4 Competition* (Samochód 1) | [BlenderKit](https://www.blenderkit.com/asset-gallery-detail/ade0d0cf-a3ec-4c9c-b242-a7b6abb27a9d/) | Creative Commons CC0 |
| **Model 3D** | *Bmw M4 Competition - Modified* (Samochód 2) | [BlenderKit](https://www.blenderkit.com/asset-gallery-detail/7bfdea2a-0f40-4f82-80bf-e6e0ac12e8e9/) | Creative Commons CC0 |
| **Mapa HDRI** | *shanghai_bund_4k* (Światło otoczenia) | [Poly Haven](https://polyhaven.com/a/shanghai_bund) | Creative Commons CC0 |

## 6. Znane ograniczenia
* **Wydajność:** Niskie szumy (Threshold na 0.01) i 2048 próbki mocno obciążają układ graficzny. Renderowanie pełnej animacji wymaga potężnego GPU.
* **Optymalizacja siatki:** Niewidoczne w kadrze budynki zostały ręcznie odcięte z projektu, aby uchronić pamięć VRAM przed przepełnieniem.
