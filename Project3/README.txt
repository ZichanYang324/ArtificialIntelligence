Group members: Yushan Zhou, Zichan Yang

This project runs on Python3
FlightStatusNetwork.py stores the structure of our network
Queries.py stores test cases, including casual query, diagnostic query, and sanity check, you could modify the test cases to check any arbitrary query
main.py reads test cases from Queries.py and print out the exact inference result, Rejection Sampling result, and Gibbs Sampling result

Example output:
Query:              Departure
Evidences:          {'Jet': True, 'Airport': True}
Exact Inference:    [0.8300000000000001, 0.16999999999999996]
Rejection Sampling: [0.8323311619620288, 0.16766883803797117]
Gibbs Sampling:     [0.82629, 0.17371]
