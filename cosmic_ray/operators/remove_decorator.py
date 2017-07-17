from .operator import Operator


class RemoveDecorator(Operator):
    """An operator that removes each of the non standard decorators."""
    REGULAR_DECORATORS = frozenset(["classmethod", "staticmethod",
                                    "abstractmethod"])

    @classmethod
    def _skip_decorator(cls, node):
        """Determine if a decorator node should not be mutated.
        """
        return hasattr(node, 'id') and node.id in cls.REGULAR_DECORATORS

    def visit_FunctionDef(self, node):  # noqa
        decorator_candidates = [x for x in node.decorator_list
                                if not self._skip_decorator(x)]
        if decorator_candidates:
            return self.visit_mutation_site(node, len(decorator_candidates))

        return node

    def mutate(self, node, idx):
        """Modify the decorator list to remove one decorator at each mutation"""
        candidates = [(i, d) for (i, d) in enumerate(node.decorator_list)
                      if not self._skip_decorator(d)]
        remove_idx, _ = candidates[idx]
        del node.decorator_list[remove_idx]
        return node
