import base64
import os
import tempfile
import contextlib
import json
import sys
import time
from io import StringIO

from flask import Flask, render_template, request, jsonify
from CreateGraph.Graph import Graph
from Heap1.Heap import Heap
from Isterler1.Ister1 import Ister1
from Isterler1.Ister3 import AVLTree
from Isterler1.Ister4 import Ister4
from Isterler1.Ister5 import Ister5
from Isterler1.Ister6 import Ister6
from Isterler1.Ister7 import Ister7
from ReadData.data import df


app = Flask(__name__,template_folder='templates')


# Initialize the graph once at the start
queue=[]
orcid_to_author, name_to_author, collaboration_graph = Graph.build_author_graph(df)


@contextlib.contextmanager
def capture_output():
    """Capture print output"""
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
        x, y = Ister6.en_cok_isbirligi_yapan_yazari_bul(collaboration_graph)
        print("{}".format(x.name))
        print("{}".format(y))
    output_text = output.getvalue().strip()
    print(x)
    if not output_text:
        return jsonify({'error': 'Çıktı üretilemedi.'}), 500
    response = app.response_class(
        response=json.dumps({'output': output_text,'orcid': x.orcid}, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/ister2', methods=['POST'])
def ister2():
    start_node_orcid = request.form['start_node']

    with capture_output() as output:
        priority_Queue = []
        if start_node_orcid in orcid_to_author:
            start_node = orcid_to_author[start_node_orcid]
            Heap.heapPush(priority_Queue,len(priority_Queue),(len(start_node.articles),start_node))
            for coauthor, weight in collaboration_graph[start_node].items():
                Heap.heapPush(priority_Queue, len(priority_Queue), (len(coauthor.articles), coauthor))
        else:
            print(f"Start node '{start_node_orcid}' not found in the graph.")
        print("Priority Queue(Artan sıralamalı)")
        while priority_Queue:
            value, yazar = Heap.heapPop(priority_Queue, len(priority_Queue), 0)
            print(f"yazar: {yazar.name}, Makale Sayısı: {value}")
    output_text = output.getvalue().strip()
    if not output_text:
        return jsonify({'error': 'Çıktı üretilemedi.'}), 500
    response = app.response_class( 
        response=json.dumps({'output': output_text,'orcid': start_node_orcid}, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )
    return response



@app.route('/ister3', methods=['POST'])
def ister3():
    global queue, orcid_to_author, name_to_author
    try:
        temp =  queue
        # Debug için queue durumunu yazdır
        print("Queue status:", queue)
        print("Queue length:", len(queue) if queue else 0)
        
        # Queue boş ise initialize et
        if not queue:
            queue = list(orcid_to_author.values())
            print("Queue initialized with:", len(queue), "items")

        start_node = request.form.get('start_node')
        print("Received start_node:", start_node)
        
        if not start_node:
            return jsonify({
                'output': 'Başlangıç düğümü gerekli',
                'success': True  # Frontend true bekliyor
            })

        if start_node not in orcid_to_author:
            available_nodes = list(orcid_to_author.keys())
            print("Available nodes:", available_nodes)
            return jsonify({
                'output': f'Geçersiz başlangıç düğümü. Mevcut düğümler: {available_nodes}',
                'success': True  # Frontend true bekliyor
            })

        # AVLTree işlemleri
        avl_tree = AVLTree()
        author_list = [(i+1, author) for i, author in enumerate(queue)]
        for author in author_list:
            avl_tree.insert(author)

        # Start node'u ağaca uygun formatta sil
        avl_tree.delete( orcid_to_author[start_node])

        # Görselleştirme dosyası oluştur
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_file.close()
        avl_tree.visualize(orcid_to_author,temp_file.name)

        with open(temp_file.name, 'rb') as f:
            img_data = f.read()
        img_base64 = base64.b64encode(img_data).decode('utf-8')

        # Geçici dosyayı temizle
        os.remove(temp_file.name)
        queue = temp 
        return jsonify({
            'output': f'Düğüm {orcid_to_author[start_node].name} başarıyla silindi.',
            'image': img_base64,
            'success': True
        })
    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            'output': 'Bir hata oluştu',
            'success': False
        })

@app.route('/ister4', methods=['POST'])
def ister4():
    global orcid_to_author, name_to_author
    try:
        start_node = request.form.get('start_node')
        print(f"Gelen start_node: {start_node}")

        # Başlangıç node'u geçerli mi kontrol et
        if not start_node or start_node not in orcid_to_author:
            return jsonify({'success': False, 'error': 'Geçersiz start_node'}), 400

        print("Grafik oluşturuluyor...")
        new_graph = Ister4.build_extended_collaboration_graph_by_id(start_node, orcid_to_author,name_to_author, collaboration_graph, depth=2)
        print("Grafik oluşturuldu.")

        output = []
        paths=[[]]
        start=orcid_to_author[start_node]
        for author in new_graph:
            if author == start:
                continue
            path = Ister4.dijkstra(collaboration_graph, start, author)
            if path:
                cost, nodes = path[:2]
                node_names = [node.name for node in nodes]
                paths.append([orcid_to_author[node.orcid].orcid for node in nodes])
                output.append(f" YAZAR {start.name}'dan  YAZAR {author.name} 'a: {' -> '.join(node_names)}  YOL MALİYETİ: {cost}")

        output_text = '\n'.join(output)
        print("Çıktı hazırlandı.")

        return jsonify({
            'success': True,
            'output': output_text,
            'path' : paths
        })

    except KeyError as e:
        error_message = f"KeyError: {str(e)} - ORCID veya grafik yapılandırmasında bir hata var."
        print(error_message)
        return jsonify({'success': False, 'error': error_message}), 500
    except Exception as e:
        error_message = f"Beklenmeyen bir hata oluştu: {str(e)}"
        print(error_message)
        return jsonify({'success': False, 'error': error_message}), 500
@app.route('/ister5', methods=['POST'])
def ister5():
    start_node = request.form.get('start_node')
    name, orcid, count = Ister5.calculate_collaborators_count(collaboration_graph, start_node)

    with capture_output() as output:
        print(f"YAZAR {name} (ORCID: {orcid}) İşbirliği sayısı: {count}")

    output_text = output.getvalue().strip()

    if not output_text:
        return jsonify({'error': 'Çıktı üretilemedi.'}), 500

    output_lines = output_text.splitlines()
    return jsonify({'output': output_lines,'author': orcid}), 200

@app.route('/ister1', methods=['POST'])
def ister1():
    global queue,name_to_author,orcid_to_author
    try:
        start_node = request.form.get('start_node')
        end_node = request.form.get('end_node')

        maliyet, yol, history,queue= Ister1.dijkstra(collaboration_graph,
                                                orcid_to_author[start_node],
                                                orcid_to_author[end_node])
        queue = yol
        output_lines = []
        output_lines.append(f"En kısa yol maliyeti: {maliyet}")
        yol_names = [node.name for node in yol]
        output_lines.append(f"Yol: {' -> '.join(yol_names)}")
        for i, step in enumerate(history, 1):
            output_lines.append(f"\nAdım {i}:")
            for node, data in step.items():
                node_name = node
                path_names = [p.name for p in data['path']]
                output_lines.append(f"{node_name}: Maliyet = {data['cost']}, Yol = {' -> '.join(path_names)}")



        output_text = '\n'.join(output_lines)
        return jsonify({
            'success': True,
            'output': output_text,
            'yol_nesne': [orcid_to_author[node.orcid].orcid for node in yol]  
        })

    except Exception as e:
        print(f"Hata: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/ister7', methods=['POST'])
def ister7():
    global collaboration_graph,orcid_to_author
    try:
        start_time=0
        end_time=0
        start_node = request.form.get('start_node')
        print(start_node)
        with capture_output() as output:
            start_time = time.time()
            current_path = Ister7.dfs_longest_path(collaboration_graph, orcid_to_author[start_node])
            end_time = time.time()
            execution_time = end_time - start_time
            
            path_names = [author.name for author in current_path]  # Convert Author objects to their names
            path = [orcid_to_author[author.orcid].orcid for author in current_path]
            print(f"En uzun yol: {' -> '.join(path_names)}")
            print(f"Yol uzunluğu: {len(current_path)}")

        output_text = output.getvalue().strip()
        execution_time = end_time - start_time
        print(f"\nÇalışma süresi: {execution_time:.2f} saniye")
        return jsonify({
            'success': True,
            'output': output_text if output_text else 'Sonuç bulunamadı',
            'path' : path
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'output': f'Hata oluştu: {str(e)}'
        })

@app.route("/get_graph_data", methods=["GET"])
def get_graph_data():
    print_graph_info()
    nodes = []
    links = []

    for author, collaborators in collaboration_graph.items():
        if not hasattr(author, 'name') or not hasattr(author, 'orcid'):
            print(f"Warning: Author with ORCID {author} has no name or orcid attribute.")
            continue

        try:
            author_label = f"{author.name.split()[0][0]}_{author.name.split()[-1]}_{author.orcid}"
        except IndexError:
            print(f"Error: Unable to process author name {author.name} with ORCID {author.orcid}.")
            continue

        articles_data = []
        for article in author.articles:
            articles_data.append({
                "doi": article.doi,
                "name": article.name,
                "coauthors": list(article.coauthors)
            })

        for collaborator, weight in collaborators.items():
            if not hasattr(collaborator, 'name') or not hasattr(collaborator, 'orcid'):
                print(f"Warning: Collaborator with ORCID {collaborator} has no name or orcid attribute.")
                continue

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
            "articles": articles_data
        })
    return jsonify({"nodes": nodes, "links": links})

@app.route('/print_graph_info', methods=['GET'])
def print_graph_info():
    total_nodes = len(collaboration_graph)
    total_edges = sum(len(neighbors) for neighbors in collaboration_graph.values())

    print(f"Total number of nodes: {total_nodes}")
    print(f"Total number of edges: {total_edges/2}")

    return jsonify({'success': True, 'message': 'Graph info printed to terminal.'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)