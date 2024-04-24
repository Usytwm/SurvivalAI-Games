from experta import Fact, Field, KnowledgeEngine, Rule, DefFacts, MATCH, NOT, AND, OR, P


class EstadoAgente(Fact):
    """Información sobre el estado del agente en el juego."""

    salud = Field(int, default=100)
    posicion = Field(tuple, default=(0, 0))
    amenaza_cercana = Field(bool, default=False)
    recurso_cercano = Field(
        tuple, default=None
    )  # (x, y) de un recurso cercano si existe
    objetivo = Field(
        str, default=""
    )  # Objetivo actual del agente: explorar, huir, recolectar


class SistemaDecisionAgente(KnowledgeEngine):
    @DefFacts()
    def setup_initial_conditions(self):
        yield EstadoAgente(salud=100, posicion=(0, 0), objetivo="explorar")

    @Rule(EstadoAgente(salud=P(lambda x: x < 50), amenaza_cercana=False))
    def buscar_curacion(self):
        print("Salud baja, buscando curación.")
        self.declare(EstadoAgente(objetivo="buscar_curacion"))

    @Rule(EstadoAgente(objetivo="huir"))
    def huir(self):
        print("Huyendo de la amenaza.")
        self.declare(EstadoAgente(objetivo="explorar"))

    @Rule(EstadoAgente(amenaza_cercana=True))
    def huir_de_amenaza(self):
        print("Amenaza detectada cerca, huyendo.")
        self.declare(EstadoAgente(objetivo="huir"))

    @Rule(EstadoAgente(recurso_cercano=MATCH.recurso & P(lambda x: x is not None)))
    def ir_a_recurso(self, recurso):
        print(f"Recurso detectado en {recurso}, moviéndose hacia el recurso.")
        self.declare(EstadoAgente(objetivo="recolectar"))

    @Rule(EstadoAgente(objetivo="recolectar"))
    def recolectar_recurso(self):
        print("Recolectando recurso.")
        self.declare(EstadoAgente(objetivo="explorar"))


# Ejemplo de uso del motor
sistema = SistemaDecisionAgente()
sistema.reset()
sistema.declare(EstadoAgente(recurso_cercano=(1, 1), amenaza_cercana=True))
sistema.run()
sistema.reset()
sistema.declare(EstadoAgente(recurso_cercano=(2, 2), objetivo="huir"))
sistema.run()


# # Definición de Hechos
# class Planta(Fact):
#     """Información sobre la planta."""

#     necesita_agua = Field(str, default="")
#     luz_solar = Field(str, default="")
#     tipo_hojas = Field(str, default="")


# class IdentificadorDePlantas(KnowledgeEngine):
#     @Rule(
#         Planta(necesita_agua="poca", luz_solar="alta", tipo_hojas="pequeñas y gruesas")
#     )
#     def es_cactus(self):
#         print("La planta es probablemente un Cactus.")

#     @Rule(
#         Planta(necesita_agua="mucha", luz_solar="baja", tipo_hojas="grandes y delgadas")
#     )
#     def es_helecho(self):
#         print("La planta es probablemente un Helecho.")

#     @Rule(
#         Planta(
#             necesita_agua="moderada",
#             luz_solar="media",
#             tipo_hojas="coloridas y duraderas",
#         )
#     )
#     def es_orquidea(self):
#         print("La planta es probablemente una Orquídea.")


# # Ejecución del Motor

# identificador = IdentificadorDePlantas()
# identificador.reset()  # Preparar el motor de inferencia

# # Recoger características de la planta del usuario
# necesita_agua = input(
#     "¿Cuánta agua necesita la planta? (poca/mucha/moderada): "
# ).lower()
# luz_solar = input("¿Cuánta luz solar necesita la planta? (baja/media/alta): ").lower()
# tipo_hojas = input(
#     "Describe las hojas de la planta (pequeñas y gruesas/grandes y delgadas/coloridas y duraderas): "
# ).lower()

# # Declarar un hecho Planta con las características recogidas
# identificador.declare(
#     Planta(necesita_agua=necesita_agua, luz_solar=luz_solar, tipo_hojas=tipo_hojas)
# )

# identificador.run()  # Ejecutar el motor
