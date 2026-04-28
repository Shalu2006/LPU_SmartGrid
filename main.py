import numpy as np
import matplotlib.pyplot as plt
import random

# --- LPU CAMPUS CONFIG ---
# Blocks: [Computing, Electronics, Classrooms, Hostels, StreetLights]
BLOCKS = ["School of Computing", "School of Electronics", "General Classrooms", "Hostels", "StreetLights"]
DEMAND_BASE = np.array([800, 600, 400, 500, 150]) 
PRIORITY = np.array([10, 8, 4, 6, 2]) # Computing is King
BATTERY_MAX = 3000
battery_soc = 1000 

def get_lpu_demand(hour, is_hackathon=False):
    current_demand = DEMAND_BASE.copy()
    # Classrooms/Schools are active 9-5
    if not (8 <= hour <= 18):
        current_demand[2] = 20 # Classrooms off at night
        current_demand[0] *= 0.4 # Computing labs on low power
    
    if is_hackathon and (10 <= hour <= 22):
        current_demand[0] += 500 # Massive spike for Computing
    return current_demand

def optimize_grid(supply, demand, battery):
    # Genetic Algorithm to find the best power distribution
    pop_size = 50
    pop = [np.random.rand(len(BLOCKS)) for _ in range(pop_size)]
    
    for _ in range(40):
        # Fitness = meeting demand * priority^2 + saving battery
        pop = sorted(pop, key=lambda p: np.sum(p * (PRIORITY**2)) if np.sum(p * demand) <= (supply + battery) else 0, reverse=True)
        next_gen = pop[:10]
        while len(next_gen) < pop_size:
            child = np.clip((pop[0] + pop[1])/2 + np.random.normal(0, 0.1, 5), 0, 1)
            next_gen.append(child)
        pop = next_gen
    return pop[0]

# --- SIMULATION ---
hours = list(range(24))
computing_perf = []
battery_lvl = []
solar_supply = []
hackathon_day = random.choice([True, False])

for h in hours:
    solar = max(0, 2000 * np.sin((h - 6) * np.pi / 12)) * (0.5 if random.random() < 0.2 else 1)
    demand = get_lpu_demand(h, is_hackathon=hackathon_day)
    
    best_plan = optimize_grid(solar, demand, battery_soc)
    
    # Update Battery
    used = np.sum(best_plan * demand)
    battery_soc = np.clip(battery_soc + (solar - used), 0, BATTERY_MAX)
    
    computing_perf.append(best_plan[0] * 100)
    battery_lvl.append(battery_soc)
    solar_supply.append(solar)

# --- THE "PROFESSIONAL" DASHBOARD ---
plt.style.use('dark_background') # Looks much cooler for an AI project
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

ax1.plot(hours, solar_supply, color='gold', label='Solar Generation (kW)', linewidth=2)
ax1.fill_between(hours, solar_supply, color='gold', alpha=0.1)
ax1.set_ylabel("Power (kW)")
ax1.set_title(f"LPU Smart Grid Dashboard {'[HACKATHON ACTIVE]' if hackathon_day else ''}")
ax1.legend()

ax2.plot(hours, computing_perf, color='cyan', label='School of Computing Uptime %', linewidth=2)
ax2.plot(hours, [b/BATTERY_MAX*100 for b in battery_lvl], color='lime', label='Battery SoC %', linestyle='--')
ax2.set_ylabel("Percentage (%)")
ax2.set_xlabel("Hour of the Day")
ax2.legend()
plt.tight_layout()
import streamlit as st
st.pyplot(fig)
