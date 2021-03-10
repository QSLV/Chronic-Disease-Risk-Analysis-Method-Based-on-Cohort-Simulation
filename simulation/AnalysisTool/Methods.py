from sim.MapReader import *
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Songti SC']
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False


def get_trade_items(death_list):
    # 统计各路线人数
    trade_count = {}
    # 计算平均年龄
    trace_age_sum = {}
    for p in death_list:
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
    return (trace_age_sum, backitems)


def conver(x, trace_age_sum, states, population):
    v = x[1]
    count = (trace_age_sum[v] / x[0]).astype(int)
    v = v[1:-1]
    arr = str(v).split(',')

    res = list(map(lambda x: states[int(x)], arr))

    buf = []
    for i, state in enumerate(res):
        buf.append("%s(%d)" % (state, count[i]))

    return " -> ".join(buf) + "  %.1f%%" % (100 * x[0] / population)


def get_top10_cohorts(backitems, trace_age_sum, states, population):
    top10_cohorts = []
    for item in backitems[:10]:
        top10_cohorts.append(conver(item, trace_age_sum, states, population))
    for cohort in top10_cohorts:
        print(str(cohort))
    return top10_cohorts


states_ch = [
    '健康',
    '缺血性心脏病',
    '缺血性卒中',
    '二型糖尿病',
    '缺血性心脏病 & 缺血性卒中',
    '缺血性卒中 & 二型糖尿病',
    '缺血性心脏病 & 二型糖尿病',
    '死亡'
]


def handle(x, trace_age_sum, states, population):
    v = x[1]
    count = (trace_age_sum[v] / x[0]).astype(int)
    v = v[1:-1]
    arr = str(v).split(',')

    res = list(map(lambda x: states[int(x)], arr))

    buf = []
    tr = []
    cs = []
    for i, state in enumerate(res):
        tr.append(state)
        cs.append(count[i])
        buf.append("%s(%d)" % (state, count[i]))

    return tr, cs, (100 * x[0] / population)


def gen_plt_data(items, trace_age_sum, states, population):
    plt_data = []
    for item in items:
        names, count, ps = handle(item, trace_age_sum, states, population)
        plt_data.append((names, count, ps))
    return plt_data


def plot_trajd(plt_data, title, path):
    states_color = {
        'Health': '#67C23A',
        'IA': '#E6A23C',
        'IS': '#E6A23C',
        'DM': '#E6A23C',
        'IA & IS': '#E6A23C',
        'IA & DM': '#E6A23C',
        'IS & DM': '#E6A23C',
        'Death': '#909399',

    }

    plt.figure('trajectory', (22, 12), dpi=150)

    plt.xlim(25, 100)
    plt.ylim(len(plt_data) + 1, 0)

    ax = plt.gca()
    plt.yticks(range(1, len(plt_data) + 1))
    plt.xticks(range(30, 95, 5))
    ax.spines['top'].set_color('none')
    # ax.spines['bottom'].set_position(('outward', -10))

    ax.set_xlabel("Age")
    ax.set_ylabel("Trajectory")
    plt.title(title)

    maxx = 0
    for y, arr in enumerate(plt_data):
        y += 1
        (names, xs, b) = arr
        for j, name in enumerate(names):
            maxx = max(xs[j], maxx)
            plt.scatter(xs[j], y, c=states_color[name])

            plt.text(xs[j], y + .15, s=name, fontsize=15,
                     verticalalignment='top', horizontalalignment='center')
            plt.text(xs[j], y - .15, s=str(xs[j]), fontsize=15,
                     verticalalignment='bottom', horizontalalignment='center')
            if j > 0:
                ax.annotate("", xy=(xs[j], y), xytext=(xs[j - 1], y),
                            arrowprops=dict(arrowstyle="->", color=states_color[names[j - 1]]))
    for y, arr in enumerate(plt_data):
        y += 1
        (names, xs, b) = arr
        plt.text(maxx + 5, y - .1, s="%.1f%%" % b, fontsize=15, verticalalignment='top', horizontalalignment='right')
    plt.savefig(path + title + ".png")
    plt.show()
