import json
import math
import random
import csv

# -----------------------------
# Utility Functions
# -----------------------------
def euclidean(p1, p2):
    """Calculate Euclidean distance"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def random_delay():
    """Random delivery delay (0–10 units)"""
    return random.uniform(0, 10)

def ascii_route(start, mid, end):
    """Simple ASCII visualization"""
    return f"{start} ---> {mid} ---> {end}"

# -----------------------------
# Load JSON Data
# -----------------------------
with open("data.json", "r") as file:
    data = json.load(file)

warehouses = data["warehouses"]
agents = data["agents"]
packages = data["packages"]

# -----------------------------
# Initialize Agent Stats
# -----------------------------
stats = {}
for agent in agents:
    stats[agent] = {
        "packages_delivered": 0,
        "total_distance": 0.0,
        "routes": []
    }

# -----------------------------
# Simulation
# -----------------------------
for i, pkg in enumerate(packages):

    # 🚚 Mid-day new agent joins
    if i == len(packages) // 2:
        agents["A4"] = [20, 80]
        stats["A4"] = {
            "packages_delivered": 0,
            "total_distance": 0.0,
            "routes": []
        }
        print("\n📢 New agent A4 joined mid-day at [20,80]\n")

    warehouse_pos = warehouses[pkg["warehouse"]]

    # Assign nearest agent
    nearest_agent = min(
        agents,
        key=lambda a: euclidean(agents[a], warehouse_pos)
    )

    # Distance calculations
    to_wh = euclidean(agents[nearest_agent], warehouse_pos)
    to_dest = euclidean(warehouse_pos, pkg["destination"])
    delay = random_delay()

    total_distance = to_wh + to_dest + delay

    # Update stats
    stats[nearest_agent]["packages_delivered"] += 1
    stats[nearest_agent]["total_distance"] += total_distance

    route = ascii_route(
        agents[nearest_agent],
        warehouse_pos,
        pkg["destination"]
    )
    stats[nearest_agent]["routes"].append(route)

# -----------------------------
# Generate Report
# -----------------------------
report = {}
best_agent = None
best_efficiency = float("inf")

for agent, data in stats.items():
    delivered = data["packages_delivered"]
    total_dist = round(data["total_distance"], 2)

    efficiency = round(total_dist / delivered, 2) if delivered > 0 else 0

    report[agent] = {
        "packages_delivered": delivered,
        "total_distance": total_dist,
        "efficiency": efficiency
    }

    if delivered > 0 and efficiency < best_efficiency:
        best_efficiency = efficiency
        best_agent = agent

report["best_agent"] = best_agent

# -----------------------------
# Save JSON Report
# -----------------------------
with open("report.json", "w") as file:
    json.dump(report, file, indent=4)

# -----------------------------
# Export Top Performer to CSV
# -----------------------------
with open("top_agent.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Agent", "Packages", "Total Distance", "Efficiency"])
    best = report[best_agent]
    writer.writerow([
        best_agent,
        best["packages_delivered"],
        best["total_distance"],
        best["efficiency"]
    ])

# -----------------------------
# ASCII Route Visualization
# -----------------------------
print("\n📦 DELIVERY ROUTES (ASCII)\n")
for agent, data in stats.items():
    for route in data["routes"]:
        print(f"{agent}: {route}")

print("\n✅ Simulation Complete")
print(f"🏆 Best Agent: {best_agent}")