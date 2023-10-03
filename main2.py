import pandas as pd
from pulp import *

df = pd.read_excel("carolina_dados.xlsx", nrows=295)
df.head()

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Simple Diet Problem", LpMinimize)

# Creates a list of the Ingredients
food_items = list(df['Alimentos'])

ajustar_pesos = True

print("So, the food items to consdier, are \n" + "-" * 100)
for f in food_items:
    print(f, end=', ')

energia = dict(zip(food_items, df['Energia']))

proteina = dict(zip(food_items, df['Proteína']))

carboidrato = dict(zip(food_items, df['Carboidrato']))

fibra = dict(zip(food_items, df['Fibra']))

calcio = dict(zip(food_items, df['Cálcio']))

magnesio = dict(zip(food_items, df['Magnésio']))

fosforo = dict(zip(food_items, df['Fósforo']))

ferro = dict(zip(food_items, df['Ferro']))

sodio = dict(zip(food_items, df['Sódio']))

zinco = dict(zip(food_items, df['Zinco']))

pesos = dict(zip(food_items, df['Pesos']))

classificacao = dict(zip(food_items, df['Classificacao']))

# Dicionário para armazenar a contagem de classificações necessárias para cada refeição
contagem_classificacoes_necessarias = {
    "Café da Manhã": {"B": 1, "F": 1, "C1": 1},
    "Primeiro Lanche": {"F/L": 1},
    "Almoço": {"C2": 1, "G": 1, "V": 2, "P": 1, "S": 1},
    "Segundo Lanche": {"B/S": 1, "C1": 1},
    "Jantar": {"C2": 1, "G": 1, "V": 1, "P": 1},
    "Ceia": {"F/L": 1}
}

# Crie uma lista com os nomes das refeições
nomes_refeicoes = ["Café da Manhã", "Primeiro Lanche", "Almoço", "Segundo Lanche", "Jantar", "Ceia"]

chosen_vars = {}
for f in food_items:
    if classificacao[f] == "V":
        chosen_vars[f] = LpVariable(f"Chosen_{f}", 0, 1, LpBinary)

# A dictionary called 'food_vars' is created to contain the referenced Variables
# Continuous para numeros reais e Integer para numeros inteiros
food_vars = LpVariable.dicts("Selecao", (nomes_refeicoes, food_items), 0, cat='Integer')

# The objective function is added to 'prob' first
prob += lpSum([((0.7 * (carboidrato[i] * food_vars[ref][i])) + (0.3 * (energia[i] * food_vars[ref][i]))) for ref in nomes_refeicoes for i in food_items])

prob += lpSum([food_vars["Café da Manhã"][f] for f in food_items]) == 3, "Total_Café_da_Manhã"
prob += lpSum([food_vars["Primeiro Lanche"][f] for f in food_items]) == 1, "Total_Primeiro_Lanche"
prob += lpSum([food_vars["Almoço"][f] for f in food_items]) == 6, "Total_Almoço_Lanche"
prob += lpSum([food_vars["Segundo Lanche"][f] for f in food_items]) == 2, "Total_Segundo_Lanche"
prob += lpSum([food_vars["Jantar"][f] for f in food_items]) == 4, "Total_Jantar_Lanche"
prob += lpSum([food_vars["Ceia"][f] for f in food_items]) == 1, "Total_Ceia_Lanche"

prob += lpSum(chosen_vars[f] for f in chosen_vars) == 2, "Exactly_2_V_Foods"

for f in chosen_vars:
    prob += food_vars["Almoço"][f] <= chosen_vars[f], f"Choose_{f}_If_ChosenVar_Is_1"

# prob += lpSum([(costs[i] * (porcao[i]/100)) * food_vars[i] for i in food_items]), "Total Cost of the balanced diet"

# prob += lpSum([(costs[f] * (porcao[f]/100)) * food_vars[f] for f in food_items]) <= 8.657, "Custo maximo"

# Pesos
prob += lpSum([(pesos[f]) * food_vars[ref][f] for ref in nomes_refeicoes for f in food_items]) <= 5.0

# Energia(Calorias) - Variável
prob += lpSum([(energia[f]) * food_vars[ref][f] for ref in nomes_refeicoes for f in food_items]) >= 1800.0, "CaloriaMinima"
#prob += lpSum([(energia[f]) * food_vars[ref][f] for ref in nomes_refeicoes for f in food_items]) <= 2200.0, "CaloriaMaxima"

# Carboidrato - Variável
prob += lpSum([(carboidrato[f]) * food_vars[ref][f] for ref in nomes_refeicoes for f in food_items]) >= 202.5, "CarboidratoMinimo"

# Sodio
prob += lpSum([(sodio[f]) * food_vars[ref][f] for ref in nomes_refeicoes for f in food_items]) <= 2000.0, "SodioMaximo"

# Proteinas
prob += lpSum([(proteina[f]) * food_vars[ref][f] for ref in nomes_refeicoes for f in food_items]) >= 75.0, "ProteinasMinimo"
#prob += lpSum([(proteina[f]) * food_vars[ref][f] for ref in nomes_refeicoes for f in food_items]) <= 38.4, "ProteinasMaximo"

# Fibras
prob += lpSum([(fibra[f]) * food_vars[ref][f] for ref in nomes_refeicoes for f in food_items]) >= 30.0, "FibrasMinimo"

# Calcio
prob += lpSum([(calcio[f]) * food_vars[ref][f] for ref in nomes_refeicoes for f in food_items]) >= 850.0, "CalcioMinimo"

