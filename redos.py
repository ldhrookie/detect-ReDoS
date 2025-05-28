import re
import sys

def count_spencer_nfa_states(regex: str) -> int: #regex 문자열 입력받는다 그안 리터럴 문자개수, 대략적인 NFA수 +1 반환
    """
    Q(상태) 개수 count NFA 개수 Q를 세는 함수라는 뜻
    """
    position_count = 0
    valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") #특수문자는 없네 아무튼 리터럴 문자 집합

    i = 0
    while i < len(regex):
        c = regex[i]
        if c in valid_chars:
            # literal character → counts as a position
            position_count += 1 #c가 리터럴문자면 상태수 늘리기
        elif c == '\\' and i + 1 < len(regex): #이스케이프문 처리
            # escaped character → counts as a position
            position_count += 1
            i += 1  # skip the escaped character
        # ignore operators like *, |, (, ) 등 메타문자는 상태를 직접만들진 않으므로 무시함.
        i += 1 #다음문자로 이동

    return position_count + 1 #일반적으로 NFA에서 종료상태를 하나 더 갖기때문



def max_backtracking_length(Q, n, a): #Q 상태수 n 입력길이 a반복되는 단위 등
    '''val = (Q,n,a에 관한 식)'''
    return val

def max_memo_length(Q, n, a):
    '''val = (Q,n,a에 관한 식)'''
    return val

#코드 설명: count_spencer_…()—> 상태 수 대강 count
#보다 정확한 녀석은 gpt 보채는 중