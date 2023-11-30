from django.contrib import admin


class ChartAdmin(admin.ModelAdmin):
    chart_url = None
    chart_url_2 = None
    chart_filter_url = None
    chart_template = None
    chart_select_filter = None

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        extra_context['url'] = self.chart_url
        # duel chart or one bar and one pie chart has 2 links
        if self.chart_url_2:
            extra_context['url2'] = self.chart_url_2

        extra_context['url_filter'] = self.chart_filter_url

        extra_context['select_filter'] = self.chart_select_filter

        self.change_list_template = self.chart_template

        return super().changelist_view(request, extra_context=extra_context)


class SingleBarChartAdmin(ChartAdmin):
    chart_template = 'django_admin_chart/one_bar_chart.html'


class DuelBarChartAdmin(ChartAdmin):
    chart_template = 'django_admin_chart/duel_bar_chart.html'


class BarAndPieChartAdmin(ChartAdmin):
    chart_template = 'django_admin_chart/one_bar_one_pie_chart.html'
    # raise ValueError('Chart filter url not found.')