# Magnesio
prob += lpSum([(magnesio[f]) * food_vars[ref][f] for ref in nomes_refeicoes for f in food_items]) >= 400.0, "MagnesioMinimo"

# Fosforo
prob += lpSum([(fosforo[f]) * food_vars[ref][f] for ref in nomes_refeicoes for f in food_items]) >= 700.0, "FosforoMinimo"

# Ferro
prob += lpSum([(ferro[f]) * food_vars[ref][f] for ref in nomes_refeicoes for f in food_items]) >= 18.0, "FerroMinimo"

# Zinco
prob += lpSum([(zinco[f]) * food_vars[ref][f] for ref in nomes_refeicoes for f in food_items]) >= 15.0, "ZincoMinimo"

# Adicione restrições para garantir que as classificações necessárias estejam presentes em cada refeição
for refeicao in nomes_refeicoes:
    for classificacao_ref in contagem_classificacoes_necessarias[refeicao]:
        if "/" in classificacao_ref:
            classes_possiveis = classificacao_ref.split("/")
            if classificacao_ref == "F/L" or classificacao_ref == "B/S":
                prob += lpSum([food_vars[refeicao][f] for f in food_items if classificacao[f] in classes_possiveis]) \
                        == contagem_classificacoes_necessarias[refeicao][classificacao_ref], \
                        "{}_{}_Exact".format(refeicao, classificacao_ref)
            else:
                prob += lpSum([food_vars[refeicao][f] for f in food_items if classificacao[f] in classes_possiveis]) \
                        <= contagem_classificacoes_necessarias[refeicao][classificacao_ref], \
                        "{}_{}_Max".format(refeicao, classificacao_ref)
        else:
            prob += lpSum([food_vars[refeicao][f] for f in food_items if classificacao[f] == classificacao_ref]) \
                    == contagem_classificacoes_necessarias[refeicao][classificacao_ref], \
                    "{}_{}_Exact".format(refeicao, classificacao_ref)

# The problem data is written to an .lp file
prob.writeLP("SimpleDietProblem.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# for f in food_items:
#     for ref in nomes_refeicoes:
#         if food_vars[ref][f].varValue > 0:
#             print(f, food_vars[ref][f].name, food_vars[ref][f].varValue)

for refeicao in nomes_refeicoes:
    print("\n")
    print("Alimentos para {}:".format(refeicao))
    for f in food_items:
        if food_vars[refeicao][f].varValue > 0:
            print(f, "=", round(food_vars[refeicao][f].varValue, 2))

energiaFinal = lpSum([energia[f] * food_vars[ref][f].varValue for ref in nomes_refeicoes for f in food_items])
print("\nCalorias: {}".format(value(energiaFinal)))

carboidratoFinal = lpSum([carboidrato[f] * food_vars[ref][f].varValue for ref in nomes_refeicoes for f in food_items])
print("Carboidratos: {}".format(value(carboidratoFinal)))

sodioFinal = lpSum([sodio[f] * food_vars[ref][f].varValue for ref in nomes_refeicoes for f in food_items])
print("Sódio: {}".format(value(sodioFinal)))

proteinaFinal = lpSum([proteina[f] * food_vars[ref][f].varValue for ref in nomes_refeicoes for f in food_items])
print("Proteínas: {}".format(value(proteinaFinal)))

fibraFinal = lpSum([fibra[f] * food_vars[ref][f].varValue for ref in nomes_refeicoes for f in food_items])
print("Fibras: {}".format(value(fibraFinal)))

calcioFinal = lpSum([calcio[f] * food_vars[ref][f].varValue for ref in nomes_refeicoes for f in food_items])
print("Cálcio: {}".format(value(calcioFinal)))

magnesioFinal = lpSum([magnesio[f] * food_vars[ref][f].varValue for ref in nomes_refeicoes for f in food_items])
print("Magnésio: {}".format(value(magnesioFinal)))

fosforoFinal = lpSum([fosforo[f] * food_vars[ref][f].varValue for ref in nomes_refeicoes for f in food_items])
print("Fósforo: {}".format(value(fosforoFinal)))

ferroFinal = lpSum([ferro[f] * food_vars[ref][f].varValue for ref in nomes_refeicoes for f in food_items])
print("Ferro: {}".format(value(ferroFinal)))

zincoFinal = lpSum([zinco[f] * food_vars[ref][f].varValue for ref in nomes_refeicoes for f in food_items])
print("Zinco: {}".format(value(zincoFinal)))

print("\nFunção Objetivo: {}".format(value(prob.objective)))

if ajustar_pesos:
    selected_foods = [food for food in food_items if sum(food_vars[ref][food].varValue for ref in nomes_refeicoes) > 0]

    # Foods not selected in the solution
    not_selected_foods = list(set(food_items) - set(selected_foods))

    # Open the Excel file
    df_updated = pd.read_excel("carolina_dados.xlsx", nrows=295)

    # Update the weights in the DataFrame for selected foods
    for food in selected_foods:
        df_updated.loc[df_updated['Alimentos'] == food, 'Pesos'] += 1

    # Update the weights in the DataFrame for non-selected foods
    for food in not_selected_foods:
        # Ensure weight doesn't fall below 0
        if df_updated.loc[df_updated['Alimentos'] == food, 'Pesos'].iloc[0] > 0:
            df_updated.loc[df_updated['Alimentos'] == food, 'Pesos'] -= 1

    # Save the updated DataFrame back to the Excel file
    df_updated.to_excel("carolina_dados.xlsx", index=False)
