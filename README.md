# ⚡ LPU Smart Grid AI Optimizer
**Course:** AI Essentials (INT428) | **School of Computing**

An interactive AI application that uses a **Genetic Algorithm** to optimize energy distribution across the LPU campus.

## 🧠 AI Logic
- **Algorithm:** Genetic Algorithm (GA)
- **Search Strategy:** Stochastic Search with Priority-Weighted Fitness.
- **Constraints:** Hard-coded energy caps and priority-based load shedding.
- **Heuristics:** Exponential priority weighting ($Priority^2$) to ensure critical uptime for School of Computing & Electronics.

## 🎮 How to Run
1. Clone the repo: `git clone <your-link>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Dashboard: `streamlit run app.py`

## 📊 Features
- Real-time "Hackathon Mode" demand spikes.
- Volatile Solar supply simulation.
- Battery State of Charge (SoC) management.
- Live Fitness Curve tracking (Proof of GA Convergence).
