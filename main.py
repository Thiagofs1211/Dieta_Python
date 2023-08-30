import pandas as pd
from pulp import *

df = pd.read_excel("alimentos_porcoes.xlsx", nrows=173)
df.head()

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Simple Diet Problem", LpMinimize)

# Creates a list of the Ingredients
food_items = list(df['Alimentos'])

ajustar_pesos = False

print("So, the food items to consdier, are \n" + "-" * 100)
for f in food_items:
    print(f, end=', ')

costs = dict(zip(food_items, df['Preço (100g)']))

energia = dict(zip(food_items, df['Energia']))

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

pesos = dict(zip(food_items, df['Pesos']))

# A dictionary called 'food_vars' is created to contain the referenced Variables
# Continuous para numeros reais e Integer para numeros inteiros
food_vars = LpVariable.dicts("", food_items, 0, cat='Integer')

# prob += lpSum([costs[i]*food_vars[i] for i in food_items]), "Total Cost of the balanced diet"

# The objective function is added to 'prob' first
prob += lpSum([(carboidrato[i] * (porcao[i] / 100)) * food_vars[i] for i in food_items])
# prob += lpSum([(costs[i] * (porcao[i]/100)) * food_vars[i] for i in food_items]), "Total Cost of the balanced diet"

# prob += lpSum([(costs[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) <= 8.657, "Custo maximo"

# Pesos
prob += lpSum([(pesos[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) <= 5.0

# Energia(Calorias) - Variável
prob += lpSum([(energia[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 1800.0, "CaloriaMinima"
prob += lpSum([(energia[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) <= 2200.0, "CaloriaMaxima"

# Carboidrato - Variável
prob += lpSum([(carboidrato[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 202.5, "CarboidratoMinimo"

# Carboidrato - Variável
# prob += lpSum([(carboidrato[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) <= 598.9, "CarboidratoMaximo"

# Lipideos - Variável
prob += lpSum([(lipideos[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) <= 60, "LipideoMaximo"

# Colesterol
prob += lpSum([(colesterol[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) <= 1800, "ColesterolMaximo"

# Sodio
prob += lpSum([(sodio[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) <= 2000.0, "SodioMaximo"

# Proteinas
prob += lpSum([(proteina[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 28.4, "ProteinasMinimo"
prob += lpSum([(proteina[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) <= 38.4, "ProteinasMaximo"

# Fibras
prob += lpSum([(fibra[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 30.0, "FibrasMinimo"

# Calcio
prob += lpSum([(calcio[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 850.0, "CalcioMinimo"

# Magnesio
prob += lpSum([(magnesio[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 400.0, "MagnesioMinimo"

# Fosforo
prob += lpSum([(fosforo[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 700.0, "FosforoMinimo"

# Ferro
prob += lpSum([(ferro[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 18.0, "FerroMinimo"

# Potassio
prob += lpSum([(potassio[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 3500.0, "PotassioMinimo"

# Zinco
prob += lpSum([(zinco[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 15.0, "ZincoMinimo"

# Vitamina A
prob += lpSum([(vitamina_A[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 80.0, "Vitamina_AMinimo"

# Vitamina C
prob += lpSum([(vitamina_C[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 200.0, "Vitamina_CMinimo"

# Vitamina B1
prob += lpSum([(vitamina_B1[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 0.98, "Vitamina_B1Minimo"

# Vitamina B2
prob += lpSum([(vitamina_B2[f] * (porcao[f] / 100)) * food_vars[f] for f in food_items]) >= 1.35, "Vitamina_B2Minimo"

# The problem data is written to an .lp file
prob.writeLP("SimpleDietProblem.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

print("Therefore, the optimal (least cost) balanced diet consists of\n" + "-" * 110)
for v in prob.variables():
    if v.name != '__dummy' and v.varValue > 0:
        print(v.name, "=", round(v.varValue, 2))

energiaFinal = lpSum([energia[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("\nCalorias: {}".format(value(energiaFinal)))

carboidratoFinal = lpSum([carboidrato[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Carboidratos: {}".format(value(carboidratoFinal)))

lipideoFinal = lpSum([lipideos[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Lipídeos: {}".format(value(lipideoFinal)))

colesterolFinal = lpSum([colesterol[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Colesterol: {}".format(value(colesterolFinal)))

sodioFinal = lpSum([sodio[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Sódio: {}".format(value(sodioFinal)))

proteinaFinal = lpSum([proteina[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Proteínas: {}".format(value(proteinaFinal)))

fibraFinal = lpSum([fibra[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Fibras: {}".format(value(fibraFinal)))

calcioFinal = lpSum([calcio[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Cálcio: {}".format(value(calcioFinal)))

magnesioFinal = lpSum([magnesio[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Magnésio: {}".format(value(magnesioFinal)))

fosforoFinal = lpSum([fosforo[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Fósforo: {}".format(value(fosforoFinal)))

ferroFinal = lpSum([ferro[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Ferro: {}".format(value(ferroFinal)))

potassioFinal = lpSum([potassio[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Potássio: {}".format(value(potassioFinal)))

zincoFinal = lpSum([zinco[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Zinco: {}".format(value(zincoFinal)))

vitaminaAFinal = lpSum([vitamina_A[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Vitamina A: {}".format(value(vitaminaAFinal)))

vitaminaCFinal = lpSum([vitamina_C[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Vitamina C: {}".format(value(vitaminaCFinal)))

vitaminaB1Final = lpSum([vitamina_B1[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Vitamina B1: {}".format(value(vitaminaB1Final)))

vitaminaB2Final = lpSum([vitamina_B2[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Vitamina B2: {}".format(value(vitaminaB2Final)))

custoFinal = lpSum([costs[f] * (porcao[f] / 100) * food_vars[f].value() for f in food_items])
print("Custo: {}".format(value(custoFinal)))

print("\nFunção Objetivo: {}".format(value(prob.objective)))

if ajustar_pesos:
    selected_foods = [food for food in food_items if food_vars[food].varValue > 0]

    # Update the Excel file with incremented weights for selected foods
    updated_weights = {}
    for food in selected_foods:
        updated_weights[food] = pesos[food] + 1

    # Open the Excel file
    df_updated = pd.read_excel("alimentos_porcoes.xlsx", nrows=173)

    # Update the weights in the DataFrame
    for food in updated_weights:
        df_updated.loc[df_updated['Alimentos'] == food, 'Pesos'] = updated_weights[food]

    # Save the updated DataFrame back to the Excel file
    df_updated.to_excel("alimentos_porcoes.xlsx", index=False)
