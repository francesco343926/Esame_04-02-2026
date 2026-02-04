class Artist:
    def __init__(self, artist_id, name, num_objects=0):
        self.artist_id = artist_id
        self.name = name
        self.num_objects = num_objects
        self.p = num_objects

    def __str__(self):
        return f"{self.name} (ID: {self.artist_id})"

    def __repr__(self):
        return self.__str__()
