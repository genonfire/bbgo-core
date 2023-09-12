import xlsxwriter

from io import BytesIO
from string import ascii_uppercase

from django.http import HttpResponse
from django.utils import timezone

from core.viewsets import (
    ReadOnlyModelViewSet,
)
from utils.constants import Const
from utils.debug import Debug


class ExcelViewSet(ReadOnlyModelViewSet):
    filename_prefix = 'excel'
    column_width = []
    title = []
    header_format = {
        'border': 1,
        'bg_color': '#CAC0D9',
        'bold': True,
        'text_wrap': True,
        'align': 'center',
        'valign': 'vcenter',
    }
    content_format = {
        'border': 1,
        'text_wrap': True,
        'align': 'center',
        'valign': 'vcenter',
    }
    merge_format = {
        'border': 1,
        'bg_color': '#F2F2F2',
        'text_wrap': True,
        'align': 'center',
        'valign': 'top',
    }
    merge_cells = []
    sheet_names = []
    sheet_keys = []

    def get_queryset(self):
        return self.model.objects.all()

    def get_sheet_name(self, instance=None):
        return 'sheet1'

    def get_filename(self):
        filename = '%s_%s.xlsx' % (
            self.filename_prefix,
            timezone.localtime().strftime(
                Const.EXCEL_FILENAME_FORMAT
            ),
        )
        return 'filename=' + filename

    def get_not_null(self, item):
        if item:
            return item
        else:
            return ''

    def make_data(self, instance=None):
        data = [
            self.title
        ]
        format_data = [
            self.header_format
        ]
        return data, format_data

    def set_sheets(self, request, data=None, one_data=None):
        self.sheet_names = [
            'sheet'
        ]
        self.sheet_keys = [
            data
        ]

    def merge(self, workbook, worksheet, data):
        for merge_cell in self.merge_cells:
            merge_format = workbook.add_format(
                merge_cell.get('format', self.merge_format)
            )
            columns = merge_cell.get('columns')
            content = merge_cell.get('content')
            worksheet.merge_range(columns, content, merge_format)

    def set_column_width(self, worksheet):
        for index, column in enumerate(ascii_uppercase):
            if index < len(self.column_width):
                worksheet.set_column(
                    column + ':' + column, self.column_width[index]
                )

    def make_excel(self, request, serializer, one_data=None):
        self.sheet_names = []
        self.sheet_keys = []
        self.set_sheets(request, serializer.data, one_data)

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)

        for index, sheet_name in enumerate(self.sheet_names):
            data, format_data = self.make_data(
                self.sheet_keys[index],
                index
            )
            if data:
                worksheet = workbook.add_worksheet(sheet_name)
                self.set_column_width(worksheet)

                for row, (columns, row_format) in enumerate(
                    zip(data, format_data)
                ):
                    for column, cell_data in enumerate(columns):
                        content_format = workbook.add_format(row_format)
                        worksheet.write(
                            row, column, cell_data, content_format
                        )
                if index == 0:
                    self.merge(workbook, worksheet, data)

        workbook.close()
        output.seek(0)
        return output

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return self.get_response(
            self.make_excel(request, serializer),
            serializer.data
        )

    def list(self, request, *args, **kwargs):
        self.q = request.query_params.get(Const.QUERY_PARAM_SEARCH)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return self.get_response(
            self.make_excel(request, serializer),
            serializer.data
        )

    def retrieve_list(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_serializer = self.set_serializer(
            self.instance_serializer,
            instance
        )
        queryset = self.filter_queryset(self.get_list_queryset(instance))
        serializer = self.get_serializer(queryset, many=True)

        return self.get_response(
            self.make_excel(request, serializer, instance_serializer.data),
            serializer.data
        )

    def get_response(self, excel, data=None):
        filename = self.get_filename()
        response = HttpResponse(excel, content_type=Const.MIME_TYPE_XLSX)
        response['Content-Disposition'] = 'attachment; ' + filename
        Debug.trace('Exporting excel %s' % filename)
        return response
