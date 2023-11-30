from django.http import JsonResponse

from django_admin_chart.chart_base import MONTHS
from django_admin_chart.chart_color import ChartColor


class ChartRender:
    months = MONTHS

    def get_year_dict(self):
        year_dict = dict()

        for month in MONTHS:
            year_dict[month] = 0

        return year_dict

    def dataset(self, data_dict, label=None, color=None):
        # print(data_dict.values())
        if not label:
            label = ""
        if not color:
            color = ChartColor.COLOR_PRIMARY
        return {
            'label': f'{label}',
            'backgroundColor': color,
            'borderColor': color,
            'data': list(data_dict.values()),
        }

    def filter(self, filter_dict):
        return JsonResponse(filter_dict)

    def chart(self, title, datasets, key, extra=None):
        return JsonResponse(
            {
                'title': f'{title}',
                'data': {
                    'labels': list(key),
                    'datasets': datasets
                },
                'extra': extra
            }
        )

    # data is an array
    def chart_pie(self, title, labels, colors, data, extra):
        return JsonResponse({
            'title': title,
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': '',
                    'backgroundColor': colors,
                    'borderColor': colors,
                    'data': data,
                }]
            },
            'extra': extra
        })
