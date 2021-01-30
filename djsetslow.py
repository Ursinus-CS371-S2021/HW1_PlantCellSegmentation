# List of lists, where each inner list corresponds to a bubble
class ListSet:
    def __init__(self, N):
        self.N = N
        self._bubbles = []
        for i in range(N):
            self._bubbles.append({i})
    
    def get_set_label(self, i):
        """
        Return a number that is the same for every element in
        the set that i is in, and which is unique to that set
        Parameters
        ----------
        i: int
            Element we're looking for
        
        Returns
        -------
        Index of the bubble containing i
        """
        index = -1
        k = 0
        while k < len(self._bubbles) and index == -1:
            if i in self._bubbles[k]:
                index = k
            k += 1
        return index

    def find(self, i, j):
        """
        Return true if i and j are in the same component, or
        false otherwise
        Parameters
        ----------
        i: int
            Index of first element
        j: int
            Index of second element
        """
        return self.get_set_label(i) == self.get_set_label(j)
    
    def union(self, i, j):
        """
        Merge the two sets containing i and j, or do nothing if they're
        in the same set
        Parameters
        ----------
        i: int
            Index of first element
        j: int
            Index of second element
        """
        idx_i = self.get_set_label(i)
        idx_j = self.get_set_label(j)
        if idx_i != idx_j:
            # Merge lists
            # Decide that bubble containing j will be absorbed into
            # bubble containing i
            self._bubbles[idx_i] |= self._bubbles[idx_j]
            # Remove the old bubble containing j
            self._bubbles = self._bubbles[0:idx_j] + self._bubbles[idx_j+1::]
            

# Single list, each element is the ID of the corresponding object
class IDsSet:
    def __init__(self, N):
        self.N = N
        self._ids = list(range(N))
    
    def get_set_label(self, i):
        """
        Return a number that is the same for every element in
        the set that i is in, and which is unique to that set
        Parameters
        ----------
        i: int
            Element we're looking for
        
        Returns
        -------
        Index of the bubble containing i
        """
        return self._ids[i]

    def find(self, i, j):
        """
        Return true if i and j are in the same component, or
        false otherwise
        Parameters
        ----------
        i: int
            Index of first element
        j: int
            Index of second element
        """
        return self._ids[i] == self._ids[j]
    
    def union(self, i, j):
        """
        Merge the two sets containing i and j, or do nothing if they're
        in the same set
        Parameters
        ----------
        i: int
            Index of first element
        j: int
            Index of second element
        """
        # If i and j have different IDs, then we have to
        # merge the bubbles
        id_i = self._ids[i]
        id_j = self._ids[j]
        if id_i != id_j:
            # Let's merge everything in the bubble containing j
            # into the bubble containing i
            # In other words, everything with id_j should now
            # have id_i
            for k, id_k in enumerate(self._ids):
                if id_k == id_j:
                    self._ids[k] = id_i