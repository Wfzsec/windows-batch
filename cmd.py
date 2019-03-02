# -*-coding:UTF-8-*-
import sys
import os
import re

'''
IF || FOR || WHILE || SET || SHIFT || ECHO || GOTO:

'''

can_shu = []
echo_swith = 0
def batch_computer(filename):
    filename = filename
    global can_shu
    #print "filename:",filename
    shell_list = open(filename,"r")
    shell_list = shell_list.readlines()
    for i in range(shell_list.__len__()):
        shell_list[i] = shell_list[i].strip('\n')
    #print "shell_list:",shell_list
    i=0
    while(i<=shell_list.__len__()-1):
    #for i in range(shell_list.__len__()):
            #遇到标签跳转
            global echo_swith
            if echo_swith == 1:
                path = os.path.dirname(os.path.abspath('__file__'))
                sys.stdout.write(path)
                sys.stdout.write(">")
                sys.stdout.write(shell_list[i])
                sys.stdout.write("\n")
            match = re.search("^:",shell_list[i],re.I)
            if match:
                if i + 2 > shell_list.__len__()-1:
                    return 0
                else:
                    i = i + 2
#                    print shell_list[i]
                    continue

            #遇到shift指令
            match = re.search("shift", shell_list[i], re.I)
            if match:
                can_shu =_shift_(shell_list[i],shell_list)
                i = i + 1
                #print can_shu
                continue

            match = re.search(".*if.*",shell_list[i],re.I)
            #print "can_shu:",can_shu
            if match:
                _if_(shell_list[i],shell_list)
                i = i + 1
                continue

            match = re.match("^SET.*",shell_list[i],re.I)
            if match:
                _set_(match.group(),shell_list)
                i = i + 1
                continue

            match = re.match("^echo.*",shell_list[i],re.I)
            if match:
                _echo_(match.group(),shell_list)
                i = i+1
                continue

            match = re.search(r"^for.*",shell_list[i],re.I)
            if match:
                _for_(shell_list[i],shell_list)
                i = i + 1
                continue

            match = re.search("^while.*",shell_list[i],re.I)
            if match:
                _while_(shell_list[i],shell_list)
                i = i + 1
                continue

            print "\"" + shell_list[i] + "\"" + "不是内部或外部命令，也不是可运行的文件或批处理文件"
            break

def match_dos(shell,shell_list):
    i = shell
    shell_list = shell_list
    global can_shu

    match = re.search("shift",i,re.I)
    if match:
        can_shu =_shift_(i,shell_list)
        #print can_shu
        return 0

    match = re.match(".*SET.*",i,re.I)
    if match:
        _set_(match.group(),shell_list)
        return 0

    match = re.match(".*echo.*",i,re.I)
    if match:
        _echo_(match.group(),shell_list)
        return 0

    match = re.search(r"goto",i,re.I)
    if match:
        _goto_(i,shell_list)

        return 0
    print  i + "不是内部或外部命令"
    _shou_hu()

def _set_(shell,shell_list):
    try:
        shell= re.sub(" ","",shell)
        vary = re.match(r"set(.*)=(.*)",shell,re.I)
        bian_liang = vary.group(1)
        bian_liang = re.sub(" ","",bian_liang)
        #print bian_liang
        bian_liang_zhi =  vary.group(2)
        bian_liang_zhi = re.sub(" ","",bian_liang_zhi)
        #print bian_liang_zhi
        os.environ[bian_liang] = bian_liang_zhi
        print "set",bian_liang,"=",bian_liang_zhi
        #print os.environ
    except:
        print  "第"+ding_wei(shell,shell_list)+"条命令错误"\
                "set命令格式错误   eg:set expr = expr"
        _shou_hu()

