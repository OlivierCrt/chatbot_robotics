import plotly.graph_objects as go
from src.const_v import *
from src.trajectory_generation import traj

def ajouter_sol(fig):
    """
    Adds a ground covering the entire XY plane between z = -1010 and z = -2110.
    """
    # Define the corners of the ground at two levels
    upper_corners = [
        [-2110, -2110, -1010],
        [-2110, 2110, -1010],
        [2110, 2110, -1010],
        [2110, -2110, -1010],
    ]
    lower_corners = [
        [-2110, -2110, -2110],
        [-2110, 2110, -2110],
        [2110, 2110, -2110],
        [2110, -2110, -2110],
    ]

    # Combined points for Mesh3d
    vertices = upper_corners + lower_corners
    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    z = [v[2] for v in vertices]

    # Define the ground faces
    # Top and bottom faces (two rectangles, split into two triangles each)
    faces = [
        [0, 1, 2], [0, 2, 3],  # Top face (z = -1010)
        [4, 5, 6], [4, 6, 7],  # Bottom face (z = -2110)
        # Side faces
        [0, 1, 5], [0, 5, 4],  # Side 1
        [1, 2, 6], [1, 6, 5],  # Side 2
        [2, 3, 7], [2, 7, 6],  # Side 3
        [3, 0, 4], [3, 4, 7],  # Side 4
    ]

    # Extract indices for i, j, k
    i = [f[0] for f in faces]
    j = [f[1] for f in faces]
    k = [f[2] for f in faces]

    # Add the ground to the figure
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
    Generates the coordinates of a cylinder between two 3D points.

    :param p1: 3D coordinates of the starting point.
    :param p2: 3D coordinates of the end point.
    :param radius: Radius of the cylinder.
    :param resolution: Number of segments to approximate the cylinder.
    :return: x, y, z coordinates of the cylinder.
    """
    # Direction between p1 and p2
    v = np.array(p2) - np.array(p1)
    v_length = np.linalg.norm(v)
    v = v / v_length  # Normalize

    # Find a perpendicular vector
    if np.isclose(v[0], 0) and np.isclose(v[1], 0):
        perp = np.array([1, 0, 0])
    else:
        perp = np.cross(v, [0, 0, 1])
    perp = perp / np.linalg.norm(perp)

    # Cylindrical base
    theta = np.linspace(0, 2 * np.pi, resolution)
    circle = np.array([np.cos(theta), np.sin(theta), np.zeros_like(theta)])
    circle = radius * circle.T

    # Rotation matrix to align the circle to v
    rotation_matrix = np.array([perp, np.cross(v, perp), v]).T
    circle_rotated = circle @ rotation_matrix.T

    # Generate the cylinder
    x, y, z = [], [], []
    for i in range(resolution):
        x.extend([p1[0] + circle_rotated[i, 0], p2[0] + circle_rotated[i, 0]])
        y.extend([p1[1] + circle_rotated[i, 1], p2[1] + circle_rotated[i, 1]])
        z.extend([p1[2] + circle_rotated[i, 2], p2[2] + circle_rotated[i, 2]])

    return x, y, z

def ajouter_table(fig):
    """
    Adds a table with legs to the 3D figure.
    """
    # Table corners (top surface)
    corners = [
        [-200, -200, 0],  # Corner 1
        [-200, 200, 0],   # Corner 2
        [200, 200, 0],    # Corner 3
        [200, -200, 0],   # Corner 4
    ]
    z_bottom = -2110

    # Add the top surface (filled rectangle with Mesh3d)
    top_x = [corners[i][0] for i in [0, 1, 2, 3]]
    top_y = [corners[i][1] for i in [0, 1, 2, 3]]
    top_z = [corners[i][2] for i in [0, 1, 2, 3]]

    fig.add_trace(go.Mesh3d(
        x=top_x,
        y=top_y,
        z=top_z,
        color='brown',
        opacity=1,
        i=[0, 1, 2, 3],  # Indices of the vertices forming the faces
        j=[1, 2, 3, 0],
        k=[2, 3, 0, 1],
        showlegend=False,
    ))

    # Add the legs (cylinders)
    for corner in corners:
        leg_x, leg_y, leg_z = generer_cylindre(corner, [corner[0], corner[1], z_bottom], radius=5, resolution=10)
        fig.add_trace(go.Mesh3d(
            x=leg_x,
            y=leg_y,
            z=leg_z,
            color='brown',
            opacity=1,
            alphahull=0,
            showlegend=False,
        ))

    return fig


def bras_rob_model3D_animation(A, B, V1, V2, K):
    """
    Animates a robotic arm following a circular trajectory defined by two points (A and B).

    :param A: Starting point.
    :param B: Ending point.
    :param V1: Initial velocity.
    :param V2: Final velocity.
    :param K: Acceleration.
    """
    q, qp, positions_circle, dt = traj(A, B, V1, V2, K, Debug=False)
    print("Generating simulation...")

    max_frames = 60  # Limit the number of frames to ease execution
    step = max(1, len(q) // max_frames)  # Calculate subsampling step

    # Initialize arm configurations
    frames = []

    for i in range(0, len(q), step):
        q1, q2, q3 = q[i]  # Take the first solution

        # Calculate intermediate positions of the arm
        L1, L2, L3 = Liaisons[0], Liaisons[1], Liaisons[2]
        x1, y1, z1 = 0, 0, L1[1]
        x2, y2, z2 = L1[0] * np.cos(q1), L1[0] * np.sin(q1), z1
        x3, y3, z3 = x2 + L2[2] * np.cos(q1 + np.pi / 2), y2 + L2[2] * np.sin(q1 + np.pi / 2), z2
        x4, y4, z4 = x3 + L2[1] * np.cos(q2) * np.cos(q1), y3 + L2[1] * np.cos(q2) * np.sin(q1), z3 + L2[1] * np.sin(q2)
        x5, y5, z5 = x4 + L3[2] * np.cos(q1 - np.pi / 2), y4 + L3[2] * np.sin(q1 - np.pi / 2), z4
        x6, y6, z6 = x5 + L3[1] * np.cos(q3 + q2) * np.cos(q1), y5 + L3[1] * np.cos(q3 + q2) * np.sin(q1), z5 + L3[1] * np.sin(q3 + q2)

        # Add cylinders for this frame
        cylinders = []
        positions = [([0, 0, 0], [x1, y1, z1]), ([x2, y2, z2], [x3, y3, z3]), ([x4, y4, z4], [x5, y5, z5])]

        pos_circle = positions_circle
        # Separate coordinates for display
        x_circle, y_circle, z_circle = zip(*pos_circle)  # Convert to tuples
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

        # Create a frame with the current position of the arm
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
        ] + cylinders))

    # Create the initial figure
    fig = go.Figure(
        data=frames[0].data,  # Use the data from the first frame directly
        frames=frames
    )

    fig = ajouter_table(fig)
    fig = ajouter_sol(fig)

    # Configure play buttons
    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(label="Replay",
                     method="animate",
                     args=[None, {"frame": {"duration": dt * 1000 * step, "redraw": True}, "fromcurrent": True}]),
                dict(label="Pause",
                     method="animate",
                     args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])
            ]
        )]
    )

    # Configure the graph design
    fig.update_layout(
        scene_aspectmode='cube',
        scene=dict(
            xaxis=dict(title="X Axis", range=[-2110, 2110]),
            yaxis=dict(title="Y Axis", range=[-2110, 2110]),
            zaxis=dict(title="Z Axis", range=[-2110, 2110])
        ),
        title="3D Animation of the Robotic Arm"
    )

    # Display the figure
    fig.show()
