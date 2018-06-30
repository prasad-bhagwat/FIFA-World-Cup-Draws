# Imports required for the program
import sys
import itertools as iter
import copy
from sympy.logic.algorithms.dpll import dpll_int_repr


# MACRO definitions used in the program
ENCODE_FACTOR = 1000


# Reading input file and assigning values to variables
def read_file(input_file):
    global group_count, pots_count, country_pots, country_regions, countries, knowledge_base, country_geography
    group_count, pots_count = 0, 0
    country_pots, country_regions, countries, country_geography, knowledge_base = [], [], [1], [], []

    with open(input_file, "r") as f:
        data 		= f.read().strip().split('\n')
        group_count 	= int(data[0])                                                                        # Groups count
        pots_count 	= int(data[1])                                                                         # Pots count

	# Creating list of countries as per input data
        for read_lines in data[2:(2 + pots_count)]:
            currentline = read_lines.rstrip().split(",")
            for country in currentline:
                if country != 'None':
                    countries.append(country)
	# Sorting countries by name
        countries.sort()
	
	# Creating pots of countries as per input data
        for read_lines in data[2:(2 + pots_count)]:
            currentline = read_lines.rstrip().split(",")
            current_pot = []
            for country in currentline:
                if country != 'None':
                    current_pot.append(countries.index(country))
            country_pots.append(current_pot)
	
	# Creating regions of countries as per input data
        for read_lines in data[(2 + pots_count):]:
            key, value 		= read_lines.rstrip().split(":")
            country_geography.append(key)
            current_line	= value.rstrip().split(",")
            current_region 	= []
            for country in current_line:
                if country != 'None':
                    current_region.append(countries.index(country))
            country_regions.append(current_region)

    # Checking whether input data satisfies given Pot Constraints
    for current_pot in country_pots:
        if len(current_pot) <= group_count:
            for country_1_index in range(len(current_pot)):
                for country_2_index in range(country_1_index+1, len(current_pot)):
                    for group_index in range(group_count):
			# Creating key for country and corresponding group index as (Country * ENCODE_FACTOR + group_index)
                        knowledge_base.append({-int((current_pot[country_1_index] * ENCODE_FACTOR) + group_index), -int((current_pot[country_2_index] * ENCODE_FACTOR) + group_index)})
        else:
            return 0

    # Checking whether input data satisfies given Region Constraints
    country_regions_count = 0
    for current_region in country_regions:
        if country_geography[country_regions_count] != 'UEFA':
            if len(current_region) <= group_count:
                for country_1_index in range(len(current_region)):
                    for country_2_index in range(country_1_index + 1, len(current_region)):
                        for group_index in range(group_count):
                            # Creating key for country and corresponding group index as (Country * ENCODE_FACTOR + group_index)
                            knowledge_base.append({-int((current_region[country_1_index] * ENCODE_FACTOR) + group_index), -int((current_region[country_2_index] * ENCODE_FACTOR) + group_index)})
            else:
                return 0
        else:
            if len(current_region) <= (2 * group_count):
                country_combinations = iter.combinations(current_region, 3)
                for current_combination in country_combinations:
                    for group_index in range(group_count):
                        # Creating key for country and corresponding group index as (Country * ENCODE_FACTOR + group_index)
                        knowledge_base.append({-int((current_combination[0] * ENCODE_FACTOR) + group_index), -int((current_combination[1] * ENCODE_FACTOR) + group_index), -int((current_combination[2] * ENCODE_FACTOR) + group_index)})
            else:
                return 0

        country_regions_count += 1

    # Checking whether input data satisfies given XOR Constraints
    for country_index in range(1, len(countries)):
        country_list = []
        for group_index in range(group_count):
            country_list.append(int((country_index * ENCODE_FACTOR) + group_index))
        knowledge_base.append(set(country_list))
        negated_country_list = [-x for x in country_list]
        country_combinations = iter.combinations(negated_country_list, 2)
        for current_combination in country_combinations:
            knowledge_base.append({current_combination[0], current_combination[1]})

    return 1


# Finding pure symbol in clauses
def find_pure_symbols(symbols):
    for symbol in symbols:
        if -symbol not in symbols:
            return symbol, True
    return None, None


