Sugarscapes, expuesto extensamente en el libro "Growing Artificial Societies", publicado en 1996 bajo la autoria de Joshua Epstein y Robert Axtell es un modelo de simulacion clasico, que a traves de una simulacion bastante simple, con agentes de un comportamiento muy sencillo y pocos rasgos a modelar, logra simular con resultados muy realistas los comportamientos de las sociedades humanas en cuanto a distribucion de la riqueza, transmision cultural, reproduccion, combates, entre otros.\n
En SugarScapes, los agentes carecen de una verdadera IA detras de si, y son mas bien homogeneos a pesar de sus diferentes rasgos, debido a que todos actuan de manera similar en la mayor parte de las simulaciones inspiradas en SugarScapes.\n
Nosotros, quisimos explorar el tema de la violencia y la formacion de agrupaciones (bandas de gangster y demas) en la socieda, a traves de nuestra propia version de SugarScapes, pero cargando a los agentes de un comportamiento basado en IA. Queremos estudiar cuanto influyen el rango de vision, de movimiento, la riqueza heredada por un agente, su nivel de consumo, asi como la zona en que nacion en su supervivencia en un ambiente donde la reparticion de los recursos naturales que aparecen distribuidos de manera desigual esta signada por la ley del mas fuerte, por la violencia. Asi, algunos agentes eligiran asociarse a otros, bajo ciertas reglas de asociacion, mientras otro eligiran huir de los conflictos todo el tiempo y otros provocarlo. Cual de estas estrategias es mejor, es mejor la misma para cada tipo de agente en cuando a su capacidad de vision, movimiento y herencia, o para cada nivel de capacidad hay una estrategia que mas probablemente le asegure la supervivencia. Estas y otras preguntas que nos plantearemos son facilmente extrapolables, al igual que nuestra simulacion, a situaciones de la vida real, donde los individuos deben agruparse para tener mas fuerza y/o ejercerla sobre los demas, para sobrevivir, o inlcuso alcanzar mas poder.\n
A diferencia de SugarScapes y sus extremadamente simples y homogeneos agentes, en nuestra simulacion los agentes presentan una diversidad de comportamientos diferentes y recurren a algoritmos clasicos de IA para atenerse a ellos y determinar las acciones que deben realizar para estar mas apegados a su forma de comortamiento y cumplir con su objetivo. Por tanto, el volumen de agentes en cada una de nuestras simulaciones sera menor que el de SugarScapes. EN nuestras simulaciones habra entre una decena y una centena de agentes.\n
Implementamos una version bastante simple de la simulacion, pero esta construida de manera escalable, como para cambiar por completo la manera en que se manejan los ataques y las asociaciones, asi como incluir otros tipos de ineracciones sociales como las extorsiones, sin tener que cambiar nada ni realizar ddemasiado esfuerzo. Primeramente explicaremos la version simple que implementamos, y luego el como se implemento. A medida que vayamos explicando los detalles de ipleentacion iremos explicando otras variantes que pueden er implementadas sin demasiado esfuerzo.\n
Sin mas expliquemos las reglas de la simulacion que estaremos llevando a cabo:
Cada casilla del tablero presenta una cantidad de azucar, que tiene un tope, aunq no es el mismo tope para todas las casillas. Los agentes en cada turno cosechan tanta azucar como hay en la casilla en la que estan ubicados. Consumen de su cosecha y sus reservas tanto como su consumo diario les requiera y el resto lo anhaden a sus reservas.
Los agentes tendran un consumo diario que deberan satisfacer, y mantener sus reservas en numeros no negativos. Cuando bajan a numeros negativos esto indica que no pudieron satisfacer sus necesidades metabolicas y por tanto mueren. \n
Los agentes se pueden atacar entre si, y para realizar un ataque deben sacrificar una parte de sus reservas, mientras mayor la inversion en el ataque mas danho le causara este al rival atacado. Cada ataque va dirigido solo a un rival, pero cada agente puede realizar tantos ataques como desee durante un turno. Cuando un agente muere producto de un ataque, una cantidad de reservas equivalente a cuanto llevaba el agente muerto en elinstante anterior al turno de su muerte, se reparte de manera proporcional entre todos aquellos que lo atacaron en el turno de su muerte.\n
Los agentes pueden asociarse entre si. Una asociacion consiste en un grupo de agentes que entregan una porcion de sus cosechas y recompensas por muertes a la asociacion, y luego toman otra porcion de las recaudaciones totales de la asociacion. Ambas porciones estan definidas para cada agente y no cambian a lo largo de la simulacion. Las asociaciones una vez creadas permanecen estaticas hasta que uno de sus miembros muere, momento en el cual se disuelven. Dos agentes que petenezcan a la misma asociacion no pueden atacarse entre si.\n
Como?
...