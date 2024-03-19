from cognata_api.web_api.cognata_demo import CognataRequests
import numpy as np
import pandas as pd
import uuid
import math

def get_api(username="apiuser", password="Aa123456", company_id="2a4ab8d2"):
        """
        Args:
            username (str, optional): Cognata Studio Username. Defaults to "apiuser".
            password (str, optional): Cognata Studio Password. Defaults to "Aa123456".
            company_id (str, optional): Cognata Studio Company ID. Defaults to "2a4ab8d2".

        Raises:
            ValueError: Either username or password are wrong

        Returns:
            CognataRequests: the API object that makes the request to Cognata 
        """
        connection = CognataRequests(
            f"https://{company_id}-api.cognata-studio.com/v1", username, password)
        if not connection.is_logged_in:
            raise ValueError("Either username / password is wrong.")
        return connection

def create_sensor(api: CognataRequests, sensor: dict):
    url = f"{api.client_api_url}/catalog/egocar"
    return api._perform_post_request(url, sensor)

def delete_sensor(api: CognataRequests, sensor_sku: str):
    import json
    url = f"{api.client_api_url}/catalog/egocar/{sensor_sku}"
    try:
        return api._perform_delete_request(url)
    except json.decoder.JSONDecodeError:
        print(f"Sensor {sensor_sku} was deleted.")

def generate_sensor_data(api: CognataRequests, p_noise: float, t_noise: float, Y_noise: float, Z_noise: float) -> dict:
    random_id = str(uuid.uuid4())[:8]
    edited_sensor = api.get_sensor(sensor_type='egocar', sensor_sku='SUVVELON14').copy()
    del edited_sensor['aicar']
    del edited_sensor['catalogData']['sku']
    edited_sensor['catalogData']['name'] = f"Noise_P:{p_noise}_T:{t_noise}_{random_id}"
    edited_sensor['properties']['sensors'][4]['sensor_data']['scanning_pattern_phi'] = p_noise
    edited_sensor['properties']['sensors'][4]['sensor_data']['scanning_pattern_theta'] = t_noise
    edited_sensor['properties']['sensors'][4]['sensor_data']['pointCloudY'] = Y_noise #new noise parameter
    edited_sensor['properties']['sensors'][4]['sensor_data']['pointCloudZ'] = Z_noise #new noise parameter
    return edited_sensor

def generate_sim(api: CognataRequests, sensor_sku: str, p_noise: float, t_noise: float, Y_noise: float, Z_noise: float): #adding y parameter
    formula = api.find_scenario('64febeae3c17c100304b2cb1')
    formula['name'] = f"Noise Study [P: {round(p_noise,3)}, T: {round(t_noise,3)}, Y: {round(Y_noise,5)},Z: {round(Z_noise,5)}]"
    formula['ego_car']['ego_car_sku'] = sensor_sku
    formula['tags'].append(f"P: {p_noise}")
    formula['tags'].append(f"T: {t_noise}")
    formula['tags'].append(f"Y: {Y_noise}")
    formula['tags'].append(f"Z: {Z_noise}")
    

    response = api.generate_simulation(formula,running_priority=10000)
    return api.get_simulation_run_id(response) if response else None

def generate_sensor_and_sim_after(p_noise: float, t_noise: float, Y_noise: float, Z_noise: float): #adding y parameter
    api = get_api()
    sensor_data = generate_sensor_data(api, p_noise, t_noise, Y_noise, Z_noise)
    created_sensor = create_sensor(api, sensor_data)
    sku = created_sensor['sku']
    run_id = generate_sim(api, sku, p_noise, t_noise, Y_noise, Z_noise)
    delete_sensor(api, sku)
    return run_id

#runer for angles noises
def run_phi_theta():
    sim_dict = {}
    p_noises = np.linspace(0, 0.07, 100)
    t_noises = np.linspace(0, 0.6, 100)
    index = 0
    for p_noise,t_noise in zip(p_noises, t_noises):
        run_id1 = generate_sensor_and_sim_after(p_noise, 0, 0)
        run_id2 = generate_sensor_and_sim_after(0, t_noise, 0)
        sim_dict[index] = [f'Phi_{p_noise}',run_id1]
        index+=1
        sim_dict[index] = [f'Theta_{t_noise}',run_id2]
        index+=1    
    print(sim_dict)
    df = pd.DataFrame(data=sim_dict)
    df = df.transpose()
    df.to_csv('run_id_list_Angle.csv')
    print(df)

#runer for pointCloud noises
def run_pointCloud():
    sim_dict = {}
    noises = np.linspace(0, 0.005, 100) 
    index = 0
    for n in noises:
        run_id1 = generate_sensor_and_sim_after(0, 0, n, 0 )
        sim_dict[index] = [f'PointCloudY_{n}',run_id1]
        index+=1 
    # print(sim_dict)
    df = pd.DataFrame(data=sim_dict)
    df = df.transpose()
    df.to_csv('run_ids/run_id_list_PointCloudY.csv')
    print(df)

if __name__ == '__main__':
    #run_phi_theta()
    run_pointCloud()
