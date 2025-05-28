from graphviz import Digraph

def visualize_nfa(nfa, filename='nfa'):
    dot = Digraph(comment='NFA')
    visited = set()

    def dfs(state):
        sid = str(id(state))
        if sid in visited:
            return
        visited.add(sid)
        shape = 'doublecircle' if state == nfa.accept else 'circle'
        dot.node(sid, sid[-5:], shape=shape)

        for symbol, dest in state.edges:
            did = str(id(dest))
            label = symbol if symbol is not None else 'ε'
            dot.edge(sid, did, label)
            dfs(dest)

    # 시작 상태 표시 (비실제 상태에서 ε로 시작상태로 연결)
    fake_start_id = 'start'
    dot.node(fake_start_id, '', shape='point')
    dot.edge(fake_start_id, str(id(nfa.start)), 'start')

    dfs(nfa.start)
    dot.render(filename, format='png', cleanup=True)
    print(f"✔️ '{filename}.png' 생성 완료!")
