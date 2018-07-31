from fuzzylogic import Environment

if __name__ == "__main__":
    environment = Environment()

    environment.init(1.0, 0.5, 0)
    environment.evaluate(1.2, 1.5, 1.0)
    environment.evaluate(1.4, 1.2, 1.8)
    environment.evaluate(1.4, 1.3, 1.2)
    environment.print_values()