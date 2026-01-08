import plotly.graph_objects as go
from src.const_v import *
from src.trajectory_generation import traj

def ajouter_sol(fig):
    """
    Ajoute un sol couvrant tout le plan XY entre z = -1010 et z = -2110.
    """
    # Définir les coins du sol aux deux niveaux
    coins_sup = [
        [-2110, -2110, -1010],
        [-2110, 2110, -1010],
        [2110, 2110, -1010],
        [2110, -2110, -1010],
    ]
    coins_inf = [
        [-2110, -2110, -2110],
        [-2110, 2110, -2110],
        [2110, 2110, -2110],
        [2110, -2110, -2110],
    ]

    # Points combinés pour le Mesh3d
    vertices = coins_sup + coins_inf
    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    z = [v[2] for v in vertices]

    # Définir les faces du sol
    # Faces supérieures et inférieures (deux rectangles, divisés en deux triangles chacun)
    faces = [
        [0, 1, 2], [0, 2, 3],  # Face supérieure (z = -1010)
        [4, 5, 6], [4, 6, 7],  # Face inférieure (z = -2110)
        # Faces latérales
        [0, 1, 5], [0, 5, 4],  # Côté 1
        [1, 2, 6], [1, 6, 5],  # Côté 2
        [2, 3, 7], [2, 7, 6],  # Côté 3
        [3, 0, 4], [3, 4, 7],  # Côté 4
    ]

    # Extraire les indices pour i, j, k
    i = [f[0] for f in faces]
    j = [f[1] for f in faces]
    k = [f[2] for f in faces]

    # Ajouter le sol à la figure
    fig.add_trace(go.Mesh3d(
        x=x,
        y=y,
        z=z,
        i=i,
        j=j,
        k=k,
        color='gray',
        opacity=1,
        showlegend=False
    ))

    return fig


def generer_cylindre(p1, p2, radius=50, resolution=20):
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

def ajouter_table(fig):
    # Coins de la table (plateau)
    coins = [
        [-200, -200, 0],  # Coin 1
        [-200, 200, 0],   # Coin 2
        [200, 200, 0],    # Coin 3
        [200, -200, 0],   # Coin 4
    ]
    z_bas = -2110

    # Ajouter le plateau (rectangle rempli avec Mesh3d)
    plateau_x = [coins[i][0] for i in [0, 1, 2, 3]]
    plateau_y = [coins[i][1] for i in [0, 1, 2, 3]]
    plateau_z = [coins[i][2] for i in [0, 1, 2, 3]]

    fig.add_trace(go.Mesh3d(
        x=plateau_x,
        y=plateau_y,
        z=plateau_z,
        color='brown',
        opacity=1,
        i=[0, 1, 2, 3],  # Indices des sommets formant les faces
        j=[1, 2, 3, 0],
        k=[2, 3, 0, 1],
        showlegend=False,
    ))

    # Ajouter les pieds (cylindres)
    for coin in coins:
        pied_x, pied_y, pied_z = generer_cylindre(coin, [coin[0], coin[1], z_bas], radius=5, resolution=10)
        fig.add_trace(go.Mesh3d(
            x=pied_x,
            y=pied_y,
            z=pied_z,
            color='brown',
            opacity=1,
            alphahull=0,
            showlegend=False,
        ))

    return fig


