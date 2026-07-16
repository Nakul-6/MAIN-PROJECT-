
# Hierachical_FL_DRL-with-AirFogSim

This is the code for "Privacy-Preserving Offloading in Dynamic Air-Ground Vehicular Fog Computing: A Hierarchical Federated Reinforcement Learning Framework" submitted to IEEE Open Journal of the Communications Society.

In "masac_config_parser.py", the user can change "method = " to any method in potential_methods = ['MAPPO_Cen_nMA','MAPPO_nFL','MAPPO_Cen','greedy_notLearn','Certain_FedAvg', 'MAPPO_AggFed_cluster3', 'MAPPO_AggFed_cluster2', 'MAPPO_AggFed_cluster3_local','MAPPO_AggFed_cluster2_local','MAPPO_AggFed_cluster1_local']. Then, change the st_iter_id as 0 or 2, respsectively. As such, the results will run 4 Deployments for all baselines in the paper.

Map from Methods to Baselines in Paper
MAPPO_Cen_nMA = Cen-PPO without Attention
MAPPO_Cen = Cen-PPO
greedy_notLearn = Greedy
Certain_FedAvg = AFedPPO-Avg
MAPPO_AggFed_cluster3 = AFedPPO-C, number of cluster=3
MAPPO_AggFed_cluster2 = AFedPPO-C, number of cluster=2
MAPPO_AggFed_cluster3_local = AFedPPO-CCP, number of cluster=3
MAPPO_AggFed_cluster2_local = AFedPPO-CCP, number of cluster=2
MAPPO_AggFed_cluster1_local = AFedPPO-CCP, number of cluster=1

output includes the tensorboard results (stored in /results/runs3) and trained models (stored in /results/models). To ensure the model is stored, please modify "fre_to_save" in masac_config_parser.py as you need, or remove --n_episode 1 in run bash.