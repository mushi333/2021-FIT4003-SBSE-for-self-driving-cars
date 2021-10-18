import pickle

from examples.AV.example_runner_ga_av import runner as ga_runner
# from examples.AV.example_runner_ba_av import runner as ba_runner
from examples.AV.example_runner_drl_av import runner as drl_runner
# from examples.AV.example_runner_ge_av import runner as go_explore_runner
from examples.AV.example_runner_mcts_av import runner as mcts_runner
import time, os

if __name__ == '__main__':
    # Which algorithms to run
    runs = 1
    RUN_DRL = False
    RUN_MCTS = False
    RUN_GA = True
    RUN_GASM = False
    RUN_GA_MOD = False

    max_path_length = 50
    s_0 = [0.0, -4.0, 1.0, 11.17, -35.0]
    base_log_dir = './data'
    run_experiment_args = {'snapshot_mode': 'last',
                           'snapshot_gap': 1,
                           'log_dir': None,
                           'exp_name': None,
                           'seed': 0,
                           'n_parallel': 8,
                           'tabular_log_file': 'progress.csv'
                           }

    runner_args = {'n_epochs': 100,
                   'batch_size': 500,
                   'plot': True
                   }

    env_args = {'id': 'ast_toolbox:GoExploreAST-v1',
                'blackbox_sim_state': True,
                'open_loop': False,
                'fixed_init_state': True,
                's_0': s_0,
                }

    sim_args = {'blackbox_sim_state': True,
                'open_loop': False,
                'fixed_initial_state': True,
                'max_path_length': max_path_length
                }

    reward_args = {'use_heuristic': True}

    spaces_args = {}

    # MCTS ----------------------------------------------------------------------------------

    if RUN_MCTS:
        # MCTS Settings

        mcts_type = 'mcts'

        mcts_sampler_args = {}

        mcts_algo_args = {'max_path_length': max_path_length,
                          'stress_test_mode': 2,
                          'ec': 100.0,
                          'n_itr': runner_args['n_epochs'],
                          'k': 0.5,
                          'alpha': 0.5,
                          'clear_nodes': True,
                          'log_interval': runner_args['batch_size'],
                          'plot_tree': False,
                          'plot_path': None,
                          'log_dir': None,
                          }

        mcts_bpq_args = {'N': 10}

        # MCTS settings
        run_experiment_args['log_dir'] = base_log_dir + '/mcts'
        run_experiment_args['exp_name'] = 'mcts'

        mcts_algo_args['max_path_length'] = max_path_length
        mcts_algo_args['log_dir'] = run_experiment_args['log_dir']
        mcts_algo_args['plot_path'] = run_experiment_args['log_dir']

        for i in range(runs):
            # Run MCTS and set time
            start = time.time()
            mcts_runner(
                mcts_type=mcts_type,
                env_args=env_args,
                run_experiment_args=run_experiment_args,
                sim_args=sim_args,
                reward_args=reward_args,
                spaces_args=spaces_args,
                algo_args=mcts_algo_args,
                runner_args=runner_args,
                bpq_args=mcts_bpq_args,
                sampler_args=mcts_sampler_args,
                save_expert_trajectory=True,
            )
            end = time.time()
            with open("mcts_time.txt", "a") as file:
                file.writelines(str(end - start) + "\n")

            # Change file names
            os.rename("mcts_paths.txt", "run_data/mcts/mcts_paths_" + str(i) + ".txt")
            os.rename("mcts_rewards.txt", "run_data/mcts/mcts_rewards_" + str(i) + ".txt")
            os.rename("mcts_crashes.txt", "run_data/mcts/mcts_crashes_" + str(i) + ".txt")

        # Move time to data file
        os.rename("mcts_time.txt", "run_data/mcts/mcts_time.txt")

        # Delete ga files from mcts run
        os.remove("ga_paths.txt")
        os.remove("ga_rewards.txt")
        os.remove("ga_crashes.txt")

    # GA ----------------------------------------------------------------------------------

    if RUN_GA:
        # GA Settings

        GA_policy_args = None

        GA_baseline_args = {}

        GA_algo_args = {'step_size': 0.01,
                        'n_itr': runner_args['n_epochs'],
                        'step_size_anneal': 1,
                        'pop_size': 50,
                        'truncation_size': 3,
                        'keep_best': 1,
                        'f_F': "mean",
                        }

        run_experiment_args['log_dir'] = base_log_dir + '/ga'
        run_experiment_args['exp_name'] = 'ga'

        GA_algo_args['max_path_length'] = max_path_length

        GA_bpq_args = {'N': 10}
        GA_sampler_args = {}

        for i in range(runs):
            # Run GA and set time
            start = time.time()
            ga_runner(
                ga_type="ga",
                env_args=env_args,
                run_experiment_args=run_experiment_args,
                sim_args=sim_args,
                reward_args=reward_args,
                spaces_args=spaces_args,
                policy_args=GA_policy_args,
                # baseline_args=GA_baseline_args,
                algo_args=GA_algo_args,
                runner_args=runner_args,
                bpq_args=GA_bpq_args,
                sampler_args=GA_sampler_args,
            )
            
            # Clock time taken
            end = time.time()
            with open("ga_time.txt", "a") as file:
                file.writelines(str(end - start) + "\n")

            # Change file names and move to individal folder
            os.rename("ga_paths.txt", "run_data/ga/ga_paths_" + str(i) + ".txt")
            os.rename("ga_rewards.txt", "run_data/ga/ga_rewards_" + str(i) + ".txt")
            os.rename("ga_crashes.txt", "run_data/ga/ga_crashes_" + str(i) + ".txt")
            
        # Move time to data file
        os.rename("ga_time.txt", "run_data/ga/ga_time.txt")

        # Delete mcts files from ga run
        os.remove("mcts_paths.txt")
        os.remove("mcts_rewards.txt")
        os.remove("mcts_crashes.txt")

    # GASM ----------------------------------------------------------------------------------

    if RUN_GASM:
        # GA Settings

        GA_policy_args = None

        GA_baseline_args = {}

        GASM_algo_args = {'step_size': 0.01,
                        'n_itr': runner_args['n_epochs'],
                        'step_size_anneal': 1,
                        'pop_size': 10,
                        'truncation_size': 3,
                        'keep_best': 1,
                        'f_F': "mean",
                        }

        run_experiment_args['log_dir'] = base_log_dir + '/ga'
        run_experiment_args['exp_name'] = 'ga'

        GASM_algo_args['max_path_length'] = max_path_length

        GA_bpq_args = {'N': 10}
        GA_sampler_args = {}

        # Run GASM
        ga_runner(
            ga_type="gasm",
            env_args=env_args,
            run_experiment_args=run_experiment_args,
            sim_args=sim_args,
            reward_args=reward_args,
            spaces_args=spaces_args,
            policy_args=GA_policy_args,
            # baseline_args=GA_baseline_args,
            algo_args=GASM_algo_args,
            runner_args=runner_args,
            bpq_args=GA_bpq_args,
            sampler_args=GA_sampler_args,
        )

    # GA_MOD ----------------------------------------------------------------------------------

    if RUN_GA_MOD:
        # GA Settings

        GA_policy_args = None

        GA_baseline_args = {}

        GA_algo_args = {'step_size': 0.01,
                        'n_itr': runner_args['n_epochs'],
                        'step_size_anneal': 1,
                        'pop_size': 5,
                        'truncation_size': 3,
                        'keep_best': 1,
                        'f_F': "mean",
                        }

        run_experiment_args['log_dir'] = base_log_dir + '/mga'
        run_experiment_args['exp_name'] = 'mga'

        GA_algo_args['max_path_length'] = max_path_length

        GA_bpq_args = {'N': 10}
        GA_sampler_args = {}

        # Run GA
        ga_runner(
            ga_type="mga",
            env_args=env_args,
            run_experiment_args=run_experiment_args,
            sim_args=sim_args,
            reward_args=reward_args,
            spaces_args=spaces_args,
            policy_args=GA_policy_args,
            # baseline_args=GA_baseline_args,
            algo_args=GA_algo_args,
            runner_args=runner_args,
            bpq_args=GA_bpq_args,
            sampler_args=GA_sampler_args,
        )

    # DRL ----------------------------------------------------------------------------------

    if RUN_DRL:
        # DRL Settings

        drl_policy_args = {'name': 'lstm_policy',
                           'hidden_dim': 64,
                           }

        drl_baseline_args = {}

        drl_algo_args = {'max_path_length': max_path_length,
                         'discount': 0.99,
                         'lr_clip_range': 1.0,
                         'max_kl_step': 1.0,
                         # 'log_dir':None,
                         }

        run_experiment_args['log_dir'] = base_log_dir + '/drl'
        run_experiment_args['exp_name'] = 'drl'

        drl_algo_args['max_path_length'] = max_path_length

        # Run DRL
        drl_runner(
            env_args=env_args,
            run_experiment_args=run_experiment_args,
            sim_args=sim_args,
            reward_args=reward_args,
            spaces_args=spaces_args,
            policy_args=drl_policy_args,
            baseline_args=drl_baseline_args,
            algo_args=drl_algo_args,
            runner_args=runner_args,
            save_expert_trajectory = False
        )
