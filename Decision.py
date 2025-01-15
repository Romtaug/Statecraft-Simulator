import random

class Government:
    def __init__(self):
        self.treasury = 20000
        self.health_budget = 1000
        self.military_budget = 1500
        self.security_budget = 500
        self.education_budget = 800
        self.economic_growth = 0.03
        self.presidential_approval = 70
        self.international_relations = 80
        self.environmental_health = 85
        self.policies = {
            '1': ('health_budget', self.adjust_budget),
            '2': ('military_budget', self.adjust_budget),
            '3': ('security_budget', self.adjust_budget),
            '4': ('education_budget', self.adjust_budget),
            '5': ('tax_increase', self.adjust_taxes),
            '6': ('none', self.no_action)
        }

    def adjust_budget(self, budget_name, amount):
        current_value = getattr(self, budget_name)
        new_value = max(0, current_value + amount)
        setattr(self, budget_name, new_value)
        self.treasury -= amount
        self.update_approval(-amount / 200)  # Adjust approval less aggressively
        print(f"{budget_name} adjusted by {amount}. New budget: {new_value}.")

    def adjust_taxes(self, amount):
        self.treasury += amount
        self.update_approval(amount / 200)  # More positive adjustment for increasing taxes
        print(f"Taxes adjusted by {amount}. Treasury now {self.treasury}.")

    def no_action(self, amount=None):
        print("No action taken this turn.")

    def update_approval(self, change):
        self.presidential_approval = max(0, min(100, self.presidential_approval + change))
        print(f"Presidential approval updated to: {self.presidential_approval}%")

    def update_economic_status(self):
        self.treasury += int(self.treasury * self.economic_growth)
        self.treasury = max(0, self.treasury)  # Ensure treasury doesn't go negative
        print(f"End of turn: Treasury is {self.treasury}, Economic Growth is {self.economic_growth:.2%}")

class Population:
    def __init__(self):
        self.happiness = 70
        self.health = 80

    def adjust_happiness(self, impact):
        self.happiness = max(0, min(100, self.happiness + impact))
        print(f"Population happiness is now {self.happiness}%.")

class World:
    def __init__(self, government, population):
        self.government = government
        self.population = population

    def simulate_turn(self):
        print("\n--- New Government Turn ---")
        self.display_current_state()
        if random.random() < 0.4:  # Adjusted to occur more frequently
            self.random_event()

        self.user_decision()
        self.government.update_economic_status()

    def display_current_state(self):
        print("Current Treasury: ${:,}".format(self.government.treasury))
        print("Health Budget: ${:,}, Military Budget: ${:,}".format(
            self.government.health_budget, self.government.military_budget))
        print("Security Budget: ${:,}, Education Budget: ${:,}".format(
            self.government.security_budget, self.government.education_budget))
        print(f"Economic Growth: {self.government.economic_growth:.2%}, Approval: {self.government.presidential_approval}%")

    def random_event(self):
        events = {
            "economic": self.handle_economic_crisis,
            "pandemic": self.handle_pandemic,
            "war": self.handle_war
        }
        event_type = random.choice(list(events.keys()))
        events[event_type]()

    def handle_economic_crisis(self):
        impact = random.randint(-1000, -500)
        self.government.treasury += impact
        self.population.adjust_happiness(-5)
        print(f"Economic crisis! Treasury impact: {impact}, new treasury: {self.government.treasury}")

    def handle_pandemic(self):
        health_impact = -15
        self.population.health += health_impact
        self.government.health_budget += 1000  # Immediate increase in health spending
        print(f"Pandemic outbreak! Health impact: {health_impact}, increased health budget.")

    def handle_war(self):
        military_spending = 2000
        self.government.military_budget += military_spending
        self.population.adjust_happiness(-10)
        print(f"War declared! Military spending increased by {military_spending}.")

    def user_decision(self):
        print("Choose a policy to implement:")
        for key, (name, _) in self.government.policies.items():
            print(f"{key}: {name.replace('_', ' ').title()}")
        choice = input("Enter your choice (or 'none'): ")
        if choice in self.government.policies:
            policy = self.government.policies[choice]
            if policy[0] != 'none':
                amount = int(input(f"Enter the amount for {policy[0]}: "))
                policy[1](policy[0], amount)
            else:
                policy[1]()
        else:
            print("Invalid policy choice. No action taken.")

# Setup
government = Government()
population = Population()
world_sim = World(government, population)

# Simulation execution
for _ in range(30):  # Simulate 30 turns for a longer game
    world_sim.simulate_turn()
