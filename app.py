from multiapp import MultiApp
from apps import uls, exportaciones, home, mapas


app = MultiApp()


# Add all your applications here
app.add_app("Inicio",home.app)
#app.add_app("Importaciones y exportaciones", exportaciones.app)
#app.add_app("ULS", uls.app)
app.add_app("Importaciones", mapas.app)

# The main app
app.run()
