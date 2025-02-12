import random

def player(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)

    # Strategy1: play the winning move of the opponent's last move
    if prev_play == 'R':
        return 'P'
    elif prev_play == 'P':
        return 'S'
    elif prev_play == 'S':
        return 'R'
    else:
        return random.choice(['R', 'P', 'S'])
    
    # Strategy2: play the winning move of the opponent's most frequent move
    if opponent_history.count('R') > opponent_history.count('P') and opponent_history.count('R') > opponent_history.count('S'):
        return 'P'
    elif opponent_history.count('P') > opponent_history.count('R') and opponent_history.count('P') > opponent_history.count('S'):
        return 'S'
    elif opponent_history.count('S') > opponent_history.count('R') and opponent_history.count('S') > opponent_history.count('P'):
        return 'R'
    else:
        return random.choice(['R', 'P', 'S'])

    # Strategy3: play the winning move through markov chain
    r2r_count = opponent_history.count('RR')
    r2p_count = opponent_history.count('RP')
    r2s_count = opponent_history.count('RS')

    p2p_count = opponent_history.count('PP')
    p2r_count = opponent_history.count('PR')
    p2s_count = opponent_history.count('PS')

    s2s_count = opponent_history.count('SS')
    s2r_count = opponent_history.count('SR')
    s2p_count = opponent_history.count('SP')

    if prev_play == 'R':
        if r2r_count > r2p_count and r2r_count > r2s_count:
            return 'R'
        elif r2p_count > r2r_count and r2p_count > r2s_count:
            return 'P'
        elif r2s_count > r2r_count and r2s_count > r2p_count:
            return 'S'
        else:
            return random.choice(['R', 'P', 'S'])
        
    elif prev_play == 'P':
        if p2p_count > p2r_count and p2p_count > p2s_count:
            return 'P'
        elif p2r_count > p2p_count and p2r_count > p2s_count:
            return 'R'
        elif p2s_count > p2p_count and p2s_count > p2r_count:
            return 'S'
        else:
            return random.choice(['R', 'P', 'S'])
        
    elif prev_play == 'S':
        if s2s_count > s2r_count and s2s_count > s2p_count:
            return 'S'
        elif s2r_count > s2s_count and s2r_count > s2p_count:
            return 'R'
        elif s2p_count > s2s_count and s2p_count > s2r_count:
            return 'P'
        else:
            return random.choice(['R', 'P', 'S'])
        
    else:
        return random.choice(['R', 'P', 'S'])