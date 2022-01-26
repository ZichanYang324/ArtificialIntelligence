test_queries = [
    # casual query
    {
        "Query": "Departure",
        "Evidences": {
            "Jet": True,
            "Airport": True,
        },
    },
    # diagnostic query
    {
        "Query": "Runway",
        "Evidences": {
            "Cancellation": False,
            "Arrival": True,
        },
    },
    # sanity check
    {
        "Query": "Weather",
        "Evidences": {
            "MemberOfCrew": True,
        },
    }
]