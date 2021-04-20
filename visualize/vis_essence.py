import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')

task_list = [
    [19662742, "资本家", "Capitalists"],
    [20073342, "社会主义", "Socialism"],
    [19916030, "剥削", "Exploitation"],
    [20064332, "996", "996"],
    [19613266, "左派", "Left-wing"],
    [19960840, "强制加班","Mandatory Overwork"],
    [19582963, "资本主义", "Capitalism"],
    [19685024, "阶级", "Class"],
    [19582433, "苏联", "Soviet"],
    [19571449, "马克思", "Marx"],
    [19924829, "共产国际", "Commintern"],
    [19599479, "世界史", "World History"],
    [19551424, "政治", "Politics"],
    [19566933, "社会", "Society"],
    [19551077, "历史", "History"]
]

def vis_essence(args=None, normalize=True):

    flow = []
    fl = '../log/{}_{}_essense.json'
    