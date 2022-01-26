flightStatusNetwork = {
    "Jet": {
        "Parent": [],
        "Child": ["MemberOfCrew"],
        "Probability": {
            (): 0.9,
        },
    },
    "Airport": {
        "Parent": [],
        "Child": ["Runway", "Weather"],
        "Probability": {
            (): 0.8,
        },
    },
    "MemberOfCrew": {
        "Parent": ["Jet"],
        "Child": ["Departure"],
        "Probability": {
            (True,): 0.8,
            (False,): 0.3,
        },
    },
    "Runway": {
        "Parent": ["Airport"],
        "Child": ["Departure"],
        "Probability": {
            (True,): 0.8,
            (False,): 0.1,
        },
    },
    "Weather": {
        "Parent": ["Airport"],
        "Child": ["Cancellation"],
        "Probability": {
            (True,): 0.4,
            (False,): 0.7,
        },
    },
    "Departure": {
        "Parent": ["MemberOfCrew", "Runway"],
        "Child": ["Arrival"],
        "Probability": {
            (True, True): 0.9,
            (True, False): 0.75,
            (False, True): 0.8,
            (False, False): 0.15,
        },
    },
    "Arrival": {
        "Parent": ["Departure"],
        "Child": [],
        "Probability": {
            (True,): 0.9,
            (False,): 0.4,
        },
    },
    "Cancellation": {
        "Parent": ["Weather"],
        "Child": [],
        "Probability": {
            (True,): 0.1,
            (False,): 0.8,
        },
    }
}
