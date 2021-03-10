from sim.StateMap import *


def get_base(val):
    xs = 0
    if val[-1] == '%':
        xs = 2
        val = val[:-1]
    xs += len(val) - val.index('.') - 1
    return 10 ** xs


# 转换百分数
def convert_val(val):
    base = get_base(val)
    if val[-1] == '%':
        val = val[:-1]
        base /= 100
    return int(base * float(val))


class MapReader(object):
    """
    读取excel文件并转化成转移概率图的类
    """
    path: str
    groups: List[Tuple[int, int]]
    states: List[str]
    base: int
    risk_map: Dict[Tuple, List[int]]
    state_map: StateMap

    def __init__(self, path: str):
        self.path = path
        self.states = []
        links = []
        df = pd.read_csv(path, index_col='Group')
        # 解析states 和 links
        for name in df.columns:
            if '->' not in str(name):
                self.states.append(name.strip())
            else:
                links.append(name.strip())
        state_id = {}
        for i, s in enumerate(self.states):
            state_id[s] = i
        groups = []  # 解析年龄组
        for name in df.index:
            arr = list(map(lambda x: x.strip(), name.split('-')))
            groups.append((int(arr[0]), int(arr[1])))
        self.groups = groups
        risk_map = {}
        link_pair = []
        for name in links:
            name = name.strip()
            arr = list(map(lambda x: x.strip(), name.split('->')))
            pair = (state_id[arr[0]], state_id[arr[1]])
            # print("pair: " + str(pair))
            vals = list(df[name])
            # print("vals: " + str(vals))
            self.base = get_base(vals[0])
            risk_map[pair] = list(map(convert_val, vals))
            # print("risk_map[" + str(pair) + "]" + " " + str(risk_map[pair]))
            link_pair.append(pair)
        self.risk_map = risk_map
        self.state_map = load_state_map(states=self.states, groups=self.groups, risk_map=risk_map, base=self.base)

    def get_state_map(self) -> StateMap:
        return self.state_map
