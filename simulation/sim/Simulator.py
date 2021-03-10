from sim.StateMap import *


class Simulator(object):
    state_map: StateMap
    rand: random.Random

    # 存idx
    init_state: int
    end_state: int

    # 总人口数
    population: int

    # 生存列表
    living_list: List[Person]
    # 死亡列表
    death_list: List[Person]

    # 当前模拟年龄
    current_age: int

    def __init__(self, state_map: StateMap, population: int = 10 ** 5, rand_seed=1):
        self.state_map = state_map
        self.state_map.build()

        # 默认
        self.init_state = 0
        self.end_state = len(self.state_map.state_list) - 1

        self.rand = random.Random(rand_seed)
        self.population = population

    def aging(self):
        """
        模拟过了一年，对人口进行模拟变化
        :return:
        """
        self.current_age += 1
        age = self.current_age
        state_count = {}
        new_living_list = []
        for person in self.living_list:
            # 随机数
            num = self.rand.randrange(0, self.state_map.base)
            state_id = person.state
            vage = age
            if vage > self.state_map.end_age:
                vage = self.state_map.end_age
            next_state = self.state_map.get_next_state(age=vage, num=num, state_id=state_id)
            if age > self.state_map.end_age:
                next_state = self.end_state
            name = self.state_map.get_state_name(next_state)
            if name in state_count:
                state_count[name] += 1
            else:
                state_count[name] = 1
            if next_state != state_id:
                person.state = next_state
                person.state_history.append(next_state)
                person.state_age_history.append(age)
            # 遍历时删除list
            if next_state != self.end_state:
                new_living_list.append(person)
            else:
                self.death_list.append(person)
        self.living_list = new_living_list
        print("\rage:", self.current_age, "live:", len(self.living_list), "death:", len(self.death_list), end='')

    def start(self):
        # 初始化
        self.current_age = self.state_map.start_age
        self.living_list = []
        self.death_list = []
        for i in range(0, self.population):
            self.living_list.append(Person(i, self.init_state, self.current_age))

        while len(self.living_list) > 0:
            self.aging()
        print("\nsim terminated:", len(self.death_list))

    def analysis(self):
        # 统计各路线人数
        trade_count = {}
        # 计算平均年龄
        trace_age_sum = {}
        for p in self.death_list:
            ckey = "%s" % p.state_history
            if ckey not in trade_count:
                trade_count[ckey] = 1
                trace_age_sum[ckey] = np.asarray(p.state_age_history)
            else:
                trade_count[ckey] += 1
                trace_age_sum[ckey] += np.asarray(p.state_age_history)
        # 选出前10
        items = trade_count.items()
        backitems = [[v[1], v[0]] for v in items]
        backitems.sort(reverse=True)
        print(backitems[:10])