class GameObject:
    def __init__(self, is_moving, speed, color):
        self.is_moving = is_moving
        self.speed = speed
        self.color = color

    def print_state(self):
        state = "Moving" if self.is_moving else "Standing"
        if self.is_moving:
            print(f"Object State: {state}, Speed: {self.speed} units per second, Color: {self.color}")
        else:
            print(f"Object State: {state}, Color: {self.color}")


if __name__ == "__main__":
    obj1 = GameObject(True, 5.0, "Red")
    obj2 = GameObject(False, 0.0, "Blue")

    obj1.print_state()
    obj2.print_state()
