Bueno, mi proyecto es una calculadora para la computadora que funciona de verdad y la he programado usando el lenguaje Python. Para que no sea solo una pantalla negra aburrida con letras, le metí una librería que se llama Tkinter, que sirve para dibujar la ventana, ponerle los botones bien cuadraditos uno por uno y una cajita de texto arriba que es la pantalla donde se ven los números que vas escribiendo.
Para que el código me salga bien y no me esté botando errores a cada rato, usé la inteligencia artificial Claude IA. Me ayudó un montón a ordenar la lógica de la matemática para que sume, reste, multiplique y divida rápido. También le programamos con la IA para que si por error alguien quiere dividir entre cero, la calculadora no se cuelgue ni se cierre de la nada, sino que te avise que está mal. El diseño lo pensé para que sea bien fácil de usar, le das clic a los botones con el mouse, calcula al toque en tiempo real y tiene su botón para borrar todo y empezar otra operación de nuevo. Me ha servido bastante para practicar cómo hacer interfaces y usar IA para mejorar mi código en este semestre de DSI.
   <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/95fb68e8-3711-417d-9452-e3d543565856" />
```python
import tkinter as tk
from tkinter import font
import math
import re

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora con Temas")
        self.root.resizable(False, False)

        # 🎨 DEFINICIÓN DE TEMAS
        self.temas = {
            "Clásico iOS": {
                "bg_principal": "#1C1C1E",
                "func":  {"bg": "#3A3A3C", "fg": "#FFFFFF", "hover": "#545458"},
                "op":    {"bg": "#FF9F0A", "fg": "#FFFFFF", "hover": "#FFB340"},
                "num":   {"bg": "#2C2C2E", "fg": "#FFFFFF", "hover": "#3A3A3C"},
                "igual": {"bg": "#FF9F0A", "fg": "#FFFFFF", "hover": "#FFB340"},
                "texto_display": "#FFFFFF",
                "texto_historial": "#8E8E93"
            },
            "Modo Matrix": {
                "bg_principal": "#000000",
                "func":  {"bg": "#0D2B0D", "fg": "#00FF00", "hover": "#1A541A"},
                "op":    {"bg": "#00FF00", "fg": "#000000", "hover": "#33FF33"},
                "num":   {"bg": "#000000", "fg": "#00FF00", "hover": "#111111"},
                "igual": {"bg": "#00FF00", "fg": "#000000", "hover": "#33FF33"},
                "texto_display": "#00FF00",
                "texto_historial": "#008800"
            },
            "Pastel Soft": {
                "bg_principal": "#F4F1DE",
                "func":  {"bg": "#E07A5F", "fg": "#FFFFFF", "hover": "#F28482"},
                "op":    {"bg": "#3D405B", "fg": "#FFFFFF", "hover": "#5C618A"},
                "num":   {"bg": "#F2CC8F", "fg": "#3D405B", "hover": "#F4D7A8"},
                "igual": {"bg": "#81B29A", "fg": "#FFFFFF", "hover": "#94C1A8"},
                "texto_display": "#3D405B",
                "texto_historial": "#7F8487"
            },
            "Monocromo": {
                "bg_principal": "#FFFFFF",
                "func":  {"bg": "#E5E5E5", "fg": "#000000", "hover": "#CCCCCC"},
                "op":    {"bg": "#000000", "fg": "#FFFFFF", "hover": "#333333"},
                "num":   {"bg": "#F5F5F7", "fg": "#000000", "hover": "#E5E5E5"},
                "igual": {"bg": "#000000", "fg": "#FFFFFF", "hover": "#333333"},
                "texto_display": "#000000",
                "texto_historial": "#8E8E93"
            }
        }
        
        # Tema inicial por defecto
        self.tema_actual = "Clásico iOS"

        self.expresion = ""
        self.resultado_mostrado = False
        self.lista_botones = []  # Almacena referencias para cambiar colores dinámicamente

        # Configuración inicial de entorno gráfico
        self.root.configure(bg=self.temas[self.tema_actual]["bg_principal"])
        self._construir_menu()
        self._construir_ui()
        self.aplicar_tema(self.tema_actual)

    def _construir_menu(self):
        # Barra superior de menú
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu)

        # Menú desplegable para los Temas
        menu_temas = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Temas", menu=menu_temas)

        # Cargar opciones desde el diccionario
        for nombre_tema in self.temas.keys():
            menu_temas.add_command(label=nombre_tema, command=lambda t=nombre_tema: self.aplicar_tema(t))

    def _construir_ui(self):
        self.pantalla_frame = tk.Frame(self.root, padx=20, pady=20)
        self.pantalla_frame.pack(fill="both")

        self.var_historial = tk.StringVar(value="")
        self.historial_label = tk.Label(
            self.pantalla_frame,
            textvariable=self.var_historial,
            font=("Helvetica Neue", 14),
            anchor="e",
            width=18,
        )
        self.historial_label.pack(fill="x")

        self.var_display = tk.StringVar(value="0")
        self.display = tk.Label(
            self.pantalla_frame,
            textvariable=self.var_display,
            font=("Helvetica Neue", 52, "bold"),
            anchor="e",
            width=10,
        )
        self.display.pack(fill="x")

        self.botones_frame = tk.Frame(self.root, padx=12, pady=8)
        self.botones_frame.pack()

        layout = [
            ("AC", 0, 0, 1, "func"),  ("±", 0, 1, 1, "func"), ("%", 0, 2, 1, "func"), ("÷", 0, 3, 1, "op"),
            ("7",  1, 0, 1, "num"),   ("8", 1, 1, 1, "num"),  ("9", 1, 2, 1, "num"),  ("×", 1, 3, 1, "op"),
            ("4",  2, 0, 1, "num"),   ("5", 2, 1, 1, "num"),  ("6", 2, 2, 1, "num"),  ("−", 2, 3, 1, "op"),
            ("1",  3, 0, 1, "num"),   ("2", 3, 1, 1, "num"),  ("3", 3, 2, 1, "num"),  ("+", 3, 3, 1, "op"),
            ("0",  4, 0, 2, "num"),   (",", 4, 2, 1, "num"),  ("=", 4, 3, 1, "igual"),
        ]

        GAP = 10
        BTN_SIZE = 72

        for (texto, fila, col, colspan, tipo) in layout:
            ancho = BTN_SIZE * colspan + GAP * (colspan - 1)

            btn = tk.Button(
                self.botones_frame,
                text=texto,
                font=("Helvetica Neue", 22, "bold") if tipo == "num" else ("Helvetica Neue", 20, "bold"),
                relief="flat",
                borderwidth=0,
                cursor="hand2",
                width=1,
                height=1,
                command=lambda t=texto: self._on_click(t),
            )

            btn.grid(
                row=fila, column=col,
                columnspan=colspan,
                padx=GAP // 2, pady=GAP // 2,
                sticky="nsew",
                ipadx=0, ipady=14,
            )
            btn.configure(width=ancho // 14)
            
            # Guardamos la referencia para el cambio de tema reactivo
            self.lista_botones.append((btn, tipo))

        for i in range(4):
            self.botones_frame.columnconfigure(i, weight=1, minsize=BTN_SIZE)

        self.root.bind("<Key>", self._on_key)

    def aplicar_tema(self, nombre_tema):
        self.tema_actual = nombre_tema
        t = self.temas[nombre_tema]

        # Cambiar color de contenedores de fondo
        self.root.configure(bg=t["bg_principal"])
        self.pantalla_frame.configure(bg=t["bg_principal"])
        self.botones_frame.configure(bg=t["bg_principal"])

        # Cambiar color de etiquetas de texto
        self.historial_label.configure(bg=t["bg_principal"], fg=t["texto_historial"])
        self.display.configure(bg=t["bg_principal"], fg=t["texto_display"])

        # Actualizar colores individuales y eventos hover de los botones
        for btn, tipo in self.lista_botones:
            colores = t[tipo]
            btn.configure(
                bg=colores["bg"],
                fg=colores["fg"],
                activebackground=colores["hover"],
                activeforeground=colores["fg"]
            )
            # Re-vincular eventos Hover con la paleta de colores del nuevo tema
            btn.bind("<Enter>", lambda e, b=btn, h=colores["hover"]: b.configure(bg=h))
            btn.bind("<Leave>", lambda e, b=btn, orig=colores["bg"]: b.configure(bg=orig))

    def _actualizar_display(self, valor=None):
        texto = valor if valor is not None else self.expresion
        if texto == "" or texto == "-":
            texto = "0"
        
        largo = len(texto)
        if largo <= 9:
            size = 52
        elif largo <= 13:
            size = 36
        else:
            size = 24
        self.display.configure(font=("Helvetica Neue", size, "bold"))
        self.var_display.set(texto)

    def _on_click(self, tecla):
        if tecla == "AC":
            self.expresion = ""
            self.var_historial.set("")
            self.resultado_mostrado = False
            self._actualizar_display("0")

        elif tecla == "⌫":
            if self.resultado_mostrado:
                self.var_historial.set("")
            self.expresion = self.expresion[:-1]
            self.resultado_mostrado = False
            self._actualizar_display()

        elif tecla == "±":
            if self.expresion:
                tokens = re.split(r'([÷×+−])', self.expresion)
                ultimo_token = tokens[-1]
                if ultimo_token and ultimo_token != "0":
                    if ultimo_token.startswith("-"):
                        tokens[-1] = ultimo_token[1:]
                    else:
                        tokens[-1] = "-" + ultimo_token
                    self.expresion = "".join(tokens)
                self._actualizar_display()

        elif tecla == "%":
            if self.expresion:
                try:
                    expr = self.expresion.replace(",", ".").replace("×", "*").replace("÷", "/").replace("−", "-")
                    val = eval(expr)
                    self.expresion = self._formatear(val / 100)
                    self.resultado_mostrado = True
                    self._actualizar_display()
                except Exception:
                    self._actualizar_display("Error")

        elif tecla in ("÷", "×", "+", "−"):
            if self.expresion:
                self.resultado_mostrado = False
                ultimo = self.expresion[-1]
                if ultimo in "÷×+−":
                    self.expresion = self.expresion[:-1]
                self.expresion += tecla
                self._actualizar_display()

        elif tecla == ",":
            if self.resultado_mostrado:
                self.expresion = "0,"
                self.resultado_mostrado = False
            else:
                if not self.expresion or self.expresion[-1] in "÷×+−":
                    self.expresion += "0"
                if "," not in self._ultimo_numero():
                    self.expresion += ","
            self._actualizar_display()

        elif tecla == "=":
            if self.expresion:
                if self.expresion[-1] in "÷×+−":
                    self.expresion = self.expresion[:-1]
                try:
                    expr = self.expresion.replace(",", ".").replace("×", "*").replace("÷", "/").replace("−", "-")
                    resultado = eval(expr)
                    historial = self.expresion + " ="
                    self.var_historial.set(historial)
                    self.expresion = self._formatear(resultado)
                    self.resultado_mostrado = True
                    self._actualizar_display()
                except ZeroDivisionError:
                    self._actualizar_display("Error")
                    self.expresion = ""
                    self.resultado_mostrado = False
                except Exception:
                    self._actualizar_display("Error")
                    self.expresion = ""
                    self.resultado_mostrado = False

        else:
            if self.resultado_mostrado:
                self.expresion = ""
                self.resultado_mostrado = False
            if self.expresion == "0" and tecla == "0":
                return
            if self.expresion == "0" and tecla != "0":
                self.expresion = ""
            self.expresion += tecla
            self._actualizar_display()

    def _ultimo_numero(self):
        partes = re.split(r'[÷×+−]', self.expresion)
        return partes[-1] if partes else ""

    def _formatear(self, valor):
        if isinstance(valor, float) and valor.is_integer():
            valor = int(valor)
        if isinstance(valor, float):
            valor = round(valor, 8)
        texto = str(valor)
        texto = texto.replace(".", ",")
        return texto

    def _on_key(self, event):
        mapa = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            "+": "+", "-": "−", "*": "×", "/": "÷",
            ".": ",", ",": ",",
            "Return": "=", "equal": "=",
            "Escape": "AC", "Delete": "AC", 
            "BackSpace": "⌫",
            "percent": "%",
        }
        tecla = mapa.get(event.keysym, mapa.get(event.char, None))
        if tecla:
            self._on_click(tecla)
```


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculadora(root)
    root.mainloop()
