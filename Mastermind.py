import random
import sys
import numpy
import copy
import matplotlib.pyplot as plt

class Chromosome():
    def __init__(self):
        self.aptitude = -1
        self.body = []

def generateRandomSolution():
    #solution = [3,0,5,0] # SOLUCION estatica -> Azul Amarillo Verde Naranja
    solution = []
    for i in range(0, 4):
        solution.append(random.randint(0,NUM_MAX_COLORES))
    return solution

def generateChromosomeBody(size):
    #body = [0,0,0,0,0,1,0,1,0,0]
    body = []
    for i in range (0, size):
        body.append(random.randint(0, NUM_MAX_COLORES))
    return body

def generateInitialPopulation(population, size):
    for i in range(0,size):
        chromosome = Chromosome()
        chromosome.body = generateChromosomeBody(4)[:]
        population.append(chromosome)

def evaluate(population):
    if population[0].aptitude == -1:
        calculateAptitudes(population)
    max = population[0].aptitude
    for i in population:
        if i.aptitude > max:
            max = i.aptitude
    return max

def evaluateAverageAptitudeGeneration(population):
    media = 0
    for i in population:
        media+=i.aptitude
    return media/len(population)


def getBest(population): #Devuelve el mejor de la poblacion
    if population[0].aptitude == -1:
        calculateAptitudes(population)
    max = population[0].aptitude
    pos = 0
    for i in range(0, len(population)):
        if population[i].aptitude > max:
            pos = i
            max = population[i].aptitude
    return population[pos]

def calculateAptitudes(population):
    for i in population:
        aptitudeFunction(i)

def aptitudeFunction(chromosome): #Funcion de aptitud (2N + B) + SUM de K desde k = 1 hasta N-1
    blancos = 0
    negros = 0
    for i in range(len(chromosome.body)):
        if chromosome.body[i] == solution[i]:
            negros+=1
        else:
            for j in solution:
                if chromosome.body[i] == j:
                    blancos+=1
                    break
    N = blancos + negros
    aptitude = 2*negros + blancos
    for k in range(1, N):
        aptitude+=k

    chromosome.aptitude = aptitude    
    

def select(population, type):
    if(type == "Ruleta con pesos"):
        if len(population) == 2:
            selected = []
            selected.append(population[0])
            selected.append(population[1])
            return selected
        boards = 0
        array = [] #Inicializo una lista vacía
        selected = []
        for i in population:
            if i.aptitude == 0:
                boards+=1
            else:
                boards+=i.aptitude #Calcular el numero maximo para hacer el random
        while len(selected) <= 2:
            for i in population: #Recorro toda la población
                for j in range(0, i.aptitude+1):
                    array.append(population.index(i)) #Relleno tantas posiciones en el array como aptitud tenga dicho elemento, EJ: elemento tiene 5 de aptitud, la lista sería: array = [0, 0, 0, 0, 0]
                rand = random.randint(1, boards)
                rand2 = random.randint(1, boards)
            while population[array[rand-1]] == population[array[rand2-1]]: #Comprobacion de que no se repiten los elementos
                rand2 = random.randint(1, boards)
            selected.append(population[array[rand-1]])
            selected.append(population[array[rand2-1]])
            print("**************SELECCION por RULETA CON PESOS**************")
            print("Los 2 cromosomas seleccionados:")
            print("1 -> ",selected[0].body, " su aptitud es: ",selected[0].aptitude)
            print("2 -> ",selected[1].body, " su aptitud es: ",selected[1].aptitude)
            return selected
    elif type == "Elitismo":
        print("SELECCION POR ELITISMO")
        aptitudes = [] #Lista de aptitudes
        selected = [] #Lista de los 2 elementos seleccionados por elitismo
        for i in population:
            aptitudes.append(i.aptitude) #Relleno una lista con las aptitudes para trabajar mas comodamente
        chromosome = Chromosome()
        body = population[aptitudes.index(max(aptitudes))].body
        chromosome.body = body
        aptitude = population   [aptitudes.index(max(aptitudes))].aptitude
        chromosome.aptitude = aptitude
        selected.append(chromosome) #Cojo el maximo de las aptitudes
        #aptitudes[aptitudes.index(max(aptitudes))] = 0 #Relleno la posicion con 0 para encontrar otro maximo
        #selected.append(populations[aptitudes.index(max(aptitudes))])
        #print("Los 2 cromosomas seleccionados:")
        print("1 -> ",selected[0].body, " su aptitud es: ",selected[0].aptitude)
        #print("2 -> ",selected[1].body, " su aptitud es: ",selected[1].aptitude)
        #populations.remove(selected[1])
        return selected
    else:
        print("ERROR EN LA SELECCION, 'Elitismo' o 'Ruleta con pesos'")
        sys.exit(0)

