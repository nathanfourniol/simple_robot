import numpy as np 
import matplotlib.pyplot as plt

def move_motif(M, x, y, θ):
    M1 = np.ones((1, len(M[1, :])))
    M2 = np.vstack((M, M1))
    R = np.array([[np.cos(θ), -np.sin(θ), x], [np.sin(θ), np.cos(θ), y]])
    return(R @ M2)

def sawtooth(x):
    # pour gérer les diffrences d'angle
    return (x+np.pi) % (2*np.pi)-np.pi   # or equivalently   2*arctan(tan(x/2))

def draw_car(ax, state):
    x, y, theta = state.flatten()
    M = np.array([[-0.5, 0.5, 0, -0.5], [0, 0, 1, 0]]) # motif du robot triangle
    M = move_motif(M, 0, 0, -np.pi/2)
    M = move_motif(M, etat[0, 0], etat[1, 0], etat[2, 0]) # la pointe pointe dans la direction du robot (theta)
    ax.plot(M[0, :], M[1, :]) # affichage du robo triangle

def evol(etat, input):
    """
    Pour faire evoluer le robot
    etat : c'est l'etat du robot : x, y et sa direction
    input : c'est la vitesse de rotation du robot
    d_etat c'est la dérivé de l'état, ou l'évolution de l'etat
    on l'utilisera pour fair une integration d'euler
    
    """
    x, y, theta = etat.flatten()
    v = 1 # vitesse du robot
    d_etat = np.array([[v*np.cos(theta)],
                       [v*np.sin(theta)],
                       [input]])
    return d_etat

def plot(ax, etat, point_a_atteindre):
    ax.cla()  # efface les dessins précédents
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.grid()
    draw_car(ax, etat) # dessine le robot
    ax.plot(point_a_atteindre[0, 0], point_a_atteindre[1, 0], 'ro') # dessine le point à atteindre

def suivre_un_cap(point_a_atteindre, etat):
    """
    Fonction qui permet de faire suivre un cap au robot pour rejoindre un point
    """
    x, y, theta = etat.flatten()
    x_a, y_a = point_a_atteindre.flatten()
    #calcul de l'angle à suivre
    theta_a = np.arctan2(y_a - y, x_a - x) # angle à suivre pour aller vers le point
    # calcul de l'erreur
    e = sawtooth(theta_a - theta) # on calcul l'erreur entre l'angle à suivre et l'angle du robot
   
    # calcul de la vitesse de rotation (l'input u du robot)
    u = 0.5 * e

    return u

if __name__ == "__main__":
    etat = np.array([[0], [0], [np.pi/3]])  # position x, y et la direction theta
    point_a_atteindre = np.array([[5], [5]]) # point à atteindre

    temps_simulation = 100  # 100s
    dt = 0.1  # pas pour l'integration
    fig, ax = plt.subplots() # pour l'affichage
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.grid()

    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Robot')

    t = 0
    while t < temps_simulation :        
        # on calcule u pour la vitesse de rotation
        u = 0.5 # vitesse de rotation du robot
        # u = suivre_un_cap(point_a_atteindre, etat) # on fait suivre un cap au robot pour aller vers le point (5, 5)
       
        # on intègre l'état du robot
        etat = etat + dt * evol(etat, u)

        #on affiche le robot
        plot(ax, etat, point_a_atteindre)

        fig.canvas.draw()  # obligé pour l'affichage 
        plt.pause(0.001)  # obligé pour l'affichage, tu peux mettre dt pour faire un simulation en temps reel 
        t = t + dt