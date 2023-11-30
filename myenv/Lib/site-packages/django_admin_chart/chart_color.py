class ChartColor:
    COLOR_PALETTE = ['#00a53a', '#81ecec', '#a29bfe', '#ffeaa7', '#fab1a0', '#ff7675', '#fd79a8']
    COLOR_PRIMARY, COLOR_SUCCESS, COLOR_DANGER = '#79aec8', COLOR_PALETTE[0], COLOR_PALETTE[5]

    @staticmethod
    def generate_color_palette(amount):
        palette = []

        i = 0
        while i < len(ChartColor.COLOR_PALETTE) and len(palette) < amount:
            palette.append(ChartColor.COLOR_PALETTE[i])
            i += 1
            if i == len(ChartColor.COLOR_PALETTE) and len(palette) < amount:
                i = 0

        return palette
