from typing import Optional

class TrieNode:
    def __init__(self, char : str):
        self.char = char
        self.children : dict[str, "TrieNode"] = {}
        self.terminal = False

    def getChild(self, childchar : str, create : bool = False) -> Optional["TrieNode"]:
        child = self.children.get(childchar, TrieNode(childchar) if create else None)
        if create:
            self.children[childchar] = child

        return child
        
    def isTerminal(self) -> bool:
        return self.terminal
    
    def setTerminal(self):
        self.terminal = True


class Trie:
    
    def __init__(self):
        self.head = TrieNode("")
        
    def put(self, value : str):
        cur : TrieNode = self.head
        for char in value:
            cur = cur.getChild(char, create=True)

        cur.setTerminal()

    def __get(self, value : str) -> Optional[TrieNode]:
        cur : TrieNode = self.head
        for char in value:
            cur = cur.getChild(char, create=False)

            if cur is None:
                return None
   
        return cur

    def isIn(self, value):
        """
        0 = not in trie
        1 = partially in trie
        2 = full match in trie
        """
        tail = self.__get(value)


        if tail is None:
            return 0
        
        if not tail.isTerminal():
            return 1
        else:
            return 2
        
if __name__ == "__main__":
    t = Trie()
    t.put("abc")
    t.put("abcd")

    assert t.isIn("ab") == 1
    assert t.isIn("abc") == 2
    assert t.isIn("abcd") == 2
    assert t.isIn("abf") == 0