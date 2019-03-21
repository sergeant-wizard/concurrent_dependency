import concurrent.futures
import time
import typing


class Node:
    def __init__(self, name: str) -> None:
        self._name = name
        self._children = []  # type: typing.List[Node]

    def add_child(self, child: "Node") -> None:
        self._children.append(child)

    def __eq__(self, other: "Node") -> bool:
        return self._name == other._name

    def __hash__(self) -> int:
        return hash(self._name)

    @property
    def name(self) -> str:
        return self._name

    @property
    def children(self) -> typing.List["Node"]:
        return self._children

    def build(self) -> "Node":
        print(f'building {self._name}')
        time.sleep(2)
        return self


def build(executor: concurrent.futures.Executor, root: Node):
    started = set()  # type: typing.Set[Node]
    built = set()  # type: typing.Set[Node]

    def get_next_task(node: Node) -> typing.Optional[Node]:
        if node in started:
            return None
        elif set(node.children).issubset(built):
            return node
        else:
            for child in node.children:
                _next_task = get_next_task(child)
                if _next_task is not None:
                    return _next_task
            return None

    def on_done(future: concurrent.futures.Future):
        built.add(future.result())

    while root not in built:
        next_task = get_next_task(A)
        if next_task is not None:
            _future = executor.submit(next_task.build)
            started.add(next_task)
            _future.add_done_callback(on_done)


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

    _executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    build(_executor, A)
