from pulp import LpMinimize, LpProblem, lpSum, LpVariable, LpBinary
import pandas as pd
import numpy as np

df = pd.read_csv("vectors.csv")
    
def find_coordinates(int):
    df_coordinate=df.iloc[int]
    theta_rad = np.radians(df_coordinate["Theta"])
    mag = df_coordinate["Magnitude"]
    if df_coordinate["FD"] == "W" and df_coordinate["SD"] == "N":
        delta_x = (-1)* mag * np.cos(theta_rad)
        delta_y = mag * np.sin(theta_rad)
    if df_coordinate["FD"] == "N" and df_coordinate["SD"] == "W":
        delta_x = (-1) * mag * np.sin(theta_rad)
        delta_y = mag * np.cos(theta_rad)
    if df_coordinate["FD"] == "E" and df_coordinate["SD"] == "N":
        delta_x = mag * np.cos(theta_rad)
        delta_y = mag * np.sin(theta_rad)
    if df_coordinate["FD"] == "N" and df_coordinate["SD"] == "E":
        delta_x = mag * np.sin(theta_rad)
        delta_y = mag * np.cos(theta_rad)
    if df_coordinate["FD"] == "W" and df_coordinate["SD"] == "S":
        delta_x = (-1)* mag * np.cos(theta_rad)
        delta_y =(-1) * mag * np.sin(theta_rad)
    if df_coordinate["FD"] == "S" and df_coordinate["SD"] == "W":
        delta_x =(-1) * mag * np.sin(theta_rad)
        delta_y =(-1) * mag * np.cos(theta_rad)
    if df_coordinate["FD"] == "E" and df_coordinate["SD"] == "S":
        delta_x = mag * np.cos(theta_rad)
        delta_y =(-1) * mag * np.sin(theta_rad)
    if df_coordinate["FD"] == "S" and df_coordinate["SD"] == "E":
        delta_x = mag * np.sin(theta_rad)
        delta_y =(-1) * mag * np.cos(theta_rad)
    
    return delta_x, delta_y

prob = LpProblem("Minimize_X_and_Y", LpMinimize)

x_components = []
y_components = []

for i in range(len(df)):
    delta_x, delta_y = find_coordinates(i)
    x_components.append(delta_x)
    y_components.append(delta_y)

selection = [LpVariable(f"vec_{i}", cat=LpBinary) for i in range(len(df))]

prob += lpSum(selection) == 9

prob += lpSum(x_components[i] * selection[i] for i in range(len(df)))  >= 0.00
prob += lpSum(y_components[i] * selection[i] for i in range(len(df))) >= 0.00
prob += lpSum(x_components[i] * selection[i] for i in range(len(df)))  <= 0.00
prob += lpSum(y_components[i] * selection[i] for i in range(len(df))) <= 0.00

prob.solve()

selected_vectors = [i for i in range(len(df)) if selection[i].varValue == 1]
print("Selected vectors (indices):", selected_vectors)