def _echo_(shell,shell_list):
    shell =  shell
    match = re.search("echo on",shell,re.I)
    global echo_swith
    if match:
        echo_swith = 1
        return 0
    match = re.search("echo off",shell,re.I)
    if match:
        echo_swith = 0
        return 0
    try:
        for i in range(shell.__len__()): #写入文件
            #print i
            #print type(shell)
            if((shell[i] == ">") and (shell[i+1]!=">")) :
                shell = re.sub(" ","***",shell)
                shell = re.match("echo\*\*\*(\w*\D*)>(.*)",shell,re.I)
                #print shell
                ming_ling = shell.group(1)
                ming_ling = re.sub("\*\*\*"," ",ming_ling)
                #print ming_ling
                ming_ling_res = os.popen(ming_ling)
                ming_ling_res = ming_ling_res.read().decode('gbk').encode('utf-8')
                #print ming_ling_res
                wen_jian = shell.group(2)
                wen_jian = re.sub("\*\*\*","",wen_jian)
                file = open(wen_jian,"w")
                file.write(ming_ling_res)
                return 0

            if(shell[i] == ">") and (shell[i+1]== ">"):
                shell = re.sub(" ","***",shell)
                shell = re.match("echo\*\*\*(\w*\D*)>>(.*)",shell,re.I)
                #print shell
                ming_ling = shell.group(1)
                ming_ling = re.sub("\*\*\*"," ",ming_ling)
                #print ming_ling
                ming_ling_res = os.popen(ming_ling)
                ming_ling_res = ming_ling_res.read().decode('gbk').encode('utf-8')
                #print ming_ling_res
                wen_jian = shell.group(2)
                wen_jian = re.sub("\*\*\*","",wen_jian)
                file = open(wen_jian,"w+")
                file.write(ming_ling_res)
                return 0

        str = re.match("echo\s{1}\"{1}(.*)\"{1}",shell,re.I)
        if str:
            str = str.group(1)
            print str
            return 0

        str = re.match("echo\s{1}(.*)", shell, re.I)
        if str:
            str = str.group(1)
            print str
            return 0
    except:
        print  "第" + ding_wei(shell, shell_list) + "条命令错误"
        print "echo命令使用错误  命令格式："
        print "echo shell > filename"
        print "echo shell >> filename"
        print "echo string > filename"
        print "echo string >> filename"
        _shou_hu()

def _if_(i,shell_list):
    i = i
    shell_list = shell_list
    #print  "i:",i
    #if exist
    try:
        match = re.search("exist",i,re.I)
        if match:
            match_not = re.search("not",i,re.I)
            if match_not:
                command = re.search("exist\s+([^\s]*)\s{1}(.*)",i,re.I)
                file_name =  command.group(1)
                #print "file_name:",file_name
                ming_ling = command.group(2)
                #print "ming_ling:",ming_ling
                if os.path.exists(file_name):
               #     print  ming_ling
                     match_dos(ming_ling,shell_list)
                    #print "*******************************************"
            else:
                command = re.search("exist\s+([^\s]*)\s{1}(.*)", i, re.I)
                file_name = command.group(1)
                #print "file_name:", file_name
                ming_ling = command.group(2)
                #print "ming_ling:", ming_ling
                if os.path.exists(file_name):
                    #print  ming_ling
                    match_dos(ming_ling,shell_list)
                 #   print "*******************************************"
        #if expr == expr

        match = re.search("==",i,re.I)
        if match:
            left = re.search("\s+([a-z,1-9,\",\',%]+)\s*==",i,re.I)
            left = left.group(1)
            #print "left:",left
            if left[1] == "%":
                #print left[2:-1]
                left = "\""+can_shu[int(left[2:-1])-1]+"\""
               # print "left:",left

            right = re.search("==\s*([a-z,1-9,\",\',%]+)",i,re.I)
            right = right.group(1)
           # print "right",right
            if right[1] == "%":
                right = "\""+can_shu[int(right[2:-1])-1]+"\""
              #  print "rirht:",right
            if left == right:
                command = re.search(r"==\s{1}[^\s]*\s{1}(.*)", i, re.I)
                # print "command:",command.group(1)
                command = command.group(1)
                match_dos(command, shell_list)
            #    print "*******************************************"
            if left!=right:
                return 0
    except:
        print "if命令格式错误 格式如下："
        print "IF [NOT] string1==string2 command"
        print "IF [NOT] EXIST filename command"
        _shou_hu()