def bras_rob_model3D_animation(A,B,V1,V2,K):
    """
    Anime un bras robotique suivant une trajectoire circulaire définie par deux points (A et B).

    :param Liaisons: Dictionnaire contenant les dimensions des liaisons du bras.
    :param Robot_pos: Liste contenant deux points [A, B] qui définissent le cercle.
    """
    q,qp, positions_cercle, dt = traj(A, B, V1,V2, K,Debug=False)
    # print(f"dt={dt}")
    print("Génération de la simulation...")

    max_frames = 60  # Limiter le nombre de frames pour faciliter l'exécution
    step = max(1, len(q) // max_frames)  # Calculer le pas de sous-échantillonnage

    # Initialiser les configurations du bras
    frames = []

    for i in range(0, len(q), step):

        q1, q2, q3 = q[i]  # Prendre la première solution

        # Calculer les positions intermédiaires du bras
        L1, L2, L3 = Liaisons[0], Liaisons[1], Liaisons[2]
        x1, y1, z1 = 0, 0, L1[1]
        x2, y2, z2 = L1[0] * np.cos(q1), L1[0] * np.sin(q1), z1
        x3, y3, z3 = x2 + L2[2] * np.cos(q1 + np.pi / 2), y2 + L2[2] * np.sin(q1 + np.pi / 2), z2
        x4, y4, z4 = x3 + L2[1] * np.cos(q2) * np.cos(q1), y3 + L2[1] * np.cos(q2) * np.sin(q1), z3 + L2[1] * np.sin(q2)
        x5, y5, z5 = x4 + L3[2] * np.cos(q1 - np.pi / 2), y4 + L3[2] * np.sin(q1 - np.pi / 2), z4
        x6, y6, z6 = x5 + L3[1] * np.cos(q3 + q2) * np.cos(q1), y5 + L3[1] * np.cos(q3 + q2) * np.sin(q1), z5 + L3[1] * np.sin(q3 + q2)

        # Ajouter des cylindres pour cette frame
        cylinders = []
        positions = [([0, 0, 0], [x1, y1, z1]), ([x2, y2, z2], [x3, y3, z3]), ([x4, y4, z4], [x5, y5, z5])]

        pos_circle = positions_cercle
        # Séparer les coordonnées pour l'affichage
        x_circle, y_circle, z_circle = zip(*pos_circle)  # Convertir en tuples
        for p_start, p_end in positions:
            start_quarter = p_start + 0.25 * (np.array(p_end) - np.array(p_start))
            end_quarter = p_start + 0.75 * (np.array(p_end) - np.array(p_start))
            x_cyl, y_cyl, z_cyl = generer_cylindre(start_quarter, end_quarter)
            cylinders.append(go.Mesh3d(
                x=x_cyl, y=y_cyl, z=z_cyl,
                color='green',
                opacity=1,
                alphahull=0,
                showlegend=False
            ))

        # Créer une frame avec la position actuelle du bras
        frames.append(go.Frame(data=[
            go.Scatter3d(
                x=[0, x1, x2, x3, x4, x5, x6],
                y=[0, y1, y2, y3, y4, y5, y6],
                z=[0, z1, z2, z3, z4, z5, z6],
                mode='lines+markers',
                marker=dict(size=4),
                line=dict(color='blue', width=5),
                showlegend=False
            ),
            go.Scatter3d(
                x=[A[0], B[0]],
                y=[A[1], B[1]],
                z=[A[2], B[2]],
                mode='markers+text',
                marker=dict(size=6, color=['green', 'red'], symbol='cross'),
                text=['A', 'B'],
                textposition='top center',
                showlegend=False
            ),
            go.Scatter3d(
                x=x_circle,
                y=y_circle,
                z=z_circle,
                mode='lines',
                line=dict(color='orange', width=2),
                showlegend=False
            )
        ]+ cylinders))


    # Créer la figure initiale
    # Créer la figure initiale avec la première frame
    fig = go.Figure(
        data=frames[0].data,  # Utiliser directement les données de la première frame
        frames=frames
    )

    fig = ajouter_table(fig)
    fig = ajouter_sol(fig)

    # Configurer les boutons de lecture
    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(label="Rejouer",
                     method="animate",
                     args=[None, {"frame": {"duration": dt*1000*step, "redraw": True}, "fromcurrent": True}]),
                dict(label="Pause",
                     method="animate",
                     args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])
            ]
        )]
    )
    #1010
    # Configurer le design du graphique
    fig.update_layout(
        scene_aspectmode='cube',
        scene=dict(
            xaxis=dict(title="Axe X", range=[-2110, 2110]),
            yaxis=dict(title="Axe Y", range=[-2110, 2110]),
            zaxis=dict(title="Axe Z", range=[-2110, 2110])
        ),
        title="Animation 3D du Bras Robotique"
    )

    # Afficher la figure
    fig.show()
