
# TODO: This should be serialised instead, or stored in redis.

# TODO: Check playlist for merged files.  Sum lengths of files and add the
# offset to the range.

# There needs to be an easier way of entering these times.  I'm not requiring
# accuracy here; on a first-pass I just want to skip sections that are a
# minute or more of nothing, such as intros and credits.

shows = {
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
        (257.6, 354.5),
        (2662.66, float("inf"))
      ]
    },
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
    }
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