def crossover(population):
    print("**************CRUZAMIENTO**************")
    #TODO Cruzar aleatoriamente 
    populat = [] #Nuevo array a rellenar con los cromosomas ya cruzados
    crossRate = 95 #Probabilidad de cruzamiento 95%
    while(len(population)>1):
        selected = select(population, "Ruleta con pesos")
        chromosome1 = selected[0]
        chromosome2 = selected[1]
        for j in range(0, len(selected)-1, 2):
            if random.randint(0, 100) <= crossRate:
                print("ANTES DEL CRUZAMIENTO")
                print("1 -> ",selected[j].body, " su aptitud es: ",selected[j].aptitude)
                print("2 -> ",selected[j+1].body, " su aptitud es: ",selected[j+1].aptitude)
                pos1 = random.randint(0, 3)
                pos2 = random.randint(0, 3)
                num = selected[j].body[pos1]
                body = selected[j+1].body[pos2]
                selected[j].body[pos1] = body
                selected[j+1].body[pos2] = num
                posicion1 = random.randint(0, 3)
                posicion2 = random.randint(0, 3)
                num2 = selected[j+1].body[posicion1]
                body2 = selected[j].body[posicion2]
                selected[j+1].body[posicion1] = body2
                selected[j].body[posicion2] = num2
                print("DESPUES DEL CRUZAMIENTO")
                calculateAptitudes(population)
                print("1 -> ",selected[j].body, " su aptitud es: ",selected[j].aptitude)
                print("2 -> ",selected[j+1].body, " su aptitud es: ",selected[j+1].aptitude)
            else:
                print("No se ha cruzado, probabilidad de cruzamiento = ",crossRate)
        populat.append(chromosome1)
        populat.append(chromosome2)
        population.remove(chromosome1)
        population.remove(chromosome2)
    if len(population)!=0:
        populat.append(population.pop())
    min = populat[0].aptitude
    minChrom = populat[0]
    for i in populat:
        if i.aptitude < min:
            min = i.aptitude
            minChrom = i
    populat.remove(minChrom)
    calculateAptitudes(populat)
    return populat

def mutate(population):
    print("**************MUTACION**************")
    mutateRate = 10
    for i in population:
        if random.randint(0, 100) <= mutateRate:
            print("El cromosoma numero: ",population.index(i), "va a mutar, su aptitud es ",i.aptitude)
            posicionesCambio = [] #Lista con las posiciones a cambiar
            cantidadCambio = random.randint(1, len(i.body)/2) #Cantidad de posiciones a cambiar, como max la mitad del cuerpo, 2
            for k in range(0, cantidadCambio):
                posicionCambio = random.randint(0, len(i.body)-1)
                while posicionCambio in posicionesCambio: #Comprobacion de que no se repite la posicion
                    posicionCambio = random.randint(0, len(i.body)-1)
                posicionesCambio.append(posicionCambio)
            for j in posicionesCambio:
                i.body[j] = random.randint(0,NUM_MAX_COLORES)
            calculateAptitudes(population)
            print("Su aptitud ahora es: ", i.aptitude)
        else:
            print("El cromosoma numero: ",population.index(i), "no ha conseguido mutar.")
    calculateAptitudes(population)

def plotBestAptitude(): #Grafica de la aptitud del mejor cromosoma de cada generacion
    plt.plot(bestOfEachGeneration)
    plt.ylabel('Aptitude of the best of each generation')
    plt.xlabel('Number of generations')
    plt.show()

def plotAverageAptitude(): #Muestra la grafica de la media de aptitud de cada generacion
    plt.plot(averageOfEachGeneration)
    plt.ylabel('Average aptitude of each generation')
    plt.xlabel('Number of generations')
    plt.show()

#Empieza el programa
NUM_MAX_COLORES = 7
solution = generateRandomSolution() #Solucion generada aleatoriamente
population = [] #Lista a rellenar con la poblacion de cada generacion
generateInitialPopulation(population, 10)
nGenerations = 0 #numero de Generaciones
lastGeneration = population #Array con la ultima generacion por cada vuelta
nextGeneration = [] #Array con la generacion que se va a formar para la siguiente vuelta, primero el elite, luego el resto con crossover y mutacion
selected = [] #Array que contiene el/los cromosomas seleccionados por elitismo
bestOfEachGeneration = [] #Array que contiene el mejor de cada generacion, para graficas
averageOfEachGeneration = [] #Array con la media de aptitudes de cada generacion, para graficas

while evaluate(lastGeneration)!=14 :
    print("\n***************************Inicio VUELTA***************************\n")
    print("*************LA SOLUCION ES : ->",solution,"*************")
    if nGenerations == 0: #Si es la primera vuelta
        aptitud = evaluate(population)
        selected = select(population, "Elitismo")
        for i in selected:
            chrom = copy.deepcopy(i)
            nextGeneration.append(chrom) #Se incluyen los mejores seleccionados por elitismo para la siguiente generacion
        population = crossover(population)
        mutate(population)
        for i in population:
            nextGeneration.append(i)
    else:
        aptitud = evaluate(lastGeneration)
        selected = select(lastGeneration, "Elitismo")
        for i in selected:
            chrom = copy.deepcopy(i)
            nextGeneration.append(chrom) #Se incluyen los mejores seleccionados por elitismo para la siguiente generacion
        lastGeneration = crossover(lastGeneration)
        mutate(lastGeneration)
        for i in lastGeneration:
            nextGeneration.append(i)

    bestOfEachGeneration.append(evaluate(nextGeneration))
    averageOfEachGeneration.append(evaluateAverageAptitudeGeneration(nextGeneration))
    aptitud2 = evaluate(nextGeneration)
    lastGeneration = nextGeneration[:]
    for i in lastGeneration:
        print("Cromosoma ",lastGeneration.index(i), "con cuerpo->",i.body, " y aptitud->", i.aptitude)
    nextGeneration = []
    nGenerations += 1
    print("Generacion numero : ",nGenerations)

print("*************LA SOLUCION ERA : ->",solution,"*************")
plotBestAptitude() #Grafica con la aptitud el mejor de cada generacion
plotAverageAptitude() #Grafica con la media de la aptitud de cada generacion

