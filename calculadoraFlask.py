from flask import Flask, request, render_template_string

app = Flask(__name__)

# ==========================================
# 1. PROGRAMACIÓN ORIENTADA A OBJETOS (OOP)
# ==========================================
class Calculadora:
    def __init__(self, numero1: float, numero2: float):
        """Constructor con tipado de datos."""
        self.num1 = numero1
        self.num2 = numero2

    def sumar(self) -> float:
        return self.num1 + self.num2

    def determinar_resta(self) -> float:
        return self.num1 - self.num2

    def multiplicar(self) -> float:
        return self.num1 * self.num2

    def dividir(self) -> float:
        if self.num2 == 0:
            raise ValueError("Error")
        return self.num1 / self.num2


# ==========================================
# 2. INTERFAZ DE USUARIO (IDÉNTICA A APPLE)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora Apple Style</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
            background-color: #1e1e24;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        /* Contenedor del Teléfono Simulado */
        .phone-container {
            background-color: #000000;
            width: 360px;
            height: 740px;
            border-radius: 45px;
            padding: 24px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            box-sizing: border-box;
            position: relative;
            border: 4px solid #3a3a3c;
        }

        /* Iconos superiores simulados */
        .top-icons {
            position: absolute;
            top: 25px;
            left: 30px;
            right: 30px;
            display: flex;
            justify-content: space-between;
            color: white;
            font-size: 15px;
            font-weight: 500;
            opacity: 0.9;
        }

        /* Zona de visualización de pantalla */
        .screen {
            text-align: right;
            padding: 0 10px;
            margin-bottom: 20px;
        }

        .history {
            color: #8e8e93;
            font-size: 26px;
            font-weight: 300;
            min-height: 32px;
            margin-bottom: 8px;
        }

        .current-value {
            color: #ffffff;
            font-size: 64px;
            font-weight: 300;
            line-height: 1;
            overflow-x: auto;
            white-space: nowrap;
        }

        /* Cuadrícula de botones */
        .grid-buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin-bottom: 15px;
        }

        /* Estilo base de los botones circulares */
        .btn {
            border: none;
            border-radius: 50%;
            height: 70px;
            width: 70px;
            font-size: 28px;
            font-weight: 400;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: filter 0.1s ease;
            user-select: none;
        }

        .btn:active {
            filter: brightness(1.4);
        }

        /* Colores oficiales de Apple */
        .btn-dark-gray {
            background-color: #333333;
            color: #ffffff;
        }

        .btn-light-gray {
            background-color: #a5a5a5;
            color: #000000;
        }

        .btn-orange {
            background-color: #ff9f0a;
            color: #ffffff;
            font-size: 34px;
        }

        /* Formulario oculto para el envío de datos */
        #calc-form {
            display: none;
        }
    </style>
