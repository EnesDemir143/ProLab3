import contextlib
import json
import sys
from io import StringIO

from CreateGraph.Graph import Graph
from Heap1.Heap import Heap
from Isterler1.Ister1 import Ister1
from Isterler1.Ister6 import Ister6
from Isterler1.Ister7 import  Ister7
from flask import Flask, render_template, request, jsonify

from ReadData.data import df

# from ExFiles.Main import dijkstra, dfs_longest_path, en_cok_isbirligi_yapan_yazari_bul, graph, heapPush, priority_Queue, \
#     heapPop, collaboration_graph



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
        x, y = Ister6.en_cok_isbirligi_yapan_yazari_bul(Graph.collaboration_graph)
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
        priority_Queue=[]
        for q in Graph.collaboration_graph[start_node]:
            Heap.heapPush(priority_Queue, len(priority_Queue), (Graph.collaboration_graph[start_node][q], q))
        print(priority_Queue)
        while priority_Queue:
            yazar, value = Heap.heapPop(priority_Queue, len(priority_Queue), 0)
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
        maliyet, yol, history = Ister1.dijkstra(Graph.collaboration_graph, start_node, end_node)
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
        start_node = request.form.get('start_node')  # Default to 'A' if not provided

        with capture_output() as output:
            current_path = Ister7.dfs_longest_path(Graph.collaboration_graph, start_node)
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

@app.route("/get_graph_data", methods=["GET"])
def get_graph_data():
    orcid_to_author, name_to_author, collaboration_graph = Graph.build_author_graph(df)

    # collaboration_graph sınıf düzeyinde bir değişken olarak saklanıyor
    Graph.collaboration_graph = collaboration_graph
    nodes = []
    links = []

    for author, collaborators in Graph.collaboration_graph.items():
        # Yazar adını kontrol edin
        if not author.name:
            print(f"Warning: Author with ORCID {author.orcid} has no name.")
            continue  # Bu yazarı atlayabilirsiniz

        try:
            # Ad soyad formatını oluştur
            author_label = f"{author.name.split()[0][0]}_{author.name.split()[-1]}_{author.orcid}"
        except IndexError:
            print(f"Error: Unable to process author name {author.name} with ORCID {author.orcid}.")
            continue  # Hatalı yazarı atla

        # Author'ın makalelerini JSON uyumlu hale getirmek
        articles_data = []
        for article in author.articles:
            articles_data.append({
                "doi": article.doi,
                "name": article.name,
                "coauthors": list(article.coauthors)  # set'i listeye dönüştürüyoruz
            })

        for collaborator, weight in collaborators.items():
            try:
                collab_label = f"{collaborator.name.split()[0][0]}_{collaborator.name.split()[-1]}_{collaborator.orcid}"
                links.append({"source": author_label, "target": collab_label, "weight": weight})
            except IndexError:
                print(f"Error: Unable to process collaborator {collaborator.name} with ORCID {collaborator.orcid}.")
                continue

        nodes.append({
            "id": author_label,
            "full_name": author.name,
            "orcid": author.orcid,
            "articles": articles_data  # Makale verilerini burada ekliyoruz
        })

    return jsonify({"nodes": nodes, "links": links})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)