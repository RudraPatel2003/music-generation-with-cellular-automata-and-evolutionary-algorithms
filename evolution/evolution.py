import random

from helpers.helper import generate_cellular_automata


def random_start_state(initial_state_1, initial_state_2):
    return random.choice([initial_state_1, initial_state_2])


def rule_crossover(rules_1, rules_2):
    return {key: random.choice([rules_1[key], rules_2[key]]) for key in rules_1}


def rule_mutations(rules):
    for key in rules:
        if random.random() < 0.05:  # 5% chance
            # Swap 0 with 1 and 1 with 0
            rules[key] = 1 if rules[key] == 0 else 0

    return rules


def generate_cellular_automata_with_evolution(
    cellular_automata_json_data_1, cellular_automata_json_data_2
):
    ca_1_initial_state = cellular_automata_json_data_1["initial_state"]
    ca_2_initial_state = cellular_automata_json_data_2["initial_state"]

    ca_1_rules = cellular_automata_json_data_1["rules"]
    ca_2_rules = cellular_automata_json_data_2["rules"]

    new_initial_state = random_start_state(ca_1_initial_state, ca_2_initial_state)
    new_rule = rule_crossover(ca_1_rules, ca_2_rules)
    new_rule = rule_mutations(new_rule)

    new_cellular_automata = {
        "rules": new_rule,
        "initial_state": new_initial_state,
        "width": cellular_automata_json_data_1["width"],
        "neighbor_size": cellular_automata_json_data_1["neighbor_size"],
        "steps": cellular_automata_json_data_1["steps"],
    }

    generate_cellular_automata(new_cellular_automata)
