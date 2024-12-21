import random
import math

"""
Dar in tabe shahr haro load mikonim.
Mokhtasat shahr ha dar file citiesLocation.txt zakhire shode.
"""
def load_cities():
    cities = []
    f = open('citiesLocation.txt')
    for line in f.readlines():
        pos = line.split()
        cities.append([float(pos[0]),float(pos[1])])
    return cities

"""
baraye tolid har chromosome as in tabe estefade mikonim
"""
def init_ch(cities):
    route = list(range(len(cities)))
    return random.sample(route, len(route))

"""
population ra ba in tabe dorost mikonim. tedad population = 1000
"""
def init_population(cities, pop_size = 1000):
    population = [init_ch(cities) for _ in range(pop_size)]
    return population


"""
tabe shayestegi ke fasele peymode shode dar safari ke dar chromosome ast ra mohasebe mikond
baraye mohasebe fasele peymode shode, fasele beine shah haro ba fasele oghlidosi (Euclidean distance)
mohasebe mikonim va anharo baham jam mikonim
nokte: ma dar akhar safar az shahr akhar be shahri ke az an shoro kardim bayad bargardim pas hazine
in safar ra niz be hazine kol ezafe mikonim
"""
def fitness(ch, cities):
    total_distance = 0
    for i in range(len(ch) - 1):
        A_pos = cities[ch[i]]
        B_pos = cities[ch[i+1]]
        d = math.sqrt(math.pow(A_pos[0] - B_pos[0], 2) + math.pow(A_pos[1] - B_pos[1], 2)) 
        total_distance += d
    A_pos = cities[ch[0]]
    B_pos = cities[ch[-1]]
    d = math.sqrt(math.pow(A_pos[0] - B_pos[0], 2) + math.pow(A_pos[1] - B_pos[1], 2))
    total_distance += d
    return total_distance

"""
Marhale selection: entekhab tedadi chromosome az population
in tabe random pick hastesh ke besorat random az popluation entekhab mikone.
dar in tabe baraye inke chance chromosome hayii ba distance kamtar bishtr bashd, maximum distance ra az distance har
chromosome kam mikonim ta minimum chance bishtri bedast biavarnd
in tabe ra jori neveshtam ke ba estefade az ehtemal tajamoii, chance entekhab chromosome ba distance kamtar, bishtr bashd
"""
def random_pick(population):
    fitnesses = [fitness(ch) for ch in population]
    max_fitness = max(fitnesses)
    fitness_probs = [(max_fitness - f) for f in fitnesses]
    total_fitness = sum(fitness_probs)
    fitness_probs = [f / total_fitness for f in fitness_probs]

    cumulative_probs = []
    cumulative_sum = 0
    for prob in fitness_probs:
        cumulative_sum += prob
        cumulative_probs.append(cumulative_sum)

    random_number = random.random()

    for i, cumulative_prob in enumerate(cumulative_probs):
        if random_number <= cumulative_prob:
            return population[i]
    return population[-1]

"""
Yek noe dige selection
in tabe noe dige az tavabee selection hast. Farsi: Nokhbe garayee!
dar in selection tedadi (k=5) chromosome az population entekhab va behtarin anhara select mikonim

maziat: ahmiat be fitness va dar natije sorate bishtr convergence (ham gara shodn be javab)
maayeb: randomness kamtar mishe -> ehtemal gir oftadn dar local minimum
"""
def tournament_selection(population, cities, tournament_size = 5):
    tournament = random.sample(population, tournament_size)
    winner = min(tournament, key=lambda x: fitness(x, cities))
    return winner

"""
Crossover: single point
Dar pdf tamrin in crossover tozih dade shod.
"""
def single_point_co(x,y):
    co_point = random.randint(1,len(x) - 1)
    offspring1 = x[:co_point] + y[co_point:]
    offspring2 = y[:co_point] + x[co_point:]

    return offspring1, offspring2

"""
Crossover: PMX
Dar pdf tamrin in crossover tozih dade shod.
"""
def pmx_co(x,y):
    n = len(x)
    pos1, pos2 = sorted(random.sample(range(1,n), k = 2))

    offspring1 = x[:]
    offspring2 = y[:]

    offspring1[pos1:pos2+1] = y[pos1:pos2+1]
    offspring2[pos1:pos2+1] = x[pos1:pos2+1]

    map1 = {y[i]: x[i] for i in range(pos1, pos2+1)}
    map2 = {x[i]: y[i] for i in range(pos1, pos2+1)}
    for i in range(n):
        if i < pos1 or i > pos2:
            if offspring1[i] not in y[pos1:pos2+1]:
                continue
            value = offspring1[i]
            while value in map1:
                value = map1[value]
            offspring1[i] = value
    
    for i in range(n):
        if i < pos1 or i > pos2:
            if offspring2[i] not in x[pos1:pos2+1]:
                continue
            value = offspring2[i]
            while value in map2:
                value = map2[value]
            offspring2[i] = value
    
    return offspring1, offspring2


