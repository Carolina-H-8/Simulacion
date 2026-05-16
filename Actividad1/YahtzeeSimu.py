import random
from collections import Counter

class YahtzeeEngine:
    @staticmethod
    def lanzar_dados(n):
        return [random.randint(1, 6) for _ in range(n)]

    @staticmethod
    def puntuar_jugada(dados):
        conteo = Counter(dados)
        valores = sorted(list(set(dados)))
        suma = sum(dados)
        cadena = "".join(map(str, valores))

        puntos = {
            "ones": conteo[1] * 1, "twos": conteo[2] * 2, "threes": conteo[3] * 3,
            "fours": conteo[4] * 4, "fives": conteo[5] * 5, "sixes": conteo[6] * 6,
            "threeOfKind": suma if any(f >= 3 for f in conteo.values()) else 0,
            "fourOfKind": suma if any(f >= 4 for f in conteo.values()) else 0,
            "fullHouse": 25 if (3 in conteo.values() and 2 in conteo.values()) else 0,
            "smallStraight": 30 if any(s in cadena for s in ["1234", "2345", "3456"]) else 0,
            "largeStraight": 40 if any(s in cadena for s in ["12345", "23456"]) else 0,
            "yahtzee": 50 if 5 in conteo.values() else 0,
            "chance": suma
        }
        return puntos

class JugadorIA:
    def __init__(self, nombre):
        self.nombre = nombre
        self.orden_prioridad = [
            "yahtzee", "largeStraight", "smallStraight", "fullHouse",
            "fourOfKind", "threeOfKind", "sixes", "fives", "fours",
            "threes", "twos", "ones", "chance"
        ]
        self.tablero = {cat: None for cat in self.orden_prioridad}
        # Diccionario para contar cuántas veces logra cada jugada especial este jugador
        self.logros = Counter()

    def jugar_turno(self):
        dados = YahtzeeEngine.lanzar_dados(5)

        for _ in range(2):
            comun, freq = Counter(dados).most_common(1)[0]
            if freq == 5: break
            dados = [comun] * freq + YahtzeeEngine.lanzar_dados(5 - freq)

        posibles = YahtzeeEngine.puntuar_jugada(dados)

        # Registro de eventos especiales si el puntaje es mayor a 0
        for cat in ["fullHouse", "smallStraight", "largeStraight", "yahtzee"]:
            if posibles[cat] > 0:
                self.logros[cat] += 1

        # Elige la mejor categoría disponible
        for cat in self.orden_prioridad:
            if self.tablero[cat] is None:
                self.tablero[cat] = posibles[cat]
                break

    @property
    def puntaje_total(self):
        return sum(v for v in self.tablero.values() if v is not None)

def simular_partidas(n_partidas):
    print(f"🚀 Iniciando simulación de {n_partidas:,} partidas...\n")
    
    # Contadores globales para toda la simulación
    stats_globales = Counter()
    victorias_j1 = 0
    victorias_j2 = 0
    ultimo_j1 = None
    ultimo_j2 = None

    for _ in range(n_partidas):
        j1 = JugadorIA("Jugador 1")
        j2 = JugadorIA("Jugador 2")

        for _ in range(13):
            j1.jugar_turno()
            j2.jugar_turno()

        # Acumular logros de los jugadores en las estadísticas globales
        stats_globales.update(j1.logros)
        stats_globales.update(j2.logros)

        if j1.puntaje_total > j2.puntaje_total: victorias_j1 += 1
        elif j2.puntaje_total > j1.puntaje_total: victorias_j2 += 1

        ultimo_j1, ultimo_j2 = j1, j2



    # --- REPORTE DE LA ÚLTIMA PARTIDA ---
    for p in [ultimo_j1, ultimo_j2]:
        print(f"{p.nombre}: {p.puntaje_total} puntos")
        for cat in ["ones", "twos", "threes", "fours", "fives", "sixes", 
                    "threeOfKind", "fourOfKind", "fullHouse", "smallStraight", 
                    "largeStraight", "yahtzee", "chance"]:
            print(f"  - {cat.ljust(15)}: {p.tablero[cat]}")
        print()

    # --- RESUMEN ESTADÍSTICO ---
    PROBS_TEORICAS = {
        "yahtzee": 4.60,
        "fullHouse": 30.10,
        "largeStraight": 25.80,
        "smallStraight": 61.50  
    }
    
    total_turnos = n_partidas * 2 * 13
    print(f"--- 📊 COMPARATIVA: TEORÍA (3 TIRO) VS. IA (3 TIROS) ---")
    print(f"Total de turnos analizados: {total_turnos:,}\n")
    
    especiales = [
        ("yahtzee", "Yahtzee"), 
        ("fullHouse", "Full House"), 
        ("largeStraight", "Esc. Grande"), 
        ("smallStraight", "Esc. Pequeña")
    ]

    for key, nombre in especiales:
        cantidad = stats_globales[key]
        prob_simulada = (cantidad / total_turnos) * 100
        prob_teorica = PROBS_TEORICAS[key]
        
        # Eficiencia: Qué tan cerca está nuestra IA del máximo posible
        eficiencia = (prob_simulada / prob_teorica) * 100
        
        print(f"  - {nombre.ljust(15)}:")
        print(f"    Simulado (IA):  {prob_simulada:7.3f}%")
        print(f"    Teórico Óptimo: {prob_teorica:7.3f}%")
        print(f"    Eficiencia IA:  {eficiencia:7.1f}% de la capacidad máxima")
        print("-" * 45)

if __name__ == "__main__":
    simular_partidas(10000)