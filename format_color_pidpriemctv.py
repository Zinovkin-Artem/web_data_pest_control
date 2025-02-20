import sql as bd



class Formatcolor:

    def color(self, book_adm, collor):

        format_1 = book_adm.add_format(
            {
                "border": 1,
                "font_size": 8,
                "align": "center",
                "valign": "vcenter",
                "font_name": "Arial",
                "bold": True,
                "fg_color": collor,
            }
        )
        format_1.set_shrink()

        return format_1

    @staticmethod
    def format(_predpr):
        podpis_danix_dict = {}
        val = bd.podpis_danix(_predpr)

        for i in val:
            number_cont = []
            numbers_cont = i[0].split(",")
            for j in numbers_cont:
                if "-" in j:
                    for num in range(int(j.split("-")[0]), int(j.split("-")[1]) + 1):
                        number_cont.append(num)
                elif j.isdigit():
                    number_cont.append(int(j))
                else:
                    pass
            number_cont.append(i[2])
            number_cont.append(i[3])
            number_cont = tuple(number_cont)
            podpis_danix_dict[number_cont] = i[1]

        return podpis_danix_dict