def _shift_(i,shell_list):
    global can_shu
    try:
        i = i
        new_can_shu = []
        pian_yi = re.search("/(\d)", i, re.I)
        pian_yi = int(pian_yi.group(1))
        print "*******************************************"
        print "old_can_shu =>",can_shu
        for i in range(pian_yi - 1, can_shu.__len__()):
            new_can_shu.append(can_shu[i])
        print "new_can_shu => ",new_can_shu
        print "*******************************************"
        return new_can_shu
    except:
        print  "第" + ding_wei(i, shell_list) + "条命令错误\n"
        print "shift命令格式错误 格式如下："
        print "SHIFT [/n]"
        _shou_hu()

def _goto_(i,shell_list):
    i = i
    try:
        shell_list = shell_list
        match = re.search(r"goto\s+([a-z,1-9,\",\']*)",i,re.I) #匹配goto 标签
       # print "biao_qian:",match.group(1)
        biao_qian = match.group(1) #获得goto标签
        for i  in range(shell_list.__len__()): #在批处理文件中找到标签
            if ":"+ biao_qian == shell_list[i]:
                match_dos(shell_list[i+1],shell_list) #执行标签所代表的命令
                break
    except:
        print  "第" + ding_wei(i, shell_list) + "条命令错误\n" #如果执行出错 报错
        print "shift命令格式错误 格式如下："
        print "GOTO label\ "
        print "label   指定批处理程序中用作标签的文字字符串。"
        _shou_hu()
def _for_(shell,shell_list):
    shell = shell
    try:
        match = re.search("/D|/d",shell,re.I)
        if match:
            set = re.search("\((.*)\)",shell,re.I)
            set = set.group(1)
            old_dir = os.getcwd()
            dir = os.chdir(set)
            dir = os.getcwd()
            dir = str(dir)
          #  print "dir:",dir
            a = os.listdir(dir)
            dirs = []
            p = set
            for i in a:
          #      print p+i.decode('gbk').encode('utf-8')
                if os.path.isdir(p+i):
                    i = i.decode('gbk').encode('utf-8')
                    dirs.append(i)
            set = dirs
            set_count = dirs.__len__()
            command = re.search("DO\s{1}(.*)",shell,re.I)
            command = command.group(1)
            for i in range(set_count):
                ti_huan = re.sub("%%.*","\""+set[i]+"\"",command)
          #      print ti_huan
                match_dos(ti_huan,shell_list)
            os.chdir(old_dir)
            return 0
        match = re.search("/R|/r", shell, re.I)
        if match:
            mu_lu = re.search("/[/r|/R]\s{1}([^\s]*)\s{1}%%",shell,re.I)
            #print "mu_lu",mu_lu
            if mu_lu:
                mu_lu = mu_lu.group(1)
                print_wenjian(mu_lu,shell)
            else:
                print_wenjian(os.getcwd(),shell)
            return 0

        match = re.search("/F|/f", shell, re.I)
        #-skip=n
        if match:
            set = re.search("\((.*)\)",shell,re.I)
            set = set.group(1)
            file = open(set,"r")
            file = file.readlines()
            for i in range(file.__len__()):
                file[i] = file[i].strip("\n")
            skip = re.search("-([^\s]*)\s{0,1}=\s{0,1}([^\s]*)",shell,re.I)
            if skip:
                left = skip.group(1)
                right = int(skip.group(2))
                command = re.search("DO\s{1}(.*)", shell, re.I)
                command = command.group(1)
                set_count = file.__len__()
                for i in range(0,file.__len__(),right):
                    ti_huan = re.sub("%%.+", "\""+file[i]+"\"", command)
                    match_dos(ti_huan,shell_list)
            else:
                command = re.search("DO\s{1}(.*)", shell, re.I)
                command = command.group(1)
                for i in range(0,file.__len__()):
                    ti_huan = re.sub("%%.+", "\""+file[i]+"\"", command)
                    match_dos(ti_huan, shell_list)
            return 0

        match = re.search("/L|/l", shell, re.I)
        if match:
            #生成序列
            set = re.search("\((.*)\)", shell, re.I)
            set = set.group(1)
            set = set.split(",")
            new_set = []
            for i in range(int(set[2])):
                if i == 0:
                    new_set.append(int(set[0]))
                else:
                    new_set.append(int(set[0])+int(set[1])*i)

            command = re.search("\)\s{1}(.*)", shell, re.I)
            command = command.group(1)
           # print  command
            set_count = new_set.__len__()
          #  print  set_count
            for i in range(set_count):
                ti_huan = re.sub("%%.+",str(new_set[i]),command)
                match_dos(ti_huan,shell_list)
                #commant = re.sub(" ", "", ti_huan)
            return 0
    except:
        print  "第" + ding_wei(shell, shell_list) + "条命令错误"
        print "for命令格式错误 格式如下："
        print "FOR %variable IN (set) DO command [command-parameters]"
        print "%variable  指定一个单一字母可替换的参数"
        print "(set)   指定一个或一组文件。可以使用通配符。"
        print "command    指定对每个文件执行的命令。"
        print "command-parameters 为特定命令指定参数或命令行开关。"
        print "FOR /D %variable IN (set) DO command [command-parameters]"
        print "如果集中包含通配符，则指定与目录名匹配，而不与文件名匹配。"
        print "FOR /R [[drive:]path] %variable IN (set) DO command [command-parameters] \n" \
        " 检查以 [drive:]path 为根的目录树，指向每个目录中的 FOR 语句。"\
        "如果在 /R 后没有指定目录规范，则使用当前目录。如果集仅为一个单点(.)字符，"\
        "则枚举该目录树。"
        print "FOR /L %variable IN (start,step,end) DO command [command-parameters]\n"\
        "该集表示以增量形式从开始到结束的一个数字序列。"
        print "FOR /F [\"options\"] %variable IN (file-set) DO command [command-parameters]\n"\
        "fileset 为一个或多个文件名。继续到 fileset 中的下一个文件之前，\n"\
        "每份文件都被打开、读取并经过处理。处理包括读取文件，将其分成一行行的文字，\n"\
        "然后将每行解析成零或更多的符号。\n"
        "skip=n          - 指在文件开始时忽略的行数。"
        _shou_hu()
