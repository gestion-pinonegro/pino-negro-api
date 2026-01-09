from database import create_tables
from menu import MenuApp

create_tables()

app = MenuApp()
app.ejecutar()
