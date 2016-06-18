
# TODO: This should be serialised instead, or stored in redis.

# TODO: Check playlist for merged files.  Sum lengths of files and add the
# offset to the range.

# There needs to be an easier way of entering these times.  I'm not requiring
# accuracy here; on a first-pass I just want to skip sections that are a
# minute or more of nothing, such as intros and credits.

shows = {
  "cosmos.space_time_odyssey.a": {
    "s01e01": {
      "ranges": [
        (139, 229.5),
        (2601.35, float("inf"))
      ]
    },
    "s01e02": {
      "ranges": [
        (46, 136.35),
        (2551.632, float("inf"))
      ]
    },
    "s01e03": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s01e04": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s01e05": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s01e06": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s01e07": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s01e08": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s01e09": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s01e10": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s01e11": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s01e12": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s01e13": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
  },
  "star_trek.next_generation.the": {
    "s02e06": {
      "ranges": [
        (196.6, 293.1),
        (2678.5, float("inf"))
      ]
    },
    "s02e07": {
      "ranges": [
        (140.52, 237.65),
        (2663.3, float("inf"))
      ]
    },
    "s02e08": {
      "ranges": [
        (236, 332.8),
        (2677.341, float("inf"))
      ]
    },
    "s02e09": {
      "ranges": [
        (219.97, 316.64),
        (2683.25, float("inf"))
      ]
    },
    "s02e10": {
      "ranges": [
        (244.202, 340.84),
        (2663.75, float("inf"))
      ]
    },
    "s02e11": {
      "ranges": [
        (253.128, 350),
        (2680.1, float("inf"))
      ]
    },
    "s02e12": {
      "ranges": [
        (187.48, 284.25),
        (2677.508, float("inf"))
      ]
    },
    "s02e13": {
      "ranges": [
        (213.505, 310.644),
        (2678.97, float("inf"))
      ]
    },
    "s02e14": {
      "ranges": [
        (160.535, 257.591),
        (2664.078, float("inf"))
      ]
    },
    "s02e15": {
      "ranges": [
        (257.85, 354.5),
        (2662.66, float("inf"))
      ]
    },
    # Stupid problem where it won't advance past the end.  It's not paused,
    # but won't continue.
    "s02e16": {
      "ranges": [
        (218.927, 315.9),
        (2662.952, float("inf"))
      ]
    },
    "s02e17": {
      "ranges": [
        (318.985, 415.1),
        (2662.952, float("inf"))
      ]
    },
    "s02e18": {
      "ranges": [
        (186.311, 282.15),
        (2785.298, float("inf"))
      ]
    },
    "s02e19": {
      "ranges": [
        (205.205, 302.177),
        (2673.921, float("inf"))
      ]
    },
    "s02e20": {
      "ranges": [
        (204.663, 301.092),
        (2679.51, float("inf"))
      ]
    },
    "s02e21": {
      "ranges": [
        (202.285, 299.049),
        (2679.051, float("inf"))
      ]
    },
    "s02e22": {
      "ranges": [
        (184.393, 280.947),
        (2678.092, float("inf"))
      ]
    },
    "s03e01": {
      "ranges": [
        (213.86, 320.717),
        (2680.074, float("inf"))
      ]
    },
    "s03e02": {
      "ranges": [
        (203.8, 310.1),
        (2679.875, float("inf"))
      ]
    },
    "s03e03": {
      "ranges": [
        (150.589, 257.237),
        (2679.74, float("inf"))
      ]
    },
    "s03e04": {
      "ranges": [
        (122.519, 229.284),
        (2665.518, float("inf"))
      ]
    },
    "s03e05": {
      "ranges": [
        (88.443, 195.342),
        (2681.158, float("inf"))
      ]
    },
    "s03e06": {
      "ranges": [
        (244.766, 353.166),
        (2682.159, float("inf"))
      ]
    },
    "s03e07": {
      "ranges": [
        (276.339, 383.905),
        (2679.031, float("inf"))
      ]
    },
    "s03e08": {
      "ranges": [
        (208.355, 316.129),
        (2670.7, float("inf"))
      ]
    },
    "s03e09": {
      "ranges": [
        (100.122, 207.062),
        (2680.69, float("inf"))
      ]
    },
    "s03e10": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s03e11": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s03e12": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s03e13": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s03e14": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s03e15": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s03e16": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
    "s03e17": {
      "ranges": [
        # (, ),
        # (, float("inf"))
      ]
    },
  },
  "rick_and_morty": {
    "s02e07": {
      "ranges": [
        (121.91, 153.75),
        (1291.91, 1323.489),
        (1367.8, float("inf"))
      ]
    },
    "s02e08": {
      "ranges": [
        (1289.87, 1320.62),
        (1341.25, float("inf"))
      ]
    }
  }
}

