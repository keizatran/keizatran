import numpy as np
import pprint


class MatrixCalculator:
    def __init__(self, matrix_data):
        self.matrix_data = matrix_data
        self.validate_matrix()

    def validate_matrix(self):
        print(f"Input: {self.matrix_data}")
        if len(self.matrix_data) != 9:
            raise ValueError("List must contain nine numbers.")

    def calculate(self):
        np_3x3 = np.array(self.matrix_data).reshape(3, 3)
        cols = np.array([np_3x3[:, i] for i in range(3)])
        rows = np.array([np_3x3[i, :] for i in range(3)])
        flattened = np_3x3.flatten()

        calculations = {
            "mean": [],
            "var": [],
            "std": [],
            "max": [],
            "min": [],
            "sum": [],
        }

        for k, v in calculations.items():
            v.append([getattr(cols[i], k)() for i in range(3)])
            v.append([getattr(rows[i], k)() for i in range(3)])
            v.append([getattr(flattened, k)()][0])

        key_mapping = {
            "mean": "mean",
            "var": "variance",
            "std": "standard deviation",
            "max": "max",
            "min": "min",
            "sum": "sum",
        }

        for old_key, new_key in key_mapping.items():
            if old_key in calculations:
                calculations[new_key] = calculations.pop(old_key)

        return calculations


if __name__ == "__main__":
    # matrix_data = [*range(8)]
    matrix_data = [i for i in range(1, 12) if i % 5]
    calculator = MatrixCalculator(matrix_data)
    result = calculator.calculate()
    print(f"\nOutput:")
    pprint.pprint(result, sort_dicts=False)
