#coding=utf-8
def incrementHip():
    import  hou
    import  re
    import  os

    versionpadding = 3
    hipfile = hou.hipFile.name()      #返回文件路径
    hipname = hou.hipFile.basename()  #返回文件名称


    search = re.findall(r'_v(?=\d+)', hipname)#正则匹配字符串 (?=)为分组扩展用法 _v(?=\d+)为后置用法 意思为匹配若_v 后为数字则匹配否则不匹配
                                              # 打个比方 匹配_v001 则不匹_va1这个字符串 \d表示数字 +表示开启贪婪模式 匹配多次+前面的规则



    if len(search) != 0:
       result=re.split(r'_v(?=\d+)', hipname)

       match=re.match("\d+", result[-1])

       newversion= str(int(match.group())+1)

       newfile =os.path.split(hipfile)[0]+"/"+result[0]+ "_v"+newversion.zfill(versionpadding)+".hip"
       if os.path.isfile(newfile) is False:
           hou.hipFile.save(newfile)
       else:
           text = "The file is exist Are you sure overwrite?"
           final= hou.ui.displayMessage(text,
                                 buttons=("yes","cancel"),
                                 severity=hou.severityType.Message,
                                 title="incrementfile"
                                 )
           if final ==0:
               hou.hipFile.save(newfile)

    else:
        raise hou.NameConflict("please use correct namespace")


