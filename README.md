# Possibilistic approach to network nonlocality 
This repository is a tool to explore the results exposed in our article https://arxiv.org/pdf/2208.13526.pdf. 
The paper proposes moving away from probabilities and focusing on possibilities to investigate network's local, quantum, and non-signaling models. The authors aim to determine which patterns of possible and impossible events are compatible with a given network structure. They present various methods to address this question, such as using the inflation technique, SAT solvers, and efficient combinatorial algorithms.
Here can be found the study of the triangle network and the square network (both for the case of binary outputs and without inputs. 
In this context, the underlying marginal compatibility problem can be expressed as a SAT problem. We use here Z3, the theorem prover from Microsoft Research https://github.com/Z3Prover/z3.
