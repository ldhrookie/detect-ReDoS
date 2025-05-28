import time

class State:
    def __init__(self, is_accept=False):
        self.transitions = {}
        self.is_accept = is_accept

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)

def build_nfa_a_plus_plus():
    start = State()
    s1 = State()
    s2 = State()
    accept = State(is_accept=True)

    start.add_transition('', s1)
    s1.add_transition('a', s1)
    s1.add_transition('', s2)
    s2.add_transition('', s1)
    s2.add_transition('', accept)

    return start, accept

def match_nfa(state, accept_state, string, pos=0):
    if pos == len(string) and state.is_accept:
        return True

    results = []

    if '' in state.transitions:
        for next_state in state.transitions['']:
            results.append(match_nfa(next_state, accept_state, string, pos))

    if pos < len(string) and string[pos] in state.transitions:
        for next_state in state.transitions[string[pos]]:
            results.append(match_nfa(next_state, accept_state, string, pos + 1))

    return any(results)

def match_nfa_memo_safe(state, accept_state, string, pos=0, memo=None, visited=None):
    if memo is None:
        memo = {}
    if visited is None:
        visited = set()

    key = (id(state), pos)
    if key in memo:
        return memo[key]
    if key in visited:
        return False

    visited.add(key)

    if pos == len(string) and state.is_accept:
        memo[key] = True
        return True

    results = []

    if '' in state.transitions:
        for next_state in state.transitions['']:
            results.append(match_nfa_memo_safe(next_state, accept_state, string, pos, memo, visited.copy()))

    if pos < len(string) and string[pos] in state.transitions:
        for next_state in state.transitions[string[pos]]:
            results.append(match_nfa_memo_safe(next_state, accept_state, string, pos + 1, memo, visited.copy()))

    memo[key] = any(results)
    return memo[key]

# 실험 입력
input_str = "a" * 20

# Naive NFA 실행
start, accept = build_nfa_a_plus_plus()
start_time = time.time()
try:
    result_naive = match_nfa(start, accept, input_str)
except RecursionError:
    result_naive = "RecursionError"
time_naive = time.time() - start_time

# Memoized NFA 실행
start, accept = build_nfa_a_plus_plus()
start_time = time.time()
try:
    result_memo = match_nfa_memo_safe(start, accept, input_str)
except RecursionError:
    result_memo = "RecursionError"
time_memo = time.time() - start_time

# 결과 출력
print("=== NFA Matcher Comparison ===")
print(f"Naive NFA Result:     {result_naive}, Time: {time_naive:.6f}s")
print(f"Memoized NFA Result:  {result_memo}, Time: {time_memo:.6f}s")
