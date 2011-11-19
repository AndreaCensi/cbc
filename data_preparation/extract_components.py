from procgraph import simple_block, COMPULSORY


@simple_block
def extract_component(rgb, i=COMPULSORY):
    return rgb[:,:,i].squeeze()


@simple_block
def select_component(rgb, i=COMPULSORY):
    rgb2 = rgb.copy()
    for j in range(3):
        if i != j:
            rgb[:,:,j] = 0
    return rgb2

    