# Finding unit clause
def find_unit_clause(knowledge_base, model):
    for clause in knowledge_base:
        diff = set(clause) - set(model.keys())
        if len(diff) == 1 and True:
            literal = diff.pop()
            return literal, True
    return None, None


# Checking whether any clause is evaluating to True
def clause_evaluation_true(clause, model):
    for literal in clause:
        if literal in model:
            if model[literal] is True:
                return True
    return False


# Checking whether any literal of clause is not in the Model
def check_unknown_clause(clause, model):
    for literal in clause:
        if literal not in model:
            return True
    return False


# DPLL satisfy function
def dpll_satisfy():
    return dpll(knowledge_base, {})


# DPLL recursive call
def dpll(knowledge_base, model):
    unknown_clauses = []
    # Checking terminating conditions
    for clause in knowledge_base:
        if clause_evaluation_true(clause, model):
            continue
        elif check_unknown_clauses(clause, model):
            unknown_clauses.append(clause)
        else:
            return False

    if not unknown_clauses:
        return model
    
    # Generating all the symbols of unknown clause
    symbols 		= generate_symbols(unknown_clauses, model)
    # Finding pure symbol from unknown clauses
    pure_symbol, value 	= find_pure_symbols(symbols)
    if pure_symbol:
        model_update 	= {pure_symbol: value, -pure_symbol: not value}
        model.update(model_update)
        return dpll(unknown_clauses, model)
    # Finding unit clause from clauses
    unit_symbol, value 	= find_unit_clause(unknown_clauses, model)
    if unit_symbol:
        model_update 	= {unit_symbol: value, -unit_symbol: not value}
        model.update(model_update)
        return dpll(unknown_clauses, model)

    # Assigning a boolean value to new unknown symbol
    current_symbol	= symbols.pop()
    # Creating copy of model for second recursive call
    model_copy 		= copy.copy(model)
    # Assigning "False" to new unknown symbol and updating copy of the model
    model_copy_update	= {current_symbol : False, -current_symbol : True}
    model_copy.update(model_copy_update)
    # Assigning "True" to new unknown symbol and updating the model
    model_update 	= {current_symbol : True, -current_symbol : False}
    model.update(model_update)
    # Recursively calling both branches
    return dpll(unknown_clauses, model) or dpll(unknown_clauses, model_copy)


# Finding Symbols from all clauses Input CNF Output Literals
def generate_symbols(knowledge_base, model):
    symbols = set()
    for clause in knowledge_base:
        symbols = symbols | set(clause)
    for symbol in model:
        if symbol in symbols:
            symbols.remove(symbol)
    return set(symbols)


# Writing results to output file
def write_output_file(output):
    with open("output.txt", "w") as output_file:
        output_file.write(output)


# Main function
def main():
    global knowledge_base
    input_file 	= sys.argv[1]
    status 	= read_file(input_file)
    # If violation in any of the given constraints
    if not status:
        write_output_file("No")
        exit(0)
    
    # If given group count more than or equal to number of countries then assigning one country per group and exit
    if len(countries) - 1 <= group_count:
        model = ["None"] * group_count
        count = 0
        for country in range(1, len(countries)):
            model[count] = countries[country]
            count += 1
        output = ["Yes"] + model
        output = ("\n").join(output)
        write_output_file(output)
        exit(0)
    
    # Calling DPLL function
    dpll_model = dpll_satisfy()
    
    if not dpll_model:
        write_output_file("No")
        exit(0)

    for key, value in dpll_model.items():
        if key < 0 or value is False:
            del dpll_model[key]

    group_distribution = {}

    for group_index in range(group_count):
        group_distribution.setdefault(group_index, [])
        for encoded_country in dpll_model.keys():
	    # Getting group index from encoded_country
            if encoded_country % ENCODE_FACTOR == group_index:
	        # Getting country from encoded_country
                group_distribution[group_index].append(encoded_country / ENCODE_FACTOR)
    # Generating output in the required format
    output_result  = "Yes"
    for key in group_distribution.keys():
        result     = ""
        for value in group_distribution[key]:
            result += countries[value] + ","
        if len(result) == 0:
            output_result += "\nNone"
        else:
            result 	  = result[:-1]
            output_result += "\n" + result

    # Write formatted result to output file
    write_output_file(output_result)

# Entry point of the program
if __name__ == '__main__':
    main()
