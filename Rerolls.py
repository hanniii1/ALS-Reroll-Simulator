import numpy as np


techniques = [
    ("Scoped 1", 0.12),
    ("Scoped 2", 0.09),
    ("Scoped 3", 0.05),
    ("Accelerate 1", 0.10),
    ("Accelerate 2", 0.07),
    ("Accelerate 3", 0.04),
    ("Sturdy 1", 0.10),
    ("Sturdy 2", 0.07),
    ("Sturdy 3", 0.04),
    ("Shining", 0.09),
    ("EagleEye", 0.04),
    ("Golden", 0.035),
    ("HyperSpeed", 0.03),
    ("Juggernaut", 0.03),
    ("ElementalMaster", 0.02),
    ("Vulture", 0.0225),
    ("Diamond", 0.0175),
    ("Cosmic", 0.01),
    ("Demigod", 0.01),
    ("AllSeeing", 0.0035),
    ("Entrepreneur", 0.003),
    ("Shinigami", 0.002),
    ("Overlord", 0.002),
    ("Avatar", 0.001),
    ("Glitched", 0.0003),
]


technique_names = [technique[0] for technique in techniques]
technique_probabilities = [technique[1] for technique in techniques]


total_probability = sum(technique_probabilities)
if total_probability != 1.0:
    technique_probabilities = [p / total_probability for p in technique_probabilities]

def get_input(prompt):
    """Helper function to get input from the user."""
    return input(prompt).strip()


print("=========================================")
print("   Welcome to ALS Reroll Simulator!    ")
print("=========================================")
print("This simulator allows you to reroll")
print("for specific traits with various probabilities.")
print("You can also apply a luck multiplier to improve your chances.")
print("=========================================")


desired_trait = get_input("Enter the desired trait: ")
num_simulations = int(get_input("Enter the number of simulations: "))
num_trials = int(get_input("Enter the number of trials per simulation: "))
use_luck_multiplier = get_input("Do you want to apply x4 luck? (yes/no): ").lower()


all_roll_offs_counts = []
all_rolled_off_traits = []
all_rolls_to_get_desired_trait = []


low_probability_threshold = 0.002  # 0.2% probability


for sim in range(num_simulations):
    roll_offs_count = 0
    rolled_off_traits = []  # Store rolled-off traits
    rolls_to_get_desired_trait = 0  # Track rolls to get the desired trait
    desired_trait_found = False

    for trial in range(num_trials):
        # Apply luck multiplier
        if use_luck_multiplier == "yes":
            current_probabilities = [min(p * 4, 1.0) for p in technique_probabilities]
            total_probability = sum(current_probabilities)
            current_probabilities = [p / total_probability for p in current_probabilities]
        else:
            current_probabilities = technique_probabilities  # Use original probabilities

        current_trait = np.random.choice(technique_names, p=current_probabilities)
        rolls_to_get_desired_trait += 1 

        if current_trait != desired_trait:
            if current_probabilities[technique_names.index(current_trait)] <= low_probability_threshold:
                roll_offs_count += 1
                rolled_off_traits.append(current_trait)  # Log rolled-off trait
        else:
            # Desired trait obtained oh yes glitched!
            desired_trait_found = True
            break

    all_roll_offs_counts.append(roll_offs_count)
    all_rolled_off_traits.append(rolled_off_traits)
    all_rolls_to_get_desired_trait.append(rolls_to_get_desired_trait)

    # Print results for the current simulation
    obtained_trait = "Yes" if desired_trait_found else "No"
    rolled_off_traits_str = ", ".join(rolled_off_traits) if rolled_off_traits else "None"
    
    print(f"\n{'-'*30}")
    print(f"Simulation {sim + 1} Results:")
    print(f"{'-'*30}")
    print(f"Did we get the desired trait '{desired_trait}': {obtained_trait}")
    print(f"Total low-probability roll offs: {roll_offs_count}")
    print(f"Rolled off traits (<= 0.2%): {rolled_off_traits_str}")
    print(f"Total rolls to get '{desired_trait}': {rolls_to_get_desired_trait}")
    print(f"{'-'*30}")

# Calculate and display mean and standard deviation for roll offs and desired trait
mean_roll_offs_counts = np.mean(all_roll_offs_counts)
std_dev_roll_offs_counts = np.std(all_roll_offs_counts)
mean_rolls_to_get_desired_trait = np.mean(all_rolls_to_get_desired_trait)
std_dev_rolls_to_get_desired_trait = np.std(all_rolls_to_get_desired_trait)

print(f"\n{'='*40}")
print(f"Overall Results for getting '{desired_trait}':")
print(f"{'='*40}")
print(f"Mean number of roll offs of techniques <= 0.2%: {mean_roll_offs_counts:.2f}")
print(f"Standard deviation of roll offs of techniques <= 0.2%: {std_dev_roll_offs_counts:.2f}")
print(f"Mean rolls to get '{desired_trait}': {mean_rolls_to_get_desired_trait:.2f}")
print(f"Standard deviation of rolls to get '{desired_trait}': {std_dev_rolls_to_get_desired_trait:.2f}")
print(f"{'='*40}")
