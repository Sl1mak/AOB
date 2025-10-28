from django.contrib import admin
from .models import User, Table, Row, Column, Cell

admin.site.register(User)

class ColumnsInLine(admin.TabularInline):
    model = Column
    extra = 1

class RowsInLine(admin.TabularInline):
    model = Row
    extra = 0

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    inlines = [ColumnsInLine]
    list_display = ['name']

class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'table', 'data_type', 'order')
    list_filter = ('table',)

class RowAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'created_at')

class CellAdmin(admin.ModelAdmin):
    list_display = ('row', 'column', 'value')
    list_filter = ('column',)

# Register your models here.
