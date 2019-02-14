
lista = [{'num_red':0},{'num_red':0},{'num_red':0},{'num_red':1},{'num_red':0},{'num_red':1},{'num_red':2}]
# string lista[1,2,2]

red_anterior = -5
num_redes = 0
nueva = []

for l in lista:
    

    if l['num_red'] == 0 and red_anterior == 0:
        nueva.append(num_redes)
        num_redes = 0
    elif l['num_red'] == 0 and red_anterior > 0:
        nueva.append(num_redes)
        num_redes = 0
    
    red_anterior = l['num_red']
    num_redes += 1

nueva.append(num_redes)
print(nueva)

    # print(l['num_red'])