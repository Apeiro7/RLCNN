import traci
import sumolib
import pandas as pd

# Initialize SUMO simulation with TraCI
def run_sumo_simulation(sumo_binary, config_file, output_csv_file):
    # Start SUMO as a subprocess
    traci.start([sumo_binary, "-c", config_file])

    # Create a list to store each step's data
    simulation_data = []

    try:
        step = 0
        while traci.simulation.getMinExpectedNumber() > 0:  # Run until all vehicles have left
            traci.simulationStep()  # Advance the simulation by one step
            
            # Collect data for the current step
            vehicle_ids = traci.vehicle.getIDList()  # Get all vehicle IDs at the current step
            vehicle_count = len(vehicle_ids)
            avg_speed = sum(traci.vehicle.getSpeed(veh) for veh in vehicle_ids) / vehicle_count if vehicle_count > 0 else 0

            avg_waiting_time = sum(traci.vehicle.getWaitingTime(veh) for veh in vehicle_ids) / vehicle_count if vehicle_count > 0 else 0
            avg_travel_time = sum(traci.vehicle.getAccumulatedWaitingTime(veh) for veh in vehicle_ids) / vehicle_count if vehicle_count > 0 else 0

            # Traffic light state
            traffic_light_ids = traci.trafficlight.getIDList()
            traffic_light_states = {tl: traci.trafficlight.getRedYellowGreenState(tl) for tl in traffic_light_ids}
            
            # Add the data to the simulation_data list
            simulation_data.append({
                'step': step,
                'vehicle_count': vehicle_count,
                'avg_speed': avg_speed,
                'avg_waiting_time': avg_waiting_time,
                'avg_travel_time': avg_travel_time,
                'traffic_light_states': traffic_light_states
            })

            step += 1

    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        # Close the TraCI connection and simulation
        traci.close()

        # Save the collected data to a CSV file
        df = pd.DataFrame(simulation_data)
        df.to_csv(output_csv_file, index=False)
        print(f"Data saved to {output_csv_file}")

if __name__ == "__main__":
    # Define the SUMO binary and the SUMO config file (change the paths as necessary)
    sumo_binary = sumolib.checkBinary('sumo')  # or 'sumo-gui' for GUI mode
    config_file = "path_to_your_sumo_config_file.sumocfg"
    output_csv_file = "sumo_simulation_data.csv"
    
    # Run the simulation and collect the data
    run_sumo_simulation(sumo_binary, config_file, output_csv_file)
