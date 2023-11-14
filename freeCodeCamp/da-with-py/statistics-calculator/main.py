# This entrypoint file to be used in development. Start by reading README.md
from mean_var_std import MatrixCalculator
from unittest import main
import pprint

matrix_data = [i for i in range(1, 12) if i % 5]
calculator = MatrixCalculator(matrix_data)
result = calculator.calculate()
print(f"\nOutput:")
pprint.pprint(result, sort_dicts=False)

# Run unit tests automatically
main(module="test_module", exit=False)
