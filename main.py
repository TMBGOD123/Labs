from neo4j import GraphDatabase
import PySimpleGUI as sg
import py2neo as p2n

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, text):
        with self.driver.session() as session:
            result = session.read_transaction(self._query, text)
            return result

    @staticmethod
    def _query(tx, text):
        result = tx.run(text)
        return [row["name"] for row in result]
uri = "bolt://localhost:7687"
user = "neo4j"
password = "123"
app = App(uri, user, password)
screens = app.query("MATCH (a:Screen) RETURN a.name AS name")
# graph = p2n.Graph("bolt://localhost:7687", auth=("neo4j", "123"))
# tx = graph.begin()
# matcher = p2n.NodeMatcher(graph)
# a = list(matcher.match("Screen"))
# a = [a[i]["name"] for i in range(len(a))]
# relMatch = p2n.RelationshipMatcher(graph)
# b = relMatch.match(r_type="RELTYPE", nodes="")
layout = [
    [sg.Text('Сценарий поведения:'), sg.Button('Без старой карты'), sg.Button('Со старой картой')],
    [sg.Text('Выбрать экран:')],
    [sg.Listbox(values=screens, size=(35, 3), enable_events=True, key='selected_key')],
    [sg.Text('Элементы интерфейса:')],
    [sg.Listbox(values=["Кнопка", "Текстовое поле"], size=(35, 3), enable_events=True, key='selected_key_el')],
    [sg.Output(size=(88, 20))],
    [sg.Button('Выход')]
]

window = sg.Window('Лаб2_Этап4', layout)
while True:
    event, values = window.read()
    if event == 'Со старой картой':
        path = ['Главный экран']
        while len(app.query(f"MATCH (Screen)-[r:RELTYPE]->(Screens) WHERE Screen.name = '{path[-1]}' RETURN Screens.name AS name;")) > 0:
            path.append(app.query(f"MATCH (Screen)-[r:RELTYPE]->(Screens) WHERE Screen.name = '{path[-1]}' RETURN Screens.name AS name;"))
            path[-1].append(0)
            path[-1] = path[-1][0]
            if path[-1] == "Главный экран":
                break
        b = []
        for i in path:
            if i in screens:
                b.append(i)
        print(' -> '. join(b))
        print('----------------------------------------------------------------------------------------------------')
    elif event == 'Без старой карты':
        path = app.query(f"MATCH path=(Screen)-[r:RELTYPE*1..100]->(Screens) WHERE Screen.name = '{'Главный экран'}' RETURN Screens.name AS name;")
        b = ['Главный экран']
        i = 0
        while len(b) < 8:
            if path[i] in screens and (path[i] != 'Главный экран'):
                b.append(path[i])
            i += 1
        b.append('Главный экран')
        print(' -> '.join(b))
        print('----------------------------------------------------------------------------------------------------')
    elif event == 'selected_key':
        screen = app.query(f"MATCH (a:Screen)-[r:RELTYPE]->(b:Event) WHERE a.name='{values[event][0]}' RETURN b.name AS name")
        print(f'События экрана {values[event][0]}:')
        for i in range(len(screen)):
            print('\t' + screen[i])
        print('----------------------------------------------------------------------------------------------------')
    elif event == 'selected_key_el':
        if values['selected_key_el'][0] == 'Кнопка':
            screen = app.query("MATCH (a:Event) RETURN [a.name, a.discription] AS name")
            for i in screen:
                if 'tap' in i[0]:
                    print(i[0],'-',i[1])
            print('----------------------------------------------------------------------------------------------------')
        elif values['selected_key_el'][0] == 'Текстовое поле':
            screen = app.query("MATCH (a:Event) RETURN [a.name, a.discription] AS name")
            for i in screen:
                if 'input' in i[0]:
                    print(i[0],'-',i[1])
    if event in (None, 'Выход'):
        break

