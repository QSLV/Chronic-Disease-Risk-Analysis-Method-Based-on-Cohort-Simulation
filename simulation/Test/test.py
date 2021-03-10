from sim.MapReader import *
from sim.Simulator import Simulator
from AnalysisTool.Methods import *

if __name__ == '__main__':
    from_year = 2009
    to_year = 2010
    pic_save_path = "../image_result/"

    reader = MapReader('../input/' + str(from_year) + '-' + str(to_year) + '.csv')
    #reader = MapReader('../input/tea_year/tea_year_1.csv')
    states = reader.states

    sim = Simulator(state_map=reader.get_state_map())
    sim.start()
    population = sim.population

    (trace_age_sum, backitems) = get_trade_items(sim.death_list)
    top10_cohorts = get_top10_cohorts(backitems, trace_age_sum, states, population)
    p_data = gen_plt_data(backitems[:10], trace_age_sum, states, population)
    #plot_trajd(p_data[:5], str(from_year) + '-' + str(to_year) + '年', pic_save_path)
    plot_trajd(p_data[:5], "tea_year_1", pic_save_path)