def _while_(shell,shell_list):
    i =shell
    try:
        left = re.search("\(([a-z,1-9,\",\',%]+)\s*==", i, re.I)
        left = left.group(1)
       # print "left:", left
        if left[1] == "%":
            # print left[2:-1]
            left = can_shu[int(left[2:-1]) - 1]
            left = "\""+left+"\""
       #     print "left:", left

        right = re.search("==\s*([a-z,1-9,\",\',%]+)\)", i, re.I)
        right = right.group(1)
      #  print "right", right
        if right[1] == "%":
            right = can_shu[int(right[2:-1]) - 1]
            right = "\"" + right + "\""
      #      print "rirht:", right
        if left == right:
            command = re.search(r"\)\s{0,1}(.*)", i, re.I)
            command = command.group(1)
            match_dos(command, shell_list)
        if left != right: #左右不相等 返回0
            return 0
    except: #出错就报错
        print  "第" + ding_wei(shell, shell_list) + "条命令错误"
        print "while命令格式错误 格式如下：\n"\
        "while (expr == expr) DO command"
        _shou_hu()

def list_dir(mu_lu,new_mu_lu):
    #print mu_lu,"mu lu"
    #print "new mu lu",new_mu_lu

    for i in mu_lu:
        if os.path.isdir(i):
            lit_dir = os.listdir(i)
            #print lit_dir
            for j in  range(lit_dir.__len__()):
                lit_dir[j] = i +"\\" +lit_dir[j]
            list_dir(lit_dir,new_mu_lu)
        else:
            new_mu_lu.append(i)
    return new_mu_lu

