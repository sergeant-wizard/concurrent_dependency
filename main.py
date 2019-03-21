import concurrent.futures
import time
import typing
import asyncio


class Node:
    def __init__(self, name: str) -> None:
        self._name = name
        self._children = []  # type: typing.List[Node]
        self._future = asyncio.Future()
        self._build_started = False

    def add_child(self, child: "Node") -> None:
        self._children.append(child)

    @property
    def name(self) -> str:
        return self._name

    @property
    def children(self) -> typing.List["Node"]:
        return self._children

    async def build(self, executor: concurrent.futures.Executor) -> "Node":
        await asyncio.gather(*[
            child.build(executor)
            for child in self._children
        ])
        future = executor.submit(self._internal_build)
        await asyncio.wrap_future(future)

    def _internal_build(self) -> None:
        if self._build_started:
            return
        self._build_started = True
        print(f'building {self._name}')
        time.sleep(2)


if __name__ == '__main__':
    A = Node('A')
    B = Node('B')
    C = Node('C')
    D = Node('D')
    E = Node('E')
    F = Node('F')
    G = Node('G')
    H = Node('H')

    A.add_child(B)
    A.add_child(C)
    A.add_child(G)
    A.add_child(H)

    B.add_child(D)
    B.add_child(E)
    B.add_child(F)
    C.add_child(G)
    C.add_child(H)

    _executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    asyncio.get_event_loop().run_until_complete(A.build(_executor))
