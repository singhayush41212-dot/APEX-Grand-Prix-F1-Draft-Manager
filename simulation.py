import random

def simulate_season(team):
    """Simulates a dynamic 20-race F1 season incorporating driver, car, and principal metrics."""
    d1 = team.driver1
    d2 = team.driver2
    car = team.car
    p = team.principal
    
    custom_name = getattr(team, 'name', "YOUR DRAFT TEAM")
    if not custom_name or custom_name.strip() == "":
        custom_name = "YOUR DRAFT TEAM"
    
    car_base_perf = min(99, car.ovr)
    base_driver_perf = (min(95, d1.ovr) + min(95, d2.ovr)) / 2
    base_strength = (car_base_perf * 0.50) + (base_driver_perf * 0.35) + (p.ovr * 0.15)
    
    trait_bonus = 0
    if "+" in p.special:
        try:
            parts = p.special.split("+")
            trait_bonus = float(parts[1].split()[0]) * 0.50
        except Exception:
            trait_bonus = 0
            
    user_team_strength = base_strength + trait_bonus

    races_config = [
        {"name": "Bahrain", "type": "balanced"},
        {"name": "Saudi Arabia", "type": "speed"},
        {"name": "Australia", "type": "balanced"},
        {"name": "Japan", "type": "speed"},
        {"name": "Miami", "type": "speed"},
        {"name": "Monaco", "type": "street"},
        {"name": "Canada", "type": "speed"},
        {"name": "Spain", "type": "balanced"},
        {"name": "Austria", "type": "balanced"},
        {"name": "Great Britain", "type": "speed"},
        {"name": "Hungary", "type": "street"},
        {"name": "Belgium", "type": "speed"},
        {"name": "Netherlands", "type": "street"},
        {"name": "Italy", "type": "speed"},
        {"name": "Azerbaijan", "type": "speed"},
        {"name": "Singapore", "type": "street"},
        {"name": "Austin", "type": "balanced"},
        {"name": "Mexico", "type": "balanced"},
        {"name": "Brazil", "type": "balanced"},
        {"name": "Abu Dhabi", "type": "balanced"}
    ]
    
    # Points awarded for positions 1-10; remaining 14 grid slots receive 0 points
    points_tier = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1] + [0] * 14
    
    base_grid = [
        {"d_name": d1.name, "team_name": custom_name, "driver_ovr": d1.ovr, "car_perf": user_team_strength, "archetype": "user"},
        {"d_name": d2.name, "team_name": custom_name, "driver_ovr": d2.ovr, "car_perf": user_team_strength, "archetype": "user"},
        {"d_name": "Max Verstappen", "team_name": "Red Bull Racing", "driver_ovr": 98, "car_perf": 94, "archetype": "speed"},
        {"d_name": "Isack Hadjar", "team_name": "Red Bull Racing", "driver_ovr": 84, "car_perf": 94, "archetype": "speed"},
        {"d_name": "Lewis Hamilton", "team_name": "Ferrari Core", "driver_ovr": 94, "car_perf": 93, "archetype": "balanced"},
        {"d_name": "Charles Leclerc", "team_name": "Ferrari Core", "driver_ovr": 95, "car_perf": 93, "archetype": "balanced"},
        {"d_name": "Lando Norris", "team_name": "McLaren Papaya", "driver_ovr": 94, "car_perf": 93.5, "archetype": "street"},
        {"d_name": "Oscar Piastri", "team_name": "McLaren Papaya", "driver_ovr": 92, "car_perf": 93.5, "archetype": "street"},
        {"d_name": "George Russell", "team_name": "Mercedes AMG", "driver_ovr": 92, "car_perf": 88, "archetype": "balanced"},
        {"d_name": "Kimi Antonelli", "team_name": "Mercedes AMG", "driver_ovr": 85, "car_perf": 88, "archetype": "balanced"},
        {"d_name": "Fernando Alonso", "team_name": "Aston Martin", "driver_ovr": 89, "car_perf": 84, "archetype": "street"},
        {"d_name": "Lance Stroll", "team_name": "Aston Martin", "driver_ovr": 78, "car_perf": 84, "archetype": "street"},
        {"d_name": "Pierre Gasly", "team_name": "Alpine Renault", "driver_ovr": 85, "car_perf": 80, "archetype": "balanced"},
        {"d_name": "Franco Colapinto", "team_name": "Alpine Renault", "driver_ovr": 82, "car_perf": 80, "archetype": "balanced"},
        {"d_name": "Carlos Sainz", "team_name": "Williams Racing", "driver_ovr": 88, "car_perf": 78, "archetype": "speed"},
        {"d_name": "Alexander Albon", "team_name": "Williams Racing", "driver_ovr": 86, "car_perf": 78, "archetype": "speed"},
        {"d_name": "Esteban Ocon", "team_name": "Haas F1 Team", "driver_ovr": 84, "car_perf": 76, "archetype": "speed"},
        {"d_name": "Oliver Bearman", "team_name": "Haas F1 Team", "driver_ovr": 82, "car_perf": 76, "archetype": "speed"},
        {"d_name": "Liam Lawson", "team_name": "Racing Bulls", "driver_ovr": 83, "car_perf": 75, "archetype": "street"},
        {"d_name": "Arvid Lindblad", "team_name": "Racing Bulls", "driver_ovr": 80, "car_perf": 75, "archetype": "street"},
        {"d_name": "Nico Hülkenberg", "team_name": "Sauber Audi", "driver_ovr": 84, "car_perf": 72, "archetype": "balanced"},
        {"d_name": "Gabriel Bortoleto", "team_name": "Sauber Audi", "driver_ovr": 79, "car_perf": 72, "archetype": "balanced"},
        {"d_name": "Sergio Pérez", "team_name": "Cadillac F1", "driver_ovr": 86, "car_perf": 74, "archetype": "street"},
        {"d_name": "Valtteri Bottas", "team_name": "Cadillac F1", "driver_ovr": 85, "car_perf": 74, "archetype": "balanced"}
    ]

    drafted_names = [d1.name.strip().lower(), d2.name.strip().lower()]
    reserve_drivers = {
        "Red Bull Racing": ("Yuki Tsunoda", 85), "Ferrari Core": ("Antonio Giovinazzi", 80),
        "McLaren Papaya": ("Pato O'Ward", 81), "Mercedes AMG": ("Mick Schumacher", 80),
        "Aston Martin": ("Jak Crawford", 76), "Alpine Renault": ("Victor Martins", 75),
        "Williams Racing": ("Logan Sargeant", 77), "Haas F1 Team": ("Pietro Fittipaldi", 74),
        "Racing Bulls": ("Ayumu Iwasa", 76), "Sauber Audi": ("Théo Pourchaire", 78),
        "Cadillac F1": ("Zhou Guanyu", 80)
    }

    active_grid = []
    for driver in base_grid:
        if driver["team_name"] == custom_name:
            active_grid.append(driver)
        elif driver["d_name"].strip().lower() in drafted_names:
            r_name, r_ovr = reserve_drivers.get(driver["team_name"], ("Reserve Driver", 75))
            active_grid.append({
                "d_name": r_name, "team_name": driver["team_name"], "driver_ovr": r_ovr, "car_perf": driver["car_perf"], "archetype": driver["archetype"]
            })
        else:
            active_grid.append(driver)

    driver_points_map = {d["d_name"]: 0 for d in active_grid}
    constructor_points_map = {d["team_name"]: 0 for d in active_grid}
    user_d1_races, user_d2_races, user_wins = [], [], 0
    races_names_list = []
    all_race_results = []

    for config in races_config:
        race_name = config["name"]
        track_type = config["type"]
        races_names_list.append(race_name)
        
        race_weekend_results = []
        ai_progression_shift = random.uniform(-1.5, 2.5)
        
        for driver in active_grid:
            current_perf = driver["car_perf"]
            
            if driver["archetype"] == "user":
                if "aero" in p.special.lower() and track_type == "street": current_perf += 1.5
                elif "speed" in p.special.lower() and track_type == "speed": current_perf += 1.5
            elif driver["archetype"] == track_type:
                current_perf += random.uniform(1.5, 3.5)
            elif driver["archetype"] != "user":
                current_perf += ai_progression_shift
                
            base_form = (current_perf * 0.60) + (driver["driver_ovr"] * 0.40)
            weekend_roll = base_form + random.randint(-15, 9)
            
            if random.random() < 0.12:
                weekend_roll -= random.randint(5, 15)
                
            is_user_driver = driver["team_name"] == custom_name
            is_dnf = random.random() < (0.07 if is_user_driver else 0.04)
            
            race_weekend_results.append({
                "d_name": driver["d_name"], "team_name": driver["team_name"], "score": -999 if is_dnf else weekend_roll
            })
            
        race_weekend_results = sorted(race_weekend_results, key=lambda x: x["score"], reverse=True)
        
        formatted_round_results = []
        for position_index, runner in enumerate(race_weekend_results):
            points_awarded = points_tier[position_index] if position_index < len(points_tier) else 0
            driver_points_map[runner["d_name"]] += points_awarded
            constructor_points_map[runner["team_name"]] += points_awarded
            formatted_round_results.append((runner["d_name"], runner["team_name"], points_awarded))
            
            if runner["d_name"] == d1.name:
                user_d1_races.append(points_awarded)
                if position_index == 0: user_wins += 1
            elif runner["d_name"] == d2.name:
                user_d2_races.append(points_awarded)
                if position_index == 0: user_wins += 1

        all_race_results.append(formatted_round_results)

    compiled_drivers = [(d["d_name"], driver_points_map[d["d_name"]], d["team_name"]) for d in active_grid]
    compiled_drivers = sorted(compiled_drivers, key=lambda x: x[1], reverse=True)
    
    compiled_constructors = [{"name": c_name, "pts": pts} for c_name, pts in constructor_points_map.items()]
    compiled_constructors = sorted(compiled_constructors, key=lambda x: x["pts"], reverse=True)
    
    your_c_pos = next(i for i, t in enumerate(compiled_constructors, 1) if t["name"] == custom_name)
    constructor_total = constructor_points_map[custom_name]

    user_drivers = [d1.name, d2.name]
    top_driver_on_grid = compiled_drivers[0][0]
    user_driver_won_wdc = top_driver_on_grid in user_drivers
    team_suffered_dnfs = user_d1_races.count(0) > 3 or user_d2_races.count(0) > 3
    total_d1, total_d2 = sum(user_d1_races), sum(user_d2_races)
    severe_driver_performance_gap = abs(total_d1 - total_d2) > 100
    
    if your_c_pos == 1 and user_driver_won_wdc:
        feedback = f"COMPLETE DOMINANCE. Powered by the legendary {car.name}, {custom_name.upper()} clean-swept both titles! {p.name} masterfully managed the team to maximize performance."
    elif your_c_pos > 1 and user_driver_won_wdc:
        feedback = f"BITTERSWEET TRIUMPH. {top_driver_on_grid.upper()} is the Drivers' World Champion in the {car.name}! However, {custom_name.upper()} missed out on the Constructors' crown due to unbalanced scoring."
    elif your_c_pos == 1 and not user_driver_won_wdc:
        feedback = f"TEAM EFFORT. {custom_name.upper()} are the Constructors' World Champions! Superb tactical coordination from {p.name} secured the shield with the {car.name}."
    elif team_suffered_dnfs and constructor_total < 80:
        feedback = f"RELIABILITY CRISIS. Mechanical degradation completely derailed your campaign with the {car.name}. {p.name}'s development map failed to protect hardware."
    elif severe_driver_performance_gap and your_c_pos <= 4:
        higher_driver = d1.name if total_d1 > total_d2 else d2.name
        lower_driver = d2.name if total_d1 > total_d2 else d1.name
        feedback = f"UNBALANCED LINEUP. A strong P{your_c_pos} finish, but your team was heavily carried by {higher_driver.upper()}. {lower_driver.upper()} struggled in the {car.name}."
    elif your_c_pos <= 3:
        feedback = f"CHAMPIONSHIP CONTENDERS. A strong P{your_c_pos} finish on the grid with the {car.name}. Regular podiums proved consistent engineering."
    elif constructor_total > 30:
        feedback = f"MIDFIELD STANZA. The {car.name} scraped into scoring positions on selective tracks, leaving you locked in the tight midfield."
    else:
        feedback = f"DEVELOPMENT FAILURE. Severe performance deficits from the {car.name} left you stranded at the back of the grid."

    return {
        "total_points": constructor_total, 
        "wins": user_wins, 
        "strength": user_team_strength,
        "feedback": feedback, 
        "team_name": custom_name, 
        "c_pos": your_c_pos, 
        "races": races_names_list,
        "d1_name": d1.name, 
        "d2_name": d2.name, 
        "car_name": car.name, 
        "d1_pts_list": user_d1_races, 
        "d2_pts_list": user_d2_races,
        "driver_standings": compiled_drivers, 
        "constructor_standings": [(c["name"], c["pts"]) for c in compiled_constructors],
        "race_results": all_race_results
    }