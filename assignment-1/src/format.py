def my_decorator(msg):
    def warp(name):
        name=name.capitalize()
        return msg(name)
    return warp
def u_decorator(msg):
    def warp(name):
        print("********")
        result = msg(name)
        print(f"❤️❤️💕{result}💕❤️❤️")
        print("********")

        return result
    return warp
@u_decorator
@my_decorator
def message(name):
    return name
promt=input("Enter your message here:-")
message(promt)

