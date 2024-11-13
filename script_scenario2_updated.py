import traci
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# Charger les capacités des parkings depuis le fichier XML
parking_capacities = {}
try:
    tree = ET.parse("parking_parking1.add.xml")
    root = tree.getroot()
    for parking in root.findall("parkingArea"):
        parking_id = parking.get("id")
        capacity = int(parking.get("capacity"))
        parking_capacities[parking_id] = capacity
except FileNotFoundError:
    print("Erreur : Le fichier parking_parking1.add.xml est introuvable.")
    exit(1)

# Configuration SUMO
sumo_binary = "sumo-gui"
sumo_cmd = [
    sumo_binary,
    "-c", "configuration.sumocfg",
    "--additional-files", "parking_parking1.add.xml",
    "--emission-output", "emissions_scenario2.xml",
    "--tripinfo-output", "tripinfo_scenario2.xml"
]

# Démarrer TraCI
traci.start(sumo_cmd)

# Variables pour stocker les données
parking_data = []
emissions_data = []

# Seuil de redirection
threshold = 0.8  # Redirection si parking1 atteint 80% de sa capacité

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    # Collecter l'état des parkings
    for parking_id in traci.parkingarea.getIDList():
        time = traci.simulation.getTime()
        occupied = traci.parkingarea.getVehicleCount(parking_id)
        capacity = parking_capacities.get(parking_id, 0)
        parking_data.append({"time": time, "parking_id": parking_id, "occupied": occupied, "capacity": capacity})

    # Redirection dynamique
    for vehicle_id in traci.vehicle.getIDList():
        stops = traci.vehicle.getStops(vehicle_id)
        if stops:
            stop = stops[0]
            parking_id = stop.stoppingPlaceID
            if parking_id == "parking1" and (traci.parkingarea.getVehicleCount(parking_id) / parking_capacities[parking_id]) >= threshold:
                if traci.parkingarea.getVehicleCount("parking2") < parking_capacities["parking2"]:
                    try:
                        traci.vehicle.changeTarget(vehicle_id, traci.parkingarea.getLaneID("parking2").split("_")[0])
                    except traci.TraCIException as e:
                        print(f"Erreur lors de la redirection : {e}")

    # Collecter les émissions de CO2
    for vehicle_id in traci.vehicle.getIDList():
        co2_emission = traci.vehicle.getCO2Emission(vehicle_id)
        time = traci.simulation.getTime()
        emissions_data.append({"time": time, "vehicle_id": vehicle_id, "co2_emission": co2_emission})

# Fermer TraCI
traci.close()

# Analyse des résultats
parking_df = pd.DataFrame(parking_data)
emissions_df = pd.DataFrame(emissions_data)
parking_df["occupancy_rate"] = (parking_df["occupied"] / parking_df["capacity"]) * 100

# Visualisations
for parking_id, group in parking_df.groupby("parking_id"):
    plt.plot(group["time"], group["occupancy_rate"], label=f"Parking {parking_id}")
plt.xlabel("Temps (s)")
plt.ylabel("Taux d'occupation (%)")
plt.title("Taux d'occupation des parkings")
plt.legend()
plt.show()

# Charger le fichier tripinfo.xml pour analyser les trajets
tripinfo_df = pd.read_xml("tripinfo_scenario2.xml")

# Sauvegarder les données en CSV
parking_df.to_csv("parking_occupancy_scenario2.csv", index=False)
emissions_df.to_csv("emissions_scenario2.csv", index=False)
tripinfo_df.to_csv("tripinfo_scenario2.csv", index=False)

# Visualiser les résultats

# 1. Évolution des taux d'occupation des parkings
for parking_id, group in parking_df.groupby("parking_id"):
    plt.plot(group["time"], group["occupancy_rate"], label=f"Parking {parking_id}")

plt.xlabel("Temps (s)")
plt.ylabel("Taux d'occupation (%)")
plt.title("Évolution des taux d'occupation des parkings")
plt.legend()
plt.show()

# 2. Émissions totales de CO2 au cours du temps
emissions_total = emissions_df.groupby("time")["co2_emission"].sum()
plt.plot(emissions_total.index, emissions_total.values)
plt.xlabel("Temps (s)")
plt.ylabel("CO2 (mg)")
plt.title("Émissions totales de CO2 au cours du temps")
plt.show()

# 3. Distribution des durées de trajet
plt.hist(tripinfo_df["duration"], bins=20, edgecolor="k")
plt.xlabel("Durée du trajet (s)")
plt.ylabel("Nombre de trajets")
plt.title("Distribution des durées de trajet")
plt.show()
