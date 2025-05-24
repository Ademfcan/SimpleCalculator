class BackedList:
    def __init__(self, backing_str : str):
        self.backing_str = backing_str
        self.data = {}
        self.extractedRange = [True] * len(backing_str)
    
    def addChunkI(self, index : int):
        self.addChunk(index, index+1)
    
    def addChunk(self, start : int, end : int):
        if not all(self.extractedRange[start:end]):
            raise ValueError("Chunk is in range of another extracted chunk")

        chunk = self.backing_str[start:end]
        self.extractedRange[start:end] = [False] * (end-start)
        
        self.data[(start, end)] = chunk

    def getAsList(self, withMark = False) -> list[str]:
        ret = []

        prev_end = 0
        for chunk_range in sorted(self.data.keys()):
            start, end = chunk_range
            chunk_str = self.data[chunk_range]

            unchunkedData = self.backing_str[prev_end:start]
            if unchunkedData:
                if withMark:
                    unchunkedData = f"R:{unchunkedData}"
                ret.append(unchunkedData)

            ret.append(chunk_str)
            prev_end = end

        if prev_end < len(self.backing_str):
            ret.append(self.backing_str[prev_end:])

        return ret
    
if __name__ == "__main__":
    backedL = BackedList("1+2+3*Sin(3)")
    backedL.addChunkI(1)
    backedL.addChunkI(3)
    backedL.addChunkI(5)
    backedL.addChunk(6, 12)


    assert backedL.getAsList() == ["1", "+", "2", "+", "3", "*", "Sin(3)"]
    assert backedL.getAsList(withMark=True) == ["R:1", "+", "R:2", "+", "R:3", "*", "Sin(3)"]

    