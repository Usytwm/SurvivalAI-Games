.PHONY: run sim setup freeze run-linux sim-linux setup-linux freeze-linux

# Comandos para Windows
run:
	@echo "Ejecutando juego de supervivencia en Windows..."
	@venv\Scripts\activate && python src/main.py

sim:
	@echo "Ejecutando pruebas de simulaciones en Windows..."
	@venv\Scripts\activate && python src/statistics_main.py

setup:
	@echo "Configurando el entorno virtual y instalando dependencias en Windows..."
	python -m venv venv
	@venv\Scripts\activate && pip install -r requirements.txt

freeze:
	@venv\Scripts\activate && pip freeze > requirements.txt

# Comandos para Linux
run-linux:
	@echo "Ejecutando juego de supervivencia en Linux..."
	@source venv/bin/activate && python src/main.py

sim-linux:
	@echo "Ejecutando pruebas de simulaciones en Linux..."
	@source venv/bin/activate && python src/statistics_main.py

setup-linux:
	@echo "Configurando el entorno virtual y instalando dependencias en Linux..."
	python -m venv venv
	@source venv/bin/activate && pip install -r requirements.txt

freeze-linux:
	@source venv/bin/activate && pip freeze > requirements.txt
