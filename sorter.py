def avg_pos(triangle):
    avg=triangle[0][2]+triangle[1][2]+triangle[2][2]
    avg/=3
    return avg

def sort_triangles(model):
    model.sort(reverse=True,key=avg_pos)
    return model