</head>
<body>

    <div class="phone-container">
        <!-- Barra de iconos superior -->
        <div class="top-icons">
            <span>9:41</span>
            <span>📶 🔋</span>
        </div>

        <!-- Pantalla de resultados -->
        <div class="screen">
            <div class="history" id="html-history">{{ historial if historial else '' }}</div>
            <div class="current-value" id="html-display">{{ resultado if resultado is not none else '0' }}</div>
        </div>

        <!-- Botonera física idéntica a la imagen -->
        <div class="grid-buttons">
            <button class="btn btn-dark-gray" onclick="pressBack()">⌫</button>
            <button class="btn btn-light-gray" onclick="pressClear()">AC</button>
            <button class="btn btn-light-gray" onclick="pressOp('%')">%</button>
            <button class="btn btn-orange" onclick="pressOp('/')">÷</button>

            <button class="btn btn-dark-gray" onclick="pressNum('7')">7</button>
            <button class="btn btn-dark-gray" onclick="pressNum('8')">8</button>
            <button class="btn btn-dark-gray" onclick="pressNum('9')">9</button>
            <button class="btn btn-orange" onclick="pressOp('*')">×</button>

            <button class="btn btn-dark-gray" onclick="pressNum('4')">4</button>
            <button class="btn btn-dark-gray" onclick="pressNum('5')">5</button>
            <button class="btn btn-dark-gray" onclick="pressNum('6')">6</button>
            <button class="btn btn-orange" onclick="pressOp('-')">—</button>

            <button class="btn btn-dark-gray" onclick="pressNum('1')">1</button>
            <button class="btn btn-dark-gray" onclick="pressNum('2')">2</button>
            <button class="btn btn-dark-gray" onclick="pressNum('3')">3</button>
            <button class="btn btn-orange" onclick="pressOp('+')">+</button>

            <button class="btn btn-dark-gray" onclick="pressToggleSign()">+/-</button>
            <button class="btn btn-dark-gray" onclick="pressNum('0')">0</button>
            <button class="btn btn-dark-gray" onclick="pressNum('.')">.</button>
            <button class="btn btn-orange" onclick="submitEquals()">=</button>
        </div>
    </div>

    <!-- Formulario oculto que procesa Flask detrás de escena -->
    <form id="calc-form" method="POST">
        <input type="hidden" name="num1" id="form-num1">
        <input type="hidden" name="num2" id="form-num2">
        <input type="hidden" name="operacion" id="form-op">
        <input type="hidden" name="historial" id="form-historial">
    </form>

    <script>
        let display = document.getElementById('html-display');
        let history = document.getElementById('html-history');
        
        let valorActual = display.innerText === '0' || display.innerText === 'Error' ? '' : display.innerText;
        let primerNumero = '';
        let operacionSeleccionada = '';

        function pressNum(num) {
            if (display.innerText === 'Error') pressClear();
            valorActual += num;
            display.innerText = valorActual;
        }

        function pressOp(op) {
            if (valorActual === '') return;
            primerNumero = valorActual;
            operacionSeleccionada = op;
            let simbolo = op === '/' ? '÷' : op === '*' ? '×' : op === '-' ? '—' : op;
            history.innerText = `${primerNumero}${simbolo}`;
            valorActual = '';
        }

        function pressClear() {
            valorActual = '';
            primerNumero = '';
            operacionSeleccionada = '';
            display.innerText = '0';
            history.innerText = '';
        }

        function pressBack() {
            valorActual = valorActual.slice(0, -1);
            display.innerText = valorActual === '' ? '0' : valorActual;
        }

        function pressToggleSign() {
            if (valorActual !== '') {
                valorActual = (parseFloat(valorActual) * -1).toString();
                display.innerText = valorActual;
            }
        }

        function submitEquals() {
            if (primerNumero === '' || valorActual === '') return;
            
            document.getElementById('form-num1').value = primerNumero;
            document.getElementById('form-num2').value = valorActual;
            document.getElementById('form-op').value = operacionSeleccionada;
            
            let simbolo = operacionSeleccionada === '/' ? '÷' : operacionSeleccionada === '*' ? '×' : operacionSeleccionada === '-' ? '—' : operacionSeleccionada;
            document.getElementById('form-historial').value = `${primerNumero}${simbolo}${valorActual}`;
            
            document.getElementById('calc-form').submit();
        }
    </script>
</body>
</html>
"""


# ==========================================
# 3. CONTROLADOR Y RUTAS DE FLASK
# ==========================================
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    historial = None

    if request.method == "POST":
        try:
            n1 = float(request.form.get("num1", 0))
            n2 = float(request.form.get("num2", 0))
            op = request.form.get("operacion")
            historial = request.form.get("historial")

            # Instanciación Orientada a Objetos (OOP) con constructor
            calc = Calculadora(n1, n2)

            # Estructura de control modular llamando a las funciones
            if op == "+":
                resultado = calc.sumar()
            elif op == "-":
                resultado = calc.determinar_resta()
            elif op == "*":
                resultado = calc.multiplicar()
            elif op == "/":
                resultado = calc.dividir()
            elif op == "%":
                resultado = (n1 * n2) / 100

            # Quitar decimales sobrantes si el resultado es un número entero
        except Exception:
            resultado = "Error"

    return render_template_string(HTML_TEMPLATE, resultado=resultado, historial=historial)


if __name__ == "__main__":
    app.run(debug=True)
