import pandas as pd
from pulp import *

df = pd.read_excel("alimentos_porcoes.xlsx", nrows=173)
df.head()

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Simple Diet Problem", LpMinimize)

# Creates a list of the Ingredients
food_items = list(df['Alimentos'])

print("So, the food items to consdier, are \n"+"-"*100)
for f in food_items:
    print(f, end=', ')

#costs = dict(zip(food_items, df['Price/ Serving']))

energia = dict(zip(food_items,  df['Energia']))

proteina = dict(zip(food_items, df['Proteína']))

lipideos = dict(zip(food_items, df['Lipídeos']))

colesterol = dict(zip(food_items, df['Colesterol']))

carboidrato = dict(zip(food_items, df['Carboidrato']))

fibra = dict(zip(food_items, df['Fibra']))

calcio = dict(zip(food_items, df['Cálcio']))

magnesio = dict(zip(food_items, df['Magnésio']))

fosforo = dict(zip(food_items, df['Fósforo']))

ferro = dict(zip(food_items, df['Ferro']))

sodio = dict(zip(food_items, df['Sódio']))

potassio = dict(zip(food_items, df['Potássio']))

zinco = dict(zip(food_items, df['Zinco']))

vitamina_A = dict(zip(food_items, df['Retinol (A)']))

vitamina_B1 = dict(zip(food_items, df['Tiamina (B1)']))

vitamina_B2 = dict(zip(food_items, df['Riboflavina (B2)']))

vitamina_C = dict(zip(food_items, df['Vitamina C']))

porcao = dict(zip(food_items, df['Porção']))

# A dictionary called 'food_vars' is created to contain the referenced Variables
# Continuous para numeros reais e Integer para numeros inteiros
food_vars = LpVariable.dicts("", food_items, 0, cat='Integer')

#prob += lpSum([costs[i]*food_vars[i] for i in food_items]), "Total Cost of the balanced diet"

# The objective function is added to 'prob' first
prob += lpSum([(carboidrato[i] * (porcao[i]/100)) * food_vars[i] for i in food_items]), "Total Cost of the balanced diet"

# Energia(Calorias) - Variável
prob += lpSum([(energia[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) >= 1800.0, "CaloriaMaxima"
prob += lpSum([(energia[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) <= 1960.0, "CaloriaMinima"

# Carboidrato - Variável
prob += lpSum([(carboidrato[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) >= 202.5, "CarboidratoMinimo"

# Lipideos - Variável
prob += lpSum([(lipideos[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) <= 60.0, "LipideoMaximo"

# Colesterol
prob += lpSum([(colesterol[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) <= 290.0, "ColesterolMaximo"

# Sodio
prob += lpSum([(sodio[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) <= 2000.0, "SodioMaximo"

# Proteinas
prob += lpSum([(proteina[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) >= 28.4, "ProteinasMinimo"
prob += lpSum([(proteina[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) <= 38.4, "ProteinasMaximo"

# Fibras
prob += lpSum([(fibra[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) >= 30.0, "FibrasMinimo"

# Calcio
prob += lpSum([(calcio[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) <= 850.0, "CalcioMinimo"

# Magnesio
prob += lpSum([(magnesio[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) >= 400.0, "MagnesioMinimo"

# Fosforo
prob += lpSum([(fosforo[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) >= 700.0, "FosforoMinimo"

# Ferro
prob += lpSum([(ferro[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) >= 18.0, "FerroMinimo"

# Potassio
prob += lpSum([(potassio[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) >= 3500.0, "PotassioMinimo"

# Zinco
prob += lpSum([(zinco[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) >= 15.0, "ZincoMinimo"

# Vitamina A
prob += lpSum([(vitamina_A[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) >= 80.0, "Vitamina_AMinimo"

# Vitamina C
prob += lpSum([(vitamina_C[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) >= 200.0, "Vitamina_CMinimo"

# Vitamina B1
prob += lpSum([(vitamina_B1[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) >= 0.98, "Vitamina_B1Minimo"

# Vitamina B2
prob += lpSum([(vitamina_B2[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) >= 1.35, "Vitamina_B2Minimo"

# The problem data is written to an .lp file
prob.writeLP("SimpleDietProblem.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

print("Therefore, the optimal (least cost) balanced diet consists of\n"+"-"*110)
for v in prob.variables():
    if v.varValue>0:
        print(v.name, "=", v.varValue)

energiaFinal = lpSum([energia[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("\nCalorias: {}".format(round(value(energiaFinal), 2)))

carboidratoFinal = lpSum([carboidrato[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Carboidratos: {}".format(round(value(carboidratoFinal), 2)))

lipideoFinal = lpSum([lipideos[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Lipídeos: {}".format(round(value(lipideoFinal), 2)))

colesterolFinal = lpSum([colesterol[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Colesterol: {}".format(round(value(colesterolFinal), 2)))

sodioFinal = lpSum([sodio[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Sódio: {}".format(round(value(sodioFinal), 2)))

proteinaFinal = lpSum([proteina[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Proteínas: {}".format(round(value(proteinaFinal), 2)))

fibraFinal = lpSum([fibra[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Fibras: {}".format(round(value(fibraFinal), 2)))

calcioFinal = lpSum([calcio[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Cálcio: {}".format(round(value(calcioFinal), 2)))

magnesioFinal = lpSum([magnesio[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Magnésio: {}".format(round(value(magnesioFinal), 2)))

fosforoFinal = lpSum([fosforo[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Fósforo: {}".format(round(value(fosforoFinal), 2)))

ferroFinal = lpSum([ferro[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Ferro: {}".format(round(value(ferroFinal), 2)))

potassioFinal = lpSum([potassio[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Potássio: {}".format(round(value(potassioFinal), 2)))

zincoFinal = lpSum([zinco[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Zinco: {}".format(round(value(zincoFinal), 2)))

vitaminaAFinal = lpSum([vitamina_A[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Vitamina A: {}".format(round(value(vitaminaAFinal), 2)))

vitaminaCFinal = lpSum([vitamina_C[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Vitamina C: {}".format(round(value(vitaminaCFinal), 2)))

vitaminaB1Final = lpSum([vitamina_B1[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Vitamina B1: {}".format(round(value(vitaminaB1Final), 2)))

vitaminaB2Final = lpSum([vitamina_B2[f] * (porcao[f]/100) * food_vars[f].value() for f in food_items])
print("Vitamina B2: {}".format(round(value(vitaminaB2Final), 2)))

print("\nFunção Objetivo: {}".format(round(value(prob.objective), 2)))