import random
from collections import Counter

class YahtzeeEngine:
    """Clase encargada de la logica matematica y reglas del juego."""

    @staticmethod
    def lanzar_dados(n):
        return [random.randint(1, 6) for _ in range(n)]

    @staticmethod
    def puntuar_jugada(dados):
        conteo = Counter(dados)
        valores = sorted(list(set(dados)))
        suma = sum(dados)

        puntos = {
            "ones": conteo[1] * 1, "twos": conteo[2] * 2, "threes": conteo[3] * 3,
            "fours": conteo[4] * 4, "fives": conteo[5] * 5, "sixes": conteo[6] * 6,
            "threeOfKind": suma if any(f >= 3 for f in conteo.values()) else 0,
            "fourOfKind": suma if any(f >= 4 for f in conteo.values()) else 0,
            "fullHouse": 25 if (3 in conteo.values() and 2 in conteo.values()) else 0,
            "smallStraight": 30 if any(s in "".join(map(str, valores)) for s in ["1234", "2345", "3456"]) else 0,
            "largeStraight": 40 if any(s in "".join(map(str, valores)) for s in ["12345", "23456"]) else 0,
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
        self.yahtzees_logrados = 0

    def jugar_turno(self):
        """Simula 3 lanzamientos"""
        dados = YahtzeeEngine.lanzar_dados(5)

        for _ in range(2):
            comun, freq = Counter(dados).most_common(1)[0]
            if freq == 5: break
            dados = [comun] * freq + YahtzeeEngine.lanzar_dados(5 - freq)

        posibles = YahtzeeEngine.puntuar_jugada(dados)

        if posibles["yahtzee"] == 50:
            self.yahtzees_logrados+=1

        # Elige la categoria disponible que dé más puntos
        for cat, pts in sorted(posibles.items(), key=lambda x: x[1], reverse=True):
            if self.tablero[cat] is None:
                self.tablero[cat] = pts
                break

    @property
    def puntaje_total(self):
        return sum(v for v in self.tablero.values() if v is not None)


def simular_partidas(n_partidas):
        print(f"Iniciando simulacion de {n_partidas} partidas con IA...\n")
        total_yahtzees=0
        victorias_j1 = 0
        victorias_j2 = 0
        # Variables para almacenar los ultimos jugadores y mostrarlos al final
        ultimo_j1 = None
        ultimo_j2 = None

        for _ in range(n_partidas):
            j1 = JugadorIA("Jugador 1")
            j2 = JugadorIA("Jugador 2")

            # Un juego real de Yahtzee tiene 13 rondas
            for _ in range(13):
                j1.jugar_turno()
                j2.jugar_turno()

            total_yahtzees += (j1.yahtzees_logrados + j2.yahtzees_logrados)

            if j1.puntaje_total > j2.puntaje_total:
                victorias_j1 += 1
            elif j2.puntaje_total > j1.puntaje_total:
                victorias_j2 += 1

            ultimo_j1 = j1
            ultimo_j2 = j2

    # Imprimimos el desglose de ambos jugadores
        for p in [ultimo_j1, ultimo_j2]:
            print(f"{p.nombre}: {p.puntaje_total} puntos")
        # Imprimir en el orden correcto de las reglas
            for cat in ["ones", "twos", "threes", "fours", "fives", "sixes",
                        "threeOfKind", "fourOfKind", "fullHouse",
                        "smallStraight", "largeStraight", "yahtzee", "chance"]:
                print(f"  - {cat.ljust(13)}: {p.tablero[cat]}")
            print()

        prob = (total_yahtzees / (n_partidas * 2 * 13)) * 100
        print(f"--- RESUMEN ({n_partidas} partidas) ---")
        print(f"Probabilidad Yahtzee: {prob:.2f}%")
        print(f"Victorias J1: {victorias_j1} ({victorias_j1/n_partidas*100:.1f}%)")
        print(f"Victorias J2: {victorias_j2} ({victorias_j2/n_partidas*100:.1f}%)")

if __name__ == "__main__":
    simular_partidas(5)