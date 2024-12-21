import random
import time

"""
baraye tolid har chromosome as in tabe estefade mikonim
"""
def init_ch(n):
    return [random.randint(1, n) for _ in range(n)]

"""
population ra ba in tabe dorost mikonim. tedad population = 500
"""
def init_population(n, pop_size = 500):
    population = [init_ch(n) for _ in range(pop_size)]
    return population

"""
tabe shayestegi ke tedad barkhord vazir haro baham mohasebe mikone
barkhord ha:
1- vojod chand vazir dar yek row
2- vojod chand vazir dar yek ghotr

2 noe ghotr darim
a- top left to bottom right
b- top right to bottom left
"""
def fitness(ch):
    n = len(ch)
    max_fitness = n * (n-1) / 2
    h_collision = 0
    d_collision = 0
    for queen in ch:
        h_collision += ch.count(queen) - 1
    h_collision /= 2

    tl_br_diags = [0] * (2 * n - 1)
    tr_bl_diags = [0] * (2 * n)
    for i in range(n):
        tl_br_diags[ch[i] - i] += 1
        tr_bl_diags[ch[i] + i] += 1 
    
    for diag in tl_br_diags:
        d_collision += diag * (diag - 1) / 2
    
    for diag in tr_bl_diags:
        d_collision += diag * (diag - 1) / 2

    return max_fitness - (h_collision + d_collision)

"""
Marhale selection: entekhab tedadi chromosome az population
in tabe random pick hastesh ke besorat random az popluation entekhab mikone.
in tabe ra jori neveshtam ke ba estefade az ehtemal tajamoii, chance entekhab chromosome ba fitness bishtr, bishtr bashd
"""
def random_pick(population):
    fitnesses = [fitness(ch) for ch in population]
    sumFitnesses = sum([fitness(ch) for ch in population])
    probs = [fn / sumFitnesses for fn in fitnesses]

    cumulative_probs = []
    cumulative_sum = 0
    for prob in probs:
        cumulative_sum += prob
        cumulative_probs.append(cumulative_sum)

    rand = random.random()

    for i, cum_prob in enumerate(cumulative_probs):
        if rand < cum_prob:
            return population[i]
    return population[-1]


"""
Yek noe dige selection
in tabe noe dige az tavabee selection hast. Farsi: Nokhbe garayee!
dar in selection tedadi (k=5) chromosome az population entekhab va behtarin anhara select mikonim

maziat: ahmiat be fitness va dar natije sorate bishtr convergence (ham gara shodn be javab)
maayeb: randomness kamtar mishe -> ehtemal gir oftadn dar local maximum
"""
def tournament_selection(population, tournament_size = 5):
    tournament = random.sample(population, tournament_size)
    winner = max(tournament, key=fitness)
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
nokte code: az anjaii ke dar masale NQueen momken ast dar yek chromosome adad tekrari dashte bashim, in tabe mitavanad dar
loop binahayat bioftad. ba estefade az numOfTries, az oftadn toye loop jolo giri kardim. dar in sharayet khas, crossover
be donbal javabi migrdd ke fght betavand ba an offspring ta tashkil dahad.
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
            numOfTries = 0
            while value in map1 and numOfTries < n:
                value = map1[value]
                numOfTries += 1
            if numOfTries >= n:
                for gene in y:
                    if gene not in y[pos1:pos2+1]:
                        value = gene
                        break
            offspring1[i] = value
    
    for i in range(n):
        if i < pos1 or i > pos2:
            if offspring2[i] not in x[pos1:pos2+1]:
                continue
            value = offspring2[i]
            numOfTries = 0
            while value in map2 and numOfTries < n:
                value = map2[value]
                numOfTries += 1
            if numOfTries >= n:
                for gene in x:
                    if gene not in x[pos1:pos2+1]:
                        value = gene
                        break
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
In tabe ra be dalil inke javab az maximum mahali farar konad neveshtm.
Pas az inke sabr algorithm (moteghayer patient dar tabe genetic_algo) be threshold resid, in tabe
farakhani mishavad. dar in tabe 50% gene ha ba fitness kamtar dobare initial mishvnd.
Bashad ke behtar shavand :)
"""
def random_restart(population, restart_fraction=0.5):
    num_to_restart = int(len(population) * restart_fraction)
    newPopulation = population
    newPopulation = sorted(newPopulation, key=lambda ch: fitness(ch), reverse=False)
    for i in range(num_to_restart):
        newPopulation[i] = init_ch(len(newPopulation[i]))
    newPopulation = sorted(newPopulation, key=lambda ch: fitness(ch), reverse=True)
    return newPopulation

"""
dar in tabe population jadid tolid mishvd
joda az population jadid, agar fitness population tekrari bod, moteghaye patient update mishvd
va agar be threshold resid, random_restart farakhani mishavad!
"""
def genetic_algo(population, best_fitness, patient):
    current_best_fitness = max([fitness(ch) for ch in population])
    
    if current_best_fitness == best_fitness:
        patient += 1
    else:
        patient = 0
        best_fitness = current_best_fitness

    if patient >= 20:
        population = random_restart(population)
        patient = 0

    new_population = []
    for i in range(int(len(population) / 2)):
        x = tournament_selection(population)
        y = tournament_selection(population)
        offspring1, offspring2 = ox_co(x,y)
        new_population.append(offspring1)
        new_population.append(offspring2)

    return new_population, patient, best_fitness

"""
Noghte shoroe barname. az karbar N gerefte mishvd, population ijad shode va ta zamani ke be javab masale naresidim,
genetic_algo farakhani mishvd.
Zaman ejra andaze giri shode va dar akhar hamrah javab chap mishvd
"""
def main():
    n = int(input("Enter N: "))
    max_fitness = n * (n-1) / 2
    population = init_population(n)
    generation = 1
    patient = 0
    best_fitness = 0
    start = time.time()
    while(not max_fitness in [fitness(ch) for ch in population]):
        population, patient, best_fitness = genetic_algo(population, best_fitness, patient)
        generation += 1
        #if(generation % 10 == 0):
            #print(f"Generation: {generation}\nBest fitness: {best_fitness}")
    end = time.time()
    fitnesses = [fitness(ch) for ch in population]
    bestCh = population[fitnesses.index(max(fitnesses))]
    maxFitness = max(fitnesses)
    print(f"Answer: {bestCh}\n Fitness: {maxFitness}")
    print(f"Elapsed time: {(end-start) * 1000} milliseconds")

if __name__ == "__main__":
    main()