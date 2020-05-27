def merge():
    import hou
    node = hou.selectedNodes()[0]
    if node is None:
        return None
    nodes = hou.selectedNodes()

    path = node.path()

    nodePath = "/".join(path.split("/")[:-1])

    merge = hou.node(nodePath).createNode("merge")

    for input_index, conectors in enumerate(nodes):
        merge.setInput(input_index, conectors)


    merge.moveToGoodPosition()
    merge.setGenericFlag(hou.nodeFlag.Display, 1)
    merge.setGenericFlag(hou.nodeFlag.Render, 1)

    merge.setColor(hou.Color(0.5, 0, 0.5))