"""
Crossover: Order
Dar pdf tamrin in crossover tozih dade shod.
nokte code: be dalil inke ma bazi az gene haro skip mikonim, in crossover mitavand chromosome haii ba gene haye None tolid
konad. baraye jologiri az in etefagh, khone haye None ro ba gene motenazer dar parent motenaseb por kardm
"""
def ox_co(x,y):
    n = len(x)
    pos1, pos2 = sorted(random.sample(range(n), k = 2))
    offspring1 = [None] * n
    offspring2 = [None] * n

    offspring1[pos1:pos2+1] = y[pos1:pos2+1]
    offspring2[pos1:pos2+1] = x[pos1:pos2+1]

    k1, k2 = (pos2 + 1) % n, (pos2 + 1) % n
    for i in range(n):
        gene1 = x[(i + pos2 + 1) % n]

        if gene1 not in offspring1[pos1:pos2+1]:
            offspring1[k1] = gene1
            k1 = (k1 + 1) % n
        gene2 = y[(i + pos2 + 1) % n]
        if gene2 not in offspring2[pos1:pos2+1]:
            offspring2[k2] = gene2
            k2 = (k2 + 1) % n
    for i in range(n):
        if offspring1[i] == None:
            offspring1[i] = x[i]
        if offspring2[i] == None:
            offspring2[i] = y[i]
    return offspring1, offspring2


"""
Mutation: Random Swap
Tebghe soal az mutation random swap estefade shod.
"""
def random_swap_mutation(ch):
    pos1, pos2 = random.sample(range(len(ch)), k = 2)
    mutated_ch = ch[:]
    mutated_ch[pos1], mutated_ch[pos2] = mutated_ch[pos2], mutated_ch[pos1]
    return mutated_ch


"""
In tabe ra be dalil inke javab az minimum mahali farar konad neveshtm.
Pas az inke sabr algorithm (moteghayer patient dar tabe genetic_algo) be threshold resid, in tabe
farakhani mishavad. dar in tabe 50% gene ha ba distance bishtr dobare initial mishvnd.
Bashad ke behtar shavand :)
"""
def random_restart(population, cities, restart_fraction=0.5):
    num_to_restart = int(len(population) * restart_fraction)
    newPopulation = population[:]
    newPopulation = sorted(newPopulation, key=lambda ch: fitness(ch,cities), reverse=True)
    for i in range(num_to_restart):
        newPopulation[i] = init_ch(cities)
    newPopulation = sorted(newPopulation, key=lambda ch: fitness(ch,cities), reverse=False)
    return newPopulation


"""
dar in tabe population jadid tolid mishvd
joda az population jadid, agar fitness population tekrari bod, moteghaye patient update mishvd
va agar be threshold resid, random_restart farakhani mishavad!
"""
def genetic_algo(population, best_distance , patient, cities):
    current_best_distance  = min([fitness(ch,cities) for ch in population])

    if current_best_distance == best_distance:
        patient += 1
    else:
        patient = 0
        best_distance = current_best_distance

    if patient >= 20:
        population = random_restart(population, cities)
        patient = 0

    new_population = []
    for i in range(int(len(population) / 2)):
        x = tournament_selection(population,cities)
        y = tournament_selection(population,cities)
        offspring1, offspring2 = pmx_co(x,y)
        new_population.append(offspring1)
        new_population.append(offspring2)

    return new_population, patient, best_distance


"""
Noghte shoroe barname. shahr ha load mishvnd, population ijad shode va genetic_algo 3000bar farakhani mishvd
(mishe adad kamtai entekhab kard vali khob mahze ehtiat 3000 entekhab shod)
Dar akhabr behtarin javab chap mishvd
"""
def main():
    cities = load_cities()
    population = init_population(cities)
    max_generations = 3000
    best_distance = 2 * math.pow(10,7)
    patient = 0
    for generation in range(max_generations):
        population, patient, best_distance = genetic_algo(population, best_distance, patient, cities)
        if(generation % 10 == 0):
            print(f"Generation: {generation}\nBest fitness: {best_distance}")
    fitnesses = [fitness(ch,cities) for ch in population]
    bestCh = population[fitnesses.index(min(fitnesses))]
    best_distance = min(fitnesses)
    print(f"Answer: {bestCh}\n Best distance: {best_distance}")


if __name__ == "__main__":
    main()