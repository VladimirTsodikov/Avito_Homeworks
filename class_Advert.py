from keyword import iskeyword


class JsonInit:
    def __init__(self, json: dict):
        for key, value in json.items():
            if iskeyword(key):
                key += '_'
            if not isinstance(value, dict):
                setattr(self, key, value)
            else:
                setattr(self, key, JsonInit(value))


class ColorizeMixin:
    text_color = 33  # default Yellow   # Values between 30 and 37
    text_style = 1  # default Bold   # Values between 0 and 5
    background_color = 40  # default Black   # Values between 40 and 47

    def __repr__(self) -> str:
        output = f"\033[{self.text_style};{self.text_color};"
        output += f"{self.background_color}m{self.title} | {self.price}₽"
        return output

    def repr_color_code(self, text_color: int, text_style: int, back_color: int) -> None:
        if 30 <= text_color <= 37:
            self.text_color = text_color
        if 0 <= text_style <= 5:
            self.text_style = text_style
        if 40 <= back_color <= 47:
            self.background_color = back_color


class Advert(ColorizeMixin, JsonInit):
    price = 0

    def __setattr__(self, key, value: int):
        if key == 'price' and int(value) < 0:
            raise ValueError("The price must be non-negative")
        super().__setattr__(key, value)

    def __init__(self, json: dict):
        super().__init__(json)
        if 'title' not in self.__dict__:
            raise ValueError("The ad must have a title")


if __name__ == "__main__":
    my = Advert({
        "title": "iPhone X",
        "class": "dog",
        "price": 100,
        "location": {
            "address": "город Самара, улица Мориса Тореза, 50",
            "metro_stations": ["Спортивная", "Гагаринская"]
        }
        }
    )
    print(my.class_)
    my.class_ = 'cat'
    print(my.class_)
    my.book = 'df'
    # print(my.__dict__)
    my.price = 4
    # print(my.__dict__)
    my.price = 45
    # print(my.__dict__)

    print(my)
    my.repr_color_code(31, 5, 42)
    print(my)
