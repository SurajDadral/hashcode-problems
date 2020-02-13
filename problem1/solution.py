from math import ceil


class Pizza:
    def __init__(self, pizzas_slice_list=[], max_slices=0):
        self.pizzas_slice_list = pizzas_slice_list
        self.pizzas_slice_list.sort(reverse=True)
        self.pizza_count = len(self.pizzas_slice_list)
        self.max_slices = max_slices
        self.sol_element_count = 0
        self.solution_list = [0 for _ in range(0, self.pizza_count)]
        self.included_elements = []
        self.exc_elements = self.pizzas_slice_list

    def getTmpSol(self, pizzas_slice_list, max_slices, sol_element_count=0):
        mid = ceil(len(pizzas_slice_list) / 2)
        l_part = pizzas_slice_list[:mid]
        r_part = pizzas_slice_list[mid:]

        if sum(l_part) < max_slices:
            max_slices -= sum(l_part)
            sol_element_count += len(l_part)
            return self.getTmpSol(r_part, max_slices, sol_element_count)
        elif len(r_part) != 0:
            return self.getTmpSol(l_part, max_slices, sol_element_count)
        else:
            self.solution_list[0:sol_element_count] = [1] * sol_element_count
            self.sol_element_count = sol_element_count
            self.included_elements = self.pizzas_slice_list[
                : self.sol_element_count
            ]
            self.exc_elements = self.pizzas_slice_list[self.sol_element_count :]
            return sol_element_count

    def optimize(self):
        included_elements_sum = sum(self.included_elements)
        diff = self.max_slices - included_elements_sum
        exc_elements = self.exc_elements
        while diff > 0 and len(exc_elements) > 0:
            exc_elements = list(filter((diff).__ge__, exc_elements))
            if len(exc_elements) > 0:
                sol_element = exc_elements[0]
                sol_element_index = self.exc_elements.index(sol_element)
                self.exc_elements.pop(sol_element_index)
                self.solution_list[
                    len(self.included_elements) + sol_element_index
                ] = 1
                self.included_elements.append(sol_element)
                diff -= sol_element

    def findPizzaCombination(self):
        sol_element_count = self.getTmpSol(
            self.pizzas_slice_list, self.max_slices
        )
        self.optimize()

        max_slices = sum(self.included_elements)
        diff = self.max_slices - max_slices

        print("Included:", self.included_elements)
        print("Excluded:", self.exc_elements)
        print("Sum:", sum(self.included_elements))
        print("Sum Excluded:", sum(self.exc_elements))
        print("Diff:", diff)
        return [i for i, x in enumerate(reversed(self.solution_list)) if x == 1]


if __name__ == "__main__":
    input_files = [
        "a_example.in",
        "b_small.in",
        "c_medium.in",
        "d_quite_big.in",
        "e_also_big.in",
    ]
    with open(input_files[1], "r") as inp_file:
        lines = inp_file.readlines()

    max_slices = int(lines[0].strip().split(" ")[0])
    type_of_pizza = lines[1].strip().split(" ")
    type_of_pizza = list(map(int, type_of_pizza))

    pizza_obj = Pizza(type_of_pizza, max_slices)
    op = pizza_obj.findPizzaCombination()
    # print(op)

    with open("output.md", "w") as output_file:
        output_file.write(str(len(op)) + "\n")
        solution = list(map(lambda x: str(x) + " ", op))
        solution[-1] = solution[-1].strip()
        output_file.writelines(solution)
