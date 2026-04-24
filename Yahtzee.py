import random
from collections import Counter

def lanzar_dados(cantidad):
    """Simula el lanzamiento de 'n' dados de 6 caras."""
    return [random.randint(1, 6) for _ in range(cantidad)]

def turno_simulado():
    """Simula el turno completo de un jugador (hasta 3 lanzamientos)."""
    # Lanzamiento 1: 5 dados
    dados = lanzar_dados(5)
    
    for lanzamiento in range(2): # 2 lanzamientos extra permitidos
        # Contamos cuántas veces aparece cada número
        conteo = Counter(dados)
        # Obtenemos el número que más salió y cuántas veces salió
        valor_mas_comun, frecuencia = conteo.most_common(1)[0]
        
        # Si ya tenemos un Yahtzee (5 iguales), no necesitamos lanzar más
        if frecuencia == 5:
            break
            
        # "Guardamos" los dados que tienen el valor más común
        dados_guardados = [valor_mas_comun] * frecuencia
        
        # Lanzamos los dados restantes (5 - los que guardamos)
        dados_nuevos = lanzar_dados(5 - frecuencia)
        
        # Juntamos los guardados con los nuevos
        dados = dados_guardados + dados_nuevos
        
    return dados

def partida_dos_jugadores():
    """Simula una partida de muestra entre 2 jugadores."""
    print("=== PARTIDA: JUGADOR 1 vs JUGADOR 2 ===")
    dados_j1 = turno_simulado()
    dados_j2 = turno_simulado()
    
    print(f"Jugador 1 finaliza su turno con: {dados_j1}")
    print(f"Jugador 2 finaliza su turno con: {dados_j2}")
    
    # Gana el que tenga la mayor cantidad de dados iguales
    max_j1 = Counter(dados_j1).most_common(1)[0][1]
    max_j2 = Counter(dados_j2).most_common(1)[0][1]
    
    if max_j1 > max_j2:
        print("-> Ganador: Jugador 1")
    elif max_j2 > max_j1:
        print("-> Ganador: Jugador 2")
    else:
        print("-> Resultado: Empate")

def simulacion_montecarlo(iteraciones):
    """Aplica el método de Montecarlo ejecutando el turno miles de veces."""
    print(f"\n=== SIMULACIÓN DE MONTECARLO ({iteraciones} iteraciones) ===")
    exitos_yahtzee = 0
    
    for _ in range(iteraciones):
        resultado_final = turno_simulado()
        # Verificamos si los 5 dados son iguales
        if Counter(resultado_final).most_common(1)[0][1] == 5:
            exitos_yahtzee += 1
            
    probabilidad = (exitos_yahtzee / iteraciones) * 100
    print(f"Total de Yahtzees obtenidos: {exitos_yahtzee}")
    print(f"Probabilidad empírica de obtener Yahtzee: {probabilidad:.2f}%")
# --- EJECUCIÓN DEL PROGRAMA ---
# Ejecuta una partida de prueba en la consola
partida_dos_jugadores()

# Ejecuta la simulación masiva de probabilidades
simulacion_montecarlo(10000)