import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="LPU AI Smart Grid Pro", layout="wide")
st.title("🛡️ LPU AI Smart Grid: Pro Edition")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/3/3a/Lovely_Professional_University_logo.png", width=100)

# --- SIDEBAR: ADVANCED CONTROLS ---
st.sidebar.header("🕹️ Simulation Settings")
priority_sector = st.sidebar.selectbox("Set Priority Focus", ["School of Computing", "School of Electronics", "Hostels"])
grid_cost_per_unit = st.sidebar.slider("Grid Electricity Price (₹/unit)", 5, 15, 8)
weather_event = st.sidebar.selectbox("Weather Condition", ["Clear Sky", "Partly Cloudy", "Heavy Rain/Storm"])
hackathon_active = st.sidebar.toggle("LPU Hackathon Mode (Server Spike)")

# --- LOGIC CONSTANTS ---
BLOCKS = ["School of Computing", "School of Electronics", "General Classrooms", "Hostels", "StreetLights"]
DEMAND_BASE = np.array([800, 600, 400, 500, 150])
PRIORITIES = {"School of Computing": [12, 8, 4, 6, 2], 
              "School of Electronics": [8, 12, 4, 6, 2],
              "Hostels": [7, 6, 4, 12, 2]}

# --- AI ENGINE ---
def run_genetic_algorithm(supply, demand, active_priority):
    pop_size = 40
    # Higher weights for the selected priority sector
    weights = np.array(PRIORITIES[active_priority])
    pop = [np.random.rand(len(BLOCKS)) for _ in range(pop_size)]
    for _ in range(40):
        pop = sorted(pop, key=lambda p: np.sum(p * (weights**2)) if np.sum(p * demand) <= supply else 0, reverse=True)
        next_gen = pop[:10]
        while len(next_gen) < pop_size:
            child = np.clip((pop[0] + pop[1])/2 + np.random.normal(0, 0.05, 5), 0, 1)
            next_gen.append(child)
        pop = next_gen
    return pop[0]

# --- SIMULATION LOOP ---
hours = list(range(24))
results = []
weather_multipliers = {"Clear Sky": 1.0, "Partly Cloudy": 0.6, "Heavy Rain/Storm": 0.2}

for h in hours:
    # 1. Supply Calculation
    solar = max(0, 2500 * np.sin((h - 6) * np.pi / 12)) * weather_multipliers[weather_event]
    
    # 2. Demand Calculation
    demand = DEMAND_BASE.copy()
    if hackathon_active and (10 <= h <= 22): demand[0] += 600
    if not (8 <= h <= 18): demand[2] = 10 # Empty classrooms
    
    # 3. AI Allocation
    allocation = run_genetic_algorithm(solar + 500, demand, priority_sector)
    
    # 4. Metrics
    actual_used = np.sum(allocation * demand)
    money_saved = (actual_used * grid_cost_per_unit) / 100 # Rough estimate
    
    results.append({
        "Hour": h,
        "Solar": solar,
        "Demand": np.sum(demand),
        "Computing_Uptime": allocation[0] * 100,
        "Electronics_Uptime": allocation[1] * 100,
        "Savings": money_saved
    })

df = pd.DataFrame(results)

# --- FRONTEND DISPLAY ---
col1, col2, col3, col4 = st.columns(4)
health = "STABLE" if df['Computing_Uptime'].mean() > 90 else "STRAINED"
col1.metric("Grid Status", health, delta=None)
col2.metric("Total Savings", f"₹{df['Savings'].sum():,.0f}")
col3.metric("Avg Computing Uptime", f"{df['Computing_Uptime'].mean():.1f}%")
col4.metric("Avg Electronics Uptime", f"{df['Electronics_Uptime'].mean():.1f}%")

# --- SAVE STATE FOR OTHER PAGES ---
st.session_state['df'] = df
st.session_state['health'] = health
st.session_state['grid_cost'] = grid_cost_per_unit
st.session_state['weather'] = weather_event
st.session_state['hackathon'] = hackathon_active
st.session_state['priority_sector'] = priority_sector

from main import optimize_grid, get_lpu_demand

st.subheader("📊 Advanced AI Graph")

hours = list(range(24))
computing_perf = []
battery_soc = 1000
battery_max = 3000

for h in hours:
    solar = max(0, 2000 * np.sin((h - 6) * np.pi / 12))
    demand = get_lpu_demand(h)
    
    best_plan = optimize_grid(solar, demand, battery_soc)
    
    used = np.sum(best_plan * demand)
    battery_soc = np.clip(battery_soc + (solar - used), 0, battery_max)
    
    computing_perf.append(best_plan[0] * 100)

fig, ax = plt.subplots()
ax.plot(hours, computing_perf)
ax.set_title("Computing Performance (24 hrs)")

st.pyplot(fig)
