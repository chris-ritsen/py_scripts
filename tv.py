
# TODO: This should be serialised instead, or stored in redis.

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
        (1279.877, float("inf"))
      ]
    }
  }
}

