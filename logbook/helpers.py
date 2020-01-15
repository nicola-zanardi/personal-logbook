from random import choice


def get_random_border_style():
    """ Return pseudo-random tailwind border styles to be rendered by the jinja templates """
    styles = ["border-solid", "border-dashed", "border-dotted", "border-double"]
    colors = [
        "border-blue-500",
        "border-red-500",
        "border-yellow-500",
        "border-indigo-500",
        "border-orange-500",
        "border-teal-500",
        "border-purple-500",
        "border-pink-500",
        "border-pink-500",
        "border-gray-500",
    ]

    return f"{choice(styles)} {choice(colors)}"
