# Drop duplicate rows from database by Django ORM

```python
def drop_duplicates(queryset, unique_fields):
    duplicates = queryset.values(*unique_fields).annotate(
        max_id=models.Max('id'),
        count_id=models.Count('id'),
    ).order_by().filter(count_id__gt=1)

    for duplicate in duplicates:
        queryset.filter(**{x: duplicate[x] for x in unique_fields}).exclude(id=duplicate['max_id']).delete()
```

Usage example:

```python
drop_duplicates(
    SberbankCard.objects.all(),
    ('client_id', 'pan'),
)
```

Source: [StackOverflow](https://stackoverflow.com/a/13700642)

