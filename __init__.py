"""
tptester

task-point tester
"""

import os
import sys
import json
import pty
from subprocess import CalledProcessError
class Test:
    """
    the main class of tptester
    contain tester interface
    """
    def __init__(self):
        self.__task_dict={}
        self.__point_dict={}

    def __run(self,args):
        """
        run args as splited command and print args & output of command
        use `pty.spawn()` to capture realtime output
        """
        print(args)
        returncode=pty.spawn(args)
        if returncode!=0:
            raise CalledProcessError(returncode,args)
        print()

    def add_task(self,name,steps):
        """ set steps of task `name` """
        self.__task_dict[name]=steps

    def add_point(self,name,opt):
        """ set option of point `name` """
        self.__point_dict[name]=opt

    def get_steps_task_on_point(self,taskname,pointname):
        """ get null-replaced steps to run task `taskname` on point `pointname` """
        return [[self.__point_dict[pointname]["project"] if x==None else x for x in step] for step in self.__task_dict[taskname]]

    def run_task_on_point(self,taskname,pointname):
        """ run the given task on given point """
        print("run task `"+taskname+"` on testpoint `"+pointname+"`")
        for step in self.get_steps_task_on_point(taskname,pointname):
            self.__run(step)

    def run_point(self,pointname):
        """ run the point with all tasks which need to run """
        for task in self.__point_dict[pointname]["tasks"]:
            self.run_task_on_point(task,pointname)

    def run_all(self):
        """ run all points """
        for point in self.__point_dict:
            self.run_point(point)

    def get_tasks(self):
        """
        get taskslist
        :returns: a dict mapping taskname -> steps
        """
        return self.__task_dict

    def get_points(self):
        """
        get pointslist
        :returns: a dict mapping pointname -> opt
        """
        return self.__point_dict

def scan_tests(tester):
    """
    scan tests in cwd
    any directory in cwd will be treated as a testpoint
    will read the info of testpoints from `.test.json` in each test directory
    """
    for project in [x for x in os.listdir() if os.path.isdir(x)]:
        opt={
            "project":project,
            "tasks":["generic"],
            "platform":sys.platform
        }
        try:
            with open(os.path.join(project,".test.json"),"r") as f:
                fopt=json.loads(f.read())
                for k,v in fopt.items():
                    opt[k]=v
        except (FileNotFoundError,json.decoder.JSONDecodeError):
            pass
        if opt["platform"]==sys.platform:
            opt["tasks"]=tuple(set([x for x in tester.get_tasks()]).intersection(opt["tasks"]))
            tester.add_point(project,opt)

def scan_tasks(tester):
    """ read tasks from `.test.json` in cwd """
    try:
        with open(".test.json","r") as f:
            ftsk=json.loads(f.read())
            for k,v in ftsk.items():
                if "platform" not in v or v["platform"]==sys.platform:
                    tester.add_task(k,v["steps"])
    except (FileNotFoundError,json.decoder.JSONDecodeError):
        pass

def auto_test():
    """ run tests autoly by scan_tasks & scan_tests """
    tester=Test()

    scan_tasks(tester)

    scan_tests(tester)

    tester.run_all()

if __name__=='__main__':
    auto_test()
