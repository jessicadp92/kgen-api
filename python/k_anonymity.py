from collections import defaultdict

class KAnonymity:
    MIN_K = 2

    def __init__(self, dataset):
        self.dataset = dataset
        self.upper_bounds = dataset.compute_upper_bounds()
        self.lower_bounds = dataset.compute_lower_bounds()
        self._cache = {}

    def is_k_anonymous(self, levels, k=MIN_K, suppression_threshold=0.0) -> bool:
        key = tuple(levels)

        if key in self._cache:
            report = self._cache[key]
        else:
            report = self._run(levels, k)
            self._cache[key] = report

        return (
            report["k_after_suppression"] >= k and
            report["suppression_ratio"] <= suppression_threshold
        )

    def _run(self, levels, k):
        generalized = self.dataset.generalize_dataset(levels)
        groups = defaultdict(list)

        for idx, row in enumerate(generalized):
            qi_key = tuple(row[name] for name in self.dataset.qi_names)
            groups[qi_key].append(idx)

        class_sizes = [len(v) for v in groups.values()]
        k_value = min(class_sizes) if class_sizes else 0

        rows_to_suppress = []
        for rows in groups.values():
            if len(rows) < k:
                rows_to_suppress.extend(rows)

        suppression_ratio = len(rows_to_suppress) / self.dataset.size if self.dataset.size else 0

        if rows_to_suppress:
            remaining_sizes = [len(rows) for rows in groups.values() if len(rows) >= k]
            k_after = min(remaining_sizes) if remaining_sizes else 0
        else:
            k_after = k_value

        return {
            "k": k_value,
            "k_after_suppression": k_after,
            "suppression_ratio": suppression_ratio,
            "rows_to_suppress": rows_to_suppress
        }