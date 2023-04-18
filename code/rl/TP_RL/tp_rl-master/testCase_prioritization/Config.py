

class Config:
    def __init__(self):
        self.padding_digit = -1
        self.win_size = -1
        self.dataset_type = "simple"
        self.max_test_cases_count = 400
        self.training_steps = 10000
        self.discount_factor = 0.9
        self.experience_replay = False
        self.first_cycle = 1
        self.cycle_count = 100
        self.train_data = "../data/tc_data_paintcontrol.csv"
        self.output_path = '../data/ACERAgent'
        self.log_file="log.csv"