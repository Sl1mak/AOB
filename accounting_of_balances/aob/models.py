from django.db import models

class User(models.Model):
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)

    def __str__(self):
        return self.username

class Table(models.Model):
    name = models.CharField(max_length = 50)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'tables')

    def __str__(self):
        return self.name

class Column(models.Model):
    name = models.CharField(max_length = 50)
    table = models.ForeignKey(Table, on_delete = models.CASCADE, related_name = 'columns')
    order = models.PositiveIntegerField(default = 0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.table.name} - {self.name}"

class Row(models.Model):
    table = models.ForeignKey(Table, on_delete = models.CASCADE, related_name = 'rows')
    created_at = models.DateTimeField(auto_now_add = True)

class Cell(models.Model):
    row = models.ForeignKey(Row, on_delete = models.CASCADE, related_name = 'cells')
    column = models.ForeignKey(Column, on_delete = models.CASCADE, related_name = 'cell_columns')
    value = models.TextField(blank = True, null = True)

    class Meta:
        unique_together = ('row', 'column')

    def __str__(self):
        return f"{self.row.table.name} - {self.row.created_at} - {self.column.name} - {self.value}"