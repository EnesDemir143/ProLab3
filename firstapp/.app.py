import contextlib
import json
import sys
from io import StringIO

from flask import Flask, render_template, request, jsonify
from Main import dijkstra, dfs_longest_path, en_cok_isbirligi_yapan_yazari_bul, graph, queue, heapPush, priority_Queue, \
    heapPop

app = Flask(__name__, template_folder='templates')


@contextlib.contextmanager
def capture_output():
    """Print çıktılarını yakalayan yardımcı fonksiyon"""
    old_stdout = sys.stdout
    stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old_stdout


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/ister6', methods=['POST'])
def ister6():
    with capture_output() as output:
        x, y = en_cok_isbirligi_yapan_yazari_bul(graph)
        print("En çok iş birliği yapan yazar:{}".format(x))
        print("İş birliği sayısı:{}".format(y))
    output_text = output.getvalue().strip()
    if not output_text:
        return jsonify({'error': 'Çıktı üretilemedi.'}), 500
    # JSON yanıtını manual olarak oluşturuyoruz
    response = app.response_class(
        response=json.dumps({'output': output_text}, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/ister2', methods=['POST'])
def ister2():
    start_node=request.form['start_node']
    with capture_output() as output:
        for q in queue[start_node]:
            heapPush(priority_Queue, len(priority_Queue), (queue[start_node][q], q))
        print(priority_Queue)
        while priority_Queue:
            yazar, value = heapPop(priority_Queue, len(priority_Queue), 0)
            print(f"yazar: {yazar}, value: {value}")
    output_text = output.getvalue().strip()
    if not output_text:
        return jsonify({'error': 'Çıktı üretilemedi.'}), 500
    response = app.response_class(
        response=json.dumps({'output': output_text}, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/ister3', methods=['POST'])
def ister3():
    # 3. ister için gerekli parametreleri alıp işlemleri yapacak
    return jsonify({'success': True})


@app.route('/ister4', methods=['POST'])
def ister4():
    # 4. ister için gerekli parametreleri alıp işlemleri yapacak
    return jsonify({'success': True})


@app.route('/ister5', methods=['POST'])
def ister5():
    # 5. ister için gerekli parametreleri alıp işlemleri yapacak
    return jsonify({'success': True})


@app.route('/ister1', methods=['POST'])
def ister1():
    start_node = request.form.get('start_node')
    end_node = request.form.get('end_node')
    with capture_output() as output:
        maliyet, yol, history = dijkstra(graph, start_node, end_node)
        for i, step in enumerate(history, 1):
            print(f"\nAdım {i}:")
            for node, data in step.items():
                print(f"{node}: Maliyet = {data['cost']}, Yol = {data['path']}")
        print(f"En kısa yol maliyeti: {maliyet}")
        print(f"Yol: {' -> '.join(yol)}")
    output_text = output.getvalue().strip()
    # JSON yanıtını manual olarak oluşturuyoruz
    response = app.response_class(
        response=json.dumps({'output': output_text}, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )
    return response


# app.py
@app.route('/ister7', methods=['POST'])
def ister7():
    try:
        start_node = request.form.get('start_node', 'A')  # Default to 'A' if not provided

        with capture_output() as output:
            current_path = dfs_longest_path(graph, start_node)
            print(f"En uzun yol: {' -> '.join(current_path)}")
            print(f"Yol uzunluğu: {len(current_path)}")

        output_text = output.getvalue().strip()

        return jsonify({
            'success': True,
            'output': output_text if output_text else 'Sonuç bulunamadı'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'output': f'Hata oluştu: {str(e)}'
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)