def print_wenjian(mu_lu,shell):
    old_mu = os.getcwd()
    dir = os.chdir(mu_lu)
    dir = os.getcwd()
    dir = str(dir)
    #print "dir:", dir
    a = os.listdir(dir)
    for i in range(a.__len__()):
        a[i] = mu_lu + "\\" + a[i]
    new_dir = []
    a = list_dir(a, new_dir)
    #print a
    dir = os.chdir(old_mu)
    set = re.search("\((.*)\)", shell, re.I)
    set = set.group(1)
    pi_pei_fu = re.search("\*\.(.*)", set, re.I)
    pi_pei_fu = pi_pei_fu.group(1)
    #print pi_pei_fu
    result_path = []
    path = ""
    for path in a:
        match = re.search(pi_pei_fu + "$", path, re.I)
        if match:
            result_path.append(path)
    set = result_path
    #print "set:", set
    set_count = set.__len__()
    command = re.search("DO\s{1}(.*)", shell, re.I)
    command = command.group(1)

    for i in range(set_count):
        #print "set:",set[i]
        set[i] = set[i].replace("\\","\\\\")
        ti_huan = re.sub("%%.+",set[i], command)
        commant = re.sub(" ", "", ti_huan)
        commant = commant[4:]
        print commant.encode("utf-8")
def ding_wei(shell,shell_list):
    for i in range(shell_list.__len__()):
        if shell == shell_list[i]:
            return str(i+1)

def _shou_hu():

    while True:
        global can_shu
        path = os.path.dirname(os.path.abspath('__file__'))
        sys.stdout.write(path)
        a=raw_input(">")

        match = re.search(".*if.*", a, re.I)
        # print "can_shu:",can_shu
        if match:
            shell_list = a
            _if_(a, shell_list)
            continue

        match = re.match("^SET.*", a, re.I)
        if match:
            shell_list = a
            _set_(match.group(), shell_list)
            continue

        match = re.match("^echo.*", a, re.I)
        if match:
            shell_list = a
            _echo_(match.group(), shell_list)
            continue

        match = re.search(r"^for.*", a, re.I)
        if match:
            shell_list = a
            _for_(a, shell_list)
            continue

        match = re.search("^while.*", a, re.I)
        if match:
            shell_list = a
            _while_(a, shell_list)
            continue

        exit_ = re.match("exit", a, re.I)
        if exit_:
            print "cmd 退出"
            break

        if a == "":
            continue

        batch = re.match("([^.,\"]*\.batch)(\w*)", a, re.I)
        # print batch.group()
        if batch:
            if batch.groups().__len__()>1:
             #   print batch.groups()
                pass
            else:
                if batch.group(1):
                    match2 = re.match("([^.,\"]*\.batch$)",a,re.I)
                    if match2:
                        if not os.path.exists(batch.group(1)):
                            print "\"" + match2.group(1) + "\"" +"不是内部或外部命令，也不是可运行的文件或批处理文件"
                            continue
                        batch = batch.group()
                        # print par.group()
                        can_shu = None
                        batch_computer(batch)
                        continue
                    else:
                        print "\"" + batch.group(1) + "\"" + "不是内部或外部命令，也不是可运行的文件或批处理文件"


        par = re.sub(" |  |   |    ", "***", a)
        #print par
        batch = re.search("(\*{3})(\w+)(\*{3})*(\w+)*(\*{3})*(\w+)*(\*{3})*(\w+)*(\*{3})*(\w+)*(\*{3})*(\w+)*(\*{3})*(\w+)*",par,re.I)
        wen_jian = re.search("\w+\.batch",a,re.I)
        try:
            wen_jian = wen_jian.group()
 #           print wen_jian
            if not os.path.exists(wen_jian):
                print "\"" + wen_jian + "\"" + "不是内部或外部命令，也不是可运行的文件或批处理文件"
                continue

            #print  "sssssssss"
            if batch:
               # print "ssssssssssss"
  #              print batch.groups()
                batch = batch.groups()

                count = 0
                for i in batch:
                    if i!=None and i!="***":
                        count = count +1
                for i in range(count):
                    can_shu.append(batch[i*2+1])
  #              print "canshu:",can_shu
        except:
            print "\"" + a + "\"" + "不是内部或外部命令，也不是可运行的文件或批处理文件"
            continue
        batch_computer(wen_jian)
        continue

if __name__ == '__main__':
    biao_zhi = open("biao_zhi.txt","r")
    biao_zhi = biao_zhi.readlines()
    for i in range(biao_zhi.__len__()):
        biao_zhi[i] = biao_zhi[i].strip("\n")
        print biao_zhi[i]
    _shou_hu()