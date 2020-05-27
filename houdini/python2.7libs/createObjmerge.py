def createNode():
    import  hou
    import  os

    node = hou.selectedNodes()[0]

    if node is None:
        return None

    path = node.path()

    nodePath = "/".join(path.split("/")[:-1])
    nodeName = "input_" + path.split("/")[-1]

    objMerge = hou.node(nodePath).createNode("object_merge")

    objMerge.parm("xformpath").set(path)

    objMerge.setName(nodeName)

    objMerge.setColor(hou.Color(1, 0, 0))