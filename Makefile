run:
	@echo "Ejecutando el juego de supervivencia..."
	@venv\Scripts\activate && python src/main.py

setup:
	@echo "Configurando el entorno virtual y instalando dependencias..."
	python -m venv venv
	@venv\Scripts\activate && pip install -r requirements.txt

freeze:
	@venv\Scripts\activate && pip freeze > requirements.txt

