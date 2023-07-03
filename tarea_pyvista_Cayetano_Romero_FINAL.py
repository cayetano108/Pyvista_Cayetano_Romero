import pyvista as pv

# ------- PARA SELECCIONAR ARCHIVO .STL LOCAL ---------------------


# PUEDE QUE LA VENTANA DE SELECCION DE ARCHIVO APAREZCA DETRAS DE LA ACTUAL

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(filetypes=[("STL files", "*.stl")])
normal = pv.read(file_path)


# ------- PARA SELECCIONAR ARCHIVO LOCAL MEDIANTE RUTA ---------------------


# normal = pv.read('./modelos/kyuubi.stl')
# normal = pv.read('./modelos/a1.stl')
# normal = pv.read('./modelos/dragon_skull.stl') # RECOMIENDO PROBAR ESTE PARA MEJOR TIEMPO DE EJECUCION

plotter = pv.Plotter(shape=(2, 2))

# ------- en modo alambre con normales ---------------------


plotter.subplot(0, 0)
normal.compute_normals(inplace=True)

plotter.set_background(color='#ededed')

def size_normales(factor):
    plotter.subplot(0, 0)
    
    plotter.remove_actor('normal')
    plotter.remove_actor('glyphs')
    plotter.add_mesh(normal, color='orange', show_edges=True, name = 'normal')
    glyphs = normal.glyph(orient='Normals', scale=False, factor=factor)
    plotter.add_mesh(glyphs, color='red', name = 'glyphs')
    return

plotter.add_slider_widget(size_normales, [5, 25], value = 10, title = 'Tamaño', color = '#797a09')


plotter.add_text('Modelo en alambre con sus normales', font = 'courier', font_size = 10, color='k')

plotter.add_mesh(normal, color='orange', show_edges=True)
glyphs = normal.glyph(orient='Normals', scale=False, factor=10)
plotter.add_mesh(glyphs, color='red')

# -------------------- decimado ---------------------
 

plotter.subplot(0, 1)

plotter.set_background(color='#ededed')

plotter.add_text('Modelo Decimado', font = 'courier', font_size = 10, color='k')

def decimar(perc):
    plotter.subplot(0, 1)
    mesh_deci = normal.decimate(perc)
    plotter.remove_actor('decimar')
    plotter.add_mesh(mesh_deci, color = 'orange', name = 'decimado')
    return

def toggle_edges1(state):
    plotter.subplot(0, 1)
    mesh_deci = normal.decimate(0.5)
    plotter.remove_actor('decimar')
    plotter.add_mesh(mesh_deci, color = 'orange', name = 'decimado', show_edges=state)

plotter.add_text('Mostrar/Quitar malla', position=(80, 40), color = '#85130b', font_size = 12)

plotter.add_checkbox_button_widget(toggle_edges1, value=False, position=(40, 40), size=30, color_on = '#85130b')

plotter.add_slider_widget(decimar, [0, 0.999], value = 0.9, title = 'Decimado', color = '#135bcf')


# -------------------- suavizado ---------------------


plotter.subplot(1, 0)

plotter.set_background(color='#ededed')


plotter.add_text('Modelo Suavizado', font = 'courier', font_size = 10, color='k')

def suavizar(relaxation):
    plotter.subplot(1, 0)
    mesh_suav = normal.smooth(relaxation_factor = relaxation)
    plotter.remove_actor('suavizar')
    plotter.add_mesh(mesh_suav, color = 'orange', name = 'suavizado')
    return

def toggle_edges2(state):
    plotter.subplot(1, 0)
    mesh_suav = normal.smooth(relaxation_factor = 0.5)
    plotter.remove_actor('suavizar')
    plotter.add_mesh(mesh_suav, color = 'orange', name = 'suavizado', show_edges=state)

plotter.add_checkbox_button_widget(toggle_edges2, value=False, position=(40, 40), size=30, color_on = '#85130b')

plotter.add_slider_widget(suavizar, [0, 1], title = 'Suavizado', color = '#109c14')

plotter.add_text('Mostrar/Quitar malla', position=(80, 40), color = '#85130b', font_size = 12)



# -------------------- decimado y suavizado ---------------------


plotter.subplot(1, 1)


plotter.set_background(color='#ededed')


plotter.add_text('Modelo Decimado y Suavizado', font = 'courier', font_size = 10, color='k')

def decimar_suavizar(perc, relaxation):
    plotter.subplot(1, 1)
    mesh_deci_suav = normal.decimate(perc).smooth(relaxation_factor = relaxation)
    plotter.remove_actor('decimar y suavizar')
    plotter.remove_actor('suavizar')
    plotter.remove_actor('decimar')

    plotter.add_mesh(mesh_deci_suav, color = 'orange', name = 'decimado y suavizado')
    return

def update_perc(value):
    plotter.subplot(1, 1)
    decimar_suavizar(value, relaxation_slider.GetSliderRepresentation().GetValue())

def update_relaxation(value):
    plotter.subplot(1, 1)
    decimar_suavizar(perc_slider.GetSliderRepresentation().GetValue(), value)

def toggle_edges3(state):
    plotter.subplot(1, 1)
    mesh_deci_suav = normal.decimate(0.5).smooth(relaxation_factor = 0.5)
    plotter.remove_actor('decimar y suavizar')
    plotter.add_mesh(mesh_deci_suav, color = 'orange', name = 'decimado y suavizado', show_edges=state)



perc_slider = plotter.add_slider_widget(update_perc, [0, 0.999], value = 0.5, color = '#135bcf', title = 'Decimado', pointa = (0.4, 0.92), pointb=(0.9, 0.92))
relaxation_slider = plotter.add_slider_widget(update_relaxation, [0, 1], value = 0.5, color = '#109c14', title = 'Suavizado', pointa = (0.4, 0.77), pointb=(0.9, 0.77))

plotter.add_checkbox_button_widget(toggle_edges3, value=False, position=(40, 40), size=30, color_on = '#85130b')

plotter.add_text('Mostrar/Quitar malla', position=(80, 40), color = '#85130b', font_size = 12)



# ----------------------------------------------
# plotter.show(interactive=False, screenshot= 'kyubi.png')  # Para guardar las capturas
# plotter.show(interactive=False, screenshot= 'dragon.png')
# plotter.show(interactive=False, screenshot= 'a1.png')

plotter.show()


