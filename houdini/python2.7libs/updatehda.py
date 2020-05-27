#coding=utf-8


def updateHda():
    import hou
    node = hou.selectedNodes()[0]
    if node is None:
        return None
    nodetyp=node.type().definition()
    if nodetyp is None:
        return None

    file_path =nodetyp.libraryFilePath()
    if file_path == "Embedded" :
        return  None

    namespace0,namespace1,name,version =  node.type().nameComponents()
    major = float(version)+1.0
    minor = float(version)+0.1

    major_ver = "update to {}".format(major)
    minor_ver = "update to {}".format(minor)

    if version != "":
        if not node.matchesCurrentDefinition():

            selected_Item=hou.ui.displayMessage("please select version to update",buttons=(major_ver,minor_ver,"cancel"))

            if selected_Item == 0 :

                nodetyp.setVersion(str(major))
                new_name = "{}::{}::{}".format(namespace1,name,major)
                nodetyp.copyToHDAFile(file_path,new_name=new_name)
                node.changeNodeType(new_name,
                                    keep_name=True,
                                    keep_parms=True,
                                    keep_network_contents = True,
                                    )

            if selected_Item == 1:

                nodetyp.setVersion(str(minor))
                new_name = "{}::{}::{}".format(namespace1,name,minor)
                nodetyp.copyToHDAFile(file_path,new_name=new_name)
                node.changeNodeType(new_name,
                                    keep_name=True,
                                    keep_parms=True,
                                    keep_network_contents=True,

                                    )

            if selected_Item == 2:
                return None
        else:
            raise(hou.Error("please unlock the asset"))
    else:
        raise(hou.Error("hda namespace is wrong"))


def savehda():
    import hou

    node = hou.selectedNodes()[0]
    node.type().definition().updateFromNode(node)
    node.matchCurrentDefinition()
