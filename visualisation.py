from readfile import read_net_file
from matrix import matrixQ, matrixR
import tkinter as tk
from tkinter import filedialog
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from algorithm import arrangeAlgorithm

matplotlib.use('TkAgg')

class AlgorithmInputWindow:
    def __init__(self, tik, file_path):
        self.file_path = file_path
        self.tik = tik
        self.root = tk.Tk()
        self.root.geometry(f"{str(300)}x{str(300)}")
        self.root.title("Введите значения k и v")

        # Создаем Entry для k
        self.label_k = tk.Label(self.root, text="Введите значение k:")
        self.entry_k = tk.Entry(self.root)
        self.label_k.pack()
        self.entry_k.pack()

        # Создаем Entry для v
        self.label_v = tk.Label(self.root, text="Введите значение v:")
        self.entry_v = tk.Entry(self.root)
        self.label_v.pack()
        self.entry_v.pack()

        # Создаем кнопку для подтверждения
        self.button_confirm = tk.Button(self.root, text="Подтвердить", command=self.confirm_values)
        self.button_confirm.pack()

    def confirm_values(self):
        # Получаем значения из Entry и сохраняем в переменные k и v
        k_value = self.entry_k.get()
        v_value = self.entry_v.get()

        # Преобразуем значения в нужный формат (int, float, etc.), при необходимости
        # Пример преобразования в int:
        try:
            k_value = int(k_value)
            v_value = int(v_value)
        except ValueError:
            # Обработка ошибки при невозможности преобразования
            print("Ошибка: Введите целочисленные значения для k и v.")
            return

        # Сохраняем значения в переменные класса, которые могут быть использованы в других частях программы
        self.k = k_value
        self.v = v_value
        
        self.tik.drawAdditionalGraph(self.k, self.v, self.file_path)
        
        # Закрываем окно
        self.root.destroy()
        



        
    
