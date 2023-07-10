import numpy as np 
import matplotlib.pyplot as plt

def move_motif(M, x, y, θ):
    M1 = np.ones((1, len(M[1, :])))
    M2 = np.vstack((M, M1))
    R = np.array([[np.cos(θ), -np.sin(θ), x], [np.sin(θ), np.cos(θ), y]])
    return(R @ M2)

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

def plot(ax, etat):
    ax.cla()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.grid()
    
    draw_car(ax, etat)





if __name__ == "__main__":
    etat = np.array([[0], [0], [np.pi/3]])  # position x, y et la direction theta

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
        # on fait une mesure par exemple une mesure de distance avec un point
        
        # on calcul u pour la vitesse de rotation
        u = 0
        # on intègre l'état du robot
        etat = etat + dt * evol(etat, u)

        #on affiche le robot
        plot(ax, etat)

        fig.canvas.draw()  # obligé pour l'affichage 
        plt.pause(dt)  # obligé pour l'affichage, tu peux mettre moins pour faire tourner la boucle plus vite

