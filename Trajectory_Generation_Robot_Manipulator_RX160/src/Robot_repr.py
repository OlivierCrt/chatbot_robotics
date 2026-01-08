import plotly.graph_objects as go
from const_v import *


"""FONTION POUR MODELISER EN 3D LE BRAS ROBOT, LA FONCTION EST DECLARE A LA TOUTE FIN"""

def generar_cilindro(p1, p2, radius=50, resolution=20):
    """
    Génère les coordonnées d'un cylindre entre deux points 3D.

    :param p1: Coordonnées 3D du point de départ.
    :param p2: Coordonnées 3D du point de fin.
    :param radius: Rayon du cylindre.
    :param resolution: Nombre de segments pour approximer le cylindre.
    :return: Coordonnées x, y, z du cylindre.
    """
    # Direction entre p1 et p2
    v = np.array(p2) - np.array(p1)
    v_length = np.linalg.norm(v)
    v = v / v_length  # Normaliser

    # Trouver un vecteur perpendiculaire
    if np.isclose(v[0], 0) and np.isclose(v[1], 0):
        perp = np.array([1, 0, 0])
    else:
        perp = np.cross(v, [0, 0, 1])
    perp = perp / np.linalg.norm(perp)

    # Base cylindrique
    theta = np.linspace(0, 2 * np.pi, resolution)
    circle = np.array([np.cos(theta), np.sin(theta), np.zeros_like(theta)])
    circle = radius * circle.T

    # Matrice de rotation pour aligner le cercle sur v
    rotation_matrix = np.array([perp, np.cross(v, perp), v]).T
    circle_rotated = circle @ rotation_matrix.T

    # Générer le cylindre
    x, y, z = [], [], []
    for i in range(resolution):
        x.extend([p1[0] + circle_rotated[i, 0], p2[0] + circle_rotated[i, 0]])
        y.extend([p1[1] + circle_rotated[i, 1], p2[1] + circle_rotated[i, 1]])
        z.extend([p1[2] + circle_rotated[i, 2], p2[2] + circle_rotated[i, 2]])

    return x, y, z

def bras_rob_model3D(Liaisons, q):
    q_rad = np.radians(q)

    L1 = Liaisons[0]
    L2 = Liaisons[1]
    L3 = Liaisons[2]

    # Angles
    teta1 = q_rad[0]
    teta2 = q_rad[1]
    teta3 = q_rad[2]

    # Calculer les coordonnées intermédiaires pour le tracé 3D
    x1, y1, z1 = 0, 0, L1[1]
    x2, y2, z2 = L1[0] * np.cos(teta1), L1[0] * np.sin(teta1), z1
    x3, y3, z3 = x2 + L2[2] * np.cos(teta1 + np.pi / 2), y2 + L2[2] * np.sin(teta1 + np.pi / 2), z2
    x4, y4, z4 = x3 + L2[1] * np.cos(teta2) * np.cos(teta1), y3 + L2[1] * np.cos(teta2) * np.sin(teta1), z3 + L2[1] * np.sin(teta2)
    x5, y5, z5 = x4 + L3[2] * np.cos(teta1 - np.pi / 2), y4 + L3[2] * np.sin(teta1 - np.pi / 2), z4
    x6, y6, z6 = x5 + L3[1] * np.cos(teta3 + teta2) * np.cos(teta1), y5 + L3[1] * np.cos(teta3 + teta2) * np.sin(teta1), z5 + L3[1] * np.sin(teta3 + teta2)

    # Ajouter des cylindres
    cylinders = []
    positions = [([0, 0, 0], [x1, y1, z1]), ([x2, y2, z2], [x3, y3, z3]), ([x4, y4, z4], [x5, y5, z5])]
    for p_start, p_end in positions:
        start_quarter = p_start + 0.25 * (np.array(p_end) - np.array(p_start))
        end_quarter = p_start + 0.75 * (np.array(p_end) - np.array(p_start))
        x_cyl, y_cyl, z_cyl = generar_cilindro(start_quarter, end_quarter)
        cylinders.append(go.Mesh3d(
            x=x_cyl, y=y_cyl, z=z_cyl,
            color='green',
            opacity=1,
            alphahull=0,
            showlegend=False
        ))

    # Création de la figure avec les segments et les cylindres
    fig = go.Figure(data=[
        go.Scatter3d(
            x=[0, x1, x2, x3, x4, x5, x6],
            y=[0, y1, y2, y3, y4, y5, y6],
            z=[0, z1, z2, z3, z4, z5, z6],
            mode='lines+markers',
            marker=dict(size=4),
            line=dict(color='blue', width=5),
            showlegend=False
        )
    ] + cylinders)  # Ajouter les cylindres à la figure

    # Configuration des axes
    fig.update_layout(scene_aspectmode='cube', scene=dict(
        xaxis=dict(title="Axe X", range=[-2110, 2110]),
        yaxis=dict(title="Axe Y", range=[-2110, 2110]),
        zaxis=dict(title="Axe Z", range=[0, 2 * 2110])
    ))

    return fig.show()
