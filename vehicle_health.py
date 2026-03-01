import random
import time


def generate_vehicle_data(prev_data=None):
    """Generate or slightly vary vehicle parameters.

    prev_data: dictionary of previous values; if provided we will
    make only small changes to simulate real driving.
    Returns a dict with engine_temp, battery, rpm, speed, fuel.
    """
    if prev_data is None:
        # start with random values within the valid ranges
        engine_temp = random.uniform(70, 120)
        battery = random.uniform(11.0, 14.5)
        rpm = random.uniform(800, 6000)
        speed = random.uniform(0, 120)
        fuel = random.uniform(0, 100)
    else:
        # vary the previous values slightly
        engine_temp = min(120, max(70, prev_data['engine_temp'] + random.uniform(-2, 2)))
        battery = min(14.5, max(11.0, prev_data['battery'] + random.uniform(-0.1, 0.1)))
        rpm = min(6000, max(800, prev_data['rpm'] + random.uniform(-100, 100)))
        speed = min(120, max(0, prev_data['speed'] + random.uniform(-5, 5)))
        fuel = min(100, max(0, prev_data['fuel'] + random.uniform(-1, 1)))

    return {
        'engine_temp': engine_temp,
        'battery': battery,
        'rpm': rpm,
        'speed': speed,
        'fuel': fuel,
    }


def evaluate_health(data):
    """Evaluate health status based on simple rules.

    Returns a string: 'Healthy', 'Warning', or 'Critical'.
    """
    critical = False
    warnings = 0

    if data['engine_temp'] > 110:
        # critical condition
        critical = True
    if data['battery'] < 11.5:
        warnings += 1
    if data['rpm'] > 5000:
        warnings += 1
    if data['fuel'] < 10:
        warnings += 1

    if critical or warnings >= 2:
        return 'Critical'
    if warnings == 1:
        return 'Warning'

    return 'Healthy'


def calculate_health_score(data):
    """Return an integer health score (0-100) computed from rules."""
    score = 100
    if data['engine_temp'] > 105:
        score -= 20
    if data['battery'] < 11.5:
        score -= 15
    if data['rpm'] > 5000:
        score -= 10
    if data['fuel'] < 10:
        score -= 5
    return max(0, score)


def main():
    """Entry point: continuously generate data and print status."""
    prev_data = None
    try:
        while True:
            prev_data = generate_vehicle_data(prev_data)
            score = calculate_health_score(prev_data)
            status = evaluate_health(prev_data)

            print("----------------------------")
            print(f"Engine Temp: {prev_data['engine_temp']:.1f} °C")
            print(f"Battery: {prev_data['battery']:.2f} V")
            print(f"RPM: {int(prev_data['rpm'])}")
            print(f"Speed: {prev_data['speed']:.1f} km/h")
            print(f"Fuel: {prev_data['fuel']:.1f} %")
            print(f"Health Score: {score}")
            print(f"Health Status: {status}")
            print("----------------------------")

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")


if __name__ == '__main__':
    main()
