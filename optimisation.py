import numpy as np
from scipy.optimize import minimize
import pandas as pd

# Fonction de coût courant Ln(x, u)
def L(n, x, u):
    """Calcule le coût courant à l'étape n."""
    return u ** 2 - x - 1

# Fonction de récurrence fn(x, u)
def f(n, x, u):
    """Calcule l'état suivant selon la récurrence f."""
    return x + u

# Fonction de coût terminal g(x)
def g(x):
    """Calcule le coût terminal."""
    return 0

# Optimisation continue pour chaque étape
def optimize_continuous(L_func, f_func, V_next, n, x):
    """Minimise la fonction de coût en continu sur l'ensemble des actions réelles (u)."""
    def objective(u):
        return L_func(n, x, u) + V_next(f_func(n, x, u))[0]
    
    result = minimize(objective, x0=0)  # Estimation initiale u = 0
    optimal_u = result.x[0]  # Contrôle optimal
    optimal_cost = result.fun  # Coût minimal
    return optimal_cost, optimal_u

# Fonction principale d'induction rétrograde
def backward_induction(x0, time_horizon):
    """Résout le problème d'optimisation dynamique par induction rétrograde."""
    V = {}
    policy = {}
    
    def V_n(n, x):
        if n == time_horizon:
            return g(x), None
        else:
            return optimize_continuous(L, f, lambda x: V_n(n+1, x), n, x)
    
    for n in range(time_horizon, -1, -1):
        V[n] = lambda x, n=n: V_n(n, x)
        policy[n] = V[n](x0)[1]
        
    return V, policy

# Utilisation de la récurrence pour calculer les états à chaque étape
def compute_states(x0, policy, time_horizon):
    """Calcule les états à chaque étape en utilisant la relation de récurrence."""
    x_values = [x0]
    for t in range(time_horizon):
        next_x = f(t, x_values[-1], policy[t])
        x_values.append(next_x)
    return x_values

# Paramètres définis par l'utilisateur
x0 = 0  # État initial
time_horizon = int(input("Entrez l'horizon temporel : "))  # Horizon temporel défini par l'utilisateur

# Résolution du problème par induction rétrograde
V, policy = backward_induction(x0, time_horizon)

# Création du dataframe pour les fonctions valeur et les politiques optimales
df_results = pd.DataFrame({
    'Étape': list(range(time_horizon + 1)),
    'Fonction Valeur': [V[t](x0)[0] for t in range(time_horizon + 1)],
    'u Optimal': [policy[t] for t in range(time_horizon + 1)]
})

print(df_results)

# Calcul et affichage des états successifs
x_values = compute_states(x0, policy, time_horizon)
df_states = pd.DataFrame({
    'Étape': list(range(time_horizon + 1)),
    'État': x_values
})

print("\nÉtats calculés :")
print(df_states)
