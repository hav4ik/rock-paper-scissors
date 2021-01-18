def agent(obs, conf):
    move_list = [2, 1, 2, 2, 1, 1, 1, 2, 0, 2, 2, 2, 0, 2, 2, 1, 2, 2, 2, 0, 0, 1, 2, 0, 0, 1,2, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 0, 2, 0, 0, 2, 2, 1,1, 0, 1, 0, 2, 0, 2, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 2, 0, 0, 1, 2, 2, 2, 0, 2, 1, 1, 0, 1, 0, 0, 1, 1, 2, 0, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 1, 2, 0, 2, 0, 0, 2, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 2, 1, 0, 0, 1, 0, 0, 2, 0, 1, 1, 2, 0, 2, 1, 1, 1, 1, 2, 2, 0, 0, 1, 0, 1, 2, 0, 2, 2, 1, 0, 1, 2, 0, 2, 2, 0, 2, 1, 1, 0, 1, 1, 1, 0, 0, 2, 1, 1, 0, 0, 2, 2, 0, 2, 0, 1, 2, 1, 1, 2, 2, 1, 2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 0, 0, 2, 2, 0, 1, 2, 0, 0, 2, 2, 0, 0, 2, 0, 2, 0, 0, 0, 1, 0, 2, 2, 1, 2, 1, 1, 2, 0, 2, 2, 1, 0, 1, 0, 0, 2, 0, 2, 0, 1, 0, 0, 0, 0, 0, 2, 1, 1, 1, 2, 2, 0, 0, 0, 2, 2, 0, 1, 2, 1, 0, 0, 2, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 2, 1, 2, 0, 1, 2, 1, 1, 0, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 1, 0, 1, 0, 1, 0, 0, 2, 0, 1, 0, 0, 2, 2, 1, 1, 2, 1, 2, 2, 2, 0, 0, 2, 0, 2, 0, 1, 0, 2, 1, 0, 2, 1, 2, 0, 1, 2, 0, 1, 1, 1, 0, 0, 1, 0, 0, 2, 1, 2, 0, 1, 0, 2, 2, 1, 0, 2, 2, 2, 2, 0, 1, 2, 2, 1, 0, 0, 0, 2, 2, 0, 0, 1, 1, 1, 0, 1, 2, 0, 2, 2, 2, 2, 0, 0, 0, 1, 2, 2, 0, 2, 1, 2,1, 2, 2, 0, 0, 1, 2, 2, 0, 0, 0, 0, 2, 2, 0, 1, 0, 1, 2, 1, 2, 2, 2, 0, 2, 0,2, 1, 0, 2, 0, 0, 1, 2, 0, 0, 1, 2, 1, 0, 2, 1, 2, 1, 0, 1, 2, 2, 0, 1, 2, 1,0, 0, 2, 2, 1, 0, 2, 0, 0, 2, 0, 2, 1, 1, 2, 0, 1, 0, 2, 1, 0, 1, 1, 1, 2, 2,1, 2, 2, 0, 0, 0, 2, 1, 0, 0, 1, 0, 1, 0, 0, 2, 0, 0, 1, 2, 2, 2, 1, 0, 0, 0,0, 1, 0, 0, 2, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 0, 0, 1, 0, 0,2, 2, 0, 0, 2, 0, 2, 0, 1, 2, 0, 0, 2, 1, 0, 0, 2, 2, 2, 1, 0, 1, 1, 2, 0, 1,1, 1, 1, 0, 2, 2, 1, 1, 1, 0, 0, 2, 0, 1, 0, 0, 0, 2, 1, 1, 2, 1, 0, 1, 2, 2,1, 0, 0, 0, 0, 1, 1, 2, 1, 2, 0, 1, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 2, 2, 1, 1,1, 1, 0, 2, 0, 0, 2, 0, 1, 1, 1, 2, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 1, 1, 2, 2, 0, 1, 0, 2, 1, 2, 2, 2, 1, 0, 1, 2, 0, 0, 0, 0, 1, 2, 0, 2, 2, 1, 0, 0, 1, 0, 0, 1, 0, 2, 0, 2, 0, 2, 0, 1, 1, 0, 2, 0, 2, 0, 0, 1, 1, 2, 2, 1, 0, 0, 2, 2, 1, 2, 0, 1, 2, 0, 2, 0, 1, 2, 0, 1, 2, 2, 0, 1, 0, 1, 2, 1, 2, 0, 0, 2, 0, 2, 0, 2, 1, 1, 1, 0, 1, 2, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 2, 2, 2, 1, 1, 0, 2, 0,2, 2, 2, 2, 1, 1, 0, 1, 1, 0, 1, 0, 2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 0, 0, 1, 1, 2, 1, 2, 1, 0, 0, 2, 0, 2, 2, 2, 0, 2, 1, 1, 1, 1, 2, 2, 1, 2, 0, 1, 2, 2, 2, 2, 1, 0, 1, 2, 1, 2, 0, 2, 0, 1, 2, 0, 0, 1, 0, 0, 0, 0, 1, 2, 2, 2, 0, 2, 0, 1, 1, 0, 2, 2, 2, 1, 0, 2, 0, 1, 1, 1, 2, 2, 0, 0,1, 2, 2, 1, 0, 1, 0, 0, 0, 2, 2, 1, 0, 0, 1, 2, 2, 2, 0, 2, 1, 1, 2, 2, 1, 0, 0, 2, 2, 0, 0, 1, 0, 1, 0, 2, 2, 2, 2, 0, 1, 2, 0, 0, 1, 0, 0, 2, 2, 2, 0, 0, 1, 1, 1, 1, 0, 2, 1, 0, 2, 1, 0, 1, 1, 1, 2, 1, 0, 0, 1, 0, 2, 1, 0, 0, 1, 2, 0, 2, 1, 1, 2, 2, 1, 0, 1, 1, 0, 2, 2, 1, 1, 0, 2, 2, 0, 2, 1, 0, 1, 1, 0, 2, 0, 2, 1, 2, 0, 0, 2, 2, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 2, 1, 0, 1, 2, 1, 2, 0, 2, 2, 0, 0, 2, 2, 0, 1, 2, 1, 1, 0, 0, 2, 2, 2, 0, 1, 0, 0, 2, 1, 0,0, 0, 2, 2, 2, 0, 0, 1, 0, 1, 1, 2, 1, 2, 1]
    
    return move_list[obs['step']]
