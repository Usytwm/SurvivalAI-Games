from environment.map_controller import Map

mapa = Map(10, 10)
mapa.display()
mapa.add_object(3, 3, 'A')
mapa.add_object(4, 5, 'B')
print(mapa.peek_from(5, 5, 2))