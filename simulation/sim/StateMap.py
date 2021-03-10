from model.BasicElements import *


class StateMap(object):
    base: int
    start_age: int
    end_age: int
    state_list: List[Node]
    link_list: List[Link]

    # 分年龄段转移概率表
    link_risk: List[Dict[int, int]]
    # link idx
    node_links: Dict[int, List[int]]

    # 记录可能的下一种状态 age -> state -> [NextState]
    age_next_state: Dict[int, Dict[int, List[NextState]]]

    def __init__(self, base=10000):
        self.base = base
        self.start_age = 0xffff
        self.end_age = -0xffff
        self.state_list = []
        self.link_list = []

        self.link_risk = []
        self.node_links = {}

    def set_base(self, base):
        self.base = base

    def add_state(self, name: str) -> int:
        idx = len(self.state_list)
        node = Node(name)
        self.state_list.append(node)
        self.node_links[idx] = []
        return idx

    def get_state_name(self, state_id: int) -> str:
        return self.state_list[state_id].name

    def get_age_next_state(self, age: int):
        for key in self.age_next_state[age]:
            print("state: " + str(key))
            for node in self.age_next_state[age][key]:
                print("next_node: " + str(node.next_idx) + " " + str(node.cut))

    def add_link(self, source: int, target: int) -> int:
        assert source < len(self.state_list) and target < len(self.state_list)
        link_idx = len(self.link_list)
        self.link_list.append(Link(source, target))
        self.link_risk.append({})
        # 存的是link的idx
        self.node_links[source].append(link_idx)

        return link_idx

    def set_risk(self, link_id: int, age_from: int, age_to: int, risk: int):
        assert link_id < len(self.link_list)
        # 同时更新年龄区间
        self.start_age = min(age_from, self.start_age)
        self.end_age = max(age_to, self.end_age)
        # link = self.link_list[link_idx]
        for i in range(age_from, age_to + 1):
            self.link_risk[link_id][i] = risk

    def build(self):
        # clean 字典 记录年龄对应下一个状态
        self.age_next_state = {}
        for age in range(self.start_age, self.end_age + 1):
            self.age_next_state[age] = {}
        # 对于年龄段内每一个年龄
        for age in range(self.start_age, self.end_age + 1):
            for node_id, node in enumerate(self.state_list):
                links = self.node_links[node_id]  # 从该节点出发的所有边
                cut = self.base
                for link_id in links:
                    if age in self.link_risk[link_id]:
                        risk = self.link_risk[link_id][age]
                    else:
                        continue
                    cut -= risk  # cut - 所有边的risk
                # 减去所有risk
                # 先加入自己的cut, 再加入其它的
                self.age_next_state[age][node_id] = [NextState(cut=cut, next_idx=node_id)]
                for link_id in links:
                    if age in self.link_risk[link_id]:
                        risk = self.link_risk[link_id][age]
                    else:
                        continue
                    link = self.link_list[link_id]
                    cut += risk
                    self.age_next_state[age][node_id].append(NextState(cut=cut, next_idx=link.target))

    def get_next_state(self, age: int, num: int, state_id: int) -> int:
        """
        根据年龄和随机数获取下一个状态
        :param age:
        :param num:
        :param state_id:
        :return:
        """
        assert state_id < len(self.state_list) and num < self.base
        # 如果年龄就不变
        if age not in self.age_next_state:
            return state_id
        if state_id not in self.age_next_state[age]:
            return state_id
        for next_state in self.age_next_state[age][state_id]:
            # print(self.age_next_state[age])
            if num < next_state.cut:
                return next_state.next_idx


def load_state_map(states: List[str], groups: List[Tuple[int, int]],
                   risk_map: Dict[Tuple[int, int], List[int]], **xargs) -> StateMap:
    mp = StateMap(**xargs)
    for n in states:
        mp.add_state(n)
    for key in risk_map:
        risks = risk_map[key]
        (source, target) = key
        link_id = mp.add_link(source, target)
        for j, ag in enumerate(groups):
            mp.set_risk(link_id=link_id, age_from=ag[0], age_to=ag[1], risk=risks[j])
    return mp
