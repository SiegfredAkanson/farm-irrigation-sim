import random
import time

class EdgeIrrigationBrain:
    def __init__(self, crop_stage="flowering"):
        # crop_stage can be: "seedling", "vegetative", "flowering"
        self.crop_stage = crop_stage

    def evaluate_sensors(self, soil_moisture, temp, humidity, is_night):
        need_score = 0

        # 1. Soil Moisture Logic
        if soil_moisture < 30:
            need_score += 50  # Critically dry
        elif soil_moisture < 50:
            need_score += 30  # Getting dry
        else:
            need_score += 0  # Soil is wet enough

        # 2. Temperature & Evaporation Context
        if temp > 35:
            need_score += 20  # Extreme heat, high evaporation
        elif temp > 28:
            need_score += 10  # Warm day

        # 3. Humidity Context
        if humidity < 40:
            need_score += 10  # Dry air sucks moisture out of soil quickly

        # 4. Time of Day Context (Efficiency optimization)
        if is_night:
            # Watering at night is efficient (less evaporation),
            # but we boost it slightly only if soil is actually dry.
            if soil_moisture < 50:
                need_score += 10
        else:
            # Midday sun might scorch plants or waste water via evaporation
            if temp > 35:
                need_score -= 10  # Deduct score to delay watering until cooler if possible

        # 5. Crop Life-Cycle Context
        if self.crop_stage == "flowering":
            need_score += 15  # Flowering stage requires peak, uninterrupted moisture
        elif self.crop_stage == "seedling":
            need_score += 5  # Seedlings need gentle, frequent moisture

        return min(need_score, 100)  # Cap at 100

    def calculate_duration(self, need_score, temp):
        if need_score < 50:
            return 0  # No watering needed

        # Base duration in minutes
        base_duration = 5

        if need_score > 80:
            base_duration += 10
        elif need_score > 60:
            base_duration += 5

        # Add environmental compensation (if scorching hot, add a bit more water)
        if temp > 35:
            base_duration += 3

        return base_duration

def run_farm_simulation():
    # Initialize our edge device
    edge_device = EdgeIrrigationBrain(crop_stage="flowering")

    print("=" * 60)
    print("STARTING EDGE-AI CONTEXT-AWARE IRRIGATION SIMULATION")
    print(f"Crop Stage: {edge_device.crop_stage.upper()}")
    print("=" * 60)

    # Simulate a 24-hour cycle (1 loop = 1 hour)
    for hour in range(6, 30):  # Simulating from 6 AM today to 5 AM tomorrow
        current_hour = hour % 24
        is_night = current_hour < 6 or current_hour > 18

        # Simulate dynamic environmental changes throughout the day
        if is_night:
            temp = random.randint(20, 24)
            humidity = random.randint(75, 90)
        else:  # Daytime peaks around 14:00 (2 PM)
            temp = random.randint(28, 38) if 11 <= current_hour <= 15 else random.randint(25, 30)
            humidity = random.randint(40, 60) if 11 <= current_hour <= 15 else random.randint(60, 75)

        # Simulate soil drying out over time, with a chance of random levels
        soil_moisture = max(20, 70 - (hour - 6) * 2 + random.randint(-5, 5))

        score = edge_device.evaluate_sensors(soil_moisture, temp, humidity, is_night)
        duration = edge_device.calculate_duration(score, temp)

        time_str = f"{current_hour:02d}:00"
        period = "NIGHT" if is_night else "DAY "

        print(f"[{time_str} | {period}] Temp: {temp}°C | Humid: {humidity}% | Soil Moist: {soil_moisture}%")
        print(f"       -> Edge Brain Score: {score}/100")

        if duration > 0:
            print(f"       => [PUMP ON] Applying precision watering for {duration} minutes.")
            # Simulate the soil absorbing water, resetting moisture for the next hour
            soil_moisture = min(85, soil_moisture + (duration * 3))
        else:
            print("       => [PUMP OFF] Water conserved.")
        print("-" * 60)

        time.sleep(0.5)  # Pause briefly so humans can read the simulation logs

if __name__ == "__main__":
    run_farm_simulation()