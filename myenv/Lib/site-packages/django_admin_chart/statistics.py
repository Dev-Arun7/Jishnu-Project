from django_admin_chart.chart_render import ChartRender


class StatisticsData:

    def get_filter(self):
        pass

    def get_data(self, *args, **kwargs):
        pass


class StatisticsChart:
    data = None
    chart = ChartRender()

    def get_filter_chart(self, request):
        pass

    def get_data_chart(self, request):
        pass
