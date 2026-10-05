from flask import Flask, jsonify, request, render_template_string
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            stock INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

HTML_FUTURISTA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taller ABP - Elaborado por Jose Rafael Correa</title>
    <style>
        :root {
            --bg-color: #05050a;
            --panel-bg: rgba(13, 17, 33, 0.7);
            --neon-cyan: #00f0ff;
            --neon-purple: #b000ff;
            --neon-green: #00ff66;
            --neon-red: #ff0055;
            --text-main: #e0e6ed;
            --text-muted: #8a99ad;
            --border-glow: rgba(0, 240, 255, 0.3);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, Helvetica, sans-serif; }
        body {
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(176, 0, 255, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(0, 240, 255, 0.08) 0%, transparent 40%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 30px 15px;
        }
        .container {
            width: 100%;
            max-width: 1000px;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-glow);
            padding-bottom: 20px;
            margin-bottom: 25px;
            flex-wrap: wrap;
            gap: 15px;
        }
        h1 {
            font-size: 1.5rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(0,240,255,0.2);
        }
        .status-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(0, 255, 102, 0.1);
            border: 1px solid var(--neon-green);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            color: var(--neon-green);
            box-shadow: 0 0 10px rgba(0,255,102,0.2);
        }
        .pulse {
            width: 8px;
            height: 8px;
            background-color: var(--neon-green);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--neon-green);
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 15px var(--neon-green); }
            100% { transform: scale(0.95); opacity: 0.8; }
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }
        .card {
            background: var(--panel-bg);
            border: 1px solid rgba(0, 240, 255, 0.15);
            border-radius: 12px;
            padding: 24px;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 3px; height: 100%;
            background: linear-gradient(to bottom, var(--neon-cyan), var(--neon-purple));
        }
        .card h2 {
            font-size: 1.2rem;
            color: var(--neon-cyan);
            margin-bottom: 12px;
            letter-spacing: 1px;
        }
        .description {
            color: var(--text-muted);
            font-size: 0.95rem;
            line-height: 1.5;
            margin-bottom: 16px;
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr auto;
            gap: 10px;
            align-items: end;
            margin-bottom: 15px;
        }
        @media (max-width: 768px) {
            .form-row {
                grid-template-columns: 1fr;
            }
        }
        .input-group label {
            display: block;
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 5px;
        }
        .input-group input {
            width: 100%;
            background: rgba(5, 5, 10, 0.8);
            border: 1px solid rgba(0, 240, 255, 0.3);
            border-radius: 6px;
            padding: 10px;
            color: var(--text-main);
            font-size: 0.95rem;
        }
        .input-group input:focus {
            outline: none;
            border-color: var(--neon-cyan);
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
        }
        .btn {
            background: linear-gradient(135deg, var(--neon-purple), var(--neon-cyan));
            border: none;
            color: #fff;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: opacity 0.2s;
        }
        .btn:hover { opacity: 0.9; }
        .btn-action {
            background: transparent;
            color: var(--neon-cyan);
            border: 1px solid var(--neon-cyan);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.8rem;
            cursor: pointer;
            text-transform: uppercase;
            text-decoration: none;
            display: inline-block;
            margin-right: 8px;
            margin-top: 5px;
        }
        .btn-action:hover {
            background: var(--neon-cyan);
            color: var(--bg-color);
            box-shadow: 0 0 10px var(--neon-cyan);
        }
        .table-container {
            overflow-x: auto;
            margin-top: 15px;
            max-height: 300px;
            overflow-y: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }
        th, td {
            padding: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        th {
            color: var(--neon-cyan);
            font-weight: 600;
        }
        .badge {
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
        }
        .badge-ok { background: rgba(0,255,102,0.15); color: var(--neon-green); border: 1px solid var(--neon-green); }
        .badge-crit { background: rgba(255,0,85,0.15); color: var(--neon-red); border: 1px solid var(--neon-red); }
        footer {
            margin-top: 30px;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.8rem;
            letter-spacing: 1px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Taller ABP - Elaborado por Jose Rafael Correa</h1>
            <div class="status-badge">
                <div class="pulse"></div>
                </div>
        </header>

        <div class="grid">
            <div class="card">
                <h2>Registro de Productos</h2>
                <p class="description">Permite registrar productos, actualizar cantidades y enviar notificaciones al sistema.</p>
                <form id="productForm">
                    <div class="form-row">
                        <div class="input-group">
                            <label>Nombre del Producto</label>
                            <input type="text" id="nombre" required placeholder="Ej. Arroz">
                        </div>
                        <div class="input-group">
                            <label>Stock / Cantidad</label>
                            <input type="number" id="stock" required placeholder="Ej. 10">
                        </div>
                        <div class="input-group">
                            <label>Precio ($)</label>
                            <input type="number" step="0.01" id="precio" required placeholder="Ej. 2500">
                        </div>
                        <button type="submit" class="btn">Guardar</button>
                    </div>
                </form>
            </div>

            <div class="card">
                <h2>Módulo de Inventario</h2>
                <p class="description">Ver los productos registrados y qué cantidad de productos tiene en tiempo real.</p>
                <button class="btn-action" onclick="cargarInventario()">Actualizar Inventario</button>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Producto</th>
                                <th>Cantidad (Stock)</th>
                                <th>Precio</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody id="tablaInventario">
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="card">
                <h2>Sistema Automatizado de Vigilancia (/alertas/stock-bajo)</h2>
                <p class="description">Sistema automatizado de vigilancia de existencias críticas. Retorna los productos cuyo stock se encuentra por debajo del umbral de seguridad (&lt; 5 unidades).</p>
                <button class="btn-action" style="color: var(--neon-red); border-color: var(--neon-red);" onclick="cargarAlertas()">Ver Alertas de Stock Crítico</button>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Producto</th>
                                <th>Cantidad Crítica</th>
                                <th>Precio</th>
                            </tr>
                        </thead>
                        <tbody id="tablaAlertas">
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <footer>
            CONTROL DE INVENTARIOS PARA PEQUEÑOS COMERCIOS // 2026
        </footer>
    </div>

    <script>
        async function cargarInventario() {
            try {
                const res = await fetch('/productos');
                const data = await res.json();
                const tbody = document.getElementById('tablaInventario');
                tbody.innerHTML = '';
                data.forEach(p => {
                    const critico = p.stock < 5;
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>#${p.id}</td>
                        <td>${p.nombre}</td>
                        <td><strong>${p.stock}</strong></td>
                        <td>$${parseFloat(p.precio).toFixed(2)}</td>
                        <td><span class="badge ${critico ? 'badge-crit' : 'badge-ok'}">${critico ? 'CRÍTICO' : 'ÓPTIMO'}</span></td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch (e) {
                console.error(e);
            }
        }

        async function cargarAlertas() {
            try {
                const res = await fetch('/alertas/stock-bajo');
                const data = await res.json();
                const tbody = document.getElementById('tablaAlertas');
                tbody.innerHTML = '';
                data.productos.forEach(p => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>#${p.id}</td>
                        <td>${p.nombre}</td>
                        <td><strong style="color: var(--neon-red);">${p.stock}</strong></td>
                        <td>$${parseFloat(p.precio).toFixed(2)}</td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch (e) {
                console.error(e);
            }
        }

        document.getElementById('productForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const nombre = document.getElementById('nombre').value;
            const stock = document.getElementById('stock').value;
            const precio = document.getElementById('precio').value;

            const res = await fetch('/productos', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({nombre, stock, precio})
            });
            const data = await res.json();
            if (res.ok) {
                alert(data.mensaje);
                document.getElementById('productForm').reset();
                cargarInventario();
                cargarAlertas();
            } else {
                alert('Error: ' + data.error);
            }
        });

        cargarInventario();
        cargarAlertas();
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_FUTURISTA)

@app.route('/productos', methods=['GET'])
def obtener_productos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos')
        rows = cursor.fetchall()
        conn.close()
        productos = [dict(row) for row in rows]
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/productos', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    if not data or not all(k in data for k in ('nombre', 'stock', 'precio')):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400
    
    try:
        nombre = str(data['nombre'])
        stock = int(data['stock'])
        precio = float(data['precio'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Tipos de datos incorrectos'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO productos (nombre, stock, precio) VALUES (?, ?, ?)', (nombre, stock, precio))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': new_id, 'mensaje': 'Producto registrado y notificación enviada exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
        product = cursor.fetchone()
        if not product:
            conn.close()
            return jsonify({'error': 'Producto no encontrado'}), 404

        nombre = data.get('nombre', product['nombre'])
        stock = data.get('stock', product['stock'])
        precio = data.get('precio', product['precio'])

        cursor.execute('UPDATE productos SET nombre = ?, stock = ?, precio = ? WHERE id = ?', (nombre, stock, precio, producto_id))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Producto y cantidades actualizados exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
        product = cursor.fetchone()
        if not product:
            conn.close()
            return jsonify({'error': 'Producto no encontrado'}), 404

        cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Producto eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/alertas/stock-bajo', methods=['GET'])
def alertas_stock_bajo():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE stock < 5')
        rows = cursor.fetchall()
        conn.close()
        productos = [dict(row) for row in rows]
        return jsonify({'alerta': 'Sistema automatizado de vigilancia de existencias críticas', 'productos': productos}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