class Interface:
    def __init__(self):
        self.root = tk.Tk()
        
    def drawInterface(self, title, length, width):
        self.root.title(title)
        self.root.geometry(f"{str(length)}x{str(width)}")

        self.frame_q = tk.Frame(self.root, bd=5, relief="ridge")
        self.frame_q.place(relx=0.05, rely=0.15, relwidth=0.4, relheight=0.45)

        self.frame_r = tk.Frame(self.root, bd=5, relief="ridge")
        self.frame_r.place(relx=0.55, rely=0.15, relwidth=0.4, relheight=0.45)

        self.text_bottom = tk.Text(self.root, bd=5, relief="ridge")
        self.text_bottom.place(relx=0.2, rely=0.65, relwidth=0.6, relheight=0.3)
        self.scrollbarText = tk.Scrollbar(self.text_bottom, orient='vertical')
        self.scrollbarText.pack(side='right', fill='y')
        self.scrollbarText.config(command=self.text_bottom.yview)


        self.button_update = tk.Button(self.root, text="Построить матрицы", command=self.update_matrices)
        self.button_update.pack(side='top', padx=10, pady=10)
        self.button_update = tk.Button(self.root, text="Сбросить матрицы", command=self.reset_matrices)
        self.button_update.pack(side='top', padx=10, pady=10)
        self.button_algorithm = tk.Button(self.root, text="Алгоритм компоновки", command=self.showInput)
        self.button_algorithm.pack(side='top', padx=10, pady=10)

        self.root.mainloop()
        
    def draw_graph(self, nodes, elements, nets_data):
        plt.clf()  
    
        G = nx.MultiGraph()
    
        G.add_nodes_from(elements)
        G.add_nodes_from(nodes)

        for element, connected_nodes in nets_data.items():
            for node, data in connected_nodes.items():
                pin = data['pin']
            
                G.add_edge(element, node, pin=pin)

        pos_elements = {element: (i, 0) for i, element in enumerate(elements)}
        pos_nodes = {node: (i, -1) for i, node in enumerate(nodes)}
        pos = {**pos_elements, **pos_nodes}

        nx.draw_networkx_nodes(G, pos, nodelist=elements, node_size=600, node_color='skyblue')
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_size=600, node_color='lightcoral')

        edges = [(element, node, {'pin': data['pin']}) for element, connected_nodes in nets_data.items() for node, data in connected_nodes.items()]
        nx.draw_networkx_edges(G, pos, edgelist=edges)

        labels = {element: element for element in elements}
        labels.update({node: node for node in nodes})
        nx.draw_networkx_labels(G, pos, labels, font_size=6)

        edge_labels = {(element, node): data['pin'] for element, connected_nodes in nets_data.items() for node, data in connected_nodes.items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.axis('off')
        plt.show()
    def showInput(self):
        file_path = filedialog.askopenfilename(title="Выберите файл списка соединений", filetypes=[("NET files", "*.NET")])
        if file_path:
            # Пример использования
            input_window = AlgorithmInputWindow(self, file_path)
            input_window.root.mainloop()
           
        
    def drawAdditionalGraph(self, k, v, file_path):
        self.file_path = file_path
        self.k = k
        self.v = v

        if self.file_path:
            nets_data, nodes, elements, data = read_net_file(self.file_path)
            matrix_q = matrixQ(nets_data, elements, nodes)
            matrix_r = matrixR(matrix_q, elements)
            alOut = arrangeAlgorithm(matrix_q, matrix_r, elements, self.k, self.v, newNodes={}, currentNode=0)
            print(alOut)
            # Создаем граф
            G = nx.Graph()

            # Добавляем связи между элементами
            for i in range(1, len(matrix_q)):
                for j in range(1, len(matrix_q[i])):
                    if matrix_q[i][j] == 1:
                        element1 = matrix_q[i][0]
                        element2 = matrix_q[0][j]
                        G.add_edge(element1, element2)

            # Распределяем узлы
            pos = nx.spring_layout(G, seed=42)

            # Создаем словарь, сопоставляющий уникальные цвета каждой партии
            color_map = {}
            for i, (party, nodes) in enumerate(alOut.items()):
                color_map.update({node: f'C{i}' for node in nodes})

            # Определяем цвет для узлов, не входящих в партии
            default_color = 'blue'

            # Создаем списки цветов для узлов и элементов
            node_colors = [color_map.get(node, default_color) for node in G.nodes]
            edge_colors = [color_map.get(edge[0], default_color) for edge in G.edges]

            # Рисуем граф
            nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color=node_colors, edge_color=edge_colors)

            # Добавляем названия элементов
            labels = {element: element for element in G.nodes}
            nx.draw_networkx_labels(G, pos, labels)

            plt.show()
            
    
    def update_matrices(self):
        file_path = filedialog.askopenfilename(title="Выберите файл списка соединений", filetypes=[("NET files", "*.NET")])
        if file_path:
            nets_data, nodes, elements, data = read_net_file(file_path)
            matrix_q = matrixQ(nets_data, elements, nodes)
            matrix_r = matrixR(matrix_q, elements)
                
            self.text_bottom.insert(tk.END, data)
            for i in range(len(matrix_q)):
                for j in range(len(matrix_q[0])):
                    label_q = tk.Label(self.frame_q, text=str(matrix_q[i][j]))
                    label_q.grid(row=i, column=j, padx=2, pady=2)

            for i in range(len(matrix_r)):
                for j in range(len(matrix_r[0])):
                    label_r = tk.Label(self.frame_r, text=str(matrix_r[i][j]))
                    label_r.grid(row=i, column=j, padx=2, pady=2)
    
        self.draw_graph(nodes, elements, nets_data)

    def reset_matrices(self):
        for widget in self.frame_q.winfo_children():
            widget.destroy()

        for widget in self.frame_r.winfo_children():
            widget.destroy()
        self.text_bottom.delete('1.0', tk.END)